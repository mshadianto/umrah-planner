"""
LABBAIK Utility Functions
"""

from typing import Union
from datetime import datetime, timedelta


def format_currency(amount: Union[int, float], currency: str = "Rp") -> str:
    """Format number as currency string"""
    if amount is None:
        return f"{currency} 0"
    return f"{currency} {amount:,.0f}".replace(",", ".")


def format_duration(days: int) -> str:
    """Format duration in days to readable string"""
    if days == 1:
        return "1 hari"
    return f"{days} hari"


def format_date(date: datetime, format_str: str = "%d %B %Y") -> str:
    """Format datetime to Indonesian date string"""
    months_id = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    
    day = date.day
    month = months_id.get(date.month, date.strftime("%B"))
    year = date.year
    
    return f"{day} {month} {year}"


def get_season(month: int) -> str:
    """Get season based on month"""
    if month in [1, 2, 6, 7]:
        return "low"
    elif month == 12:
        return "high"
    else:
        return "regular"


def calculate_savings(original: float, discounted: float) -> dict:
    """Calculate savings percentage and amount"""
    savings_amount = original - discounted
    savings_percent = (savings_amount / original) * 100 if original > 0 else 0
    
    return {
        "amount": savings_amount,
        "percent": savings_percent,
        "formatted": format_currency(savings_amount)
    }


def validate_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate Indonesian phone number"""
    import re
    # Remove spaces and dashes
    phone = phone.replace(" ", "").replace("-", "")
    # Check for valid Indonesian format
    pattern = r'^(\+62|62|0)[0-9]{9,12}$'
    return bool(re.match(pattern, phone))


def generate_booking_id() -> str:
    """Generate unique booking ID"""
    import random
    import string
    timestamp = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"LBK-{timestamp}-{random_str}"


def get_islamic_date() -> str:
    """Get approximate Islamic/Hijri date (simplified)"""
    # This is a simplified approximation
    # For accurate dates, use a proper Hijri calendar library
    from datetime import datetime
    
    gregorian = datetime.now()
    
    # Approximate conversion (not accurate for all dates)
    hijri_year = int((gregorian.year - 622) * (33/32))
    
    # Simplified month names
    hijri_months = [
        "Muharram", "Safar", "Rabiul Awal", "Rabiul Akhir",
        "Jumadil Awal", "Jumadil Akhir", "Rajab", "Sya'ban",
        "Ramadan", "Syawal", "Dzulqa'dah", "Dzulhijjah"
    ]
    
    # Approximate month (very simplified)
    hijri_month_idx = (gregorian.month + 9) % 12
    
    return f"{hijri_months[hijri_month_idx]} {hijri_year} H"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with default value for zero division"""
    if denominator == 0:
        return default
    return numerator / denominator
