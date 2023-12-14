import os
import requests

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

token = {
    "access_token": "593486034.OOGSHG-8F7QdFL4Miis3JVGgsN_44A_p_a83XLFcmLGG9IWs5uI03x9s6OnoIz186ROYXNsEYV115D29ZZSrr5eCsQ",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "593486034.d3MBLhPlVVERapCc6ubtOxtg4sCX-xQKZ9aYmW-sy9Pke98KEWsEZSxinnQKJZOEoN4cIg0vFv1REUAZE_tq0THUtZ"
}

def get_payments(api_key, token, shop_id):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": api_key,
        "Authorization": f"{token['token_type']} {token['access_token']}",
    }

    # Add payment_ids parameter with values from 1 to 10
    params = {"payment_ids": ",".join(map(str, range(1, 5)))}

    # Endpoint with payment_ids parameter
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/payments"
    
    r = requests.get(endpoint, headers=headers, params=params)

    print("Status Code:", r.status_code)
    print("Response Content:", r.text)

# Replace the following shop_id with an actual value
shop_id = "34038896"
get_payments(etsy_keystring, token, shop_id)
