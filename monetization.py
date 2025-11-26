"""
Monetization Module for Umrah Planner AI
=========================================
Revenue Streams: Affiliate, Lead Generation, Premium Subscription, B2B
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import hashlib
import random
import string

# ============================================
# CONFIGURATION
# ============================================

PRICING_TIERS = {
    "free": {
        "name": "Gratis",
        "price": 0,
        "price_yearly": 0,
        "features": [
            "✅ Simulasi biaya dasar",
            "✅ Perbandingan 2 skenario",
            "✅ Chat AI (5 pertanyaan/hari)",
            "✅ Checklist persiapan",
            "✅ Konverter mata uang",
            "❌ Pencarian tiket & hotel",
            "❌ Konsultan AI personal",
            "❌ Price alert",
            "❌ Dokumen management",
            "❌ Priority support",
        ],
        "limits": {
            "ai_chat_daily": 5,
            "scenario_compare": 2,
            "saved_plans": 1,
        }
    },
    "basic": {
        "name": "Basic",
        "price": 49000,
        "price_yearly": 490000,
        "badge": "🥉",
        "features": [
            "✅ Semua fitur Gratis",
            "✅ Chat AI unlimited",
            "✅ Perbandingan semua skenario",
            "✅ Pencarian tiket pesawat",
            "✅ Pencarian hotel",
            "✅ Simpan 5 rencana",
            "❌ Konsultan AI personal",
            "❌ Price alert real-time",
            "❌ Dokumen management",
            "❌ Priority support",
        ],
        "limits": {
            "ai_chat_daily": -1,  # unlimited
            "scenario_compare": -1,
            "saved_plans": 5,
        }
    },
    "premium": {
        "name": "Premium",
        "price": 149000,
        "price_yearly": 1490000,
        "badge": "🥈",
        "popular": True,
        "features": [
            "✅ Semua fitur Basic",
            "✅ Konsultan AI personal 24/7",
            "✅ Price alert real-time",
            "✅ Exclusive deals dari partner",
            "✅ Simpan unlimited rencana",
            "✅ Export PDF itinerary",
            "✅ Dokumen management",
            "❌ Dedicated account manager",
            "❌ Group booking discount",
        ],
        "limits": {
            "ai_chat_daily": -1,
            "scenario_compare": -1,
            "saved_plans": -1,
        }
    },
    "vip": {
        "name": "VIP",
        "price": 499000,
        "price_yearly": 4990000,
        "badge": "🥇",
        "features": [
            "✅ Semua fitur Premium",
            "✅ Dedicated account manager",
            "✅ Group booking discount 10%",
            "✅ Priority customer support",
            "✅ Akses webinar eksklusif",
            "✅ Konsultasi 1-on-1 (2x/bulan)",
            "✅ Early access fitur baru",
            "✅ Cashback program",
        ],
        "limits": {
            "ai_chat_daily": -1,
            "scenario_compare": -1,
            "saved_plans": -1,
        }
    }
}

# Partner Travel Agents (Affiliate)
PARTNER_AGENTS = [
    {
        "id": "patuna",
        "name": "PT. Patuna Mekar Jaya",
        "logo": "🏢",
        "commission": 3.5,  # percent
        "rating": 4.8,
        "reviews": 2500,
        "verified": True,
        "featured": True,
        "packages": ["ekonomis", "standard", "premium"],
        "contact": {
            "phone": "+62-21-7654321",
            "whatsapp": "6281234567890",
            "website": "https://patuna.co.id"
        }
    },
    {
        "id": "alkhalid",
        "name": "PT. Al Khalid Tour",
        "logo": "🕌",
        "commission": 4.0,
        "rating": 4.7,
        "reviews": 1800,
        "verified": True,
        "featured": True,
        "packages": ["standard", "premium", "vip"],
        "contact": {
            "phone": "+62-21-8765432",
            "whatsapp": "6281234567891",
            "website": "https://alkhalid.co.id"
        }
    },
    {
        "id": "arminareka",
        "name": "PT. Arminareka Perdana",
        "logo": "⭐",
        "commission": 3.0,
        "rating": 4.9,
        "reviews": 5000,
        "verified": True,
        "featured": True,
        "packages": ["ekonomis", "standard", "premium", "vip"],
        "contact": {
            "phone": "+62-21-9876543",
            "whatsapp": "6281234567892",
            "website": "https://arminareka.com"
        }
    },
    {
        "id": "maktour",
        "name": "PT. Maktour",
        "logo": "🌙",
        "commission": 5.0,
        "rating": 4.6,
        "reviews": 1200,
        "verified": True,
        "featured": False,
        "packages": ["premium", "vip"],
        "contact": {
            "phone": "+62-21-1234567",
            "whatsapp": "6281234567893",
            "website": "https://maktour.co.id"
        }
    },
    {
        "id": "ebad",
        "name": "PT. Ebad Al-Rahman",
        "logo": "☪️",
        "commission": 3.5,
        "rating": 4.5,
        "reviews": 900,
        "verified": True,
        "featured": False,
        "packages": ["ekonomis", "standard"],
        "contact": {
            "phone": "+62-21-2345678",
            "whatsapp": "6281234567894",
            "website": "https://ebad.co.id"
        }
    }
]

# Advertisement Slots
AD_SLOTS = {
    "banner_top": {
        "size": "728x90",
        "price_monthly": 5000000,
        "position": "Top of page"
    },
    "sidebar": {
        "size": "300x250",
        "price_monthly": 3000000,
        "position": "Sidebar"
    },
    "in_content": {
        "size": "468x60",
        "price_monthly": 2000000,
        "position": "Between content"
    },
    "popup": {
        "size": "500x400",
        "price_monthly": 7000000,
        "position": "Modal popup"
    }
}


# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_ref_code(length: int = 8) -> str:
    """Generate unique referral code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_lead_id() -> str:
    """Generate unique lead ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"LEAD-{timestamp}-{random_suffix}"


def calculate_commission(package_price: float, commission_rate: float) -> float:
    """Calculate affiliate commission"""
    return package_price * (commission_rate / 100)


def format_price(amount: float) -> str:
    """Format price to Indonesian Rupiah"""
    return f"Rp {amount:,.0f}"


# ============================================
# SESSION STATE MANAGEMENT
# ============================================

def init_monetization_state():
    """Initialize monetization session state"""
    if "user_tier" not in st.session_state:
        st.session_state.user_tier = "free"
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "referral_code" not in st.session_state:
        st.session_state.referral_code = None
    if "leads_generated" not in st.session_state:
        st.session_state.leads_generated = []
    if "affiliate_clicks" not in st.session_state:
        st.session_state.affiliate_clicks = []
    if "saved_plans" not in st.session_state:
        st.session_state.saved_plans = []
    if "price_alerts" not in st.session_state:
        st.session_state.price_alerts = []


# ============================================
# 1. SUBSCRIPTION & PRICING
# ============================================

def render_pricing_page():
    """Render subscription pricing page"""
    st.markdown("### 💎 Pilih Paket Berlangganan")
    st.markdown("Tingkatkan pengalaman perencanaan umrah Anda")
    
    # Billing toggle
    billing = st.radio(
        "Periode Pembayaran",
        options=["Bulanan", "Tahunan (Hemat 17%)"],
        horizontal=True
    )
    is_yearly = "Tahunan" in billing
    
    st.markdown("---")
    
    # Pricing cards
    cols = st.columns(4)
    
    for i, (tier_id, tier) in enumerate(PRICING_TIERS.items()):
        with cols[i]:
            # Popular badge
            if tier.get("popular"):
                st.markdown("""
                <div style="
                    background: linear-gradient(90deg, #ff6b6b, #ee5a5a);
                    color: white;
                    text-align: center;
                    padding: 5px;
                    border-radius: 5px 5px 0 0;
                    font-weight: bold;
                    font-size: 0.8rem;
                ">🔥 PALING POPULER</div>
                """, unsafe_allow_html=True)
            
            # Card
            price = tier["price_yearly"] if is_yearly else tier["price"]
            monthly_price = tier["price_yearly"] / 12 if is_yearly else tier["price"]
            
            badge = tier.get("badge", "")
            
            st.markdown(f"""
            <div style="
                border: {'3px solid #ff6b6b' if tier.get('popular') else '1px solid #ddd'};
                border-radius: {'0 0 10px 10px' if tier.get('popular') else '10px'};
                padding: 1.5rem;
                text-align: center;
                background: white;
                min-height: 450px;
            ">
                <h3>{badge} {tier['name']}</h3>
                <h2 style="color: #1e88e5; margin: 0.5rem 0;">
                    {format_price(monthly_price)}
                </h2>
                <p style="color: #888; font-size: 0.85rem;">per bulan</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Features list
            for feature in tier["features"][:6]:
                st.markdown(f"<small>{feature}</small>", unsafe_allow_html=True)
            
            if len(tier["features"]) > 6:
                with st.expander("Lihat semua fitur"):
                    for feature in tier["features"][6:]:
                        st.markdown(f"<small>{feature}</small>", unsafe_allow_html=True)
            
            # CTA Button
            if tier_id == "free":
                if st.session_state.user_tier == "free":
                    st.button("✅ Paket Saat Ini", key=f"btn_{tier_id}", disabled=True)
                else:
                    st.button("Downgrade", key=f"btn_{tier_id}")
            else:
                if st.session_state.user_tier == tier_id:
                    st.button("✅ Aktif", key=f"btn_{tier_id}", disabled=True)
                else:
                    if st.button(f"Pilih {tier['name']}", key=f"btn_{tier_id}", type="primary" if tier.get("popular") else "secondary"):
                        st.session_state.selected_plan = tier_id
                        st.session_state.show_checkout = True
    
    # Checkout modal
    if st.session_state.get("show_checkout"):
        render_checkout_modal()
    
    # FAQ
    st.markdown("---")
    st.markdown("### ❓ FAQ")
    
    with st.expander("Bagaimana cara berlangganan?"):
        st.markdown("""
        1. Pilih paket yang sesuai
        2. Masukkan email dan data pembayaran
        3. Pilih metode pembayaran (Transfer, E-Wallet, Kartu Kredit)
        4. Konfirmasi pembayaran
        5. Akses premium langsung aktif!
        """)
    
    with st.expander("Apakah bisa refund?"):
        st.markdown("""
        Ya! Kami menyediakan garansi **7 hari uang kembali** tanpa syarat.
        Hubungi customer service kami untuk proses refund.
        """)
    
    with st.expander("Bagaimana jika ingin upgrade/downgrade?"):
        st.markdown("""
        Anda bisa upgrade kapan saja dan hanya membayar selisih prorata.
        Untuk downgrade, perubahan akan berlaku di periode billing berikutnya.
        """)


def render_checkout_modal():
    """Render checkout modal"""
    plan_id = st.session_state.get("selected_plan", "basic")
    plan = PRICING_TIERS.get(plan_id, PRICING_TIERS["basic"])
    
    st.markdown("---")
    st.markdown(f"### 🛒 Checkout - Paket {plan['name']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Data Pelanggan")
        name = st.text_input("Nama Lengkap", key="checkout_name")
        email = st.text_input("Email", key="checkout_email")
        phone = st.text_input("No. WhatsApp", key="checkout_phone", placeholder="08xxxxxxxxxx")
        
        promo_code = st.text_input("Kode Promo (opsional)", key="promo_code")
        if promo_code:
            if promo_code.upper() == "UMRAH2024":
                st.success("✅ Kode promo valid! Diskon 20%")
            else:
                st.error("❌ Kode promo tidak valid")
    
    with col2:
        st.markdown("#### 💳 Metode Pembayaran")
        
        payment_method = st.radio(
            "Pilih metode",
            options=[
                "🏦 Transfer Bank (BCA, Mandiri, BNI, BRI)",
                "📱 E-Wallet (GoPay, OVO, DANA, ShopeePay)",
                "💳 Kartu Kredit/Debit",
                "🏪 Minimarket (Indomaret, Alfamart)"
            ]
        )
        
        # Order summary
        st.markdown("#### 📋 Ringkasan Order")
        
        discount = 0.2 if promo_code and promo_code.upper() == "UMRAH2024" else 0
        subtotal = plan["price"]
        discount_amount = subtotal * discount
        total = subtotal - discount_amount
        
        st.markdown(f"""
        | Item | Harga |
        |------|-------|
        | Paket {plan['name']} | {format_price(subtotal)} |
        | Diskon | -{format_price(discount_amount)} |
        | **Total** | **{format_price(total)}** |
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Batal", use_container_width=True):
            st.session_state.show_checkout = False
            st.rerun()
    
    with col2:
        if st.button("✅ Bayar Sekarang", type="primary", use_container_width=True):
            if name and email and phone:
                st.success("🎉 Pembayaran berhasil diproses!")
                st.session_state.user_tier = plan_id
                st.session_state.user_email = email
                st.session_state.show_checkout = False
                st.balloons()
            else:
                st.error("Mohon lengkapi semua data")


# ============================================
# 2. LEAD GENERATION
# ============================================

def render_lead_capture_form(context: str = "general"):
    """Render lead capture form"""
    st.markdown("### 📝 Dapatkan Penawaran Terbaik")
    st.markdown("Isi form berikut dan travel agent terpercaya akan menghubungi Anda")
    
    with st.form(f"lead_form_{context}"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
            phone = st.text_input("No. WhatsApp *", placeholder="08xxxxxxxxxx")
            city = st.selectbox(
                "Kota Keberangkatan",
                ["Jakarta", "Surabaya", "Medan", "Makassar", "Bandung", 
                 "Semarang", "Yogyakarta", "Denpasar", "Lainnya"]
            )
        
        with col2:
            package_type = st.selectbox(
                "Tipe Paket Yang Diminati",
                ["Ekonomis (Rp 25-32 Juta)", "Standard (Rp 35-45 Juta)",
                 "Premium (Rp 55-85 Juta)", "VIP (Rp 100+ Juta)"]
            )
            
            num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=1)
            
            travel_month = st.selectbox(
                "Rencana Bulan Keberangkatan",
                ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                 "Juli", "Agustus", "September", "Oktober", "November", "Desember",
                 "Belum Pasti"]
            )
            
            budget = st.text_input("Budget (opsional)", placeholder="Rp 35.000.000")
        
        notes = st.text_area("Catatan Tambahan", placeholder="Misal: Ada jamaah lansia, butuh kursi roda, dll")
        
        agree = st.checkbox("Saya setuju untuk dihubungi oleh travel agent partner")
        
        submitted = st.form_submit_button("📤 Kirim & Dapatkan Penawaran", use_container_width=True, type="primary")
        
        if submitted:
            if name and email and phone and agree:
                lead_id = generate_lead_id()
                lead_data = {
                    "id": lead_id,
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "city": city,
                    "package_type": package_type,
                    "num_people": num_people,
                    "travel_month": travel_month,
                    "budget": budget,
                    "notes": notes,
                    "context": context,
                    "timestamp": datetime.now().isoformat(),
                    "status": "new"
                }
                
                st.session_state.leads_generated.append(lead_data)
                
                st.success(f"""
                🎉 **Terima kasih {name}!**
                
                Lead ID Anda: **{lead_id}**
                
                Travel agent partner kami akan menghubungi Anda dalam 1x24 jam 
                melalui WhatsApp di nomor {phone}.
                
                💡 **Tips:** Simpan Lead ID untuk tracking status penawaran.
                """)
                
                # Show matching partners
                st.markdown("---")
                st.markdown("### 🏆 Partner Travel Terpilih untuk Anda")
                
                for partner in PARTNER_AGENTS[:3]:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.markdown(f"**{partner['logo']} {partner['name']}**")
                        st.markdown(f"⭐ {partner['rating']} ({partner['reviews']} reviews)")
                    with col2:
                        st.markdown(f"{'✅ Verified' if partner['verified'] else ''}")
                        st.markdown(f"Paket: {', '.join(partner['packages'])}")
                    with col3:
                        wa_link = f"https://wa.me/{partner['contact']['whatsapp']}"
                        st.markdown(f"[💬 WhatsApp]({wa_link})")
                    st.markdown("---")
            else:
                st.error("Mohon lengkapi semua field yang wajib (*) dan centang persetujuan")


def render_quick_quote_widget():
    """Render quick quote widget for sidebar/popup"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    ">
        <h4 style="margin: 0;">💬 Mau Konsultasi GRATIS?</h4>
        <p style="font-size: 0.85rem; margin: 0.5rem 0;">
            Travel agent berpengalaman siap membantu
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("quick_quote"):
        phone = st.text_input("No. WhatsApp", placeholder="08xxxxxxxxxx")
        if st.form_submit_button("📞 Hubungi Saya", use_container_width=True):
            if phone:
                st.success("✅ Tim kami akan menghubungi Anda segera!")
            else:
                st.error("Masukkan nomor WhatsApp")


# ============================================
# 3. AFFILIATE PARTNER LISTING
# ============================================

def render_partner_directory():
    """Render partner travel agent directory with affiliate tracking"""
    st.markdown("### 🤝 Partner Travel Agent Terpercaya")
    st.markdown("Booking melalui partner kami dan dapatkan harga terbaik + bonus eksklusif")
    
    # Filter
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_package = st.multiselect(
            "Filter Paket",
            ["ekonomis", "standard", "premium", "vip"],
            default=["ekonomis", "standard", "premium", "vip"]
        )
    with col2:
        sort_by = st.selectbox(
            "Urutkan",
            ["Rating Tertinggi", "Review Terbanyak", "Featured"]
        )
    with col3:
        verified_only = st.checkbox("Verified Only", value=True)
    
    st.markdown("---")
    
    # Filter and sort partners
    partners = PARTNER_AGENTS.copy()
    
    if verified_only:
        partners = [p for p in partners if p["verified"]]
    
    partners = [p for p in partners if any(pkg in p["packages"] for pkg in filter_package)]
    
    if sort_by == "Rating Tertinggi":
        partners = sorted(partners, key=lambda x: x["rating"], reverse=True)
    elif sort_by == "Review Terbanyak":
        partners = sorted(partners, key=lambda x: x["reviews"], reverse=True)
    else:
        partners = sorted(partners, key=lambda x: x["featured"], reverse=True)
    
    # Display partners
    for partner in partners:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            
            with col1:
                featured_badge = "🏆 FEATURED " if partner["featured"] else ""
                verified_badge = "✅ " if partner["verified"] else ""
                
                st.markdown(f"""
                ### {partner['logo']} {partner['name']}
                {featured_badge}{verified_badge}
                
                ⭐ **{partner['rating']}**/5.0 • {partner['reviews']:,} reviews
                """)
            
            with col2:
                st.markdown("**Paket Tersedia:**")
                for pkg in partner["packages"]:
                    st.markdown(f"• {pkg.title()}")
            
            with col3:
                st.markdown("**Kontak:**")
                st.markdown(f"📞 {partner['contact']['phone']}")
                st.markdown(f"🌐 [Website]({partner['contact']['website']})")
            
            with col4:
                # Affiliate tracking link
                ref_code = f"UPL-{partner['id'].upper()}-{generate_ref_code(4)}"
                wa_link = f"https://wa.me/{partner['contact']['whatsapp']}?text=Halo,%20saya%20dari%20Umrah%20Planner%20AI%20(Ref:%20{ref_code})"
                
                st.markdown(f"""
                <a href="{wa_link}" target="_blank" style="
                    display: inline-block;
                    background: #25D366;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    text-decoration: none;
                    font-weight: bold;
                ">💬 Chat WhatsApp</a>
                """, unsafe_allow_html=True)
                
                st.caption(f"Ref: {ref_code}")
                
                # Track click
                if st.button(f"📋 Lihat Paket", key=f"view_{partner['id']}"):
                    st.session_state.affiliate_clicks.append({
                        "partner_id": partner["id"],
                        "ref_code": ref_code,
                        "timestamp": datetime.now().isoformat()
                    })
            
            st.markdown("---")
    
    # Exclusive offers
    st.markdown("### 🎁 Penawaran Eksklusif")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
        ">
            <h4>🔥 Early Bird Discount</h4>
            <p>Booking 3 bulan sebelum keberangkatan, dapatkan <strong>diskon 10%</strong></p>
            <p style="font-size: 0.8rem;">*Berlaku untuk semua partner</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
        ">
            <h4>👨‍👩‍👧‍👦 Family Package</h4>
            <p>Rombongan 5+ orang, <strong>1 orang GRATIS handling</strong></p>
            <p style="font-size: 0.8rem;">*Syarat & ketentuan berlaku</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# 4. PREMIUM FEATURES
# ============================================

def render_premium_features():
    """Render premium-only features"""
    user_tier = st.session_state.get("user_tier", "free")
    
    st.markdown("### ⭐ Fitur Premium")
    
    # Feature cards
    features = [
        {
            "name": "🔔 Price Alert",
            "desc": "Notifikasi real-time saat harga turun",
            "tier_required": "premium",
            "action": "set_price_alert"
        },
        {
            "name": "📄 Export PDF Itinerary",
            "desc": "Download rencana perjalanan lengkap",
            "tier_required": "premium",
            "action": "export_pdf"
        },
        {
            "name": "💼 Document Manager",
            "desc": "Simpan & kelola dokumen perjalanan",
            "tier_required": "premium",
            "action": "doc_manager"
        },
        {
            "name": "🎯 Personal AI Consultant",
            "desc": "Konsultasi 24/7 dengan AI khusus",
            "tier_required": "premium",
            "action": "ai_consultant"
        },
        {
            "name": "👤 Dedicated Account Manager",
            "desc": "CS khusus untuk Anda",
            "tier_required": "vip",
            "action": "account_manager"
        },
        {
            "name": "💰 Cashback Program",
            "desc": "Dapatkan cashback setiap transaksi",
            "tier_required": "vip",
            "action": "cashback"
        }
    ]
    
    cols = st.columns(3)
    
    for i, feature in enumerate(features):
        with cols[i % 3]:
            tier_order = ["free", "basic", "premium", "vip"]
            has_access = tier_order.index(user_tier) >= tier_order.index(feature["tier_required"])
            
            if has_access:
                st.markdown(f"""
                <div style="
                    background: #e8f5e9;
                    padding: 1rem;
                    border-radius: 10px;
                    border: 2px solid #4caf50;
                    min-height: 120px;
                ">
                    <h4>{feature['name']}</h4>
                    <p style="font-size: 0.85rem;">{feature['desc']}</p>
                    <span style="color: #4caf50;">✅ Tersedia</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Gunakan", key=f"use_{feature['action']}"):
                    st.info(f"Membuka {feature['name']}...")
            else:
                st.markdown(f"""
                <div style="
                    background: #f5f5f5;
                    padding: 1rem;
                    border-radius: 10px;
                    border: 2px solid #ddd;
                    min-height: 120px;
                    opacity: 0.7;
                ">
                    <h4>{feature['name']}</h4>
                    <p style="font-size: 0.85rem;">{feature['desc']}</p>
                    <span style="color: #ff9800;">🔒 {feature['tier_required'].title()}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Upgrade", key=f"upgrade_{feature['action']}"):
                    st.session_state.show_pricing = True


def render_price_alert_setup():
    """Render price alert setup for premium users"""
    st.markdown("### 🔔 Setup Price Alert")
    st.markdown("Dapatkan notifikasi saat harga paket turun sesuai target Anda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        package_type = st.selectbox(
            "Tipe Paket",
            ["Ekonomis", "Standard", "Premium", "VIP"]
        )
        
        target_price = st.number_input(
            "Target Harga Maksimum (Rp)",
            min_value=20000000,
            max_value=200000000,
            value=35000000,
            step=1000000
        )
    
    with col2:
        departure_month = st.selectbox(
            "Bulan Keberangkatan",
            ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
             "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        )
        
        notification_method = st.multiselect(
            "Metode Notifikasi",
            ["Email", "WhatsApp", "Push Notification"],
            default=["Email", "WhatsApp"]
        )
    
    if st.button("🔔 Aktifkan Price Alert", use_container_width=True, type="primary"):
        alert = {
            "id": generate_ref_code(6),
            "package_type": package_type,
            "target_price": target_price,
            "departure_month": departure_month,
            "notification_method": notification_method,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        st.session_state.price_alerts.append(alert)
        st.success("✅ Price Alert berhasil diaktifkan! Kami akan menghubungi Anda saat ada penawaran yang sesuai.")
    
    # Active alerts
    if st.session_state.price_alerts:
        st.markdown("---")
        st.markdown("### 📋 Alert Aktif")
        
        for alert in st.session_state.price_alerts:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{alert['package_type']}** - {alert['departure_month']}")
            with col2:
                st.markdown(f"Target: {format_price(alert['target_price'])}")
            with col3:
                if st.button("🗑️", key=f"del_{alert['id']}"):
                    st.session_state.price_alerts.remove(alert)
                    st.rerun()


# ============================================
# 5. REFERRAL PROGRAM
# ============================================

def render_referral_program():
    """Render referral program page"""
    st.markdown("### 🎁 Program Referral")
    st.markdown("Ajak teman dan dapatkan reward hingga **Rp 500.000** per referral!")
    
    # Generate or get referral code
    if not st.session_state.referral_code:
        st.session_state.referral_code = f"REF-{generate_ref_code(8)}"
    
    ref_code = st.session_state.referral_code
    ref_link = f"https://umrah-planner-by-mshadianto.streamlit.app?ref={ref_code}"
    
    # Referral stats card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    ">
        <h3>Kode Referral Anda</h3>
        <h1 style="font-family: monospace; letter-spacing: 5px;">{ref_code}</h1>
        <p>Share kode ini dan dapatkan reward!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Copy link
    st.code(ref_link, language=None)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        wa_share = f"https://wa.me/?text=Hai!%20Cek%20aplikasi%20Umrah%20Planner%20AI%20untuk%20perencanaan%20umrah%20kamu.%20Gunakan%20kode%20{ref_code}%20untuk%20dapat%20bonus!%20{ref_link}"
        st.markdown(f"[📱 Share via WhatsApp]({wa_share})")
    with col2:
        st.markdown(f"[📘 Share via Facebook](https://facebook.com/sharer/sharer.php?u={ref_link})")
    with col3:
        st.markdown(f"[🐦 Share via Twitter](https://twitter.com/intent/tweet?url={ref_link})")
    
    st.markdown("---")
    
    # Reward tiers
    st.markdown("### 💰 Reward Tiers")
    
    rewards = [
        {"referrals": 1, "reward": "Rp 50.000", "bonus": ""},
        {"referrals": 5, "reward": "Rp 300.000", "bonus": "+ 1 Bulan Premium GRATIS"},
        {"referrals": 10, "reward": "Rp 750.000", "bonus": "+ 3 Bulan Premium GRATIS"},
        {"referrals": 25, "reward": "Rp 2.000.000", "bonus": "+ Lifetime VIP Access"},
    ]
    
    cols = st.columns(4)
    for i, tier in enumerate(rewards):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                border: 2px solid #e0e0e0;
            ">
                <h3>{tier['referrals']} Referral</h3>
                <h4 style="color: #4caf50;">{tier['reward']}</h4>
                <p style="font-size: 0.8rem; color: #666;">{tier['bonus']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("---")
    st.markdown("### 📊 Statistik Referral Anda")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Klik", "0")
    with col2:
        st.metric("Registrasi", "0")
    with col3:
        st.metric("Konversi", "0")
    with col4:
        st.metric("Reward Earned", "Rp 0")


# ============================================
# 6. B2B WHITE LABEL
# ============================================

def render_b2b_page():
    """Render B2B partnership page"""
    st.markdown("### 🏢 Kemitraan B2B / White Label")
    st.markdown("Solusi teknologi untuk travel agent dan perusahaan")
    
    # Value props
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: #e3f2fd;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
        ">
            <h1>🏷️</h1>
            <h4>White Label</h4>
            <p>Gunakan dengan brand Anda sendiri</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: #e8f5e9;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
        ">
            <h1>🔌</h1>
            <h4>API Access</h4>
            <p>Integrasi dengan sistem Anda</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: #fff3e0;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
        ">
            <h1>📊</h1>
            <h4>Analytics Dashboard</h4>
            <p>Pantau performa bisnis</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pricing tiers
    st.markdown("### 💼 Paket Kemitraan")
    
    b2b_tiers = {
        "starter": {
            "name": "Starter",
            "price": "Rp 2.5 Juta/bulan",
            "features": [
                "White label basic",
                "Up to 100 leads/bulan",
                "Email support",
                "Basic analytics"
            ]
        },
        "growth": {
            "name": "Growth",
            "price": "Rp 7.5 Juta/bulan",
            "features": [
                "Full white label",
                "Unlimited leads",
                "API access",
                "Priority support",
                "Advanced analytics",
                "Custom domain"
            ]
        },
        "enterprise": {
            "name": "Enterprise",
            "price": "Custom",
            "features": [
                "Semua fitur Growth",
                "Dedicated server",
                "Custom development",
                "Account manager",
                "SLA 99.9%",
                "On-premise option"
            ]
        }
    }
    
    cols = st.columns(3)
    for i, (tier_id, tier) in enumerate(b2b_tiers.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 1.5rem;
                text-align: center;
                min-height: 300px;
            ">
                <h3>{tier['name']}</h3>
                <h2 style="color: #1e88e5;">{tier['price']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            for feature in tier["features"]:
                st.markdown(f"✅ {feature}")
            
            st.button(f"Hubungi Sales", key=f"b2b_{tier_id}", use_container_width=True)
    
    # Contact form
    st.markdown("---")
    st.markdown("### 📞 Hubungi Tim B2B Kami")
    
    with st.form("b2b_contact"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Nama Perusahaan *")
            name = st.text_input("Nama PIC *")
            email = st.text_input("Email Bisnis *")
        with col2:
            phone = st.text_input("No. Telepon *")
            employees = st.selectbox("Jumlah Karyawan", ["1-10", "11-50", "51-200", "200+"])
            interest = st.selectbox("Tertarik Dengan", ["White Label", "API Integration", "Custom Solution"])
        
        message = st.text_area("Pesan")
        
        if st.form_submit_button("📤 Kirim Inquiry", use_container_width=True, type="primary"):
            if company and name and email and phone:
                st.success("✅ Inquiry berhasil dikirim! Tim kami akan menghubungi dalam 1x24 jam.")
            else:
                st.error("Mohon lengkapi semua field wajib")


# ============================================
# MAIN RENDER FUNCTION
# ============================================

def render_monetization_page():
    """Main function to render monetization features"""
    init_monetization_state()
    
    st.markdown("### 💼 Business Hub")
    
    feature = st.selectbox(
        "Pilih Menu",
        options=[
            "💎 Paket Berlangganan",
            "📝 Dapatkan Penawaran",
            "🤝 Partner Travel Agent",
            "⭐ Fitur Premium",
            "🎁 Program Referral",
            "🏢 Kemitraan B2B"
        ]
    )
    
    st.markdown("---")
    
    if "Berlangganan" in feature:
        render_pricing_page()
    elif "Penawaran" in feature:
        render_lead_capture_form()
    elif "Partner" in feature:
        render_partner_directory()
    elif "Premium" in feature:
        render_premium_features()
    elif "Referral" in feature:
        render_referral_program()
    elif "B2B" in feature:
        render_b2b_page()


# ============================================
# SIDEBAR WIDGETS
# ============================================

def render_monetization_sidebar():
    """Render monetization widgets in sidebar"""
    user_tier = st.session_state.get("user_tier", "free")
    
    if user_tier == "free":
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
        ">
            <p style="margin: 0; font-size: 0.9rem;">🔓 Upgrade ke Premium</p>
            <p style="margin: 0.5rem 0; font-size: 0.8rem;">Unlock semua fitur</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        tier_info = PRICING_TIERS.get(user_tier, {})
        st.markdown(f"""
        <div style="
            background: #e8f5e9;
            padding: 0.75rem;
            border-radius: 10px;
            text-align: center;
        ">
            <p style="margin: 0;">{tier_info.get('badge', '')} {tier_info.get('name', 'Member')}</p>
        </div>
        """, unsafe_allow_html=True)
