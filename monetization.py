"""
💰 Monetization Module for Umrah Planner AI - Startup Edition
==============================================================
Multi-Stream Revenue: Affiliate, Lead Gen, Subscription, Marketplace, Insurance, Forex
Target: Rp 500 Juta - 2 Miliar/tahun

Developer: MS Hadianto
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random
import string

# ============================================
# CONFIGURATION - REVENUE STREAMS
# ============================================

# 1. SUBSCRIPTION TIERS
PRICING_TIERS = {
    "free": {
        "name": "Gratis",
        "price": 0,
        "price_yearly": 0,
        "features": [
            "✅ Simulasi biaya dasar",
            "✅ Perbandingan 2 skenario",
            "✅ Chat AI (5x/hari)",
            "✅ Checklist persiapan",
            "❌ Booking tiket & hotel",
            "❌ Price alert",
            "❌ Cashback rewards",
            "❌ Priority support",
        ],
        "limits": {"ai_chat_daily": 5, "scenario_compare": 2, "saved_plans": 1}
    },
    "basic": {
        "name": "Basic",
        "price": 49000,
        "price_yearly": 490000,
        "badge": "🥉",
        "features": [
            "✅ Semua fitur Gratis",
            "✅ Chat AI (50x/hari)",
            "✅ Booking tiket & hotel",
            "✅ Simpan 5 rencana",
            "✅ Diskon partner 5%",
            "❌ Price alert real-time",
            "❌ Cashback rewards",
            "❌ Priority support",
        ],
        "limits": {"ai_chat_daily": 50, "scenario_compare": -1, "saved_plans": 5}
    },
    "premium": {
        "name": "Premium",
        "price": 149000,
        "price_yearly": 1490000,
        "badge": "🥈",
        "popular": True,
        "features": [
            "✅ Semua fitur Basic",
            "✅ Chat AI Unlimited",
            "✅ Price alert real-time",
            "✅ Cashback 2% booking",
            "✅ Diskon partner 10%",
            "✅ Asuransi gratis*",
            "✅ Lounge airport disc.",
            "❌ Dedicated manager",
        ],
        "limits": {"ai_chat_daily": -1, "scenario_compare": -1, "saved_plans": -1}
    },
    "vip": {
        "name": "VIP Elite",
        "price": 499000,
        "price_yearly": 4990000,
        "badge": "👑",
        "features": [
            "✅ Semua fitur Premium",
            "✅ Dedicated manager 24/7",
            "✅ Cashback 5% semua booking",
            "✅ Free airport transfer",
            "✅ Upgrade hotel gratis*",
            "✅ Exclusive webinar",
            "✅ Group discount 15%",
            "✅ Garansi harga termurah",
        ],
        "limits": {"ai_chat_daily": -1, "scenario_compare": -1, "saved_plans": -1}
    }
}

# 2. PARTNER TRAVEL AGENTS (Affiliate Commission 3-7%)
PARTNER_AGENTS = [
    {
        "id": "patuna", "name": "PT. Patuna Mekar Jaya", "logo": "🏢",
        "commission": 5.0, "rating": 4.8, "reviews": 2847, "verified": True, "featured": True,
        "min_price": 28000000, "packages": ["ekonomis", "standard", "premium"],
        "promo": "Early Bird -10%", "quota": 50,
        "contact": {"whatsapp": "6281234567890", "website": "https://patuna.co.id"}
    },
    {
        "id": "alkhalid", "name": "PT. Al Khalid Tour", "logo": "🕌",
        "commission": 6.0, "rating": 4.7, "reviews": 1923, "verified": True, "featured": True,
        "min_price": 35000000, "packages": ["standard", "premium", "vip"],
        "promo": "Gratis Koper", "quota": 30,
        "contact": {"whatsapp": "6281234567891", "website": "https://alkhalid.co.id"}
    },
    {
        "id": "arminareka", "name": "PT. Arminareka Perdana", "logo": "⭐",
        "commission": 4.5, "rating": 4.9, "reviews": 5234, "verified": True, "featured": True,
        "min_price": 32000000, "packages": ["ekonomis", "standard", "premium", "vip"],
        "promo": "Cicilan 0%", "quota": 100,
        "contact": {"whatsapp": "6281234567892", "website": "https://arminareka.com"}
    },
    {
        "id": "maktour", "name": "PT. Maktour", "logo": "🌙",
        "commission": 7.0, "rating": 4.6, "reviews": 1456, "verified": True, "featured": False,
        "min_price": 55000000, "packages": ["premium", "vip"],
        "promo": "Upgrade Gratis", "quota": 25,
        "contact": {"whatsapp": "6281234567893", "website": "https://maktour.co.id"}
    },
    {
        "id": "ebad", "name": "PT. Ebad Al-Rahman", "logo": "☪️",
        "commission": 5.5, "rating": 4.5, "reviews": 987, "verified": True, "featured": False,
        "min_price": 25000000, "packages": ["ekonomis", "standard"],
        "promo": "Diskon Rombongan", "quota": 75,
        "contact": {"whatsapp": "6281234567894", "website": "https://ebad.co.id"}
    },
    {
        "id": "azzahra", "name": "PT. Az-Zahra Tour", "logo": "🌟",
        "commission": 6.5, "rating": 4.8, "reviews": 2156, "verified": True, "featured": True,
        "min_price": 38000000, "packages": ["standard", "premium", "vip"],
        "promo": "Bonus Zamzam 10L", "quota": 40,
        "contact": {"whatsapp": "6281234567895", "website": "https://azzahratour.com"}
    },
]

# 3. INSURANCE PRODUCTS (Commission 15-25%)
INSURANCE_PRODUCTS = [
    {
        "id": "travel_basic", "name": "Travel Basic", "provider": "Allianz",
        "price": 150000, "commission": 20, "coverage": 500000000,
        "features": ["Kecelakaan", "Sakit", "Bagasi hilang"],
        "popular": False
    },
    {
        "id": "travel_plus", "name": "Travel Plus", "provider": "AXA Mandiri",
        "price": 350000, "commission": 22, "coverage": 1000000000,
        "features": ["Kecelakaan", "Sakit", "Bagasi", "Delay", "Pembatalan"],
        "popular": True
    },
    {
        "id": "travel_premium", "name": "Travel Premium", "provider": "Prudential",
        "price": 750000, "commission": 25, "coverage": 2500000000,
        "features": ["All Risk", "Evakuasi Medis", "Repatriasi", "COVID-19", "Haji Mabrur"],
        "popular": False
    },
]

# 4. FOREX / MONEY CHANGER (Commission 0.5-1%)
FOREX_PARTNERS = [
    {"id": "vip_money", "name": "VIP Money Changer", "rate_markup": 0.5, "min_amount": 500},
    {"id": "dolarindo", "name": "Dolarindo", "rate_markup": 0.7, "min_amount": 100},
    {"id": "central_money", "name": "Central Money", "rate_markup": 0.6, "min_amount": 200},
]

# 5. TELCO / SIM CARD (Commission 10-15%)
SIMCARD_PRODUCTS = [
    {"id": "sim_saudi_7", "name": "Saudi SIM 7 Hari", "data": "5GB", "price": 150000, "commission": 15},
    {"id": "sim_saudi_14", "name": "Saudi SIM 14 Hari", "data": "10GB", "price": 250000, "commission": 15},
    {"id": "sim_saudi_30", "name": "Saudi SIM 30 Hari", "data": "20GB", "price": 400000, "commission": 12},
    {"id": "esim_global", "name": "eSIM Global", "data": "Unlimited", "price": 500000, "commission": 10},
]

# 6. AIRPORT SERVICES (Commission 10-20%)
AIRPORT_SERVICES = [
    {"id": "lounge_cgk", "name": "Lounge CGK Premium", "price": 350000, "commission": 20},
    {"id": "lounge_sub", "name": "Lounge SUB Executive", "price": 300000, "commission": 20},
    {"id": "fasttrack", "name": "Fast Track Immigration", "price": 500000, "commission": 15},
    {"id": "porter", "name": "Porter Service", "price": 100000, "commission": 25},
    {"id": "wheelchair", "name": "Wheelchair Assist", "price": 150000, "commission": 20},
]

# 7. MERCHANDISE (Margin 30-50%)
MERCHANDISE = [
    {"id": "ihram_set", "name": "Set Ihram Premium", "price": 250000, "cost": 150000, "stock": 100},
    {"id": "mukena_travel", "name": "Mukena Travel", "price": 350000, "cost": 200000, "stock": 75},
    {"id": "sajadah_portable", "name": "Sajadah Portable", "price": 150000, "cost": 80000, "stock": 150},
    {"id": "tasbih_digital", "name": "Tasbih Digital", "price": 75000, "cost": 35000, "stock": 200},
    {"id": "buku_manasik", "name": "Buku Panduan Manasik", "price": 85000, "cost": 40000, "stock": 300},
    {"id": "travel_kit", "name": "Travel Kit Umrah", "price": 450000, "cost": 250000, "stock": 50},
    {"id": "koper_umrah", "name": "Koper Umrah 24inch", "price": 850000, "cost": 500000, "stock": 30},
]

# 8. FLASH SALE CONFIG
FLASH_SALES = [
    {
        "id": "flash_ramadhan",
        "title": "🔥 Flash Sale Ramadhan",
        "discount": 15,
        "end_time": datetime(2025, 3, 1, 23, 59, 59),
        "quota": 50,
        "used": 23,
    },
]


# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_ref_code(prefix: str = "UPL", length: int = 6) -> str:
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(chars, k=length))
    return f"{prefix}-{code}"

def generate_order_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"ORD-{timestamp}-{suffix}"

def format_currency(amount: float, currency: str = "IDR") -> str:
    if currency == "IDR":
        return f"Rp {amount:,.0f}"
    return f"{amount:,.2f}"

def calculate_commission(amount: float, rate: float) -> float:
    return amount * (rate / 100)

def init_monetization_state():
    defaults = {
        "user_tier": "free",
        "user_email": None,
        "user_phone": None,
        "referral_code": None,
        "wallet_balance": 0,
        "loyalty_points": 0,
        "cart": [],
        "orders": [],
        "leads": [],
        "affiliate_clicks": [],
        "price_alerts": [],
        "show_checkout": False,
        "selected_plan": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================
# 1. SUBSCRIPTION & PRICING PAGE
# ============================================

def render_pricing_page():
    st.markdown("## 💎 Pilih Paket Berlangganan")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Users", "12,847")
    with col2:
        st.metric("⭐ Premium Users", "2,156")
    with col3:
        st.metric("💰 Savings", "Rp 2.8M")
    with col4:
        st.metric("🎯 Satisfaction", "98.5%")
    
    st.markdown("---")
    
    billing = st.radio("Periode", ["Bulanan", "Tahunan (Hemat 17%)"], horizontal=True)
    is_yearly = "Tahunan" in billing
    
    cols = st.columns(4)
    for i, (tier_id, tier) in enumerate(PRICING_TIERS.items()):
        with cols[i]:
            if tier.get("popular"):
                st.markdown('<div style="background:#ff6b6b;color:white;text-align:center;padding:5px;border-radius:5px 5px 0 0;font-weight:bold;font-size:0.8rem;">🔥 POPULER</div>', unsafe_allow_html=True)
            
            price = tier["price_yearly"] / 12 if is_yearly else tier["price"]
            badge = tier.get("badge", "")
            
            st.markdown(f"""
            <div style="border:{'3px solid #ff6b6b' if tier.get('popular') else '1px solid #ddd'};border-radius:{'0 0 10px 10px' if tier.get('popular') else '10px'};padding:1rem;text-align:center;background:white;">
                <h3>{badge} {tier['name']}</h3>
                <h2 style="color:#1e88e5;">{format_currency(price)}</h2>
                <p style="color:#888;font-size:0.8rem;">/bulan</p>
            </div>
            """, unsafe_allow_html=True)
            
            for feature in tier["features"][:5]:
                st.caption(feature)
            
            if tier_id == "free":
                st.button("✅ Paket Saat Ini", key=f"btn_{tier_id}", disabled=True, use_container_width=True)
            else:
                if st.button(f"Pilih {tier['name']}", key=f"btn_{tier_id}", type="primary" if tier.get("popular") else "secondary", use_container_width=True):
                    st.session_state.selected_plan = tier_id
                    st.session_state.show_checkout = True
                    st.rerun()
    
    if st.session_state.get("show_checkout"):
        render_checkout_modal()


def render_checkout_modal():
    plan_id = st.session_state.get("selected_plan", "basic")
    plan = PRICING_TIERS.get(plan_id)
    
    st.markdown("---")
    st.markdown(f"### 🛒 Checkout - Paket {plan['name']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Data Pelanggan")
        name = st.text_input("Nama Lengkap *")
        email = st.text_input("Email *")
        phone = st.text_input("WhatsApp *", placeholder="08xxx")
        promo = st.text_input("Kode Promo")
        
        discount = 0
        if promo:
            if promo.upper() in ["UMRAH2024", "HEMAT20"]:
                discount = 0.2
                st.success("✅ Diskon 20%!")
            elif promo.upper() == "WELCOME10":
                discount = 0.1
                st.success("✅ Diskon 10%!")
            else:
                st.error("❌ Kode tidak valid")
    
    with col2:
        st.markdown("#### 💳 Pembayaran")
        payment = st.radio("Metode", ["🏦 Transfer Bank", "📱 E-Wallet", "💳 Kartu Kredit", "🏪 Minimarket"])
        
        subtotal = plan["price"]
        disc_amount = subtotal * discount
        total = subtotal - disc_amount
        
        st.markdown(f"""
        | Item | Harga |
        |------|-------|
        | Paket {plan['name']} | {format_currency(subtotal)} |
        | Diskon | -{format_currency(disc_amount)} |
        | **Total** | **{format_currency(total)}** |
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Batal", use_container_width=True):
            st.session_state.show_checkout = False
            st.rerun()
    with col2:
        if st.button("✅ Bayar", type="primary", use_container_width=True):
            if name and email and phone:
                order_id = generate_order_id()
                st.success(f"🎉 Berhasil! Order: {order_id}")
                st.session_state.user_tier = plan_id
                st.session_state.show_checkout = False
                st.balloons()
            else:
                st.error("Lengkapi data!")


