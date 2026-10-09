# Core Agency Automation Pipeline

## Problem
Agencies spend hours after client kickoff calls manually extracting briefs, provisioning Google Drive folders, drafting Scope of Work (SOW) docs, calculating task estimates, scheduling employee workflows, and generating Purchase Orders.

## Solution
An end-to-end automated n8n pipeline powered by AI (Anthropic & OpenAI) and Fireflies.ai that automatically handles transcript extraction, folder provisioning, SOW drafting, estimate calculation, employee workflow scheduling, and PO generation.

## Tech Stack
- **Automation**: n8n (`https://n8n.vkapsprojects.com`)
- **AI Models**: Anthropic (Claude 3.5 Sonnet / Haiku), OpenAI (GPT-4 / Embeddings)
- **Integrations**: Fireflies.ai, Supabase Vector Store, PDF4me, Google Workspace (Drive, Docs, Sheets, Gmail)
- **Scripting**: Python 3

## Setup & Quickstart

```bash
# 1. Clone repository & enter directory
git clone <repository_url>
cd coreAgency

# 2. Configure environment variables
cp .env.example .env

# 3. Import all 10 workflows into n8n
python scripts/import_workflows.py
```

## Workflows Included
1. `01 FIREFLIES TRIGGER` - Meeting webhook & transcript extraction
2. `02 Brief Extraction Flow` - AI brief, scope & estimate calculation
3. `03 Client Folder & Scope of Work` - Google Drive & SOW doc provisioning
4. `04 Timeline Doc Generation` - Project timeline & milestone generation
5. `05 Pre Approval Tasks` - Pre-approval check & estimate setup
6. `06 Job Approval & PO Generation` - PO doc generation upon approval
7. `07 Employee Workflow Scheduling` - Employee task assignment & scheduling
8. `08 Team Notification & Account Manager Summary Email` - Email & Slack summaries
9. `09 Continous Learning` - Feedback & knowledge optimization loop
10. `10 TRACKING` - Pipeline tracking & audit logging

## Directory Structure
```
.
├── workflows/         # 10 Exported n8n workflow JSON files
├── scripts/           # Python workflow import script (import_workflows.py)
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules for n8n & secrets
└── README.md          # Project documentation
```

## Author
- **Team**: Harsh Malviya
