# irodolly
funcy analytics features for painting

# Environment Required

* docker service - https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script
* python 3.11
* poetry

```
$ poetry shell
$ cdk ls
```

# CDK Python

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
