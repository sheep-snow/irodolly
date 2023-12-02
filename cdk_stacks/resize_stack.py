# from aws_cdk import aws_apigateway as apigw
from aws_cdk import Duration, Stack, aws_iam
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class IrodollyResizeStack(Stack):
    """_summary_

    Args:
        Stack (_type_): _description_
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        resize_lambda_role = aws_iam.Role(
            self,
            "lambdaRole",
            role_name="resize_lambda_role",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        resize_lambda_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaExecute")
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
            memory_size=128,
            retry_attempts=0,
            environment={"APP_NAME": "resize_function"},
        )
