# How to run locally:
- Create AWS account and create an IAM user to get the access key id and secret access id.
- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration Use the link to configure AWS using python
- Make sure to change the default us-east-2 aws region in the awsses.py
- All the emails subscribing to the websites should be verified if the SES is still in the sandbox.
- The sender email should also be verified in the AWS console.
- Do ``export FLASK_APP=backend`` and run ``flask run``