# Team Armadillo — Enterprise Ready AI
**IBM AI Experiential Learning Lab 2025**

This repository contains the final submission materials for the *Enterprise-Ready AI* project built entirely within IBM watsonx.ai. The solution demonstrates programmatic access to Granite foundation models, risk evaluation logic, and compliance logging for governance.

## Quick Start
1. Open this repo in **IBM watsonx.ai (Dallas region)**.
2. Add your IBM Cloud API key under `IBM_API_KEY` in the notebook.
3. Run all cells in `notebooks/enterprise_ready_ai.ipynb`.
4. Check `/data` for generated risk summaries and governance logs.

## Project Scope
- Industry: **Banking**
- Challenge: AI-assisted risk analysis of loan and policy documentation
- Model: **Granite 13B Instruct**
- Environment: **watsonx.ai Jupyter Notebook**

## Structure
- `/notebooks` — Main Jupyter notebook
- `/scripts` — Helper functions for authentication & governance
- `/data` — Policy samples and model outputs

## Dependencies

```
pip install -r requirements.txt
```

```
requests
pandas
ibm-watsonx-ai
```
