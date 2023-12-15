import os
from requests_oauthlib import OAuth2Session

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"

# Replace the following token dictionary with your actual Etsy OAuth token
token = {
    "access_token": "593486034.9oiAhX7VGDumboT5MubEUuLOyROrNJGuV7N__3zHaKi9B2O4JmUcOwupprBHCxkrEs5XFwVtSCDJ7R4c7kh5lbB3hW",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "593486034.8Fiz744_ikZtZAQFKN2Nt3qSq1Yfn0TmhW4sEC7fb4WYyeKlOZ9z4RZ2kmZ9IGDKs1C1FkCgYQzAavFCEjzqWEsloX"
}

def get_listings_by_shop(keystring, token, shop_id, state=None):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": keystring,
    }

    # Create a new OAuth2Session instance
    etsy_auth = OAuth2Session(keystring, token=token)

    # Define the endpoint for getting listings by shop
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings"

    # Optional: Add 'state' parameter to filter listings by state
    params = {'state': state} if state else {}

    # Send a GET request to retrieve listings
    r = etsy_auth.get(endpoint, headers=headers, params=params)

    # Print the response text
    print(r.text)

# Replace the following shop_id with an actual value
shop_id = "34038896"

# Optional: You can specify a state to filter listings (e.g., 'active', 'inactive', 'draft')
listing_state = "active"

get_listings_by_shop(etsy_keystring, token, shop_id, state=listing_state)
