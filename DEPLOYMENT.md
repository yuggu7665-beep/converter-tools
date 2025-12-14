# Quick Deployment Guide 🚀

## Option 1: Netlify CLI (5 minutes)

```bash
# Step 1: Install Netlify CLI
npm install -g netlify-cli

# Step 2: Navigate to project directory
cd "C:\Users\yuggu\Downloads\my tool\2"

# Step 3: Login to Netlify
netlify login

# Step 4: Deploy
netlify deploy --prod
```

After deployment, your site will be live at: `https://your-site.netlify.app`

---

## Option 2: GitHub + Netlify (10 minutes)

### A. Push to GitHub

```bash
# Initialize git
cd "C:\Users\yuggu\Downloads\my tool\2"
git init
git add .
git commit -m "Initial commit: Converter Tools"

# Create new repo on GitHub, then:
git remote add origin https://github.com/yourusername/converter-tools.git
git push -u origin main
```

### B. Deploy on Netlify

1. Go to https://app.netlify.com
2. Click **"New site from Git"**
3. Select **GitHub** and authorize
4. Choose your repository
5. Netlify will auto-detect settings from `netlify.toml`
6. Click **"Deploy site"**

✅ Done! Your site will be live in 2-3 minutes.

---

## Test Locally First (Recommended)

```bash
# Terminal 1: Start backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api.main:app --reload

# Terminal 2: Serve frontend
cd frontend
python -m http.server 8000
```

Then open:
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

---

## Post-Deployment Checklist

After deploying to Netlify:

1. ✅ Test the live site URL
2. ✅ Check `/api/docs` endpoint works
3. ✅ Test 2-3 converters via API
4. ✅ Verify mobile responsiveness
5. ✅ Test dark mode toggle

### Optional: Add Custom Domain

1. Go to **Site settings** → **Domain management**
2. Click **"Add custom domain"**
3. Follow DNS configuration steps

### Optional: Add Environment Variables

If using currency/crypto APIs:

1. Go to **Site settings** → **Environment variables**
2. Add:
   - `CURRENCY_API_KEY`
   - `CRYPTO_API_KEY`

---

## Troubleshooting

### Issue: API routes return 404
**Solution**: Check `netlify.toml` redirects are configured

### Issue: Functions timeout
**Solution**: Optimize slow converters, consider caching

### Issue: CORS errors
**Solution**: Update `ALLOWED_ORIGINS` in `backend/core/config.py`

---

## 📊 Expected Results

After deployment, you'll have:

- ✅ Live site at `your-name.netlify.app`
- ✅ 18 working API endpoints
- ✅ Interactive API documentation
- ✅ Mobile-responsive landing page
- ✅ Dark mode theme
- ✅ SEO optimized
- ✅ Ready for monetization

**Deployment time**: 5-10 minutes
**Free tier limits**: 125k API requests/month
