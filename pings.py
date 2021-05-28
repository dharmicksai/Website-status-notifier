import os
import mysql.connector
import requests
from awsses import Email
import time
from dotenv import load_dotenv
load_dotenv()



mydb = mysql.connector.connect(
  host=os.getenv("MYSQL_DATABASE_HOST"),
  user=os.getenv('MYSQL_DATABASE_USER'),
  password=os.getenv('MYSQL_DATABASE_PASSWORD')
)
mycursor = mydb.cursor()

mycursor.execute("use websiteStatus");

while 1:

    mycursor.execute("select email,domain from subscriptions ;")
    myresult = mycursor.fetchall()
    
    emails = []
    domains = []
    
    for x in myresult:
        emails.append(x[0])
        domains.append(x[1])
    
    mycursor.execute("select domain , statusCode from lastStatus ;")
    domain_result = mycursor.fetchall()

    status = {}

    for x in domain_result:
        
        status[x[0]] = x[1]

    print(emails)
    print(domains)
    print(status)
    for i in range(len(emails)):
        email =  emails[i]
        domain = "https://"+domains[i]
        
        r = requests.get(domain)
        # print(r.status_code)
        if str(r.status_code) != status[domains[i]]:
            if r.status_code != 200 :
                subject = "Error: "+str(r.status_code)+" for "+domain
                mail = Email(subject)
                mail.body_text(r.text)
                mail.body_html(r.text)
                mail.send([email])
                mycursor.execute("update lastStatus set statusCode = %s  where domain = %s ;",(str(r.status_code) , domains[i]))
                mydb.commit()
                status[domains[i]] = r.status_code
                print(1)
            else:
                subject = " Domain: "+domain+" is up and running  "
                mail = Email(subject)
                mail.body_text(r.text)
                mail.body_html(r.text)
                mail.send([email])
                mycursor.execute("update lastStatus set statusCode = %s  where domain = %s;",(str(r.status_code),domains[i]))
                mydb.commit()
                status[domains[i]] = r.status_code
                print(2)
        # except:
        #     subject = " Domain not present "
        #     mail = Email(subject)
        #     mail.body_text(" ")
        #     mail.body_html(" ")
        #     mail.send([email])
        #     print(3)
    time.sleep(300)
