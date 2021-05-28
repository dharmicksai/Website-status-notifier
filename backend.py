from flask import Flask, request ,render_template
from markupsafe import escape
from awsses import Email
import os
from validate import emailValidation, isValidDomain
from flaskext.mysql import MySQL
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
mysql = MySQL()
print(os.getenv('MYSQL_DATABASE_USER'))
print(os.getenv('MYSQL_DATABASE_PASSWORD'))
print(os.getenv("MYSQL_DATABASE_HOST"))

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = 'websiteStatus'
app.config['MYSQL_DATABASE_HOST'] = os.getenv("MYSQL_DATABASE_HOST")

mysql.init_app(app)


@app.route('/')
def home():
    return "Home"


@app.route("/add/", methods=['GET', 'POST'])
def addWebsite():
    if request.method == 'GET':
        # Render the subscribe page.
        return render_template("form.html")

    #print(request)
    
    userEmail = request.form['email'].lower()
    websiteRequested = request.form['website'].lower()
    print(userEmail + "    " + websiteRequested)
    # Entered email and webiste are None
    if not userEmail or not websiteRequested:
        return {
            'status': 'failure',
            'reason': 'Post request required fields not found'
        }

    # Entered email is not None but it is invalid
    if not emailValidation(userEmail):
        return {
            'status': 'failure',
            'reason': 'Entered email is invalid'
        }

    if not isValidDomain(websiteRequested):
        return {
            'status': 'failure',
            'reason': 'Entered domain is invalid'
        }

    conn = mysql.connect()
    cursor = conn.cursor()

    print(userEmail, websiteRequested)
    
    # Primary key is domain itself in lastStatus
    try:
        cursor.execute("INSERT INTO lastStatus(domain) VALUES (%s)", (websiteRequested,))
    except:
        print("The domain already exists in the lastStatus table")


    # Primary key in subscriptions is id, need to avoid duplicate entries
    cursor.execute("SELECT * FROM subscriptions where email = %s and domain = %s", (userEmail, websiteRequested))
    if cursor.fetchone():
        conn.commit()
        conn.close()
        return {
            'status': 'success'
        }
    
    cursor.execute("INSERT INTO subscriptions (email, domain) VALUES (%s, %s)", (userEmail, websiteRequested))
    conn.commit()
    conn.close()

    email = Email('New subscription')
    email.body_text('Testing AWS SES')
    html = """<html>
    <head></head>
    <body>
    <h1>New subcription to our service</h1>
    <p>Thank you for subscribing to the website
        <a href='{websiteRequested}'>{websiteRequested}</a>.
    You will be receiving the status of website every five minutes.
    </body>
    </html>
    
    """.format(websiteRequested=websiteRequested)
    email.body_html(html)
    email.send([userEmail])

    return {
        'status': 'success'
    }


if __name__ == '__main__':
    app.run(debug=True)