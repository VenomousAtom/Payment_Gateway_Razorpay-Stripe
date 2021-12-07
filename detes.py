import csv

# Getting API Key Details from the Key File
def get_razorpay_details():
    with open('rzp.csv', 'r') as rzp:
        reader = csv.DictReader(rzp)
        for details in reader:
            key_id =  details["key_id"]
            key_secret =  details["key_secret"]
    return key_id, key_secret

def get_stripe_details():
    with open('stripe.csv', 'r') as rzp:
        reader = csv.DictReader(rzp)
        for details in reader:
            key_public = details["public_key"]
            key_secret = details["secret_key"]
    return key_public, key_secret