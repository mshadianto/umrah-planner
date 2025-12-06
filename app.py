"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  لَبَّيْكَ LABBAIK v3.8.1 - DATABASE INTEGRATED                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🚀 NEON POSTGRESQL • ⚡ LIGHTWEIGHT • 📱 MOBILE-READY                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
Copyright (c) 2025 MS Hadianto. All Rights Reserved.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json, base64, random, hashlib, secrets

# ═══════════════════════════════════════════════════════════════════
# 🔧 PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="LABBAIK - Platform Umrah AI #1 Indonesia",
    page_icon="🕋", layout="wide", initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════
# 📊 CONSTANTS
# ═══════════════════════════════════════════════════════════════════
VERSION = "3.8.1"
BRAND = {"name": "LABBAIK", "arabic": "لَبَّيْكَ", "tagline": "Panggilan-Nya, Langkahmu"}
COLORS = {"black": "#1A1A1A", "gold": "#D4AF37", "green": "#006B3C", "sand": "#C9A86C"}
CONTACT = {"email": "sopian.hadianto@gmail.com", "wa": "+62 815 9658 833"}
BASE_VISITORS = 966  # Historical base from production

# ═══════════════════════════════════════════════════════════════════
# 🗄️ DATABASE FUNCTIONS (Matching Neon Schema)
# ═══════════════════════════════════════════════════════════════════
def get_db():
    """Get database connection"""
    try: return st.connection("neon", type="sql")
    except: return None

def db_available(): return get_db() is not None

def hash_pwd(pwd):
    salt = secrets.token_hex(16)
    return f"{salt}:{hashlib.sha256((pwd + salt).encode()).hexdigest()}"

def verify_pwd(pwd, stored):
    try:
        if ':' in stored:
            salt, h = stored.split(':')
            return hashlib.sha256((pwd + salt).encode()).hexdigest() == h
        return hashlib.sha256(pwd.encode()).hexdigest() == stored
    except: return False

# ─────────────────────────────────────────────────────────────────
# 👤 USER MANAGEMENT
# ─────────────────────────────────────────────────────────────────
def db_register(email, pwd, name):
    """Register user to database"""
    conn = get_db()
    if not conn: return False, "Database tidak tersedia"
    try:
        existing = conn.query("SELECT id FROM users WHERE email = :e", params={"e": email.lower()}, ttl=0)
        if len(existing) > 0: return False, "Email sudah terdaftar"
        
        role = "admin" if "admin" in email.lower() else "user"
        with conn.session as s:
            s.execute("""INSERT INTO users (email, password_hash, name, role, created_at) 
                        VALUES (:e, :p, :n, :r, CURRENT_TIMESTAMP)""",
                     {"e": email.lower(), "p": hash_pwd(pwd), "n": name, "r": role})
            s.commit()
        return True, f"✅ Registrasi berhasil! Role: {role.upper()}"
    except Exception as e: return False, str(e)

def db_login(email, pwd):
    """Login from database"""
    conn = get_db()
    if not conn: return None
    try:
        result = conn.query("SELECT * FROM users WHERE email = :e", params={"e": email.lower()}, ttl=0)
        if len(result) == 0: return None
        user = result.to_dict('records')[0]
        if verify_pwd(pwd, user.get('password_hash', '')):
            try:
                with conn.session as s:
                    s.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = :id", {"id": user['id']})
                    s.commit()
            except: pass
            return {"id": user['id'], "email": user['email'], "name": user['name'], 
                    "role": user.get('role', 'user'), "avatar": user.get('avatar', '👤')}
        return None
    except: return None

# ─────────────────────────────────────────────────────────────────
# 📊 PAGE VIEWS (Matching: page_views table)
# ─────────────────────────────────────────────────────────────────
def db_log_page_view(page_name, visitor_id):
    """Log page view - matches page_views table schema"""
    conn = get_db()
    if not conn: return
    try:
        with conn.session as s:
            s.execute("""INSERT INTO page_views (page_name, visitor_id, viewed_at) 
                        VALUES (:p, :v, CURRENT_TIMESTAMP)""", {"p": page_name, "v": visitor_id})
            s.commit()
    except: pass

def db_get_visitor_stats():
    """Get visitor stats from page_views table"""
    conn = get_db()
    base = {"total_visitors": BASE_VISITORS, "total_views": BASE_VISITORS * 5, "today_visitors": 0, "today_views": 0}
    if not conn: return base
    try:
        # Total unique visitors from page_views
        r = conn.query("SELECT COUNT(DISTINCT visitor_id) as c FROM page_views", ttl=60)
        db_visitors = r.to_dict('records')[0]['c'] or 0
        base["total_visitors"] = BASE_VISITORS + db_visitors
        
        # Total views
        r = conn.query("SELECT COUNT(*) as c FROM page_views", ttl=60)
        db_views = r.to_dict('records')[0]['c'] or 0
        base["total_views"] = (BASE_VISITORS * 5) + db_views
        
        # Today's unique visitors
        r = conn.query("SELECT COUNT(DISTINCT visitor_id) as c FROM page_views WHERE DATE(viewed_at) = CURRENT_DATE", ttl=60)
        base["today_visitors"] = r.to_dict('records')[0]['c'] or 0
        
        # Today's views
        r = conn.query("SELECT COUNT(*) as c FROM page_views WHERE DATE(viewed_at) = CURRENT_DATE", ttl=60)
        base["today_views"] = r.to_dict('records')[0]['c'] or 0
        
        return base
    except: return base

def db_get_page_stats():
    """Get per-page statistics"""
    conn = get_db()
    if not conn: return {}
    try:
        r = conn.query("SELECT page_name, COUNT(*) as views FROM page_views GROUP BY page_name ORDER BY views DESC", ttl=60)
        return {row['page_name']: row['views'] for row in r.to_dict('records')}
    except: return {}

# ─────────────────────────────────────────────────────────────────
# 🤝 OPEN TRIPS
# ─────────────────────────────────────────────────────────────────
def db_get_open_trips():
    """Get open trips from database"""
    conn = get_db()
    if not conn: return []
    try:
        r = conn.query("""SELECT t.*, u.name as creator_name FROM open_trips t 
                         LEFT JOIN users u ON t.creator_id = u.id 
                         WHERE t.status = 'open' ORDER BY t.created_at DESC LIMIT 50""", ttl=30)
        trips = r.to_dict('records')
        for t in trips:
            t['amenities'] = t.get('amenities', '').split(',') if t.get('amenities') else []
        return trips
    except: return []

