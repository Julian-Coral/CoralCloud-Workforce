# CoralCloud Workforce
**Tagline:** Turning enterprise complexity into intelligent simplicity.  
**Signature:** *Intelligent Simplicity™*  
**Version:** 2025-10-18

This repository contains the **CoralCloud Workforce™** agent playbooks, data trackers, and automation workflows (GitHub Actions) for Coral & Cloud.

## Structure
```
CoralCloud-Workforce/
├── agents/
├── reports/
│   └── templates/
├── .github/
│   └── workflows/
├── data/
└── README.md
```

## Quick Start (Create Repo & Push)
```bash
# 1) Create repo on GitHub: CoralCloud-Workforce (empty, no README)
# 2) Initialize locally and push
git init
git branch -M main
git remote add origin https://github.com/Julian-Coral/CoralCloud-Workforce.git
git add .
git commit -m "Initial CoralCloud Workforce repo skeleton"
git push -u origin main
```

## Timezones for GitHub Actions
> GitHub Actions cron uses **UTC**.  
- 09:00 GST = **05:00 UTC**  
- 18:00 GST = **14:00 UTC**

Update crons if needed.
