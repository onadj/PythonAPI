import os
import requests
import time 
from requests_oauthlib import OAuth2Session

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

token = {
    "access_token": "593486034.OOGSHG-8F7QdFL4Miis3JVGgsN_44A_p_a83XLFcmLGG9IWs5uI03x9s6OnoIz186ROYXNsEYV115D29ZZSrr5eCsQ",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "593486034.d3MBLhPlVVERapCc6ubtOxtg4sCX-xQKZ9aYmW-sy9Pke98KEWsEZSxinnQKJZOEoN4cIg0vFv1REUAZE_tq0THUtZ"
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

def get_shop_id(keystring, token):
    # Check if the access token is still valid
    if time.time() > token['expires_in']:
        token['access_token'] = refresh_token(keystring, token['refresh_token'])
        token['expires_in'] = time.time() + 3600  # Set the new expiration time

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": keystring,
    }

    # Create a new OAuth2Session instance
    etsy_auth = OAuth2Session(keystring, token=token)

    # Send a GET request to retrieve shop information
    r = etsy_auth.get("https://api.etsy.com/v3/application/shops?shop_name=BingusMerch", headers=headers)

    # Print the response text
    print(r.text)

get_shop_id(etsy_keystring, token)
