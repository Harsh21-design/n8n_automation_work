"""
n8n Workflow Bulk Importer (Python AI Automation Script)

Automates bulk importing of all JSON workflows from the 'workflows/' folder
into an active n8n instance via the n8n REST API.

Usage:
    python scripts/import_workflows.py
"""

import os
import sys
import json
from pathlib import Path
import urllib.request
import urllib.error

# Load environment variables from .env if python-dotenv or manual reading is available
def load_env_file():
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())

load_env_file()

# Ensure UTF-8 output encoding for Windows terminals
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Retrieve Configuration
N8N_HOST = os.getenv("N8N_HOST", "https://n8n.vkapsprojects.com").rstrip('/')
N8N_API_KEY = os.getenv("N8N_API_KEY", "")

if not N8N_HOST.startswith("http"):
    N8N_HOST = f"https://{N8N_HOST}"

if not N8N_API_KEY or N8N_API_KEY == "your_n8n_api_key_here":
    print("[ERROR] N8N_API_KEY is not set or invalid in environment/.env file.")
    print("Please set a valid N8N_API_KEY in your .env file or environment variables.")
    sys.exit(1)

WORKFLOWS_DIR = Path(__file__).resolve().parent.parent / 'workflows'

if not WORKFLOWS_DIR.exists():
    print(f"[ERROR] Workflows directory not found at {WORKFLOWS_DIR}")
    sys.exit(1)

json_files = list(WORKFLOWS_DIR.glob("*.json"))

if not json_files:
    print(f"[NOTICE] No .json workflow files found in {WORKFLOWS_DIR}")
    sys.exit(0)

print(f"[START] Found {len(json_files)} workflows to import into n8n ({N8N_HOST})...\n")

api_url = f"{N8N_HOST}/api/v1/workflows"
headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Python-n8n-Importer/1.0"
}

success_count = 0

for file_path in sorted(json_files):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            workflow_data = json.load(f)
        
        # Prepare import payload
        payload = {
            "name": workflowData.get("name", file_path.stem) if 'workflowData' in locals() else workflow_data.get("name", file_path.stem),
            "nodes": workflow_data.get("nodes", []),
            "connections": workflow_data.get("connections", {}),
            "settings": workflow_data.get("settings", {})
        }
        
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=req_data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            wf_id = res_json.get("id", "N/A")
            print(f"[SUCCESS] Imported '{payload['name']}' (ID: {wf_id})")
            success_count += 1
            
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[FAILED] '{file_path.name}' (HTTP {e.code}): {err_msg}")
    except Exception as e:
        print(f"[ERROR] '{file_path.name}': {str(e)}")

print(f"\n[DONE] Successfully imported {success_count}/{len(json_files)} workflows!")
