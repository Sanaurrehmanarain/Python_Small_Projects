import requests
import time

BASE_URL = "https://api.mail.tm"

domain_names = requests.get(f"{BASE_URL}/domains").json()

print(domain_names)

domain = domain_names['hydra:member'][0]['domain']

username = "write you user_name"
email = f"{username}@{domain}"
password = "write your password"

print("Creating Account\n")

account = requests.post(f"{BASE_URL}/accounts", json = {
    "address": email,
    "password": password
})

if account.status_code!=201:
    print("Account creation failed!")
    exit()

token_response = requests.post(f"{BASE_URL}/token", json = {
    "address": email,
    "password": password
})

token = token_response.json()["token"]

headers = {"Authorization": f"Bearer {token}"}

print("Email created successfully, now it is ready\n", email)

print("Waiting for incoming message\n")

for i in range(30):
    inbox = requests.get(f"{BASE_URL}/messages", headers = headers).json()
    messages = inbox['hydra:member']

    if messages:
        print(f"\n {len(messages)} new emails received")
        for msg in messages:
            full_msg = requests.get(f"{BASE_URL}/messages/{msg['id']}", headers = headers).json()
            print(f"\nFrom: {full_msg['from']['address']}")
            print(f"\Subject: {full_msg['subject']}")
            print(f"\Text: \n{full_msg['text']}")
            break
    time.sleep(2)

else:
    print("No email received within 1 minute")