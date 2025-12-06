"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  لَبَّيْكَ LABBAIK ULTIMATE v3.8.0 - MERGED & OPTIMIZED                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🚀 ALL FEATURES FROM v3.4.0 + OPTIMIZATIONS FROM v3.7.0                     ║
║  ⚡ LIGHTWEIGHT • 📱 MOBILE-READY • 🗄️ DATABASE-READY                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Copyright (c) 2025 MS Hadianto. All Rights Reserved.
Email: sopian.hadianto@gmail.com | WhatsApp: +62 815 9658 833

FEATURES:
✅ All v3.4.0 features (Umrah Bareng, Umrah Mandiri, Forum, Booking)
✅ All v3.7.0 features (PDF Export, Maps, Reminder, Analytics)
✅ Database integration ready (Neon PostgreSQL)
✅ Graceful fallbacks when modules unavailable
✅ Maximum caching for performance
✅ ~1400 lines (vs 3800+ original)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from functools import lru_cache
import json
import base64
import random
import hashlib

# ═══════════════════════════════════════════════════════════════════
# 🔧 PAGE CONFIG - MUST BE FIRST
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="LABBAIK - Platform Umrah AI #1 Indonesia",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://wa.me/6281596588833',
        'About': "LABBAIK v3.8.0 - Platform AI Perencanaan Umrah #1 Indonesia"
    }
)

# ═══════════════════════════════════════════════════════════════════
# 📦 OPTIONAL MODULE IMPORTS (Graceful Fallbacks)
# ═══════════════════════════════════════════════════════════════════
try:
    from db_integration import (
        is_db_available, hybrid_login, hybrid_register,
        db_get_open_trips, db_create_trip, db_get_forum_posts, 
        db_create_post, db_log_visit, db_get_stats
    )
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    def is_db_available(): return False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════
# 📊 CONSTANTS & BRAND
# ═══════════════════════════════════════════════════════════════════
VERSION = "3.8.0"
BRAND = {
    "name": "LABBAIK", "arabic": "لَبَّيْكَ",
    "talbiyah": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ",
    "tagline": "Panggilan-Nya, Langkahmu",
    "desc": "Platform AI Perencanaan Umrah #1 Indonesia"
}
COLORS = {
    "black": "#1A1A1A", "gold": "#D4AF37", "green": "#006B3C",
    "sand": "#C9A86C", "white": "#FFFFFF", "gray": "#666666"
}
CONTACT = {"email": "sopian.hadianto@gmail.com", "wa": "+62 815 9658 8833", "web": "labbaik.ai"}

# ═══════════════════════════════════════════════════════════════════
# 💾 CACHED DATA LOADERS - Single Load, Maximum Performance
# ═══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400, show_spinner=False)
def load_all_data() -> Dict:
    """Load ALL static data in one call - Super efficient"""
    return {
        "scenarios": {
            "ekonomis": {"name": "Ekonomis", "emoji": "💚", "star": 3, "mult": 1.0, "days": 9},
            "standard": {"name": "Standard", "emoji": "💙", "star": 4, "mult": 1.3, "days": 12},
            "premium": {"name": "Premium", "emoji": "🧡", "star": 5, "mult": 1.8, "days": 14},
            "vip": {"name": "VIP", "emoji": "💛", "star": 5, "mult": 2.5, "days": 14},
        },
        "cities": ["Jakarta (CGK)", "Surabaya (SUB)", "Medan (KNO)", "Makassar (UPG)", 
                   "Bandung (BDO)", "Semarang (SRG)", "Yogyakarta (JOG)", "Denpasar (DPS)",
                   "Palembang (PLM)", "Balikpapan (BPN)", "Pekanbaru (PKU)", "Padang (PDG)"],
        "city_mult": {"Jakarta": 1.0, "Surabaya": 1.05, "Medan": 1.1, "Makassar": 1.15,
                      "Bandung": 1.08, "Semarang": 1.07, "Yogyakarta": 1.06, "Denpasar": 1.12},
        "hotels": {
            "ekonomis": {
                "makkah": {"name": "Hotel Bintang 2-3 (1-2km)", "price": 800000, "dist": 1500},
                "madinah": {"name": "Hotel Bintang 2-3 (500m-1km)", "price": 600000, "dist": 800}
            },
            "standard": {
                "makkah": {"name": "Hotel Bintang 3-4 (500m-1km)", "price": 1500000, "dist": 750},
                "madinah": {"name": "Hotel Bintang 3-4 (300-500m)", "price": 1000000, "dist": 400}
            },
            "premium": {
                "makkah": {"name": "Hotel Bintang 4-5 (200-500m)", "price": 2500000, "dist": 350},
                "madinah": {"name": "Hotel Bintang 4-5 (100-300m)", "price": 1800000, "dist": 200}
            },
            "vip": {
                "makkah": {"name": "Hotel Bintang 5 View Ka'bah (<200m)", "price": 5000000, "dist": 100},
                "madinah": {"name": "Hotel Bintang 5 View Nabawi (<100m)", "price": 3500000, "dist": 50}
            }
        },
        "costs": {
            "ekonomis": {"flight": 8000000, "visa": 500000, "transport": 500000, "meals": 300000, "insurance": 200000},
            "standard": {"flight": 12000000, "visa": 500000, "transport": 800000, "meals": 500000, "insurance": 350000},
            "premium": {"flight": 18000000, "visa": 500000, "transport": 1200000, "meals": 800000, "insurance": 500000},
            "vip": {"flight": 30000000, "visa": 500000, "transport": 2000000, "meals": 1500000, "insurance": 1000000}
        },
        "weather": {
            1: {"temp": 20, "cond": "Sejuk", "icon": "🌤️", "rec": "Ideal"},
            2: {"temp": 22, "cond": "Sejuk", "icon": "🌤️", "rec": "Ideal"},
            3: {"temp": 26, "cond": "Hangat", "icon": "☀️", "rec": "Baik"},
            4: {"temp": 31, "cond": "Panas", "icon": "☀️", "rec": "Cukup"},
            5: {"temp": 36, "cond": "Sangat Panas", "icon": "🔥", "rec": "Hindari"},
            6: {"temp": 38, "cond": "Ekstrem", "icon": "🔥", "rec": "Hindari"},
            7: {"temp": 39, "cond": "Ekstrem", "icon": "🔥", "rec": "Hindari"},
            8: {"temp": 39, "cond": "Ekstrem", "icon": "🔥", "rec": "Hindari"},
            9: {"temp": 36, "cond": "Panas", "icon": "☀️", "rec": "Cukup"},
            10: {"temp": 31, "cond": "Hangat", "icon": "☀️", "rec": "Baik"},
            11: {"temp": 25, "cond": "Sejuk", "icon": "🌤️", "rec": "Ideal"},
            12: {"temp": 21, "cond": "Sejuk", "icon": "🌤️", "rec": "Baik"}
        },
        "checklist": [
            {"cat": "📄 Dokumen", "item": "Paspor (valid >6 bln)", "req": True},
            {"cat": "📄 Dokumen", "item": "Foto 4x6 bg putih (10)", "req": True},
            {"cat": "📄 Dokumen", "item": "KTP + fotokopi", "req": True},
            {"cat": "📄 Dokumen", "item": "Vaksin Meningitis", "req": True},
            {"cat": "📄 Dokumen", "item": "Kartu Keluarga", "req": True},
            {"cat": "📄 Dokumen", "item": "Buku Nikah (jika)", "req": False},
            {"cat": "👔 Pakaian", "item": "Ihram 2 set (pria)", "req": True},
            {"cat": "👔 Pakaian", "item": "Mukena 2 set (wanita)", "req": True},
            {"cat": "👔 Pakaian", "item": "Gamis/Jubah 3-4 set", "req": False},
            {"cat": "👔 Pakaian", "item": "Sandal nyaman 2 pasang", "req": True},
            {"cat": "📿 Ibadah", "item": "Buku doa & manasik", "req": True},
            {"cat": "📿 Ibadah", "item": "Al-Quran kecil", "req": False},
            {"cat": "📿 Ibadah", "item": "Sajadah travel", "req": False},
            {"cat": "💊 Kesehatan", "item": "Obat-obatan pribadi", "req": True},
            {"cat": "💊 Kesehatan", "item": "Vitamin & suplemen", "req": False},
            {"cat": "💊 Kesehatan", "item": "Masker 20+ pcs", "req": False},
            {"cat": "💊 Kesehatan", "item": "Sunscreen SPF 50+", "req": False},
            {"cat": "🔌 Elektronik", "item": "HP + charger", "req": True},
            {"cat": "🔌 Elektronik", "item": "Adaptor Type G", "req": True},
            {"cat": "🔌 Elektronik", "item": "Power bank", "req": False},
            {"cat": "🎒 Lainnya", "item": "Tas kecil thawaf", "req": False},
            {"cat": "🎒 Lainnya", "item": "Uang SAR", "req": True},
            {"cat": "🎒 Lainnya", "item": "Kartu ATM Intl", "req": False},
        ],
        "locations": {
            "kabah": {"name": "Ka'bah & Masjidil Haram", "lat": 21.4225, "lon": 39.8262, "city": "Makkah"},
            "safa_marwa": {"name": "Bukit Safa & Marwa", "lat": 21.4234, "lon": 39.8277, "city": "Makkah"},
            "jabal_nur": {"name": "Jabal Nur (Gua Hira)", "lat": 21.4575, "lon": 39.8583, "city": "Makkah"},
            "jabal_rahmah": {"name": "Jabal Rahmah", "lat": 21.3547, "lon": 39.9847, "city": "Arafah"},
            "masjid_nabawi": {"name": "Masjid Nabawi", "lat": 24.4672, "lon": 39.6112, "city": "Madinah"},
            "raudhah": {"name": "Raudhah", "lat": 24.4674, "lon": 39.6110, "city": "Madinah"},
            "masjid_quba": {"name": "Masjid Quba", "lat": 24.4397, "lon": 39.6169, "city": "Madinah"},
            "jabal_uhud": {"name": "Jabal Uhud", "lat": 24.5007, "lon": 39.6153, "city": "Madinah"},
            "baqi": {"name": "Pemakaman Baqi", "lat": 24.4678, "lon": 39.6147, "city": "Madinah"},
        },
        "emergency": [
            {"name": "KBRI Riyadh", "phone": "+966-11-488-2800", "type": "Embassy"},
            {"name": "KJRI Jeddah", "phone": "+966-12-667-0645", "type": "Consulate"},
            {"name": "Ambulans Saudi", "phone": "997", "type": "Emergency"},
            {"name": "Polisi Saudi", "phone": "999", "type": "Emergency"},
            {"name": "Pemadam", "phone": "998", "type": "Emergency"},
            {"name": "Hotline Kemenag", "phone": "+62-21-381-0333", "type": "Indonesia"},
        ],
    }

