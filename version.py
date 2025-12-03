# version.py - LABBAIK Version Information
# Updated: 2025-12-03

__version__ = "3.4.1"

DEVELOPER = {
    "name": "MS Hadianto",
    "role": "Founder & Lead Developer",
    "company": "KIM Consulting",
    "email": "sopian.hadianto@gmail.com",
    "whatsapp": "6281596588833",
    "github": "https://github.com/mshadianto",
    "linkedin": "https://linkedin.com/in/mshadianto",
    "location": "Jakarta, Indonesia"
}

APP_INFO = {
    "name": "LABBAIK",
    "arabic": "لَبَّيْكَ",
    "tagline": "Panggilan-Nya, Langkahmu",
    "description": "Platform AI Perencanaan Umrah #1 Indonesia",
    "repository": "https://github.com/mshadianto/umrah-planner",
    "demo_url": "https://umrah-planner-by-mshadianto.streamlit.app",
    "license": "Proprietary",
    "first_release": "2025-11-26"
}

# ============================================
# CHANGELOG - Version History
# ============================================

CHANGELOG = {
    "3.4.1": {
        "name": "PWA Support & Visitor Database",
        "date": "2025-12-03",
        "features": [
            ("📱", "Progressive Web App (PWA) implementation"),
            ("🏠", "Add to Home Screen capability"),
            ("🎨", "Custom app icons (48px - 512px)"),
            ("📄", "Web App Manifest configuration"),
            ("⚙️", "Service Worker for caching"),
            ("📴", "Offline fallback page"),
            ("📲", "Tab 'Install App' di Tentang Aplikasi"),
            ("🎯", "Standalone display mode (fullscreen)"),
            ("📊", "Visitor counter persistent ke database Neon"),
            ("🔄", "Auto-fallback jika database tidak tersedia"),
            ("📈", "Page view tracking per halaman"),
        ]
    },
    "3.4.0": {
        "name": "Neon Database Integration",
        "date": "2025-12-02",
        "features": [
            ("🗄️", "Neon PostgreSQL cloud database integration"),
            ("🤝", "Umrah Bareng - Open trip matching platform"),
            ("🕋", "Umrah Mandiri - Independent umrah guide & forum"),
            ("📋", "DYOR Disclaimer - Do Your Own Research guidance"),
            ("⚖️", "Legal & Disclaimer page di Tentang Aplikasi"),
            ("🎨", "Improved sidebar user badge (dark theme)"),
            ("🔐", "Enhanced login/logout flow"),
            ("💾", "Persistent data storage for trips & forum posts"),
            ("🔄", "Auto-fallback to session state if DB unavailable"),
        ]
    },
    "3.3.0": {
        "name": "Umrah Mandiri & Forum",
        "date": "2025-12-02",
        "features": [
            ("🕋", "Umrah Mandiri comprehensive guide"),
            ("📖", "Regulasi Saudi Arabia & Indonesia"),
            ("💬", "Forum Diskusi dengan sample posts"),
            ("✍️", "Tulis Pengalaman feature"),
            ("❤️", "Like, comment, dan view counter"),
            ("📊", "Forum statistics dashboard"),
        ]
    },
    "3.2.0": {
        "name": "Umrah Bareng Feature",
        "date": "2025-12-02",
        "features": [
            ("🤝", "Umrah Bareng - Open Trip platform"),
            ("🔍", "Filter trips by budget, gender, city"),
            ("📝", "Create & manage open trips"),
            ("👥", "Member slot tracking"),
            ("📱", "WhatsApp group integration"),
        ]
    },
    "3.1.0": {
        "name": "Budget Finder & Video Tutorial",
        "date": "2025-12-02",
        "features": [
            ("💵", "Cari Paket by Budget feature"),
            ("🎬", "Ustadz Adi Hidayat video tutorial integration"),
            ("🏨", "Makkah/Madinah duration sliders"),
            ("🔧", "KeyError fixes for deployment"),
        ]
    },
    "3.0.0": {
        "name": "Major UI Overhaul",
        "date": "2025-12-01",
        "features": [
            ("🎨", "Complete LABBAIK branding redesign"),
            ("🌙", "Dark theme with gold accents"),
            ("📱", "Responsive mobile-friendly layout"),
            ("🕋", "Arabic typography integration"),
            ("📊", "Enhanced analytics dashboard"),
        ]
    },
    "2.5.0": {
        "name": "Supabase Database Integration",
        "date": "2025-11-26",
        "features": [
            ("🗄️", "Supabase PostgreSQL database integration"),
            ("👥", "Complete user authentication system"),
            ("🔒", "Role-based access control (6 levels)"),
            ("🛡️", "Admin & Super Admin dashboard"),
            ("📊", "User analytics & audit logs"),
            ("💳", "Subscription management"),
            ("📈", "Lead tracking system"),
            ("🛒", "Order management"),
            ("🔄", "Auto-fallback to in-memory storage"),
            ("🔐", "Row Level Security (RLS) support"),
        ]
    },
    "2.4.0": {
        "name": "User Authentication System",
        "date": "2025-11-26",
        "features": [
            ("🔐", "Login & Register system"),
            ("👥", "6 user levels (Free → Super Admin)"),
            ("🛡️", "Admin dashboard"),
            ("📋", "User management"),
            ("🎫", "Role-based feature access"),
        ]
    },
    "2.3.0": {
        "name": "Monetization & Business Features",
        "date": "2025-11-25",
        "features": [
            ("💰", "Pricing tiers (Free, Basic, Pro, Business)"),
            ("📧", "Quick Quote widget"),
            ("💼", "Business Hub for partners"),
            ("📊", "Usage tracking & limits"),
        ]
    },
    "2.2.0": {
        "name": "Visitor Analytics",
        "date": "2025-11-24",
        "features": [
            ("📊", "Real-time visitor tracking"),
            ("📈", "Page view analytics"),
            ("🗓️", "Daily/weekly/monthly stats"),
            ("📍", "Session tracking"),
        ]
    },
    "2.1.0": {
        "name": "Booking Features",
        "date": "2025-11-23",
        "features": [
            ("✈️", "Flight search integration"),
            ("🏨", "Hotel booking for Makkah & Madinah"),
            ("🚗", "Ground transportation options"),
            ("📋", "Booking summary & export"),
        ]
    },
    "2.0.0": {
        "name": "AI Chat & Scenarios",
        "date": "2025-11-22",
        "features": [
            ("🤖", "AI Chat Assistant (Groq/OpenAI)"),
            ("📊", "Multi-scenario comparison"),
            ("📅", "Timing analysis"),
            ("📋", "Plan builder with PDF export"),
        ]
    },
    "1.0.0": {
        "name": "Initial Release",
        "date": "2025-11-20",
        "features": [
            ("💰", "Cost simulation calculator"),
            ("📊", "Basic package comparison"),
            ("🎨", "Streamlit UI foundation"),
        ]
    },
}

