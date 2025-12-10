"""
LABBAIK AI v6.0 - Utility Functions
===================================
Common utility functions and helpers.
"""

import re
import hashlib
import secrets
import string
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any, Union
from functools import wraps
import logging
import time
import json

logger = logging.getLogger(__name__)


# =============================================================================
# STRING UTILITIES
# =============================================================================

def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.
    
    Args:
        text: Text to convert
    
    Returns:
        Slugified text
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def generate_random_string(length: int = 32, include_special: bool = False) -> str:
    """
    Generate random string.
    
    Args:
        length: String length
        include_special: Include special characters
    
    Returns:
        Random string
    """
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


def mask_string(text: str, visible_chars: int = 4, mask_char: str = "*") -> str:
    """
    Mask sensitive string.
    
    Args:
        text: Text to mask
        visible_chars: Number of visible characters at start and end
        mask_char: Character to use for masking
    
    Returns:
        Masked string
    """
    if len(text) <= visible_chars * 2:
        return mask_char * len(text)
    return text[:visible_chars] + mask_char * (len(text) - visible_chars * 2) + text[-visible_chars:]


def mask_email(email: str) -> str:
    """
    Mask email address.
    
    Args:
        email: Email to mask
    
    Returns:
        Masked email
    """
    if "@" not in email:
        return mask_string(email)
    
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked_local = local[0] + "*"
    else:
        masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"


def clean_phone(phone: str) -> str:
    """
    Clean and normalize phone number.
    
    Args:
        phone: Phone number
    
    Returns:
        Cleaned phone number
    """
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Normalize Indonesian numbers
    if cleaned.startswith('0'):
        cleaned = '+62' + cleaned[1:]
    elif cleaned.startswith('62'):
        cleaned = '+' + cleaned
    
    return cleaned


# =============================================================================
# VALIDATION UTILITIES
# =============================================================================

def is_valid_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email to validate
    
    Returns:
        True if valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number
    
    Returns:
        True if valid
    """
    cleaned = clean_phone(phone)
    pattern = r'^\+?[0-9]{10,15}$'
    return bool(re.match(pattern, cleaned))


def is_valid_passport(passport: str) -> bool:
    """
    Validate passport number format.
    
    Args:
        passport: Passport number
    
    Returns:
        True if valid
    """
    # Indonesian passport format
    pattern = r'^[A-Z][0-9]{7,8}$'
    return bool(re.match(pattern, passport.upper()))


def validate_date_range(start_date: date, end_date: date) -> tuple[bool, str]:
    """
    Validate date range.
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if start_date >= end_date:
        return False, "End date must be after start date"
    
    if start_date < date.today():
        return False, "Start date cannot be in the past"
    
    return True, ""


# =============================================================================
# DATE/TIME UTILITIES
# =============================================================================

def format_date(dt: Union[date, datetime], format_str: str = "%d %B %Y") -> str:
    """
    Format date for display.
    
    Args:
        dt: Date/datetime object
        format_str: Format string
    
    Returns:
        Formatted date string
    """
    return dt.strftime(format_str)


def format_date_id(dt: Union[date, datetime]) -> str:
    """
    Format date in Indonesian format.
    
    Args:
        dt: Date/datetime object
    
    Returns:
        Indonesian formatted date
    """
    months_id = [
        "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    
    day = dt.day
    month = months_id[dt.month]
    year = dt.year
    
    return f"{day} {month} {year}"


def format_datetime_id(dt: datetime) -> str:
    """
    Format datetime in Indonesian format.
    
    Args:
        dt: Datetime object
    
    Returns:
        Indonesian formatted datetime
    """
    date_str = format_date_id(dt)
    time_str = dt.strftime("%H:%M")
    return f"{date_str}, {time_str} WIB"


def time_ago(dt: datetime) -> str:
    """
    Get human-readable time ago string.
    
    Args:
        dt: Datetime object
    
    Returns:
        Time ago string
    """
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "baru saja"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} menit lalu"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} jam lalu"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} hari lalu"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} minggu lalu"
    else:
        return format_date_id(dt)


def get_prayer_times(latitude: float = 21.4225, longitude: float = 39.8262) -> Dict[str, str]:
    """
    Get prayer times for location (defaults to Makkah).
    
    Note: This is a simplified calculation.
    For production, use a proper prayer time calculation library.
    
    Args:
        latitude: Latitude
        longitude: Longitude
    
    Returns:
        Dictionary of prayer times
    """
    # Placeholder - in production, use a proper calculation
    return {
        "fajr": "04:45",
        "sunrise": "06:05",
        "dhuhr": "12:15",
        "asr": "15:30",
        "maghrib": "18:25",
        "isha": "19:45",
    }


