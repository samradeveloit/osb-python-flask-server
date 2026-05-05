import os

import jwt


IBM_IAM_ISSUER = "https://iam.cloud.ibm.com/identity"
IBM_IAM_JWKS_URL = os.environ.get("IBM_IAM_JWKS_URL", "https://iam.cloud.ibm.com/identity/keys")
BROKER_CRN = os.environ.get("BROKER_CRN", "")
JWK_CLIENT = jwt.PyJWKClient(IBM_IAM_JWKS_URL)


def _normalize_crn(value):
    if not value:
        return ""
    if value.startswith("crn-crn:"):
        return value[len("crn-"):]
    return value


def check_bearer_crn(apikey, required_scopes):
    if not apikey or not BROKER_CRN:
        return None

    parts = apikey.split(" ", 1)
    token = parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else apikey
    if not token:
        return None

    signing_key = JWK_CLIENT.get_signing_key_from_jwt(token)
    claims = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=IBM_IAM_ISSUER,
        options={"verify_aud": False},
    )

    expected_crn = _normalize_crn(BROKER_CRN)
    token_identities = {
        _normalize_crn(claims.get("id")),
        _normalize_crn(claims.get("iam_id")),
    }

    if expected_crn not in token_identities:
        return None

    return {
        "uid": expected_crn,
        "token": claims,
    }
