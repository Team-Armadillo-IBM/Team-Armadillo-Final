import requests


def get_iam_token(api_key: str) -> str:
    """Generate an IBM Cloud IAM token using the provided API key."""
    url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    token = response.json()["access_token"]
    print("✅ IBM Cloud IAM token generated.")
    return token
