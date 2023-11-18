import aws_cdk as cdk

from cdk_stacks.front_stack import IrodollyFrontStack

app = cdk.App()
IrodollyFrontStack(app, "IrodollyFrontStack")

app.synth()
