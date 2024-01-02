import os
import json
from datetime import datetime

def refresh_tokens():
    refresh_command = "python refreshtoken.py"
    os.system(refresh_command)

    with open("tokens.txt", "r") as file:
        lines = file.readlines()
        new_access_token = lines[0].split(":")[1].strip()
        new_token_type = lines[1].split(":")[1].strip()
        new_expires_in = lines[2].split(":")[1].strip()
        new_refresh_token = lines[3].split(":")[1].strip()

    return new_access_token, new_token_type, new_expires_in, new_refresh_token

def run_get_shop_receipts(access_token, token_type, expires_in, refresh_token, shop_id):
    get_receipts_command = f"python getShopReceipts.py {access_token} {token_type} {expires_in} {refresh_token} {shop_id}"
    response = os.popen(get_receipts_command).read()

    # Check if the response is a valid JSON
    try:
        json_response = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw response: {response}")
        return

    # Get the absolute path to the current script (turbo.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the relative path within the etsygenerator app folder
    relative_path = "receipts_response.json"

    # Create the absolute path by joining script_dir and relative_path
    file_path = os.path.join(script_dir, "etsygenerator", relative_path)

    # Save the response to a JSON file within the etsygenerator app folder
    with open(file_path, "w") as json_file:
        json.dump(json_response, json_file, indent=4)

    # Redirect to the homepage after fetching data
    print("Content-type: text/html")
    print()
    print("<html><head><meta http-equiv='refresh' content='0;url=index.html'></head><body></body></html>")

def main():
    shop_id = "34038896"
    new_access_token, new_token_type, new_expires_in, new_refresh_token = refresh_tokens()

    run_get_shop_receipts(new_access_token, new_token_type, new_expires_in, new_refresh_token, shop_id)

    print("Script executed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()