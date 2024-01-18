# getShopReceipts.py

import os
import requests
import time
import sys
import json
import subprocess

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

def refresh_token(api_key, refresh_token):
    endpoint = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": api_key,
        "refresh_token": refresh_token
    }

    r = requests.post(endpoint, data=data)
    response_data = r.json()

    if 'access_token' in response_data:
        return response_data
    else:
        print("Failed to refresh access token.")
        return None

# Run refresh_token.py to obtain tokens
try:
    with open("tokens.txt", "r") as file:
        token_data = file.read()
        token = json.loads(token_data)
except (FileNotFoundError, json.JSONDecodeError):
    print("Error loading tokens. Running refresh_token.py to obtain new tokens.")
    
    # Run refresh_token.py
    subprocess.run(["python", "refreshtoken.py"])
    
    # Load tokens after running refresh_token.py
    try:
        with open("tokens.txt", "r") as file:
            token_data = file.read()
            token = json.loads(token_data)
    except FileNotFoundError:
        print("Error: Tokens not found. Please check refresh_token.py.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to decode token data. Please check refresh_token.py.")
        sys.exit(1)

def get_receipts(api_key, token, shop_id):
    # Check if the access token is expired
    if time.time() > token['expires_in']:
        # Refresh the access token
        token_response = refresh_token(api_key, token['refresh_token'])

        # Update the token with the new values
        token['access_token'] = token_response['access_token']
        token['token_type'] = token_response['token_type']
        token['expires_in'] = time.time() + float(token_response['expires_in'])
        token['refresh_token'] = token_response['refresh_token']

        print("Access Token refreshed.")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": api_key,
        "Authorization": f"{token['token_type']} {token['access_token']}",
    }

    # Fetch existing orders
    params = {"receipt_ids": ",".join(map(str, range(1, 2)))}
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/receipts"
    r = requests.get(endpoint, headers=headers, params=params)

    print("Existing Orders - Status Code:", r.status_code)
    response_content = r.text 
    print("Existing Orders - Response Content:", response_content)

    try:
        response_dict = json.loads(response_content)

        with open("existing_orders_response.json", "w", encoding="utf-8") as json_file:
            json.dump(response_dict, json_file, indent=4, ensure_ascii=False)
            print("Existing Orders - Response saved to 'existing_orders_response.json'")
    except json.JSONDecodeError as e:
        print(f"Existing Orders - Error decoding JSON: {e}")
        print("Existing Orders - Raw response:", response_content)

    # Fetch new orders
    params = {"was_paid": "true", "was_shipped": "false", "was_canceled": "false"}
    r = requests.get(endpoint, headers=headers, params=params)

    print("New Orders - Status Code:", r.status_code)
    response_content = r.text 
    print("New Orders - Response Content:", response_content)

    try:
        response_dict = json.loads(response_content)

        with open("new_orders_response.json", "w", encoding="utf-8") as json_file:
            json.dump(response_dict, json_file, indent=4, ensure_ascii=False)
            print("New Orders - Response saved to 'new_orders_response.json'")
        
        # Check if there are new orders
        if response_dict.get('count', 0) > 0:
            print("There are new orders!")

            # Save CSV file
            with open("new_orders_response.csv", "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)

                # Write header
                header = ["Order ID", "Item Name", "Quantity", "Price"]
                csv_writer.writerow(header)

                # Write rows
                for order in response_dict.get("results", []):
                    order_id = order.get("receipt_id", "")
                    item_name = order.get("title", "")
                    quantity = order.get("quantity", "")
                    price = order.get("price", "")
                    csv_writer.writerow([order_id, item_name, quantity, price])

                print("New Orders - CSV file saved successfully!")

        else:
            print("There are no new orders.")

    except json.JSONDecodeError as e:
        print(f"New Orders - Error decoding JSON: {e}")
        print("New Orders - Raw response:", response_content)
