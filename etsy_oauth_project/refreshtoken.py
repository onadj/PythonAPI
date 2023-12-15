import os
import requests

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"
refresh_token = "593486034.wa2UO-9w2FBjrqY22M28zP7gT5SI2xMqBCqU9kdGiHUoSlCwjE2WWZpPgZVlOtGe5j8W6HX4tyg2xPdqmMDE2r8sHl"

def refresh_access_token(api_key, refresh_token):
    endpoint = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": api_key,
        "refresh_token": refresh_token
    }

    r = requests.post(endpoint, data=data)
    response_data = r.json()

    if 'access_token' in response_data:
        return response_data
    else:
        print("Failed to refresh access token.")
        return None

# Refresh the access token
new_token_response = refresh_access_token(etsy_keystring, refresh_token)

if new_token_response:
    print("New Access Token:", new_token_response['access_token'])
    print("Token Type:", new_token_response['token_type'])
    print("Expires In:", new_token_response['expires_in'])
    print("New Refresh Token:", new_token_response['refresh_token'])

    # Save tokens to a text file
    with open("tokens.txt", "w") as file:
        file.write(f"Access Token: {new_token_response['access_token']}\n")
        file.write(f"Token Type: {new_token_response['token_type']}\n")
        file.write(f"Expires In: {new_token_response['expires_in']}\n")
        file.write(f"Refresh Token: {new_token_response['refresh_token']}\n")

    print("Tokens saved to tokens.txt.")
else:
    print("Failed to obtain a new access token.")
