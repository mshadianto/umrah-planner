"""
LABBAIK AI v6.0 - Utilities Package
==================================
Common utility functions and helpers.
"""

from utils.helpers import (
    # String utilities
    slugify,
    truncate,
    generate_random_string,
    mask_string,
    mask_email,
    clean_phone,
    
    # Validation
    is_valid_email,
    is_valid_phone,
    is_valid_passport,
    validate_date_range,
    
    # Date/Time
    format_date,
    format_date_id,
    format_datetime_id,
    time_ago,
    get_prayer_times,
    get_hijri_date,
    
    # Currency
    format_currency,
    parse_currency,
    convert_currency,
    
    # Hash
    hash_string,
    generate_verification_token,
    generate_booking_number,
    
    # Decorators
    retry,
    timing,
    cache_result,
    
    # Data utilities
    safe_get,
    flatten_dict,
    chunk_list,
    remove_none_values,
    deep_merge,
    safe_json_loads,
    safe_json_dumps,
)

__all__ = [
    # String
    "slugify",
    "truncate",
    "generate_random_string",
    "mask_string",
    "mask_email",
    "clean_phone",
    
    # Validation
    "is_valid_email",
    "is_valid_phone",
    "is_valid_passport",
    "validate_date_range",
    
    # Date/Time
    "format_date",
    "format_date_id",
    "format_datetime_id",
    "time_ago",
    "get_prayer_times",
    "get_hijri_date",
    
    # Currency
    "format_currency",
    "parse_currency",
    "convert_currency",
    
    # Hash
    "hash_string",
    "generate_verification_token",
    "generate_booking_number",
    
    # Decorators
    "retry",
    "timing",
    "cache_result",
    
    # Data
    "safe_get",
    "flatten_dict",
    "chunk_list",
    "remove_none_values",
    "deep_merge",
    "safe_json_loads",
    "safe_json_dumps",
]
