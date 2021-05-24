from flask import Flask, request
from markupsafe import escape
from validate_email import validate_email


app = Flask(__name__)

@app.route('/')
def home():
    print(is_valid)
    return "hello world"

@app.route("/add/", methods=['GET', 'POST'])
def addWebsite():
    if request.method == 'GET':
        # Render the subscribe page.
        return {
            "form":'form'
        }
    userEmail = request.args.get('email')
    websiteRequested = request.args.get('website')
    if not userEmail or not websiteRequested:
        return {
            'status': 'failure',
            'reason': 'Post request required fields not found'
        }
    print(userEmail, websiteRequested)

    # Validates the email. No need to send an email and verify
    is_valid = validate_email(userEmail, verify=True)
    
    if(is_valid):
        # TO-DO -> Add to the database.
        return {
            'status': 'success'
        }
    else:
        return {
            'status': 'failure',
            'reason': 'Invalid email'
        }

if __name__ == '__main__':
    app.run(debug=True)