import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
load_dotenv()

class Email(object):
    def __init__(self, subject):
        self.subject  = subject
        self.text = None
        self.html = None
        self.recipients = None

    def body_html(self, html):
        self.html = html

    def body_text(self, text):
        self.text = text

    def send(self, recipients):
        # recipients is an array
        self.recipients = recipients
        
        SENDER = os.getenv("SENDER_EMAIL")

        AWS_REGION = os.getenv("AWS_REGION")

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = self.text or ("Amazon SES Test (Python)\r\n"
                    "This email was sent with Amazon SES using the "
                    "AWS SDK for Python (Boto)."
                    )
                    
        # The HTML body of the email.
        BODY_HTML = self.html or """<html>
        <head></head>
        <body>
        <h1>Amazon SES Test (SDK for Python)</h1>
        <p>This email was sent with
            <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
            <a href='https://aws.amazon.com/sdk-for-python/'>
            AWS SDK for Python (Boto)</a>.</p>
        </body>
        </html>
                    """            

        CHARSET = "UTF-8"

        client = boto3.client('ses',region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': 
                        self.recipients,
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': self.subject,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            print("Error:")
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
