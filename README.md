# Converter Tools 🚀

**Production-grade converter tools** - 18 free trending converters across 6 categories for AI, Media, Finance, Developer Tools, Utilities, and Education.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy)

## 🌟 Features

- **18 Trending Converters** across 6 categories
- **Lightning Fast** - Optimized algorithms for instant conversions
- **100% Free** - No signup required
- **API-First Architecture** - Full REST API with OpenAPI documentation
- **Mobile Responsive** - Works perfectly on all devices
- **Dark Mode** - Beautiful dark theme with light mode toggle
- **SEO Optimized** - Structured data and meta tags

## 📋 Categories & Tools

### 1. AI & Data
- CSV → JSONL Converter
- Token Counter (GPT, Claude, Gemini)
- JSON → CSV Converter

### 2. Media & Content
- Image → WebP Converter
- Image Compressor
- PDF → Text Extractor

### 3. Finance & Crypto
- Currency Converter (Real-time rates)
- Crypto Price Tracker
- GST/Tax Calculator

### 4. Developer Tools
- JSON ↔ YAML Converter
- Base64 Encoder/Decoder
- JWT Token Decoder

### 5. Daily Utility
- Unit Converter (Length, Weight, Temperature, Area)
- Timezone Converter
- QR Code Generator

### 6. Education & Engineering
- Number System Converter (Binary, Octal, Decimal, Hex)
- Color Code Converter (HEX, RGB, HSL, CMYK)
- Percentage Calculator

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd converter-tools
```

2. **Set up Python environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the backend**
```bash
cd backend
python -m uvicorn api.main:app --reload
```

5. **Serve the frontend**
```bash
cd frontend
python -m http.server 8000
```

6. **Open in browser**
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## 📦 Deployment to Netlify

### Option 1: Deploy Button (Easiest)

Click the "Deploy to Netlify" button above and follow the instructions.

### Option 2: Manual Deployment

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Login to Netlify**
```bash
netlify login
```

3. **Deploy**
```bash
netlify deploy --prod
```

### Option 3: Git-based Deployment

1. Push your code to GitHub/GitLab
2. Go to [Netlify](https://app.netlify.com)
3. Click "New site from Git"
4. Select your repository
5. Netlify will auto-detect settings from `netlify.toml`
6. Click "Deploy site"

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
DEBUG=False
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_HOUR=100

# Optional API keys for specific converters
CURRENCY_API_KEY=your_key_here
CRYPTO_API_KEY=your_key_here
```

In Netlify, set these in: **Site settings → Environment variables**

## 📁 Project Structure

```
converter-tools/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app
│   │   └── routes/              # API endpoints (6 files)
│   ├── converters/              # Converter logic (6 modules)
│   ├── core/                    # Configuration & utilities
│   └── requirements.txt
├── frontend/
│   ├── index.html               # Landing page
│   ├── css/
│   │   └── style.css           # Custom styles
│   ├── js/
│   │   ├── main.js             # Main logic
│   │   └── api.js              # API client
│   └── pages/                   # Individual tool pages
├── netlify/
│   └── functions/
│       └── api.py              # Serverless function wrapper
├── netlify.toml                 # Netlify configuration
├── requirements.txt             # Python dependencies
└── README.md
```

## 🔌 API Documentation

Once deployed, access the interactive API documentation at:
- **Swagger UI**: `https://your-site.netlify.app/api/docs`
- **ReDoc**: `https://your-site.netlify.app/api/redoc`

### Example API Request

```bash
curl -X POST "https://your-site.netlify.app/api/ai-data/token-count" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "model": "gpt-4"
  }'
```

## 🎨 Customization

### Adding Your Own Converter

1. Create converter logic in `backend/converters/your_category/`
2. Add API route in `backend/api/routes/your_category.py`
3. Register router in `backend/api/main.py`
4. Create frontend page in `frontend/pages/`
5. Update landing page with new category

### Changing Theme Colors

Edit `frontend/index.html` Tailwind config:
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: {
                    500: '#your-color',
                    // ... more shades
                }
            }
        }
    }
}
```

## 💰 Monetization

### Built-in Features

- **Ad Placeholders** - Ready for Google AdSense or other ad networks
- **Rate Limiting** - Foundation for premium tiers
- **Premium Tool Markers** - Easily mark tools as premium

### Scaling to Paid

1. Add authentication (Firebase/Auth0)
2. Integrate Stripe for payments
3. Implement API key system for developers
4. Add usage analytics

## 📊 Analytics

Add Google Analytics or other analytics:

```html
<!-- Add to frontend/index.html <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
```

## 🐛 Troubleshooting

### Netlify Functions Not Working

- Ensure `mangum` is in `requirements.txt`
- Check Python version is 3.11 in `netlify.toml`
- Verify `netlify/functions/api.py` path is correct

### API Requests Failing

- Check CORS settings in `backend/core/config.py`
- Verify API base URL in `frontend/js/api.js`
- Check Netlify Function logs

### File Upload Errors

- Netlify free tier has 10MB file limit
- Check file size validation in frontend
- Consider using Cloudinary/S3 for large files

## 📈 Performance

- Average API response time: < 500ms
- Lighthouse score: 90+
- Mobile-optimized with lazy loading
- Cached static assets (1 year)

## 🔒 Security

- CORS protection
- Rate limiting to prevent abuse
- Input validation on all endpoints
- XSS and CSRF protection
- Security headers configured

## 📝 License

MIT License - Feel free to use for commercial projects!

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🌐 Live Demo

[View Live Demo](https://your-converter-tools.netlify.app)

## 📧 Support

For issues and questions:
- Open a GitHub issue
- Check API docs at `/api/docs`

---

**Built with ❤️ using FastAPI + Tailwind CSS**

*Production-ready • SEO-optimized • Mobile-first*
