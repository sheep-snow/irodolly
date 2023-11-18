#!/usr/bin/env python3

import aws_cdk as cdk
from cdk_example.cdk_example_stack import CdkExampleStack

app = cdk.App()
CdkExampleStack(app, "CdkExampleStack")

app.synth()
