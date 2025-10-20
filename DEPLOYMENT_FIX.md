# Fix GitHub Actions Permission Error

## ❌ The Error
```
remote: Permission to Julian-Coral/CoralCloud-Workforce.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/...': The requested URL returned error: 403
```

This error occurs when GitHub Actions doesn't have permission to push commits back to your repository.

## ✅ Solution: Enable Workflow Permissions

### Step 1: Go to Repository Settings
1. Navigate to: https://github.com/Julian-Coral/CoralCloud-Workforce/settings/actions
2. Or: Your repo → Settings → Actions → General

### Step 2: Update Workflow Permissions
Scroll down to **"Workflow permissions"** section

**Select:**
- ✅ **"Read and write permissions"**

**Check:**
- ✅ **"Allow GitHub Actions to create and approve pull requests"** (optional but recommended)

### Step 3: Save
Click **"Save"** button at the bottom

### Step 4: Re-run Failed Workflow
1. Go to: https://github.com/Julian-Coral/CoralCloud-Workforce/actions
2. Find the failed workflow run
3. Click "Re-run all jobs"

---

## 🔧 Alternative Solution (If Above Doesn't Work)

If your organization has strict policies, you may need to use a Personal Access Token (PAT):

### Create a PAT
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "CoralCloud Agents"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

### Add PAT to Secrets
1. Go to: https://github.com/Julian-Coral/CoralCloud-Workforce/settings/secrets/actions
2. Click "New repository secret"
3. Name: `GH_PAT`
4. Value: Your token
5. Click "Add secret"

### Update Checkout Step in Workflows
Then update each workflow file's checkout step to use the PAT:

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    token: ${{ secrets.GH_PAT }}
    fetch-depth: 0
```

---

## 🧪 Testing

After enabling permissions, test with a manual trigger:

1. Go to: https://github.com/Julian-Coral/CoralCloud-Workforce/actions
2. Select "Growth Agent - Daily LinkedIn Post"
3. Click "Run workflow" → "Run workflow"
4. Wait for completion
5. Check that files were committed to `reports/growth/`

---

## ✅ Verification

You'll know it's working when:
- ✅ Workflow completes successfully (green checkmark)
- ✅ New files appear in `reports/` directories
- ✅ Git commits from "CoralCloud [Agent Name]" appear in history
- ✅ No permission errors in workflow logs

---

## 📝 Note About `[skip ci]`

The workflows include `[skip ci]` in commit messages to prevent infinite loops:
- Agent creates output → commits → workflow runs → creates output → commits → ...
- `[skip ci]` tells GitHub Actions to NOT trigger workflows on these commits

This is already configured in all 5 workflows, so you don't need to change anything.

---

## 🆘 Still Having Issues?

If you still get permission errors after enabling "Read and write permissions":

1. **Check Organization Settings** (if repo is in an organization)
   - Organization → Settings → Actions → General
   - Ensure "Read and write permissions" is allowed

2. **Check Branch Protection Rules**
   - Settings → Branches
   - If `main` has protection rules, ensure "Allow force pushes" or add the GitHub Actions bot as an exception

3. **Use the PAT Method** described above as a fallback

---

## 🎯 Quick Fix Checklist

- [ ] Repository Settings → Actions → General
- [ ] Workflow permissions → "Read and write permissions"
- [ ] Click "Save"
- [ ] Re-run failed workflow
- [ ] Verify new commits appear

That's it! Your agents will now be able to commit their outputs. 🚀
