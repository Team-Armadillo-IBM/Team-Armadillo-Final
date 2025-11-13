# Setup & Operations Runbook

This runbook describes exactly how to stand up the Team Armadillo agent in a new environment, invoke it, and inspect the generated artifacts.

## 1. Prerequisites
- Python **3.11+**.
- Access to an **IBM Cloud** account with watsonx.ai enabled.
- API key with permission to call Granite foundation models and manage the target project/space.
- Optional: access to the `sample_bank_policy.csv` dataset so you can repeat the demo end-to-end.

## 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
```

## 3. Install dependencies
From the repository root run:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Provide credentials
The CLI relies on environment variables. Add them to your shell or `.env` file before running the agent.

| Variable | Required | Description |
| --- | --- | --- |
| `IBM_API_KEY` | ✅ | API key that is exchanged for a watsonx bearer token. |
| `WATSONX_URL` | ⛔ (defaults to `https://us-south.ml.cloud.ibm.com`) | Override when calling a different region. |
| `PROJECT_ID` | ⚠️ | Required when running in a project context. |
| `SPACE_ID` | ⚠️ | Required when targeting a deployment space. |

Only one of `PROJECT_ID` or `SPACE_ID` is needed. The CLI flags `--project-id` and `--space-id` override the environment variables during ad-hoc runs.

## 5. Run the agent
```bash
PYTHONPATH=src python -m scripts.run_agent "How should I evaluate a mortgage refinance in Texas?" \
  --vector-index-id 40824957-150a-4607-a08c-7f8885b0befa \
  --print-full-response
```
- Remove `--print-full-response` to show only the final answer.
- Replace the sample prompt with your own risk evaluation question.
- Use `--project-id`/`--space-id` when the defaults in `scripts/run_agent.py` do not match your workspace.

## 6. Inspect artifacts
- **CLI output** provides the narrative response along with credential provenance.
- **`data/`** contains timestamped summaries and governance logs emitted by the agent.
- **`notebooks/`** shows the experimentation lineage if you need to validate behavior or demo the workflow.

## 7. Troubleshooting
| Symptom | Resolution |
| --- | --- |
| `AuthenticationError: Missing IBM_API_KEY` | Confirm the variable is exported in the same shell session that runs the CLI. |
| `404 Not Found` from Granite endpoints | Ensure the `vector_index_id`, `project_id`, and `space_id` match your watsonx deployment. |
| Empty responses or timeouts | Rerun with `--print-full-response` to capture trace IDs and open a support ticket with IBM if the issue persists. |

---
Maintainers can extend this runbook with internal deployment steps (for example, containerization) without modifying the public README.
