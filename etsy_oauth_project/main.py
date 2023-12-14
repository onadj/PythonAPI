# main.py
from authentication import EtsyAuthenticator

def main():
    authenticator = EtsyAuthenticator()
    access_token = authenticator.get_access_token()
    
    # Use the access token to make Etsy API calls or perform other tasks
    print("Access Token:", access_token)

if __name__ == "__main__":
    main()
