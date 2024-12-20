# etsy_code_challenge_generator.py
import secrets
import base64
import hashlib

def generate_challenge(code_verifier):
    m = hashlib.sha256(code_verifier.encode("utf-8"))
    b64_encode = base64.urlsafe_b64encode(m.digest()).decode("utf-8")
    # per https://docs.python.org/3/library/base64.html, there may be a trailing '=' - get rid of it
    return b64_encode.split("=")[0]

code_verifier = secrets.token_urlsafe(48)
code_challenge = generate_challenge(code_verifier)

print("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)
