import os
from requests_oauthlib import OAuth2Session

# Assign values directly
etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"
callback_url = "https://eoek1zxudta6gmi.m.pipedream.net"
etsy_state = "rQsMKKb2pWnOQ-9kpja30g"
etsy_code_verifier = "uCZhFnja4SXu03ly_EY2s6hz6ugLI1dLe4bOIc29VsWMa150bMplx242vE_lRY7c"
etsy_auth_code_full = "kSEDDSL6sSvJismiEXvkxwqusnA0_vrHLgSdx7nOF4B7O8RCW5Hh6ECHb4kWUjIvlBsc3UgtcRYKEKbk8k8ft7QQK4qY_bPRywgs"



# Extract authorization code and state from the ETSY_AUTH_CODE
if etsy_auth_code_full:
    parts = etsy_auth_code_full.split('&state=')
    if len(parts) == 2:
        etsy_auth_code, etsy_auth_state = map(str.strip, parts)
    else:
        etsy_auth_code = etsy_auth_code_full
        etsy_auth_state = None
else:
    print("ETSY_AUTH_CODE not found in environment variables.")
    # Handle the error appropriately

etsy_scope = ["transactions_r","listings_r","transactions_w "]

def get_access_token(keystring, auth_code, code_verifier, redirect_url, scopes):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": keystring,
    }

    oauth = OAuth2Session(
        keystring, redirect_uri=redirect_url, scope=scopes
    )

    try:
        token = oauth.fetch_token(
            "https://api.etsy.com/v3/public/oauth/token",
            code=auth_code,
            code_verifier=code_verifier,
            include_client_id=True,
            headers=headers,
        )
        return token
    except Exception as e:
        print("Error fetching access token:", str(e))
        return None

access_token_response = get_access_token(
    etsy_keystring, etsy_auth_code, etsy_code_verifier, callback_url, etsy_scope
)

if access_token_response:
    print("Access Token:", access_token_response.get("access_token"))
    print("Token Type:", access_token_response.get("token_type"))
    print("Expires In:", access_token_response.get("expires_in"))
    print("Refresh Token:", access_token_response.get("refresh_token"))
else:
    print("Failed to obtain access token.")
