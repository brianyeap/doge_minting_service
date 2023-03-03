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
        print(response.text)


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
        print(response.text)


# for filename in os.listdir(WALLETS_FOLDER_PATH):
#     if filename.endswith('.json'):
#         with open(os.path.join(WALLETS_FOLDER_PATH, filename), 'r') as f:
#             wallet_data = json.load(f)
#             print(wallet_data)

mint_nft(f'{IMAGES_FOLDER_PATH}/1.png')

query_bal(f"{WALLETS_FOLDER_PATH}/wallet_1276373877.json")