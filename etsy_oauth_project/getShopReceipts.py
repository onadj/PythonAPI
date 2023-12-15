import os
import requests
import time 

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

token = {
    "access_token": "593486034.O8c9maNFSTeXc274Pe2GxeruBiZpel7hiLGDiK3GE961_p3OX_F6qPshZmSqrdaTw3szxuCtemnoGaYhxQyZABXpOd",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "593486034.rYHz7ZKyTy-gX8hMBNxpLlU8XwyUDRbrjErUzFcn6joPZM2tH596QiuisOhaeIcMB_b74dbHA99ScTFkNnJUiaYZ7K"
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

    
    params = {"receipt_ids": ",".join(map(str, range(1, 6)))}

    # Endpoint with receipt_ids parameter
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/receipts"
    
    r = requests.get(endpoint, headers=headers, params=params)

    print("Status Code:", r.status_code)
    print("Response Content:", r.text)

# Replace the following shop_id with an actual value
shop_id = "34038896"
get_receipts(etsy_keystring, token, shop_id)
