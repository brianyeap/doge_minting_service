import time
import os
import requests
import json
import random
import threading

WALLETS_FOLDER_PATH = 'off_chain/wallets'


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


for filename in os.listdir(WALLETS_FOLDER_PATH):
    if filename.endswith('.json'):
        with open(os.path.join(WALLETS_FOLDER_PATH, filename), 'r') as f:
            wallet_data = json.load(f)
            print(wallet_data)
