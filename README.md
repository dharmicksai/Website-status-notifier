# How to run locally:
- Create AWS account and create an IAM user to get the access key id and secret access id.
- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration Use the link to configure AWS using python
- Make sure to change the default us-east-2 aws region in the awsses.py
- All the emails subscribing to the websites should be verified if the SES is still in the sandbox.
- The sender email should also be verified in the AWS console.
- Install all the dependencies mentioned in requirements.txt
- Insert all the required keys in .env file
- Make sure ``~/.aws/credentials`` and ``~/.aws/config`` are there and contains all the required keys.
- Do ``export FLASK_APP=backend`` and run ``flask run`` to start the backend server.


## .env Template
```
MYSQL_DATABASE_USER=
MYSQL_DATABASE_PASSWORD=
MYSQL_DATABASE_HOST=
SENDER_EMAIL=
AWS_REGION=
```

## DB init
- ``CREATE TABLE subscriptions(id INT NOT NULL AUTO_INCREMENT, domain varchar(50), email varchar(50), PRIMARY KEY (id));``
- ``CREATE TABLE lastStatus(domain varchar(30), statusCode varchar(3), PRIMARY KEY (domain));``


## Technologies used:
- AWS SES for Emails
- Flask as backend
- MySQL for database.