from aws_cdk import Duration, Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class IrodollyFrontStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        resize_lambda = _lambda.Function(
            self,
            "ResizeHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("src"),
            handler="resize.handler",
            environment={"APP_NAME": "resizeFunction"},
            timeout=Duration.seconds(30),
            memory_size=128,
            retry_attempts=0,
        )
        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=resize_lambda,
        )
