# Local Testing Guide - All 18 Converters 🧪

Your app is running! Let's test everything.

## 🟢 Currently Running
- **Backend API**: http://localhost:8000 ✅
- **Frontend**: http://localhost:3000 ✅
- **API Docs**: http://localhost:8000/api/docs ✅

---

## Quick Test - All Categories

### Option 1: Swagger UI (Easiest - Available Now!)

**Go to**: http://localhost:8000/api/docs

**Steps to test any tool:**
1. Click a category (e.g., "AI & Data")
2. Click an endpoint (e.g., "/api/ai-data/token-count")
3. Click "Try it out"
4. Enter test data
5. Click "Execute"
6. See results!

---

## 🧪 Test Each Tool

### AI & Data (3 tools)

#### 1. Token Counter
```bash
curl -X POST "http://localhost:8000/api/ai-data/token-count" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello, this is a test prompt for GPT-4\", \"model\": \"gpt-4\"}"
```

**Expected**: Characters, words, tokens, and cost estimate

#### 2. CSV → JSONL
```bash
curl -X POST "http://localhost:8000/api/ai-data/csv-to-jsonl" \
  -H "Content-Type: application/json" \
  -d "{\"csv_content\": \"name,age\\nAlice,30\\nBob,25\"}"
```

**Expected**: JSONL format output

#### 3. JSON → CSV
```bash
curl -X POST "http://localhost:8000/api/ai-data/json-to-csv" \
  -H "Content-Type: application/json" \
  -d "{\"json_content\": \"[{\\\"name\\\":\\\"Alice\\\",\\\"age\\\":30},{\\\"name\\\":\\\"Bob\\\",\\\"age\\\":25}]\"}"
```

**Expected**: CSV format output

---

### Finance & Crypto (3 tools)

#### 4. Currency Converter
```bash
curl -X POST "http://localhost:8000/api/finance/currency-convert" \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 100, \"from_currency\": \"USD\", \"to_currency\": \"EUR\"}"
```

**Expected**: Converted amount with exchange rate

#### 5. Crypto Price Tracker
```bash
curl -X POST "http://localhost:8000/api/finance/crypto-price" \
  -H "Content-Type: application/json" \
  -d "{\"crypto_symbol\": \"BTC\", \"vs_currency\": \"USD\"}"
```

**Expected**: Current BTC price and 24h change

#### 6. GST Calculator
```bash
curl -X POST "http://localhost:8000/api/finance/gst-calculate" \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 100, \"tax_rate\": 18, \"include_tax\": false}"
```

**Expected**: Base, tax amount, and total

---

### Developer Tools (5 tools)

#### 7. JSON → YAML
```bash
curl -X POST "http://localhost:8000/api/developer/json-to-yaml" \
  -H "Content-Type: application/json" \
  -d "{\"json_content\": \"{\\\"name\\\":\\\"test\\\",\\\"value\\\":123}\"}"
```

#### 8. YAML → JSON
```bash
curl -X POST "http://localhost:8000/api/developer/yaml-to-json" \
  -H "Content-Type: application/json" \
  -d "{\"yaml_content\": \"name: test\\nvalue: 123\", \"pretty\": true}"
```

#### 9. Base64 Encode
```bash
curl -X POST "http://localhost:8000/api/developer/base64-encode" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello, World!\"}"
```

#### 10. Base64 Decode
```bash
curl -X POST "http://localhost:8000/api/developer/base64-decode" \
  -H "Content-Type: application/json" \
  -d "{\"encoded_text\": \"SGVsbG8sIFdvcmxkIQ==\"}"
```

#### 11. JWT Decoder
```bash
curl -X POST "http://localhost:8000/api/developer/jwt-decode" \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U\", \"verify\": false}"
```

---

### Daily Utility (3 tools)

