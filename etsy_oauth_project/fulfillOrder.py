import requests
import json
import time

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

token = {
    "access_token": "593486034.Z2SqF8T0GePJAHLy4ZdC3dB7a7b9awSGUv6glySRYFHQDuTLq7PR0MeoOoHISF0-SEnTS3hwuQ9pQcHbtjhzaAaIe3",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "593486034.y70hqaPJkkLxxcnbsjcB2nupWUI4yxI2dA7kMmkPfqA_T-IkElNQn3YPw-4NJlN2dU1L5LGw8kVs9CVhPa_nGXLJJN"
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
        # Update the token information
        token.update({
            'access_token': response_data['access_token'],
            'expires_in': time.time() + response_data['expires_in']
        })
        return response_data['access_token']
    else:
        raise Exception("Token refresh failed")

def fulfill_order(api_key, token, shop_id, receipt_id, tracking_code, carrier_name):
    if time.time() > token['expires_in']:
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
receipt_id = "3135290012"
tracking_code = "6456456455555"
carrier_name = "hrvatska-posta"

fulfill_order(etsy_keystring, token, shop_id, receipt_id, tracking_code, carrier_name)