def db_create_trip(creator_id, trip_data):
    """Create open trip"""
    conn = get_db()
    if not conn: return {"success": False, "error": "Database tidak tersedia"}
    try:
        code = f"OT{secrets.token_hex(4).upper()}"
        with conn.session as s:
            s.execute("""INSERT INTO open_trips (creator_id, trip_code, title, departure_date, departure_city,
                        package_type, budget_per_person, duration_days, max_members, status, created_at)
                        VALUES (:cid, :code, :title, :date, :city, :pkg, :budget, :days, :max, 'open', CURRENT_TIMESTAMP)""",
                     {"cid": creator_id, "code": code, "title": trip_data.get("title", ""),
                      "date": trip_data.get("departure_date"), "city": trip_data.get("departure_city", ""),
                      "pkg": trip_data.get("package_type", "standard"), "budget": trip_data.get("budget_per_person", 0),
                      "days": trip_data.get("duration_days", 9), "max": trip_data.get("max_members", 10)})
            s.commit()
        return {"success": True, "trip_code": code}
    except Exception as e: return {"success": False, "error": str(e)}

# ─────────────────────────────────────────────────────────────────
# 💬 FORUM POSTS
# ─────────────────────────────────────────────────────────────────
def db_get_forum_posts():
    """Get forum posts"""
    conn = get_db()
    if not conn: return []
    try:
        r = conn.query("""SELECT p.*, u.name as author_name, u.avatar as author_avatar 
                         FROM forum_posts p LEFT JOIN users u ON p.author_id = u.id 
                         ORDER BY p.created_at DESC LIMIT 50""", ttl=30)
        return r.to_dict('records')
    except: return []

def db_create_post(author_id, title, category, content):
    """Create forum post"""
    conn = get_db()
    if not conn: return {"success": False}
    try:
        with conn.session as s:
            s.execute("""INSERT INTO forum_posts (author_id, title, category, content, likes, views, created_at)
                        VALUES (:aid, :t, :c, :ct, 0, 0, CURRENT_TIMESTAMP)""",
                     {"aid": author_id, "t": title, "c": category, "ct": content})
            s.commit()
        return {"success": True}
    except: return {"success": False}

# ═══════════════════════════════════════════════════════════════════
# 💾 CACHED DATA
# ═══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400, show_spinner=False)
def load_all_data():
    return {
        "scenarios": {
            "ekonomis": {"name": "Ekonomis", "emoji": "💚", "star": 3, "mult": 1.0},
            "standard": {"name": "Standard", "emoji": "💙", "star": 4, "mult": 1.3},
            "premium": {"name": "Premium", "emoji": "🧡", "star": 5, "mult": 1.8},
            "vip": {"name": "VIP", "emoji": "💛", "star": 5, "mult": 2.5},
        },
        "cities": ["Jakarta (CGK)", "Surabaya (SUB)", "Medan (KNO)", "Makassar (UPG)", 
                   "Bandung (BDO)", "Semarang (SRG)", "Yogyakarta (JOG)", "Denpasar (DPS)",
                   "Palembang (PLM)", "Balikpapan (BPN)", "Pekanbaru (PKU)", "Padang (PDG)"],
        "hotels": {
            "ekonomis": {"makkah": {"name": "Hotel ⭐⭐⭐ (1-2km)", "price": 800000}, "madinah": {"name": "Hotel ⭐⭐⭐ (500m)", "price": 600000}},
            "standard": {"makkah": {"name": "Hotel ⭐⭐⭐⭐ (500m)", "price": 1500000}, "madinah": {"name": "Hotel ⭐⭐⭐⭐ (300m)", "price": 1000000}},
            "premium": {"makkah": {"name": "Hotel ⭐⭐⭐⭐⭐ (200m)", "price": 2500000}, "madinah": {"name": "Hotel ⭐⭐⭐⭐⭐ (100m)", "price": 1800000}},
            "vip": {"makkah": {"name": "Hotel ⭐⭐⭐⭐⭐ View Ka'bah", "price": 5000000}, "madinah": {"name": "Hotel ⭐⭐⭐⭐⭐ View Nabawi", "price": 3500000}}
        },
        "costs": {
            "ekonomis": {"flight": 8000000, "visa": 500000, "transport": 500000, "meals": 300000},
            "standard": {"flight": 12000000, "visa": 500000, "transport": 800000, "meals": 500000},
            "premium": {"flight": 18000000, "visa": 500000, "transport": 1200000, "meals": 800000},
            "vip": {"flight": 30000000, "visa": 500000, "transport": 2000000, "meals": 1500000}
        },
        "weather": {m: {"temp": [20,22,26,31,36,38,39,39,36,31,25,21][m-1], "cond": ["Sejuk","Sejuk","Hangat","Panas","Sangat Panas","Ekstrem","Ekstrem","Ekstrem","Panas","Hangat","Sejuk","Sejuk"][m-1]} for m in range(1,13)},
        "checklist": [
            {"cat": "📄 Dokumen", "items": ["Paspor (valid >6 bln)", "Foto 4x6 bg putih", "KTP", "Vaksin Meningitis", "KK"]},
            {"cat": "👔 Pakaian", "items": ["Ihram 2 set (pria)", "Mukena 2 set (wanita)", "Sandal nyaman"]},
            {"cat": "📿 Ibadah", "items": ["Buku doa & manasik", "Al-Quran kecil", "Sajadah travel"]},
            {"cat": "💊 Kesehatan", "items": ["Obat pribadi", "Vitamin", "Masker", "Sunscreen SPF 50+"]},
            {"cat": "🔌 Elektronik", "items": ["HP + charger", "Adaptor Type G", "Power bank"]},
        ],
        "locations": {
            "kabah": {"name": "Ka'bah & Masjidil Haram", "lat": 21.4225, "lon": 39.8262},
            "safa_marwa": {"name": "Bukit Safa & Marwa", "lat": 21.4234, "lon": 39.8277},
            "masjid_nabawi": {"name": "Masjid Nabawi", "lat": 24.4672, "lon": 39.6112},
            "raudhah": {"name": "Raudhah", "lat": 24.4674, "lon": 39.6110},
            "masjid_quba": {"name": "Masjid Quba", "lat": 24.4397, "lon": 39.6169},
        },
        "emergency": [
            {"name": "KBRI Riyadh", "phone": "+966-11-488-2800"},
            {"name": "KJRI Jeddah", "phone": "+966-12-667-0645"},
            {"name": "Ambulans Saudi", "phone": "997"},
            {"name": "Polisi Saudi", "phone": "999"},
        ],
    }

