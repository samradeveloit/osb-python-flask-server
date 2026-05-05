from typing import List
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_basicAuth(username, password, required_scopes):
    return {'test_key': 'test_value'}

def check_bearer_header(apikey, required_scopes):
    if not apikey:
        return None

    parts = apikey.split(" ", 1)
    token = parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else apikey
    if token:
        return {'uid': 'user'}
    return None

def check_bearerAuth(token):
    if token:
        return {'uid': 'user'}
    return None
