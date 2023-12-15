import os
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
    os.system(get_receipts_command)

def main():
    
    shop_id = "34038896"
    new_access_token, new_token_type, new_expires_in, new_refresh_token = refresh_tokens()

    run_get_shop_receipts(new_access_token, new_token_type, new_expires_in, new_refresh_token, shop_id)

    print("Script executed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
