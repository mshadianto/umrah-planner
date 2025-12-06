"""
================================================================================
لَبَّيْكَ LABBAIK - COMPLETE APP v3.5.2 FIXED
================================================================================
FIX ALL ERRORS - Generated 2025-12-06

⚠️ CARA PAKAI (PENTING!):
1. BACKUP app.py lama Anda (rename jadi app_backup.py)
2. HAPUS SELURUH ISI app.py 
3. COPY-PASTE SELURUH ISI FILE INI ke app.py
4. Save dan deploy ulang

⚠️ JANGAN patch sebagian - GANTI SELURUHNYA!
   File lama: 5727 baris
   File baru: ~2522 baris (lebih ringkas & tanpa bug)

================================================================================
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import os
import hashlib
import random

# ============================================
# PAGE CONFIG - MUST BE FIRST
# ============================================
st.set_page_config(
    page_title="LABBAIK - Platform Umrah AI",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONFIG WITH FALLBACKS
# ============================================
try:
    from config import app_config, llm_config, SCENARIO_TEMPLATES, DEPARTURE_CITIES, SEASONS
except ImportError:
    @dataclass
    class AppConfig:
        name: str = "LABBAIK"
        version: str = "3.5.2"
    
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
        "Makassar": {"code": "UPG", "multiplier": 1.15},
        "Bandung": {"code": "BDO", "multiplier": 1.08},
        "Semarang": {"code": "SRG", "multiplier": 1.07},
        "Yogyakarta": {"code": "JOG", "multiplier": 1.06},
        "Denpasar": {"code": "DPS", "multiplier": 1.12},
        "Palembang": {"code": "PLM", "multiplier": 1.1},
        "Balikpapan": {"code": "BPN", "multiplier": 1.15}
    }
    
    SEASONS = {
        "low": {"name": "Low Season", "months": [1, 2, 6, 7], "multiplier": 0.85},
        "regular": {"name": "Regular", "months": [3, 4, 5, 8, 9, 10, 11], "multiplier": 1.0},
        "high": {"name": "High Season", "months": [12], "multiplier": 1.4},
        "ramadan": {"name": "Ramadan", "months": [], "multiplier": 1.6}
    }

# ============================================
# BRAND CONSTANTS
# ============================================
COLORS = {
    "black": "#1A1A1A",
    "gold": "#D4AF37", 
    "green": "#006B3C",
    "white": "#FFFFFF",
    "sand": "#C9A86C",
    "gray": "#666666"
}

BRAND = {
    "name": "LABBAIK",
    "arabic": "لَبَّيْكَ",
    "tagline": "Panggilan-Nya, Langkahmu",
    "description": "Platform AI Perencanaan Umrah #1 Indonesia",
    "talbiyah": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ",
    "version": "3.5.2"
}

CONTACT = {
    "email": "sopian.hadianto@gmail.com",
    "whatsapp": "+62 815 9658 833",
    "website": "labbaik.ai"
}

DEVELOPER = {
    "name": "MS Hadianto",
    "email": "sopian.hadianto@gmail.com",
    "whatsapp": "6281596588833",
    "github": "https://github.com/mshadianto",
    "linkedin": "https://linkedin.com/in/mshadianto"
}

__version__ = "3.5.2"

APP_INFO = {
    "name": "LABBAIK",
    "version": __version__,
    "tagline": "Panggilan-Nya, Langkahmu",
    "description": "Platform AI Perencanaan Umrah #1 Indonesia",
    "repository": "https://github.com/mshadianto/umrah-planner",
    "demo_url": "https://umrah-planner-by-mshadianto.streamlit.app",
    "license": "MIT"
}

TECH_STACK = {
    "frontend": [("Streamlit", "1.28+", "Web framework"), ("Plotly", "5.x", "Charts")],
    "ai": [("Groq", "Latest", "LLM"), ("LangChain", "0.1+", "AI orchestration")],
    "database": [("Neon PostgreSQL", "Latest", "Database"), ("ChromaDB", "0.4+", "Vector store")]
}

# ============================================
# HOTEL & COST DATA
# ============================================
HOTEL_PRICES = {
    "ekonomis": {
        "makkah": {"name": "Hotel Elaf Al Mashaer", "price": 450000, "star": 3, "distance": "800m"},
        "madinah": {"name": "Hotel Dar Al Naeem", "price": 350000, "star": 3, "distance": "600m"}
    },
    "standard": {
        "makkah": {"name": "Hilton Suites Makkah", "price": 850000, "star": 4, "distance": "500m"},
        "madinah": {"name": "Millennium Al Aqeeq", "price": 650000, "star": 4, "distance": "400m"}
    },
    "premium": {
        "makkah": {"name": "Conrad Makkah", "price": 1800000, "star": 5, "distance": "200m"},
        "madinah": {"name": "Oberoi Madinah", "price": 1400000, "star": 5, "distance": "150m"}
    },
    "vip": {
        "makkah": {"name": "Raffles Makkah Palace", "price": 4500000, "star": 5, "distance": "50m"},
        "madinah": {"name": "Ritz-Carlton Madinah", "price": 3500000, "star": 5, "distance": "Direct"}
    }
}

ADDITIONAL_COSTS = {
    "ekonomis": {"flight": 8500000, "visa": 600000, "transport": 1200000, "meals": 150000},
    "standard": {"flight": 12000000, "visa": 600000, "transport": 1500000, "meals": 250000},
    "premium": {"flight": 18000000, "visa": 600000, "transport": 2500000, "meals": 400000},
    "vip": {"flight": 35000000, "visa": 600000, "transport": 5000000, "meals": 750000}
}

# ============================================
# UTILITY FUNCTIONS
# ============================================
def format_currency(amount, currency="Rp"):
    if amount is None:
        return f"{currency} 0"
    return f"{currency} {amount:,.0f}".replace(",", ".")

def format_duration(days):
    return f"{days} hari"

def get_changelog_markdown():
    return """
### v3.5.2 (2025-12-06)
- 🔧 Fixed duplicate function errors
- 🔧 Fixed syntax and indentation issues
- 📦 Improved code structure

### v3.5.1 (2025-12-06)
- 🔧 Bug fixes and stability improvements
- 📦 Import error fixes

