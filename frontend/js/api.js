/**
 * API Client untuk Converter Tools
 * Handles all API requests to backend
 */

const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api'
    : '/api';  // For Netlify deployment

class ConverterAPI {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || error.detail || 'API request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Upload file
     */
    async uploadFile(endpoint, file, additionalData = {}) {
        const formData = new FormData();
        formData.append('file', file);

        // Add additional form fields
        Object.keys(additionalData).forEach(key => {
            formData.append(key, additionalData[key]);
        });

        const url = `${this.baseURL}${endpoint}`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || error.detail || 'File upload failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Upload Error:', error);
            throw error;
        }
    }

    // ==================== AI & Data APIs ====================

    async csvToJsonl(csvContent) {
        return this.request('/ai-data/csv-to-jsonl', {
            method: 'POST',
            body: JSON.stringify({ csv_content: csvContent }),
        });
    }

    async tokenCount(text, model = 'gpt-4') {
        return this.request('/ai-data/token-count', {
            method: 'POST',
            body: JSON.stringify({ text, model }),
        });
    }

    async jsonToCsv(jsonContent) {
        return this.request('/ai-data/json-to-csv', {
            method: 'POST',
            body: JSON.stringify({ json_content: jsonContent }),
        });
    }

    // ==================== Media APIs ====================

    async imageToWebP(file, quality = 85) {
        return this.uploadFile('/media/image-to-webp', file, { quality });
    }

    async compressImage(file, maxSizeKb = 500, quality = 85) {
        return this.uploadFile('/media/image-compress', file, {
            max_size_kb: maxSizeKb,
            quality
        });
    }

    async pdfToText(file) {
        return this.uploadFile('/media/pdf-to-text', file);
    }

    // ==================== Finance APIs ====================

    async convertCurrency(amount, fromCurrency, toCurrency) {
        return this.request('/finance/currency-convert', {
            method: 'POST',
            body: JSON.stringify({
                amount: parseFloat(amount),
                from_currency: fromCurrency,
                to_currency: toCurrency,
            }),
        });
    }

    async getCryptoPrice(cryptoSymbol, vsCurrency = 'USD') {
        return this.request('/finance/crypto-price', {
            method: 'POST',
            body: JSON.stringify({
                crypto_symbol: cryptoSymbol,
                vs_currency: vsCurrency,
            }),
        });
    }

    async calculateGST(amount, taxRate, includeTax = false) {
        return this.request('/finance/gst-calculate', {
            method: 'POST',
            body: JSON.stringify({
                amount: parseFloat(amount),
                tax_rate: parseFloat(taxRate),
                include_tax: includeTax,
            }),
        });
    }

    // ==================== Developer APIs ====================

    async jsonToYaml(jsonContent) {
        return this.request('/developer/json-to-yaml', {
            method: 'POST',
            body: JSON.stringify({ json_content: jsonContent }),
        });
    }

    async yamlToJson(yamlContent, pretty = true) {
        return this.request('/developer/yaml-to-json', {
            method: 'POST',
            body: JSON.stringify({ yaml_content: yamlContent, pretty }),
        });
    }

    async base64Encode(text) {
        return this.request('/developer/base64-encode', {
            method: 'POST',
            body: JSON.stringify({ text }),
        });
    }

    async base64Decode(encodedText) {
        return this.request('/developer/base64-decode', {
            method: 'POST',
            body: JSON.stringify({ encoded_text: encodedText }),
        });
    }

    async jwtDecode(token, verify = false, secret = null) {
        return this.request('/developer/jwt-decode', {
            method: 'POST',
            body: JSON.stringify({ token, verify, secret }),
        });
    }

    // ==================== Utility APIs ====================

    async convertUnit(value, fromUnit, toUnit, category) {
        return this.request('/utility/unit-convert', {
            method: 'POST',
            body: JSON.stringify({
                value: parseFloat(value),
                from_unit: fromUnit,
                to_unit: toUnit,
                category,
            }),
        });
    }

    async convertTimezone(timeStr, fromTimezone, toTimezone, dateStr = null) {
        return this.request('/utility/timezone-convert', {
            method: 'POST',
            body: JSON.stringify({
                time_str: timeStr,
                from_timezone: fromTimezone,
                to_timezone: toTimezone,
                date_str: dateStr,
            }),
        });
    }

    async generateQRCode(data, size = 10, border = 4) {
        return this.request('/utility/qr-generate', {
            method: 'POST',
            body: JSON.stringify({ data, size, border }),
        });
    }

    // ==================== Education APIs ====================

    async convertNumberSystem(number, fromSystem, toSystem) {
        return this.request('/education/number-system', {
            method: 'POST',
            body: JSON.stringify({
                number,
                from_system: fromSystem,
                to_system: toSystem,
            }),
        });
    }

    async convertColor(colorValue, fromFormat, toFormat = null) {
        return this.request('/education/color-convert', {
            method: 'POST',
            body: JSON.stringify({
                color_value: colorValue,
                from_format: fromFormat,
                to_format: toFormat,
            }),
        });
    }

    async calculatePercentage(calculationType, values) {
        return this.request('/education/percentage-calculate', {
            method: 'POST',
            body: JSON.stringify({
                calculation_type: calculationType,
                values,
            }),
        });
    }
}

// Export global API instance
window.API = new ConverterAPI();
