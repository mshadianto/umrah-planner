"""
Version Management for Umrah Planner AI
========================================
Dynamic versioning with changelog and build info
"""

import os
from datetime import datetime
from typing import Optional

# Application Version
__version__ = "2.3.0"
__version_info__ = (2, 3, 0)

# Build Information
BUILD_DATE = "2025-11-26"
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local")

# Developer Information
DEVELOPER = {
    "name": "MS Hadianto",
    "title": "SE, Ak, M.M., CACP®, CCFA®, QIA®, CA®, GRCP®, GRCA®, CGP®",
    "role": "Founder & Lead Developer",
    "email": "sopian.hadianto@gmail.com",
    "whatsapp": "628159658833",
    "github": "https://github.com/mshadianto",
    "linkedin": "https://linkedin.com/in/sopian-adi-mulyana"
}

# Application Metadata
APP_INFO = {
    "name": "Umrah Planner AI",
    "tagline": "Platform Cerdas Perencanaan Umrah #1 Indonesia",
    "description": """
    Platform RAG Agentic AI untuk perencanaan dan simulasi biaya perjalanan umrah.
    Solusi lengkap untuk jamaah Indonesia dengan fitur booking, financing, dan loyalty.
    """,
    "license": "MIT License",
    "repository": "https://github.com/mshadianto/umrah-planner",
    "demo_url": "https://umrah-planner-by-mshadianto.streamlit.app"
}

# Changelog
CHANGELOG = {
    "2.3.0": {
        "date": "2025-11-26",
        "title": "Advanced Revenue Optimization",
        "changes": [
            "💳 Payment Gateway Integration (Midtrans, Xendit, DOKU)",
            "🎯 AI Dynamic Pricing Engine dengan competitor analysis",
            "⚡ Flash Sale & Auction system",
            "👥 Group Buying dengan tiered discounts",
            "🏪 Multi-vendor Marketplace",
            "🔌 API Monetization dengan pricing tiers",
            "📊 Data Products & Market Insights",
            "🎮 Gamification (achievements, badges, leaderboard)",
            "💬 WhatsApp Commerce dengan chatbot flows",
            "📈 AI Revenue Forecast & Projections",
        ]
    },
    "2.2.0": {
        "date": "2025-11-26",
        "title": "Startup Scale Features",
        "changes": [
            "📊 Analytics Dashboard dengan real-time metrics",
            "👥 CRM & Lead Management system",
            "🤖 Marketing Automation (Email & WhatsApp)",
            "💰 Commission & Payout Tracking",
            "🎁 Loyalty Program dengan tier membership",
            "🛡️ Insurance partner integration (AXA, Allianz, Zurich)",
            "💳 Financing partner integration (Kredivo, Akulaku, Home Credit)",
            "🤝 Partner Management dashboard",
            "📈 Revenue analytics & forecasting",
            "🔄 Automated follow-up workflows",
        ]
    },
    "2.1.0": {
        "date": "2025-11-26",
        "title": "Monetization & Business Features",
        "changes": [
            "💎 Added subscription tiers (Free, Basic, Premium, VIP)",
            "📝 Lead generation system with partner integration",
            "🤝 Affiliate partner directory with tracking",
            "🎁 Referral program with rewards",
            "🏢 B2B white label partnership page",
            "🔔 Price alert system for premium users",
            "💼 Business Hub dashboard",
            "💬 Quick quote widget in sidebar",
            "📊 Revenue analytics foundation",
        ]
    },
    "2.0.0": {
        "date": "2025-11-26",
        "title": "Major Feature Release",
        "changes": [
            "🆕 Added flight booking search",
            "🆕 Added hotel booking comparison",
            "🆕 Added ground transportation booking",
            "🆕 Added visa processing tracker",
            "🆕 Added payment installment calculator",
            "🆕 Added travel package comparison",
            "🆕 Added holy sites interactive map",
            "🆕 Added packing weight calculator",
            "📱 Enhanced mobile responsive UI",
            "🚀 Improved AI response quality",
            "🔧 Performance optimizations",
        ]
    },
    "1.0.0": {
        "date": "2025-11-26",
        "title": "Initial Release",
        "changes": [
            "💰 Cost simulation with multiple scenarios",
            "📊 Scenario comparison tool",
            "🤖 AI Chat Assistant with RAG",
            "📅 Time analysis for best travel dates",
            "✅ Preparation checklist",
            "💰 Savings calculator",
            "📿 Doa & Manasik guide",
            "💱 Currency converter",
            "🆘 Emergency contacts",
            "🌡️ Weather information",
        ]
    }
}

# Technology Stack
TECH_STACK = {
    "frontend": [
        ("Streamlit", "1.29.0", "Web Framework"),
        ("Plotly", "5.18.0", "Data Visualization"),
    ],
    "ai_ml": [
        ("LangChain", "0.1.0", "LLM Framework"),
        ("Groq", "0.4.2", "LLM Provider"),
        ("ChromaDB", "0.4.22", "Vector Database"),
        ("Sentence Transformers", "2.2.2", "Embeddings"),
    ],
    "data": [
        ("Pandas", "2.1.4", "Data Processing"),
        ("NumPy", "1.26.3", "Numerical Computing"),
    ]
}


def get_version() -> str:
    """Get current version string"""
    return __version__


def get_full_version() -> str:
    """Get full version with build info"""
    return f"v{__version__} (Build: {BUILD_NUMBER})"


def get_version_badge() -> str:
    """Get version badge HTML"""
    return f"""
    <span style="
        background: linear-gradient(90deg, #1e88e5, #43a047);
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    ">v{__version__}</span>
    """


def get_developer_card() -> str:
    """Get developer info card HTML"""
    dev = DEVELOPER
    wa_link = f"https://wa.me/{dev['whatsapp']}"
    return f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    ">
        <h3 style="margin: 0;">👨‍💻 {dev['name']}</h3>
        <p style="font-size: 0.85rem; opacity: 0.9; margin: 0.5rem 0;">{dev['title']}</p>
        <p style="font-size: 0.9rem; margin: 0.5rem 0;"><strong>{dev['role']}</strong></p>
        <div style="margin-top: 1rem;">
            <a href="{dev['github']}" target="_blank" style="color: white; margin: 0 10px;">🔗 GitHub</a>
            <a href="{dev['linkedin']}" target="_blank" style="color: white; margin: 0 10px;">💼 LinkedIn</a>
            <a href="{wa_link}" target="_blank" style="color: white; margin: 0 10px;">💬 WhatsApp</a>
        </div>
    </div>
    """


def get_changelog_markdown() -> str:
    """Get formatted changelog"""
    md = "## 📋 Changelog\n\n"
    for version, info in CHANGELOG.items():
        md += f"### v{version} - {info['title']}\n"
        md += f"*Released: {info['date']}*\n\n"
        for change in info['changes']:
            md += f"- {change}\n"
        md += "\n"
    return md


def get_app_age() -> str:
    """Get app age since first release"""
    first_release = datetime(2025, 11, 26)
    now = datetime.now()
    delta = now - first_release
    
    if delta.days == 0:
        return "Hari ini"
    elif delta.days == 1:
        return "1 hari yang lalu"
    elif delta.days < 30:
        return f"{delta.days} hari yang lalu"
    elif delta.days < 365:
        months = delta.days // 30
        return f"{months} bulan yang lalu"
    else:
        years = delta.days // 365
        return f"{years} tahun yang lalu"
