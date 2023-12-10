# from aws_cdk import aws_apigateway as apigw
from aws_cdk import Duration, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_event_sources as lambda_events
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_notifications as s3n
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as sns_subs
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class IrodollyResizeStack(Stack):
    """CDK Stack

    See:
        https://github.com/aws-samples/aws-cdk-examples/blob/master/python/s3-sns-sqs-lambda-chain/s3_sns_sqs_lambda_chain/s3_sns_sqs_lambda_chain_stack.py
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        LAMBDA_TIMEOUT = 60

        # dead letter queue for the upload event queue
        dlq = sqs.Queue(
            self, id="dead_letter_queue_id", retention_period=Duration.days(7)
        )
        dead_letter_queue = sqs.DeadLetterQueue(max_receive_count=1, queue=dlq)

        # s3 upload event queue
        upload_queue = sqs.Queue(
            self,
            id="sample_queue_id",
            dead_letter_queue=dead_letter_queue,
            visibility_timeout=Duration.seconds(LAMBDA_TIMEOUT * 6),
        )
        sqs_subscription = sns_subs.SqsSubscription(
            upload_queue, raw_message_delivery=True
        )
        upload_event_topic = sns.Topic(self, id="sample_sns_topic_id")
        # binds the SNS Topic to the SQS Queue
        upload_event_topic.add_subscription(sqs_subscription)

        # cost save rule for the bucket
        lifecycle_rules = [
            s3.LifecycleRule(
                enabled=True,
                expiration=Duration.days(90),
                transitions=[
                    s3.Transition(
                        storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                        transition_after=Duration.days(5),
                    ),
                    s3.Transition(
                        storage_class=s3.StorageClass.GLACIER,
                        transition_after=Duration.days(30),
                    ),
                ],
            )
        ]
        # s3 bucket as an uploading destination
        s3_bucket = s3.Bucket(
            self,
            id=f"{__name__}-sample-bucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            lifecycle_rules=lifecycle_rules,
        )
        s3_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3n.SnsDestination(upload_event_topic),
            s3.NotificationKeyFilter(prefix="uploads", suffix=".jpg"),
        )

        # role for the lambda
        resize_lambda_role = iam.Role(
            self,
            "lambdaRole",
            role_name="resize_lambda_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        resize_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaExecute")
        )
        resize_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaExecute")
        )

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/DockerImageFunction.html
        resize_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="ResizeHandler",
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/DockerImageCode.html#aws_cdk.aws_lambda.DockerImageCode.from_image_asset
            code=_lambda.DockerImageCode.from_image_asset(
                directory=".",
                cmd=["resize.handler"],
            ),
            role=resize_lambda_role,
            timeout=Duration.seconds(10),
            memory_size=512,
            retry_attempts=0,
            description="",
            environment={"APP_NAME": "resize_function"},
        )
        # This binds the lambda to the SQS Queue
        invoke_event_source = lambda_events.SqsEventSource(upload_queue)
        resize_lambda.add_event_source(invoke_event_source)