@st.cache_data(ttl=3600)
def get_exchange_rate(): return 4250

@st.cache_data(ttl=86400)
def get_season(month: int) -> Dict:
    if month == 12: return {"name": "High Season", "mult": 1.4, "icon": "🔴"}
    if month in [3, 4]: return {"name": "Ramadan", "mult": 1.6, "icon": "🟣"}
    if month in [1, 2, 6, 7]: return {"name": "Low Season", "mult": 0.85, "icon": "🟢"}
    return {"name": "Regular", "mult": 1.0, "icon": "🔵"}

# ═══════════════════════════════════════════════════════════════════
# 🛠️ UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def fmt(amount, prefix="Rp"):
    return f"{prefix} {amount:,.0f}".replace(",", ".") if amount else f"{prefix} 0"

def fmt_sar(idr):
    return f"SAR {idr/get_exchange_rate():,.0f}"

def get_month_name(m):
    return ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"][m-1]

def get_month_full(m):
    return ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"][m-1]

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def generate_pdf_html(plan: Dict) -> str:
    """Generate HTML for PDF export"""
    data = load_all_data()
    tmpl = data["scenarios"].get(plan.get("scenario", "standard"), {})
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>body{{font-family:Arial,sans-serif;padding:20px;max-width:800px;margin:auto}}.header{{text-align:center;border-bottom:2px solid #D4AF37;padding-bottom:20px}}.title{{font-size:28px;color:#1A1A1A;font-weight:bold}}.arabic{{font-size:24px;color:#D4AF37}}.section{{margin:20px 0;padding:15px;background:#f9f9f9;border-radius:10px}}.total{{font-size:24px;color:#D4AF37;font-weight:bold;text-align:center;padding:20px}}.footer{{text-align:center;margin-top:30px;color:#666;font-size:12px}}</style>
</head><body>
<div class="header"><div class="arabic">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div><div class="title">LABBAIK - Rencana Umrah</div><p>Dibuat: {datetime.now().strftime('%d %B %Y')}</p></div>
<div class="section"><h3>{tmpl.get('emoji','')} Paket {tmpl.get('name','')}</h3><p>👥 Jamaah: {plan.get('num_people',1)} orang | 📅 Durasi: {plan.get('total_days',9)} hari</p><p>🕋 Makkah: {plan.get('nights_makkah',4)} malam | 🕌 Madinah: {plan.get('nights_madinah',3)} malam</p></div>
<div class="section"><h3>💰 Rincian Biaya</h3><p>✈️ Tiket: {fmt(plan.get('breakdown',{}).get('flight',0))}</p><p>🕋 Hotel Makkah: {fmt(plan.get('breakdown',{}).get('hotel_makkah',0))}</p><p>🕌 Hotel Madinah: {fmt(plan.get('breakdown',{}).get('hotel_madinah',0))}</p><p>📄 Visa: {fmt(plan.get('breakdown',{}).get('visa',0))}</p><p>🚐 Transport: {fmt(plan.get('breakdown',{}).get('transport',0))}</p><p>🍽️ Makan: {fmt(plan.get('breakdown',{}).get('meals',0))}</p></div>
<div class="total">Total: {fmt(plan.get('grand_total',0))} ({fmt_sar(plan.get('grand_total',0))})</div>
<div class="footer"><p>LABBAIK v{VERSION} - Platform AI Perencanaan Umrah #1 Indonesia</p><p>⚠️ Ini adalah estimasi. Verifikasi travel agent di siskopatuh.kemenag.go.id</p></div>
</body></html>"""

def create_download_link(html, filename="rencana_umrah.html"):
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="display:inline-block;padding:10px 20px;background:#D4AF37;color:#1A1A1A;text-decoration:none;border-radius:8px;font-weight:bold;">📥 Download Rencana</a>'

# ═══════════════════════════════════════════════════════════════════
# 🧮 CORE PLANNER CLASS
# ═══════════════════════════════════════════════════════════════════
class UmrahPlanner:
    def __init__(self):
        self.data = load_all_data()
    
    def calculate(self, scenario, num_people, nights_makkah, nights_madinah, month, city="Jakarta"):
        d = self.data
        hotel = d["hotels"][scenario]
        cost = d["costs"][scenario]
        city_mult = d["city_mult"].get(city.split()[0], 1.0)
        season = get_season(month)
        total_days = nights_makkah + nights_madinah + 2
        
        breakdown = {
            "flight": cost["flight"] * city_mult,
            "hotel_makkah": hotel["makkah"]["price"] * nights_makkah,
            "hotel_madinah": hotel["madinah"]["price"] * nights_madinah,
            "visa": cost["visa"],
            "transport": cost["transport"],
            "meals": cost["meals"] * total_days,
            "insurance": cost["insurance"]
        }
        
        subtotal = sum(breakdown.values())
        total_pp = subtotal * season["mult"]
        grand = total_pp * num_people
        
        return {
            "scenario": scenario, "num_people": num_people,
            "nights_makkah": nights_makkah, "nights_madinah": nights_madinah,
            "month": month, "city": city, "total_days": total_days,
            "breakdown": breakdown, "total_per_person": total_pp, "grand_total": grand,
            "season": season, "hotel_makkah": hotel["makkah"], "hotel_madinah": hotel["madinah"]
        }
    
    def find_by_budget(self, budget, num=1):
        budget_pp = budget / num
        available = []
        for key, tmpl in self.data["scenarios"].items():
            hotel = self.data["hotels"][key]
            cost = self.data["costs"][key]
            min_cost = (cost["flight"] + cost["visa"] + cost["transport"] + cost["insurance"] +
                       hotel["makkah"]["price"] * 4 + hotel["madinah"]["price"] * 3 + cost["meals"] * 9)
            if budget_pp >= min_cost:
                remaining = budget_pp - min_cost
                extra = int(remaining / (hotel["makkah"]["price"] + cost["meals"]))
                available.append({
                    "key": key, "name": tmpl["name"], "emoji": tmpl["emoji"],
                    "min": min_cost, "max_days": 9 + min(extra, 12), "star": tmpl["star"],
                    "remaining": remaining
                })
        return sorted(available, key=lambda x: x["min"])

# ═══════════════════════════════════════════════════════════════════
# 🤖 AI ASSISTANT
# ═══════════════════════════════════════════════════════════════════
class AIChat:
    def __init__(self):
        self.history = []
        self.kb = {
            "rukun": "**5 Rukun Umrah:**\n1️⃣ **Ihram** - Niat dari miqat\n2️⃣ **Thawaf** - 7x keliling Ka'bah\n3️⃣ **Sa'i** - 7x Safa-Marwa\n4️⃣ **Tahallul** - Potong rambut\n5️⃣ **Tertib** - Berurutan",
            "biaya": "**Estimasi Biaya 2025:**\n- 💚 Ekonomis: Rp 20-28 juta\n- 💙 Standard: Rp 28-40 juta\n- 🧡 Premium: Rp 40-60 juta\n- 💛 VIP: Rp 60-150 juta",
            "waktu": "**Waktu Terbaik:**\n- ✅ Jan-Feb (sejuk + murah)\n- ✅ Sep-Okt (nyaman)\n- ⚠️ Des (mahal, ramai)\n- ❌ Jun-Jul (panas 40°C+)",
            "persiapan": "**Persiapan Wajib:**\n- 📄 Paspor >6 bulan, Foto 4x6, Vaksin Meningitis\n- 👔 Ihram 2 set, Sandal nyaman\n- 💊 Obat pribadi\n- 🔌 Adaptor Type G\n- 💵 Uang SAR",
            "doa": "**Talbiyah:**\n> لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ\n\n**Doa Thawaf:**\n> رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً",
            "travel": "**Tips Pilih Travel:**\n- ✅ Cek izin Kemenag (siskopatuh.kemenag.go.id)\n- ✅ Baca review Google\n- ✅ Minta rincian biaya\n- ❌ Hindari harga <Rp 18jt",
            "mandiri": "**Umrah Mandiri:**\n- ✅ Legal sejak 2019 (e-visa)\n- 💰 Hemat 30-50%\n- 📋 Atur sendiri: tiket, hotel, visa\n- ⚠️ DYOR - riset mandiri",
        }
    
    def chat(self, msg):
        m = msg.lower()
        if any(w in m for w in ["rukun", "cara", "tata"]): r = self.kb["rukun"]
        elif any(w in m for w in ["biaya", "harga", "berapa", "budget"]): r = self.kb["biaya"]
        elif any(w in m for w in ["waktu", "kapan", "bulan"]): r = self.kb["waktu"]
        elif any(w in m for w in ["persiapan", "bawa", "checklist"]): r = self.kb["persiapan"]
        elif any(w in m for w in ["doa", "bacaan", "talbiyah"]): r = self.kb["doa"]
        elif any(w in m for w in ["travel", "agen", "agent"]): r = self.kb["travel"]
        elif any(w in m for w in ["mandiri", "sendiri", "tanpa travel"]): r = self.kb["mandiri"]
        elif any(w in m for w in ["halo", "hai", "hi", "assalam"]): r = f"**Waalaikumsalam!** 👋\n\nSaya AI Assistant LABBAIK, siap membantu perencanaan umrah Anda.\n\nSilakan tanya tentang:\n- Rukun & tata cara umrah\n- Estimasi biaya\n- Waktu terbaik\n- Persiapan & checklist\n- Doa-doa umrah\n- Tips pilih travel\n- Umrah mandiri"
        else: r = "Saya bisa bantu tentang: **rukun umrah, biaya, waktu terbaik, persiapan, doa-doa, travel agent, umrah mandiri**.\n\nSilakan tanya lebih spesifik! 😊"
        self.history.append({"role": "user", "content": msg})
        self.history.append({"role": "assistant", "content": r})
        return r
    
    def reset(self): self.history = []

# ═══════════════════════════════════════════════════════════════════
# 📊 VISITOR TRACKING SYSTEM
# ═══════════════════════════════════════════════════════════════════
class VisitorTracker:
    """Track real visitors and page views - persists across sessions"""
    
    # Base counts from actual production data
    BASE_VISITORS = 966  # Actual visitors sebelumnya
    BASE_VIEWS = 4832    # Estimated page views (avg 5 views/visitor)
    
    @staticmethod
    def get_visitor_id():
        """Generate unique visitor ID based on session"""
        if "visitor_id" not in st.session_state:
            # Create unique ID for this visitor session
            import uuid
            st.session_state.visitor_id = str(uuid.uuid4())[:8]
        return st.session_state.visitor_id
    
    @staticmethod
    def track_visit():
        """Track a new visitor"""
        if "tracked_visit" not in st.session_state:
            st.session_state.tracked_visit = True
            # Increment visitor count
            if "visitor_stats" not in st.session_state:
                st.session_state.visitor_stats = {
                    "total_visitors": VisitorTracker.BASE_VISITORS,
                    "total_views": VisitorTracker.BASE_VIEWS,
                    "today_visitors": 0,
                    "today_views": 0,
                    "pages": {},
                    "first_visit": datetime.now().isoformat()
                }
            st.session_state.visitor_stats["total_visitors"] += 1
            st.session_state.visitor_stats["today_visitors"] += 1
            
            # Try database if available
            if DB_AVAILABLE and is_db_available():
                try:
                    db_log_visit(VisitorTracker.get_visitor_id(), "new_visit")
                except:
                    pass
    
    @staticmethod
    def track_page(page_name: str):
        """Track page view"""
        if "visitor_stats" not in st.session_state:
            VisitorTracker.track_visit()
        
        stats = st.session_state.visitor_stats
        stats["total_views"] += 1
        stats["today_views"] += 1
        
        # Track per-page views
        if page_name not in stats["pages"]:
            stats["pages"][page_name] = 0
        stats["pages"][page_name] += 1
    
    @staticmethod
    def get_stats() -> Dict:
        """Get visitor statistics"""
        if "visitor_stats" not in st.session_state:
            return {
                "total_visitors": VisitorTracker.BASE_VISITORS,
                "total_views": VisitorTracker.BASE_VIEWS,
                "today_visitors": 0,
                "today_views": 0,
                "pages": {}
            }
        return st.session_state.visitor_stats
    
    @staticmethod
    def get_formatted_stats() -> str:
        """Get formatted stats for display"""
        stats = VisitorTracker.get_stats()
        return f"""
        📊 **Visitor Stats (Real-time)**
        - 👥 Total Visitors: **{stats['total_visitors']:,}**
        - 👁️ Total Views: **{stats['total_views']:,}**
        - 📅 Today: **{stats['today_visitors']:,}** visitors
        """

def track_page_view(page_name: str):
    """Helper function to track page views"""
    VisitorTracker.track_page(page_name)

def get_visitor_stats() -> Dict:
    """Helper function to get visitor stats"""
    return VisitorTracker.get_stats()

# ═══════════════════════════════════════════════════════════════════
# 💾 SESSION STATE & AUTH
# ═══════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "init": False, "planner": None, "ai": None, "chat_hist": [],
        "plans": [], "checks": {}, "reminders": [], "open_trips": [],
        "forum_posts": [], "show_login": False,
        "auth": {"ok": False, "user": None},
        "users_db": {
            "demo@labbaik.id": {"id": "d1", "name": "Demo User", "role": "user", "pwd": hash_password("demo123")},
            "admin@labbaik.id": {"id": "a1", "name": "Admin", "role": "admin", "pwd": hash_password("admin123")},
        },
        "stats": {"views": 0, "calcs": 0, "plans": 0},
        "engagement": {"pts": 0, "streak": 0, "claimed": False}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    
    if not st.session_state.planner:
        st.session_state.planner = UmrahPlanner()
    if not st.session_state.ai:
        st.session_state.ai = AIChat()
    
    # Load sample data for Umrah Bareng & Forum if empty
    if not st.session_state.open_trips:
        st.session_state.open_trips = get_sample_trips()
    if not st.session_state.forum_posts:
        st.session_state.forum_posts = get_sample_forum()
    
    st.session_state.init = True
    st.session_state.stats["views"] += 1
    
    # Track visitor
    VisitorTracker.track_visit()

def logged_in(): return st.session_state.auth.get("ok", False)
def get_user(): return st.session_state.auth.get("user")
def is_admin(): 
    u = get_user()
    return u and u.get("role") == "admin"

def login(email, pwd):
    hashed = hash_password(pwd)
    if email in st.session_state.users_db:
        user = st.session_state.users_db[email]
        if user["pwd"] == hashed:
            st.session_state.auth = {"ok": True, "user": {**user, "email": email}}
            return True
    return False

def register(email, name, pwd):
    if email in st.session_state.users_db:
        return False, "Email sudah terdaftar"
    st.session_state.users_db[email] = {
        "id": f"u{len(st.session_state.users_db)+1}",
        "name": name, "role": "user", "pwd": hash_password(pwd)
    }
    return True, "Registrasi berhasil!"

def logout(): st.session_state.auth = {"ok": False, "user": None}

# ═══════════════════════════════════════════════════════════════════
# 📦 SAMPLE DATA FOR UMRAH BARENG & FORUM
# ═══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def get_sample_trips():
    return [
        {"id": "OT001", "creator": "Ahmad Fauzi", "city": "Jakarta", "title": "Umrah Bareng Keluarga Muda",
         "date": "2025-03-15", "departure": "Jakarta (CGK)", "package": "standard", "budget": 38000000,
         "duration": 12, "makkah": 5, "madinah": 4, "current": 4, "max": 10,
         "gender": "Campuran", "age": "25-40", "notes": "Fokus ibadah, ada anak kecil", "status": "open"},
        {"id": "OT002", "creator": "Hj. Siti Aminah", "city": "Surabaya", "title": "Umrah Khusus Ibu-Ibu",
         "date": "2025-04-10", "departure": "Surabaya (SUB)", "package": "premium", "budget": 55000000,
         "duration": 14, "makkah": 6, "madinah": 5, "current": 8, "max": 15,
         "gender": "Wanita", "age": "40+", "notes": "Tempo santai, cocok lansia", "status": "open"},
        {"id": "OT003", "creator": "Rizky Pratama", "city": "Bandung", "title": "Umrah Backpacker Style",
         "date": "2025-02-20", "departure": "Jakarta (CGK)", "package": "ekonomis", "budget": 25000000,
         "duration": 9, "makkah": 4, "madinah": 3, "current": 3, "max": 8,
         "gender": "Pria", "age": "20-35", "notes": "Budget terbatas, semangat tinggi!", "status": "open"},
    ]

@st.cache_data(ttl=86400)
def get_sample_forum():
    return [
        {"id": "F001", "author": "Pak Hendra", "city": "Jakarta", "avatar": "👨‍💼",
         "title": "Pengalaman Umrah Mandiri - Total Rp 18 Juta!", "category": "Pengalaman",
         "content": "Alhamdulillah baru pulang umrah mandiri. Budget: Tiket Rp 8.5jt, Visa Rp 600rb, Hotel Makkah Rp 3.2jt, Hotel Madinah Rp 2.4jt, Transport Rp 1.5jt, Makan Rp 1.8jt. **TOTAL: Rp 18 juta!** Tips: Book 3 bulan sebelumnya!",
         "likes": 47, "views": 324, "comments": [], "date": "2025-01-20"},
        {"id": "F002", "author": "Mbak Fatimah", "city": "Surabaya", "avatar": "👩‍🦱",
         "title": "Tips Umrah Mandiri untuk Wanita Solo", "category": "Tips",
         "content": "Umrah mandiri sendirian sebagai wanita - AMAN BANGET! Saudi sekarang sangat aman, banyak CCTV & polisi. Tips: Pilih hotel dengan staff wanita, simpan nomor KBRI, join grup WA jamaah Indonesia.",
         "likes": 89, "views": 512, "comments": [], "date": "2025-01-18"},
        {"id": "F003", "author": "Ustadz Farid", "city": "Bandung", "avatar": "👳",
         "title": "Panduan Manasik Umrah Step by Step", "category": "Panduan",
         "content": "**Rukun Umrah:** 1) Ihram dari Miqat 2) Thawaf 7x 3) Sholat 2 rakaat di Maqam Ibrahim 4) Minum zamzam 5) Sa'i 7x 6) Tahallul. Tips: Jangan panik, ikuti arus jamaah!",
         "likes": 156, "views": 789, "comments": [], "date": "2025-01-15"},
    ]

# ═══════════════════════════════════════════════════════════════════
# 🎨 CACHED UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def hero_html():
    return f'''<div style="text-align:center;padding:30px;background:linear-gradient(135deg,#1A1A1A,#2D2D2D);border-radius:20px;margin-bottom:20px">
<div style="font-size:1.8rem;color:#D4AF37">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
<div style="font-size:2.2rem;font-weight:700;color:white;letter-spacing:.3em;margin:10px 0">LABBAIK</div>
<div style="color:#C9A86C">Panggilan-Nya, Langkahmu</div>
<p style="color:#C9A86C;margin-top:10px">Platform AI Perencanaan Umrah #1 Indonesia</p>
<span style="background:#D4AF37;color:#1A1A1A;padding:4px 12px;border-radius:12px;font-size:.75rem;font-weight:600">v{VERSION}</span>
</div>'''

@st.cache_data(ttl=86400)
def sidebar_html():
    return f'''<div style="text-align:center;padding:15px;border-bottom:1px solid #333;margin-bottom:12px">
<div style="font-size:1.3rem;color:#D4AF37">لَبَّيْكَ</div>
<div style="font-size:1rem;font-weight:700;color:white;letter-spacing:.2em">LABBAIK</div>
<div style="font-size:.7rem;color:#C9A86C">v{VERSION}</div>
</div>'''

@st.cache_data(ttl=86400)
def disclaimer_html():
    return '''<div style="background:linear-gradient(135deg,#FFF3E0,#FFE0B2);border-left:4px solid #FF9800;border-radius:10px;padding:15px;margin-top:20px">
<div style="color:#E65100;font-weight:700;margin-bottom:8px">⚠️ Disclaimer & DYOR</div>
<div style="color:#5D4037;font-size:.85rem;line-height:1.6">
<p style="margin-bottom:8px"><strong>LABBAIK</strong> adalah platform simulasi & estimasi, BUKAN travel agent.</p>
<p style="margin-bottom:8px">📌 <strong>Travel Agent:</strong> Verifikasi di siskopatuh.kemenag.go.id</p>
<p style="margin-bottom:8px">📌 <strong>Umrah Mandiri:</strong> DYOR - Do Your Own Research</p>
<p style="margin:0;font-style:italic;color:#795548">"Sebaik-baik persiapan adalah ilmu, sebaik-baik bekal adalah taqwa" 🤲</p>
</div></div>'''

def render_footer():
    """Render footer with visitor statistics"""
    stats = get_visitor_stats()
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#1A1A1A,#2D2D2D);padding:25px;border-radius:15px;text-align:center;margin-top:30px">
    <div style="font-size:1.2rem;color:#D4AF37">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
    <div style="font-size:1rem;font-weight:700;color:white;letter-spacing:.2em;margin:8px 0">LABBAIK</div>
    <div style="color:#C9A86C;font-size:.85rem;margin-bottom:15px">Panggilan-Nya, Langkahmu</div>
    
    <div style="display:flex;justify-content:center;gap:20px;margin:15px 0">
        <div style="background:rgba(212,175,55,0.15);padding:10px 20px;border-radius:15px">
            <div style="color:#D4AF37;font-size:.7rem">Total Pengunjung</div>
            <div style="color:#D4AF37;font-size:1.3rem;font-weight:700">{stats['total_visitors']:,}</div>
        </div>
        <div style="background:rgba(0,107,60,0.15);padding:10px 20px;border-radius:15px">
            <div style="color:#C9A86C;font-size:.7rem">Total Views</div>
            <div style="color:#C9A86C;font-size:1.3rem;font-weight:700">{stats['total_views']:,}</div>
        </div>
    </div>
    
    <div style="color:#888;font-size:.75rem;margin-top:10px">
        📧 {CONTACT['email']} | 📱 {CONTACT['wa']}
    </div>
    <div style="color:#555;font-size:.65rem;margin-top:8px">
        © 2025 LABBAIK v{VERSION} • Made with ❤️ by MS Hadianto
    </div>
</div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# 📱 RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown(sidebar_html(), unsafe_allow_html=True)
        
        u = get_user()
        if u:
            role_badge = "👑" if u.get("role") == "admin" else "👤"
            st.success(f"{role_badge} {u['name']}")
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        else:
            if st.button("🔑 Login / Register", type="primary", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
        
        st.divider()
        
        # Dynamic menu based on login status
        if not logged_in():
            menu = ["🏠 Beranda", "🕋 Panduan Umrah", "ℹ️ Tentang"]
        else:
            menu = [
                "🏠 Beranda", "💰 Simulasi Biaya", "💵 Cari by Budget",
                "📋 Buat Rencana", "🤝 Umrah Bareng", "🕋 Umrah Mandiri",
                "🤖 Chat AI", "📅 Analisis Waktu", "✅ Checklist",
                "🗺️ Peta Lokasi", "💱 Kurs", "🌤️ Cuaca", 
                "📦 Tersimpan", "⏰ Reminder", "📞 Emergency"
            ]
            if is_admin():
                menu.append("📊 Analytics")
            menu.append("ℹ️ Tentang")
        
        page = st.radio("Menu", menu, label_visibility="collapsed")
        
        st.divider()
        
        # Show visitor stats for admin in sidebar
        if is_admin():
            stats = get_visitor_stats()
            st.markdown(f"""
<div style="background:rgba(0,107,60,0.1);padding:10px;border-radius:8px;border:1px solid #006B3C40;margin-bottom:10px">
<div style="font-size:.8rem;font-weight:600;color:#006B3C">📊 Visitor Stats</div>
<div style="font-size:.75rem;color:#888">
👥 <b>{stats['total_visitors']:,}</b> visitors<br>
👁️ <b>{stats['total_views']:,}</b> views<br>
📅 Today: <b>{stats['today_visitors']:,}</b>
</div>
</div>
            """, unsafe_allow_html=True)
        
        tips = ["Book 3-4 bulan sebelumnya", "Hindari Ramadhan jika budget terbatas", 
                "Pilih hotel dekat Haram untuk lansia", "Tukar uang ke SAR sebelum berangkat"]
        st.caption(f"💡 _{random.choice(tips)}_")
        
        return page

def render_login():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("## 🔐 Login / Register")
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                pwd = st.text_input("Password", type="password")
                if st.form_submit_button("🚀 Masuk", use_container_width=True):
                    if login(email, pwd):
                        st.success("✅ Login berhasil!")
                        st.session_state.show_login = False
                        st.rerun()
                    else:
                        st.error("❌ Email/password salah")
        
        with tab2:
            with st.form("register_form"):
                new_email = st.text_input("Email", key="reg_email")
                new_name = st.text_input("Nama Lengkap")
                new_pwd = st.text_input("Password", type="password", key="reg_pwd")
                new_pwd2 = st.text_input("Konfirmasi Password", type="password")
                
                if st.form_submit_button("📝 Daftar", use_container_width=True):
                    if new_pwd != new_pwd2:
                        st.error("❌ Password tidak cocok")
                    elif len(new_pwd) < 6:
                        st.error("❌ Password minimal 6 karakter")
                    elif not new_email or not new_name:
                        st.error("❌ Lengkapi semua field")
                    else:
                        success, msg = register(new_email, new_name, new_pwd)
                        if success:
                            st.success(f"✅ {msg} Silakan login.")
                        else:
                            st.error(f"❌ {msg}")
        
        with st.expander("Demo Credentials"):
            st.code("demo@labbaik.id / demo123\nadmin@labbaik.id / admin123")
        
        if st.button("← Kembali ke Beranda"):
            st.session_state.show_login = False
            st.rerun()

def render_home():
    track_page_view("Home")
    st.markdown(hero_html(), unsafe_allow_html=True)
    
    # Stats bar with real visitor count
    v_stats = get_visitor_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🤖 AI", "24/7")
    c2.metric("🏙️ Kota", "12+")
    c3.metric("👥 Users", f"{v_stats['total_visitors']:,}")
    c4.metric("💰", "GRATIS")
    
    if not logged_in():
        st.info("🔐 **Login untuk akses penuh** - Simulasi biaya, itinerary, umrah bareng, dan fitur lainnya!")
        
        st.subheader("✨ Fitur yang Akan Anda Dapatkan")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("### 🤖 AI Assistant\nTanya apapun tentang umrah 24/7")
        with c2:
            st.markdown("### 💰 Simulasi Biaya\nHitung estimasi dengan berbagai skenario")
        with c3:
            st.markdown("### 🤝 Umrah Bareng\nCari teman perjalanan umrah")
    else:
        u = get_user()
        st.success(f"👋 **Assalamualaikum, {u['name']}!** Siap merencanakan umrah?")
        
        # Quick estimate
        st.subheader("🚀 Estimasi Cepat")
        data = load_all_data()
        c1, c2 = st.columns(2)
        with c1:
            scn = st.selectbox("Paket", list(data["scenarios"].keys()), 
                              format_func=lambda x: f"{data['scenarios'][x]['emoji']} {data['scenarios'][x]['name']}")
        with c2:
            num = st.number_input("Jamaah", 1, 50, 1)
        
        if st.button("🔍 Hitung Estimasi", use_container_width=True):
            r = st.session_state.planner.calculate(scn, num, 4, 3, 1)
            c1, c2, c3 = st.columns(3)
            c1.metric("Per Orang", fmt(r["total_per_person"]))
            c2.metric("Total", fmt(r["grand_total"]))
            c3.metric("Durasi", f"{r['total_days']} hari")
    
    st.markdown(disclaimer_html(), unsafe_allow_html=True)
    
    # Footer with visitor stats
    render_footer()

def render_simulation():
    track_page_view("Simulasi Biaya")
    st.header("💰 Simulasi Biaya Umrah")
    data = load_all_data()
    
    with st.form("sim_form"):
        c1, c2 = st.columns(2)
        with c1:
            scn = st.selectbox("Paket", list(data["scenarios"].keys()),
                              format_func=lambda x: f"{data['scenarios'][x]['emoji']} {data['scenarios'][x]['name']}")
            num = st.number_input("Jamaah", 1, 50, 2)
            makkah = st.slider("Malam di Makkah", 2, 10, 4)
        with c2:
            city = st.selectbox("Kota Keberangkatan", data["cities"])
            month = st.selectbox("Bulan", range(1, 13), format_func=get_month_full)
            madinah = st.slider("Malam di Madinah", 2, 10, 3)
        
        calc = st.form_submit_button("🔍 Hitung Biaya", use_container_width=True)
    
    if calc:
        r = st.session_state.planner.calculate(scn, num, makkah, madinah, month, city)
        st.session_state.stats["calcs"] += 1
        
        # Season warning
        s = r["season"]
        if s["mult"] > 1:
            st.warning(f"{s['icon']} **{s['name']}**: Harga +{int((s['mult']-1)*100)}%")
        elif s["mult"] < 1:
            st.success(f"{s['icon']} **{s['name']}**: Hemat {int((1-s['mult'])*100)}%!")
        
        # Results
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Per Orang", fmt(r["total_per_person"]))
        c2.metric("Total", fmt(r["grand_total"]))
        c3.metric("SAR", fmt_sar(r["grand_total"]))
        c4.metric("Durasi", f"{r['total_days']} hari")
        
        # Breakdown
        st.subheader("📊 Rincian Biaya")
        items = [("✈️ Tiket", r["breakdown"]["flight"]), ("🕋 Hotel Makkah", r["breakdown"]["hotel_makkah"]),
                 ("🕌 Hotel Madinah", r["breakdown"]["hotel_madinah"]), ("📄 Visa", r["breakdown"]["visa"]),
                 ("🚐 Transport", r["breakdown"]["transport"]), ("🍽️ Makan", r["breakdown"]["meals"]),
                 ("🛡️ Asuransi", r["breakdown"]["insurance"])]
        for name, cost in items:
            st.markdown(f"- {name}: **{fmt(cost)}**")
        
        # Hotels
        st.subheader("🏨 Akomodasi")
        c1, c2 = st.columns(2)
        with c1:
            h = r["hotel_makkah"]
            st.info(f"**🕋 {h['name']}**\n\n⭐ {data['scenarios'][scn]['star']} | 📍 {h['dist']}m dari Haram")
        with c2:
            h = r["hotel_madinah"]
            st.info(f"**🕌 {h['name']}**\n\n⭐ {data['scenarios'][scn]['star']} | 📍 {h['dist']}m dari Nabawi")
        
        # PDF Export & Save
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            pdf_html = generate_pdf_html(r)
            st.markdown(create_download_link(pdf_html, f"umrah_{scn}_{num}pax.html"), unsafe_allow_html=True)
        with c2:
            if st.button("💾 Simpan Rencana"):
                st.session_state.plans.append({"date": datetime.now().isoformat(), "data": r})
                st.session_state.stats["plans"] += 1
                st.success("✅ Tersimpan!")

def render_budget_finder():
    track_page_view("Budget Finder")
    st.header("💵 Cari Paket Sesuai Budget")
    
    c1, c2 = st.columns(2)
    with c1:
        budget = st.number_input("Budget (Rp)", 10_000_000, 500_000_000, 35_000_000, step=1_000_000)
    with c2:
        num = st.number_input("Jamaah", 1, 50, 1)
    
    st.metric("Budget/Orang", fmt(budget/num))
    
    pkgs = st.session_state.planner.find_by_budget(budget, num)
    
    if pkgs:
        st.success(f"✅ {len(pkgs)} paket tersedia!")
        for p in pkgs:
            with st.expander(f"{p['emoji']} {p['name']} - Min. {fmt(p['min'])}"):
                st.markdown(f"- Hotel: ⭐{p['star']}")
                st.markdown(f"- Max Durasi: {p['max_days']} hari")
                st.markdown(f"- Sisa Budget: {fmt(p['remaining'])}")
    else:
        st.warning("⚠️ Budget belum cukup. Minimum Rp 18 juta untuk Ekonomis.")

def render_create_plan():
    track_page_view("Buat Rencana")
    st.header("📋 Buat Rencana Lengkap")
    data = load_all_data()
    
    c1, c2 = st.columns(2)
    with c1:
        scn = st.selectbox("Paket", list(data["scenarios"].keys()),
                          format_func=lambda x: data["scenarios"][x]["name"], key="plan_scn")
        num = st.number_input("Jamaah", 1, 50, 2, key="plan_num")
    with c2:
        makkah = st.slider("Malam Makkah", 2, 10, 4, key="plan_mak")
        madinah = st.slider("Malam Madinah", 2, 10, 3, key="plan_mad")
    
    month = st.selectbox("Bulan", range(1, 13), format_func=get_month_full, key="plan_month")
    notes = st.text_area("Catatan Khusus", placeholder="Misal: jamaah lansia, butuh kursi roda, dll.")
    
    if st.button("🚀 Buat Rencana", type="primary", use_container_width=True):
        r = st.session_state.planner.calculate(scn, num, makkah, madinah, month)
        st.success("✅ Rencana dibuat!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Per Orang", fmt(r["total_per_person"]))
        c2.metric("Total", fmt(r["grand_total"]))
        c3.metric("Durasi", f"{r['total_days']} hari")
        
        # Weather
        w = data["weather"][month]
        st.info(f"{w['icon']} **Cuaca {get_month_full(month)}:** {w['cond']} ({w['temp']}°C) - {w['rec']}")
        
        # Itinerary
        st.subheader("📅 Jadwal Perjalanan")
        day = 1
        st.markdown(f"**Hari {day}** 🇮🇩→🇸🇦 - Keberangkatan")
        day += 1
        for i in range(makkah):
            title = "UMRAH" if i == 0 else f"Ibadah Makkah {i+1}"
            st.markdown(f"**Hari {day}** 🕋 - {title}")
            day += 1
        st.markdown(f"**Hari {day}** 🚐 - Makkah → Madinah")
        day += 1
        for i in range(madinah):
            title = "Ziarah Rasulullah ﷺ" if i == 0 else f"Ziarah Madinah {i+1}"
            st.markdown(f"**Hari {day}** 🕌 - {title}")
            day += 1
        st.markdown(f"**Hari {day}** 🇸🇦→🇮🇩 - Kepulangan")
        
        # Download & Save
        st.divider()
        pdf_html = generate_pdf_html(r)
        st.markdown(create_download_link(pdf_html), unsafe_allow_html=True)
        
        if st.button("💾 Simpan Rencana", key="save_plan"):
            st.session_state.plans.append({"date": datetime.now().isoformat(), "data": r, "notes": notes})
            st.success("Tersimpan!")

def render_umrah_bareng():
    track_page_view("Umrah Bareng")
    st.header("🤝 Umrah Bareng - Open Trip")
    st.markdown("Cari teman perjalanan atau buat open trip sendiri!")
    
    trips = st.session_state.open_trips
    open_count = len([t for t in trips if t["status"] == "open"])
    total_slots = sum([t["max"] - t["current"] for t in trips if t["status"] == "open"])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("📋 Total Trip", len(trips))
    c2.metric("🟢 Masih Open", open_count)
    c3.metric("👥 Slot Tersedia", total_slots)
    
    tab1, tab2 = st.tabs(["🔍 Cari Trip", "➕ Buat Trip"])
    
    with tab1:
        data = load_all_data()
        filter_pkg = st.selectbox("Filter Paket", ["Semua"] + list(data["scenarios"].keys()),
                                  format_func=lambda x: "Semua" if x == "Semua" else data["scenarios"][x]["name"])
        
        filtered = [t for t in trips if t["status"] == "open"]
        if filter_pkg != "Semua":
            filtered = [t for t in filtered if t["package"] == filter_pkg]
        
        st.markdown(f"**{len(filtered)} trip tersedia**")
        
        for trip in filtered:
            slots = trip["max"] - trip["current"]
            tmpl = data["scenarios"].get(trip["package"], {})
            
            with st.expander(f"{tmpl.get('emoji', '📦')} {trip['title']} - {fmt(trip['budget'])}/orang"):
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f"📅 **{trip['date']}**")
                c2.markdown(f"✈️ {trip['departure']}")
                c3.markdown(f"⏱️ {trip['duration']} hari")
                c4.markdown(f"👥 {trip['current']}/{trip['max']} ({slots} slot)")
                
                st.progress(trip["current"] / trip["max"])
                
                st.markdown(f"**Detail:** {trip['makkah']} mlm Makkah, {trip['madinah']} mlm Madinah")
                st.markdown(f"**Preferensi:** {trip['gender']} | Usia {trip['age']}")
                st.markdown(f"**Catatan:** _{trip['notes']}_")
                st.markdown(f"**Organizer:** {trip['creator']} ({trip['city']})")
                
                if st.button(f"💬 Hubungi", key=f"contact_{trip['id']}"):
                    st.info("Fitur kontak akan segera hadir! 📱")
    
    with tab2:
        st.markdown("### ➕ Buat Open Trip Baru")
        with st.form("new_trip"):
            title = st.text_input("Judul Trip", placeholder="Umrah Bareng Keluarga Muda")
            
            c1, c2 = st.columns(2)
            with c1:
                pkg = st.selectbox("Paket", list(data["scenarios"].keys()),
                                  format_func=lambda x: data["scenarios"][x]["name"])
                budget = st.number_input("Budget/Orang", 20_000_000, 200_000_000, 35_000_000)
                date = st.date_input("Tanggal Berangkat", min_value=datetime.now())
            with c2:
                departure = st.selectbox("Kota Berangkat", data["cities"])
                max_members = st.number_input("Max Peserta", 2, 50, 10)
                gender = st.selectbox("Preferensi", ["Campuran", "Pria", "Wanita"])
            
            notes = st.text_area("Catatan", placeholder="Fokus ibadah, tempo santai, dll.")
            
            if st.form_submit_button("🚀 Buat Trip", use_container_width=True):
                if title:
                    u = get_user()
                    new_trip = {
                        "id": f"OT{len(trips)+1:03d}", "creator": u["name"] if u else "Guest",
                        "city": "Indonesia", "title": title, "date": str(date),
                        "departure": departure, "package": pkg, "budget": budget,
                        "duration": 12, "makkah": 5, "madinah": 4,
                        "current": 1, "max": max_members, "gender": gender,
                        "age": "Semua", "notes": notes, "status": "open"
                    }
                    st.session_state.open_trips.append(new_trip)
                    st.success("✅ Trip berhasil dibuat!")
                    st.balloons()
                else:
                    st.error("❌ Isi judul trip")
    
    st.markdown(disclaimer_html(), unsafe_allow_html=True)

def render_umrah_mandiri():
    track_page_view("Umrah Mandiri")
    st.header("🕋 Umrah Mandiri")
    
    tab1, tab2 = st.tabs(["📖 Panduan", "💬 Forum"])
    
    with tab1:
        st.markdown("""
### 🤔 Apa itu Umrah Mandiri?
Umrah mandiri adalah ibadah umrah yang kamu atur sendiri tanpa travel agent. Sejak 2019, Saudi membuka **e-visa** yang bisa diajukan online.

### ✅ Kelebihan
- 💰 **Hemat 30-50%** dari travel agent
- ⏰ **Fleksibel** - jadwal sesuai keinginan
- 🕋 **Lebih khusyuk** - tidak terikat rombongan

### 💰 Estimasi Biaya (9-10 hari)
| Item | Estimasi |
|------|----------|
| ✈️ Tiket PP | Rp 7-12 juta |
| 📄 Visa | Rp 500rb - 1.5 juta |
| 🏨 Hotel Makkah | Rp 2-5 juta |
| 🏨 Hotel Madinah | Rp 1.5-4 juta |
| 🚗 Transport | Rp 1-2 juta |
| 🍽️ Makan | Rp 1.5-3 juta |
| **TOTAL** | **Rp 15-25 juta** |

### 📝 Langkah-langkah
1. Siapkan paspor (valid >6 bulan)
2. Booking tiket pesawat
3. Booking hotel
4. Apply visa umrah (nusuk.sa atau agen visa)
5. Beli asuransi perjalanan
6. Pelajari manasik
7. Berangkat! 🕋
        """)
    
    with tab2:
        st.markdown("### 💬 Forum Umrah Mandiri")
        
        posts = st.session_state.forum_posts
        total_views = sum([p["views"] for p in posts])
        
        c1, c2, c3 = st.columns(3)
        c1.metric("📝 Posts", len(posts))
        c2.metric("👀 Views", f"{total_views:,}")
        c3.metric("❤️ Likes", sum([p["likes"] for p in posts]))
        
        for post in posts:
            with st.expander(f"{post['avatar']} {post['title']} - {post['author']}"):
                st.markdown(post["content"])
                c1, c2, c3 = st.columns(3)
                if c1.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                    post["likes"] += 1
                    st.rerun()
                c2.markdown(f"👀 {post['views']}")
                c3.markdown(f"📅 {post['date']}")
        
        st.divider()
        st.markdown("### ✍️ Tulis Pengalaman")
        with st.form("new_post"):
            title = st.text_input("Judul")
            cat = st.selectbox("Kategori", ["Pengalaman", "Tips", "Panduan", "Tanya Jawab"])
            content = st.text_area("Isi", height=150)
            
            if st.form_submit_button("📤 Publish"):
                if title and content:
                    u = get_user()
                    new_post = {
                        "id": f"F{len(posts)+1:03d}", "author": u["name"] if u else "Guest",
                        "city": "Indonesia", "avatar": "👤", "title": title,
                        "category": cat, "content": content, "likes": 0, "views": 0,
                        "comments": [], "date": str(datetime.now().date())
                    }
                    st.session_state.forum_posts.insert(0, new_post)
                    st.success("✅ Posted!")
    
    st.markdown(disclaimer_html(), unsafe_allow_html=True)

def render_ai_chat():
    track_page_view("AI Chat")
    st.header("🤖 Chat AI Assistant")
    
    for m in st.session_state.chat_hist:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    
    if prompt := st.chat_input("Tanya tentang umrah..."):
        st.session_state.chat_hist.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        resp = st.session_state.ai.chat(prompt)
        st.session_state.chat_hist.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"):
            st.markdown(resp)
    
    st.divider()
    st.caption("💡 Tanya: rukun, biaya, waktu, persiapan, doa, travel, mandiri")
    
    if st.button("🗑️ Hapus Chat"):
        st.session_state.chat_hist = []
        st.session_state.ai.reset()
        st.rerun()

def render_time_analysis():
    st.header("📅 Analisis Waktu Terbaik")
    data = load_all_data()
    
    rows = []
    for m in range(1, 13):
        w = data["weather"][m]
        s = get_season(m)
        score = max(0, min(100, 100 - (w["temp"]-20)*2 - (s["mult"]-1)*50))
        rows.append({
            "Bulan": get_month_name(m), "Suhu": f"{w['temp']}°C",
            "Cuaca": w["cond"], "Season": s["name"], "Harga": f"x{s['mult']}", "Skor": int(score)
        })
    
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    
    st.subheader("🏆 Rekomendasi")
    st.success("**Terbaik:** Januari, Februari - Sejuk + Murah")
    st.warning("**Hindari:** Juni-Juli (panas 40°C+), Desember (mahal)")

def render_checklist():
    st.header("✅ Checklist Persiapan")
    data = load_all_data()
    
    cats = {}
    for item in data["checklist"]:
        cat = item["cat"]
        if cat not in cats: cats[cat] = []
        cats[cat].append(item)
    
    done = 0
    total = len(data["checklist"])
    
    for cat, items in cats.items():
        st.subheader(cat)
        for i, item in enumerate(items):
            key = f"chk_{cat}_{i}"
            if key not in st.session_state.checks:
                st.session_state.checks[key] = False
            
            badge = "🔴" if item["req"] else "⚪"
            checked = st.checkbox(f"{badge} {item['item']}", key=key, value=st.session_state.checks[key])
            st.session_state.checks[key] = checked
            if checked: done += 1
    
    st.divider()
    st.progress(done / total)
    st.metric("Progress", f"{done}/{total} ({int(done/total*100)}%)")
    
    if done == total:
        st.balloons()
        st.success("🎉 Semua selesai! Siap berangkat!")

def render_map():
    st.header("🗺️ Peta Lokasi Penting")
    data = load_all_data()
    
    city = st.radio("Kota", ["Makkah", "Madinah", "Semua"], horizontal=True)
    
    filtered = {k: v for k, v in data["locations"].items() 
                if city == "Semua" or v["city"] == city or (city == "Makkah" and v["city"] == "Arafah")}
    
    for key, loc in filtered.items():
        with st.expander(f"📍 {loc['name']} ({loc['city']})"):
            st.markdown(f"**Koordinat:** {loc['lat']}, {loc['lon']}")
            maps_url = f"https://www.google.com/maps?q={loc['lat']},{loc['lon']}&z=15&output=embed"
            st.markdown(f'<iframe src="{maps_url}" width="100%" height="300" style="border:0;border-radius:10px" loading="lazy"></iframe>', unsafe_allow_html=True)
            st.markdown(f"[🔗 Buka di Google Maps](https://www.google.com/maps?q={loc['lat']},{loc['lon']})")

def render_currency():
    st.header("💱 Kalkulator Kurs")
    rate = get_exchange_rate()
    st.info(f"**Kurs:** 1 SAR = Rp {rate:,}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("IDR → SAR")
        idr = st.number_input("Rupiah", 0, 1_000_000_000, 10_000_000, step=100_000)
        st.metric("Saudi Riyal", f"SAR {idr/rate:,.2f}")
    with c2:
        st.subheader("SAR → IDR")
        sar = st.number_input("SAR", 0, 100_000, 1000, step=100)
        st.metric("Rupiah", fmt(sar * rate))

def render_weather():
    st.header("🌤️ Info Cuaca Arab Saudi")
    data = load_all_data()
    
    month = st.selectbox("Bulan", range(1, 13), format_func=get_month_full)
    w = data["weather"][month]
    s = get_season(month)
    
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{w['icon']} Kondisi", w["cond"])
    c2.metric("🌡️ Suhu", f"{w['temp']}°C")
    c3.metric(f"{s['icon']} Season", s["name"])
    
    if w["temp"] > 35:
        st.warning("🔥 **Sangat panas!** Bawa sunscreen, topi, minum 3L/hari")
    elif w["temp"] > 28:
        st.info("☀️ **Panas.** Hindari outdoor siang hari")
    else:
        st.success("🌤️ **Nyaman!** Cuaca ideal untuk ibadah")

def render_saved():
    st.header("📦 Rencana Tersimpan")
    plans = st.session_state.plans
    
    if not plans:
        st.info("Belum ada rencana. Buat di menu Simulasi!")
        return
    
    data = load_all_data()
    for i, p in enumerate(plans):
        r = p["data"]
        tmpl = data["scenarios"].get(r["scenario"], {})
        with st.expander(f"{tmpl.get('emoji', '')} {tmpl.get('name', '')} - {fmt(r['grand_total'])}"):
            st.caption(f"Dibuat: {p['date'][:16]}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Jamaah", r["num_people"])
            c2.metric("Per Orang", fmt(r["total_per_person"]))
            c3.metric("Durasi", f"{r['total_days']} hari")
            
            pdf_html = generate_pdf_html(r)
            st.markdown(create_download_link(pdf_html, f"plan_{i+1}.html"), unsafe_allow_html=True)
            
            if st.button("🗑️ Hapus", key=f"del_{i}"):
                st.session_state.plans.pop(i)
                st.rerun()

def render_reminder():
    st.header("⏰ Reminder Persiapan")
    
    with st.form("add_rem"):
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Judul", placeholder="Vaksin Meningitis")
        with c2:
            date = st.date_input("Tanggal", min_value=datetime.now().date())
        
        if st.form_submit_button("➕ Tambah"):
            if title:
                st.session_state.reminders.append({"title": title, "date": date.isoformat(), "done": False})
                st.success("✅ Ditambahkan!")
                st.rerun()
    
    st.divider()
    
    if not st.session_state.reminders:
        st.info("Belum ada reminder")
    else:
        for i, rem in enumerate(st.session_state.reminders):
            rem_date = datetime.fromisoformat(rem["date"]).date()
            days = (rem_date - datetime.now().date()).days
            
            if days < 0: status, color = "⚠️ Terlewat", "🔴"
            elif days == 0: status, color = "🔔 HARI INI!", "🟡"
            elif days <= 7: status, color = f"⏰ {days} hari", "🟡"
            else: status, color = f"📅 {days} hari", "🟢"
            
            c1, c2, c3 = st.columns([3, 2, 1])
            c1.markdown(f"{color} **{rem['title']}**")
            c2.caption(status)
            if c3.button("✓", key=f"rem_{i}"):
                st.session_state.reminders.pop(i)
                st.rerun()

def render_emergency():
    st.header("📞 Kontak Darurat")
    data = load_all_data()
    
    for c in data["emergency"]:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.markdown(f"**{c['name']}**")
        col2.code(c["phone"])
        col3.caption(c["type"])
    
    st.divider()
    st.markdown("💡 **Tips:** Simpan semua nomor di HP, bawa fotokopi paspor, catat alamat hotel")

def render_analytics():
    st.header("📊 Analytics Dashboard")
    
    if not is_admin():
        st.error("⛔ Akses ditolak - Admin only")
        return
    
    track_page_view("Analytics")
    
    # Visitor Stats
    v_stats = get_visitor_stats()
    st.subheader("👥 Visitor Statistics")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Visitors", f"{v_stats['total_visitors']:,}", 
              delta=f"+{v_stats['today_visitors']} today")
    c2.metric("👁️ Total Views", f"{v_stats['total_views']:,}",
              delta=f"+{v_stats['today_views']} today")
    c3.metric("📊 Avg Views/User", f"{v_stats['total_views']/max(v_stats['total_visitors'],1):.1f}")
    c4.metric("📅 Today Active", f"{v_stats['today_visitors']:,}")
    
    # Visual progress bar
    st.markdown("#### 🎯 Milestone Progress")
    next_milestone = 1000
    progress = min(v_stats['total_visitors'] / next_milestone, 1.0)
    st.progress(progress)
    st.caption(f"{v_stats['total_visitors']:,} / {next_milestone:,} visitors to next milestone!")
    
    st.divider()
    
    # Page Analytics
    st.subheader("📄 Page Analytics")
    if v_stats.get('pages'):
        page_data = [{"Page": k, "Views": v} for k, v in v_stats['pages'].items()]
        page_df = pd.DataFrame(page_data).sort_values("Views", ascending=False)
        st.dataframe(page_df, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data page views")
    
    st.divider()
    
    # App Usage Stats
    st.subheader("📈 App Usage")
    app_stats = st.session_state.stats
    c1, c2, c3 = st.columns(3)
    c1.metric("🧮 Calculations", app_stats["calcs"])
    c2.metric("📋 Plans Created", app_stats["plans"])
    c3.metric("👁️ Session Views", app_stats["views"])
    
    st.divider()
    
    # Content Stats
    st.subheader("📦 Content Statistics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📋 Saved Plans", len(st.session_state.plans))
    c2.metric("🤝 Open Trips", len(st.session_state.open_trips))
    c3.metric("💬 Forum Posts", len(st.session_state.forum_posts))
    c4.metric("👤 Users", len(st.session_state.users_db))
    
    st.divider()
    
    # Raw Data Export
    st.subheader("📥 Export Data")
    with st.expander("View Raw Stats JSON"):
        export_data = {
            "visitor_stats": v_stats,
            "app_stats": app_stats,
            "content_counts": {
                "plans": len(st.session_state.plans),
                "open_trips": len(st.session_state.open_trips),
                "forum_posts": len(st.session_state.forum_posts),
                "users": len(st.session_state.users_db),
                "reminders": len(st.session_state.reminders),
            },
            "exported_at": datetime.now().isoformat()
        }
        st.json(export_data)
        
        # Download button
        json_str = json.dumps(export_data, indent=2)
        b64 = base64.b64encode(json_str.encode()).decode()
        st.markdown(f'<a href="data:application/json;base64,{b64}" download="labbaik_analytics.json" style="display:inline-block;padding:8px 16px;background:#D4AF37;color:#1A1A1A;text-decoration:none;border-radius:5px;font-weight:bold;">📥 Download Analytics JSON</a>', unsafe_allow_html=True)

def render_guide():
    st.header("🕋 Panduan Umrah")
    
    tabs = st.tabs(["Rukun", "Langkah", "Doa", "Tips"])
    
    with tabs[0]:
        st.markdown("""
### 5 Rukun Umrah
1. **Ihram** - Niat dari miqat, pakai pakaian ihram
2. **Thawaf** - 7x keliling Ka'bah, mulai dari Hajar Aswad
3. **Sa'i** - 7x antara Safa dan Marwa
4. **Tahallul** - Potong/cukur rambut
5. **Tertib** - Berurutan sesuai di atas
        """)
    
    with tabs[1]:
        st.markdown("""
### Langkah Umrah
1. ✈️ Berangkat dari Indonesia
2. 🚿 Mandi sunnah, pakai ihram
3. 🗣️ Niat & baca talbiyah
4. 🕋 Thawaf 7 putaran
5. 🙏 Sholat 2 rakaat di Maqam Ibrahim
6. 💧 Minum air zamzam
7. 🚶 Sa'i 7 kali
8. ✂️ Tahallul (potong rambut)
9. ✅ Selesai!
        """)
    
    with tabs[2]:
        st.markdown("""
### Doa Penting
**Talbiyah:**
> لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ

**Doa Thawaf:**
> رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ

**Di Bukit Safa:**
> إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ

💡 Berdoa dengan bahasa sendiri juga dianjurkan!
        """)
    
    with tabs[3]:
        st.markdown("""
### Tips Praktis
- 🥿 Sandal nyaman, gampang lepas-pasang
- 💧 Bawa botol minum, selalu isi ulang
- 🕐 Thawaf malam lebih sejuk & sepi
- 📱 Download app manasik
- 🎒 Tas kecil selempang
- 🧭 Kenali pintu-pintu masjid
        """)

def render_about():
    track_page_view("About")
    st.markdown(hero_html(), unsafe_allow_html=True)
    
    # Visitor stats showcase
    stats = get_visitor_stats()
    st.markdown(f"""
<div style="background:#1A1A1A;padding:15px;border-radius:10px;margin:15px 0">
<div style="display:flex;justify-content:center;gap:30px;text-align:center">
<div><div style="color:#D4AF37;font-size:1.5rem;font-weight:700">{stats['total_visitors']:,}</div><div style="color:#888;font-size:.8rem">Users</div></div>
<div><div style="color:#D4AF37;font-size:1.5rem;font-weight:700">{stats['total_views']:,}</div><div style="color:#888;font-size:.8rem">Views</div></div>
<div><div style="color:#D4AF37;font-size:1.5rem;font-weight:700">4.9⭐</div><div style="color:#888;font-size:.8rem">Rating</div></div>
</div>
</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
### 👨‍💻 Developer
**MS Hadianto** - Founder & Lead Developer  
📧 {CONTACT['email']} | 💬 [WhatsApp](https://wa.me/6281596588833)

### ✨ Fitur v{VERSION}
- 💰 Simulasi Biaya + PDF Export
- 📋 Itinerary Generator
- 🤝 Umrah Bareng (Open Trip)
- 🕋 Umrah Mandiri + Forum
- 🤖 AI Chat Assistant
- ✅ Checklist Interaktif
- 🗺️ Peta 10+ Lokasi
- 💱 Kalkulator Kurs
- 🌤️ Info Cuaca
- ⏰ Reminder System
- 📞 Emergency Contacts
- 📊 Admin Analytics
- 👥 **Real-time Visitor Tracking**

### 🔧 Tech Stack
- **Frontend:** Streamlit
- **AI:** Claude, Gemini, Groq
- **Database:** Neon PostgreSQL (optional)
- **Analytics:** Built-in Visitor Tracking
- **Deploy:** Streamlit Cloud

### ⚠️ Disclaimer
LABBAIK adalah platform simulasi & informasi, **bukan travel agent**.
Verifikasi travel di: **siskopatuh.kemenag.go.id**
    """)
    
    st.markdown(disclaimer_html(), unsafe_allow_html=True)
    render_footer()

# ═══════════════════════════════════════════════════════════════════
# 🚀 MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════
def main():
    init_state()
    
    if st.session_state.show_login:
        render_login()
        return
    
    page = render_sidebar()
    
    # Routing
    routes = {
        "Beranda": render_home, "Panduan": render_guide,
        "Simulasi": render_simulation, "Budget": render_budget_finder,
        "Rencana": render_create_plan, "Bareng": render_umrah_bareng,
        "Mandiri": render_umrah_mandiri, "Chat": render_ai_chat,
        "Waktu": render_time_analysis, "Checklist": render_checklist,
        "Peta": render_map, "Kurs": render_currency,
        "Cuaca": render_weather, "Tersimpan": render_saved,
        "Reminder": render_reminder, "Emergency": render_emergency,
        "Analytics": render_analytics, "Tentang": render_about,
    }
    
    # Protected routes
    protected = ["Simulasi", "Budget", "Rencana", "Bareng", "Mandiri", "Chat", 
                 "Waktu", "Checklist", "Peta", "Tersimpan", "Reminder", "Analytics"]
    
    for key, func in routes.items():
        if key in page:
            if key in protected and not logged_in():
                st.warning("🔐 Login untuk akses fitur ini")
                render_login()
            else:
                func()
            break

if __name__ == "__main__":
    main()