TECH_STACK = {
    "frontend": [
        ("Streamlit", "1.28+", "Web application framework"),
        ("Plotly", "5.x", "Interactive charts & visualizations"),
        ("HTML/CSS", "-", "Custom styling & components"),
    ],
    "backend": [
        ("Python", "3.10+", "Core programming language"),
        ("Pandas", "2.x", "Data manipulation"),
        ("NumPy", "1.24+", "Numerical computing"),
    ],
    "database": [
        ("Neon PostgreSQL", "-", "Cloud serverless database"),
        ("SQLAlchemy", "2.x", "ORM & database toolkit"),
        ("psycopg2", "2.9+", "PostgreSQL adapter"),
    ],
    "ai_llm": [
        ("Groq", "Llama 3.3", "Primary LLM provider"),
        ("OpenAI", "GPT-4", "Alternative LLM provider"),
        ("ChromaDB", "0.4+", "Vector database for RAG"),
    ],
    "deployment": [
        ("Streamlit Cloud", "-", "Hosting platform"),
        ("GitHub", "-", "Version control & CI/CD"),
    ],
}

# ============================================
# ROADMAP - Future Plans
# ============================================

ROADMAP = {
    "Q1 2026": [
        ("📱", "Android Mobile App (Play Store)"),
        ("🍎", "iOS Mobile App (App Store)"),
        ("🔔", "Push notifications"),
    ],
    "Q2 2026": [
        ("💳", "Payment gateway integration"),
        ("🤝", "Travel agent partnership portal"),
        ("📍", "Real-time location tracking"),
    ],
    "Q3 2026": [
        ("🌐", "Multi-language support (Arabic, English)"),
        ("🎤", "Voice assistant integration"),
        ("📸", "Photo gallery & sharing"),
    ],
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_version_badge():
    """Return styled version badge HTML"""
    return f"""
<span style="background: linear-gradient(135deg, #D4AF37 0%, #C9A86C 100%); 
            color: #1A1A1A; padding: 5px 15px; border-radius: 15px; 
            font-weight: 700; font-size: 0.85rem;">
    v{__version__}
</span>
"""

def get_developer_card():
    """Return styled developer info card HTML"""
    company = DEVELOPER.get('company', 'Independent Developer')
    return f"""
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
            border-radius: 15px; padding: 25px; border: 1px solid #D4AF3740;">
    <div style="display: flex; align-items: center; gap: 20px;">
        <div style="font-size: 4rem;">👨‍💻</div>
        <div>
            <h3 style="color: #D4AF37; margin: 0;">{DEVELOPER.get('name', 'Developer')}</h3>
            <p style="color: #C9A86C; margin: 5px 0;">{DEVELOPER.get('role', 'Developer')}</p>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">{company}</p>
        </div>
    </div>
    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #333;">
        <p style="color: #aaa; font-size: 0.85rem; line-height: 1.6;">
            Platform ini dikembangkan oleh non-developer profesional di bidang GRC & Internal Audit, 
            dengan memanfaatkan teknologi AI (Claude by Anthropic & Gemini by Google) untuk membantu 
            calon jamaah merencanakan perjalanan umrah yang terencana dan sesuai budget.
        </p>
    </div>
</div>
"""

def get_changelog_markdown():
    """Return formatted changelog as markdown"""
    md = "## 📋 Changelog\n\n"
    
    for version, info in CHANGELOG.items():
        md += f"### v{version} - {info['name']}\n"
        md += f"*Released: {info['date']}*\n\n"
        
        for emoji, feature in info['features']:
            md += f"- {emoji} {feature}\n"
        
        md += "\n"
    
    return md

def get_roadmap_markdown():
    """Return formatted roadmap as markdown"""
    md = "## 🗺️ Roadmap\n\n"
    
    for quarter, items in ROADMAP.items():
        md += f"### {quarter}\n"
        for emoji, feature in items:
            md += f"- {emoji} {feature}\n"
        md += "\n"
    
    return md

def get_app_age():
    """Calculate app age since first release"""
    from datetime import datetime
    first_release = datetime.strptime(APP_INFO['first_release'], "%Y-%m-%d")
    today = datetime.now()
    days = (today - first_release).days
    
    if days < 7:
        return f"{days} hari"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} minggu"
    else:
        months = days // 30
        return f"{months} bulan"
