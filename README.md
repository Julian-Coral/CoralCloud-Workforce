# CoralCloud Workforce
**Tagline:** Turning enterprise complexity into intelligent simplicity.
**Signature:** *Intelligent Simplicity™*
**Version:** 2025-10-18

This repository contains the **CoralCloud Workforce™** - an AI-powered agent system that automates strategic, operational, and tactical work for Coral & Cloud using Claude API.

## 🤖 The Agents

### 🧠 Strategic Agent (AI Co-Founder)
**Purpose:** Orchestrates all agents, maintains roadmap, publishes Weekly Founder Report
**Schedule:** Weekly (Fridays 4 PM UTC)
**KPIs:** ≥90% goal completion; 100% on-time reports

### 📣 Growth Agent (Marketing)
**Purpose:** Build brand awareness via daily LinkedIn content
**Schedule:** Daily (Mon-Fri 7 AM UTC)
**KPIs:** 4-5 posts/week; ≥5% engagement; +100 followers/month

### 🧾 Finance & Compliance Agent
**Purpose:** Unified UAE+NL finance tracking, runway monitoring, compliance
**Schedule:** Weekly (Mondays 9 AM UTC)
**KPIs:** 100% filing accuracy; ≥3-month runway

### 💼 Business Agent (Income)
**Purpose:** Generate revenue via consulting/freelance leads & proposals
**Schedule:** Daily (Mon-Fri 10 AM UTC)
**KPIs:** ≥5 proposals/week; ≥1 project/month

### ⚙️ Retail Intelligence Agent (SAP Retail/CAR)
**Purpose:** Create technical assets, provide SAP expertise
**Schedule:** Biweekly (Wednesdays 2 PM UTC)
**KPIs:** ≥4 deliverables/month; ≥1 project/quarter

## 📁 Structure
```
CoralCloud-Workforce/
├── agents/               # Agent configurations (YAML)
│   ├── strategic/
│   ├── growth/
│   ├── finance/
│   ├── business/
│   └── retail/
├── src/
│   └── agent_runner.py   # Python orchestrator
├── reports/              # Agent outputs (markdown)
│   ├── strategic/
│   ├── growth/
│   ├── finance/
│   ├── business/
│   ├── retail/
│   └── templates/
├── data/                 # CSV trackers
│   ├── Agent_Performance_Tracker.csv
│   ├── Finance_Tracker.csv
│   ├── Engagement_Tracker.csv
│   └── Compliance_Calendar.csv
├── .github/
│   └── workflows/        # GitHub Actions per agent
└── requirements.txt
```

## 🚀 Setup

### Prerequisites
- Python 3.11+
- Anthropic API key (Claude)
- GitHub repository with Actions enabled

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Julian-Coral/CoralCloud-Workforce.git
cd CoralCloud-Workforce
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up API key:**

For local testing:
```bash
export ANTHROPIC_API_KEY="your_key_here"
```

For GitHub Actions:
- Go to: Settings → Secrets and variables → Actions
- Add secret: `ANTHROPIC_API_KEY` with your Claude API key

### Running Agents

**Locally:**
```bash
# Run individual agents
python src/agent_runner.py strategic
python src/agent_runner.py growth
python src/agent_runner.py finance
python src/agent_runner.py business
python src/agent_runner.py retail
```

**Via GitHub Actions:**
- Agents run automatically on schedule
- Manual trigger: Actions tab → Select workflow → "Run workflow"

## 📊 How It Works

1. **Configuration:** Each agent has a `config.yaml` defining purpose, schedule, inputs, outputs, and prompts
2. **Orchestration:** `agent_runner.py` reads configs, fetches inputs, calls Claude API, saves outputs
3. **Automation:** GitHub Actions workflows trigger agents on schedule (cron)
4. **Outputs:** Agents commit markdown reports and update CSV trackers
5. **Monitoring:** Strategic Agent reviews all agent performance weekly

## ⏰ Schedules (UTC)

| Agent | Frequency | Cron | Description |
|-------|-----------|------|-------------|
| Strategic | Weekly | `0 16 * * 5` | Fridays 4 PM |
| Growth | Daily | `0 7 * * 1-5` | Mon-Fri 7 AM |
| Finance | Weekly | `0 9 * * 1` | Mondays 9 AM |
| Business | Daily | `0 10 * * 1-5` | Mon-Fri 10 AM |
| Retail | Biweekly | `0 14 * * 3` | Wednesdays 2 PM |

**Convert to your timezone:**
- 09:00 GST = 05:00 UTC
- 18:00 GST = 14:00 UTC

## 🛠️ Customization

### Adding a New Agent
1. Create `agents/<agent_name>/config.yaml`
2. Add `run_<agent_name>()` function in `src/agent_runner.py`
3. Create `.github/workflows/agent_<agent_name>_*.yml`
4. Test locally first

### Modifying Agent Behavior
Edit the agent's `config.yaml`:
- `prompts`: Change what the agent does
- `schedule`: Adjust frequency
- `inputs`/`outputs`: Add new data sources

## 📈 Monitoring

- **Weekly Founder Report:** `reports/strategic/weekly_founder_report_*.md`
- **Agent Performance:** `data/Agent_Performance_Tracker.csv`
- **GitHub Actions:** Check Actions tab for run status

## 🔒 Security

- Never commit `ANTHROPIC_API_KEY` to the repo
- Use GitHub Secrets for sensitive data
- Review agent outputs before publishing (especially LinkedIn posts)

## 📝 License

Proprietary - Coral & Cloud © 2025
