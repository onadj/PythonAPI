import os
from authentication import AuthHelper

# Load environment variables
etsy_keystring = os.getenv("ETSY_CLIENT_ID")
etsy_scope = ["transactions_r","listings_r"]
callback_url = os.getenv("ETSY_REDIRECT_URI")
etsy_state = os.getenv("ETSY_STATE")
etsy_code_verifier = os.getenv("ETSY_CODE_VERIFIER")

etsy_auth = AuthHelper(etsy_keystring, callback_url, etsy_scope, etsy_code_verifier, etsy_state)

# Get the authorization URL and state
auth_url, auth_state = etsy_auth.get_auth_code()
print("Authorization URL:", auth_url)
print("State:", auth_state)

