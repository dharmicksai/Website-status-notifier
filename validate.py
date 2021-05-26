import re
from validate_email import validate_email
import validators

# Validates the email. No need to send an email and verify    
def emailValidation(userEmail):
    return validate_email(userEmail, verify=True)


# Checks if the entered domain is valid but not if it actually exists
def isValidDomain(domain):
    if validators.domain(domain):
        return True
    return False

