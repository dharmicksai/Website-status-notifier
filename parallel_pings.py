import os
import mysql.connector
import requests
from awsses import Email
import time
from multiprocessing import Pool
from dotenv import load_dotenv
load_dotenv()


#connecting to sql
mydb = mysql.connector.connect(
  host=os.getenv("MYSQL_DATABASE_HOST"),
  user=os.getenv('MYSQL_DATABASE_USER'),
  password=os.getenv('MYSQL_DATABASE_PASSWORD')
)

mycursor = mydb.cursor()

mycursor.execute("use websiteStatus");

#input is a tuple (email,domain)
def check_domain_mail(email_domain):
    email = email_domain[0]
    domain = "https://"+email_domain[1]
    
    r = requests.get(domain)
    # print(r.status_code)
    #check if status of domain has changed
    if str(r.status_code) != status[email_domain[1]]:
        #if domain has crashed
        if r.status_code != 200 :
            subject = "Error: "+str(r.status_code)+" for "+domain
            mail = Email(subject)
            mail.body_text(r.text)
            mail.body_html(r.text)
            mail.send([email])
            mycursor.execute("update lastStatus set statusCode = %s  where domain = %s ;",(str(r.status_code) , email_domain[1]))
            mydb.commit()
            print(1)
        #domain is working correctly
        else:
            subject = " Domain: "+domain+" is up and running  "
            mail = Email(subject)
            mail.body_text(r.text)
            mail.body_html(r.text)
            mail.send([email])
            mycursor.execute("update lastStatus set statusCode = %s  where domain = %s;",(str(r.status_code),email_domain[1]))
            mydb.commit()
            print(2)


status = {}

while 1:
    # get list of email and domain
    mycursor.execute("select email,domain from subscriptions ;")
    myresult = mycursor.fetchall()
    
    emails_domains = []
    
    for x in myresult:
        emails_domains.append(x)
    # print(emails_domains)

    #get status of each domain
    mycursor.execute("select domain , statusCode from lastStatus ;")
    domain_result = mycursor.fetchall()

    for x in domain_result:
        
        status[x[0]] = x[1]

    #create new processes to check  each domain
    pool = Pool(processes=len(emails_domains))
    pool.map(check_domain_mail , emails_domains)
   
    time.sleep(300)
