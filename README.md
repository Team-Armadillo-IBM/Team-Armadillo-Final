# Team Armadillo Enterprise Ready AI
**IBM AI Experiential Learning Lab 2025**

This repository contains the final submission materials for the *Enterprise-Ready AI* project built entirely within IBM watsonx.ai. The solution demonstrates programmatic access to Granite foundation models, risk evaluation logic, and compliance logging for governance.

## Quick Start
1. Install dependencies with `pip install -r requirements.txt`.
2. Set the `IBM_API_KEY` environment variable (and optionally `WATSONX_URL`, `PROJECT_ID`, `SPACE_ID`).
3. Run the refactored command line entry point:
   ```bash
   PYTHONPATH=src python -m scripts.run_agent "How should I evaluate a mortgage refinance in Texas?"
   ```
4. Inspect `/data` for generated risk summaries and governance logs.

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

```
requests
pandas
ibm-watsonx-ai
langchain-ibm
langgraph
``` 
