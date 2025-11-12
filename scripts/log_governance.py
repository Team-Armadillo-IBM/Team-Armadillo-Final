import json
import os
import time


def log_governance(result: dict, folder="../data"):
    """Log AI outputs with timestamp for governance traceability."""
    os.makedirs(folder, exist_ok=True)
    filename = f"governance_{int(time.time())}.json"
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"🗂️ Governance log saved: {path}")
    return path
