import time
import os
import requests
import json
import random
import threading
import base64

WALLETS_FOLDER_PATH = 'off_chain/wallets'
IMAGES_FOLDER_PATH = 'off_chain/images'


def create_wallet(count):
    url = "http://49.206.31.38:8000/api/create_user_wallet/"
    payload = json.dumps({
        "count": 1
    })
    headers = {
        'Content-Type': 'application/json'
    }

    i = 0
    while i < count:
        def temp_func():
            response = requests.request("POST", url, headers=headers, data=payload)

            # Parse the message and extract the JSON object
            parsed_message = json.loads(response.text)
            wallet_data = json.loads(parsed_message['message'])

            # Create the wallet1.json file
            with open(f'off_chain/wallets/wallet_{int(random.random() * 10 ** 10)}.json', 'w') as f:
                json.dump(wallet_data, f, indent=4)

        t = threading.Thread(target=temp_func)
        t.start()
        t.join()
        i += 1
        time.sleep(0.4)
    return 1


def query_bal(wallet_file):
    with open(wallet_file) as file:
        data = file.read()
        url = "http://49.206.31.38:8000/api/query_bal/"
        payload = json.dumps({
            "wallet_data": data
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = response.json()
        if json_data["status"] == 1:
            balance = json_data["message"].split('balance ')[1]
            return balance


def mint_nft(file_path):
    with open(file_path, "rb") as image_file:
        file_name = os.path.basename(file_path)
        encoded_string = base64.b64encode(image_file.read())

        url = "http://49.206.31.38:8000/api/mint_nft/"
        payload = json.dumps({
            "file_name": file_name,
            "base64": encoded_string.decode()
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = response.json()
        if json_data["status"] == 1:
            tx_id = json_data["message"].split('txid: ')[1]
            print(tx_id)


# for filename in os.listdir(WALLETS_FOLDER_PATH):
#     if filename.endswith('.json'):
#         with open(os.path.join(WALLETS_FOLDER_PATH, filename), 'r') as f:
#             wallet_data = json.load(f)
#             print(wallet_data)

# mint_nft(f'{IMAGES_FOLDER_PATH}/1.png')

def main():
    delete_folder = input("Delete wallet y/n?:")
    if delete_folder.lower() == 'y':
        for filename in os.listdir(WALLETS_FOLDER_PATH):
            file_path = os.path.join(WALLETS_FOLDER_PATH, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {file_path} - {e}")
        create_wallet(3)
    files = os.listdir(WALLETS_FOLDER_PATH)
    first_file = files[0]

    while True:
        balance = int(query_bal(f"{WALLETS_FOLDER_PATH}/{first_file}"))
        if balance != 0:
            print(f"Balance: {balance}")
            break
        else:
            with open(f"{WALLETS_FOLDER_PATH}/{first_file}") as file:
                address = json.loads(file.read())['address']
            print(f'Wallet Balance 0!\nSend Doge: {address}')
            input("Done?: ")
    mint_nft(f'{IMAGES_FOLDER_PATH}/1.png')


# main()

import http.client
import json


# conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
# payload = json.dumps({
#   "name": "Buy Mint Token",
#   "description": "Buy Mint token to mint NFT",
#   "pricing_type": "fixed_price",
#   "local_price": {
#     "amount": "0.1",
#     "currency": "USD"
#   },
#   "metadata": {
#     "customer_id": "brian",
#     "customer_name": "brian"
#   },
#   "redirect_url": "https://dogecoinmonkeys.web.app/"
# })
# headers = {
#   'Content-Type': 'application/json',
#   'Accept': 'application/json',
#   'X-CC-Api-Key': 'f7ed034d-f942-4c21-9f7f-af748112a019'
# }
# conn.request("POST", "/charges", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

# import http.client
# import json
#
# conn = http.client.HTTPSConnection("api.commerce.coinbase.com")
# payload = ''
# headers = {
#   'Content-Type': 'application/json',
#   'Accept': 'application/json',
#   'X-CC-Version': 'f7ed034d-f942-4c21-9f7f-af748112a019'
# }
# conn.request("GET", "/charges/FCY4QWD2", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

# create_wallet(1)
def send_funds(doge_address, quantity):
    wallet_data = {
        "privkey": "QRnp5agZ2hYUVAi9DzE1Zg4tHbJ3SpRjBippfJXCZNR8h4i6Po7Y",
        "address": "D81hfV2Gi1XVs9U6ZKLSqhvqvYmhp3Q3zJ",
        "utxos": []
    }

    url = "http://49.206.31.38:8000/api/query_bal/"
    payload = json.dumps({
        "wallet_data": str(wallet_data),
        "quantity": quantity,
        "receiver_address": doge_address
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


send_funds("DGFipFMaeatV3zbRCAx1kzrYQF3wqsiUmS", 0.1)



files = os.listdir(WALLETS_FOLDER_PATH)
first_file = files[0]

print(query_bal(f"{WALLETS_FOLDER_PATH}/{first_file}"))
