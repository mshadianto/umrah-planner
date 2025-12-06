"""
================================================================================
لَبَّيْكَ LABBAIK - Main Application
================================================================================

Labbaik Allahumma Labbaik - Aku Datang Memenuhi Panggilan-Mu

Copyright (c) 2025 MS Hadianto. All Rights Reserved.

================================================================================
Platform: AI-Powered Umrah Planning Platform
Version:  4.0.0
Codename: Labbaik Ultimate
Author:   MS Hadianto
Email:    sopian.hadianto@gmail.com
Website:  labbaik.ai
================================================================================

Version: 4.0.0
Updated: 2025-12-06
Changes: 
- Merged v3.5.0 Engagement System + v3.9.0 Enhanced Features
- Removed PWA for lightweight access
- Added: Savings Calculator, Countdown, Doa & Manasik, Enhanced Checklist
- Added: Points, Levels, Badges, Streaks, Quiz, Referral System
- Optimized imports and performance
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
        version: str = "4.0.0"
    
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
    "version": "4.0.0",
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
    "complete_simulation": 25,
    "share_social": 50,
    "referral_signup": 200,
    "referral_bonus": 75,
    "quiz_correct": 15,
    "read_guide": 10,
}

BADGES = {
    "newcomer": {"name": "Pendatang Baru", "icon": "🌟", "points": 0},
    "explorer": {"name": "Penjelajah", "icon": "🔍", "points": 100},
    "planner": {"name": "Perencana Handal", "icon": "📋", "points": 500},
    "expert": {"name": "Ahli Umrah", "icon": "🎓", "points": 1000},
    "ambassador": {"name": "Duta LABBAIK", "icon": "👑", "points": 2500},
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
        "page_views": 3500,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def init_engagement():
    if "engagement" not in st.session_state:
        st.session_state.engagement = {
            "points": 0, "level": 1, "streak": 0,
            "badges": ["newcomer"], "daily_claimed": False,
            "referral_count": 0, "quiz_completed": []
        }

def award_points(amount, reason=""):
    init_engagement()
    st.session_state.engagement["points"] += amount
    # Check level up
    points = st.session_state.engagement["points"]
    new_level = 1 + (points // 500)
    if new_level > st.session_state.engagement["level"]:
        st.session_state.engagement["level"] = new_level
        st.toast(f"🎉 Level Up! Sekarang Level {new_level}")
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
                "🏠 Beranda", "💰 Simulasi Biaya", "💵 Cari by Budget",
                "🤝 Umrah Bareng", "🕋 Umrah Mandiri", "📊 Perbandingan",
                "🧰 Tools & Fitur", "🎮 Rewards & Quiz", "👤 Profil", "ℹ️ Tentang"
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
            email = st.text_input("Email", placeholder="admin@labbaik.id")
            password = st.text_input("Password", type="password", placeholder="@Jakarta01")
            submitted = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if submitted:
                success, msg = login(email, password)
                if success:
                    st.success(msg)
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error(msg)
        
        st.info("**Demo Admin:** admin@labbaik.id / @Jakarta01")
    
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
    st.header("🎮 Rewards & Quiz Center")
    
    init_engagement()
    eng = st.session_state.engagement
    points = eng["points"]
    level = 1 + (points // 500)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: {COLORS['black']}; padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2rem;">⭐</div>
            <div style="color: {COLORS['gold']}; font-size: 2rem; font-weight: 800;">{points:,}</div>
            <div style="color: {COLORS['sand']};">LABBAIK Points</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: {COLORS['black']}; padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2rem;">🏆</div>
            <div style="color: {COLORS['gold']}; font-size: 2rem; font-weight: 800;">{level}</div>
            <div style="color: {COLORS['sand']};">Level</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: {COLORS['black']}; padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2rem;">🔥</div>
            <div style="color: {COLORS['gold']}; font-size: 2rem; font-weight: 800;">{eng['streak']}</div>
            <div style="color: {COLORS['sand']};">Streak</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Daily claim
    if not eng["daily_claimed"]:
        if st.button("🎁 Klaim Bonus Harian (+10 LP)", use_container_width=True):
            award_points(10, "Daily login")
            st.session_state.engagement["daily_claimed"] = True
            st.session_state.engagement["streak"] += 1
            st.success("✅ +10 LP diklaim!")
            st.rerun()
    else:
        st.info("✅ Bonus harian sudah diklaim. Kembali besok!")
    
    st.markdown("---")
    
    # Badges
    st.subheader("🏅 Badges")
    badge_cols = st.columns(5)
    for i, (badge_id, badge) in enumerate(BADGES.items()):
        with badge_cols[i % 5]:
            owned = badge_id in eng["badges"]
            opacity = "1" if owned else "0.3"
            st.markdown(f"""
            <div style="text-align: center; opacity: {opacity}; padding: 10px;">
                <div style="font-size: 2rem;">{badge['icon']}</div>
                <div style="font-size: 0.75rem;">{badge['name']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quiz
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
        if st.button("🔄 Ulangi Quiz"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.rerun()
    
    st.markdown("---")
    
    # Referral
    st.subheader("🎁 Ajak Teman")
    user = get_current_user()
    user_id = user.get("id", "guest") if user else "guest"
    ref_code = generate_referral_code(str(user_id))
    
    st.markdown(f"""
    <div style="background: {COLORS['black']}; padding: 20px; border-radius: 15px; text-align: center;">
        <div style="color: {COLORS['sand']};">Kode Referral Anda:</div>
        <div style="color: {COLORS['gold']}; font-size: 2rem; font-weight: 800; letter-spacing: 4px;">{ref_code}</div>
        <div style="color: #888; font-size: 0.85rem; margin-top: 10px;">Dapat +200 LP setiap teman mendaftar!</div>
    </div>
    """, unsafe_allow_html=True)

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
    st.info("🚧 Fitur ini sedang dalam pengembangan. Stay tuned!")
    
    st.markdown("""
    **Fitur yang akan hadir:**
    - 🔍 Cari teman perjalanan umrah
    - ➕ Buat open trip sendiri
    - 💬 Grup WhatsApp koordinasi
    - 💰 Share cost untuk lebih hemat
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
    
    tab1, tab2 = st.tabs(["👨‍💻 Developer", "⚖️ Disclaimer"])
    
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
    st.markdown(f"""
    <div style="background: {COLORS['black']}; padding: 30px; border-radius: 15px; text-align: center; margin-top: 30px;">
        <div style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1.5rem;">{BRAND['talbiyah']}</div>
        <div style="color: white; font-weight: 700; letter-spacing: 0.2em; margin: 10px 0;">{BRAND['name']}</div>
        <div style="color: {COLORS['sand']}; font-size: 0.85rem;">{BRAND['tagline']}</div>
        <div style="color: #666; font-size: 0.75rem; margin-top: 15px;">
            © 2025 LABBAIK | Made with ❤️ by MS Hadianto | v{BRAND['version']}
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        render_home()
        render_footer()
    elif "Simulasi Biaya" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            render_cost_simulation()
    elif "Cari by Budget" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            render_budget_finder()
    elif "Perbandingan" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            render_scenario_comparison()
    elif "Umrah Bareng" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            render_umrah_bareng()
    elif "Umrah Mandiri" in page:
        render_umrah_mandiri()
    elif "Tools" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            render_tools_features()
    elif "Rewards" in page or "Quiz" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            render_engagement_page()
    elif "Profil" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login")
            render_login_page()
        else:
            render_profile()
    elif "Tentang" in page:
        render_about()
        render_footer()

if __name__ == "__main__":
    main()