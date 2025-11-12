# Team Armadillo Enterprise Ready AI
**IBM AI Experiential Learning Lab 2025**

This repository contains the final submission materials for the *Enterprise-Ready AI* project built entirely within IBM watsonx.ai. The solution demonstrates programmatic access to Granite foundation models, risk evaluation logic, and compliance logging for governance.

## Quick Start

The project can be experienced in two complementary ways:

* **Guided walkthrough for non-technical stakeholders** – ideal if you want to understand the
  purpose of the agent, review generated artifacts, or present the prototype to decision makers.
* **Hands-on setup for technical contributors** – follow this path if you plan to run the agent,
  modify prompts, or integrate it into other systems.

### Guided walkthrough (non-technical)
1. Review the business problem and outcomes in the [Project Scope](#project-scope) section below.
2. Open the `/data` folder to review the example policy dataset (`sample_bank_policy.csv`) and a
   sample generated summary (`bank_policy_summary.json`).
3. Browse the `notebooks/` directory to see the step-by-step experimentation history. Each notebook
   includes headings that describe the objective of the experiment and links to the generated
   outputs so you can follow the story without executing any code.
4. Share feedback with the technical team using the questions in the
   [Validation & Next Steps](#validation--next-steps) checklist.

### Hands-on setup (technical)
1. Ensure you are using Python 3.11 or newer. We recommend creating a virtual environment with
   `python -m venv .venv` followed by `source .venv/bin/activate` (Linux/macOS) or
   `.venv\Scripts\activate` (Windows).
2. Install dependencies with `pip install -r requirements.txt` from the repository root.
3. Obtain an IBM Cloud API key with access to watsonx.ai and export it:
   * Linux/macOS: `export IBM_API_KEY="<your-key>"`
   * Windows PowerShell: `$Env:IBM_API_KEY="<your-key>"`
   Optionally set `WATSONX_URL`, `PROJECT_ID`, and `SPACE_ID` to target a specific deployment.
4. Run the refactored command line entry point:
   ```bash
   PYTHONPATH=src python -m scripts.run_agent "How should I evaluate a mortgage refinance in Texas?"
   ```
5. Inspect `/data` for generated risk summaries and governance logs. New outputs are timestamped so
   you can trace each run.

### Validation & Next Steps
- **Non-technical reviewers**: Capture business feedback by answering:
  - Does the generated risk narrative match the language expected by compliance teams?
  - Are the governance logs sufficient for audit trails?
  - What additional policy types should be evaluated next?
- **Technical contributors**: Log follow-up tasks such as adjusting prompt templates,
  integrating with downstream systems, or containerizing the CLI.

## Project Scope
- Industry: **Banking**
- Challenge: AI-assisted risk analysis of loan and policy documentation
- Model: **Granite 13B Instruct**
- Environment: **watsonx.ai Jupyter Notebook**

## Structure
- `src/agent_lab` — Reusable Python package extracted from the original notebook
- `/notebooks` — Archived Jupyter notebooks used during experimentation
- `/scripts` — Helper functions for authentication & governance plus the CLI wrapper
- `/data` — Policy samples and model outputs

## Dependencies

These packages are installed automatically during the [hands-on setup](#hands-on-setup-technical).

```
requests
pandas
ibm-watsonx-ai
langchain-ibm
langgraph
```
