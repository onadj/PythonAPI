import os
from authentication import AuthHelper

# Load environment variables
etsy_keystring = os.getenv("ETSY_CLIENT_ID")
etsy_scope = ["transactions_r", "listings_r", "transactions_w"]
callback_url = os.getenv("ETSY_REDIRECT_URI")
etsy_state = os.getenv("ETSY_STATE")
etsy_code_verifier = os.getenv("ETSY_CODE_VERIFIER")
auth_code = os.getenv("ETSY_AUTHORIZATION_CODE")

# If auth code is not present in the environment variable, get it interactively
if auth_code is None:
    etsy_auth = AuthHelper(etsy_keystring, callback_url, etsy_scope, etsy_code_verifier, etsy_state)

    # Get the authorization URL and state
    auth_url, state = etsy_auth.get_auth_code()
    print("Authorization URL:", auth_url)

    # Wait for user input to get the auth code
    auth_code = input("Enter the authorization code: ")

    # Save the obtained auth code to the environment variable for future use
    os.environ["ETSY_AUTHORIZATION_CODE"] = auth_code

# Continue with the rest of your script
etsy_auth = AuthHelper(etsy_keystring, callback_url, etsy_scope, etsy_code_verifier, etsy_state)
etsy_auth.set_authorisation_code(auth_code, state)  # Pass 'state' here

# Exchange authorization code for access token
token_response = etsy_auth.get_access_token()
if token_response:
    print("Access Token:", token_response['access_token'])
    print("Token Type:", token_response['token_type'])
    print("Expires In:", token_response['expires_in'])
    print("Refresh Token:", token_response['refresh_token'])

    # Save tokens to a text file
    with open("tokens.txt", "w") as file:
        file.write(f"Access Token: {token_response['access_token']}\n")
        file.write(f"Token Type: {token_response['token_type']}\n")
        file.write(f"Expires In: {token_response['expires_in']}\n")
        file.write(f"Refresh Token: {token_response['refresh_token']}\n")

    print("Tokens saved to tokens.txt.")
else:
    print("Failed to obtain access token.")
