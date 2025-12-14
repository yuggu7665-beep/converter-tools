# 🚀 Deploy to Netlify - Step by Step Guide

## Method 1: GitHub + Netlify (EASIEST - No Installation Required)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `converter-tools` (or any name you want)
3. Set to **Public** or **Private**
4. **DO NOT** check "Add README", ".gitignore", or "license"
5. Click **"Create repository"**

You'll see a page with commands. **Copy the repository URL** (looks like: `https://github.com/yourusername/converter-tools.git`)

---

### Step 2: Push Your Code to GitHub

Open PowerShell in your project folder and run:

```powershell
# Add the GitHub repository as remote
git remote add origin https://github.com/YOURUSERNAME/converter-tools.git

# Push your code
git push -u origin master
```

*(Replace `YOURUSERNAME` with your actual GitHub username)*

If it asks for credentials, use your GitHub username and **Personal Access Token** (not password).

**Need a token?** Go to: https://github.com/settings/tokens → Generate new token (classic) → Check "repo" → Generate

---

### Step 3: Deploy on Netlify

1. Go to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Click **"Deploy with GitHub"**
4. Authorize Netlify to access your GitHub
5. Select your `converter-tools` repository
6. Netlify will auto-detect settings from `netlify.toml`
7. Click **"Deploy site"**

**That's it!** ✅ Your site will be live in 2-3 minutes.

---

## Method 2: Netlify CLI (If You Want)

### Install Netlify CLI:
```powershell
npm install -g netlify-cli
```

### Then Deploy:
```powershell
netlify login
netlify deploy --prod
```

---

## ⚡ Quick Commands Reference

```powershell
# Check Git status
git status

# Add GitHub remote (only once)
git remote add origin https://github.com/YOURUSERNAME/converter-tools.git

# Push to GitHub
git push -u origin master

# If you already pushed and made changes:
git add .
git commit -m "Update"
git push
```

---

## 🎯 After Deployment

You'll get a URL like: **`https://random-name-123.netlify.app`**

### Test Your Site:
1. Visit the URL
2. Test tools at `/pages/qr-generator.html`
3. Check API at `/api/docs`

### Change Site Name:
1. Go to **Site settings** → **General** → **Site details**
2. Click **"Change site name"**
3. Enter your preferred name: `my-converter-tools`
4. Now your URL is: `https://my-converter-tools.netlify.app`

### Add Custom Domain (Optional):
1. **Site settings** → **Domain management**
2. Click **"Add custom domain"**
3. Follow DNS instructions

---

## 🐛 Troubleshooting

### "Fatal: 'origin' already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOURUSERNAME/converter-tools.git
```

### "Authentication failed"
Use a **Personal Access Token** instead of password:
1. https://github.com/settings/tokens
2. Generate new token
3. Use token as password when pushing

### "Branch not found"
Your branch might be called `main` instead of `master`:
```powershell
git branch -M master
git push -u origin master
```

---

## 📊 Deployment Checklist

- [ ] Create GitHub repository
- [ ] Copy repository URL
- [ ] Add remote: `git remote add origin URL`
- [ ] Push code: `git push -u origin master`
- [ ] Go to Netlify: https://app.netlify.com
- [ ] Import from GitHub
- [ ] Select repository
- [ ] Deploy!
- [ ] Test live site
- [ ] Change site name (optional)

---

## 🎉 You're Done!

Your converter tools app will be **live on the internet** accessible to everyone!

**Share your URL:** `https://your-site.netlify.app`
