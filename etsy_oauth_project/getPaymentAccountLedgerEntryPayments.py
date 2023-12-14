import os
from requests_oauthlib import OAuth2Session

def token_saver(token):
    # Save the updated token as needed
    pass

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

token = {
    "access_token": "593486034.OOGSHG-8F7QdFL4Miis3JVGgsN_44A_p_a83XLFcmLGG9IWs5uI03x9s6OnoIz186ROYXNsEYV115D29ZZSrr5eCsQ",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "593486034.d3MBLhPlVVERapCc6ubtOxtg4sCX-xQKZ9aYmW-sy9Pke98KEWsEZSxinnQKJZOEoN4cIg0vFv1REUAZE_tq0THUtZ"
}

def get_payment_account_ledger_entry_payments(keystring, token, shop_id, ledger_entry_ids):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": keystring,
    }

    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(keystring, token=token, auto_refresh_url=refresh_url, token_updater=token_saver)

    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/payment-account/ledger-entries/payments"
    params = {"ledger_entry_ids": ledger_entry_ids}
    
    r = etsy_auth.get(endpoint, headers=headers, params=params)
    print(r.text)

# Replace the following shop_id and ledger_entry_ids with actual values
shop_id = "34038896"
ledger_entry_ids = "comma_separated_list_of_ledger_entry_ids"
get_payment_account_ledger_entry_payments(etsy_keystring, token, shop_id, ledger_entry_ids)
