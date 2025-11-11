# Team Armadillo – watsonx.ai Granite Demo

This repository contains a minimal Python example that demonstrates how Team Armadillo can authenticate with IBM Cloud and query the Granite instruct model hosted on watsonx.ai.

## Getting started

1. Create and export the required environment variables:
   ```bash
   export IBM_API_KEY="<your-ibm-cloud-api-key>"
   # Optional: scope requests to a specific watsonx.ai project
   export WATSONX_PROJECT_ID="<your-watsonx-project-id>"
   ```
2. (Optional) Place a CSV file named `bank_policy.csv` under `../data/` relative to this repository root. If the file is missing the script falls back to a mock dataframe.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the demo script:
   ```bash
   python granite_inference.py
   ```

The script prints the IAM access token acquisition message, loads the sample data, queries the Granite model, and outputs the JSON response returned by watsonx.ai.

## Dependencies

Dependencies are tracked in `requirements.txt` so they can be installed in a reproducible environment.