#### 12. Unit Converter
```bash
curl -X POST "http://localhost:8000/api/utility/unit-convert" \
  -H "Content-Type: application/json" \
  -d "{\"value\": 100, \"from_unit\": \"meter\", \"to_unit\": \"foot\", \"category\": \"length\"}"
```

#### 13. Timezone Converter
```bash
curl -X POST "http://localhost:8000/api/utility/timezone-convert" \
  -H "Content-Type: application/json" \
  -d "{\"time_str\": \"14:30\", \"from_timezone\": \"America/New_York\", \"to_timezone\": \"Europe/London\"}"
```

#### 14. QR Code Generator
```bash
curl -X POST "http://localhost:8000/api/utility/qr-generate" \
  -H "Content-Type: application/json" \
  -d "{\"data\": \"https://example.com\", \"size\": 10}"
```

**Expected**: Base64 encoded QR code image

---

### Education & Engineering (3 tools)

#### 15. Number System Converter
```bash
curl -X POST "http://localhost:8000/api/education/number-system" \
  -H "Content-Type: application/json" \
  -d "{\"number\": \"255\", \"from_system\": \"decimal\", \"to_system\": \"hexadecimal\"}"
```

**Expected**: FF

#### 16. Color Code Converter
```bash
curl -X POST "http://localhost:8000/api/education/color-convert" \
  -H "Content-Type: application/json" \
  -d "{\"color_value\": \"#FF5733\", \"from_format\": \"hex\"}"
```

**Expected**: HEX, RGB, HSL, CMYK values

#### 17. Percentage Calculator (5 types)
```bash
# Type 1: What is X% of Y?
curl -X POST "http://localhost:8000/api/education/percentage-calculate" \
  -H "Content-Type: application/json" \
  -d "{\"calculation_type\": \"percentage_of\", \"values\": {\"percentage\": 20, \"total\": 500}}"

# Type 2: X is what % of Y?
curl -X POST "http://localhost:8000/api/education/percentage-calculate" \
  -H "Content-Type: application/json" \
  -d "{\"calculation_type\": \"what_percent\", \"values\": {\"value\": 50, \"total\": 200}}"

# Type 3: Increase X by Y%
curl -X POST "http://localhost:8000/api/education/percentage-calculate" \
  -H "Content-Type: application/json" \
  -d "{\"calculation_type\": \"increase\", \"values\": {\"value\": 100, \"percentage\": 20}}"
```

---

### Media Tools (3 tools - Need file uploads)

#### 18. Test in Swagger UI
For image and PDF tools, use Swagger UI:
1. Go to http://localhost:8000/api/docs
2. Find "Media" section
3. Try `/api/media/image-to-webp` or `/api/media/pdf-to-text`
4. Click "Try it out"
5. Upload a file
6. Execute

---

## Checklist - Test All Tools

Copy this to track your testing:

### AI & Data
- [ ] CSV → JSONL
- [ ] Token Counter
- [ ] JSON → CSV

### Media & Content  
- [ ] Image → WebP
- [ ] Image Compressor
- [ ] PDF → Text

### Finance & Crypto
- [ ] Currency Converter
- [ ] Crypto Price Tracker
- [ ] GST Calculator

### Developer Tools
- [ ] JSON → YAML
- [ ] YAML → JSON
- [ ] Base64 Encode
- [ ] Base64 Decode
- [ ] JWT Decoder

### Daily Utility
- [ ] Unit Converter
- [ ] Timezone Converter
- [ ] QR Code Generator

### Education & Engineering
- [ ] Number System Converter
- [ ] Color Code Converter
- [ ] Percentage Calculator

---

## Performance Test

Test how fast the API responds:
```bash
# Time a request
time curl -X POST "http://localhost:8000/api/ai-data/token-count" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"test\", \"model\": \"gpt-4\"}"
```

**Expected**: < 200ms for most tools

---

## After Testing

Once you've verified all tools work:
✅ Ready to deploy to Netlify!

Run: `netlify deploy --prod`
