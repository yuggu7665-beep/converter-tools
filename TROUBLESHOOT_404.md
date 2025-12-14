# Netlify 404 Error - Troubleshooting Guide

## Most Common Causes

### 1. Site Still Deploying (Wait 2-3 minutes)
- Netlify takes time to build and deploy
- Check deploy status at: https://app.netlify.com

### 2. Wrong URL
- Make sure you're visiting the root URL
- NOT: `https://yoursite.netlify.app/some-page`
- YES: `https://yoursite.netlify.app`

### 3. Deployment Failed
Check build logs:
1. Go to https://app.netlify.com
2. Click your site
3. Click "Deploys" tab
4. Check if status is "Failed" or "Published"

---

## Quick Fixes

### Fix 1: Check Netlify Dashboard
```
1. Go to https://app.netlify.com
2. Find your "converter-tools" site
3. Look at deploy status:
   - "Published" ✅ = Working (wait for DNS)
   - "Building" ⏳ = Still deploying (wait)
   - "Failed" ❌ = Need to fix (see below)
```

### Fix 2: If Build Failed
Common issue: Python dependencies

**Solution - Add runtime.txt:**
```bash
# In your project folder:
echo "3.11" > runtime.txt
git add runtime.txt
git commit -m "Add Python runtime version"
git push
```

### Fix 3: Check Build Settings
Make sure Netlify settings match:
- **Build command**: (leave empty)
- **Publish directory**: `frontend`
- **Functions directory**: `netlify/functions`

---

## Manual Deploy (If Needed)

If auto-deploy isn't working:

```powershell
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Link to existing site
netlify link

# Deploy manually
netlify deploy --prod --dir=frontend
```

---

## Test Checklist

After deployment succeeds:

- [ ] Root URL loads: `https://yoursite.netlify.app`
- [ ] API docs work: `https://yoursite.netlify.app/api/docs`
- [ ] Tool page works: `https://yoursite.netlify.app/pages/qr-generator.html`

---

## Get Your Site URL

From command line:
```powershell
cd "C:\Users\yuggu\Downloads\my tool\2"
git remote -v
```

The URL will be based on your repo name.

Or check: https://app.netlify.com (your site list)

---

## Still Not Working?

Share the error from Netlify deploy logs:
1. Go to https://app.netlify.com
2. Click your site
3. Click "Deploys"
4. Click the failed deploy
5. Copy the error message
