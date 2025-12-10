"""
LABBAIK AI v6.0 - UI Pages Package
==================================
All page modules for the LABBAIK platform.
"""

# Page imports
from ui.pages.home import render_home_page
from ui.pages.chat import render_chat_page
from ui.pages.simulator import render_simulator_page
from ui.pages.umrah_bareng import render_umrah_bareng_page
from ui.pages.umrah_mandiri import render_umrah_mandiri_page
from ui.pages.booking import render_booking_page

# Page registry
PAGE_REGISTRY = {
    "home": {
        "title": "Beranda",
        "icon": "🏠",
        "renderer": render_home_page,
        "requires_auth": False,
        "description": "Halaman utama LABBAIK AI",
    },
    "chat": {
        "title": "AI Assistant",
        "icon": "🤖",
        "renderer": render_chat_page,
        "requires_auth": False,
        "description": "Tanya jawab dengan AI tentang umrah",
    },
    "simulator": {
        "title": "Simulasi Biaya",
        "icon": "💰",
        "renderer": render_simulator_page,
        "requires_auth": False,
        "description": "Hitung estimasi biaya umrah",
    },
    "umrah_bareng": {
        "title": "Umrah Bareng",
        "icon": "👥",
        "renderer": render_umrah_bareng_page,
        "requires_auth": False,
        "description": "Cari teman perjalanan umrah",
    },
    "umrah_mandiri": {
        "title": "Umrah Mandiri",
        "icon": "🧭",
        "renderer": render_umrah_mandiri_page,
        "requires_auth": False,
        "description": "SUPER BOOM! Gamification + Virtual Manasik + Budget AI + Daily Challenges",
    },
    "booking": {
        "title": "Booking",
        "icon": "📦",
        "renderer": render_booking_page,
        "requires_auth": False,
        "description": "Pesan paket umrah",
    },
}


def get_page_renderer(page_name: str):
    """Get page renderer function by name."""
    page = PAGE_REGISTRY.get(page_name)
    if page:
        return page["renderer"]
    return None


def get_all_pages():
    """Get all available pages."""
    return PAGE_REGISTRY


def get_public_pages():
    """Get pages that don't require authentication."""
    return {k: v for k, v in PAGE_REGISTRY.items() if not v.get("requires_auth")}


# Exports
__all__ = [
    "render_home_page",
    "render_chat_page", 
    "render_simulator_page",
    "render_umrah_bareng_page",
    "render_umrah_mandiri_page",
    "render_booking_page",
    "PAGE_REGISTRY",
    "get_page_renderer",
    "get_all_pages",
    "get_public_pages",
]
