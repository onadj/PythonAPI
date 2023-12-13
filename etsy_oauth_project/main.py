# main.py
import os
from dotenv import load_dotenv
from authentication import AuthHelper

# Load environment variables
load_dotenv()

# Your Etsy API key and shared secret
etsy_api_key = os.getenv("ETSY_API_KEY")
etsy_shared_secret = os.getenv("ETSY_SHARED_SECRET")
etsy_redirect_uri = os.getenv("ETSY_REDIRECT_URI")
etsy_scope = os.getenv("ETSY_SCOPE").split() if os.getenv("ETSY_SCOPE") else None
etsy_state = os.getenv("ETSY_STATE")
etsy_code_challenge = os.getenv("ETSY_CODE_CHALLENGE")

# Update the redirect URI with the Pipedream URL
etsy_redirect_uri = "https://eokvmbi494rupln.m.pipedream.net"

# Create an instance of AuthHelper
auth_helper = AuthHelper(
    keystring=etsy_api_key,
    redirect_uri=etsy_redirect_uri,
    scopes=etsy_scope,
    state=etsy_state,
    code_challenge=etsy_code_challenge,
)

# Step 1: Get the authorization URL and state
authorization_url, state = auth_helper.get_auth_code()

# Output the authorization URL for the user to visit
print("Please visit this URL to authorize your app:")
print(authorization_url)

# Step 2: Retrieve the authorization code (You need to manually input this)
auth_code = input("Enter the authorization code from the URL: ")

# Step 3: Set the authorization code in AuthHelper
auth_helper.set_authorisation_code(auth_code, state)

# Step 4: Get the access token
access_token = auth_helper.get_access_token()

# Now you can use the access_token for your Etsy API requests
print("Access Token:", access_token)
