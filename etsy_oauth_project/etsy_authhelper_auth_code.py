# etsy_authhelper_auth_code.py
import os
from dotenv import load_dotenv
from authentication import AuthHelper

# Load environment variables
load_dotenv()

etsy_keystring = os.getenv("ETSY_API_KEY")
etsy_scope = ["transactions_w", "transactions_r"]
callback_url = os.getenv("ETSY_REDIRECT_URI")
etsy_state = os.getenv("ETSY_STATE")
etsy_code_verifier = os.getenv("ETSY_CODE_VERIFIER")

# Create an instance of AuthHelper
etsy_auth = AuthHelper(etsy_keystring, callback_url, etsy_scope, etsy_code_verifier, etsy_state)

# Step 1: Get the authorization URL and state
authorization_url, state = etsy_auth.get_auth_code()

# Output the authorization URL for the user to visit
print("Please visit this URL to authorize your app:")
print(authorization_url)

# (Optional) You may want to save the state for later use

# Now, you can open the authorization URL in a browser to proceed with the authentication process.
