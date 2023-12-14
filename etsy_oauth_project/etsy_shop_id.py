import os
from requests_oauthlib import OAuth2Session

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

token = {
    "access_token": "593486034.OOGSHG-8F7QdFL4Miis3JVGgsN_44A_p_a83XLFcmLGG9IWs5uI03x9s6OnoIz186ROYXNsEYV115D29ZZSrr5eCsQ",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "593486034.d3MBLhPlVVERapCc6ubtOxtg4sCX-xQKZ9aYmW-sy9Pke98KEWsEZSxinnQKJZOEoN4cIg0vFv1REUAZE_tq0THUtZ"
}

def get_shop_id(keystring, token):
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