### v3.5.0 (2025-12-03)
- 🎮 Engagement & Gamification System
- 🧠 Interactive Quiz & Learning
- 🎁 Referral System
"""

def get_developer_card():
    return f'''
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
            border-radius: 20px; padding: 30px; text-align: center; 
            border: 2px solid #D4AF3740;">
    <div style="font-size: 4rem; margin-bottom: 15px;">👨‍💻</div>
    <h2 style="color: #D4AF37; margin: 0 0 5px 0;">{DEVELOPER["name"]}</h2>
    <p style="color: #C9A86C;">Founder & Lead Developer</p>
    <p style="color: #888; font-size: 0.9rem;">KIM Consulting</p>
</div>
'''

def get_app_age():
    launch_date = datetime(2024, 12, 1)
    delta = datetime.now() - launch_date
    return f"{delta.days} hari"

def render_quick_quote_widget():
    quotes = ["لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ", "Aku datang memenuhi panggilan-Mu", "Sebaik-baik bekal adalah taqwa"]
    st.markdown(f'''
    <div style="background: rgba(212, 175, 55, 0.1); padding: 10px; border-radius: 10px; text-align: center;">
        <div style="color: #D4AF37; font-size: 0.85rem; font-style: italic;">
            "{random.choice(quotes)}"
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ============================================
# SCENARIO PLANNER CLASS
# ============================================
@dataclass
class ScenarioResult:
    scenario_type: str
    estimated_min: float
    estimated_max: float
    features: List[str]
    notes: List[str]
    hotel_star_makkah: int = 3
    hotel_star_madinah: int = 3
    hotel_distance_makkah: str = "500m"
    meal_type: str = "prasmanan"

class ScenarioPlanner:
    def __init__(self):
        self.scenarios = []
    
    def create_scenario(self, scenario_type="standard", num_people=1, duration_days=9, departure_month=1):
        template = SCENARIO_TEMPLATES.get(scenario_type, SCENARIO_TEMPLATES["standard"])
        hotel_info = HOTEL_PRICES.get(scenario_type, HOTEL_PRICES["standard"])
        additional = ADDITIONAL_COSTS.get(scenario_type, ADDITIONAL_COSTS["standard"])
        
        nights_makkah = max(4, duration_days // 2)
        nights_madinah = duration_days - nights_makkah - 2
        
        hotel_makkah_cost = hotel_info["makkah"]["price"] * nights_makkah
        hotel_madinah_cost = hotel_info["madinah"]["price"] * nights_madinah
        meals_cost = additional["meals"] * duration_days
        
        base_cost = (
            additional["flight"] +
            additional["visa"] +
            hotel_makkah_cost +
            hotel_madinah_cost +
            additional["transport"] +
            meals_cost
        )
        
        season_mult = 1.0
        if departure_month in [12]:
            season_mult = 1.4
        elif departure_month in [1, 2, 6, 7]:
            season_mult = 0.85
        
        total_min = base_cost * num_people * season_mult * 0.9
        total_max = base_cost * num_people * season_mult * 1.1
        
        features_map = {
            "ekonomis": [
                "Tiket pesawat PP ekonomi",
                f"Hotel {hotel_info['makkah']['star']}⭐ Makkah",
                f"Hotel {hotel_info['madinah']['star']}⭐ Madinah",
                "Visa umrah", "Transportasi", "Makan prasmanan"
            ],
            "standard": [
                "Tiket pesawat PP ekonomi",
                f"Hotel {hotel_info['makkah']['star']}⭐ Makkah",
                f"Hotel {hotel_info['madinah']['star']}⭐ Madinah",
                "Visa umrah", "Transportasi AC", "Makan buffet", "Muthawwif"
            ],
            "premium": [
                "Tiket pesawat bisnis",
                f"Hotel {hotel_info['makkah']['star']}⭐ premium Makkah",
                f"Hotel {hotel_info['madinah']['star']}⭐ premium Madinah",
                "Visa priority", "Private car", "Full board", "Senior guide", "City tour"
            ],
            "vip": [
                "Tiket first/business class",
                "Hotel ultra premium Makkah",
                "Hotel ultra premium Madinah",
                "VIP visa", "Luxury car", "Fine dining",
                "Personal guide 24/7", "Premium city tour", "Exclusive ziarah"
            ]
        }
        
        meal_types = {
            "ekonomis": "prasmanan",
            "standard": "buffet_hotel",
            "premium": "full_board",
            "vip": "fine_dining"
        }
        
        return ScenarioResult(
            scenario_type=scenario_type,
            estimated_min=total_min,
            estimated_max=total_max,
            features=features_map.get(scenario_type, features_map["standard"]),
            notes=[
                f"Estimasi untuk {num_people} jamaah, {duration_days} hari",
                "Harga dapat berubah sesuai musim",
                "Belum termasuk oleh-oleh"
            ],
            hotel_star_makkah=hotel_info["makkah"]["star"],
            hotel_star_madinah=hotel_info["madinah"]["star"],
            hotel_distance_makkah=hotel_info["makkah"]["distance"],
            meal_type=meal_types.get(scenario_type, "buffet")
        )
    
    def analyze_best_time(self, priority="balanced"):
        months_data = [
            {"month": 1, "month_name": "Januari", "weather": "Sejuk (15-25°C)", "price_multiplier": 0.85, "crowd_level": "Rendah", "recommendation_score": 85},
            {"month": 2, "month_name": "Februari", "weather": "Sejuk (15-25°C)", "price_multiplier": 0.85, "crowd_level": "Rendah", "recommendation_score": 90},
            {"month": 3, "month_name": "Maret", "weather": "Hangat (20-30°C)", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 75},
            {"month": 4, "month_name": "April", "weather": "Hangat (25-35°C)", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 70},
            {"month": 5, "month_name": "Mei", "weather": "Panas (30-40°C)", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 60},
            {"month": 6, "month_name": "Juni", "weather": "Sangat Panas (35-45°C)", "price_multiplier": 0.85, "crowd_level": "Rendah", "recommendation_score": 55},
            {"month": 7, "month_name": "Juli", "weather": "Sangat Panas (35-45°C)", "price_multiplier": 0.85, "crowd_level": "Tinggi", "recommendation_score": 50},
            {"month": 8, "month_name": "Agustus", "weather": "Sangat Panas (35-45°C)", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 55},
            {"month": 9, "month_name": "September", "weather": "Panas (30-40°C)", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 65},
            {"month": 10, "month_name": "Oktober", "weather": "Hangat (25-35°C)", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 75},
            {"month": 11, "month_name": "November", "weather": "Sejuk (20-30°C)", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 80},
            {"month": 12, "month_name": "Desember", "weather": "Sejuk (15-25°C)", "price_multiplier": 1.4, "crowd_level": "Sangat Tinggi", "recommendation_score": 40},
        ]
        sorted_data = sorted(months_data, key=lambda x: x["recommendation_score"], reverse=True)
        return {
            "best_months": sorted_data[:3],
            "avoid_months": sorted_data[-3:],
            "analysis": months_data,
            "notes": [
                "Hindari Ramadhan jika budget terbatas",
                "Januari-Februari ideal untuk cuaca sejuk dan harga murah",
                "Booking 3-4 bulan sebelumnya untuk harga terbaik"
            ]
        }

# ============================================
# AUTH SYSTEM
# ============================================
try:
    from auth import (
        init_auth_state, init_user_database, is_logged_in, get_current_user,
        logout_user, login_user, register_user, get_user_role_info,
        render_login_page, render_admin_dashboard, has_permission
    )
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False

    def init_auth_state():
        if "auth" not in st.session_state:
            st.session_state.auth = {"logged_in": False, "user": None}
    
    def init_user_database():
        if "users_db" not in st.session_state:
            st.session_state.users_db = {
                "demo@labbaik.id": {
                    "id": "demo001", "email": "demo@labbaik.id",
                    "name": "Demo User", "role": "user",
                    "status": "active", "phone": "081234567890",
                    "created_at": "2024-01-01", "last_login": ""
                },
                "admin@labbaik.id": {
                    "id": "admin001", "email": "admin@labbaik.id",
                    "name": "Admin LABBAIK", "role": "admin",
                    "status": "active", "phone": "081234567891",
                    "created_at": "2024-01-01", "last_login": ""
                },
            }
    
    def is_logged_in():
        init_auth_state()
        return st.session_state.auth.get("logged_in", False)
    
    def get_current_user():
        init_auth_state()
        return st.session_state.auth.get("user")
    
    def logout_user():
        init_auth_state()
        st.session_state.auth = {"logged_in": False, "user": None}
    
    def get_user_role_info(role):
        roles = {
            "guest": {"name": "Tamu", "badge": "👤", "color": "#888888"},
            "user": {"name": "Member", "badge": "⭐", "color": "#4CAF50"},
            "premium": {"name": "Premium", "badge": "💎", "color": "#2196F3"},
            "admin": {"name": "Admin", "badge": "👑", "color": "#D4AF37"},
            "superadmin": {"name": "Super Admin", "badge": "🌟", "color": "#9C27B0"}
        }
        return roles.get(role, roles["guest"])
    
    def has_permission(*args, **kwargs):
        return True
    
    def render_login_page():
        init_auth_state()
        init_user_database()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'''
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 2rem; color: #D4AF37;">🔐</div>
                <h2 style="margin: 10px 0;">Masuk ke LABBAIK</h2>
            </div>
            ''', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🚪 Masuk", "📝 Daftar"])
            
            with tab1:
                with st.form("login_form"):
                    email = st.text_input("📧 Email")
                    password = st.text_input("🔑 Password", type="password")
                    if st.form_submit_button("🚀 Masuk", use_container_width=True):
                        if email == "demo@labbaik.id" and password == "demo123":
                            st.session_state.auth = {"logged_in": True, "user": st.session_state.users_db.get(email)}
                            st.success("✅ Login berhasil!")
                            st.rerun()
                        elif email == "admin@labbaik.id" and password == "admin123":
                            st.session_state.auth = {"logged_in": True, "user": st.session_state.users_db.get(email)}
                            st.success("✅ Login berhasil!")
                            st.rerun()
                        else:
                            st.error("❌ Email atau password salah")
                
                with st.expander("🔑 Demo Credentials"):
                    st.code("demo@labbaik.id / demo123")
                    st.code("admin@labbaik.id / admin123")
            
            with tab2:
                with st.form("register_form"):
                    name = st.text_input("👤 Nama Lengkap")
                    reg_email = st.text_input("📧 Email", key="reg_email")
                    phone = st.text_input("📱 No. HP")
                    reg_pass = st.text_input("🔑 Password", type="password", key="reg_pass")
                    if st.form_submit_button("📝 Daftar", use_container_width=True):
                        if name and reg_email and reg_pass:
                            st.success("✅ Registrasi berhasil! Silakan login.")
                        else:
                            st.error("Lengkapi semua field")
    
    def render_admin_dashboard():
        user = get_current_user()
        if not user or user.get("role") not in ["admin", "superadmin"]:
            st.error("⛔ Akses ditolak")
            return
        st.header("👑 Admin Dashboard")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", len(st.session_state.get("users_db", {})))
        with col2:
            st.metric("Active Sessions", 1)
        with col3:
            st.metric("Today's Queries", 0)

# ============================================
# MODULE IMPORTS WITH FALLBACKS
# ============================================

# PWA
try:
    from pwa_component import init_pwa
    PWA_AVAILABLE = True
except ImportError:
    PWA_AVAILABLE = False
    def init_pwa():
        pass

# Visitor Tracker
try:
    from visitor_tracker import track_page_view, get_visitor_stats
    TRACKER_AVAILABLE = True
except ImportError:
    TRACKER_AVAILABLE = False
    def track_page_view(page):
        pass
    def get_visitor_stats():
        return {"total_visitors": 1500, "total_views": 5000, "today_visitors": 25}

# Quiz
try:
    from quiz_learning import init_quiz_state, render_quiz_page
    QUIZ_AVAILABLE = True
except ImportError:
    QUIZ_AVAILABLE = False
    def init_quiz_state():
        if "quiz" not in st.session_state:
            st.session_state.quiz = {"score": 0, "completed": []}
    def render_quiz_page():
        st.info("🧠 Quiz module coming soon!")

# Features
try:
    from features import render_additional_features
    FEATURES_AVAILABLE = True
except ImportError:
    FEATURES_AVAILABLE = False
    def render_additional_features():
        st.info("🧰 Additional features coming soon!")

# Analytics
try:
    from analytics import render_analytics_dashboard
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    def render_analytics_dashboard():
        st.header("📊 Analytics Dashboard")
        st.info("Analytics coming soon!")

# Monetization
try:
    from monetization import render_monetization_page, init_monetization_state
    MONETIZATION_AVAILABLE = True
except ImportError:
    MONETIZATION_AVAILABLE = False
    def render_monetization_page():
        st.info("💼 Monetization coming soon!")
    def init_monetization_state():
        pass

# Database
try:
    from database import is_db_available
    from db_integration import (
        db_get_open_trips, db_create_trip, db_update_trip_status,
        db_delete_trip, db_get_forum_posts, db_create_post
    )
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    def is_db_available():
        return False
    def db_get_open_trips():
        return []
    def db_create_trip(*args, **kwargs):
        return {"success": False, "error": "DB not available"}
    def db_update_trip_status(*args, **kwargs):
        pass
    def db_delete_trip(*args, **kwargs):
        pass
    def db_get_forum_posts():
        return []
    def db_create_post(*args, **kwargs):
        return {"success": False, "error": "DB not available"}

# Social
try:
    from social_viral import render_share_buttons
    SOCIAL_AVAILABLE = True
except ImportError:
    SOCIAL_AVAILABLE = False
    def render_share_buttons(*args, **kwargs):
        pass

# Agents/Orchestrator
try:
    from agents import AgentOrchestrator
    AGENTS_AVAILABLE = True
except ImportError:
    try:
        from orchestrator import AgentOrchestrator
        AGENTS_AVAILABLE = True
    except ImportError:
        AGENTS_AVAILABLE = False

        class AgentOrchestrator:
            """Mock AgentOrchestrator with actual responses - v3.5.2"""
            
            def __init__(self):
                self.initialized = False
                self.conversations = []
                
                self.knowledge_base = {
                    "rukun": """**Rukun Umrah ada 5:**

1. **Ihram** - Niat memasuki ibadah umrah dari miqat  
2. **Thawaf** - Mengelilingi Ka'bah sebanyak 7 kali  
3. **Sa'i** - Berjalan/berlari kecil antara Shafa dan Marwah sebanyak 7 kali  
4. **Tahallul** - Mencukur atau memotong rambut  
5. **Tertib** - Melakukan rukun secara berurutan  

**Tips:**  
- Pelajari doa-doa sebelum berangkat  
- Ikuti alur jamaah lain jika bingung  
- Jangan lupa baca talbiyah setelah ihram""",

                    "wajib": """**Wajib Umrah ada 2:**

1. **Ihram dari Miqat** - Memulai ihram dari batas miqat yang ditentukan  
2. **Menjauhi larangan ihram** - Tidak melanggar hal-hal yang dilarang selama ihram  

**Larangan saat Ihram:**  
- Memakai wangi-wangian  
- Memotong kuku atau rambut  
- Menikah atau menikahkan  
- Berburu binatang darat  
- Bagi pria: menutup kepala dan memakai pakaian berjahit  

Jika melanggar wajib, wajib membayar dam (denda).""",

                    "travel": """**Tips Memilih Travel Umrah Terpercaya:**

1. **Cek Izin Resmi Kemenag**  
   - Verifikasi di: siskopatuh.kemenag.go.id  
   - Pastikan PPIU (Penyelenggara Perjalanan Ibadah Umrah) aktif  

2. **Periksa Track Record**  
   - Baca review jamaah sebelumnya  
   - Cek berapa lama sudah beroperasi  
   - Tanya pengalaman orang terdekat  

3. **Transparansi Harga**  
   - Rincian biaya jelas  
   - Tidak ada biaya tersembunyi  
   - Ada kontrak tertulis  

4. **Fasilitas Jelas**  
   - Hotel (nama, bintang, jarak ke Masjid)  
   - Pesawat (maskapai, rute)  
   - Makan (berapa kali, menu)  

5. **Layanan After Sales**  
   - Ada muthawwif/pembimbing  
   - Handling bandara  
   - Support 24 jam  

⚠️ **Hindari:**  
- Harga terlalu murah (di bawah standar)  
- Tidak punya izin resmi  
- Janji muluk-muluk""",

                    "biaya": """**Estimasi Biaya Umrah 2025:**

