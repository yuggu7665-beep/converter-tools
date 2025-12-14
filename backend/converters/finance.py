"""Finance Converters"""
import requests
from typing import Dict, Any
from datetime import datetime
from core.exceptions import ValidationException, ProcessingException


class CurrencyConverter:
    """Convert between currencies using real-time exchange rates"""
    
    # Free API endpoint (no key required for basic usage)
    API_URL = "https://api.exchangerate-api.com/v4/latest/{base}"
    
    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """
        Convert currency amounts
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code (e.g., USD)
            to_currency: Target currency code (e.g., EUR)
            
        Returns:
            Dictionary with conversion result and rate
        """
        if amount < 0:
            raise ValidationException("Amount must be positive")
        
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        try:
            # Fetch exchange rates
            response = requests.get(
                CurrencyConverter.API_URL.format(base=from_currency),
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if to_currency not in data.get('rates', {}):
                raise ValidationException(f"Unsupported currency: {to_currency}")
            
            rate = data['rates'][to_currency]
            converted_amount = amount * rate
            
            return {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "amount": amount,
                "converted_amount": round(converted_amount, 2),
                "exchange_rate": rate,
                "timestamp": datetime.now().isoformat()
            }
            
        except requests.RequestException as e:
            raise ProcessingException(f"Failed to fetch exchange rates: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Currency conversion failed: {str(e)}")


class CryptoPriceTracker:
    """Track cryptocurrency prices"""
    
    # Free API endpoint (CoinGecko - no key required)
    API_URL = "https://api.coingecko.com/api/v3/simple/price"
    
    SUPPORTED_COINS = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "XRP": "ripple",
        "ADA": "cardano",
        "DOGE": "dogecoin",
        "SOL": "solana",
        "MATIC": "matic-network"
    }
    
    @staticmethod
    def get_price(crypto_symbol: str, vs_currency: str = "USD") -> Dict[str, Any]:
        """
        Get cryptocurrency price
        
        Args:
            crypto_symbol: Crypto symbol (BTC, ETH, etc.)
            vs_currency: Target currency (USD, EUR, etc.)
            
        Returns:
            Dictionary with price data
        """
        crypto_symbol = crypto_symbol.upper()
        vs_currency = vs_currency.lower()
        
        if crypto_symbol not in CryptoPriceTracker.SUPPORTED_COINS:
            raise ValidationException(f"Unsupported cryptocurrency: {crypto_symbol}")
        
        coin_id = CryptoPriceTracker.SUPPORTED_COINS[crypto_symbol]
        
        try:
            response = requests.get(
                CryptoPriceTracker.API_URL,
                params={
                    "ids": coin_id,
                    "vs_currencies": vs_currency,
                    "include_24hr_change": "true"
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if coin_id not in data:
                raise ProcessingException("Failed to fetch price data")
            
            price_data = data[coin_id]
            price = price_data.get(vs_currency, 0)
            change_24h = price_data.get(f"{vs_currency}_24h_change", 0)
            
            return {
                "cryptocurrency": crypto_symbol,
                "currency": vs_currency.upper(),
                "price": price,
                "change_24h_percent": round(change_24h, 2) if change_24h else None,
                "timestamp": datetime.now().isoformat()
            }
            
        except requests.RequestException as e:
            raise ProcessingException(f"Failed to fetch crypto price: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Price tracking failed: {str(e)}")


class GSTCalculator:
    """Calculate GST/VAT/Sales Tax"""
    
    @staticmethod
    def calculate(amount: float, tax_rate: float, include_tax: bool = False) -> Dict[str, Any]:
        """
        Calculate GST/Tax
        
        Args:
            amount: Base amount or total amount (depending on include_tax)
            tax_rate: Tax rate as percentage (e.g., 18 for 18%)
            include_tax: If True, amount includes tax; if False, tax will be added
            
        Returns:
            Dictionary with tax breakdown
        """
        if amount < 0:
            raise ValidationException("Amount must be positive")
        
        if not 0 <= tax_rate <= 100:
            raise ValidationException("Tax rate must be between 0 and 100")
        
        if include_tax:
            # Amount includes tax, extract base amount
            base_amount = amount / (1 + tax_rate / 100)
            tax_amount = amount - base_amount
            total_amount = amount
        else:
            # Amount is base, calculate tax
            base_amount = amount
            tax_amount = amount * (tax_rate / 100)
            total_amount = amount + tax_amount
        
        return {
            "base_amount": round(base_amount, 2),
            "tax_rate_percent": tax_rate,
            "tax_amount": round(tax_amount, 2),
            "total_amount": round(total_amount, 2),
            "tax_included": include_tax
        }