@st.cache_data(ttl=3600)
def get_exchange_rate(): return 4250

def get_season(month):
    if month == 12: return {"name": "High", "mult": 1.4, "icon": "🔴"}
    if month in [3, 4]: return {"name": "Ramadan", "mult": 1.6, "icon": "🟣"}
    if month in [1, 2, 6, 7]: return {"name": "Low", "mult": 0.85, "icon": "🟢"}
    return {"name": "Regular", "mult": 1.0, "icon": "🔵"}

def fmt(amount, prefix="Rp"): return f"{prefix} {amount:,.0f}".replace(",", ".")
def fmt_sar(idr): return f"SAR {idr/get_exchange_rate():,.0f}"
def get_month_name(m): return ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"][m-1]
def get_month_full(m): return ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"][m-1]

# ═══════════════════════════════════════════════════════════════════
# 🧮 PLANNER CLASS
# ═══════════════════════════════════════════════════════════════════
class UmrahPlanner:
    def __init__(self): self.data = load_all_data()
    
    def calculate(self, scenario, num, makkah_nights, madinah_nights, month):
        d = self.data
        hotel, cost = d["hotels"][scenario], d["costs"][scenario]
        season = get_season(month)
        total_days = makkah_nights + madinah_nights + 2
        
        breakdown = {
            "flight": cost["flight"], "hotel_makkah": hotel["makkah"]["price"] * makkah_nights,
            "hotel_madinah": hotel["madinah"]["price"] * madinah_nights, "visa": cost["visa"],
            "transport": cost["transport"], "meals": cost["meals"] * total_days
        }
        subtotal = sum(breakdown.values())
        total_pp = subtotal * season["mult"]
        
        return {"scenario": scenario, "num_people": num, "nights_makkah": makkah_nights,
                "nights_madinah": madinah_nights, "total_days": total_days, "breakdown": breakdown,
                "total_per_person": total_pp, "grand_total": total_pp * num, "season": season,
                "hotel_makkah": hotel["makkah"], "hotel_madinah": hotel["madinah"]}
    
    def find_by_budget(self, budget, num=1):
        budget_pp = budget / num
        available = []
        for key, tmpl in self.data["scenarios"].items():
            hotel, cost = self.data["hotels"][key], self.data["costs"][key]
            min_cost = cost["flight"] + cost["visa"] + cost["transport"] + hotel["makkah"]["price"]*4 + hotel["madinah"]["price"]*3 + cost["meals"]*9
            if budget_pp >= min_cost:
                available.append({"key": key, "name": tmpl["name"], "emoji": tmpl["emoji"], "min": min_cost, "star": tmpl["star"]})
        return sorted(available, key=lambda x: x["min"])

# ═══════════════════════════════════════════════════════════════════
# 🤖 AI CHAT
# ═══════════════════════════════════════════════════════════════════
class AIChat:
    def __init__(self):
        self.kb = {
            "rukun": "**5 Rukun Umrah:**\n1️⃣ Ihram - Niat dari miqat\n2️⃣ Thawaf - 7x keliling Ka'bah\n3️⃣ Sa'i - 7x Safa-Marwa\n4️⃣ Tahallul - Potong rambut\n5️⃣ Tertib - Berurutan",
            "biaya": "**Estimasi 2025:**\n- 💚 Ekonomis: Rp 20-28jt\n- 💙 Standard: Rp 28-40jt\n- 🧡 Premium: Rp 40-60jt\n- 💛 VIP: Rp 60-150jt",
            "waktu": "**Waktu Terbaik:** Jan-Feb (sejuk+murah), Sep-Okt\n**Hindari:** Jun-Jul (panas 40°C+), Des (mahal)",
            "persiapan": "**Wajib Bawa:** Paspor >6bln, Foto 4x6, Vaksin Meningitis, Ihram, Sandal nyaman, Obat pribadi, Adaptor Type G",
            "doa": "**Talbiyah:**\n> لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ",
        }
    def chat(self, msg):
        m = msg.lower()
        if any(w in m for w in ["rukun", "cara", "langkah"]): return self.kb["rukun"]
        if any(w in m for w in ["biaya", "harga", "budget", "berapa"]): return self.kb["biaya"]
        if any(w in m for w in ["waktu", "kapan", "bulan"]): return self.kb["waktu"]
        if any(w in m for w in ["persiapan", "bawa", "siap"]): return self.kb["persiapan"]
        if any(w in m for w in ["doa", "talbiyah", "dzikir"]): return self.kb["doa"]
        if any(w in m for w in ["halo", "hai", "assalam", "hi"]): return "**Waalaikumsalam!** 👋 Saya AI LABBAIK, siap bantu perencanaan umrah Anda."
        return "Silakan tanya tentang: **rukun umrah, biaya, waktu terbaik, persiapan, doa-doa** 😊"

# ═══════════════════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "init": False, "planner": None, "ai": None, "chat_hist": [],
        "plans": [], "checks": {}, "reminders": [], "show_login": False,
        "auth": {"ok": False, "user": None}, "stats": {"calcs": 0, "plans": 0}
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
    
    if not st.session_state.planner: st.session_state.planner = UmrahPlanner()
    if not st.session_state.ai: st.session_state.ai = AIChat()
    
    # Generate visitor ID (persistent per session)
    if "visitor_id" not in st.session_state:
        st.session_state.visitor_id = secrets.token_hex(8)
    
    st.session_state.init = True

def logged_in(): return st.session_state.auth.get("ok", False)
def get_user(): return st.session_state.auth.get("user")
def is_admin(): 
    u = get_user()
    return u and u.get("role") == "admin"

