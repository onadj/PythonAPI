import requests
import json
import time

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

def load_token_from_file():
    with open("tokens.txt", "r") as file:
        lines = file.readlines()

    token = {}

    for line in lines:
        key, value = line.strip().split(": ")
        # Map the loaded keys to the correct keys used in the script
        key_mapping = {
            'Access Token': 'access_token',
            'Token Type': 'token_type',
            'Expires In': 'expires_in',
            'Refresh Token': 'refresh_token'
        }
        corrected_key = key_mapping.get(key, key)
        if corrected_key == "expires_in":
            value = float(value)  # Convert expires_in to float
        token[corrected_key] = value

    return token

# Load token from file
token = load_token_from_file()

print("Loaded token:", token)

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
        # Update the token information
        token.update({
            'access_token': response_data['access_token'],
            'expires_in': time.time() + response_data['expires_in']
        })
        return response_data['access_token']
    else:
        raise Exception("Token refresh failed")

def fulfill_order(api_key, token, shop_id, receipt_id, tracking_code, carrier_name):
    print("Token before checking expiration:", token)
    if 'expires_in' not in token:
        print("Warning: 'expires_in' not found in token.")
        return

    if time.time() > float(token['expires_in']):
        token['access_token'] = refresh_token(api_key, token['refresh_token'])

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": api_key,
        "Authorization": f"{token['token_type']} {token['access_token']}",
    }

    # Form a valid URL for createReceiptShipment
    endpoint = f"https://api.etsy.com/v3/application/shops/{shop_id}/receipts/{receipt_id}/tracking"

    # Build the request body
    data = {
        "tracking_code": tracking_code,
        "carrier_name": carrier_name
    }

    # Execute a createReceiptShipment POST request
    r = requests.post(endpoint, headers=headers, data=data)

    print("Status Code:", r.status_code)
    response_content = r.text
    print("Response Content:", response_content)

    try:
        response_dict = json.loads(response_content)
        with open("fulfillment_response.json", "w", encoding="utf-8") as json_file:
            json.dump(response_dict, json_file, indent=4, ensure_ascii=False)
            print("Response saved to 'fulfillment_response.json'")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Raw response:", response_content)

# Replace the following values with actual data
shop_id = "34038896"
receipt_id = "3168059268"
tracking_code = "45645865444333"
carrier_name = "hrvatska-posta"

fulfill_order(etsy_keystring, token, shop_id, receipt_id, tracking_code, carrier_name)
