"""
================================================================================
لَبَّيْكَ LABBAIK - Main Application
================================================================================

Labbaik Allahumma Labbaik - Aku Datang Memenuhi Panggilan-Mu

Copyright (c) 2025 MS Hadianto. All Rights Reserved.

================================================================================
Platform: AI-Powered Umrah Planning Platform
Version:  4.4.0
Codename: Labbaik Ultimate
Author:   MS Hadianto
Email:    sopian.hadianto@gmail.com
Website:  labbaik.ai
================================================================================

Version: 4.4.0
Updated: 2025-12-06
Changes: 
- Added Time Analysis feature (best time for umrah)
- Added AI Chat with built-in knowledge base
- Added visitor tracking with CountAPI (lightweight)
- Enhanced footer with visitor count & disclaimer
- Integrated features from v3.0.0 modular version
- Page view tracking for analytics
- Kept single-file lightweight architecture
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import hashlib

# ============================================
# CONFIGURATION & FALLBACKS
# ============================================
try:
    from config import app_config, llm_config, SCENARIO_TEMPLATES, DEPARTURE_CITIES, SEASONS
except ImportError:
    from dataclasses import dataclass
    import os
    
    @dataclass
    class AppConfig:
        name: str = "LABBAIK"
        version: str = "4.4.0"
    
    @dataclass
    class LLMConfig:
        provider: str = "groq"
        groq_api_key: str = ""
        openai_api_key: str = ""
        model: str = "llama-3.3-70b-versatile"
        groq_model: str = "llama-3.3-70b-versatile"
        openai_model: str = "gpt-4o-mini"
        temperature: float = 0.7
        max_tokens: int = 2000
        
        def __post_init__(self):
            self.groq_api_key = os.getenv("GROQ_API_KEY", "")
            self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    
    app_config = AppConfig()
    llm_config = LLMConfig()
    
    SCENARIO_TEMPLATES = {
        "ekonomis": {"name": "Ekonomis", "multiplier": 1.0, "duration_days": 9},
        "standard": {"name": "Standard", "multiplier": 1.3, "duration_days": 9},
        "premium": {"name": "Premium", "multiplier": 1.8, "duration_days": 12},
        "vip": {"name": "VIP", "multiplier": 2.5, "duration_days": 14}
    }
    
    DEPARTURE_CITIES = {
        "Jakarta": {"code": "CGK", "multiplier": 1.0},
        "Surabaya": {"code": "SUB", "multiplier": 1.05},
        "Medan": {"code": "KNO", "multiplier": 1.1},
        "Bandung": {"code": "BDO", "multiplier": 1.08}
    }
    
    SEASONS = {
        "low": {"name": "Low Season", "multiplier": 0.85, "months": [1, 2, 9, 10, 11]},
        "regular": {"name": "Regular", "multiplier": 1.0, "months": [4, 5, 8]},
        "high": {"name": "High Season", "multiplier": 1.4, "months": [3, 6, 7, 12]}
    }

# ============================================
# LABBAIK BRAND CONSTANTS
# ============================================
BRAND = {
    "name": "LABBAIK",
    "arabic": "لَبَّيْكَ",
    "talbiyah": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ",
    "tagline": "Panggilan-Nya, Langkahmu",
    "description": "Platform AI Perencanaan Umrah #1 Indonesia",
    "version": "4.4.0",
}

COLORS = {
    "black": "#1A1A1A",
    "gold": "#D4AF37",
    "gold_light": "#F5E6C8",
    "green": "#006B3C",
    "white": "#FFFFFF",
    "sand": "#C9A86C",
}

CONTACT = {
    "email": "sopian.hadianto@gmail.com",
    "whatsapp": "+62 815 9658 833",
}

# ============================================
# DEFAULT ADMIN CREDENTIALS (Offline Fallback)
# ============================================
DEFAULT_ADMIN = {
    "email": "admin@labbaik.id",
    "password": "@Jakarta01",
    "name": "Admin LABBAIK",
    "role": "admin"
}

# ============================================
# HOTEL PRICES CONFIGURATION
# ============================================
HOTEL_PRICES = {
    "ekonomis": {
        "makkah": {"name": "Hotel Bintang 2-3 (1-2 km dari Haram)", "price": 800000},
        "madinah": {"name": "Hotel Bintang 2-3 (500m-1 km dari Nabawi)", "price": 600000}
    },
    "standard": {
        "makkah": {"name": "Hotel Bintang 3-4 (500m-1 km dari Haram)", "price": 1500000},
        "madinah": {"name": "Hotel Bintang 3-4 (300-500m dari Nabawi)", "price": 1000000}
    },
    "premium": {
        "makkah": {"name": "Hotel Bintang 4-5 (200-500m dari Haram)", "price": 2500000},
        "madinah": {"name": "Hotel Bintang 4-5 (100-300m dari Nabawi)", "price": 1800000}
    },
    "vip": {
        "makkah": {"name": "Hotel Bintang 5 (View Ka'bah, <200m)", "price": 5000000},
        "madinah": {"name": "Hotel Bintang 5 (View Masjid Nabawi, <100m)", "price": 3500000}
    }
}

ADDITIONAL_COSTS = {
    "ekonomis": {"flight": 8000000, "visa": 500000, "transport": 500000, "meals": 300000},
    "standard": {"flight": 12000000, "visa": 500000, "transport": 800000, "meals": 500000},
    "premium": {"flight": 18000000, "visa": 500000, "transport": 1200000, "meals": 800000},
    "vip": {"flight": 30000000, "visa": 500000, "transport": 2000000, "meals": 1500000}
}

# ============================================
# ENHANCED FEATURES DATA (v3.9.0)
# ============================================
CHECKLIST_DATA = {
    "dokumen": {
        "title": "📄 Dokumen",
        "items": [
            ("Paspor (valid >6 bln)", True),
            ("Fotokopi paspor 5 lbr", True),
            ("Foto 4x6 bg putih 10 lbr", True),
            ("Buku vaksin meningitis", True),
            ("Visa umrah (dari travel)", True),
            ("KTP asli + fotokopi", False),
            ("Kartu keluarga fotokopi", False),
            ("Surat nikah (jika berpasangan)", False),
        ]
    },
    "pakaian": {
        "title": "👔 Pakaian",
        "items": [
            ("Kain ihram 2 set (pria)", True),
            ("Mukena 2 set (wanita)", True),
            ("Pakaian harian 5-7 stel", True),
            ("Sandal nyaman untuk jalan", True),
            ("Jaket tipis (AC/malam)", True),
            ("Kaos kaki (untuk masjid)", False),
            ("Sarung 2 buah", False),
            ("Pakaian dalam secukupnya", True),
        ]
    },
    "kesehatan": {
        "title": "💊 Kesehatan",
        "items": [
            ("Obat pribadi rutin", True),
            ("Obat flu & batuk", True),
            ("Paracetamol/pereda nyeri", True),
            ("Minyak angin/balsem", True),
            ("Masker medis", True),
            ("Hand sanitizer", True),
            ("Vitamin C & multivitamin", False),
            ("P3K mini (plester, betadine)", False),
        ]
    },
    "elektronik": {
        "title": "🔌 Elektronik",
        "items": [
            ("HP + charger", True),
            ("Power bank (min 10000mAh)", True),
            ("Adaptor colokan (tipe G)", True),
            ("Kabel data cadangan", False),
            ("Earphone", False),
        ]
    },
    "lainnya": {
        "title": "🎒 Lainnya",
        "items": [
            ("Tas kecil untuk di Haram", True),
            ("Buku doa & dzikir", True),
            ("Sajadah travel", False),
            ("Tasbih", False),
            ("Gunting kuku kecil", True),
            ("Sisir", False),
            ("Payung lipat", False),
            ("Uang SAR secukupnya", True),
            ("Kunci gembok koper", False),
            ("Label nama di koper", True),
        ]
    }
}

DOA_MANASIK = {
    "niat": {
        "title": "1️⃣ Niat Ihram",
        "arab": "لَبَّيْكَ اللَّهُمَّ عُمْرَةً",
        "latin": "Labbaika Allāhumma 'Umratan",
        "arti": "Aku penuhi panggilan-Mu ya Allah untuk umrah"
    },
    "talbiyah": {
        "title": "2️⃣ Talbiyah",
        "arab": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لاَ شَرِيْكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لاَ شَرِيْكَ لَكَ",
        "latin": "Labbaika Allāhumma labbaik, labbaika lā syarīka laka labbaik, innal ḥamda wan ni'mata laka wal mulk, lā syarīka lak",
        "arti": "Aku datang memenuhi panggilan-Mu ya Allah, Engkau tidak punya sekutu, segala puji dan nikmat adalah milik-Mu, demikian pula kerajaan, tiada sekutu bagi-Mu"
    },
    "kabah": {
        "title": "3️⃣ Melihat Ka'bah",
        "arab": "اللَّهُمَّ زِدْ هَذَا الْبَيْتَ تَشْرِيفًا وَتَعْظِيمًا وَتَكْرِيمًا وَمَهَابَةً",
        "latin": "Allāhumma zid hādhal baita tasyrīfan wa ta'ẓīman wa takrīman wa mahābah",
        "arti": "Ya Allah, tambahkanlah kemuliaan, keagungan, kehormatan dan kewibawaan pada rumah ini (Ka'bah)"
    },
    "thawaf": {
        "title": "4️⃣ Mulai Thawaf",
        "arab": "بِسْمِ اللَّهِ وَاللَّهُ أَكْبَرُ، اللَّهُمَّ إِيمَانًا بِكَ وَتَصْدِيقًا بِكِتَابِكَ وَوَفَاءً بِعَهْدِكَ وَاتِّبَاعًا لِسُنَّةِ نَبِيِّكَ مُحَمَّدٍ ﷺ",
        "latin": "Bismillāhi wallāhu akbar, Allāhumma īmānan bika wa taṣdīqan bikitābika wa wafā'an bi'ahdika wattibā'an lisunnati nabiyyika Muḥammadin ṣallallāhu 'alaihi wasallam",
        "arti": "Dengan nama Allah, Allah Maha Besar. Ya Allah, dengan iman kepada-Mu, membenarkan kitab-Mu, memenuhi janji-Mu, dan mengikuti sunnah Nabi-Mu Muhammad SAW"
    },
    "rukun": {
        "title": "5️⃣ Rukun Yamani-Hajar Aswad",
        "arab": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
        "latin": "Rabbanā ātinā fid dunyā ḥasanatan wa fil ākhirati ḥasanatan wa qinā 'adzāban nār",
        "arti": "Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan lindungilah kami dari siksa neraka"
    },
    "sai": {
        "title": "6️⃣ Mulai Sa'i (Shafa)",
        "arab": "إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللَّهِ",
        "latin": "Innash shafā wal marwata min sya'ā'irillāh",
        "arti": "Sesungguhnya Shafa dan Marwah adalah sebagian dari syiar Allah"
    }
}

EMERGENCY_CONTACTS = [
    {"name": "🏛️ KBRI Riyadh", "phone": "+966-11-488-2800"},
    {"name": "🏛️ KJRI Jeddah", "phone": "+966-12-667-6270"},
    {"name": "🚔 Polisi Saudi", "phone": "999"},
    {"name": "🚑 Ambulans", "phone": "997"},
    {"name": "🚒 Pemadam", "phone": "998"},
    {"name": "🏥 RS King Faisal Makkah", "phone": "+966-12-553-3300"},
]

# ============================================
# VISITOR TRACKING (Lightweight with CountAPI)
# ============================================
def get_visitor_count():
    """Get total visitor count using CountAPI - lightweight external tracking"""
    try:
        import urllib.request
        import json
        
        # Only count once per session to avoid inflating numbers
        if "visitor_counted" not in st.session_state:
            url = "https://api.countapi.xyz/hit/labbaik-umrah/visitors"
            with urllib.request.urlopen(url, timeout=3) as response:
                data = json.loads(response.read().decode())
                st.session_state.visitor_counted = True
                st.session_state.visitor_count = data.get("value", 0)
        
        return st.session_state.get("visitor_count", 0)
    except:
        # Fallback if API fails - use session-based counter
        if "visitor_count" not in st.session_state:
            st.session_state.visitor_count = 1250  # Base count
        return st.session_state.visitor_count

def track_page_view(page_name: str):
    """Track individual page views in session"""
    # Ensure page_views is a dictionary
    if "page_views" not in st.session_state or not isinstance(st.session_state.page_views, dict):
        st.session_state.page_views = {"_total": 3500}
    
    if page_name not in st.session_state.page_views:
        st.session_state.page_views[page_name] = 0
    
    st.session_state.page_views[page_name] += 1
    st.session_state.page_views["_total"] = st.session_state.page_views.get("_total", 3500) + 1

# Video Tutorials - Ustadz Adi Hidayat Featured
VIDEO_TUTORIALS = [
    {
        "id": "uah_manasik",
        "title": "Panduan Lengkap Manasik Umrah - Ustadz Adi Hidayat",
        "url": "https://youtu.be/e1XsLF6aUaA?si=Bxpy9w5r7fkc2Yw1",
        "description": "Kajian lengkap tata cara manasik umrah dari Ustadz Adi Hidayat, Lc., MA. Penjelasan detail mulai dari ihram hingga tahallul dengan dalil-dalil shahih.",
        "speaker": "Ustadz Adi Hidayat, Lc., MA",
        "duration": "2+ jam",
        "featured": True,
    },
    {
        "id": "generic_manasik",
        "title": "Video Panduan Manasik Umrah Singkat",
        "url": "https://www.youtube.com/watch?v=TRYDkDwqJv0",
        "description": "Video panduan manasik umrah singkat untuk referensi tambahan.",
        "speaker": "Various",
        "duration": "~15 menit",
        "featured": False,
    }
]

# Currency Exchange Rates
CURRENCY_RATES = {
    "IDR_TO_SAR": 0.000242,
    "SAR_TO_IDR": 4130,
    "IDR_TO_USD": 0.0000645,
    "USD_TO_IDR": 15500,
}

# Weather Data (Monthly Average)
WEATHER_DATA = {
    "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
    "Makkah": [24, 25, 28, 32, 36, 38, 39, 38, 37, 33, 29, 25],
    "Madinah": [18, 20, 24, 29, 34, 37, 38, 38, 35, 30, 24, 19],
}

# ============================================
# ENGAGEMENT SYSTEM (v3.5.0)
# ============================================
POINTS_CONFIG = {
    "daily_login": 10,
    "daily_streak_bonus": 5,
    "complete_simulation": 25,
    "share_social": 50,
    "referral_signup": 200,
    "referral_bonus": 75,
    "quiz_correct": 15,
    "read_guide": 10,
    "complete_profile": 50,
    "create_plan": 30,
    "compare_packages": 10,
    "helpful_answer": 30,
    "complete_learning": 100,
}

# Enhanced Levels System (10 Levels)
LEVELS = [
    {"level": 1, "name": "Jamaah Pemula", "min_points": 0, "icon": "🌱", "color": "#8BC34A"},
    {"level": 2, "name": "Jamaah Aktif", "min_points": 100, "icon": "🌿", "color": "#4CAF50"},
    {"level": 3, "name": "Jamaah Setia", "min_points": 300, "icon": "🌳", "color": "#2E7D32"},
    {"level": 4, "name": "Calon Mutawwif", "min_points": 600, "icon": "⭐", "color": "#FFC107"},
    {"level": 5, "name": "Mutawwif", "min_points": 1000, "icon": "🌟", "color": "#FF9800"},
    {"level": 6, "name": "Mutawwif Senior", "min_points": 1500, "icon": "💫", "color": "#FF5722"},
    {"level": 7, "name": "Jamaah Berpengalaman", "min_points": 2500, "icon": "🏅", "color": "#9C27B0"},
    {"level": 8, "name": "Pakar Umrah", "min_points": 4000, "icon": "🎖️", "color": "#673AB7"},
    {"level": 9, "name": "Mentor Jamaah", "min_points": 6000, "icon": "👑", "color": "#3F51B5"},
    {"level": 10, "name": "Haji Mabrur", "min_points": 10000, "icon": "🕋", "color": "#D4AF37"},
]

# Enhanced Badges System
BADGES = {
    # Starter Badges
    "newcomer": {"name": "Pendatang Baru", "icon": "🌟", "points": 0, "category": "starter"},
    "profile_complete": {"name": "Profil Lengkap", "icon": "📝", "points": 50, "category": "starter"},
    
    # Planning Badges
    "explorer": {"name": "Penjelajah", "icon": "🔍", "points": 100, "category": "planning"},
    "planner": {"name": "Perencana Handal", "icon": "📋", "points": 500, "category": "planning"},
    "budget_master": {"name": "Ahli Anggaran", "icon": "📊", "points": 750, "category": "planning"},
    
    # Achievement Badges
    "expert": {"name": "Ahli Umrah", "icon": "🎓", "points": 1000, "category": "achievement"},
    "ambassador": {"name": "Duta LABBAIK", "icon": "👑", "points": 2500, "category": "achievement"},
    "legend": {"name": "Legenda LABBAIK", "icon": "🏆", "points": 5000, "category": "achievement"},
    
    # Streak Badges
    "streak_7": {"name": "Istiqomah Seminggu", "icon": "🔥", "points": 100, "category": "streak"},
    "streak_30": {"name": "Istiqomah Sebulan", "icon": "💎", "points": 500, "category": "streak"},
    "streak_100": {"name": "Istiqomah 100 Hari", "icon": "🏆", "points": 2000, "category": "streak"},
    
    # Social Badges
    "first_share": {"name": "Penyebar Kebaikan", "icon": "📤", "points": 50, "category": "social"},
    "influencer": {"name": "Influencer Umrah", "icon": "🌟", "points": 1000, "category": "social"},
    "community_hero": {"name": "Pahlawan Komunitas", "icon": "🦸", "points": 750, "category": "social"},
    
    # Learning Badges
    "doa_master": {"name": "Hafidz Doa", "icon": "📖", "points": 200, "category": "learning"},
    "manasik_complete": {"name": "Lulus Manasik", "icon": "🎓", "points": 300, "category": "learning"},
    "perfect_quiz": {"name": "Nilai Sempurna", "icon": "💯", "points": 200, "category": "learning"},
}

# Daily Rewards System
DAILY_REWARDS = [
    {"day": 1, "reward": "10 LP", "points": 10, "icon": "🎁"},
    {"day": 2, "reward": "15 LP", "points": 15, "icon": "🎁"},
    {"day": 3, "reward": "20 LP", "points": 20, "icon": "🎁"},
    {"day": 4, "reward": "25 LP", "points": 25, "icon": "🎁"},
    {"day": 5, "reward": "30 LP", "points": 30, "icon": "🎁"},
    {"day": 6, "reward": "40 LP", "points": 40, "icon": "🎁"},
    {"day": 7, "reward": "100 LP + Badge", "points": 100, "icon": "🏆"},
]

# Daily Challenges
DAILY_CHALLENGES = [
    {"id": "simulate_budget", "title": "Simulasi Budget", "desc": "Lakukan 1x simulasi biaya", "points": 20, "icon": "💰"},
    {"id": "read_tips", "title": "Pembaca Aktif", "desc": "Baca 3 tips umrah", "points": 15, "icon": "📚"},
    {"id": "share_app", "title": "Berbagi Kebaikan", "desc": "Share LABBAIK", "points": 25, "icon": "📤"},
    {"id": "complete_quiz", "title": "Uji Pengetahuan", "desc": "Selesaikan 1 quiz", "points": 30, "icon": "❓"},
]

# Subscription Plans
SUBSCRIPTION_PLANS = {
    "basic": {
        "name": "Basic Member",
        "price": 49000,
        "price_display": "Rp 49.000",
        "features": ["50 Chat AI / hari", "Simpan 5 rencana", "Diskon 5% booking"],
        "badge": "🥉"
    },
    "premium": {
        "name": "Premium Member",
        "price": 149000,
        "price_display": "Rp 149.000",
        "features": ["Unlimited Chat AI", "Simpan 20 rencana", "Export PDF", "Price alert", "Diskon 10%"],
        "badge": "⭐",
        "popular": True
    },
    "vip": {
        "name": "VIP Elite",
        "price": 499000,
        "price_display": "Rp 499.000",
        "features": ["Semua fitur Premium", "Dedicated assistant 24/7", "Konsultasi video call", "Diskon 15%"],
        "badge": "👑"
    }
}

# Sponsorship Tiers
SPONSORSHIP_TIERS = {
    "bronze": {
        "name": "Bronze Partner",
        "price": 2500000,
        "benefits": ["Logo di footer", "1 slot featured", "Basic analytics"],
        "color": "#CD7F32",
        "icon": "🥉"
    },
    "silver": {
        "name": "Silver Partner",
        "price": 5000000,
        "benefits": ["Logo di sidebar", "3 slot featured", "Priority listing", "Monthly report"],
        "color": "#C0C0C0",
        "icon": "🥈"
    },
    "gold": {
        "name": "Gold Partner",
        "price": 10000000,
        "benefits": ["Logo di homepage", "5 slot featured", "Top priority", "Weekly report", "Custom branding"],
        "color": "#FFD700",
        "icon": "🥇"
    }
}

QUIZ_QUESTIONS = [
    {
        "question": "Apa rukun pertama dalam umrah?",
        "options": ["Thawaf", "Ihram", "Sa'i", "Tahallul"],
        "correct": 1,
        "explanation": "Ihram adalah rukun pertama. Dimulai dari miqat dengan niat dan memakai pakaian ihram."
    },
    {
        "question": "Berapa kali putaran thawaf?",
        "options": ["5 kali", "6 kali", "7 kali", "8 kali"],
        "correct": 2,
        "explanation": "Thawaf dilakukan 7 kali putaran mengelilingi Ka'bah, dimulai dari Hajar Aswad."
    },
    {
        "question": "Sa'i dilakukan antara bukit apa?",
        "options": ["Arafah-Muzdalifah", "Shafa-Marwah", "Mina-Arafah", "Jabal Nur-Tsur"],
        "correct": 1,
        "explanation": "Sa'i dilakukan 7 kali perjalanan antara bukit Shafa dan Marwah."
    },
    {
        "question": "Apa arti 'Labbaik'?",
        "options": ["Terima kasih", "Aku datang memenuhi panggilan-Mu", "Selamat datang", "Semoga berkah"],
        "correct": 1,
        "explanation": "'Labbaik' artinya 'Aku datang memenuhi panggilan-Mu', diucapkan saat talbiyah."
    },
    {
        "question": "Kapan waktu terbaik untuk umrah dari segi biaya?",
        "options": ["Ramadhan", "Musim haji", "Januari-Februari", "Juni-Juli"],
        "correct": 2,
        "explanation": "Januari-Februari adalah low season dengan harga lebih terjangkau."
    },
]

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title=f"{BRAND['name']} - {BRAND['description']}",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# OPTIMIZED CSS (Lightweight)
# ============================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Noto+Naskh+Arabic:wght@500;700&display=swap');
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['black']} 0%, #2D2D2D 100%);
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%);
        color: {COLORS['black']};
        border: none;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }}
    
    [data-testid="stMetricValue"] {{
        color: {COLORS['gold']} !important;
        font-weight: 700;
    }}
    
    .labbaik-hero {{
        background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }}
    .labbaik-arabic {{
        font-family: 'Noto Naskh Arabic', serif;
        font-size: 2.5rem;
        color: {COLORS['gold']};
    }}
    .feature-card {{
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 2px solid #E0E0E0;
        transition: all 0.3s ease;
        height: 100%;
    }}
    .feature-card:hover {{
        border-color: {COLORS['gold']};
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.15);
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# UTILITY FUNCTIONS
# ============================================
def format_currency(amount, currency="Rp"):
    return f"{currency} {amount:,.0f}".replace(",", ".")

def generate_referral_code(user_id):
    hash_str = hashlib.md5(str(user_id).encode()).hexdigest()[:8].upper()
    return f"LBK{hash_str}"

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def init_session_state():
    defaults = {
        "initialized": False,
        "chat_history": [],
        "current_scenario": None,
        "auth": {"ok": False, "user": None},
        "users_db": {},
        "engagement": {
            "points": 0,
            "level": 1,
            "streak": 0,
            "badges": ["newcomer"],
            "daily_claimed": False,
            "referral_count": 0,
            "quiz_completed": []
        },
        "checklist_state": {},
        "savings_data": {"target": 35000000, "current": 5000000},
        "departure_date": None,
        "visitor_count": 1250,
        "page_views": {"_total": 3500},  # Dictionary with base count
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def init_engagement():
    if "engagement" not in st.session_state:
        st.session_state.engagement = {
            "points": 0, "level": 1, "streak": 0,
            "badges": ["newcomer"], "daily_claimed": False,
            "referral_count": 0, "quiz_completed": [],
            "last_login": None, "stats": {
                "simulations": 0, "plans_created": 0,
                "shares": 0, "articles_read": 0
            }
        }

def get_user_level(points):
    """Get user level based on points"""
    current_level = LEVELS[0]
    for level in LEVELS:
        if points >= level["min_points"]:
            current_level = level
        else:
            break
    return current_level

def get_next_level(current_level):
    """Get next level info"""
    for i, level in enumerate(LEVELS):
        if level["level"] == current_level["level"]:
            if i < len(LEVELS) - 1:
                return LEVELS[i + 1]
    return None

def calculate_level_progress(points, current_level):
    """Calculate progress to next level"""
    next_level = get_next_level(current_level)
    if next_level is None:
        return 100
    current_min = current_level["min_points"]
    next_min = next_level["min_points"]
    progress = (points - current_min) / (next_min - current_min) * 100
    return min(100, max(0, progress))

def award_points(amount, reason=""):
    init_engagement()
    st.session_state.engagement["points"] += amount
    points = st.session_state.engagement["points"]
    
    # Check level up using new system
    new_level = get_user_level(points)
    old_level_num = st.session_state.engagement["level"]
    
    if new_level["level"] > old_level_num:
        st.session_state.engagement["level"] = new_level["level"]
        st.toast(f"🎉 Level Up! Sekarang {new_level['icon']} {new_level['name']}")
    
    # Check badges
    for badge_id, badge in BADGES.items():
        if points >= badge["points"] and badge_id not in st.session_state.engagement["badges"]:
            st.session_state.engagement["badges"].append(badge_id)
            st.toast(f"🏅 Badge Baru: {badge['icon']} {badge['name']}")

# ============================================
# AUTHENTICATION SYSTEM (with Offline Fallback)
# ============================================
def is_logged_in():
    return st.session_state.get("auth", {}).get("ok", False)

def get_current_user():
    return st.session_state.get("auth", {}).get("user")

def login(email, password):
    # Check default admin first
    if email == DEFAULT_ADMIN["email"] and password == DEFAULT_ADMIN["password"]:
        st.session_state.auth = {
            "ok": True,
            "user": {
                "id": 1,
                "email": DEFAULT_ADMIN["email"],
                "name": DEFAULT_ADMIN["name"],
                "role": DEFAULT_ADMIN["role"],
            }
        }
        return True, "Login berhasil!"
    
    # Check session-based users
    if email in st.session_state.users_db:
        user = st.session_state.users_db[email]
        if user["password"] == password:
            st.session_state.auth = {"ok": True, "user": user}
            return True, "Login berhasil!"
    
    return False, "Email/password salah"

def register(email, password, name):
    if email in st.session_state.users_db:
        return False, "Email sudah terdaftar"
    
    user = {
        "id": len(st.session_state.users_db) + 2,
        "email": email,
        "password": password,
        "name": name,
        "role": "admin" if "admin" in email else "user",
    }
    st.session_state.users_db[email] = user
    st.session_state.auth = {"ok": True, "user": user}
    return True, "Registrasi berhasil!"

def logout():
    st.session_state.auth = {"ok": False, "user": None}

def get_role_info(role):
    roles = {
        "admin": {"name": "Admin", "icon": "👑", "color": "#D4AF37", "badge": "👑"},
        "user": {"name": "Member", "icon": "👤", "color": "#4CAF50", "badge": "🌟"},
    }
    return roles.get(role, roles["user"])

# ============================================
# SCENARIO PLANNER
# ============================================
class ScenarioPlanner:
    BASE_PRICES = {
        "flight": 8000000, "visa": 1500000,
        "hotel_3star": 800000, "hotel_4star": 1500000, "hotel_5star": 3000000,
        "transport": 500000, "meals": 300000,
    }
    
    SCENARIO_CONFIGS = {
        "ekonomis": {"multiplier": 1.0, "hotel_star": 3, "features": [
            "Hotel bintang 3 (±500m dari Haram)", "Penerbangan ekonomi (transit)",
            "Bus transportasi bersama", "Makan 3x sehari (catering)"
        ]},
        "standard": {"multiplier": 1.3, "hotel_star": 4, "features": [
            "Hotel bintang 4 (±300m dari Haram)", "Penerbangan ekonomi (direct)",
            "Bus AC eksklusif", "Makan 3x sehari (prasmanan)"
        ]},
        "premium": {"multiplier": 1.8, "hotel_star": 5, "features": [
            "Hotel bintang 5 (±100m dari Haram)", "Penerbangan bisnis class",
            "Private car per keluarga", "Makan 3x sehari (fine dining)"
        ]},
        "vip": {"multiplier": 2.5, "hotel_star": 5, "features": [
            "Hotel bintang 5 (view Ka'bah)", "Penerbangan first class",
            "Limousine service", "Makan premium + room service"
        ]}
    }
    
    def create_scenario(self, scenario_type="standard", num_people=1, duration_days=9, departure_month=None):
        config = self.SCENARIO_CONFIGS.get(scenario_type, self.SCENARIO_CONFIGS["standard"])
        multiplier = config["multiplier"]
        
        flight = self.BASE_PRICES["flight"] * multiplier
        visa = self.BASE_PRICES["visa"]
        hotel = self.BASE_PRICES[f"hotel_{config['hotel_star']}star"] * duration_days
        transport = self.BASE_PRICES["transport"] * duration_days
        meals = self.BASE_PRICES["meals"] * duration_days * multiplier
        
        per_person = flight + visa + hotel + transport + meals
        total = per_person * num_people
        
        # Season adjustment
        season_mult = 1.0
        if departure_month in [3, 6, 7, 12]:
            season_mult = 1.3
        elif departure_month in [1, 2, 9, 10]:
            season_mult = 0.9
        
        total *= season_mult
        
        return type('Scenario', (), {
            'name': SCENARIO_TEMPLATES[scenario_type]["name"],
            'scenario_type': scenario_type,
            'num_people': num_people,
            'duration_days': duration_days,
            'total': total,
            'per_person': total / num_people,
            'estimated_min': total * 0.9,
            'estimated_max': total * 1.1,
            'features': config["features"],
            'hotel_star': config["hotel_star"],
        })()
    
    def compare_scenarios(self, num_people=1, duration_days=9):
        return [self.create_scenario(s, num_people, duration_days) for s in ["ekonomis", "standard", "premium", "vip"]]

# ============================================
# RENDER FUNCTIONS - SIDEBAR
# ============================================
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 10px; border-bottom: 1px solid #333;">
            <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.8rem; color: {COLORS['gold']};">{BRAND['arabic']}</div>
            <div style="font-size: 1.2rem; font-weight: 700; letter-spacing: 0.2em; margin-top: 5px;">{BRAND['name']}</div>
            <div style="font-size: 0.75rem; color: {COLORS['sand']}; margin-top: 5px;">{BRAND['tagline']}</div>
            <span style="background: {COLORS['gold']}; color: {COLORS['black']}; padding: 2px 10px; border-radius: 10px; font-size: 0.7rem; font-weight: 600;">v{BRAND['version']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # User badge
        user = get_current_user()
        if user:
            role_info = get_role_info(user.get("role", "user"))
            st.markdown(f"""
            <div style="background: {role_info['color']}30; border: 2px solid {role_info['color']}; border-radius: 10px; padding: 15px; text-align: center; margin: 10px 0;">
                <div style="font-size: 2rem;">{role_info['badge']}</div>
                <div style="font-weight: 700;">{user['name']}</div>
                <div style="color: {role_info['color']}; font-size: 0.8rem;">{role_info['name']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        else:
            st.markdown("""
            <div style="background: #333; border: 2px solid #D4AF37; border-radius: 10px; padding: 15px; text-align: center; margin: 10px 0;">
                <div style="font-size: 2rem;">👤</div>
                <div>Guest User</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔑 Login / Register", type="primary", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
        
        st.markdown("---")
        
        # Navigation
        if not is_logged_in():
            nav_items = ["🏠 Beranda", "🕋 Umrah Mandiri", "ℹ️ Tentang"]
        else:
            nav_items = [
                "🏠 Beranda", "💰 Simulasi Biaya", "📋 Buat Rencana", "💵 Cari by Budget",
                "🤝 Umrah Bareng", "🕋 Umrah Mandiri", "📊 Perbandingan", "📅 Waktu Terbaik",
                "🤖 AI Chat", "🧰 Tools & Fitur", "🎮 Rewards & Quiz", "👤 Profil", "ℹ️ Tentang"
            ]
        
        page = st.radio("📍 Navigasi", nav_items, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; font-size: 0.7rem; color: #666;">
            © 2025 {BRAND['name']}<br>Made with ❤️ by MS Hadianto
        </div>
        """, unsafe_allow_html=True)
        
        return page

# ============================================
# RENDER FUNCTIONS - MAIN PAGES
# ============================================
def render_home():
    st.markdown(f"""
    <div class="labbaik-hero">
        <div class="labbaik-arabic">{BRAND['talbiyah']}</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: white; letter-spacing: 0.3em; margin: 10px 0;">{BRAND['name']}</div>
        <div style="color: {COLORS['sand']};">{BRAND['tagline']}</div>
        <p style="color: {COLORS['sand']}; margin-top: 10px;">{BRAND['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats bar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🤖 AI Assistant", "24/7")
    with col2:
        st.metric("🏙️ Kota", "10+")
    with col3:
        st.metric("📊 Skenario", "5+")
    with col4:
        st.metric("🆓 Akses", "GRATIS")
    
    if not is_logged_in():
        st.markdown(f"""
        <div style="background: {COLORS['gold']}20; border: 2px solid {COLORS['gold']}; border-radius: 15px; padding: 25px; text-align: center; margin: 20px 0;">
            <h3 style="color: {COLORS['black']};">🔐 Login untuk Akses Penuh</h3>
            <p>Daftar GRATIS untuk semua fitur perencanaan umrah</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔑 Login / Register Sekarang", type="primary", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
    else:
        user = get_current_user()
        st.success(f"Assalamualaikum, **{user.get('name', 'User')}**! Selamat merencanakan umrah.")
    
    # Features grid
    st.markdown("### ✨ Fitur Utama")
    features = [
        ("🤖", "AI Assistant", "Tanya apapun tentang umrah"),
        ("💰", "Simulasi Biaya", "Hitung estimasi biaya"),
        ("📊", "Perbandingan", "Bandingkan paket"),
        ("🤝", "Umrah Bareng", "Cari teman perjalanan"),
        ("📿", "Doa & Manasik", "Panduan lengkap ibadah"),
        ("✅", "Checklist", "Persiapan perjalanan"),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-weight: 700; margin: 5px 0;">{title}</div>
                <div style="font-size: 0.85rem; color: #666;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

def render_login_page():
    st.header("🔑 Login / Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="email@example.com")
            password = st.text_input("Password", type="password", placeholder="********")
            submitted = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if submitted:
                success, msg = login(email, password)
                if success:
                    st.success(msg)
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error(msg)
    
    with tab2:
        with st.form("register_form"):
            name = st.text_input("Nama Lengkap")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            submitted = st.form_submit_button("📝 Register", use_container_width=True)
            
            if submitted and name and email and password:
                success, msg = register(email, password, name)
                if success:
                    st.success(msg)
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error(msg)

def render_cost_simulation():
    st.header("💰 Simulasi Biaya Umrah")
    
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        with col1:
            scenario = st.selectbox("Skenario Paket", list(SCENARIO_TEMPLATES.keys()), format_func=lambda x: SCENARIO_TEMPLATES[x]["name"])
            num_people = st.number_input("Jumlah Jamaah", 1, 50, 2)
            duration = st.slider("Durasi (hari)", 7, 21, 9)
        with col2:
            departure_city = st.selectbox("Kota Keberangkatan", list(DEPARTURE_CITIES.keys()))
            departure_month = st.selectbox("Bulan", range(1, 13), format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"][x-1])
        
        submitted = st.form_submit_button("🔍 Hitung Biaya", use_container_width=True)
    
    if submitted:
        planner = ScenarioPlanner()
        result = planner.create_scenario(scenario, num_people, duration, departure_month)
        
        award_points(POINTS_CONFIG["complete_simulation"], "Simulasi biaya")
        
        st.markdown("### 📊 Hasil Simulasi")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Minimum", format_currency(result.estimated_min))
        with col2:
            st.metric("Total Maksimum", format_currency(result.estimated_max))
        with col3:
            st.metric("Per Orang", format_currency(result.per_person))
        
        # Chart
        components = [
            {"Komponen": "Tiket Pesawat", "Estimasi": result.total * 0.25},
            {"Komponen": "Hotel", "Estimasi": result.total * 0.35},
            {"Komponen": "Makan", "Estimasi": result.total * 0.15},
            {"Komponen": "Transportasi", "Estimasi": result.total * 0.10},
            {"Komponen": "Visa & Lainnya", "Estimasi": result.total * 0.15},
        ]
        fig = px.pie(pd.DataFrame(components), values="Estimasi", names="Komponen", title="Distribusi Biaya")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### ✨ Fasilitas Termasuk")
        for f in result.features:
            st.markdown(f"✅ {f}")

def render_budget_finder():
    st.header("💵 Cari Paket Sesuai Budget")
    
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("💰 Budget Anda (Rp)", 10_000_000, 500_000_000, 35_000_000, step=1_000_000)
    with col2:
        num_people = st.number_input("👥 Jumlah Jamaah", 1, 50, 1)
    
    budget_per_person = budget / num_people
    st.markdown(f"""
    <div style="background: {COLORS['black']}; padding: 15px; border-radius: 10px; text-align: center; margin: 15px 0;">
        <div style="color: {COLORS['sand']}; font-size: 0.85rem;">Budget Per Orang</div>
        <div style="color: {COLORS['gold']}; font-size: 1.8rem; font-weight: 700;">Rp {budget_per_person:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Find suitable packages
    planner = ScenarioPlanner()
    available = []
    for scenario_type in ["ekonomis", "standard", "premium", "vip"]:
        result = planner.create_scenario(scenario_type, 1, 9)
        if result.per_person <= budget_per_person:
            available.append(result)
    
    if available:
        st.success(f"✅ **{len(available)} Paket Tersedia** untuk budget Anda!")
        for pkg in available:
            with st.expander(f"📦 {pkg.name} - Rp {pkg.per_person:,.0f}/orang"):
                st.markdown(f"**Hotel:** ⭐ {pkg.hotel_star}")
                st.markdown(f"**Durasi:** {pkg.duration_days} hari")
                for f in pkg.features:
                    st.markdown(f"✅ {f}")
    else:
        st.warning("⚠️ Budget belum mencukupi. Minimum Rp 20 juta per orang untuk Paket Ekonomis.")

def render_create_plan():
    """Render create plan page with Makkah/Madinah duration selection"""
    st.header("📋 Buat Rencana Umrah Lengkap")
    st.markdown("Susun rencana perjalanan umrah dengan estimasi biaya detail per komponen.")
    
    st.markdown("### 📝 Detail Perjalanan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario = st.selectbox("Skenario Paket", list(SCENARIO_TEMPLATES.keys()), 
                               format_func=lambda x: SCENARIO_TEMPLATES[x]["name"], key="plan_scenario")
        num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=2, key="plan_num_people")
        departure_city = st.selectbox("Kota Keberangkatan", list(DEPARTURE_CITIES.keys()))
        
        months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        departure_month = st.selectbox("Bulan Keberangkatan", range(1, 13), 
                                       format_func=lambda x: months[x-1], key="plan_month")
    
    with col2:
        st.markdown("#### 🕋 Durasi Menginap")
        nights_makkah = st.slider("🕋 Lama di Mekkah (malam)", min_value=2, max_value=10, value=4, 
                                  key="nights_makkah", help="Pilih jumlah malam menginap di Mekkah")
        nights_madinah = st.slider("🕌 Lama di Madinah (malam)", min_value=2, max_value=10, value=3, 
                                   key="nights_madinah", help="Pilih jumlah malam menginap di Madinah")
        total_duration = nights_makkah + nights_madinah + 2
        st.info(f"📅 **Total Durasi:** {total_duration} hari ({nights_makkah} malam Mekkah + {nights_madinah} malam Madinah + 2 hari transit)")
    
    st.markdown("---")
    st.markdown("### 💰 Preview Biaya Akomodasi")
    
    hotel_makkah = HOTEL_PRICES[scenario]["makkah"]
    hotel_madinah = HOTEL_PRICES[scenario]["madinah"]
    additional = ADDITIONAL_COSTS[scenario]
    
    cost_makkah = hotel_makkah["price"] * nights_makkah
    cost_madinah = hotel_madinah["price"] * nights_madinah
    cost_accommodation = cost_makkah + cost_madinah
    
    col1, col2, col3 = st.columns(3)
    
    # Build hotel cards HTML separately to avoid f-string issues
    with col1:
        makkah_html = f'''
        <div style="background: #fff3e0; padding: 15px; border-radius: 10px; border-left: 4px solid #e65100;">
            <div style="font-weight: 700; color: #e65100; margin-bottom: 8px;">🕋 Hotel Mekkah</div>
            <div style="font-size: 0.85rem; color: #666; margin-bottom: 5px;">{hotel_makkah["name"]}</div>
            <div style="font-size: 0.8rem; color: #888;">Rp {hotel_makkah["price"]:,}/malam × {nights_makkah} malam</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #e65100; margin-top: 8px;">Rp {cost_makkah:,}</div>
        </div>
        '''
        st.markdown(makkah_html, unsafe_allow_html=True)
    
    with col2:
        madinah_html = f'''
        <div style="background: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 4px solid #2e7d32;">
            <div style="font-weight: 700; color: #2e7d32; margin-bottom: 8px;">🕌 Hotel Madinah</div>
            <div style="font-size: 0.85rem; color: #666; margin-bottom: 5px;">{hotel_madinah["name"]}</div>
            <div style="font-size: 0.8rem; color: #888;">Rp {hotel_madinah["price"]:,}/malam × {nights_madinah} malam</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #2e7d32; margin-top: 8px;">Rp {cost_madinah:,}</div>
        </div>
        '''
        st.markdown(madinah_html, unsafe_allow_html=True)
    
    with col3:
        total_accommodation = cost_accommodation * num_people
        total_html = f'''
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 15px; border-radius: 10px;">
            <div style="font-weight: 700; color: #D4AF37; margin-bottom: 8px;">💰 Total Akomodasi</div>
            <div style="font-size: 0.85rem; color: #C9A86C; margin-bottom: 5px;">Per orang: Rp {cost_accommodation:,}</div>
            <div style="font-size: 0.8rem; color: #888;">× {num_people} jamaah</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #D4AF37; margin-top: 8px;">Rp {total_accommodation:,}</div>
        </div>
        '''
        st.markdown(total_html, unsafe_allow_html=True)
    
    st.markdown("---")
    special_requests = st.text_area("Permintaan Khusus (opsional)", 
                                     placeholder="Misal: jamaah lansia, butuh kursi roda, vegetarian, dll.")
    
    if st.button("🚀 Buat Rencana Lengkap", use_container_width=True, type="primary"):
        # Calculate all costs
        flight_cost = additional["flight"]
        visa_cost = additional["visa"]
        transport_cost = additional["transport"]
        meals_cost = additional["meals"] * total_duration
        
        total_per_person = cost_accommodation + flight_cost + visa_cost + transport_cost + meals_cost
        grand_total = total_per_person * num_people
        
        # Apply season multiplier
        season_multiplier = 1.0
        season_name = "Regular"
        for season_key, season in SEASONS.items():
            if departure_month in season["months"]:
                season_multiplier = season["multiplier"]
                season_name = season["name"]
                break
        
        total_per_person_adjusted = int(total_per_person * season_multiplier)
        grand_total_adjusted = int(grand_total * season_multiplier)
        
        st.success("✅ Rencana berhasil dibuat!")
        award_points(POINTS_CONFIG["create_plan"], "Buat Rencana Umrah")
        
        st.markdown("### 📊 Ringkasan Perjalanan")
        sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
        with sum_col1:
            st.metric("👥 Jamaah", f"{num_people} orang")
        with sum_col2:
            st.metric("🕋 Mekkah", f"{nights_makkah} malam")
        with sum_col3:
            st.metric("🕌 Madinah", f"{nights_madinah} malam")
        with sum_col4:
            st.metric("📅 Total", f"{total_duration} hari")
        
        if season_multiplier != 1.0:
            if season_multiplier > 1:
                st.warning(f"⚠️ **{season_name}**: Harga naik {int((season_multiplier-1)*100)}% di bulan ini")
            else:
                st.success(f"🎉 **{season_name}**: Hemat {int((1-season_multiplier)*100)}% di bulan ini!")
        
        st.markdown("### 💰 Rincian Biaya Per Orang")
        
        cost_items = [
            ("✈️ Tiket Pesawat PP", flight_cost),
            ("🕋 Hotel Mekkah", cost_makkah),
            ("🕌 Hotel Madinah", cost_madinah),
            ("📄 Visa & Handling", visa_cost),
            ("🚐 Transportasi Lokal", transport_cost),
            (f"🍽️ Makan ({total_duration} hari)", meals_cost),
        ]
        
        for item_name, item_cost in cost_items:
            item_html = f'''
            <div style="display: flex; justify-content: space-between; padding: 8px 12px; 
                        background: #f9f9f9; border-radius: 5px; margin: 4px 0;">
                <span>{item_name}</span>
                <span style="font-weight: 600;">Rp {item_cost:,}</span>
            </div>
            '''
            st.markdown(item_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        total_col1, total_col2 = st.columns(2)
        with total_col1:
            perperson_html = f'''
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 0.9rem; color: #1565c0;">Per Orang</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #1565c0;">Rp {total_per_person_adjusted:,}</div>
            </div>
            '''
            st.markdown(perperson_html, unsafe_allow_html=True)
        with total_col2:
            grandtotal_html = f'''
            <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 0.9rem; color: #D4AF37;">GRAND TOTAL ({num_people} orang)</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #D4AF37;">Rp {grand_total_adjusted:,}</div>
            </div>
            '''
            st.markdown(grandtotal_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📋 Checklist Persiapan")
        
        checklist = [
            ("📄 Dokumen", ["Paspor (min. 6 bulan)", "Visa Umrah", "Tiket Pesawat", "Voucher Hotel"]),
            ("🧳 Pakaian", ["Ihram (pria)", "Mukena (wanita)", "Pakaian harian", "Sandal nyaman"]),
            ("💊 Kesehatan", ["Obat pribadi", "Masker", "Hand sanitizer", "Vitamin"]),
        ]
        
        for category, items in checklist:
            st.markdown(f"**{category}**")
            for item in items:
                st.checkbox(item, key=f"check_{item}")

def render_scenario_comparison():
    st.header("📊 Perbandingan Skenario")
    
    col1, col2 = st.columns(2)
    with col1:
        num_people = st.number_input("Jumlah Jamaah", 1, 50, 1)
    with col2:
        duration = st.slider("Durasi (hari)", 7, 21, 9)
    
    if st.button("🔍 Bandingkan Semua", use_container_width=True):
        planner = ScenarioPlanner()
        scenarios = planner.compare_scenarios(num_people, duration)
        
        data = []
        for s in scenarios:
            data.append({
                "Skenario": s.name,
                "Hotel": f"⭐ {s.hotel_star}",
                "Min (Rp)": s.estimated_min,
                "Max (Rp)": s.estimated_max,
            })
        
        st.dataframe(pd.DataFrame(data).style.format({"Min (Rp)": "{:,.0f}", "Max (Rp)": "{:,.0f}"}), use_container_width=True)
        
        # Bar chart
        fig = px.bar(pd.DataFrame(data), x="Skenario", y="Max (Rp)", color="Skenario", title="Perbandingan Harga")
        st.plotly_chart(fig, use_container_width=True)

def render_time_analysis():
    """Render time analysis page - best time for umrah"""
    st.header("📅 Analisis Waktu Terbaik Umrah")
    
    st.markdown("Temukan waktu terbaik untuk umrah berdasarkan harga, cuaca, dan keramaian.")
    
    priority = st.selectbox(
        "Prioritas Anda",
        ["balanced", "cost", "crowd"],
        format_func=lambda x: {
            "balanced": "🎯 Seimbang (Harga & Keramaian)",
            "cost": "💰 Prioritas Hemat Biaya",
            "crowd": "👥 Prioritas Hindari Keramaian"
        }[x]
    )
    
    if st.button("📊 Analisis Waktu Terbaik", use_container_width=True):
        # Month analysis data
        months_data = [
            {"month": 1, "name": "Januari", "price": 0.85, "crowd": "Rendah", "weather": "Sejuk (15-25°C)", "score": 85},
            {"month": 2, "name": "Februari", "price": 0.85, "crowd": "Rendah", "weather": "Sejuk (16-26°C)", "score": 85},
            {"month": 3, "name": "Maret", "price": 1.2, "crowd": "Sedang", "weather": "Hangat (20-30°C)", "score": 70},
            {"month": 4, "name": "April", "price": 1.0, "crowd": "Sedang", "weather": "Hangat (22-32°C)", "score": 75},
            {"month": 5, "name": "Mei", "price": 1.0, "crowd": "Sedang", "weather": "Panas (25-38°C)", "score": 65},
            {"month": 6, "name": "Juni", "price": 1.3, "crowd": "Tinggi", "weather": "Panas (28-42°C)", "score": 50},
            {"month": 7, "name": "Juli", "price": 1.4, "crowd": "Tinggi", "weather": "Sangat Panas (30-45°C)", "score": 40},
            {"month": 8, "name": "Agustus", "price": 1.0, "crowd": "Sedang", "weather": "Sangat Panas (30-44°C)", "score": 55},
            {"month": 9, "name": "September", "price": 0.9, "crowd": "Rendah", "weather": "Panas (28-40°C)", "score": 70},
            {"month": 10, "name": "Oktober", "price": 0.85, "crowd": "Rendah", "weather": "Hangat (24-35°C)", "score": 80},
            {"month": 11, "name": "November", "price": 0.85, "crowd": "Rendah", "weather": "Sejuk (20-30°C)", "score": 85},
            {"month": 12, "name": "Desember", "price": 1.3, "crowd": "Tinggi", "weather": "Sejuk (15-25°C)", "score": 60},
        ]
        
        # Adjust scores based on priority
        if priority == "cost":
            for m in months_data:
                m["score"] = int(100 - (m["price"] - 0.85) * 100)
        elif priority == "crowd":
            crowd_scores = {"Rendah": 90, "Sedang": 60, "Tinggi": 30}
            for m in months_data:
                m["score"] = crowd_scores.get(m["crowd"], 50)
        
        # Sort by score
        sorted_months = sorted(months_data, key=lambda x: x["score"], reverse=True)
        
        # Best months
        st.markdown("### ✅ Bulan Terbaik untuk Umrah")
        cols = st.columns(3)
        for i, month in enumerate(sorted_months[:3]):
            with cols[i]:
                st.markdown(f'''
                <div style="background: linear-gradient(135deg, #006B3C20 0%, #006B3C10 100%); 
                            border-left: 4px solid #006B3C; padding: 15px; border-radius: 0 10px 10px 0;">
                    <h4 style="color: #006B3C; margin: 0;">#{i+1} {month["name"]}</h4>
                    <p style="margin: 8px 0; font-size: 0.9rem;">🌡️ {month["weather"]}</p>
                    <p style="margin: 5px 0; font-size: 0.85rem;">💰 Multiplier: {month["price"]}x</p>
                    <p style="margin: 5px 0; font-size: 0.85rem;">👥 Keramaian: {month["crowd"]}</p>
                    <p style="margin: 5px 0; font-size: 0.85rem;">⭐ Skor: {month["score"]}/100</p>
                </div>
                ''', unsafe_allow_html=True)
        
        # Months to avoid
        st.markdown("### ⚠️ Bulan yang Perlu Dipertimbangkan")
        cols = st.columns(3)
        for i, month in enumerate(sorted_months[-3:]):
            with cols[i]:
                st.markdown(f'''
                <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; border-radius: 0 10px 10px 0;">
                    <h4 style="color: #e65100; margin: 0;">{month["name"]}</h4>
                    <p style="margin: 8px 0; font-size: 0.9rem;">🌡️ {month["weather"]}</p>
                    <p style="margin: 5px 0; font-size: 0.85rem;">💰 Multiplier: {month["price"]}x</p>
                    <p style="margin: 5px 0; font-size: 0.85rem;">👥 Keramaian: {month["crowd"]}</p>
                </div>
                ''', unsafe_allow_html=True)
        
        # Year chart
        st.markdown("### 📈 Skor Rekomendasi Sepanjang Tahun")
        df = pd.DataFrame(months_data)
        fig = px.line(df, x="name", y="score", title="Skor Rekomendasi per Bulan", markers=True)
        fig.update_layout(xaxis_title="Bulan", yaxis_title="Skor Rekomendasi")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tips
        st.markdown("### 💡 Tips Memilih Waktu")
        tips = [
            "📅 **Booking 3-4 bulan sebelumnya** untuk harga terbaik",
            "🌙 **Hindari Ramadhan** jika budget terbatas (harga naik 40-50%)",
            "☀️ **Perhatikan cuaca** - musim panas bisa mencapai 45°C",
            "👥 **Low season** (Jan-Feb, Sep-Nov) lebih nyaman untuk ibadah",
            "🎒 **Bawa perlengkapan** sesuai cuaca saat keberangkatan",
        ]
        for tip in tips:
            st.markdown(f"• {tip}")

def render_ai_chat():
    """Render AI chat page with quick questions"""
    st.header("🤖 Chat dengan AI Assistant")
    
    st.markdown("Tanyakan apa saja tentang umrah kepada AI Assistant!")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ketik pertanyaan Anda..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Simple AI response (without external API for lightweight)
        with st.spinner("🤔 AI sedang berpikir..."):
            ai_response = get_ai_response(prompt)
        
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").write(ai_response)
    
    # Quick questions
    st.markdown("---")
    st.markdown("### 💡 Pertanyaan Cepat")
    
    quick_questions = [
        "Apa saja rukun umrah?",
        "Bagaimana tips hemat biaya umrah?",
        "Kapan waktu terbaik untuk umrah?",
        "Apa yang harus dipersiapkan sebelum umrah?",
        "Bagaimana memilih travel umrah yang terpercaya?",
    ]
    
    cols = st.columns(2)
    for i, q in enumerate(quick_questions):
        if cols[i % 2].button(q, key=f"quick_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.rerun()
    
    # Clear chat
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.chat_history = []
        st.rerun()

def get_ai_response(question: str) -> str:
    """Get AI response - lightweight built-in knowledge base"""
    question_lower = question.lower()
    
    # Knowledge base for common questions
    if "rukun" in question_lower:
        return """**Rukun Umrah ada 5:**

1. **Ihram** - Niat dan memakai pakaian ihram dari miqat
2. **Thawaf** - Mengelilingi Ka'bah 7 kali
3. **Sa'i** - Berjalan antara Shafa dan Marwah 7 kali
4. **Tahallul** - Mencukur/memotong rambut
5. **Tertib** - Melakukan rukun secara berurutan

💡 Tips: Pelajari tata cara setiap rukun sebelum berangkat agar ibadah lebih khusyuk."""
    
    elif "hemat" in question_lower or "budget" in question_lower or "murah" in question_lower:
        return """**Tips Hemat Biaya Umrah:**

💰 **Waktu Keberangkatan:**
- Pilih low season (Jan-Feb, Sep-Nov)
- Hindari Ramadhan & liburan sekolah

✈️ **Tiket Pesawat:**
- Booking 3-4 bulan sebelumnya
- Pilih penerbangan transit (lebih murah)
- Pantau promo airlines

🏨 **Hotel:**
- Pilih hotel 500m-1km dari Haram
- Sharing room dengan jamaah lain

📦 **Paket:**
- Bandingkan minimal 3 travel agent
- Pilih paket grup (lebih ekonomis)

Estimasi paket ekonomis: **Rp 20-25 juta/orang**"""
    
    elif "waktu" in question_lower or "kapan" in question_lower or "bulan" in question_lower:
        return """**Waktu Terbaik untuk Umrah:**

✅ **Rekomendasi Terbaik:**
- **Januari-Februari**: Cuaca sejuk, harga rendah
- **September-November**: Low season, nyaman

⚠️ **Perlu Pertimbangan:**
- **Juni-Juli**: Sangat panas (40-45°C)
- **Ramadhan**: Harga naik 40-50%, sangat ramai
- **Desember**: Liburan, harga naik

💡 Tips: Gunakan fitur Analisis Waktu di menu untuk rekomendasi personal!"""
    
    elif "persiap" in question_lower or "bawa" in question_lower or "perlengkapan" in question_lower:
        return """**Persiapan Sebelum Umrah:**

📄 **Dokumen:**
- Paspor (min. 6 bulan berlaku)
- Visa umrah
- Tiket & voucher hotel
- Foto 4x6 (10 lembar)

🧳 **Pakaian:**
- Ihram 2 set (pria)
- Mukena (wanita)
- Pakaian nyaman & sopan
- Sandal jepit

💊 **Kesehatan:**
- Vaksin meningitis
- Obat-obatan pribadi
- Vitamin & suplemen

📱 **Digital:**
- Install app: Eatmarna, Tawakkalna
- SIM card lokal/roaming
- Power bank

💡 Gunakan fitur Checklist di menu Tools untuk memastikan tidak ada yang terlewat!"""
    
    elif "travel" in question_lower or "agen" in question_lower or "terpercaya" in question_lower:
        return """**Tips Memilih Travel Umrah Terpercaya:**

✅ **Wajib Dicek:**
1. Terdaftar di **Kemenag** (siskopatuh.kemenag.go.id)
2. Memiliki **PPIU** (Penyelenggara Perjalanan Ibadah Umrah)
3. Jelas alamat kantor & kontak

📋 **Pertanyaan Penting:**
- Sudah berapa lama beroperasi?
- Berapa jamaah yang sudah diberangkatkan?
- Ada testimoni dari jamaah sebelumnya?
- Jelas rincian biaya & fasilitas?

⚠️ **Red Flags:**
- Harga terlalu murah
- Tidak mau kasih rincian biaya
- Tidak ada alamat kantor jelas
- Desak-desakan untuk DP

💡 Bandingkan minimal 3 travel agent sebelum memutuskan!"""
    
    else:
        return f"""Terima kasih atas pertanyaan Anda tentang: **"{question}"**

Saya adalah AI Assistant LABBAIK yang siap membantu perencanaan umrah Anda.

**Topik yang bisa saya bantu:**
- 📿 Rukun dan tata cara umrah
- 💰 Tips hemat biaya
- 📅 Waktu terbaik berangkat
- 🧳 Persiapan & perlengkapan
- ✈️ Tips memilih travel agent

Silakan ajukan pertanyaan yang lebih spesifik, atau gunakan tombol **Pertanyaan Cepat** di bawah!

💡 *Untuk informasi lebih lengkap, gunakan fitur Tools & Fitur di menu.*"""

def render_tools_features():
    st.header("🧰 Tools & Fitur")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["💰 Tabungan", "⏰ Countdown", "📿 Doa & Manasik", "✅ Checklist", "📞 Darurat", "💱 Kurs", "🌡️ Cuaca"])
    
    # Tab 1: Savings Calculator
    with tab1:
        st.subheader("💰 Kalkulator Tabungan")
        col1, col2 = st.columns(2)
        with col1:
            target = st.number_input("🎯 Target Biaya Umrah", 10_000_000, 200_000_000, 35_000_000, step=1_000_000)
            current = st.number_input("💵 Tabungan Saat Ini", 0, 200_000_000, 5_000_000, step=500_000)
        with col2:
            target_date = st.date_input("📅 Target Berangkat", datetime.now() + timedelta(days=365))
        
        remaining = target - current
        days_left = (target_date - datetime.now().date()).days
        
        if days_left > 0 and remaining > 0:
            daily = remaining / days_left
            weekly = remaining / (days_left / 7)
            monthly = remaining / (days_left / 30)
            
            progress = (current / target) * 100
            st.progress(min(progress / 100, 1.0))
            st.markdown(f"**Progress: {progress:.1f}%** - Kurang **Rp {remaining:,.0f}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📅 Per Hari", f"Rp {daily:,.0f}")
            with col2:
                st.metric("📆 Per Minggu", f"Rp {weekly:,.0f}")
            with col3:
                st.metric("🗓️ Per Bulan", f"Rp {monthly:,.0f}")
            
            if monthly > 5_000_000:
                st.warning("⚠️ Target bulanan cukup tinggi. Pertimbangkan perpanjang waktu menabung.")
        elif remaining <= 0:
            st.success("🎉 Alhamdulillah! Target tabungan sudah tercapai!")
            st.balloons()
    
    # Tab 2: Countdown
    with tab2:
        st.subheader("⏰ Countdown Keberangkatan")
        dep_date = st.date_input("📅 Tanggal Berangkat", datetime.now() + timedelta(days=90), key="countdown_date")
        
        days_left = (dep_date - datetime.now().date()).days
        
        if days_left > 0:
            weeks = days_left // 7
            remaining_days = days_left % 7
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <div style="color: {COLORS['gold']}; font-size: 4rem; font-weight: 800;">{days_left}</div>
                <div style="color: white; font-size: 1.2rem;">Hari Menuju Umrah</div>
                <div style="color: {COLORS['sand']}; margin-top: 10px;">{weeks} minggu {remaining_days} hari</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Milestones
            milestones = [
                (90, "H-90: Booking tiket & hotel"),
                (60, "H-60: Apply visa"),
                (30, "H-30: Vaksin meningitis"),
                (14, "H-14: Cek kelengkapan"),
                (7, "H-7: Packing"),
                (3, "H-3: Final check"),
            ]
            st.markdown("**📌 Milestone:**")
            for m_days, m_text in milestones:
                status = "✅" if days_left <= m_days else "⬜"
                st.markdown(f"{status} {m_text}")
        elif days_left == 0:
            st.success("🕋 Hari ini berangkat! Labbaik Allahumma Labbaik!")
            st.balloons()
        else:
            st.info("📅 Tanggal sudah lewat. Pilih tanggal keberangkatan baru.")
    
    # Tab 3: Doa & Manasik with Video Tutorial
    with tab3:
        st.subheader("📿 Doa & Manasik Umrah")
        
        doa_tab, tata_tab, video_tab = st.tabs(["🤲 Doa-doa", "📖 Tata Cara", "🎥 Video Tutorial"])
        
        with doa_tab:
            for key, doa in DOA_MANASIK.items():
                with st.expander(doa["title"]):
                    st.markdown(f"""
                    <div style="background: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                        <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.5rem; text-align: right; color: {COLORS['black']}; line-height: 2;">{doa['arab']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"**Latin:** *{doa['latin']}*")
                    st.markdown(f"**Arti:** {doa['arti']}")
        
        with tata_tab:
            steps = [
                ("1️⃣", "Ihram", "Mandi sunnah, pakai pakaian ihram, niat dari miqat"),
                ("2️⃣", "Talbiyah", "Membaca talbiyah dari miqat sampai thawaf"),
                ("3️⃣", "Thawaf", "7 putaran mengelilingi Ka'bah"),
                ("4️⃣", "Sholat 2 Rakaat", "Di belakang Maqam Ibrahim"),
                ("5️⃣", "Minum Zamzam", "Di area zamzam sambil berdoa"),
                ("6️⃣", "Sa'i", "7 kali antara Shafa dan Marwah"),
                ("7️⃣", "Tahallul", "Potong/cukur rambut, umrah selesai"),
            ]
            for icon, title, desc in steps:
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 15px; padding: 15px; background: #f9f9f9; border-radius: 10px; border-left: 4px solid {COLORS['gold']};">
                    <div style="font-size: 1.5rem; margin-right: 15px;">{icon}</div>
                    <div>
                        <div style="font-weight: 700;">{title}</div>
                        <div style="color: #666; font-size: 0.9rem;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with video_tab:
            st.markdown("#### 🎥 Video Panduan Manasik Umrah")
            st.markdown("Pelajari tata cara manasik dari ulama terpercaya:")
            
            # Featured Video - Ustadz Adi Hidayat
            for video in VIDEO_TUTORIALS:
                if video.get("featured"):
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%); padding: 3px; border-radius: 15px; margin-bottom: 20px;">
                        <div style="background: white; padding: 20px; border-radius: 12px;">
                            <span style="background: {COLORS['gold']}; color: {COLORS['black']}; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">⭐ REKOMENDASI</span>
                            <h4 style="margin: 10px 0 8px 0; color: {COLORS['black']};">{video['title']}</h4>
                            <p style="color: #666; font-size: 0.9rem; margin-bottom: 8px;">{video['description']}</p>
                            <p style="color: {COLORS['gold']}; font-size: 0.85rem; font-weight: 600;">🎤 {video['speaker']} | ⏱️ {video['duration']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.video(video['url'])
                    st.markdown("---")
            
            # Other videos
            st.markdown("#### 📺 Video Lainnya")
            for video in VIDEO_TUTORIALS:
                if not video.get("featured"):
                    with st.expander(f"🎬 {video['title']}"):
                        st.markdown(f"**{video['description']}**")
                        st.markdown(f"🎤 *{video['speaker']}* | ⏱️ {video['duration']}")
                        st.video(video['url'])
            
            st.info("💡 **Tips:** Tonton video beberapa kali sebelum berangkat dan hafalkan doa-doa utama.")
    
    # Tab 4: Checklist
    with tab4:
        st.subheader("✅ Checklist Persiapan Umrah")
        st.caption("🔴 = Wajib | ⚪ = Opsional")
        
        total_items = 0
        checked_items = 0
        
        for cat_key, cat_data in CHECKLIST_DATA.items():
            with st.expander(cat_data["title"], expanded=True):
                for item, required in cat_data["items"]:
                    key = f"check_{cat_key}_{item}"
                    if key not in st.session_state.checklist_state:
                        st.session_state.checklist_state[key] = False
                    
                    total_items += 1
                    marker = "🔴" if required else "⚪"
                    checked = st.checkbox(f"{marker} {item}", value=st.session_state.checklist_state[key], key=key)
                    st.session_state.checklist_state[key] = checked
                    if checked:
                        checked_items += 1
        
        progress = (checked_items / total_items) * 100 if total_items > 0 else 0
        st.progress(progress / 100)
        st.markdown(f"**Progress: {progress:.0f}%** ({checked_items}/{total_items} items)")
        
        if progress == 100:
            st.success("🎉 Alhamdulillah! Semua persiapan lengkap!")
            st.balloons()
    
    # Tab 5: Emergency
    with tab5:
        st.subheader("📞 Kontak Darurat")
        for contact in EMERGENCY_CONTACTS:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: #f9f9f9; border-radius: 10px; margin-bottom: 8px;">
                <span style="font-weight: 600;">{contact['name']}</span>
                <span style="color: {COLORS['gold']}; font-weight: 700;">{contact['phone']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**📱 App Wajib di Saudi:**")
        apps = ["Eatmarna - Booking sholat di Haram", "Tawakkalna - Health app resmi", "Nusuk - Layanan haji & umrah"]
        for app in apps:
            st.markdown(f"• {app}")
    
    # Tab 6: Currency Converter
    with tab6:
        st.subheader("💱 Konverter Mata Uang")
        
        col1, col2 = st.columns(2)
        with col1:
            from_currency = st.selectbox("Dari", ["IDR (Rupiah)", "SAR (Riyal)", "USD (Dollar)"], index=0)
            amount = st.number_input("Jumlah", min_value=0.0, value=1000000.0, step=100000.0, format="%.0f")
        with col2:
            to_currency = st.selectbox("Ke", ["SAR (Riyal)", "IDR (Rupiah)", "USD (Dollar)"], index=0)
        
        from_code = from_currency.split()[0]
        to_code = to_currency.split()[0]
        
        # Convert
        if from_code == to_code:
            result = amount
        elif from_code == "IDR" and to_code == "SAR":
            result = amount * CURRENCY_RATES["IDR_TO_SAR"]
        elif from_code == "SAR" and to_code == "IDR":
            result = amount * CURRENCY_RATES["SAR_TO_IDR"]
        elif from_code == "IDR" and to_code == "USD":
            result = amount * CURRENCY_RATES["IDR_TO_USD"]
        elif from_code == "USD" and to_code == "IDR":
            result = amount * CURRENCY_RATES["USD_TO_IDR"]
        elif from_code == "SAR" and to_code == "USD":
            result = amount * CURRENCY_RATES["SAR_TO_IDR"] * CURRENCY_RATES["IDR_TO_USD"]
        elif from_code == "USD" and to_code == "SAR":
            result = amount * CURRENCY_RATES["USD_TO_IDR"] * CURRENCY_RATES["IDR_TO_SAR"]
        else:
            result = amount
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['green']} 0%, #388E3C 100%); border-radius: 15px; margin: 15px 0;">
            <h2 style="margin: 0; color: white;">{amount:,.0f} {from_code} = {result:,.2f} {to_code}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick reference
        st.markdown("**📊 Referensi Cepat:**")
        ref_col1, ref_col2, ref_col3 = st.columns(3)
        with ref_col1:
            st.metric("1 SAR", f"Rp {CURRENCY_RATES['SAR_TO_IDR']:,.0f}")
        with ref_col2:
            st.metric("1 USD", f"Rp {CURRENCY_RATES['USD_TO_IDR']:,.0f}")
        with ref_col3:
            st.metric("Rp 1 Juta", f"{1000000 * CURRENCY_RATES['IDR_TO_SAR']:,.2f} SAR")
        
        st.caption("⚠️ Kurs bersifat estimasi. Cek kurs terkini sebelum penukaran.")
    
    # Tab 7: Weather Info
    with tab7:
        st.subheader("🌡️ Info Cuaca Makkah & Madinah")
        
        # Chart
        df_weather = pd.DataFrame(WEATHER_DATA)
        fig = px.line(df_weather, x="Bulan", y=["Makkah", "Madinah"], 
                      title="Suhu Rata-rata Bulanan (°C)",
                      markers=True)
        fig.update_layout(yaxis_title="Suhu (°C)", legend_title="Kota")
        st.plotly_chart(fig, use_container_width=True)
        
        # Current month
        current_month = datetime.now().month
        months_id = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                     "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        
        makkah_temp = WEATHER_DATA["Makkah"][current_month - 1]
        madinah_temp = WEATHER_DATA["Madinah"][current_month - 1]
        
        col1, col2 = st.columns(2)
        with col1:
            delta = "🔥 Panas" if makkah_temp > 35 else "☀️ Hangat" if makkah_temp > 28 else "🌤️ Sejuk"
            st.metric(f"🕋 Makkah ({months_id[current_month-1]})", f"{makkah_temp}°C", delta=delta)
        with col2:
            delta = "🔥 Panas" if madinah_temp > 35 else "☀️ Hangat" if madinah_temp > 28 else "🌤️ Sejuk"
            st.metric(f"🕌 Madinah ({months_id[current_month-1]})", f"{madinah_temp}°C", delta=delta)
        
        # Recommendations
        st.markdown("---")
        st.markdown("**👕 Rekomendasi Pakaian:**")
        if makkah_temp > 35:
            st.warning("""
            🌡️ **Cuaca Panas!**
            - Pakai baju tipis & menyerap keringat
            - Bawa payung untuk teduh
            - Minum air minimal 3 liter/hari
            - Hindari aktivitas siang (11:00-15:00)
            - Gunakan sunscreen SPF 50+
            """)
        elif makkah_temp > 28:
            st.info("""
            ☀️ **Cuaca Hangat**
            - Pakaian tipis tapi sopan
            - Jaket tipis untuk AC
            - Tetap bawa payung
            """)
        else:
            st.success("""
            🌤️ **Cuaca Nyaman**
            - Waktu terbaik untuk umrah!
            - Bawa jaket untuk malam hari
            """)

def render_engagement_page():
    st.header("🎮 Rewards & Engagement Center")
    
    init_engagement()
    eng = st.session_state.engagement
    points = eng["points"]
    level = get_user_level(points)
    progress = calculate_level_progress(points, level)
    next_level = get_next_level(level)
    
    # Enhanced Stats Display with Level Progress
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px;
                border: 1px solid {COLORS['gold']}40;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 2.5rem;">{level['icon']}</span>
                <div>
                    <div style="color: {level['color']}; font-weight: 700; font-size: 1.2rem;">{level['name']}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.85rem;">Level {level['level']}</div>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="color: {COLORS['gold']}; font-weight: 800; font-size: 2rem;">{points:,}</div>
                <div style="color: {COLORS['sand']}; font-size: 0.8rem;">LABBAIK Points</div>
            </div>
        </div>
        <div style="background: {COLORS['black']}; border-radius: 10px; height: 10px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, {COLORS['gold']} 0%, {level['color']} 100%); 
                        height: 100%; width: {progress}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
            <span style="color: {COLORS['sand']}; font-size: 0.75rem;">{level['min_points']} LP</span>
            <span style="color: {COLORS['sand']}; font-size: 0.75rem;">
                {f"{next_level['min_points']} LP" if next_level else "MAX LEVEL! 🏆"}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Streak Fire Display
    streak = eng["streak"]
    flame_color = "#FF9800" if streak < 7 else ("#F44336" if streak < 30 else COLORS['gold'])
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
                    padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2.5rem; text-shadow: 0 0 20px {flame_color};">🔥</div>
            <div style="color: white; font-size: 2rem; font-weight: 800;">{streak}</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Hari Berturut</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Daily claim
        if not eng["daily_claimed"]:
            day_index = min(streak, len(DAILY_REWARDS) - 1)
            today_reward = DAILY_REWARDS[day_index]
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {COLORS['black']} 0%, #2D1F3D 100%);
                        border: 2px solid {COLORS['gold']}; border-radius: 15px; padding: 20px; text-align: center;">
                <div style="font-size: 2rem;">🎁</div>
                <div style="color: {COLORS['gold']}; font-size: 1.1rem; font-weight: 700;">Hadiah Hari ke-{streak + 1}</div>
                <div style="color: white; font-size: 1.3rem; font-weight: 800; margin: 5px 0;">{today_reward['reward']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🎁 Klaim Bonus Harian!", use_container_width=True, type="primary"):
                award_points(today_reward["points"], "Daily login")
                st.session_state.engagement["daily_claimed"] = True
                st.session_state.engagement["streak"] += 1
                if streak + 1 == 7:
                    if "streak_7" not in eng["badges"]:
                        eng["badges"].append("streak_7")
                        st.toast("🏅 Badge: Istiqomah Seminggu!")
                st.balloons()
                st.rerun()
        else:
            st.info("✅ Bonus harian sudah diklaim. Kembali besok untuk melanjutkan streak!")
    
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Tantangan", "🏆 Badge", "📊 Leaderboard", "🎁 Referral", "🕋 Kesiapan"])
    
    with tab1:
        st.subheader("📋 Tantangan Harian")
        for challenge in DAILY_CHALLENGES:
            st.markdown(f"""
            <div style="background: #FFFFFF10; border-radius: 10px; padding: 12px 15px; margin-bottom: 8px;
                        display: flex; justify-content: space-between; align-items: center;
                        border-left: 3px solid {COLORS['gold']};">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.3rem;">{challenge['icon']}</span>
                    <div>
                        <div style="font-weight: 600;">{challenge['title']}</div>
                        <div style="color: {COLORS['sand']}; font-size: 0.8rem;">{challenge['desc']}</div>
                    </div>
                </div>
                <div style="background: {COLORS['gold']}; color: {COLORS['black']}; padding: 5px 12px;
                            border-radius: 15px; font-weight: 700; font-size: 0.85rem;">
                    +{challenge['points']} LP
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🏆 Koleksi Badge")
        owned_count = len(eng["badges"])
        total_badges = len([b for b in BADGES.values() if b.get("category") != "secret"])
        st.markdown(f"**Progress:** {owned_count}/{total_badges} badges")
        
        badge_cols = st.columns(5)
        for i, (badge_id, badge) in enumerate(BADGES.items()):
            with badge_cols[i % 5]:
                owned = badge_id in eng["badges"]
                opacity = "1" if owned else "0.3"
                border = f"2px solid {COLORS['gold']}" if owned else "1px solid #333"
                st.markdown(f"""
                <div style="text-align: center; opacity: {opacity}; padding: 15px;
                            background: {COLORS['black']}; border-radius: 12px;
                            border: {border}; margin-bottom: 10px;">
                    <div style="font-size: 2rem;">{badge['icon']}</div>
                    <div style="font-size: 0.7rem; color: {COLORS['gold'] if owned else '#666'}; margin-top: 5px;">{badge['name']}</div>
                    <div style="font-size: 0.65rem; color: #888;">{badge['points']} LP</div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("📊 Leaderboard Mingguan")
        
        # Sample leaderboard data
        leaders = [
            {"rank": 1, "name": "Ahmad Fauzi", "city": "Jakarta", "points": 15420, "avatar": "👳"},
            {"rank": 2, "name": "Siti Aisyah", "city": "Surabaya", "points": 12850, "avatar": "👩"},
            {"rank": 3, "name": "Muhammad Rizki", "city": "Bandung", "points": 11200, "avatar": "👨"},
            {"rank": 4, "name": "Fatimah Zahra", "city": "Medan", "points": 9800, "avatar": "👩"},
            {"rank": 5, "name": "Ibrahim Hassan", "city": "Makassar", "points": 8500, "avatar": "👨"},
        ]
        medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#555", "#555"]
        
        for i, leader in enumerate(leaders):
            rank_display = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{leader['rank']}"
            st.markdown(f"""
            <div style="background: {medal_colors[i]}15; border-radius: 12px; padding: 12px 15px;
                        margin-bottom: 8px; display: flex; align-items: center; gap: 15px;
                        border: 1px solid {medal_colors[i]}40;">
                <div style="font-size: 1.3rem; width: 40px; text-align: center;">{rank_display}</div>
                <div style="font-size: 1.5rem;">{leader['avatar']}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600;">{leader['name']}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.75rem;">📍 {leader['city']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: {COLORS['gold']}; font-weight: 700;">{leader['points']:,}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.7rem;">LP</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 15px; padding: 10px; background: {COLORS['gold']}20; border-radius: 10px;">
            📊 Peringkat Anda: <strong style="color: {COLORS['gold']};">#42</strong> • {points:,} LP
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("🎁 Ajak Teman")
        user = get_current_user()
        user_id = user.get("id", "guest") if user else "guest"
        ref_code = generate_referral_code(str(user_id))
        referrals = eng.get("referral_count", 0)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
                    border-radius: 20px; padding: 25px; text-align: center;
                    border: 1px solid {COLORS['gold']}50;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🎁</div>
            <div style="color: white; font-size: 1.2rem; font-weight: 700;">Ajak Teman, Dapat Bonus!</div>
            <div style="color: {COLORS['sand']}; margin: 10px 0;">
                Dapatkan <strong style="color: {COLORS['gold']};">200 LP</strong> untuk setiap teman yang bergabung
            </div>
            
            <div style="background: {COLORS['black']}; border-radius: 15px; padding: 15px; margin: 20px 0;
                        border: 2px dashed {COLORS['gold']}50;">
                <div style="color: {COLORS['sand']}; font-size: 0.85rem;">Kode Referral Anda</div>
                <div style="color: {COLORS['gold']}; font-size: 2rem; font-weight: 800; letter-spacing: 4px;">{ref_code}</div>
            </div>
            
            <div style="display: flex; justify-content: space-around; padding: 15px; background: {COLORS['black']}50; border-radius: 10px;">
                <div>
                    <div style="color: {COLORS['gold']}; font-size: 1.5rem; font-weight: 700;">{referrals}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.75rem;">Teman Diajak</div>
                </div>
                <div style="width: 1px; background: {COLORS['gold']}30;"></div>
                <div>
                    <div style="color: #4CAF50; font-size: 1.5rem; font-weight: 700;">{referrals * 200}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.75rem;">LP Didapat</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab5:
        st.subheader("🕋 Skor Kesiapan Umrah")
        
        # Calculate readiness based on various factors
        readiness = {
            "knowledge": min(100, (len([q for q in eng.get("quiz_completed", [])]) / len(QUIZ_QUESTIONS)) * 100) if QUIZ_QUESTIONS else 50,
            "financial": 60,
            "physical": 75,
            "spiritual": 70,
            "documents": 40,
        }
        overall = sum(readiness.values()) // len(readiness)
        
        # Circular progress
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <div style="position: relative; width: 150px; height: 150px; margin: 0 auto;">
                <svg viewBox="0 0 36 36" style="transform: rotate(-90deg);">
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none" stroke="{COLORS['black']}" stroke-width="3"/>
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none" stroke="{COLORS['green']}" stroke-width="3"
                          stroke-dasharray="{overall}, 100"/>
                </svg>
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                    <div style="color: {COLORS['green']}; font-size: 2rem; font-weight: 800;">{overall}%</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.7rem;">SIAP</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bars for each category
        categories = [
            ("📚 Pengetahuan Manasik", readiness["knowledge"], "#2196F3"),
            ("💰 Keuangan & Tabungan", readiness["financial"], COLORS['gold']),
            ("🏃 Persiapan Fisik", readiness["physical"], "#4CAF50"),
            ("🤲 Persiapan Spiritual", readiness["spiritual"], "#9C27B0"),
            ("📄 Dokumen & Visa", readiness["documents"], "#FF9800"),
        ]
        
        for name, value, color in categories:
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-size: 0.9rem;">{name}</span>
                    <span style="color: {color}; font-weight: 600;">{value:.0f}%</span>
                </div>
                <div style="background: {COLORS['black']}; border-radius: 5px; height: 8px; overflow: hidden;">
                    <div style="background: {color}; height: 100%; width: {value}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("💡 Tingkatkan skor dengan menyelesaikan quiz, checklist, dan fitur lainnya!")
    
    st.markdown("---")
    
    # Quiz Section
    st.subheader("🧠 Quiz Umrah")
    
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
    
    if st.session_state.quiz_index < len(QUIZ_QUESTIONS):
        q = QUIZ_QUESTIONS[st.session_state.quiz_index]
        st.markdown(f"**Soal {st.session_state.quiz_index + 1}/{len(QUIZ_QUESTIONS)}:** {q['question']}")
        
        answer = st.radio("Pilih jawaban:", q["options"], key=f"quiz_{st.session_state.quiz_index}")
        
        if st.button("Submit Jawaban"):
            if q["options"].index(answer) == q["correct"]:
                st.success("✅ Benar!")
                st.session_state.quiz_score += 1
                award_points(POINTS_CONFIG["quiz_correct"], "Quiz benar")
            else:
                st.error(f"❌ Salah. Jawaban: {q['options'][q['correct']]}")
            st.info(f"💡 {q['explanation']}")
            st.session_state.quiz_index += 1
            st.rerun()
    else:
        score = st.session_state.quiz_score
        total = len(QUIZ_QUESTIONS)
        st.success(f"🎉 Quiz Selesai! Skor: {score}/{total}")
        if score == total:
            st.balloons()
            if "perfect_quiz" not in eng["badges"]:
                eng["badges"].append("perfect_quiz")
                st.toast("🏅 Badge: Nilai Sempurna!")
        if st.button("🔄 Ulangi Quiz"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.rerun()

def render_umrah_mandiri():
    st.header("🕋 Umrah Mandiri")
    st.markdown("Panduan lengkap umrah mandiri & forum sharing!")
    
    tab1, tab2 = st.tabs(["📖 Panduan", "💬 FAQ"])
    
    with tab1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">✅ Umrah Mandiri itu LEGAL!</h3>
            <p style="color: #E8F5E9; margin: 10px 0 0 0;">Sejak 2019, Saudi membuka e-visa umrah untuk solo traveler</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Langkah Umrah Mandiri")
        steps = [
            "1️⃣ **Persiapan Dokumen** - Paspor valid >6 bulan",
            "2️⃣ **Booking Tiket** - Langsung ke website maskapai",
            "3️⃣ **Booking Hotel** - Via Booking.com/Agoda",
            "4️⃣ **Apply Visa** - Via nusuk.sa atau agen visa",
            "5️⃣ **Beli Asuransi** - Wajib! Cover medical",
            "6️⃣ **Pelajari Manasik** - Lihat tab Doa & Manasik",
            "7️⃣ **Siapkan Perlengkapan** - Gunakan Checklist",
            "8️⃣ **Berangkat** - Bismillah! 🕋",
        ]
        for step in steps:
            st.markdown(step)
        
        st.markdown("### 💰 Estimasi Biaya (9 hari)")
        costs = [
            ("✈️ Tiket PP", "Rp 7-12 juta"),
            ("📄 Visa", "Rp 500rb-1.5 juta"),
            ("🏨 Hotel Makkah (4 malam)", "Rp 2-5 juta"),
            ("🏨 Hotel Madinah (3 malam)", "Rp 1.5-4 juta"),
            ("🚗 Transport", "Rp 1-2 juta"),
            ("🍽️ Makan & lainnya", "Rp 1.5-3 juta"),
        ]
        for item, price in costs:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(item)
            with col2:
                st.markdown(f"**{price}**")
        st.markdown(f"**TOTAL: Rp 15-25 juta**")
    
    with tab2:
        faqs = [
            ("Wanita boleh umrah mandiri sendiri?", "Ya! Sejak 2021, wanita 18+ tidak perlu mahram."),
            ("Bagaimana dapat visa tanpa travel?", "Via nusuk.sa (self-apply) atau agen visa online."),
            ("Perlu vaksin apa?", "Meningitis wajib. COVID-19 tidak wajib (per 2024)."),
            ("Tidak bisa bahasa Arab?", "Tidak masalah! Banyak yang bisa Inggris. Gunakan Google Translate."),
        ]
        for q, a in faqs:
            with st.expander(q):
                st.markdown(a)

def render_umrah_bareng():
    st.header("🤝 Umrah Bareng")
    st.markdown("Cari teman perjalanan, buat open trip, dan hemat biaya bersama!")
    
    # Initialize umrah bareng state
    if "umrah_trips" not in st.session_state:
        st.session_state.umrah_trips = [
            {
                "id": 1,
                "title": "Umrah Ekonomis Maret 2025",
                "organizer": "Ahmad Fauzi",
                "organizer_id": 101,
                "departure_city": "Jakarta",
                "departure_date": "2025-03-15",
                "return_date": "2025-03-24",
                "duration": 9,
                "package": "ekonomis",
                "budget_range": "Rp 22-25 Juta",
                "slots_total": 10,
                "slots_filled": 6,
                "members": ["Ahmad F.", "Budi S.", "Citra D.", "Diana R.", "Eko P.", "Fatimah Z."],
                "whatsapp": "https://chat.whatsapp.com/abc123",
                "description": "Trip hemat untuk jamaah pemula. Berangkat dari Jakarta, hotel bintang 3, dekat Haram.",
                "status": "open",
                "created_at": "2025-01-15"
            },
            {
                "id": 2,
                "title": "Umrah Premium Ramadhan",
                "organizer": "Siti Aisyah",
                "organizer_id": 102,
                "departure_city": "Surabaya",
                "departure_date": "2025-03-25",
                "return_date": "2025-04-05",
                "duration": 12,
                "package": "premium",
                "budget_range": "Rp 45-55 Juta",
                "slots_total": 8,
                "slots_filled": 3,
                "members": ["Siti A.", "Hana M.", "Irfan K."],
                "whatsapp": "https://chat.whatsapp.com/def456",
                "description": "Umrah Ramadhan di hotel bintang 5, view Ka'bah. Termasuk city tour.",
                "status": "open",
                "created_at": "2025-01-20"
            },
            {
                "id": 3,
                "title": "Umrah Keluarga April",
                "organizer": "Muhammad Rizki",
                "organizer_id": 103,
                "departure_city": "Bandung",
                "departure_date": "2025-04-10",
                "return_date": "2025-04-19",
                "duration": 9,
                "package": "standard",
                "budget_range": "Rp 30-35 Juta",
                "slots_total": 15,
                "slots_filled": 8,
                "members": ["M. Rizki", "Keluarga A", "Keluarga B", "Keluarga C", "Dewi S.", "Fajar H.", "Gita P.", "Hendra W."],
                "whatsapp": "https://chat.whatsapp.com/ghi789",
                "description": "Trip ramah keluarga dengan anak-anak. Hotel dekat Haram, ada pendamping anak.",
                "status": "open",
                "created_at": "2025-01-25"
            },
        ]
    
    if "my_joined_trips" not in st.session_state:
        st.session_state.my_joined_trips = []
    
    user = get_current_user()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Cari Trip", "➕ Buat Trip", "📋 Trip Saya", "💡 Tips"])
    
    with tab1:
        st.subheader("🔍 Open Trip Tersedia")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_city = st.selectbox("Kota Keberangkatan", ["Semua", "Jakarta", "Surabaya", "Bandung", "Medan", "Makassar"])
        with col2:
            filter_package = st.selectbox("Tipe Paket", ["Semua", "ekonomis", "standard", "premium", "vip"])
        with col3:
            filter_month = st.selectbox("Bulan", ["Semua", "Januari", "Februari", "Maret", "April", "Mei", "Juni"])
        
        st.markdown("---")
        
        # Trip cards
        for trip in st.session_state.umrah_trips:
            if trip["status"] != "open":
                continue
            if filter_city != "Semua" and trip["departure_city"] != filter_city:
                continue
            if filter_package != "Semua" and trip["package"] != filter_package:
                continue
            
            slots_available = trip["slots_total"] - trip["slots_filled"]
            progress = trip["slots_filled"] / trip["slots_total"]
            progress_pct = progress * 100
            
            # Package color
            package_colors = {
                "ekonomis": "#4CAF50",
                "standard": "#2196F3", 
                "premium": "#9C27B0",
                "vip": "#D4AF37"
            }
            pkg_color = package_colors.get(trip["package"], "#666")
            
            # Slot color
            if slots_available > 3:
                slot_color = "#4CAF50"
            elif slots_available > 0:
                slot_color = "#FF9800"
            else:
                slot_color = "#F44336"
            
            # Build card HTML
            card_html = f'''
            <div style="background: white; border-radius: 15px; padding: 20px; margin-bottom: 15px; 
                        border: 1px solid #E0E0E0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                    <div>
                        <span style="background: {pkg_color}; color: white; padding: 3px 10px; border-radius: 12px; 
                                     font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">{trip["package"]}</span>
                        <h3 style="margin: 10px 0 5px 0; color: #1A1A1A;">{trip["title"]}</h3>
                        <p style="color: #666; font-size: 0.9rem; margin: 0;">👤 {trip["organizer"]} • 📍 {trip["departure_city"]}</p>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #D4AF37; font-size: 1.2rem; font-weight: 700;">{trip["budget_range"]}</div>
                        <div style="color: #666; font-size: 0.8rem;">{trip["duration"]} hari</div>
                    </div>
                </div>
                
                <p style="color: #555; font-size: 0.9rem; margin-bottom: 15px;">{trip["description"]}</p>
                
                <div style="display: flex; gap: 20px; margin-bottom: 15px; font-size: 0.85rem; color: #666;">
                    <span>📅 {trip["departure_date"]}</span>
                    <span>➡️ {trip["return_date"]}</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-size: 0.85rem; color: #666;">👥 {trip["slots_filled"]}/{trip["slots_total"]} peserta</span>
                        <span style="font-size: 0.85rem; color: {slot_color};">{slots_available} slot tersisa</span>
                    </div>
                    <div style="background: #E0E0E0; border-radius: 5px; height: 8px; overflow: hidden;">
                        <div style="background: {pkg_color}; height: 100%; width: {progress_pct:.1f}%;"></div>
                    </div>
                </div>
            </div>
            '''
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if slots_available > 0:
                    if st.button(f"🙋 Gabung Trip", key=f"join_{trip['id']}", use_container_width=True):
                        if trip['id'] not in st.session_state.my_joined_trips:
                            st.session_state.my_joined_trips.append(trip['id'])
                            trip['slots_filled'] += 1
                            trip['members'].append(user.get('name', 'User') if user else 'Guest')
                            st.success(f"✅ Berhasil gabung trip: {trip['title']}")
                            award_points(50, "Gabung Umrah Bareng")
                            st.rerun()
                        else:
                            st.warning("Anda sudah terdaftar di trip ini")
                else:
                    st.button("❌ Slot Penuh", key=f"full_{trip['id']}", disabled=True, use_container_width=True)
            with col2:
                if st.button(f"💬 WhatsApp", key=f"wa_{trip['id']}", use_container_width=True):
                    st.markdown(f"[Buka Grup WhatsApp]({trip['whatsapp']})")
            with col3:
                with st.expander("👥 Peserta"):
                    for member in trip['members']:
                        st.write(f"• {member}")
            
            st.markdown("---")
    
    with tab2:
        st.subheader("➕ Buat Open Trip Baru")
        st.markdown("Ajak jamaah lain untuk umrah bersama dan hemat biaya!")
        
        with st.form("create_trip_form"):
            trip_title = st.text_input("📝 Judul Trip", placeholder="contoh: Umrah Ekonomis Mei 2025")
            
            col1, col2 = st.columns(2)
            with col1:
                departure_city = st.selectbox("📍 Kota Keberangkatan", ["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar", "Semarang", "Yogyakarta"])
                departure_date = st.date_input("📅 Tanggal Berangkat", min_value=datetime.now().date() + timedelta(days=30))
                package_type = st.selectbox("📦 Tipe Paket", ["ekonomis", "standard", "premium", "vip"])
            with col2:
                slots_total = st.number_input("👥 Jumlah Slot", min_value=2, max_value=50, value=10)
                duration = st.slider("⏱️ Durasi (hari)", 7, 21, 9)
                budget_min = st.number_input("💰 Budget Min (Juta)", min_value=15, max_value=100, value=25)
            
            budget_max = st.number_input("💰 Budget Max (Juta)", min_value=budget_min, max_value=150, value=budget_min + 5)
            description = st.text_area("📝 Deskripsi Trip", placeholder="Jelaskan tentang trip ini, hotel, fasilitas, dll...")
            whatsapp_link = st.text_input("💬 Link Grup WhatsApp", placeholder="https://chat.whatsapp.com/...")
            
            agree = st.checkbox("Saya setuju menjadi organizer dan bertanggung jawab atas koordinasi trip ini")
            
            submitted = st.form_submit_button("🚀 Buat Trip", use_container_width=True, type="primary")
            
            if submitted:
                if not trip_title or not description:
                    st.error("Mohon isi judul dan deskripsi trip")
                elif not agree:
                    st.error("Mohon setujui syarat sebagai organizer")
                else:
                    new_trip = {
                        "id": len(st.session_state.umrah_trips) + 1,
                        "title": trip_title,
                        "organizer": user.get('name', 'User') if user else 'Guest',
                        "organizer_id": user.get('id', 0) if user else 0,
                        "departure_city": departure_city,
                        "departure_date": departure_date.strftime("%Y-%m-%d"),
                        "return_date": (departure_date + timedelta(days=duration)).strftime("%Y-%m-%d"),
                        "duration": duration,
                        "package": package_type,
                        "budget_range": f"Rp {budget_min}-{budget_max} Juta",
                        "slots_total": slots_total,
                        "slots_filled": 1,
                        "members": [user.get('name', 'User') if user else 'Guest'],
                        "whatsapp": whatsapp_link or "#",
                        "description": description,
                        "status": "open",
                        "created_at": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.umrah_trips.append(new_trip)
                    award_points(100, "Buat Open Trip")
                    st.success("✅ Trip berhasil dibuat! Anda dapat 100 LP")
                    st.balloons()
    
    with tab3:
        st.subheader("📋 Trip Saya")
        
        # My organized trips
        st.markdown("#### 👑 Trip yang Saya Buat")
        my_organized = [t for t in st.session_state.umrah_trips if t.get('organizer_id') == (user.get('id', 0) if user else 0)]
        
        if my_organized:
            for trip in my_organized:
                slots_available = trip["slots_total"] - trip["slots_filled"]
                status_color = "#4CAF50" if trip['status'] == 'open' else "#666"
                
                organized_html = f'''
                <div style="background: linear-gradient(135deg, #D4AF3720 0%, #C9A86C20 100%); 
                            border-radius: 12px; padding: 15px; margin-bottom: 10px;
                            border-left: 4px solid #D4AF37;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{trip["title"]}</strong>
                            <div style="color: #666; font-size: 0.85rem;">📅 {trip["departure_date"]} • 👥 {trip["slots_filled"]}/{trip["slots_total"]}</div>
                        </div>
                        <span style="background: {status_color}; color: white; 
                                     padding: 3px 10px; border-radius: 12px; font-size: 0.75rem;">
                            {trip["status"].upper()}
                        </span>
                    </div>
                </div>
                '''
                st.markdown(organized_html, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if trip['status'] == 'open':
                        if st.button(f"🔒 Tutup Pendaftaran", key=f"close_{trip['id']}"):
                            trip['status'] = 'closed'
                            st.success("Trip ditutup")
                            st.rerun()
                with col2:
                    with st.expander("👥 Lihat Peserta"):
                        for i, member in enumerate(trip['members'], 1):
                            st.write(f"{i}. {member}")
        else:
            st.info("Anda belum membuat trip. Buat trip pertama Anda di tab 'Buat Trip'!")
        
        st.markdown("---")
        
        # My joined trips
        st.markdown("#### 🎒 Trip yang Saya Ikuti")
        my_joined = [t for t in st.session_state.umrah_trips if t['id'] in st.session_state.my_joined_trips]
        
        if my_joined:
            for trip in my_joined:
                joined_html = f'''
                <div style="background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px;
                            border: 1px solid #E0E0E0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{trip["title"]}</strong>
                            <div style="color: #666; font-size: 0.85rem;">
                                👤 {trip["organizer"]} • 📅 {trip["departure_date"]} • 📍 {trip["departure_city"]}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #D4AF37; font-weight: 600;">{trip["budget_range"]}</div>
                        </div>
                    </div>
                </div>
                '''
                st.markdown(joined_html, unsafe_allow_html=True)
                
                if st.button(f"💬 Grup WhatsApp", key=f"mywa_{trip['id']}"):
                    st.markdown(f"[Buka Grup]({trip['whatsapp']})")
        else:
            st.info("Anda belum bergabung trip manapun. Cari trip di tab 'Cari Trip'!")
    
    with tab4:
        st.subheader("💡 Tips Umrah Bareng")
        
        tips = [
            ("🤝", "Pilih Partner Tepat", "Cari teman dengan budget dan preferensi serupa untuk pengalaman lebih nyaman."),
            ("📋", "Buat Kesepakatan", "Diskusikan pembagian biaya, jadwal, dan aturan grup sebelum berangkat."),
            ("💬", "Komunikasi Aktif", "Gunakan grup WhatsApp untuk koordinasi. Responsif terhadap pesan organizer."),
            ("💰", "Transparansi Biaya", "Minta rincian biaya dari organizer. Pastikan tidak ada biaya tersembunyi."),
            ("📄", "Cek Legalitas", "Pastikan travel agent yang digunakan terdaftar di Kemenag (siskopatuh.kemenag.go.id)."),
            ("🛡️", "Asuransi Perjalanan", "Pastikan semua peserta memiliki asuransi perjalanan yang memadai."),
        ]
        
        for icon, title, desc in tips:
            tip_html = f'''
            <div style="background: #F5F5F5; border-radius: 12px; padding: 15px; margin-bottom: 10px;
                        display: flex; align-items: flex-start; gap: 15px;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div>
                    <div style="font-weight: 600; margin-bottom: 5px;">{title}</div>
                    <div style="color: #666; font-size: 0.9rem;">{desc}</div>
                </div>
            </div>
            '''
            st.markdown(tip_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.warning("""
        ⚠️ **Disclaimer Umrah Bareng:**
        - LABBAIK hanya memfasilitasi pertemuan antar jamaah
        - LABBAIK bukan travel agent dan tidak bertanggung jawab atas transaksi
        - Selalu verifikasi travel agent di **siskopatuh.kemenag.go.id**
        - Lakukan DYOR (Do Your Own Research) sebelum bergabung trip
        """)

def render_profile():
    st.header("👤 Profil Saya")
    
    user = get_current_user()
    if not user:
        st.warning("🔐 Silakan login")
        return
    
    role_info = get_role_info(user.get("role", "user"))
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div style="background: {role_info['color']}40; border: 3px solid {role_info['color']}; border-radius: 15px; padding: 25px; text-align: center;">
            <div style="font-size: 4rem;">{role_info['badge']}</div>
            <h2 style="margin: 10px 0;">{user.get('name', 'User')}</h2>
            <p style="color: {role_info['color']}; font-weight: bold;">{role_info['name']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("### 📋 Informasi Akun")
        st.markdown(f"**Email:** {user.get('email', '-')}")
        st.markdown(f"**Role:** {role_info['name']}")
        
        # Engagement stats
        init_engagement()
        eng = st.session_state.engagement
        st.markdown(f"**Points:** {eng['points']:,} LP")
        st.markdown(f"**Level:** {1 + eng['points'] // 500}")
        st.markdown(f"**Badges:** {len(eng['badges'])}")

def render_about():
    st.markdown(f"""
    <div class="labbaik-hero">
        <div class="labbaik-arabic">{BRAND['talbiyah']}</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: white; letter-spacing: 0.3em; margin: 15px 0;">{BRAND['name']}</div>
        <div style="color: {COLORS['sand']}; font-size: 1rem;">{BRAND['tagline']}</div>
        <div style="color: {COLORS['sand']}; margin-top: 10px;">{BRAND['description']}</div>
        <span style="background: {COLORS['gold']}; color: {COLORS['black']}; padding: 5px 15px; border-radius: 15px; font-weight: 700; margin-top: 15px; display: inline-block;">v{BRAND['version']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Visitor Stats Bar
    visitor_count = st.session_state.get("visitor_count", 1250)
    page_views_dict = st.session_state.get("page_views", {"_total": 3500})
    page_views = page_views_dict.get("_total", 3500) if isinstance(page_views_dict, dict) else 3500
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Pengunjung", f"{visitor_count:,}")
    with col2:
        st.metric("👁️ Total Views", f"{page_views:,}")
    with col3:
        st.metric("⭐ Rating", "4.9/5")
    with col4:
        st.metric("🕋 Fitur", "25+")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👨‍💻 Developer", "🤝 Kerjasama", "💎 Upgrade", "⚖️ Disclaimer"])
    
    with tab1:
        st.markdown("""
        ### 👨‍💻 Developer
        
        **MS Hadianto**  
        Founder & Lead Developer - KIM Consulting
        
        📧 sopian.hadianto@gmail.com  
        📱 +62 815 9658 833
        
        ---
        
        ### 🔧 Tech Stack
        - **Frontend:** Streamlit
        - **AI:** Groq (Llama 3.3), OpenAI
        - **Database:** Neon PostgreSQL
        - **Hosting:** Streamlit Cloud
        """)
    
    with tab2:
        st.subheader("🤝 Kerjasama & Partnership")
        st.markdown("LABBAIK membuka kesempatan kerjasama dengan berbagai pihak untuk memberikan layanan terbaik bagi jamaah umrah Indonesia.")
        
        # Sponsorship Tiers
        cols = st.columns(3)
        for i, (tier_id, tier) in enumerate(SPONSORSHIP_TIERS.items()):
            with cols[i]:
                # Build benefits list HTML
                benefits_html = ""
                for b in tier['benefits']:
                    benefits_html += f'<div style="margin-bottom: 5px;">✓ {b}</div>'
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
                            border-radius: 15px; padding: 20px; text-align: center;
                            border: 2px solid {tier['color']}40; height: 320px;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">{tier['icon']}</div>
                    <div style="color: {tier['color']}; font-size: 1.1rem; font-weight: 700;">{tier['name']}</div>
                    <div style="color: #D4AF37; font-size: 1.3rem; font-weight: 700; margin: 15px 0;">
                        Rp {tier['price']:,.0f}
                    </div>
                    <div style="color: #888; font-size: 0.8rem; margin-bottom: 15px;">per bulan</div>
                    <div style="text-align: left; color: #E8E8E8; font-size: 0.8rem;">
                        {benefits_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("📧 Hubungi: **partner@labbaik.id** atau **sopian.hadianto@gmail.com**")
    
    with tab3:
        st.subheader("💎 Paket Langganan")
        st.markdown("Upgrade untuk akses fitur premium dan diskon eksklusif!")
        
        cols = st.columns(3)
        for i, (plan_id, plan) in enumerate(SUBSCRIPTION_PLANS.items()):
            with cols[i]:
                is_popular = plan.get("popular", False)
                border_style = f"3px solid {COLORS['gold']}" if is_popular else "1px solid #555"
                
                # Build features list HTML
                features_html = ""
                for f in plan['features'][:5]:
                    features_html += f'<div style="padding:5px 0;border-bottom:1px solid #eee;">✅ {f}</div>'
                
                # Popular badge
                popular_badge = ""
                if is_popular:
                    popular_badge = f'<div style="position:absolute;top:-10px;right:20px;background:{COLORS["gold"]};color:{COLORS["black"]};padding:3px 15px;border-radius:20px;font-size:0.75rem;font-weight:bold;">POPULER</div>'
                
                st.markdown(f"""
                <div style="background: white; border: {border_style}; border-radius: 15px;
                            padding: 25px; text-align: center; height: 380px; position: relative;">
                    {popular_badge}
                    <div style="font-size: 2rem; margin-bottom: 10px;">{plan['badge']}</div>
                    <h4 style="color: #1A1A1A; margin: 0;">{plan['name']}</h4>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #006B3C; margin: 15px 0;">
                        {plan['price_display']}
                    </div>
                    <div style="color: #666; font-size: 0.85rem; margin-bottom: 15px;">/ bulan</div>
                    <div style="text-align: left; font-size: 0.85rem;">
                        {features_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("💡 Fitur upgrade akan segera tersedia! Saat ini semua fitur dapat diakses GRATIS.")
    
    with tab4:
        st.markdown(f"""
        <div style="background: #FFEBEE; border: 2px solid #D32F2F; border-radius: 15px; padding: 20px;">
            <h4 style="color: #B71C1C;">⚠️ DISCLAIMER</h4>
            <p><strong>LABBAIK</strong> adalah platform simulasi & perencanaan umrah.</p>
            <ul>
                <li>BUKAN travel agent</li>
                <li>BUKAN pengganti konsultasi dengan travel resmi</li>
                <li>Verifikasi travel agent di: <strong>siskopatuh.kemenag.go.id</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 📋 Sumber Resmi
        - **Arab Saudi:** nusuk.sa
        - **Indonesia:** kemenag.go.id
        - **KBRI Riyadh:** +966-11-488-2800
        """)

def render_footer():
    # Get visitor count
    visitor_count = get_visitor_count()
    visitor_str = f"{visitor_count:,}" if visitor_count else "0"
    
    footer_html = f'''
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                padding: 40px; border-radius: 20px; text-align: center; margin-top: 50px;">
        <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.8rem; color: #D4AF37;">
            {BRAND['talbiyah']}
        </div>
        <div style="font-size: 1.3rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin: 12px 0;">
            {BRAND['name']}
        </div>
        <div style="color: #C9A86C; font-size: 0.95rem; margin-bottom: 20px;">
            {BRAND['tagline']}
        </div>
        
        <div style="background: rgba(212, 175, 55, 0.15); display: inline-block; 
                    padding: 8px 20px; border-radius: 20px; margin-bottom: 20px;">
            <span style="color: #D4AF37; font-size: 0.85rem;">
                👥 Total Pengunjung: <strong>{visitor_str}</strong>
            </span>
        </div>
        
        <div style="color: #888; font-size: 0.85rem; margin-bottom: 15px;">
            📧 sopian.hadianto@gmail.com | 📱 +62 815 9658 833 | 🌐 labbaik.ai
        </div>
        
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 10px; padding: 15px 20px; margin: 20px auto; max-width: 600px;">
            <div style="color: #D4AF37; font-size: 0.8rem; font-weight: 600; margin-bottom: 8px;">
                ⚠️ Disclaimer
            </div>
            <div style="color: #aaa; font-size: 0.75rem; line-height: 1.6;">
                Aplikasi ini dikembangkan oleh <strong>non-developer</strong> dengan memanfaatkan teknologi AI.
                Informasi bersifat simulasi dan estimasi. Selalu konsultasikan dengan travel agent resmi berizin.
            </div>
        </div>
        
        <div style="border-top: 1px solid #333; padding-top: 20px; margin-top: 20px; color: #666; font-size: 0.8rem;">
            © 2025 LABBAIK. Hak Cipta Dilindungi.<br>
            <span style="color: #D4AF37;">Made with ❤️ & AI by MS Hadianto</span><br>
            <span style="color: #555; font-size: 0.7rem;">v{BRAND['version']} Beta • Powered by Streamlit</span>
        </div>
    </div>
    '''
    st.markdown(footer_html, unsafe_allow_html=True)

# ============================================
# MAIN APPLICATION
# ============================================
def main():
    init_session_state()
    init_engagement()
    
    # Check for login page redirect
    if st.session_state.get("show_login") and not is_logged_in():
        render_login_page()
        if st.button("← Kembali"):
            st.session_state.show_login = False
            st.rerun()
        return
    
    if is_logged_in():
        st.session_state.show_login = False
    
    page = render_sidebar()
    
    # Route pages
    if "Beranda" in page:
        track_page_view("Home")
        render_home()
        render_footer()
    elif "Simulasi Biaya" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Cost Simulation")
            render_cost_simulation()
    elif "Buat Rencana" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Create Plan")
            render_create_plan()
    elif "Cari by Budget" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Budget Finder")
            render_budget_finder()
    elif "Perbandingan" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Comparison")
            render_scenario_comparison()
    elif "Waktu Terbaik" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Time Analysis")
            render_time_analysis()
    elif "AI Chat" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("AI Chat")
            render_ai_chat()
    elif "Umrah Bareng" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Umrah Bareng")
            render_umrah_bareng()
    elif "Umrah Mandiri" in page:
        track_page_view("Umrah Mandiri")
        render_umrah_mandiri()
    elif "Tools" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Tools")
            render_tools_features()
    elif "Rewards" in page or "Quiz" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Rewards")
            render_engagement_page()
    elif "Profil" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            track_page_view("Profile")
            render_profile()
    elif "Tentang" in page:
        track_page_view("About")
        render_about()
        render_footer()

if __name__ == "__main__":
    main()