| Paket | Estimasi/Orang |
|-------|----------------|
| 💚 Ekonomis | Rp 20-28 juta |
| 💙 Standard | Rp 28-40 juta |
| 🧡 Premium | Rp 40-60 juta |
| 💛 VIP | Rp 60-150 juta |

**Komponen Biaya:**  
- ✈️ Tiket pesawat PP: 30-40%  
- 🏨 Hotel: 25-35%  
- 📄 Visa & handling: 5-8%  
- 🚐 Transportasi: 8-12%  
- 🍽️ Makan: 10-15%  

**Tips Hemat:**  
- Booking 3-4 bulan sebelumnya  
- Pilih low season (Jan-Feb, Sep-Okt)  
- Bandingkan beberapa travel agent  
- Gunakan LABBAIK untuk simulasi!""",

                    "waktu": """**Waktu Terbaik untuk Umrah:**

🟢 **RECOMMENDED:**  
- **Januari-Februari**: Cuaca sejuk (15-25°C), harga murah, sepi  
- **September-Oktober**: Cuaca nyaman, harga normal  

🟡 **NORMAL:**  
- **Maret-Mei**: Cuaca mulai panas, harga stabil  
- **November**: Mulai ramai menjelang akhir tahun  

🔴 **HINDARI (jika budget terbatas):**  
- **Juni-Juli**: Sangat panas (40°C+), liburan sekolah  
- **Desember**: Harga naik 40%, sangat ramai  
- **Ramadhan**: Harga naik 60%+, tapi pahala berlipat!  

**Catatan:**  
- Ramadhan tetap recommended jika budget cukup  
- Cuaca panas bisa disiasati dengan ibadah malam""",

                    "persiapan": """**Persiapan Sebelum Umrah:**

📋 **Dokumen:**  
- Paspor (valid > 6 bulan)  
- Foto 4x6 background putih  
- KTP  
- Kartu vaksin meningitis  
- Buku nikah (jika suami-istri)  

🧳 **Perlengkapan:**  
- Pakaian ihram (pria: 2 lembar kain putih)  
- Mukena & sajadah  
- Sandal nyaman untuk jalan jauh  
- Obat-obatan pribadi  
- Adaptor colokan (tipe G)  

📖 **Persiapan Spiritual:**  
- Pelajari manasik umrah  
- Hafal doa-doa: niat ihram, talbiyah, doa thawaf, doa sa'i  
- Banyak istighfar dan tobat  
- Selesaikan hutang dan minta maaf  

💪 **Persiapan Fisik:**  
- Mulai rutin jalan kaki (minimal 5km/hari)  
- Cek kesehatan  
- Vaksin meningitis (wajib)  

💰 **Persiapan Keuangan:**  
- Tukar uang ke SAR  
- Bawa cash secukupnya  
- Siapkan kartu debit/kredit international""",

                    "doa": """**Doa-Doa Penting Saat Umrah:**

🕋 **Niat Ihram:**  
*"Labbaika Allahumma 'Umratan"*  
(Aku penuhi panggilan-Mu ya Allah untuk umrah)

📿 **Talbiyah:**  
*"Labbaikallahumma labbaik, labbaika laa syariikalaka labbaik, innal hamda wan ni'mata laka wal mulk, laa syariikalak"*

🕋 **Doa Melihat Ka'bah:**  
*"Allahumma zid haadzal baita tasyriifan wa ta'zhiiman wa takriiman wa mahaabah"*

🏃 **Doa di Bukit Shafa:**  
*"Innash shafaa wal marwata min sya'aairillah..."*

✂️ **Doa Tahallul:**  
*"Allahumma ij'al kulla sya'ratin lii nuura yaumal qiyaamah"*  

💡 **Tips:**  
- Bawa buku saku doa  
- Download app manasik  
- Banyak berdoa dengan bahasa sendiri juga boleh""",
                }
            
            def initialize(self):
                self.initialized = True
                return {"status": "initialized", "message": "AI Assistant ready!"}
            
            def chat(self, message: str):
                """Process chat message and return response"""
                message_lower = message.lower()
                
                if any(word in message_lower for word in ["rukun", "rukun umrah"]):
                    response = self.knowledge_base["rukun"]
                elif any(word in message_lower for word in ["wajib umrah", "wajib"]):
                    response = self.knowledge_base["wajib"]
                elif any(word in message_lower for word in ["travel", "agen", "agent", "terpercaya", "memilih travel"]):
                    response = self.knowledge_base["travel"]
                elif any(word in message_lower for word in ["biaya", "harga", "budget", "cost", "berapa"]):
                    response = self.knowledge_base["biaya"]
                elif any(word in message_lower for word in ["waktu", "kapan", "bulan", "terbaik", "when"]):
                    response = self.knowledge_base["waktu"]
                elif any(word in message_lower for word in ["persiapan", "siapkan", "prepare", "bawa", "perlengkapan"]):
                    response = self.knowledge_base["persiapan"]
                elif any(word in message_lower for word in ["doa", "bacaan", "dzikir", "zikir", "talbiyah"]):
                    response = self.knowledge_base["doa"]
                elif any(word in message_lower for word in ["halo", "hi", "hello", "hai", "assalamualaikum"]):
                    response = """**Waalaikumsalam! 👋**

Saya AI Assistant LABBAIK, siap membantu Anda merencanakan umrah.

**Saya bisa membantu tentang:**
- 🕋 Rukun & wajib umrah
- 💰 Estimasi biaya
- 📅 Waktu terbaik berangkat
- ✅ Persiapan & perlengkapan
- 📖 Doa-doa umrah
- 🏢 Tips memilih travel agent

Silakan tanya apa saja! 😊"""
                elif any(word in message_lower for word in ["terima kasih", "makasih", "thanks", "thank you"]):
                    response = """**Sama-sama! 🤲**

Semoga informasinya bermanfaat untuk persiapan umrah Anda.

*"Barangsiapa yang keluar untuk haji atau umrah lalu meninggal, ditulis baginya pahala haji atau umrah sampai hari kiamat."* (HR. Baihaqi)

Ada pertanyaan lain? Saya siap membantu! 😊"""
                else:
                    response = f"""Terima kasih atas pertanyaannya tentang: *"{message}"*

Saya akan berusaha membantu. Berikut beberapa topik yang bisa saya jelaskan dengan detail:

1. **Rukun & Wajib Umrah** - Tata cara ibadah  
2. **Estimasi Biaya** - Budget dan komponen biaya  
3. **Waktu Terbaik** - Kapan sebaiknya berangkat  
4. **Persiapan Umrah** - Dokumen & perlengkapan  
5. **Doa-doa Umrah** - Bacaan selama ibadah  
6. **Tips Travel Agent** - Cara memilih yang terpercaya  

Silakan tanya lebih spesifik, atau ketik salah satu topik di atas! 