# ============================================
# 2. LEAD GENERATION
# ============================================

def render_lead_capture():
    st.markdown("## 📝 Dapatkan Penawaran Terbaik")
    
    st.markdown("""
    <div style="background:linear-gradient(90deg,#ff6b6b,#ee5a5a);color:white;padding:1rem;border-radius:10px;text-align:center;margin-bottom:1rem;">
        🔥 <strong>PROMO TERBATAS!</strong> Booking minggu ini dapat DISKON 10% + Gratis Koper!
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
            phone = st.text_input("WhatsApp *", placeholder="08xxx")
            city = st.selectbox("Kota Keberangkatan", 
                ["Jakarta", "Surabaya", "Medan", "Makassar", "Bandung", "Semarang", "Yogyakarta", "Lainnya"])
        
        with col2:
            package = st.selectbox("Tipe Paket", 
                ["💰 Ekonomis (Rp 25-32 Jt)", "⭐ Standard (Rp 35-45 Jt)", "👑 Premium (Rp 50-75 Jt)", "🌟 VIP (Rp 80 Jt+)"])
            num_pax = st.number_input("Jumlah Jamaah", 1, 50, 1)
            month = st.selectbox("Bulan Keberangkatan", 
                ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember", "Belum Pasti"])
            budget = st.text_input("Budget (opsional)", placeholder="Rp 35.000.000")
        
        notes = st.text_area("Catatan", placeholder="Misal: ada lansia, butuh wheelchair")
        agree = st.checkbox("Saya setuju dihubungi travel agent partner")
        
        if st.form_submit_button("📤 Kirim & Dapatkan Penawaran", type="primary", use_container_width=True):
            if name and email and phone and agree:
                lead_id = generate_ref_code("LEAD")
                st.session_state.leads.append({
                    "id": lead_id, "name": name, "email": email, "phone": phone,
                    "city": city, "package": package, "num_pax": num_pax,
                    "month": month, "timestamp": datetime.now().isoformat()
                })
                
                st.success(f"🎉 Terima kasih {name}! Lead ID: **{lead_id}**")
                st.markdown("### 🏆 Partner Terpilih")
                for p in PARTNER_AGENTS[:3]:
                    st.markdown(f"**{p['logo']} {p['name']}** - ⭐ {p['rating']} - {p['promo']}")
            else:
                st.error("Lengkapi field wajib dan centang persetujuan")


# ============================================
# 3. MARKETPLACE
# ============================================

def render_marketplace():
    st.markdown("## 🏪 Marketplace Travel Agent")
    
    for sale in FLASH_SALES:
        if datetime.now() < sale["end_time"]:
            remaining = sale["end_time"] - datetime.now()
            hours = int(remaining.total_seconds() // 3600)
            st.markdown(f"""
            <div style="background:linear-gradient(90deg,#ff416c,#ff4b2b);color:white;padding:1rem;border-radius:10px;margin-bottom:1rem;">
                <h4 style="margin:0;">{sale['title']}</h4>
                <p style="margin:0;">Diskon {sale['discount']}% • Sisa {sale['quota'] - sale['used']} kuota • ⏰ {hours} jam</p>
            </div>
            """, unsafe_allow_html=True)
            break
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_pkg = st.multiselect("Tipe Paket", ["ekonomis", "standard", "premium", "vip"], default=["ekonomis", "standard", "premium", "vip"])
    with col2:
        sort_by = st.selectbox("Urutkan", ["Rating Tertinggi", "Harga Terendah", "Review Terbanyak"])
    with col3:
        verified_only = st.checkbox("Verified Only ✅", True)
    
    st.markdown("---")
    
    partners = PARTNER_AGENTS.copy()
    if verified_only:
        partners = [p for p in partners if p["verified"]]
    partners = [p for p in partners if any(pkg in p["packages"] for pkg in filter_pkg)]
    
    if sort_by == "Rating Tertinggi":
        partners.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "Harga Terendah":
        partners.sort(key=lambda x: x["min_price"])
    else:
        partners.sort(key=lambda x: x["reviews"], reverse=True)
    
    for p in partners:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            featured = "🏆 " if p["featured"] else ""
            st.markdown(f"### {p['logo']} {p['name']}\n{featured}{'✅' if p['verified'] else ''}\n\n⭐ **{p['rating']}** • {p['reviews']:,} reviews")
        
        with col2:
            st.markdown(f"**Mulai dari:**\n### {format_currency(p['min_price'])}\n\n🎁 {p['promo']}")
        
        with col3:
            st.markdown("**Paket:** " + ", ".join(p["packages"]))
            st.caption(f"📦 Kuota: {p['quota']} seat")
        
        with col4:
            ref_code = generate_ref_code(f"AFF-{p['id'][:3].upper()}")
            wa_link = f"https://wa.me/{p['contact']['whatsapp']}?text=Halo%20dari%20Umrah%20Planner%20AI%20(Ref:{ref_code})"
            
            st.markdown(f'<a href="{wa_link}" target="_blank" style="display:block;background:#25D366;color:white;padding:10px;border-radius:5px;text-align:center;text-decoration:none;">💬 WhatsApp</a>', unsafe_allow_html=True)
            
            if st.button(f"📋 Detail", key=f"d_{p['id']}", use_container_width=True):
                st.session_state.affiliate_clicks.append({"partner": p["id"], "ref": ref_code, "time": datetime.now().isoformat()})
                st.info(f"💰 Komisi: {format_currency(p['min_price'] * p['commission'] / 100)}")
        
        st.markdown("---")


# ============================================
# 4. INSURANCE
# ============================================

def render_insurance():
    st.markdown("## 🛡️ Asuransi Perjalanan")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### 🏥\n**Biaya Medis**\nHingga Rp 2.5M")
    with col2:
        st.markdown("### 🧳\n**Bagasi Hilang**\nHingga Rp 50 Jt")
    with col3:
        st.markdown("### ✈️\n**Delay/Cancel**\nHingga Rp 25 Jt")
    with col4:
        st.markdown("### 🚑\n**Evakuasi**\n24/7 Worldwide")
    
    st.markdown("---")
    
    cols = st.columns(3)
    for i, ins in enumerate(INSURANCE_PRODUCTS):
        with cols[i]:
            popular = '<span style="background:#ff6b6b;color:white;padding:2px 8px;border-radius:10px;font-size:0.7rem;">POPULER</span>' if ins["popular"] else ""
            
            st.markdown(f"""
            <div style="border:{'2px solid #ff6b6b' if ins['popular'] else '1px solid #ddd'};border-radius:10px;padding:1rem;">
                <h4>{ins['name']} {popular}</h4>
                <p style="color:#888;">{ins['provider']}</p>
                <h3 style="color:#1e88e5;">{format_currency(ins['price'])}</h3>
                <p>Coverage: {format_currency(ins['coverage'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            for f in ins["features"]:
                st.caption(f"✅ {f}")
            
            if st.button(f"Beli", key=f"ins_{ins['id']}", use_container_width=True, type="primary" if ins["popular"] else "secondary"):
                st.session_state.cart.append({"type": "insurance", "product": ins, "qty": 1})
                st.success(f"✅ Ditambahkan! Komisi: {format_currency(ins['price'] * ins['commission'] / 100)}")


# ============================================
# 5. FOREX
# ============================================

def render_forex():
    st.markdown("## 💱 Tukar Mata Uang")
    
    base_rate = 4150
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background:#e3f2fd;padding:1rem;border-radius:10px;">
            <h2>1 SAR = Rp {base_rate:,}</h2>
            <p style="color:green;">▲ +15 dari kemarin</p>
        </div>
        """, unsafe_allow_html=True)
        
        amount_sar = st.number_input("Jumlah SAR", 100, 10000, 1000, 100)
    
    with col2:
        st.markdown("### Pilih Money Changer")
        
        for fx in FOREX_PARTNERS:
            rate = base_rate * (1 + fx["rate_markup"] / 100)
            total_idr = amount_sar * rate
            
            st.markdown(f"""
            <div style="border:1px solid #ddd;padding:0.75rem;border-radius:10px;margin-bottom:0.5rem;">
                <strong>{fx['name']}</strong> • Rate: Rp {rate:,.0f}/SAR<br>
                Total: <strong>{format_currency(total_idr)}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Tukar", key=f"fx_{fx['id']}", use_container_width=True):
                st.success(f"✅ {amount_sar} SAR = {format_currency(total_idr)}")


# ============================================
# 6. SIM CARD
# ============================================

def render_simcard():
    st.markdown("## 📱 SIM Card Saudi Arabia")
    
    cols = st.columns(4)
    for i, sim in enumerate(SIMCARD_PRODUCTS):
        with cols[i]:
            st.markdown(f"""
            <div style="border:1px solid #ddd;border-radius:10px;padding:1rem;text-align:center;">
                <h4>{sim['name']}</h4>
                <h3>📶 {sim['data']}</h3>
                <h3 style="color:#1e88e5;">{format_currency(sim['price'])}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Beli", key=f"sim_{sim['id']}", use_container_width=True):
                st.session_state.cart.append({"type": "simcard", "product": sim, "qty": 1})
                st.success("✅ Ditambahkan!")


# ============================================
# 7. AIRPORT SERVICES
# ============================================

def render_airport_services():
    st.markdown("## ✈️ Layanan Bandara")
    
    cols = st.columns(5)
    for i, svc in enumerate(AIRPORT_SERVICES):
        with cols[i]:
            st.markdown(f"""
            <div style="border:1px solid #ddd;border-radius:10px;padding:1rem;text-align:center;">
                <h5>{svc['name']}</h5>
                <h4 style="color:#1e88e5;">{format_currency(svc['price'])}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Pesan", key=f"apt_{svc['id']}", use_container_width=True):
                st.session_state.cart.append({"type": "airport", "product": svc, "qty": 1})
                st.success("✅ Ditambahkan!")


# ============================================
# 8. MERCHANDISE
# ============================================

def render_merchandise():
    st.markdown("## 🛍️ Toko Perlengkapan Umrah")
    
    cols = st.columns(4)
    for i, item in enumerate(MERCHANDISE):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="border:1px solid #ddd;border-radius:10px;padding:1rem;">
                <h4>{item['name']}</h4>
                <h3 style="color:#1e88e5;">{format_currency(item['price'])}</h3>
                <small>Stok: {item['stock']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            qty = st.number_input("Qty", 1, item["stock"], 1, key=f"qty_{item['id']}")
            
            if st.button(f"🛒 Beli", key=f"m_{item['id']}", use_container_width=True):
                st.session_state.cart.append({"type": "merchandise", "product": item, "qty": qty})
                profit = (item["price"] - item["cost"]) * qty
                st.success(f"✅ Margin: {format_currency(profit)}")


# ============================================
# 9. REFERRAL
# ============================================

def render_referral():
    st.markdown("## 🎁 Program Referral")
    st.markdown("Ajak teman, dapat **Rp 500.000** per booking!")
    
    if not st.session_state.referral_code:
        st.session_state.referral_code = generate_ref_code("REF")
    
    ref_code = st.session_state.referral_code
    ref_link = f"https://umrah-planner-by-mshadianto.streamlit.app?ref={ref_code}"
    
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:2rem;border-radius:15px;text-align:center;">
        <h3>Kode Referral</h3>
        <h1 style="font-family:monospace;letter-spacing:5px;">{ref_code}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.code(ref_link)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"[📱 WhatsApp](https://wa.me/?text=Cek%20Umrah%20Planner!%20Kode:{ref_code})")
    with col2:
        st.markdown(f"[📘 Facebook](https://facebook.com/sharer/sharer.php?u={ref_link})")
    with col3:
        st.markdown(f"[🐦 Twitter](https://twitter.com/intent/tweet?url={ref_link})")
    
    st.markdown("---")
    
    rewards = [
        {"refs": 1, "reward": "Rp 500K", "bonus": ""},
        {"refs": 5, "reward": "Rp 3 Jt", "bonus": "+ Premium 3 Bln"},
        {"refs": 10, "reward": "Rp 7.5 Jt", "bonus": "+ iPhone 15"},
        {"refs": 25, "reward": "Rp 25 Jt", "bonus": "+ Umrah GRATIS!"},
    ]
    
    cols = st.columns(4)
    for i, r in enumerate(rewards):
        with cols[i]:
            st.markdown(f"""
            <div style="background:#f8f9fa;padding:1rem;border-radius:10px;text-align:center;">
                <h4>{r['refs']} Referral</h4>
                <h3 style="color:#4caf50;">{r['reward']}</h3>
                <small>{r['bonus']}</small>
            </div>
            """, unsafe_allow_html=True)


# ============================================
# 10. B2B
# ============================================

def render_b2b():
    st.markdown("## 🏢 Kemitraan B2B / White Label")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div style="background:#e3f2fd;padding:1.5rem;border-radius:10px;text-align:center;"><h1>🏷️</h1><h4>White Label</h4></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background:#e8f5e9;padding:1.5rem;border-radius:10px;text-align:center;"><h1>🔌</h1><h4>API Access</h4></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background:#fff3e0;padding:1.5rem;border-radius:10px;text-align:center;"><h1>📊</h1><h4>Dashboard</h4></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    plans = [
        {"name": "Starter", "price": "Rp 2.5 Jt/bln", "features": ["100 leads/bln", "White label basic"]},
        {"name": "Growth", "price": "Rp 7.5 Jt/bln", "features": ["Unlimited leads", "API access", "Priority support"]},
        {"name": "Enterprise", "price": "Custom", "features": ["Dedicated server", "Custom dev", "SLA 99.9%"]},
    ]
    
    cols = st.columns(3)
    for i, plan in enumerate(plans):
        with cols[i]:
            st.markdown(f"""
            <div style="border:1px solid #ddd;border-radius:10px;padding:1.5rem;text-align:center;">
                <h3>{plan['name']}</h3>
                <h2 style="color:#1e88e5;">{plan['price']}</h2>
            </div>
            """, unsafe_allow_html=True)
            for f in plan["features"]:
                st.caption(f"✅ {f}")
            st.button(f"Hubungi Sales", key=f"b2b_{plan['name']}", use_container_width=True)


# ============================================
# 11. CART
# ============================================

def render_cart():
    st.markdown("## 🛒 Keranjang Belanja")
    
    cart = st.session_state.cart
    
    if not cart:
        st.info("Keranjang kosong")
        return
    
    total = 0
    total_comm = 0
    
    for i, item in enumerate(cart):
        product = item["product"]
        qty = item["qty"]
        subtotal = product["price"] * qty
        total += subtotal
        
        if item["type"] == "insurance":
            comm = subtotal * product["commission"] / 100
        elif item["type"] == "merchandise":
            comm = (product["price"] - product["cost"]) * qty
        else:
            comm = subtotal * product.get("commission", 15) / 100
        total_comm += comm
        
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"**{product['name']}**")
        with col2:
            st.markdown(f"x{qty}")
        with col3:
            st.markdown(format_currency(subtotal))
        with col4:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
    
    st.markdown("---")
    st.markdown(f"### Total: {format_currency(total)}")
    st.caption(f"💰 Komisi/Margin: {format_currency(total_comm)}")
    
    if st.button("✅ Checkout", type="primary", use_container_width=True):
        order_id = generate_order_id()
        st.session_state.orders.append({
            "id": order_id, "items": cart.copy(), "total": total,
            "commission": total_comm, "timestamp": datetime.now().isoformat()
        })
        st.session_state.cart = []
        st.success(f"🎉 Order: {order_id}")
        st.balloons()


# ============================================
# 12. DASHBOARD
# ============================================

def render_revenue_dashboard():
    st.markdown("## 📊 Dashboard Revenue")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Revenue MTD", "Rp 45.8 Jt", "+12%")
    with col2:
        st.metric("📝 Leads", f"{len(st.session_state.leads)}", "+5")
    with col3:
        st.metric("🛒 Orders", f"{len(st.session_state.orders)}", "+3")
    with col4:
        st.metric("🔗 Clicks", f"{len(st.session_state.affiliate_clicks)}", "+15")
    
    st.markdown("---")
    st.markdown("### 💵 Revenue Breakdown")
    
    import pandas as pd
    data = {
        "Stream": ["Lead Gen", "Affiliate", "Insurance", "Forex", "SIM Card", "Airport", "Merchandise", "Subscription"],
        "Revenue (Rp Jt)": [15, 12, 8, 3, 2.5, 2, 1.8, 1.5],
        "Target (Rp Jt)": [20, 15, 10, 5, 3, 3, 2.5, 2],
    }
    df = pd.DataFrame(data)
    df["Achievement %"] = (df["Revenue (Rp Jt)"] / df["Target (Rp Jt)"] * 100).round(0)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📈 Proyeksi Tahunan")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        | Stream | Potensi/Tahun |
        |--------|---------------|
        | Lead Generation | Rp 180 - 360 Jt |
        | Affiliate Commission | Rp 150 - 300 Jt |
        | Insurance | Rp 100 - 200 Jt |
        | Subscription | Rp 50 - 100 Jt |
        | Merchandise | Rp 30 - 60 Jt |
        | Lainnya | Rp 40 - 80 Jt |
        | **TOTAL** | **Rp 550 Jt - 1.1 M** |
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Key Metrics Target
        - **MAU:** 50,000 users
        - **Conversion:** 3-5%
        - **ARPU:** Rp 25,000
        - **CAC:** Rp 15,000
        - **LTV:** Rp 150,000
        """)


# ============================================
# MAIN RENDER
# ============================================

def render_monetization_page():
    init_monetization_state()
    
    st.markdown("## 💼 Business Hub")
    
    menu = st.selectbox("Menu", [
        "📊 Dashboard Revenue",
        "💎 Subscription",
        "📝 Lead Generation",
        "🏪 Marketplace Travel",
        "🛡️ Asuransi",
        "💱 Forex",
        "📱 SIM Card",
        "✈️ Layanan Bandara",
        "🛍️ Merchandise",
        "🎁 Referral",
        "🏢 B2B White Label",
        "🛒 Keranjang",
    ])
    
    st.markdown("---")
    
    if "Dashboard" in menu:
        render_revenue_dashboard()
    elif "Subscription" in menu:
        render_pricing_page()
    elif "Lead" in menu:
        render_lead_capture()
    elif "Marketplace" in menu:
        render_marketplace()
    elif "Asuransi" in menu:
        render_insurance()
    elif "Forex" in menu:
        render_forex()
    elif "SIM" in menu:
        render_simcard()
    elif "Bandara" in menu:
        render_airport_services()
    elif "Merchandise" in menu:
        render_merchandise()
    elif "Referral" in menu:
        render_referral()
    elif "B2B" in menu:
        render_b2b()
    elif "Keranjang" in menu:
        render_cart()


def render_monetization_sidebar():
    tier = st.session_state.get("user_tier", "free")
    tier_info = PRICING_TIERS.get(tier, {})
    
    if tier == "free":
        st.markdown("""
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:0.75rem;border-radius:10px;color:white;text-align:center;">
            <small>🔓 Upgrade Premium</small><br>
            <small>Diskon 20%: UMRAH2024</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background:#e8f5e9;padding:0.75rem;border-radius:10px;text-align:center;">{tier_info.get("badge", "")} <strong>{tier_info.get("name", "")}</strong></div>', unsafe_allow_html=True)


def render_quick_quote_widget():
    st.markdown('<div style="background:linear-gradient(135deg,#11998e,#38ef7d);padding:0.75rem;border-radius:10px;color:white;text-align:center;"><small>💬 Konsultasi GRATIS</small></div>', unsafe_allow_html=True)
    
    with st.form("quick_quote", clear_on_submit=True):
        phone = st.text_input("WhatsApp", placeholder="08xxx", label_visibility="collapsed")
        if st.form_submit_button("📞 Hubungi", use_container_width=True):
            if phone:
                st.success("✅ Akan dihubungi!")
            else:
                st.error("Isi nomor")
