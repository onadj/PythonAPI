 # fulfillOrder.py
 
import json
import time
import requests

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"
shop_id = "34038896"
carrier_name = "hrvatska-posta"

def load_token_from_file():
    with open("tokens.txt", "r") as file:
        token_data = file.read()
        return json.loads(token_data)

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
        return response_data
    else:
        print("Failed to refresh access token.")
        return None

def fulfill_order(receipt_id, tracking_code):
    token = load_token_from_file()

    # Check if the access token is expired
    if time.time() > token['expires_in']:
        # Refresh the access token
        token_response = refresh_token(etsy_keystring, token['refresh_token'])

        # Update the token with the new values
        token['access_token'] = token_response['access_token']
        token['token_type'] = token_response['token_type']
        token['expires_in'] = time.time() + float(token_response['expires_in'])
        token['refresh_token'] = token_response['refresh_token']

        # Save the updated token to file
        with open("tokens.txt", "w") as file:
            json.dump(token, file)

        print("Access Token refreshed.")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": etsy_keystring,
        "Authorization": f"{token['token_type']} {token['access_token']}",
    }

    endpoint = f"https://api.etsy.com/v3/application/shops/{shop_id}/receipts/{receipt_id}/tracking"
    data = {
        "tracking_code": tracking_code,
        "carrier_name": carrier_name
    }

    r = requests.post(endpoint, headers=headers, data=data)

    print("Status Code:", r.status_code)
    response_content = r.text
    print("Response Content:", response_content)

    try:
        response_dict = json.loads(response_content)
        with open("fulfillment_response.json", "w", encoding="utf-8") as json_file:
            json.dump(response_dict, json_file, indent=4, ensure_ascii=False)
            print("Response saved to 'fulfillment_response.json'")
        return response_dict, r.status_code
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Raw response:", response_content)
        return {"error": "Error decoding JSON response"}, 500

# Example usage
if __name__ == "__main__":
    receipt_id = "3177513447"  # Replace with your actual receipt ID
    tracking_code = "665555666"  # Replace with your actual tracking code
    fulfill_order(receipt_id, tracking_code)
