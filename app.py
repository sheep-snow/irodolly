import aws_cdk as cdk

from cdk_stacks.resize_stack import IrodollyResizeStack

app = cdk.App()
IrodollyResizeStack(app, "IrodollyFrontStack")

app.synth()
