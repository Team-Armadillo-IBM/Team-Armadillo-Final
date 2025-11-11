"""Example script for querying IBM's Granite instruct model via watsonx.ai."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR.parent / "data" / "bank_policy.csv"
IBM_API_KEY = os.getenv("IBM_API_KEY")


def get_iam_token(api_key: str) -> str:
    """Fetch an IAM access token for the provided IBM Cloud API key."""
    url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers, timeout=30)
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()
    return payload["access_token"]


def load_sample_data(path: str | None = None) -> pd.DataFrame:
    """Load the demo CSV file if it exists, otherwise create a mock dataframe."""
    resolved_path = Path(path) if path is not None else DEFAULT_DATA_PATH

    if resolved_path.exists():
        df = pd.read_csv(resolved_path)
        print(f"✅ Bank policy dataset loaded: {df.shape}")
        return df

    print("⚠️ No dataset found — using mock sample.")
    return pd.DataFrame({"Policy": ["Loan approval threshold", "Risk governance"]})


def query_granite(prompt: str, access_token: str, model_id: str = "ibm-granite-13b-instruct") -> Dict[str, Any]:
    """Call the watsonx.ai text generation endpoint with the supplied prompt."""
    endpoint = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model_id": model_id,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 256,
            "min_new_tokens": 1,
            "stop": ["\n\n"],
            "temperature": 0.5,
        },
        "project_id": os.getenv("WATSONX_PROJECT_ID"),
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    return response.json()


def main() -> None:
    if not IBM_API_KEY:
        raise RuntimeError("Set the IBM_API_KEY environment variable before running the script.")

    access_token = get_iam_token(IBM_API_KEY)
    print("✅ IBM Cloud IAM token acquired.")

    df = load_sample_data()

    policy_text = df.iloc[0, 0] if not df.empty else "General risk management guidance"
    sample_prompt = (
        "Summarize the following policy in plain language:\n\n"
        f"Policy: {policy_text}"
    )
    result = query_granite(sample_prompt, access_token)
    print("✅ Granite model response received.")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
