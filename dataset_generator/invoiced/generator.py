import invoiced
import string
import random
import requests

import os
curpath = os.path.abspath(os.curdir)

# https://invoiced.com/docs/api/?python#create-a-customer
client = invoiced.Client('LxSEOCWMPNVyr495J1aaUoto7oPA7GJ9')

INVOICES_FOLDER = 'invoices/pdf/'
RECEIPTS_FOLDER = 'receipts/pdf/'
STATEMENTS_FOLDER = 'statements/pdf/'

ascii = string.ascii_uppercase
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

#generate random email
domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
letters = string.ascii_lowercase[:12]

def get_one_random_domain(domains):
    return random.choice(domains)

def get_one_random_name(letters):
    return ''.join(random.choice(letters) for i in range(7))

def generate_random_emails():
    return [get_one_random_name(letters) + '@' + get_one_random_domain(domains) for i in range(10)]

def save_to_pdf(url, path):
    r = requests.get(url, stream=True)

    with open(path+'.pdf', 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)

payment_terms = ['NET 30', 'NET 14', 'NET 7']

customer_names = [random_string(random.randint(4,12)) for _ in range(50)]


for customer_name in customer_names:  # create random customer
    customer = client.Customer.create(
        name=customer_name,
        email="billing@acmecorp.com",#generate_random_emails(),
        payment_terms=payment_terms[random.randint(0,2)],
        type="company"
    )

    customer.contacts().create(
        name="{} {}".format(random_string(random.randint(4,6)), random_string(random.randint(4,7))),
        email="nancy.talty@example.com"
    )

    #print(customer.id)

    for i in range(random.randint(4,8)):  # create invoices via customers
        invoice = client.Invoice.create(
            customer=customer.id,
            payment_terms=customer.payment_terms,
            items=[
                {
                    'name': random_string(random.randint(4,18)),
                    'quantity': random.randint(1,10),
                    'unit_cost': random.randint(10,100)
                }
                for _ in range(random.randint(1,10))
            ],
            taxes=[
                {
                    'amount': 7
                }
            ]
        )
        # invoice.pdf_url
        save_to_pdf(invoice.pdf_url, os.path.join(INVOICES_FOLDER,str(invoice.id)))

        if random.randint(0,2) > 0:
            # create receipt
            receipt = client.Transaction.create(
                invoice=invoice.id,
                method="check",
                gateway_id="1450",
                amount=invoice.total
            )
            # receipt.pdf_url
            save_to_pdf(receipt.pdf_url, os.path.join(RECEIPTS_FOLDER,str(receipt.id)))

    # customer.statement_pdf_url return pdf link of customer
    save_to_pdf(customer.statement_pdf_url, os.path.join(STATEMENTS_FOLDER,str(customer.id)))

#customers, metadata = invoiced.Customer.list() #list all customer