def login(email, pwd):
    if not email or not pwd: return False, "Email dan password harus diisi"
    user = db_login(email.strip().lower(), pwd)
    if user:
        st.session_state.auth = {"ok": True, "user": user}
        return True, "Login berhasil!"
    return False, "Email/password salah atau belum terdaftar"

def register(email, name, pwd):
    if not email or not name or not pwd: return False, "Semua field harus diisi"
    if "@" not in email: return False, "Format email tidak valid"
    if len(pwd) < 6: return False, "Password minimal 6 karakter"
    return db_register(email.strip(), pwd, name.strip())

def logout(): st.session_state.auth = {"ok": False, "user": None}

def track_page(page):
    """Track page view to database"""
    db_log_page_view(page, st.session_state.get("visitor_id", "unknown"))

# ═══════════════════════════════════════════════════════════════════
# 🎨 CACHED UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def hero_html():
    return f'''<div style="text-align:center;padding:30px;background:linear-gradient(135deg,#1A1A1A,#2D2D2D);border-radius:20px;margin-bottom:20px">
<div style="font-size:1.8rem;color:#D4AF37">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
<div style="font-size:2rem;font-weight:700;color:white;letter-spacing:.3em;margin:10px 0">LABBAIK</div>
<div style="color:#C9A86C">Panggilan-Nya, Langkahmu</div>
<span style="background:#D4AF37;color:#1A1A1A;padding:4px 12px;border-radius:12px;font-size:.75rem;font-weight:600">v{VERSION}</span>
</div>'''

@st.cache_data(ttl=86400)
def sidebar_html():
    return f'''<div style="text-align:center;padding:15px;border-bottom:1px solid #333;margin-bottom:12px">
<div style="font-size:1.3rem;color:#D4AF37">لَبَّيْكَ</div>
<div style="font-size:1rem;font-weight:700;color:white;letter-spacing:.2em">LABBAIK</div>
<div style="font-size:.7rem;color:#C9A86C">v{VERSION}</div>
</div>'''

def disclaimer_html():
    return '''<div style="background:linear-gradient(135deg,#FFF3E0,#FFE0B2);border-left:4px solid #FF9800;border-radius:10px;padding:15px;margin-top:20px">
<div style="color:#E65100;font-weight:700;margin-bottom:8px">⚠️ Disclaimer</div>
<div style="color:#5D4037;font-size:.85rem">LABBAIK adalah platform simulasi, BUKAN travel agent resmi. Selalu verifikasi travel agent di <b>siskopatuh.kemenag.go.id</b></div>
</div>'''