def get_hijri_date(gregorian_date: date = None) -> Dict[str, Any]:
    """
    Convert Gregorian date to Hijri date.
    
    Note: This is a simplified conversion.
    For production, use a proper Hijri calendar library.
    
    Args:
        gregorian_date: Gregorian date (defaults to today)
    
    Returns:
        Hijri date info
    """
    if gregorian_date is None:
        gregorian_date = date.today()
    
    # Simplified approximation
    # In production, use hijri-converter library
    hijri_months = [
        "Muharram", "Safar", "Rabi'ul Awwal", "Rabi'ul Akhir",
        "Jumadil Awwal", "Jumadil Akhir", "Rajab", "Sya'ban",
        "Ramadan", "Syawwal", "Dzulqa'dah", "Dzulhijjah"
    ]
    
    # Very rough approximation
    base_gregorian = date(2024, 7, 7)  # 1 Muharram 1446 H
    days_diff = (gregorian_date - base_gregorian).days
    
    hijri_day = (days_diff % 30) + 1
    hijri_month = ((days_diff // 30) % 12)
    hijri_year = 1446 + (days_diff // 354)
    
    return {
        "day": hijri_day,
        "month": hijri_month + 1,
        "month_name": hijri_months[hijri_month],
        "year": hijri_year,
        "formatted": f"{hijri_day} {hijri_months[hijri_month]} {hijri_year} H"
    }


# =============================================================================
# CURRENCY UTILITIES
# =============================================================================

def format_currency(amount: float, currency: str = "IDR") -> str:
    """
    Format number as currency.
    
    Args:
        amount: Amount
        currency: Currency code
    
    Returns:
        Formatted currency string
    """
    if currency == "IDR":
        return f"Rp {amount:,.0f}"
    elif currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "SAR":
        return f"SAR {amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"


def parse_currency(text: str) -> Optional[float]:
    """
    Parse currency string to float.
    
    Args:
        text: Currency string
    
    Returns:
        Float value or None
    """
    # Remove currency symbols and whitespace
    cleaned = re.sub(r'[Rp$SAR\s,]', '', text)
    
    try:
        return float(cleaned)
    except ValueError:
        return None


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: Dict[str, float] = None
) -> float:
    """
    Convert between currencies.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency
        to_currency: Target currency
        rates: Exchange rates (USD base)
    
    Returns:
        Converted amount
    """
    if rates is None:
        # Default rates (approximate)
        rates = {
            "USD": 1.0,
            "IDR": 15500,
            "SAR": 3.75,
        }
    
    # Convert to USD first, then to target
    usd_amount = amount / rates.get(from_currency, 1)
    return usd_amount * rates.get(to_currency, 1)


# =============================================================================
# HASH UTILITIES
# =============================================================================

def hash_string(text: str, algorithm: str = "sha256") -> str:
    """
    Hash a string.
    
    Args:
        text: Text to hash
        algorithm: Hash algorithm
    
    Returns:
        Hex digest
    """
    if algorithm == "sha256":
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def generate_verification_token() -> str:
    """
    Generate verification token.
    
    Returns:
        Secure random token
    """
    return secrets.token_urlsafe(32)


def generate_booking_number() -> str:
    """
    Generate unique booking number.
    
    Returns:
        Booking number (format: LBK-XXXXXXXX)
    """
    random_part = secrets.token_hex(4).upper()
    return f"LBK-{random_part}"


# =============================================================================
# DECORATORS
# =============================================================================

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum retry attempts
        delay: Initial delay between retries
        backoff: Backoff multiplier
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed: {e}"
                    )
                    
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception
        return wrapper
    return decorator


def timing(func):
    """
    Decorator to log function execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000
        
        logger.debug(f"{func.__name__} executed in {elapsed:.2f}ms")
        return result
    return wrapper


def cache_result(ttl_seconds: int = 300):
    """
    Simple in-memory cache decorator.
    
    Args:
        ttl_seconds: Cache TTL in seconds
    """
    cache = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = hash_string(str(args) + str(kwargs), "md5")
            
            if key in cache:
                value, timestamp = cache[key]
                if time.time() - timestamp < ttl_seconds:
                    return value
            
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator


# =============================================================================
# DATA UTILITIES
# =============================================================================

def safe_get(data: Dict, path: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value.
    
    Args:
        data: Dictionary
        path: Dot-separated path (e.g., "user.profile.name")
        default: Default value if not found
    
    Returns:
        Value or default
    """
    keys = path.split(".")
    value = data
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default
        
        if value is None:
            return default
    
    return value


def flatten_dict(data: Dict, parent_key: str = "", sep: str = ".") -> Dict:
    """
    Flatten nested dictionary.
    
    Args:
        data: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Key separator
    
    Returns:
        Flattened dictionary
    """
    items = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep).items())
        else:
            items.append((new_key, value))
    
    return dict(items)


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    Split list into chunks.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_none_values(data: Dict) -> Dict:
    """
    Remove None values from dictionary.
    
    Args:
        data: Dictionary
    
    Returns:
        Dictionary without None values
    """
    return {k: v for k, v in data.items() if v is not None}


def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: Base dictionary
        dict2: Dictionary to merge
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


# =============================================================================
# JSON UTILITIES
# =============================================================================

def safe_json_loads(text: str, default: Any = None) -> Any:
    """
    Safely load JSON string.
    
    Args:
        text: JSON string
        default: Default value on error
    
    Returns:
        Parsed value or default
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """
    Safely dump to JSON string.
    
    Args:
        data: Data to serialize
        default: Default value on error
    
    Returns:
        JSON string or default
    """
    try:
        return json.dumps(data, default=str)
    except (TypeError, ValueError):
        return default