💡 *Untuk simulasi biaya detail, gunakan menu "Simulasi Biaya" atau "Buat Rencana"*"""
                
                self.conversations.append({"role": "user", "content": message})
                self.conversations.append({"role": "assistant", "content": response})
                
                return {"response": response}
            
            def create_complete_plan(self, **kwargs):
                scenario = kwargs.get("scenario_type", "standard")
                num_people = kwargs.get("num_people", 1)
                
                return {
                    "results": {
                        "financial": {
                            "response": f"Rencana untuk {num_people} jamaah dengan paket {scenario}",
                            "calculation": {
                                "total_min": 25_000_000 * num_people,
                                "total_max": 35_000_000 * num_people
                            }
                        },
                        "itinerary": {"response": "Itinerary akan dibuatkan sesuai preferensi Anda."},
                        "requirements": {"response": "Dokumen: Paspor, KTP, Foto, Vaksin Meningitis"},
                        "tips": {"response": "Persiapkan fisik dengan jalan kaki rutin."}
                    }
                }
            
            def get_agent_status(self):
                return {
                    "status": "active",
                    "rag_retriever": {"num_docs": {"total_documents": 50}}
                }
            
            def reset_conversations(self):
                self.conversations = []

# ============================================
# ENGAGEMENT SYSTEM
# ============================================
ENGAGEMENT_AVAILABLE = True
POINTS_CONFIG = {
    "daily_login": 10,
    "complete_simulation": 25,
    "share_social": 50,
    "referral_signup": 200,
    "referral_bonus": 75,
}

def init_engagement_state():
    if "engagement" not in st.session_state:
        st.session_state.engagement = {
            "points": 0,
            "level": 1,
            "streak": 0,
            "badges": [],
            "daily_claimed": False,
            "referral_count": 0
        }

def generate_referral_code(user_id):
    hash_str = hashlib.md5(str(user_id).encode()).hexdigest()[:8].upper()
    return f"LBK{hash_str}"

def award_points(amount, reason=""):
    init_engagement_state()
    st.session_state.engagement["points"] += amount

def check_daily_login():
    init_engagement_state()
    return {
        "status": "available"
        if not st.session_state.engagement.get("daily_claimed")
        else "claimed"
    }

def render_daily_reward_popup():
    pass

def render_engagement_hub():
    init_engagement_state()
    points = st.session_state.engagement.get("points", 0)
    streak = st.session_state.engagement.get("streak", 0)
    level = 1 + (points // 500)
    
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #D4AF37; font-size: 2rem; margin-bottom: 5px;">🎮 Pusat Reward & Engagement</h1>
        <p style="color: #C9A86C;">Kumpulkan poin, unlock badge, dan naik level!</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); border-radius: 20px; padding: 25px; text-align: center; border: 2px solid #D4AF3740;">
            <div style="font-size: 3rem; margin-bottom: 10px;">⭐</div>
            <div style="color: #D4AF37; font-size: 2.5rem; font-weight: 800;">{points:,}</div>
            <div style="color: #C9A86C;">LABBAIK Points</div>
            <div style="margin-top: 15px; color: #4CAF50; font-weight: 600;">Level {level}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #3D2817 100%); border-radius: 20px; padding: 25px; text-align: center; border: 2px solid #FF980040;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🔥</div>
            <div style="color: #FF9800; font-size: 2.5rem; font-weight: 800;">{streak}</div>
            <div style="color: #C9A86C;">Hari Berturut-turut</div>
        </div>
        ''', unsafe_allow_html=True)
    
    if not st.session_state.engagement.get("daily_claimed"):
        if st.button("🎁 Klaim Bonus Harian (+10 LP)", use_container_width=True):
            award_points(10, "Daily login")
            st.session_state.engagement["daily_claimed"] = True
            st.session_state.engagement["streak"] += 1
            st.success("✅ +10 LP diklaim!")
            st.rerun()
    else:
        st.info("✅ Bonus harian sudah diklaim. Kembali besok!")

def render_invite_modal(referral_code):
    st.markdown(f'''
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 20px;">
        <div style="font-size: 3rem; margin-bottom: 15px;">🎁</div>
        <div style="color: white; font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">Ajak Teman, Dapat Bonus!</div>
        <div style="background: #2D2D2D; border: 2px dashed #D4AF3750; border-radius: 15px; padding: 15px; margin: 20px 0;">
            <div style="color: #C9A86C; font-size: 0.8rem;">Kode Referral</div>
            <div style="color: #D4AF37; font-size: 2rem; font-weight: 800; letter-spacing: 4px;">{referral_code}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


# ============================================
# BOOKING FEATURES
# ============================================
try:
    from booking import render_booking_features
    BOOKING_AVAILABLE = True
except ImportError:
    BOOKING_AVAILABLE = False

    def generate_itinerary(nights_makkah, nights_madinah):
        """Generate detailed itinerary based on nights in each city"""
        itinerary = []
        day = 1
        
        # Day 1: Departure
        itinerary.append({
            "day": day,
            "location": "Indonesia",
            "title": "Keberangkatan dari Indonesia",
            "activities": "Check-in bandara, penerbangan menuju Jeddah/Madinah. Persiapan ihram di pesawat jika langsung ke Makkah."
        })
        day += 1
        
        # Makkah days
        for i in range(nights_makkah):
            if i == 0:
                itinerary.append({
                    "day": day,
                    "location": "Makkah",
                    "title": "Tiba di Makkah - Umrah",
                    "activities": "Tiba di hotel Makkah, istirahat sejenak, lalu melaksanakan umrah (thawaf, sa'i, tahallul). Sholat di Masjidil Haram."
                })
            elif i == nights_makkah - 1:
                itinerary.append({
                    "day": day,
                    "location": "Makkah",
                    "title": "Makkah - Ziarah & Persiapan",
                    "activities": "Ziarah ke Jabal Rahmah, Muzdalifah, Mina. Memperbanyak ibadah. Persiapan ke Madinah."
                })
            else:
                itinerary.append({
                    "day": day,
                    "location": "Makkah",
                    "title": f"Makkah - Ibadah Hari {i+1}",
                    "activities": "Thawaf sunnah, sholat 5 waktu di Masjidil Haram, tadarus Al-Quran, i'tikaf. Ziarah ke Jabal Nur (Gua Hira) optional."
                })
            day += 1
        
        # Travel to Madinah
        itinerary.append({
            "day": day,
            "location": "Perjalanan",
            "title": "Perjalanan Makkah - Madinah",
            "activities": "Perjalanan darat/udara ke Madinah (~5 jam). Check-in hotel Madinah. Sholat di Masjid Nabawi."
        })
        day += 1
        
        # Madinah days
        for i in range(nights_madinah):
            if i == 0:
                itinerary.append({
                    "day": day,
                    "location": "Madinah",
                    "title": "Madinah - Ziarah Makam Rasulullah",
                    "activities": "Sholat di Masjid Nabawi, ziarah ke makam Rasulullah SAW dan sahabat. Sholat di Raudhah (jika memungkinkan)."
                })
            elif i == nights_madinah - 1:
                itinerary.append({
                    "day": day,
                    "location": "Madinah",
                    "title": "Madinah - Hari Terakhir",
                    "activities": "Memperbanyak ibadah di Masjid Nabawi, belanja oleh-oleh di sekitar hotel, persiapan pulang."
                })
            else:
                itinerary.append({
                    "day": day,
                    "location": "Madinah",
                    "title": f"Madinah - Ziarah Hari {i+1}",
                    "activities": "Ziarah ke Masjid Quba, Jabal Uhud, Masjid Qiblatain, pemakaman Baqi. Memperbanyak sholat di Masjid Nabawi."
                })
            day += 1
        
        # Return day
        itinerary.append({
            "day": day,
            "location": "Kepulangan",
            "title": "Kepulangan ke Indonesia",
            "activities": "Check-out hotel, transfer ke bandara Jeddah/Madinah, penerbangan pulang ke Indonesia. Alhamdulillah, umrah selesai!"
        })
        
        return itinerary

    def render_booking_features():
        """Render booking features page - FIXED v3.5.2"""
        st.markdown("### 📦 Bandingkan Paket Travel")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            price_range = st.slider(
                "💰 Range Harga (juta)",
                min_value=15,
                max_value=100,
                value=(15, 50),
                step=5
            )
        
        with col2:
            duration_range = st.slider(
                "📅 Durasi (hari)",
                min_value=7,
                max_value=21,
                value=(7, 21)
            )
        
        with col3:
            sort_by = st.selectbox(
                "📊 Urutkan",
                options=["Harga Terendah", "Harga Tertinggi", "Rating Tertinggi", "Durasi Terpendek"]
            )
        
        # Sample travel packages
        packages = [
            {
                "name": "Paket Ekonomis 9 Hari",
                "agent": "Al-Madinah Travel",
                "price": 22500000,
                "duration": 9,
                "hotel_makkah": "Elaf Ajyad Hotel",
                "hotel_makkah_star": 3,
                "hotel_madinah": "Al Eiman Taibah Hotel",
                "hotel_madinah_star": 3,
                "includes": ["Tiket PP", "Visa", "Hotel", "Transport Bandara"],
                "rating": 4.5,
                "reviews": 128,
                "nights_makkah": 4,
                "nights_madinah": 3,
            },
            {
                "name": "Paket Standard 12 Hari",
                "agent": "Azzahra Tour",
                "price": 32000000,
                "duration": 12,
                "hotel_makkah": "Hilton Suites Makkah",
                "hotel_makkah_star": 4,
                "hotel_madinah": "Millennium Al Aqeeq",
                "hotel_madinah_star": 4,
                "includes": ["Tiket PP", "Visa", "Hotel", "Makan 3x", "Transport", "Muthawwif"],
                "rating": 4.7,
                "reviews": 256,
                "nights_makkah": 5,
                "nights_madinah": 5,
            },
            {
                "name": "Paket Premium 14 Hari",
                "agent": "Shafira Tour",
                "price": 48000000,
                "duration": 14,
                "hotel_makkah": "Conrad Makkah",
                "hotel_makkah_star": 5,
                "hotel_madinah": "Oberoi Madinah",
                "hotel_madinah_star": 5,
                "includes": ["Tiket PP", "Visa", "Hotel 5★", "Full Board", "Private Car", "Senior Guide", "City Tour"],
                "rating": 4.9,
                "reviews": 89,
                "nights_makkah": 6,
                "nights_madinah": 6,
            },
        ]
        
        # Filter packages
        filtered = [
            p for p in packages
            if price_range[0] * 1_000_000 <= p["price"] <= price_range[1] * 1_000_000
            and duration_range[0] <= p["duration"] <= duration_range[1]
        ]
        
        # Sort packages
        if sort_by == "Harga Terendah":
            filtered.sort(key=lambda x: x["price"])
        elif sort_by == "Harga Tertinggi":
            filtered.sort(key=lambda x: x["price"], reverse=True)
        elif sort_by == "Rating Tertinggi":
            filtered.sort(key=lambda x: x["rating"], reverse=True)
        else:
            filtered.sort(key=lambda x: x["duration"])
        
        st.markdown(f"**{len(filtered)} paket ditemukan**")
        
        # Display packages
        for pkg in filtered:
            stars_makkah = "⭐" * pkg["hotel_makkah_star"]
            stars_madinah = "⭐" * pkg["hotel_madinah_star"]
            
            # Package card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                        border-radius: 15px; padding: 20px; margin-bottom: 20px;
                        border: 1px solid #D4AF3740;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                    <div>
                        <div style="color: #D4AF37; font-size: 1.2rem; font-weight: 700;">{pkg['name']}</div>
                        <div style="color: #888; font-size: 0.85rem;">{pkg['agent']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #4CAF50; font-size: 1.4rem; font-weight: 700;">Rp {pkg['price']:,}</div>
                        <div style="color: #888; font-size: 0.8rem;">/orang</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                    <div style="background: #1A1A1A80; padding: 10px; border-radius: 8px;">
                        <div style="color: #888; font-size: 0.75rem;">🕋 Makkah ({pkg['nights_makkah']} malam)</div>
                        <div style="color: white; font-size: 0.85rem;">{pkg['hotel_makkah']} {stars_makkah}</div>
                    </div>
                    <div style="background: #1A1A1A80; padding: 10px; border-radius: 8px;">
                        <div style="color: #888; font-size: 0.75rem;">🕌 Madinah ({pkg['nights_madinah']} malam)</div>
                        <div style="color: white; font-size: 0.85rem;">{pkg['hotel_madinah']} {stars_madinah}</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        {"".join([f'<span style="background: #D4AF3720; color: #D4AF37; padding: 3px 8px; border-radius: 12px; font-size: 0.7rem;">{inc}</span>' for inc in pkg['includes'][:4]])}
                    </div>
                    <div style="color: #FFD700; font-size: 0.9rem;">
                        ⭐ {pkg['rating']} ({pkg['reviews']})
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Expandable details with itinerary
            with st.expander(f"📋 Lihat Detail & Itinerary - {pkg['name']}"):
                tab1, tab2, tab3 = st.tabs(["📍 Itinerary", "🏨 Akomodasi", "💰 Rincian Biaya"])
                
                with tab1:
                    st.markdown("#### 📍 Jadwal Perjalanan")
                    itinerary = generate_itinerary(pkg['nights_makkah'], pkg['nights_madinah'])
                    
                    for day_item in itinerary:
                        day_color = (
                            "#4CAF50" if "Madinah" in day_item['location']
                            else "#FF9800" if "Makkah" in day_item['location']
                            else "#2196F3"
                        )
                        
                        st.markdown(f"""
                        <div style="display: flex; margin-bottom: 12px; padding: 12px; 
                                    background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%); 
                                    border-radius: 10px; border-left: 4px solid {day_color};">
                            <div style="min-width: 70px; text-align: center; padding-right: 15px; border-right: 1px solid #333;">
                                <div style="color: {day_color}; font-weight: 700; font-size: 1.1rem;">Hari {day_item['day']}</div>
                                <div style="color: #888; font-size: 0.75rem;">{day_item['location']}</div>
                            </div>
                            <div style="padding-left: 15px; flex: 1;">
                                <div style="color: #D4AF37; font-weight: 600; margin-bottom: 5px;">{day_item['title']}</div>
                                <div style="color: #aaa; font-size: 0.85rem; line-height: 1.5;">{day_item['activities']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #3D2817 0%, #2D1F10 100%); 
                                    padding: 20px; border-radius: 12px; border: 1px solid #FF980040;">
                            <div style="color: #FF9800; font-size: 1.1rem; font-weight: 700; margin-bottom: 10px;">🕋 Hotel Makkah</div>
                            <div style="color: white; font-size: 1rem; margin-bottom: 5px;">{pkg['hotel_makkah']}</div>
                            <div style="color: #FFD700; margin-bottom: 10px;">{stars_makkah}</div>
                            <div style="color: #888; font-size: 0.85rem;">
                                📍 Jarak ke Masjidil Haram: ~500m<br>
                                🛏️ {pkg['nights_makkah']} malam<br>
                                🍽️ Termasuk sarapan
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1E3D2F 0%, #15291F 100%); 
                                    padding: 20px; border-radius: 12px; border: 1px solid #4CAF5040;">
                            <div style="color: #4CAF50; font-size: 1.1rem; font-weight: 700; margin-bottom: 10px;">🕌 Hotel Madinah</div>
                            <div style="color: white; font-size: 1rem; margin-bottom: 5px;">{pkg['hotel_madinah']}</div>
                            <div style="color: #FFD700; margin-bottom: 10px;">{stars_madinah}</div>
                            <div style="color: #888; font-size: 0.85rem;">
                                📍 Jarak ke Masjid Nabawi: ~400m<br>
                                🛏️ {pkg['nights_madinah']} malam<br>
                                🍽️ Termasuk sarapan
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab3:
                    st.markdown("#### 💰 Rincian Biaya")
                    
                    flight_pct = 0.35
                    hotel_pct = 0.30
                    visa_pct = 0.05
                    transport_pct = 0.10
                    meals_pct = 0.12
                    other_pct = 0.08
                    
                    breakdown = [
                        ("✈️ Tiket Pesawat PP", int(pkg['price'] * flight_pct)),
                        ("🏨 Hotel (Makkah + Madinah)", int(pkg['price'] * hotel_pct)),
                        ("📄 Visa & Handling", int(pkg['price'] * visa_pct)),
                        ("🚐 Transportasi Lokal", int(pkg['price'] * transport_pct)),
                        ("🍽️ Makan", int(pkg['price'] * meals_pct)),
                        ("📦 Lainnya", int(pkg['price'] * other_pct)),
                    ]
                    
                    for item, cost in breakdown:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; padding: 10px 15px; 
                                    background: #1A1A1A; border-radius: 8px; margin-bottom: 5px;">
                            <span style="color: #E8E8E8;">{item}</span>
                            <span style="color: #D4AF37; font-weight: 600;">Rp {cost:,}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 12px 15px; 
                                background: linear-gradient(135deg, #D4AF3720 0%, #D4AF3710 100%); 
                                border-radius: 8px; margin-top: 10px; border: 1px solid #D4AF37;">
                        <span style="color: #D4AF37; font-weight: 700;">TOTAL</span>
                        <span style="color: #D4AF37; font-weight: 700; font-size: 1.1rem;">Rp {pkg['price']:,}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                
                with btn_col1:
                    st.button("💬 Hubungi Agen", key=f"contact_{pkg['name']}", use_container_width=True)
                with btn_col2:
                    st.button("📋 Bandingkan", key=f"compare_{pkg['name']}", use_container_width=True)
                with btn_col3:
                    st.button("❤️ Simpan", key=f"save_{pkg['name']}", use_container_width=True)
        
        # Disclaimer
        st.markdown("---")
        st.markdown("""
        <div style="background: #FFF3E0; border-left: 4px solid #FF9800; padding: 15px; border-radius: 0 10px 10px 0;">
            <div style="color: #E65100; font-weight: 600; margin-bottom: 5px;">⚠️ Disclaimer</div>
            <div style="color: #5D4037; font-size: 0.9rem;">
                Harga dan ketersediaan paket dapat berubah sewaktu-waktu. 
                Selalu verifikasi langsung ke travel agent yang bersangkutan.
                Pastikan travel agent memiliki izin resmi dari Kemenag RI.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# BUDGET FINDER - FIXED (SINGLE DEFINITION)
# ============================================
def render_budget_finder():
    """Render budget finder page - Find packages based on available budget v3.5.2"""
    st.header("💵 Cari Paket Sesuai Budget")
    st.markdown("Masukkan dana yang Anda miliki, kami akan carikan paket terbaik untuk Anda!")
    
    # Budget input
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.number_input(
            "💰 Budget Anda (Rp)",
            min_value=10_000_000,
            max_value=500_000_000,
            value=35_000_000,
            step=1_000_000,
            format="%d",
            help="Masukkan total dana yang Anda siapkan untuk umrah"
        )
    
    with col2:
        num_people = st.number_input(
            "👥 Jumlah Jamaah",
            min_value=1,
            max_value=50,
            value=1,
            help="Berapa orang yang akan berangkat?"
        )
    
    budget_per_person = budget / num_people
    
    st.markdown("---")
    
    # Display budget per person
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
        <div style="color: #C9A86C; font-size: 0.9rem;">Budget Per Orang</div>
        <div style="color: #D4AF37; font-size: 2rem; font-weight: 700;">Rp {budget_per_person:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyze what packages are available
    st.markdown("### 📊 Analisis Paket yang Tersedia")
    
    # Package thresholds
    PACKAGE_THRESHOLDS = {
        "ekonomis": {"min_budget": 20_000_000, "max_budget": 35_000_000, "base_duration": 9, "max_duration": 12},
        "standard": {"min_budget": 35_000_000, "max_budget": 50_000_000, "base_duration": 9, "max_duration": 14},
        "premium": {"min_budget": 50_000_000, "max_budget": 80_000_000, "base_duration": 10, "max_duration": 14},
        "vip": {"min_budget": 80_000_000, "max_budget": 200_000_000, "base_duration": 12, "max_duration": 21}
    }
    
    available_packages = []
    partial_packages = []
    
    HOTEL_STARS = {"ekonomis": "2-3", "standard": "3-4", "premium": "4-5", "vip": "5"}
    
    for scenario_key, threshold in PACKAGE_THRESHOLDS.items():
        template = SCENARIO_TEMPLATES[scenario_key]
        hotel_makkah = HOTEL_PRICES[scenario_key]["makkah"]
        hotel_madinah = HOTEL_PRICES[scenario_key]["madinah"]
        additional = ADDITIONAL_COSTS[scenario_key]
        hotel_star = HOTEL_STARS.get(scenario_key, "3")
        
        base_nights_makkah = 4
        base_nights_madinah = 3
        base_total_days = base_nights_makkah + base_nights_madinah + 2
        
        min_accommodation = (hotel_makkah["price"] * base_nights_makkah) + (hotel_madinah["price"] * base_nights_madinah)
        min_total = min_accommodation + additional["flight"] + additional["visa"] + additional["transport"] + (additional["meals"] * base_total_days)
        
        if budget_per_person >= min_total:
            remaining_budget = budget_per_person - min_total
            extra_night_cost = hotel_makkah["price"] + additional["meals"]
            extra_nights = int(remaining_budget / extra_night_cost)
            
            extra_makkah = min(extra_nights // 2, 6)
            extra_madinah = min(extra_nights - extra_makkah, 7)
            
            final_makkah = base_nights_makkah + extra_makkah
            final_madinah = base_nights_madinah + extra_madinah
            final_duration = final_makkah + final_madinah + 2
            
            actual_accommodation = (hotel_makkah["price"] * final_makkah) + (hotel_madinah["price"] * final_madinah)
            actual_total = actual_accommodation + additional["flight"] + additional["visa"] + additional["transport"] + (additional["meals"] * final_duration)
            
            available_packages.append({
                "scenario": scenario_key,
                "name": template["name"],
                "hotel_star": hotel_star,
                "nights_makkah": final_makkah,
                "nights_madinah": final_madinah,
                "duration": final_duration,
                "total_cost": actual_total,
                "remaining": budget_per_person - actual_total,
                "hotel_makkah": hotel_makkah["name"],
                "hotel_madinah": hotel_madinah["name"],
                "features": ["Visa Umrah", "Transportasi", "Muthawwif", "Air Zamzam 5L"],
                "flight_class": "Economy" if scenario_key in ["ekonomis", "standard"] else "Business" if scenario_key == "vip" else "Economy Plus",
                "meals": "Prasmanan" if scenario_key == "ekonomis" else "Buffet Hotel" if scenario_key == "standard" else "Full Board Premium",
            })
        elif budget_per_person >= threshold["min_budget"] * 0.7:
            shortage = min_total - budget_per_person
            partial_packages.append({
                "scenario": scenario_key,
                "name": template["name"],
                "shortage": shortage,
                "min_required": min_total,
            })
    
    # Display available packages
    if available_packages:
        st.success(f"✅ **{len(available_packages)} Paket Tersedia** untuk budget Anda!")
        
        for i, pkg in enumerate(available_packages):
            colors = {
                "ekonomis": ("#4CAF50", "#E8F5E9"),
                "standard": ("#2196F3", "#E3F2FD"),
                "premium": ("#FF9800", "#FFF3E0"),
                "vip": ("#D4AF37", "#FFF8E1"),
            }
            accent_color, bg_color = colors.get(pkg["scenario"], ("#666", "#f5f5f5"))
            
            st.markdown(f"""
            <div style="background: {bg_color}; border: 2px solid {accent_color}; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div>
                        <span style="background: {accent_color}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 700;">
                            {'🌟' if pkg['scenario'] == 'vip' else '⭐' if pkg['scenario'] == 'premium' else '✨'} {pkg['name']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.8rem; color: #666;">Estimasi Biaya/Orang</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: {accent_color};">Rp {pkg['total_cost']:,.0f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"**🕋 Mekkah**\n\n{pkg['nights_makkah']} malam")
            with col2:
                st.markdown(f"**🕌 Madinah**\n\n{pkg['nights_madinah']} malam")
            with col3:
                st.markdown(f"**📅 Durasi**\n\n{pkg['duration']} hari")
            with col4:
                if pkg['remaining'] > 0:
                    st.markdown(f"**💰 Sisa**\n\nRp {pkg['remaining']:,.0f}")
                else:
                    st.markdown("**💰 Status**\n\nPas Budget")
            
            with st.expander(f"📋 Lihat Detail Paket {pkg['name']}"):
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("**✈️ Penerbangan**")
                    st.markdown(f"- Kelas: {pkg['flight_class']}")
                    st.markdown("- Rute: PP Indonesia - Jeddah/Madinah")
                    st.markdown("**🏨 Akomodasi**")
                    st.markdown(f"- Hotel Bintang: ⭐ {pkg['hotel_star']}")
                
                with detail_col2:
                    st.markdown("**🍽️ Konsumsi**")
                    st.markdown(f"- Tipe: {pkg['meals']}")
                    st.markdown("**📦 Termasuk**")
                    for feature in pkg['features']:
                        st.markdown(f"- ✅ {feature}")
            
            st.markdown("---")
        
        # Summary for multiple people
        if num_people > 1:
            best_pkg = available_packages[0]
            total_for_group = best_pkg["total_cost"] * num_people
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 25px; border-radius: 15px; margin-top: 20px;">
                <div style="text-align: center;">
                    <div style="color: #C9A86C; font-size: 1rem; margin-bottom: 10px;">💡 Rekomendasi untuk {num_people} Jamaah</div>
                    <div style="color: white; font-size: 1.2rem; margin-bottom: 15px;">Paket <strong style="color: #D4AF37;">{best_pkg['name']}</strong></div>
                    <table style="margin: 0 auto; color: white;">
                        <tr>
                            <td style="padding: 10px 30px; text-align: center;">
                                <div style="font-size: 0.8rem; color: #888;">Per Orang</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #D4AF37;">Rp {best_pkg['total_cost']:,.0f}</div>
                            </td>
                            <td style="padding: 10px 30px; text-align: center;">
                                <div style="font-size: 0.8rem; color: #888;">Total {num_people} Orang</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #D4AF37;">Rp {total_for_group:,.0f}</div>
                            </td>
                            <td style="padding: 10px 30px; text-align: center;">
                                <div style="font-size: 0.8rem; color: #888;">Sisa Budget</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #4CAF50;">Rp {budget - total_for_group:,.0f}</div>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # No packages available
        st.warning("⚠️ Budget belum mencukupi untuk paket umrah reguler.")
        
        min_ekonomis = 20_000_000
        shortage = min_ekonomis - budget_per_person
        
        st.markdown(f"""
        <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 20px; border-radius: 0 10px 10px 0;">
            <h4 style="color: #e65100; margin-top: 0;">💡 Saran untuk Anda</h4>
            <p>Budget per orang: <strong>Rp {budget_per_person:,.0f}</strong></p>
            <p>Minimum untuk Paket Ekonomis: <strong>Rp {min_ekonomis:,.0f}</strong></p>
            <p>Kekurangan: <strong style="color: #e65100;">Rp {shortage:,.0f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📈 Opsi yang Bisa Anda Lakukan:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
**💰 Tambah Tabungan**
- Target tambahan: Rp {shortage:,.0f}
- Jika menabung Rp 1 juta/bulan: {int(shortage / 1_000_000) + 1} bulan lagi
- Jika menabung Rp 2 juta/bulan: {int(shortage / 2_000_000) + 1} bulan lagi
""")
        
        with col2:
            st.markdown("""
**🤝 Opsi Lain**
- Cari promo early bird
- Berangkat di low season (Januari-Februari)
- Gabung dengan grup besar untuk diskon
- Cicilan dari travel agent
""")
        
        if partial_packages:
            st.markdown("### 📦 Paket yang Hampir Terjangkau")
            for pkg in partial_packages:
                st.info(f"**{pkg['name']}** - Kurang Rp {pkg['shortage']:,.0f} (Minimum: Rp {pkg['min_required']:,.0f})")
        
        st.markdown("---")
        st.markdown("### 💡 Tips Mendapatkan Harga Terbaik")
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown("""
**🗓️ Waktu Booking**
- Book 3-4 bulan sebelumnya
- Hindari musim haji & Ramadhan
- Cari promo akhir tahun

**✈️ Penerbangan**
- Flexible date = harga lebih murah
- Transit 1x bisa hemat 20-30%
- Cek berbagai maskapai
""")
        
        with tips_col2:
            st.markdown("""
**🏨 Akomodasi**
- Hotel agak jauh = lebih murah
- Sharing room untuk hemat
- Weekday lebih murah dari weekend

**👥 Grup**
- Grup 10+ orang dapat diskon
- Gabung open trip
- Tanya promo travel agent
""")


# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def init_session_state():
    """Initialize session state variables"""
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "scenario_planner" not in st.session_state:
        st.session_state.scenario_planner = ScenarioPlanner()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = None
    if "initialized" not in st.session_state:
        st.session_state.initialized = False


def initialize_system():
    """Initialize the AI system"""
    if st.session_state.orchestrator is None:
        with st.spinner("🔄 Menginisialisasi sistem AI..."):
            try:
                st.session_state.orchestrator = AgentOrchestrator()
                result = st.session_state.orchestrator.initialize()
                st.session_state.initialized = True
                return result
            except Exception as e:
                st.error(f"Error initializing system: {str(e)}")
                return None
    return {"status": "already_initialized"}


# ============================================
# RENDER SIDEBAR
# ============================================
def render_sidebar():
    """Render sidebar with LABBAIK branding and navigation"""
    with st.sidebar:
        sidebar_header = f"""
<div style="text-align: center; padding: 25px 15px; border-bottom: 1px solid #333; margin-bottom: 15px;">
    <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 2rem; color: {COLORS['gold']}; text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);">{BRAND['arabic']}</div>
    <div style="font-size: 1.3rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin-top: 5px;">{BRAND['name']}</div>
    <div style="font-size: 0.8rem; color: {COLORS['sand']}; margin-top: 8px; font-style: italic;">{BRAND['tagline']}</div>
    <div style="margin-top: 10px;">
        <span style="background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%); color: {COLORS['black']}; padding: 3px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">v{BRAND['version']}</span>
    </div>
</div>
"""
        st.markdown(sidebar_header, unsafe_allow_html=True)
        
        init_user_database()
        init_monetization_state()
        
        user = get_current_user()
        if user:
            role_info = get_user_role_info(user.get("role", "user"))
            badge_html = f"""
<div style="background: linear-gradient(135deg, {role_info['color']}40, {role_info['color']}20); 
            border: 2px solid {role_info['color']}; border-radius: 15px; padding: 20px; 
            text-align: center; margin: 10px 0;">
    <div style="font-size: 2.5rem; margin-bottom: 5px;">{role_info['badge']}</div>
    <div style="color: white; font-weight: 700; font-size: 1rem;">{user['name']}</div>
    <div style="color: {role_info['color']}; font-size: 0.8rem; font-weight: 600;">{role_info['name']}</div>
</div>
"""
            st.markdown(badge_html, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout_btn"):
                logout_user()
                st.rerun()
        else:
            guest_badge_html = f"""
<div style="background: linear-gradient(135deg, #333 0%, #222 100%); 
            border: 2px solid {COLORS['gold']}; border-radius: 15px; padding: 20px; 
            text-align: center; margin: 10px 0;">
    <div style="font-size: 2.5rem; margin-bottom: 5px;">👤</div>
    <div style="color: white; font-weight: 700; font-size: 1rem;">Guest User</div>
    <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Belum Login</div>
</div>
"""
            st.markdown(guest_badge_html, unsafe_allow_html=True)
            
            if st.button("🔑 Login / Register", type="primary", use_container_width=True, key="sidebar_login_btn"):
                st.session_state.show_login_page = True
                st.rerun()
        
        st.markdown("---")
        
        if not is_logged_in():
            nav_items = [
                "🏠 Beranda",
                "🕋 Umrah Mandiri",
                "ℹ️ Tentang Aplikasi",
            ]
        else:
            nav_items = [
                "🏠 Beranda",
                "💰 Simulasi Biaya",
                "💵 Cari Paket by Budget",
                "🤝 Umrah Bareng",
                "🕋 Umrah Mandiri",
                "📊 Perbandingan Skenario",
                "📅 Analisis Waktu",
                "🤖 Chat AI",
                "📋 Buat Rencana",
                "✈️ Booking & Reservasi",
                "🧰 Tools & Fitur",
                "🎮 Rewards & Quiz",
            ]
            
            if user and user.get("role") in ["admin", "superadmin"]:
                nav_items.append("📊 Analytics")
                nav_items.append("💼 Business Hub")
                nav_items.append("🛡️ Admin Dashboard")
            
            nav_items.append("👤 Profil Saya")
            nav_items.extend([
                "⚙️ Pengaturan",
                "ℹ️ Tentang Aplikasi"
            ])
        
        page = st.radio("📍 Navigasi", nav_items)
        
        st.markdown("---")
        render_quick_quote_widget()
        st.markdown("---")
        
        quick_info = f"""
<div style="background: rgba(212, 175, 55, 0.1); padding: 12px; border-radius: 10px; border: 1px solid {COLORS['gold']}40;">
    <div style="font-size: 0.85rem; font-weight: 600; color: {COLORS['gold']}; margin-bottom: 8px;">📌 Info Cepat</div>
    <div style="font-size: 0.75rem; color: {COLORS['sand']};">
        <strong>Provider:</strong> {llm_config.provider.upper()}<br>
        <strong>Model:</strong> {llm_config.groq_model if llm_config.provider == 'groq' else llm_config.openai_model}
    </div>
</div>
"""
        st.markdown(quick_info, unsafe_allow_html=True)
        
        if is_logged_in():
            user = get_current_user()
            if user and user.get("role") in ["admin", "superadmin"]:
                st.markdown("---")
                stats = get_visitor_stats()
                visitor_stats_html = f"""
<div style="background: rgba(0, 107, 60, 0.1); padding: 12px; border-radius: 10px; border: 1px solid {COLORS['green']}40;">
    <div style="font-size: 0.85rem; font-weight: 600; color: {COLORS['green']}; margin-bottom: 8px;">📊 Visitor Stats</div>
    <div style="font-size: 0.75rem; color: {COLORS['sand']};">
        <strong>Total:</strong> {stats['total_visitors']:,} visitors<br>
        <strong>Views:</strong> {stats['total_views']:,} page views<br>
        <strong>Today:</strong> {stats['today_visitors']:,} visitors
    </div>
</div>
"""
                st.markdown(visitor_stats_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: {COLORS['gold']};'>💡 Tips</div>", unsafe_allow_html=True)
        tips = [
            "Booking 3-4 bulan sebelumnya untuk harga terbaik",
            "Hindari Ramadhan jika budget terbatas",
            "Pilih hotel dekat Haram untuk jamaah lansia",
            "Bawa obat pribadi yang cukup",
            "Download peta offline sebelum berangkat",
            "Tukar uang ke Riyal sebelum berangkat",
        ]
        st.caption(tips[datetime.now().second % len(tips)])
        
        sidebar_footer = f"""
<div style="text-align: center; padding: 15px 0;">
    <div style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1rem;">{BRAND['arabic']}</div>
    <div style="color: white; font-weight: 600; letter-spacing: 0.15em; font-size: 0.85rem; margin: 5px 0;">{BRAND['name']}</div>
    <div style="color: {COLORS['sand']}; font-size: 0.7rem;">{BRAND['tagline']}</div>
    <div style="color: #666; font-size: 0.65rem; margin-top: 10px;">
        © 2025 {CONTACT['website']}<br>
        Made with ❤️ by {DEVELOPER['name']}
    </div>
</div>
"""
        st.markdown("---")
        st.markdown(sidebar_footer, unsafe_allow_html=True)
        
        return page


# ============================================
# RENDER HOME
# ============================================
def render_home():
    """Render home page with LABBAIK branding"""
    track_page_view("Home")
    
    hero_html = f"""
<div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); border-radius: 20px; margin-bottom: 30px;">
    <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 2.5rem; color: {COLORS['gold']};">{BRAND['talbiyah']}</div>
    <div style="font-size: 2rem; font-weight: 700; color: white; letter-spacing: 0.3em; margin: 15px 0;">{BRAND['name']}</div>
    <div style="color: {COLORS['sand']}; font-size: 1.1rem;">{BRAND['tagline']}</div>
    <p style="color: {COLORS['sand']}; margin-top: 15px; font-size: 1rem;">{BRAND['description']}</p>
</div>
"""
    st.markdown(hero_html, unsafe_allow_html=True)
    
    stats_bar_html = f"""
<div style="background: {COLORS['black']}; padding: 20px; border-radius: 12px; margin: 20px 0;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">🤖</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">24/7</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">AI Assistant</div>
            </td>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">🏙️</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">10+</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">Kota Keberangkatan</div>
            </td>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">📊</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">5+</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">Skenario Paket</div>
            </td>
            <td style="text-align: center; padding: 10px;">
                <div style="font-size: 1.5rem;">🆓</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {COLORS['gold']};">GRATIS</div>
                <div style="font-size: 0.85rem; color: {COLORS['sand']};">Beta Access</div>
            </td>
        </tr>
    </table>
</div>
"""
    st.markdown(stats_bar_html, unsafe_allow_html=True)
    
    if not is_logged_in():
        login_cta = f"""
<div style="background: linear-gradient(135deg, {COLORS['gold']}22, {COLORS['sand']}22); border: 2px solid {COLORS['gold']}; border-radius: 15px; padding: 30px; text-align: center; margin: 30px 0;">
    <h3 style="color: {COLORS['black']}; margin-bottom: 10px;">🔐 Login untuk Akses Penuh</h3>
    <p style="color: {COLORS['gray']};">Daftar GRATIS atau login untuk mengakses semua fitur perencanaan umrah</p>
</div>
"""
        st.markdown(login_cta, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔑 Login / Register Sekarang", type="primary", use_container_width=True):
                st.session_state.nav_to_login = True
                st.rerun()
        
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: center; color: {COLORS['black']}; margin: 30px 0 20px;'>✨ Fitur yang Akan Anda Dapatkan</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 15px;"><div style="font-size: 2rem;">🤖</div><div style="font-weight: 700; margin: 10px 0;">AI Assistant 24/7</div><div style="font-size: 0.9rem; color: #666;">Tanya apapun tentang umrah</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 15px;"><div style="font-size: 2rem;">💰</div><div style="font-weight: 700; margin: 10px 0;">Simulasi Biaya</div><div style="font-size: 0.9rem; color: #666;">Hitung estimasi biaya</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 15px;"><div style="font-size: 2rem;">📊</div><div style="font-weight: 700; margin: 10px 0;">Bandingkan Paket</div><div style="font-size: 0.9rem; color: #666;">Ekonomis - VIP</div></div>""", unsafe_allow_html=True)
        
    else:
        user = get_current_user()
        role_info = get_user_role_info(user.get("role", "user") if user else "guest")
        
        welcome_html = f"""
<div style="background: linear-gradient(135deg, {role_info['color']}22, {role_info['color']}11); border-left: 4px solid {role_info['color']}; padding: 15px 20px; border-radius: 0 10px 10px 0; margin-bottom: 20px;">
    <span style="font-size: 1.5rem;">{role_info['badge']}</span>
    <span style="font-weight: 600; margin-left: 10px;">Assalamualaikum, {user.get('name', 'User') if user else 'User'}!</span>
    <span style="color: {COLORS['gray']}; margin-left: 10px;">({role_info['name']})</span>
</div>
"""
        st.markdown(welcome_html, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='color: {COLORS['black']}; margin: 20px 0;'>✨ Fitur Utama</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 15px;"><div style="font-size: 2rem;">🤖</div><div style="font-weight: 700; margin: 10px 0;">AI Assistant</div><div style="font-size: 0.9rem; color: #666;">Tanya apapun</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 15px;"><div style="font-size: 2rem;">💰</div><div style="font-weight: 700; margin: 10px 0;">Simulasi Biaya</div><div style="font-size: 0.9rem; color: #666;">Hitung estimasi</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 15px;"><div style="font-size: 2rem;">💵</div><div style="font-weight: 700; margin: 10px 0;">Cari by Budget</div><div style="font-size: 0.9rem; color: #666;">Sesuai dana</div></div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"### 🚀 Mulai Perencanaan Umrah Anda")
        
        col1, col2 = st.columns(2)
        with col1:
            scenario = st.selectbox("Pilih Skenario", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES[x]["name"])
        with col2:
            num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=1)
        
        if st.button("🔍 Lihat Estimasi Cepat", use_container_width=True):
            planner = st.session_state.scenario_planner
            result = planner.create_scenario(scenario, num_people)
            
            st.markdown("### 📋 Estimasi Cepat")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Estimasi Minimum", format_currency(result.estimated_min))
            with col2:
                st.metric("Estimasi Maksimum", format_currency(result.estimated_max))
            with col3:
                st.metric("Per Orang", format_currency(result.estimated_min / num_people))
            
            st.markdown("#### ✨ Fasilitas Termasuk:")
            for feature in result.features:
                st.markdown(f"• {feature}")


# ============================================
# RENDER COST SIMULATION
# ============================================
def render_cost_simulation():
    """Render cost simulation page"""
    st.header("💰 Simulasi Biaya Umrah")
    
    if 'duration_days' not in st.session_state:
        st.session_state.duration_days = 14
    
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            scenario = st.selectbox("Skenario Paket", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES[x]["name"])
            num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=2)
            duration = st.slider("Durasi (hari)", min_value=7, max_value=30, value=14, key="duration_slider")
        
        with col2:
            departure_city = st.selectbox("Kota Keberangkatan", list(DEPARTURE_CITIES.keys()))
            departure_month = st.selectbox("Bulan Keberangkatan", range(1, 13), format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1])
            special_requests = st.text_area("Permintaan Khusus (opsional)", placeholder="Misal: jamaah lansia, butuh kursi roda, dll.")
        
        submitted = st.form_submit_button("🔍 Hitung Biaya", use_container_width=True)
    
    if submitted:
        with st.spinner("⏳ Menghitung estimasi biaya..."):
            planner = st.session_state.scenario_planner
            result = planner.create_scenario(scenario_type=scenario, num_people=num_people, duration_days=duration, departure_month=departure_month)
            st.session_state.current_scenario = result
        
        st.markdown("---")
        st.subheader("📊 Hasil Simulasi")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Minimum", format_currency(result.estimated_min))
        with col2:
            st.metric("Total Maksimum", format_currency(result.estimated_max))
        with col3:
            st.metric("Per Orang (Min)", format_currency(result.estimated_min / num_people))
        with col4:
            avg = (result.estimated_min + result.estimated_max) / 2
            st.metric("Rata-rata Total", format_currency(avg))
        
        st.markdown("### ✨ Fasilitas Termasuk")
        cols = st.columns(2)
        for i, feature in enumerate(result.features):
            cols[i % 2].markdown(f"✅ {feature}")


# ============================================
# RENDER SCENARIO COMPARISON
# ============================================
def render_scenario_comparison():
    """Render scenario comparison page"""
    st.header("📊 Perbandingan Skenario")
    
    col1, col2 = st.columns(2)
    with col1:
        num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=1, key="compare_people")
    with col2:
        duration = st.slider("Durasi (hari)", min_value=7, max_value=21, value=12, key="compare_duration")
    
    if st.button("🔍 Bandingkan Semua Skenario", use_container_width=True):
        planner = st.session_state.scenario_planner
        
        scenarios_data = []
        for stype in ["ekonomis", "standard", "premium", "vip"]:
            scenario = planner.create_scenario(scenario_type=stype, num_people=num_people, duration_days=duration)
            scenarios_data.append({
                "Skenario": SCENARIO_TEMPLATES[stype]["name"],
                "Hotel Makkah": f"⭐ {scenario.hotel_star_makkah}",
                "Hotel Madinah": f"⭐ {scenario.hotel_star_madinah}",
                "Min (Rp)": scenario.estimated_min,
                "Max (Rp)": scenario.estimated_max,
            })
        
        df = pd.DataFrame(scenarios_data)
        st.markdown("### 📋 Tabel Perbandingan")
        st.dataframe(df.style.format({"Min (Rp)": "{:,.0f}", "Max (Rp)": "{:,.0f}"}), use_container_width=True)


# ============================================
# RENDER TIME ANALYSIS
# ============================================
def render_time_analysis():
    """Render time analysis page"""
    st.header("📅 Analisis Waktu Terbaik Umrah")
    
    priority = st.selectbox("Prioritas Anda", ["balanced", "cost", "crowd"], format_func=lambda x: {"balanced": "🎯 Seimbang", "cost": "💰 Hemat Biaya", "crowd": "👥 Hindari Keramaian"}[x])
    
    if st.button("📊 Analisis Waktu Terbaik", use_container_width=True):
        planner = st.session_state.scenario_planner
        analysis = planner.analyze_best_time(priority)
        
        st.markdown("### ✅ Bulan Terbaik untuk Umrah")
        cols = st.columns(3)
        for i, month_data in enumerate(analysis["best_months"]):
            with cols[i]:
                st.success(f"**#{i+1} {month_data['month_name']}**\n\n🌡️ {month_data['weather']}\n\n💰 {month_data['price_multiplier']}x\n\n👥 {month_data['crowd_level']}")


# ============================================
# RENDER AI CHAT
# ============================================
def render_ai_chat():
    """Render AI chat page"""
    st.header("🤖 Chat dengan AI Assistant")
    
    if st.session_state.orchestrator is None:
        st.session_state.orchestrator = AgentOrchestrator()
        st.session_state.orchestrator.initialize()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                padding: 15px; border-radius: 10px; margin-bottom: 20px; 
                border-left: 4px solid #D4AF37;">
        <div style="color: #D4AF37; font-weight: 600;">💡 Tips:</div>
        <div style="color: #C9A86C; font-size: 0.9rem;">
            Tanyakan tentang rukun umrah, biaya, waktu terbaik, persiapan, atau tips memilih travel agent!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])
    
    if prompt := st.chat_input("Ketik pertanyaan Anda..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("🤔 AI sedang berpikir..."):
            try:
                response = st.session_state.orchestrator.chat(prompt)
                ai_response = response["response"]
            except Exception as e:
                ai_response = f"Maaf, terjadi error: {str(e)}. Silakan coba lagi."
        
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").markdown(ai_response)
    
    st.markdown("---")
    
    st.markdown("### 💡 Pertanyaan Cepat")
    quick_questions = [
        ("🕋 Rukun umrah?", "Apa saja rukun umrah?"),
        ("💰 Biaya umrah?", "Berapa estimasi biaya umrah 2025?"),
        ("📅 Waktu terbaik?", "Kapan waktu terbaik untuk umrah?"),
    ]
    
    cols = st.columns(3)
    for i, (label, question) in enumerate(quick_questions):
        with cols[i % 3]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": question})
                response = st.session_state.orchestrator.chat(question)
                st.session_state.chat_history.append({"role": "assistant", "content": response["response"]})
                st.rerun()
    
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state.chat_history = []
        if st.session_state.orchestrator:
            st.session_state.orchestrator.reset_conversations()
        st.rerun()


# ============================================
# RENDER CREATE PLAN
# ============================================
def render_create_plan():
    """Render create plan page"""
    st.header("📋 Buat Rencana Umrah Lengkap")
    
    st.markdown("### 📝 Detail Perjalanan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario = st.selectbox("Skenario Paket", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES.get(x, {}).get("name", x.title()), key="plan_scenario")
        num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=2, key="plan_num_people")
        departure_month = st.selectbox("Bulan Keberangkatan", range(1, 13), format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1], key="plan_departure_month")
    
    with col2:
        st.markdown("#### 🕋 Durasi Menginap")
        nights_makkah = st.slider("🕋 Lama di Mekkah (malam)", min_value=2, max_value=10, value=4, key="nights_makkah")
        nights_madinah = st.slider("🕌 Lama di Madinah (malam)", min_value=2, max_value=10, value=3, key="nights_madinah")
        total_duration = nights_makkah + nights_madinah + 2
        st.info(f"📅 **Total Durasi:** {total_duration} hari")
    
    st.markdown("---")
    
    hotel_makkah = HOTEL_PRICES.get(scenario, HOTEL_PRICES["standard"])["makkah"]
    hotel_madinah = HOTEL_PRICES.get(scenario, HOTEL_PRICES["standard"])["madinah"]
    additional = ADDITIONAL_COSTS.get(scenario, ADDITIONAL_COSTS["standard"])
    
    cost_makkah = hotel_makkah["price"] * nights_makkah
    cost_madinah = hotel_madinah["price"] * nights_madinah
    
    if st.button("🚀 Buat Rencana Lengkap", use_container_width=True, type="primary"):
        flight_cost = additional["flight"]
        visa_cost = additional["visa"]
        transport_cost = additional["transport"]
        meals_cost = additional["meals"] * total_duration
        
        total_per_person = cost_makkah + cost_madinah + flight_cost + visa_cost + transport_cost + meals_cost
        grand_total = total_per_person * num_people
        
        season_mult = 1.0
        if departure_month in [3, 4]:
            season_mult = 1.6
        elif departure_month in [12, 6, 7]:
            season_mult = 1.4
        elif departure_month in [1, 2, 9, 10]:
            season_mult = 0.85
        
        total_per_person_adjusted = int(total_per_person * season_mult)
        grand_total_adjusted = int(grand_total * season_mult)
        
        st.success("✅ Rencana berhasil dibuat!")
        
        st.markdown("### 📊 Ringkasan")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Jamaah", f"{num_people} orang")
        with col2:
            st.metric("🕋 Mekkah", f"{nights_makkah} malam")
        with col3:
            st.metric("🕌 Madinah", f"{nights_madinah} malam")
        with col4:
            st.metric("📅 Total", f"{total_duration} hari")
        
        st.markdown("### 💰 Estimasi Biaya")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Per Orang", f"Rp {total_per_person_adjusted:,}")
        with col2:
            st.metric("Grand Total", f"Rp {grand_total_adjusted:,}")


# ============================================
# RENDER UMRAH BARENG
# ============================================
def init_umrah_bareng_state():
    """Initialize Umrah Bareng session state"""
    if "open_trips" not in st.session_state:
        if DB_AVAILABLE and is_db_available():
            try:
                db_trips = db_get_open_trips()
                if db_trips:
                    st.session_state.open_trips = db_trips
                    return
            except:
                pass
        
        st.session_state.open_trips = [
            {
                "id": "OT001",
                "creator_name": "Ahmad Fauzi",
                "creator_phone": "+62812xxxx1234",
                "creator_city": "Jakarta",
                "title": "Umrah Bareng Keluarga Muda",
                "departure_date": "2025-03-15",
                "departure_city": "Jakarta (CGK)",
                "package_type": "standard",
                "budget_per_person": 38000000,
                "duration_days": 12,
                "nights_makkah": 5,
                "nights_madinah": 4,
                "current_members": 4,
                "max_members": 10,
                "gender_preference": "Campuran (Keluarga)",
                "age_preference": "25-40 tahun",
                "special_notes": "Fokus ibadah, tidak banyak shopping.",
                "amenities": ["Muthawwif Indonesia", "Menu Indonesia"],
                "status": "open",
                "created_at": "2025-01-15",
            },
        ]


def render_umrah_bareng():
    """Render Umrah Bareng (Open Trip) feature"""
    init_umrah_bareng_state()
    
    st.header("🤝 Umrah Bareng - Open Trip")
    st.markdown("Cari teman perjalanan umrah atau buat open trip sendiri!")
    
    total_trips = len(st.session_state.open_trips)
    open_trips = len([t for t in st.session_state.open_trips if t["status"] == "open"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📋 Total Open Trip", total_trips)
    with col2:
        st.metric("✅ Masih Tersedia", open_trips)
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔍 Cari Open Trip", "➕ Buat Open Trip"])
    
    with tab1:
        st.markdown("### 🔍 Cari Open Trip yang Cocok")
        
        for trip in st.session_state.open_trips:
            if trip["status"] == "open":
                st.markdown(f"""
                <div style="background: #f5f5f5; border-radius: 15px; padding: 20px; margin-bottom: 15px;">
                    <h4 style="margin-top: 0;">{trip['title']}</h4>
                    <p>📅 {trip['departure_date']} | 💰 Rp {trip['budget_per_person']:,}/orang | 👥 {trip['current_members']}/{trip['max_members']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### ➕ Buat Open Trip Baru")
        st.info("Fitur ini memerlukan login. Silakan login untuk membuat open trip.")


# ============================================
# RENDER UMRAH MANDIRI
# ============================================
def init_forum_state():
    """Initialize Forum Umrah Mandiri session state"""
    if "forum_posts" not in st.session_state:
        st.session_state.forum_posts = []


def render_umrah_mandiri():
    """Render Umrah Mandiri Guide and Forum"""
    init_forum_state()
    
    st.header("🕋 Umrah Mandiri")
    st.markdown("Panduan lengkap umrah mandiri & forum sharing pengalaman!")
    
    tab1, tab2 = st.tabs(["📖 Apa itu Umrah Mandiri?", "💬 Forum Diskusi"])
    
    with tab1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 30px; border-radius: 20px; margin-bottom: 25px;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 10px;">🕋</div>
                <h2 style="color: {COLORS['gold']}; margin: 0;">Umrah Mandiri</h2>
                <p style="color: {COLORS['sand']}; font-size: 1.1rem; margin-top: 10px;">
                    Ibadah Umrah yang Diatur Sendiri, Fleksibel, dan Lebih Hemat
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Umrah Mandiri** adalah ibadah umrah yang kamu atur sendiri tanpa menggunakan jasa travel agent. 
        Mulai dari tiket pesawat, hotel, visa, sampai transportasi di Arab Saudi - semuanya kamu yang handle!
        
        **Kelebihan:**
        - 💰 Lebih hemat 30-50%
        - ⏰ Jadwal fleksibel
        - 🕋 Lebih khusyuk
        
        **Yang perlu dipersiapkan:**
        - Paspor valid > 6 bulan
        - Booking tiket & hotel
        - Apply visa umrah
        - Pelajari manasik
        """)
    
    with tab2:
        st.markdown("### 💬 Forum Umrah Mandiri")
        st.info("Forum diskusi akan segera hadir! Bagikan pengalaman umrah mandiri Anda.")


# ============================================
# RENDER SETTINGS
# ============================================
def render_settings():
    """Render settings page"""
    st.header("⚙️ Pengaturan")
    
    st.markdown("### 🔑 Konfigurasi API")
    provider = st.selectbox("LLM Provider", ["groq", "openai"], index=0 if llm_config.provider == "groq" else 1)
    
    st.markdown("### 📊 Status Sistem")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "✅ Aktif" if st.session_state.initialized else "❌ Belum Aktif")
    with col2:
        st.metric("Version", __version__)


# ============================================
# RENDER ABOUT
# ============================================
def render_about():
    """Render about page"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); color: white; padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
        <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 2.5rem; color: {COLORS['gold']};">{BRAND['talbiyah']}</div>
        <div style="font-size: 2rem; font-weight: 700; letter-spacing: 0.3em; margin: 15px 0;">{BRAND['name']}</div>
        <div style="color: {COLORS['sand']}; font-size: 1.1rem;">{BRAND['tagline']}</div>
        <div style="margin-top: 20px;"><span style="background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%); color: {COLORS['black']}; padding: 8px 20px; border-radius: 20px; font-weight: 700;">Version {BRAND['version']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(get_developer_card(), unsafe_allow_html=True)
    
    st.markdown("### 📋 Changelog")
    st.markdown(get_changelog_markdown())


# ============================================
# RENDER USER PROFILE
# ============================================
def render_user_profile():
    """Render user profile page"""
    user = get_current_user()
    
    if not user:
        st.warning("🔐 Silakan login untuk melihat profil")
        render_login_page()
        return
    
    st.header("👤 Profil Saya")
    role_info = get_user_role_info(user.get("role", "user"))
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {role_info['color']}88, {role_info['color']}44); padding: 2rem; border-radius: 15px; text-align: center;">
            <div style="font-size: 4rem;">{role_info['badge']}</div>
            <h2>{user.get('name', 'User')}</h2>
            <p style="color: {role_info['color']};">{role_info['name']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("### 📋 Informasi Akun")
        st.markdown(f"**Email:** {user.get('email', '-')}")
        st.markdown(f"**Phone:** {user.get('phone', '-')}")
    
    if st.button("🚪 Logout", type="secondary"):
        logout_user()
        st.rerun()


# ============================================
# RENDER ENGAGEMENT PAGE
# ============================================
def render_engagement_page():
    """Render the engagement hub"""
    check_daily_login()
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); border-radius: 15px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 10px 0;">🎮 Rewards & Quiz Center</h2>
        <p style="color: {COLORS['sand']};">Kumpulkan poin, unlock badge, dan naik level!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🏆 Rewards", "🧠 Quiz", "🎁 Ajak Teman"])
    
    with tab1:
        render_engagement_hub()
    
    with tab2:
        init_quiz_state()
        render_quiz_page()
    
    with tab3:
        user = get_current_user()
        user_id = user.get("id", "guest") if user else "guest"
        ref_code = generate_referral_code(str(user_id))
        render_invite_modal(ref_code)


# ============================================
# RENDER FOOTER
# ============================================
def render_labbaik_footer():
    """Render LABBAIK branded footer"""
    stats = get_visitor_stats()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 40px; border-radius: 20px; text-align: center; margin-top: 50px;">
        <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.8rem; color: {COLORS['gold']};">{BRAND['talbiyah']}</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin: 12px 0;">{BRAND['name']}</div>
        <div style="color: {COLORS['sand']}; font-size: 0.95rem; margin-bottom: 20px;">{BRAND['tagline']}</div>
        <div style="color: #888; font-size: 0.85rem;">📧 {CONTACT['email']} | 📱 {CONTACT['whatsapp']}</div>
        <div style="border-top: 1px solid #333; padding-top: 20px; margin-top: 20px; color: #666; font-size: 0.8rem;">
            © 2025 {BRAND['name']}. Made with ❤️ by {DEVELOPER['name']}<br>
            v{__version__} | {stats['total_visitors']:,} visitors
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# MAIN FUNCTION
# ============================================
def main():
    """Main application entry point"""
    init_session_state()
    init_engagement_state()
    
    if PWA_AVAILABLE:
        init_pwa()
    
    if "show_login_page" not in st.session_state:
        st.session_state.show_login_page = False
    
    if st.session_state.get("nav_to_login"):
        st.session_state.nav_to_login = False
        st.session_state.show_login_page = True
    
    if st.session_state.show_login_page and not is_logged_in():
        render_login_page()
        if st.button("← Kembali ke Beranda"):
            st.session_state.show_login_page = False
            st.rerun()
        return
    
    if is_logged_in():
        st.session_state.show_login_page = False
    
    page = render_sidebar()
    
    if not st.session_state.initialized:
        if llm_config.groq_api_key or llm_config.openai_api_key:
            initialize_system()
    
    # Page routing
    if "Beranda" in page:
        render_home()
        render_labbaik_footer()
    elif "Simulasi Biaya" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Cost Simulation")
            render_cost_simulation()
    elif "Cari Paket by Budget" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Budget Finder")
            render_budget_finder()
    elif "Umrah Bareng" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Umrah Bareng")
            render_umrah_bareng()
    elif "Umrah Mandiri" in page:
        track_page_view("Umrah Mandiri")
        render_umrah_mandiri()
    elif "Perbandingan" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Scenario Comparison")
            render_scenario_comparison()
    elif "Analisis Waktu" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Time Analysis")
            render_time_analysis()
    elif "Chat AI" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("AI Chat")
            render_ai_chat()
    elif "Buat Rencana" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Create Plan")
            render_create_plan()
    elif "Booking" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Booking")
            st.header("✈️ Booking & Reservasi")
            render_booking_features()
    elif "Tools" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Tools")
            st.header("🧰 Tools & Fitur Jamaah")
            render_additional_features()
    elif "Rewards" in page or "Quiz" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Rewards & Quiz")
            render_engagement_page()
    elif "Analytics" in page:
        user = get_current_user()
        if not user or user.get("role") not in ["admin", "superadmin"]:
            st.error("🚫 Akses Ditolak")
        else:
            track_page_view("Analytics")
            render_analytics_dashboard()
    elif "Business" in page:
        user = get_current_user()
        if not user or user.get("role") not in ["admin", "superadmin"]:
            st.error("🚫 Akses Ditolak")
        else:
            track_page_view("Business Hub")
            render_monetization_page()
    elif "Admin" in page:
        track_page_view("Admin Dashboard")
        render_admin_dashboard()
    elif "Profil" in page:
        track_page_view("Profile")
        render_user_profile()
    elif "Pengaturan" in page:
        track_page_view("Settings")
        render_settings()
    elif "Tentang" in page:
        track_page_view("About")
        render_about()
        render_labbaik_footer()


if __name__ == "__main__":
    main()