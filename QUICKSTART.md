# CoralCloud Workforce - Quick Start Guide

This guide will help you get your AI workforce up and running in 15 minutes.

## ✅ Checklist

- [ ] Python 3.11+ installed
- [ ] Anthropic API account & key
- [ ] GitHub repository access
- [ ] 15 minutes

## 📦 Step 1: Install Dependencies

```bash
# Clone the repo (if not already done)
git clone https://github.com/Julian-Coral/CoralCloud-Workforce.git
cd CoralCloud-Workforce

# Install Python dependencies
pip install -r requirements.txt
```

## 🔑 Step 2: Set Up Claude API Key

### Get Your API Key
1. Go to: https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to: API Keys
4. Create a new key and copy it

### Add to GitHub Secrets
1. Go to your repo: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: [paste your key]
5. Click "Add secret"

### For Local Testing
```bash
# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-api03-..."

# Or create a .env file (add .env to .gitignore!)
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." > .env
```

## 🧪 Step 3: Test an Agent Locally

```bash
# Test the Growth Agent (fastest to run)
python src/agent_runner.py growth

# Check the output
ls -la reports/growth/

# Read the generated LinkedIn post
cat reports/growth/linkedin_post_*.md
```

If this works, you're ready!

## 🚀 Step 4: Enable GitHub Actions

1. Go to your repo on GitHub
2. Click the "Actions" tab
3. If prompted, click "I understand my workflows, go ahead and enable them"
4. You should see 5 workflows:
   - Strategic Agent - Weekly Founder Report
   - Growth Agent - Daily LinkedIn Post
   - Finance Agent - Weekly Summary
   - Business Agent - Daily Pipeline Check
   - Retail Intelligence Agent - Biweekly Asset Generation

## ⚡ Step 5: Run Your First Agent on GitHub

### Manual Trigger (Recommended for First Run)
1. Go to: Actions tab
2. Select "Growth Agent - Daily LinkedIn Post"
3. Click "Run workflow" dropdown
4. Click green "Run workflow" button
5. Wait 30-60 seconds
6. Click on the running workflow to see progress
7. Once complete, check `reports/growth/` for output

### Check the Results
```bash
# Pull the latest changes
git pull

# View the generated post
cat reports/growth/linkedin_post_*.md
```

## 📊 Step 6: Understanding the Outputs

Each agent creates outputs in `reports/<agent_name>/`:

- **Strategic:** `weekly_founder_report_YYYY-MM-DD.md`
- **Growth:** `linkedin_post_YYYY-MM-DD.md`
- **Finance:** `weekly_finance_summary_YYYY-MM-DD.md`
- **Business:** `daily_pipeline_check_YYYY-MM-DD.md` or `proposal_draft_*.md`
- **Retail:** `technical_asset_YYYY-MM-DD_<topic>.md`

## ⏰ Automatic Schedules

Once enabled, agents run automatically:

| Agent | When | What It Does |
|-------|------|--------------|
| Growth | Mon-Fri 7 AM UTC | Drafts LinkedIn post |
| Business | Mon-Fri 10 AM UTC | Checks pipeline, suggests actions |
| Finance | Mondays 9 AM UTC | Weekly financial summary |
| Strategic | Fridays 4 PM UTC | Weekly founder report |
| Retail | Every other Wed 2 PM UTC | Creates technical asset |

## 🛠️ Customization Quick Tips

### Change Agent Schedule
Edit `.github/workflows/agent_<name>_*.yml`:
```yaml
schedule:
  - cron: '0 7 * * 1-5'  # Change these numbers
```

### Modify Agent Behavior
Edit `agents/<name>/config.yaml`:
```yaml
prompts:
  system: |
    [Change what the agent does here]
```

### Change Model or Temperature
Edit `agents/<name>/config.yaml`:
```yaml
claude_config:
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.7  # Lower = more focused, Higher = more creative
```

## 🐛 Troubleshooting

### Agent Fails in GitHub Actions
1. Check: Settings → Secrets → `ANTHROPIC_API_KEY` exists
2. View the workflow run logs for error details
3. Common issues:
   - Invalid API key
   - API rate limits
   - Missing input files

### Agent Runs But No Output
1. Check the agent ran successfully (green checkmark)
2. Pull latest: `git pull`
3. Look in correct directory: `ls reports/<agent_name>/`
4. Check workflow logs for errors

### API Rate Limits
If you hit rate limits:
1. Space out agent runs (edit cron schedules)
2. Use `workflow_dispatch` (manual trigger) more
3. Consider upgrading Anthropic API tier

## 📈 Next Steps

1. **Review Outputs:** Check agent reports in `reports/` directories
2. **Customize Prompts:** Edit `agents/*/config.yaml` to fit your needs
3. **Add Data:** Update CSV files in `data/` for agents to analyze
4. **Monitor Performance:** Weekly Founder Report tracks all agents
5. **Create New Agents:** Follow the pattern in existing agents

## 💡 Pro Tips

1. **Start with Manual Triggers:** Test each agent manually before relying on schedules
2. **Review Before Publishing:** Growth Agent posts need review before LinkedIn
3. **Keep Data Updated:** Finance/Business agents need current data
4. **Check Weekly Reports:** Strategic Agent's Friday report is your dashboard
5. **Adjust Temperatures:** Higher for creative (Growth), lower for analytical (Finance)

## 🆘 Getting Help

- **Issues:** Open a GitHub issue in this repo
- **Anthropic API Docs:** https://docs.anthropic.com/
- **GitHub Actions Docs:** https://docs.github.com/en/actions

## ✅ Success Criteria

You're successfully set up when:
- [x] All 5 agents run without errors
- [x] Outputs appear in `reports/` directories
- [x] GitHub Actions show green checkmarks
- [x] Weekly Founder Report generates on Fridays
- [x] Daily agents run Mon-Fri

**Congratulations! Your AI workforce is operational! 🎉**
