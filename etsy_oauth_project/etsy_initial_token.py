import os
import secrets
import base64
import hashlib
from requests_oauthlib import OAuth2Session

def generate_challenge(code_verifier):
    m = hashlib.sha256(code_verifier.encode("utf-8"))
    b64_encode = base64.urlsafe_b64encode(m.digest()).decode("utf-8")
    # per https://docs.python.org/3/library/base64.html, there may be a trailing '=' - get rid of it
    return b64_encode.split("=")[0]

def get_auth_code(keystring, redirect_url, scopes, code_verifier, etsy_state):
    code_challenge = generate_challenge(code_verifier)

    oauth = OAuth2Session(etsy_keystring, redirect_uri=callback_url, scope=etsy_scope)
    authorization_url, state = oauth.authorization_url(
        "https://www.etsy.com/oauth/connect",
        state=etsy_state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    return authorization_url, state

etsy_keystring = os.getenv("ETSY_API_KEY")
etsy_scope = ["transactions_w", "transactions_r"]
callback_url = os.getenv("ETSY_REDIRECT_URI")
etsy_state = os.getenv("ETSY_STATE")
etsy_code_verifier = secrets.token_urlsafe(48)  # Generate a new code verifier

print("Generated code_verifier:", etsy_code_verifier)
print(get_auth_code(etsy_keystring, callback_url, etsy_scope, etsy_code_verifier, etsy_state))
