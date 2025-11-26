"""
Formatters Module
=================
Utility functions for formatting output
"""

from typing import Union
from datetime import datetime, date


def format_currency(
    amount: Union[int, float],
    currency: str = "IDR",
    show_decimal: bool = False
) -> str:
    """
    Format number as currency string
    
    Args:
        amount: Amount to format
        currency: Currency code
        show_decimal: Whether to show decimal places
        
    Returns:
        Formatted currency string
    """
    if currency == "IDR":
        if show_decimal:
            return f"Rp {amount:,.2f}"
        else:
            return f"Rp {amount:,.0f}"
    elif currency == "SAR":
        return f"SAR {amount:,.2f}"
    elif currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"


def format_date(
    dt: Union[datetime, date, str],
    format_type: str = "full"
) -> str:
    """
    Format date to Indonesian format
    
    Args:
        dt: Date to format
        format_type: Type of format (full/short/iso)
        
    Returns:
        Formatted date string
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    elif isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime.combine(dt, datetime.min.time())
    
    months_id = [
        "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus",
        "September", "Oktober", "November", "Desember"
    ]
    
    days_id = [
        "Senin", "Selasa", "Rabu", "Kamis",
        "Jumat", "Sabtu", "Minggu"
    ]
    
    if format_type == "full":
        day_name = days_id[dt.weekday()]
        month_name = months_id[dt.month - 1]
        return f"{day_name}, {dt.day} {month_name} {dt.year}"
    elif format_type == "short":
        month_name = months_id[dt.month - 1][:3]
        return f"{dt.day} {month_name} {dt.year}"
    elif format_type == "iso":
        return dt.strftime("%Y-%m-%d")
    else:
        return str(dt)


def format_duration(days: int) -> str:
    """
    Format duration in days to human readable string
    
    Args:
        days: Number of days
        
    Returns:
        Formatted duration string
    """
    if days == 1:
        return "1 hari"
    elif days < 7:
        return f"{days} hari"
    elif days == 7:
        return "1 minggu"
    elif days < 14:
        weeks = days // 7
        remaining = days % 7
        if remaining == 0:
            return f"{weeks} minggu"
        else:
            return f"{weeks} minggu {remaining} hari"
    else:
        weeks = days // 7
        remaining = days % 7
        if remaining == 0:
            return f"{weeks} minggu"
        else:
            return f"{weeks} minggu {remaining} hari"


def format_price_range(min_price: float, max_price: float) -> str:
    """
    Format price range
    
    Args:
        min_price: Minimum price
        max_price: Maximum price
        
    Returns:
        Formatted price range string
    """
    return f"{format_currency(min_price)} - {format_currency(max_price)}"


def format_star_rating(stars: int) -> str:
    """
    Format star rating as emoji
    
    Args:
        stars: Number of stars (1-5)
        
    Returns:
        Star emoji string
    """
    return "⭐" * min(max(stars, 1), 5)


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format value as percentage
    
    Args:
        value: Value to format (0-100 or 0-1)
        decimal_places: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    # If value is 0-1, convert to percentage
    if -1 <= value <= 1:
        value = value * 100
    
    return f"{value:.{decimal_places}f}%"


def format_list_items(items: list, bullet: str = "•") -> str:
    """
    Format list items with bullets
    
    Args:
        items: List of items
        bullet: Bullet character
        
    Returns:
        Formatted list string
    """
    return "\n".join(f"{bullet} {item}" for item in items)


def format_table_row(columns: list, widths: list = None) -> str:
    """
    Format a table row
    
    Args:
        columns: List of column values
        widths: List of column widths
        
    Returns:
        Formatted row string
    """
    if widths is None:
        return " | ".join(str(col) for col in columns)
    else:
        formatted = []
        for col, width in zip(columns, widths):
            formatted.append(str(col).ljust(width))
        return " | ".join(formatted)
