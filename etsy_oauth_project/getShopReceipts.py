import os
import requests
import time
import sys
import json

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

token = {
    "access_token": sys.argv[1],
    "token_type": sys.argv[2],
    "expires_in": float(sys.argv[3]),
    "refresh_token": sys.argv[4]
}

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
        return response_data['access_token']
    else:
        raise Exception("Token refresh failed")

def get_receipts(api_key, token, shop_id):
    if time.time() > token['expires_in']:
        token['access_token'] = refresh_token(api_key, token['refresh_token'])
        token['expires_in'] = time.time() + 3600  # Set the new expiration time

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": api_key,
        "Authorization": f"{token['token_type']} {token['access_token']}",
    }

    params = {"receipt_ids": ",".join(map(str, range(1, 7)))}

    # Endpoint with receipt_ids parameter
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/receipts"

    r = requests.get(endpoint, headers=headers, params=params)

    print("Status Code:", r.status_code)
    response_content = r.text
    print("Response Content:", response_content)

    try:
        # Attempt to load the JSON response into a Python dictionary
        response_dict = json.loads(response_content)

        # Save the response to a JSON file with indentation for better readability
        with open("receipts_response.json", "w", encoding="utf-8") as json_file:
            json.dump(response_dict, json_file, indent=4, ensure_ascii=False)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Raw response:", response_content)

# Replace the following shop_id with an actual value
shop_id = "34038896"
get_receipts(etsy_keystring, token, shop_id)