def render_footer():
    stats = db_get_visitor_stats()
    st.markdown(f'''<div style="background:linear-gradient(135deg,#1A1A1A,#2D2D2D);padding:25px;border-radius:15px;text-align:center;margin-top:30px">
<div style="font-size:1.2rem;color:#D4AF37">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
<div style="font-size:1rem;font-weight:700;color:white;letter-spacing:.2em;margin:8px 0">LABBAIK</div>
<div style="display:flex;justify-content:center;gap:20px;margin:15px 0">
<div style="background:rgba(212,175,55,0.15);padding:10px 20px;border-radius:15px">
<div style="color:#D4AF37;font-size:.7rem">Pengunjung</div>
<div style="color:#D4AF37;font-size:1.3rem;font-weight:700">{stats['total_visitors']:,}</div>
</div>
<div style="background:rgba(0,107,60,0.15);padding:10px 20px;border-radius:15px">
<div style="color:#C9A86C;font-size:.7rem">Views</div>
<div style="color:#C9A86C;font-size:1.3rem;font-weight:700">{stats['total_views']:,}</div>
</div>
</div>
<div style="color:#666;font-size:.65rem">© 2025 LABBAIK v{VERSION} • Made with ❤️ by MS Hadianto</div>
</div>''', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# 📱 RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown(sidebar_html(), unsafe_allow_html=True)
        
        u = get_user()
        if u:
            badge = "👑" if u.get("role") == "admin" else "👤"
            st.success(f"{badge} {u['name']}")
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        else:
            if st.button("🔑 Login / Register", type="primary", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
        
        st.divider()
        
        if not logged_in():
            menu = ["🏠 Beranda", "🕋 Panduan Umrah", "ℹ️ Tentang"]
        else:
            menu = ["🏠 Beranda", "💰 Simulasi Biaya", "💵 Cari by Budget", "📋 Buat Rencana",
                    "🤝 Umrah Bareng", "🕋 Umrah Mandiri", "🤖 Chat AI", "📅 Analisis Waktu",
                    "✅ Checklist", "🗺️ Peta Lokasi", "💱 Kurs", "🌤️ Cuaca",
                    "📦 Tersimpan", "⏰ Reminder", "📞 Emergency"]
            if is_admin():
                menu.extend(["📊 Analytics", "💼 Business Hub"])
            menu.append("ℹ️ Tentang")
        
        page = st.radio("Menu", menu, label_visibility="collapsed")
        
        st.divider()
        
        # Admin stats widget
        if is_admin():
            stats = db_get_visitor_stats()
            st.markdown(f'''<div style="background:rgba(0,107,60,0.1);padding:10px;border-radius:8px;font-size:.75rem">
📊 <b>{stats['total_visitors']:,}</b> visitors<br>
📅 Today: <b>{stats['today_visitors']}</b> | Views: <b>{stats['today_views']}</b>
</div>''', unsafe_allow_html=True)
        
        tips = ["Book 3-4 bulan sebelumnya", "Hindari Ramadhan jika budget terbatas", "Tukar uang ke SAR sebelum berangkat"]
        st.caption(f"💡 _{random.choice(tips)}_")
        return page

def render_login():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("## 🔐 Login / Register")
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="email@example.com")
                pwd = st.text_input("Password", type="password")
                if st.form_submit_button("🚀 Masuk", use_container_width=True):
                    ok, msg = login(email, pwd)
                    if ok:
                        st.success(f"✅ {msg}")
                        st.session_state.show_login = False
                        st.rerun()
                    else: st.error(f"❌ {msg}")
        
        with tab2:
            with st.form("register_form"):
                new_email = st.text_input("Email", key="reg_email", placeholder="email@example.com")
                new_name = st.text_input("Nama Lengkap", placeholder="Nama Anda")
                new_pwd = st.text_input("Password", type="password", key="reg_pwd")
                new_pwd2 = st.text_input("Konfirmasi Password", type="password")
                st.caption("💡 Email dengan kata 'admin' otomatis dapat akses Admin")
                
                if st.form_submit_button("📝 Daftar", use_container_width=True):
                    if new_pwd != new_pwd2: st.error("❌ Password tidak cocok")
                    else:
                        ok, msg = register(new_email, new_name, new_pwd)
                        if ok: st.success(f"{msg}")
                        else: st.error(f"❌ {msg}")
        
        if st.button("← Kembali"):
            st.session_state.show_login = False
            st.rerun()

def render_home():
    track_page("Home")
    st.markdown(hero_html(), unsafe_allow_html=True)
    
    stats = db_get_visitor_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🤖 AI", "24/7")
    c2.metric("🏙️ Kota", "12+")
    c3.metric("👥 Users", f"{stats['total_visitors']:,}")
    c4.metric("💰", "GRATIS")
    
    if not logged_in():
        st.info("🔐 **Login untuk akses penuh** - Simulasi biaya, itinerary, dan fitur lainnya!")
        c1, c2, c3 = st.columns(3)
        c1.markdown("### 🤖 AI Assistant\nTanya apapun tentang umrah")
        c2.markdown("### 💰 Simulasi Biaya\nHitung estimasi biaya")
        c3.markdown("### 🤝 Umrah Bareng\nCari teman perjalanan")
    else:
        u = get_user()
        st.success(f"👋 **Assalamualaikum, {u['name']}!**")
        
        st.subheader("🚀 Estimasi Cepat")
        data = load_all_data()
        c1, c2 = st.columns(2)
        scn = c1.selectbox("Paket", list(data["scenarios"].keys()), format_func=lambda x: f"{data['scenarios'][x]['emoji']} {data['scenarios'][x]['name']}")
        num = c2.number_input("Jamaah", 1, 50, 1)
        
        if st.button("🔍 Hitung", use_container_width=True):
            r = st.session_state.planner.calculate(scn, num, 4, 3, 1)
            c1, c2, c3 = st.columns(3)
            c1.metric("Per Orang", fmt(r["total_per_person"]))
            c2.metric("Total", fmt(r["grand_total"]))
            c3.metric("Durasi", f"{r['total_days']} hari")
    
    st.markdown(disclaimer_html(), unsafe_allow_html=True)
    render_footer()

def render_simulation():
    track_page("Simulasi Biaya")
    st.header("💰 Simulasi Biaya Umrah")
    data = load_all_data()
    
    with st.form("sim"):
        c1, c2 = st.columns(2)
        scn = c1.selectbox("Paket", list(data["scenarios"].keys()), format_func=lambda x: f"{data['scenarios'][x]['emoji']} {data['scenarios'][x]['name']}")
        num = c1.number_input("Jamaah", 1, 50, 2)
        mak = c1.slider("Malam Makkah", 2, 10, 4)
        month = c2.selectbox("Bulan", range(1, 13), format_func=get_month_full)
        mad = c2.slider("Malam Madinah", 2, 10, 3)
        calc = st.form_submit_button("🔍 Hitung Biaya", use_container_width=True, type="primary")
    
    if calc:
        r = st.session_state.planner.calculate(scn, num, mak, mad, month)
        st.session_state.stats["calcs"] += 1
        
        s = r["season"]
        if s["mult"] > 1: st.warning(f"{s['icon']} **{s['name']} Season**: Harga +{int((s['mult']-1)*100)}%")
        elif s["mult"] < 1: st.success(f"{s['icon']} **{s['name']} Season**: Hemat {int((1-s['mult'])*100)}%!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("💵 Per Orang", fmt(r["total_per_person"]))
        c2.metric("💰 Total", fmt(r["grand_total"]))
        c3.metric("📅 Durasi", f"{r['total_days']} hari")
        
        st.subheader("📊 Rincian Biaya")
        items = [("✈️ Tiket PP", r["breakdown"]["flight"]), ("🕋 Hotel Makkah", r["breakdown"]["hotel_makkah"]),
                 ("🕌 Hotel Madinah", r["breakdown"]["hotel_madinah"]), ("📄 Visa", r["breakdown"]["visa"]),
                 ("🚐 Transport", r["breakdown"]["transport"]), ("🍽️ Makan", r["breakdown"]["meals"])]
        for name, cost in items:
            st.markdown(f"- {name}: **{fmt(cost)}**")
        
        if st.button("💾 Simpan Rencana"):
            st.session_state.plans.append({"date": datetime.now().isoformat(), "data": r})
            st.session_state.stats["plans"] += 1
            st.success("✅ Tersimpan!")

def render_budget_finder():
    track_page("Budget Finder")
    st.header("💵 Cari Paket Sesuai Budget")
    c1, c2 = st.columns(2)
    budget = c1.number_input("Budget Total (Rp)", 10_000_000, 500_000_000, 35_000_000, step=1_000_000)
    num = c2.number_input("Jumlah Jamaah", 1, 50, 1)
    
    st.metric("Budget per Orang", fmt(budget/num))
    pkgs = st.session_state.planner.find_by_budget(budget, num)
    
    if pkgs:
        st.success(f"✅ {len(pkgs)} paket tersedia untuk budget Anda!")
        for p in pkgs:
            with st.expander(f"{p['emoji']} {p['name']} - Mulai {fmt(p['min'])}"):
                st.markdown(f"⭐ Bintang {p['star']} | Minimum: **{fmt(p['min'])}**/orang")
    else:
        st.warning("⚠️ Budget belum cukup untuk paket apapun. Minimum sekitar Rp 18 juta/orang.")

def render_create_plan():
    track_page("Buat Rencana")
    st.header("📋 Buat Rencana Lengkap")
    data = load_all_data()
    
    c1, c2 = st.columns(2)
    scn = c1.selectbox("Paket", list(data["scenarios"].keys()), format_func=lambda x: f"{data['scenarios'][x]['emoji']} {data['scenarios'][x]['name']}")
    num = c1.number_input("Jamaah", 1, 50, 2)
    mak = c2.slider("Malam Makkah", 2, 10, 4)
    mad = c2.slider("Malam Madinah", 2, 10, 3)
    month = st.selectbox("Bulan Keberangkatan", range(1, 13), format_func=get_month_full)
    
    if st.button("🚀 Buat Rencana", type="primary", use_container_width=True):
        r = st.session_state.planner.calculate(scn, num, mak, mad, month)
        st.success("✅ Rencana berhasil dibuat!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Per Orang", fmt(r["total_per_person"]))
        c2.metric("Total", fmt(r["grand_total"]))
        c3.metric("Durasi", f"{r['total_days']} hari")
        
        st.subheader("📅 Jadwal Perjalanan")
        day = 1
        st.markdown(f"**Hari {day}**: 🇮🇩→🇸🇦 Keberangkatan ke Jeddah")
        day += 1
        for i in range(mak):
            activity = "🕋 **UMRAH** - Thawaf, Sa'i, Tahallul" if i==0 else f"🕋 Ibadah di Makkah (hari {i+1})"
            st.markdown(f"**Hari {day}**: {activity}")
            day += 1
        st.markdown(f"**Hari {day}**: 🚐 Makkah → Madinah (±450km)")
        day += 1
        for i in range(mad):
            activity = "🕌 Ziarah Masjid Nabawi & Raudhah" if i==0 else f"🕌 Ziarah Madinah (hari {i+1})"
            st.markdown(f"**Hari {day}**: {activity}")
            day += 1
        st.markdown(f"**Hari {day}**: 🇸🇦→🇮🇩 Kepulangan")

def render_umrah_bareng():
    track_page("Umrah Bareng")
    st.header("🤝 Umrah Bareng - Open Trip")
    
    trips = db_get_open_trips()
    if not trips:  # Fallback data
        trips = [
            {"id": 1, "title": "Umrah Bareng Keluarga Muda", "creator_name": "Ahmad", "departure_date": "2025-03-15",
             "package_type": "standard", "budget_per_person": 38000000, "duration_days": 12, "max_members": 10, "status": "open"},
            {"id": 2, "title": "Umrah Khusus Ibu-Ibu", "creator_name": "Hj. Siti", "departure_date": "2025-04-10",
             "package_type": "premium", "budget_per_person": 55000000, "duration_days": 14, "max_members": 15, "status": "open"},
        ]
    
    c1, c2 = st.columns(2)
    c1.metric("📋 Total Trip", len(trips))
    c2.metric("👥 Slot Open", len([t for t in trips if t.get("status") == "open"]))
    
    st.divider()
    data = load_all_data()
    
    for trip in trips[:10]:
        tmpl = data["scenarios"].get(trip.get("package_type", "standard"), {"emoji": "📦"})
        with st.expander(f"{tmpl.get('emoji', '📦')} {trip['title']} - {fmt(trip.get('budget_per_person', 0))}"):
            st.markdown(f"👤 **{trip.get('creator_name', 'Anonymous')}** | 📅 {trip.get('departure_date', '-')}")
            st.markdown(f"⏱️ {trip.get('duration_days', 9)} hari | 👥 Max {trip.get('max_members', 10)} orang")
            st.button("📩 Hubungi", key=f"contact_{trip['id']}")
    
    st.markdown(disclaimer_html(), unsafe_allow_html=True)

def render_umrah_mandiri():
    track_page("Umrah Mandiri")
    st.header("🕋 Umrah Mandiri")
    
    tab1, tab2 = st.tabs(["📖 Panduan", "💬 Forum"])
    
    with tab1:
        st.markdown("""
### Apa itu Umrah Mandiri?
Umrah yang diatur sendiri tanpa travel agent. Legal sejak 2019 dengan sistem e-visa.

### 💰 Estimasi Biaya (9-10 hari)
| Item | Estimasi Biaya |
|------|----------------|
| ✈️ Tiket PP | Rp 7-12jt |
| 📄 Visa | Rp 500rb-1.5jt |
| 🏨 Hotel | Rp 3.5-9jt |
| 🚗 Transport | Rp 1-2jt |
| 🍽️ Makan | Rp 1.5-3jt |
| **Total** | **Rp 15-25jt** |

### ✅ Kelebihan
- 💰 Hemat 30-50% dari travel agent
- ⏰ Jadwal fleksibel
- 🕋 Lebih khusyuk & fokus ibadah

### ⚠️ Disclaimer
> **DYOR (Do Your Own Research)** - Pastikan Anda siap mengurus semuanya sendiri.
        """)
    
    with tab2:
        posts = db_get_forum_posts()
        if not posts:  # Fallback data
            posts = [
                {"id": 1, "title": "Pengalaman Umrah Mandiri Rp 18 Juta", "author_name": "Pak Hendra", "likes": 47},
                {"id": 2, "title": "Tips Wanita Solo Umrah Mandiri", "author_name": "Mbak Fatimah", "likes": 89},
            ]
        
        for p in posts[:10]:
            with st.expander(f"💬 {p.get('title', '-')} - {p.get('author_name', 'Anonim')}"):
                st.markdown(f"❤️ {p.get('likes', 0)} likes | 👁️ {p.get('views', 0)} views")
    
    st.markdown(disclaimer_html(), unsafe_allow_html=True)

def render_ai_chat():
    track_page("AI Chat")
    st.header("🤖 Chat AI Assistant")
    
    for m in st.session_state.chat_hist:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if prompt := st.chat_input("Tanya tentang umrah..."):
        st.session_state.chat_hist.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        resp = st.session_state.ai.chat(prompt)
        st.session_state.chat_hist.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"): st.markdown(resp)
    
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.chat_hist = []
        st.rerun()

def render_time_analysis():
    track_page("Analisis Waktu")
    st.header("📅 Analisis Waktu Terbaik")
    data = load_all_data()
    
    rows = []
    for m in range(1, 13):
        w = data["weather"][m]
        s = get_season(m)
        score = max(0, min(100, 100 - (w["temp"]-20)*2 - (s["mult"]-1)*50))
        rows.append({"Bulan": get_month_name(m), "Suhu": f"{w['temp']}°C", "Kondisi": w["cond"], "Season": f"{s['icon']} {s['name']}", "Skor": int(score)})
    
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.success("**Rekomendasi Terbaik:** Januari-Februari (sejuk + murah) atau September-Oktober")

def render_checklist():
    track_page("Checklist")
    st.header("✅ Checklist Persiapan Umrah")
    data = load_all_data()
    
    done, total = 0, 0
    for cat in data["checklist"]:
        st.subheader(cat["cat"])
        for item in cat["items"]:
            total += 1
            key = f"chk_{item}"
            if key not in st.session_state.checks: st.session_state.checks[key] = False
            if st.checkbox(item, key=key, value=st.session_state.checks[key]):
                st.session_state.checks[key] = True
                done += 1
    
    st.divider()
    progress = done / total if total > 0 else 0
    st.progress(progress)
    st.metric("Progress", f"{done}/{total} ({int(progress*100)}%)")

def render_map():
    track_page("Peta Lokasi")
    st.header("🗺️ Peta Lokasi Penting")
    data = load_all_data()
    
    for key, loc in data["locations"].items():
        with st.expander(f"📍 {loc['name']}"):
            url = f"https://www.google.com/maps?q={loc['lat']},{loc['lon']}&z=17&output=embed"
            st.markdown(f'<iframe src="{url}" width="100%" height="300" style="border:0;border-radius:10px" loading="lazy"></iframe>', unsafe_allow_html=True)
            st.markdown(f"📍 Koordinat: `{loc['lat']}, {loc['lon']}`")

def render_currency():
    track_page("Kurs")
    st.header("💱 Kalkulator Kurs IDR ↔ SAR")
    rate = get_exchange_rate()
    st.info(f"**Kurs Saat Ini:** 1 SAR = Rp {rate:,}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Rupiah → SAR")
        idr = st.number_input("Rupiah", 0, 1_000_000_000, 10_000_000, step=100_000)
        st.metric("Saudi Riyal", f"SAR {idr/rate:,.2f}")
    
    with c2:
        st.subheader("SAR → Rupiah")
        sar = st.number_input("SAR", 0, 100_000, 1000, step=100)
        st.metric("Rupiah", fmt(sar * rate))

def render_weather():
    track_page("Cuaca")
    st.header("🌤️ Info Cuaca Arab Saudi")
    data = load_all_data()
    month = st.selectbox("Pilih Bulan", range(1, 13), format_func=get_month_full)
    w = data["weather"][month]
    s = get_season(month)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("🌡️ Suhu Rata-rata", f"{w['temp']}°C")
    c2.metric("☁️ Kondisi", w["cond"])
    c3.metric(f"{s['icon']} Season", s["name"])
    
    if w["temp"] >= 35:
        st.warning("⚠️ **Tips:** Bawa sunscreen SPF 50+, minum banyak air, hindari aktivitas siang hari")
    elif w["temp"] <= 25:
        st.success("✅ **Cuaca ideal** untuk ibadah!")

def render_saved():
    track_page("Tersimpan")
    st.header("📦 Rencana Tersimpan")
    
    if not st.session_state.plans:
        st.info("📋 Belum ada rencana tersimpan. Buat rencana di menu **Simulasi Biaya**!")
        return
    
    data = load_all_data()
    for i, p in enumerate(st.session_state.plans):
        r = p["data"]
        tmpl = data["scenarios"].get(r["scenario"], {})
        with st.expander(f"{tmpl.get('emoji', '')} {tmpl.get('name', '')} - {fmt(r['grand_total'])}"):
            st.caption(f"📅 Dibuat: {p['date'][:16]}")
            st.markdown(f"👥 {r['num_people']} orang | 📆 {r['total_days']} hari")
            if st.button("🗑️ Hapus", key=f"del_{i}"):
                st.session_state.plans.pop(i)
                st.rerun()

def render_reminder():
    track_page("Reminder")
    st.header("⏰ Reminder Persiapan")
    
    with st.form("add_rem"):
        c1, c2 = st.columns(2)
        title = c1.text_input("Judul Reminder")
        date = c2.date_input("Tanggal", min_value=datetime.now().date())
        if st.form_submit_button("➕ Tambah Reminder"):
            if title:
                st.session_state.reminders.append({"title": title, "date": date.isoformat()})
                st.success("✅ Reminder ditambahkan!")
                st.rerun()
    
    for i, rem in enumerate(st.session_state.reminders):
        days = (datetime.fromisoformat(rem["date"]).date() - datetime.now().date()).days
        icon = "🔴" if days < 0 else "🟡" if days <= 7 else "🟢"
        status = "Lewat" if days < 0 else f"{days} hari lagi"
        st.markdown(f"{icon} **{rem['title']}** - {status}")

def render_emergency():
    track_page("Emergency")
    st.header("📞 Kontak Darurat")
    data = load_all_data()
    for c in data["emergency"]:
        st.markdown(f"📞 **{c['name']}**: `{c['phone']}`")
    
    st.divider()
    st.markdown(f"📧 **Developer:** {CONTACT['email']}")
    st.markdown(f"💬 **WhatsApp:** [{CONTACT['wa']}](https://wa.me/6281596588833)")

def render_analytics():
    track_page("Analytics")
    st.header("📊 Analytics Dashboard")
    
    if not is_admin():
        st.error("⛔ Akses ditolak - Admin only")
        return
    
    stats = db_get_visitor_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Visitors", f"{stats['total_visitors']:,}", f"+{stats['today_visitors']} today")
    c2.metric("👁️ Total Views", f"{stats['total_views']:,}", f"+{stats['today_views']} today")
    c3.metric("📊 Calculations", st.session_state.stats["calcs"])
    c4.metric("📋 Plans Saved", st.session_state.stats["plans"])
    
    st.divider()
    
    st.subheader("📄 Page Views Breakdown")
    page_stats = db_get_page_stats()
    if page_stats:
        df = pd.DataFrame([{"Page": k, "Views": v} for k, v in page_stats.items()])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📥 Export JSON"):
            st.json({"stats": stats, "pages": page_stats})
    else:
        st.info("Belum ada data page views")

def render_business_hub():
    track_page("Business Hub")
    st.header("💼 Business Hub")
    
    if not is_admin():
        st.error("⛔ Akses ditolak - Admin only")
        st.info("💡 Daftar dengan email mengandung 'admin' untuk akses penuh")
        return
    
    tabs = st.tabs(["💰 Revenue", "🤝 Partners", "📈 Growth", "⚙️ Settings"])
    
    with tabs[0]:
        st.subheader("💰 Revenue Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("💵 Revenue MTD", "Rp 0", "Setup required")
        c2.metric("📊 Transactions", "0")
        c3.metric("📈 Conversion", "0%")
        st.info("💡 **Coming Soon:** Payment gateway integration untuk booking commissions")
    
    with tabs[1]:
        st.subheader("🤝 Partner Management")
        st.dataframe(pd.DataFrame([
            {"Partner": "Travel Agent A", "Status": "🟡 Pending", "Commission": "5%"},
            {"Partner": "Travel Agent B", "Status": "🟡 Pending", "Commission": "5%"},
        ]), use_container_width=True, hide_index=True)
        st.button("➕ Tambah Partner")
    
    with tabs[2]:
        st.subheader("📈 Growth Metrics")
        stats = db_get_visitor_stats()
        
        # Milestone tracker
        milestones = [
            {"name": "🎯 1,000 Users", "target": 1000, "current": stats['total_visitors']},
            {"name": "🎯 10,000 Views", "target": 10000, "current": stats['total_views']},
        ]
        for m in milestones:
            progress = min(m['current'] / m['target'], 1.0)
            st.markdown(f"**{m['name']}** - {m['current']:,}/{m['target']:,}")
            st.progress(progress)
    
    with tabs[3]:
        st.subheader("⚙️ Platform Settings")
        st.text_input("Company Name", value="LABBAIK")
        st.text_input("Contact Email", value=CONTACT['email'])
        st.text_input("WhatsApp", value=CONTACT['wa'])
        st.button("💾 Save Settings")

def render_guide():
    track_page("Panduan Umrah")
    st.header("🕋 Panduan Umrah Lengkap")
    
    tabs = st.tabs(["📖 Rukun", "📋 Langkah", "🤲 Doa", "💡 Tips"])
    
    with tabs[0]:
        st.markdown("""
### 5 Rukun Umrah
1. **Ihram** - Niat dari miqat, memakai pakaian ihram
2. **Thawaf** - Mengelilingi Ka'bah 7 kali
3. **Sa'i** - Berjalan antara Safa-Marwa 7 kali
4. **Tahallul** - Mencukur/memotong rambut
5. **Tertib** - Melakukan urutan dengan benar
        """)
    
    with tabs[1]:
        st.markdown("""
### Langkah-langkah Umrah
1. Mandi sunnah & memakai ihram di miqat
2. Niat umrah
3. Membaca talbiyah
4. Masuk Masjidil Haram
5. Thawaf 7 putaran
6. Shalat 2 rakaat di belakang Maqam Ibrahim
7. Minum air zamzam
8. Sa'i 7 kali
9. Tahallul (potong rambut)
        """)
    
    with tabs[2]:
        st.markdown("""
### Doa-doa Penting

**Talbiyah:**
> لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ

**Doa Melihat Ka'bah:**
> اللَّهُمَّ زِدْ هَذَا الْبَيْتَ تَشْرِيفًا وَتَعْظِيمًا وَتَكْرِيمًا وَمَهَابَةً
        """)
    
    with tabs[3]:
        st.markdown("""
### Tips Penting
- 📱 Unduh aplikasi **Nusuk** untuk manajemen umrah
- 💊 Bawa obat-obatan pribadi yang cukup
- 🧴 Gunakan sunscreen SPF 50+
- 💧 Minum air minimal 2-3 liter/hari
- 👟 Pakai sandal yang nyaman
- 🔌 Bawa adaptor Type G untuk charger
        """)

def render_about():
    track_page("About")
    st.markdown(hero_html(), unsafe_allow_html=True)
    
    stats = db_get_visitor_stats()
    st.markdown(f'''<div style="background:#1A1A1A;padding:15px;border-radius:10px;margin:15px 0;text-align:center">
<span style="color:#D4AF37;font-size:1.5rem;font-weight:700">{stats['total_visitors']:,}</span> <span style="color:#888">users</span> • 
<span style="color:#D4AF37;font-size:1.5rem;font-weight:700">{stats['total_views']:,}</span> <span style="color:#888">views</span>
</div>''', unsafe_allow_html=True)
    
    st.markdown(f"""
### 👨‍💻 Developer
**MS Hadianto** | 📧 {CONTACT['email']} | 💬 [WhatsApp](https://wa.me/6281596588833)

### ✨ Fitur v{VERSION}
💰 Simulasi Biaya • 📋 Itinerary Builder • 🤝 Umrah Bareng • 🕋 Umrah Mandiri + Forum • 🤖 AI Chat Assistant • ✅ Checklist • 🗺️ Peta Interaktif • 💱 Kurs Converter • 🌤️ Info Cuaca • ⏰ Reminder • 📞 Emergency Contacts • 📊 Analytics • 💼 Business Hub

### 🔧 Tech Stack
Streamlit • Neon PostgreSQL • Python • Claude AI

### 🗄️ Database
{f"✅ Connected to Neon PostgreSQL" if db_available() else "⚠️ Database offline - using fallback"}
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
    
    # Route mapping
    routes = {
        "Beranda": render_home, "Panduan": render_guide, "Simulasi": render_simulation,
        "Budget": render_budget_finder, "Rencana": render_create_plan, "Bareng": render_umrah_bareng,
        "Mandiri": render_umrah_mandiri, "Chat": render_ai_chat, "Waktu": render_time_analysis,
        "Checklist": render_checklist, "Peta": render_map, "Kurs": render_currency,
        "Cuaca": render_weather, "Tersimpan": render_saved, "Reminder": render_reminder,
        "Emergency": render_emergency, "Analytics": render_analytics, "Business": render_business_hub,
        "Tentang": render_about,
    }
    
    protected = ["Simulasi", "Budget", "Rencana", "Bareng", "Mandiri", "Chat", "Waktu", 
                 "Checklist", "Peta", "Tersimpan", "Reminder", "Analytics", "Business"]
    
    for key, func in routes.items():
        if key in page:
            if key in protected and not logged_in():
                st.warning("🔐 Silakan login untuk mengakses fitur ini")
                render_login()
            else:
                func()
            break

if __name__ == "__main__":
    main()