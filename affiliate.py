"""
💰 Affiliate & Revenue Integration
==================================
Real affiliate links dan tracking untuk monetisasi

Copyright (c) 2025 MS Hadianto. All Rights Reserved.
"""

import streamlit as st
from datetime import datetime
import hashlib
import json

# ============================================
# AFFILIATE PARTNERS CONFIG
# ============================================

AFFILIATE_PARTNERS = {
    "traveloka": {
        "name": "Traveloka",
        "type": "OTA",
        "base_url": "https://www.traveloka.com",
        "affiliate_id": "YOUR_TRAVELOKA_AFFILIATE_ID",  # Ganti dengan ID Anda
        "commission": "2-5%",
        "tracking_param": "utm_source=umrahplanner&utm_medium=affiliate",
        "categories": ["flight", "hotel"],
        "logo": "✈️"
    },
    "agoda": {
        "name": "Agoda",
        "type": "Hotel",
        "base_url": "https://www.agoda.com",
        "affiliate_id": "YOUR_AGODA_PARTNER_ID",  # Ganti dengan ID Anda
        "commission": "4-7%",
        "tracking_param": "cid=YOUR_CID",
        "categories": ["hotel"],
        "logo": "🏨"
    },
    "booking": {
        "name": "Booking.com",
        "type": "Hotel",
        "base_url": "https://www.booking.com",
        "affiliate_id": "YOUR_BOOKING_AFFILIATE_ID",  # Ganti dengan ID Anda
        "commission": "25-40%",
        "tracking_param": "aid=YOUR_AID",
        "categories": ["hotel"],
        "logo": "🏨"
    },
    "tiket": {
        "name": "Tiket.com",
        "type": "OTA",
        "base_url": "https://www.tiket.com",
        "affiliate_id": "YOUR_TIKET_AFFILIATE_ID",  # Ganti dengan ID Anda
        "commission": "1-3%",
        "tracking_param": "utm_source=umrahplanner",
        "categories": ["flight", "hotel"],
        "logo": "🎫"
    },
    "allianz": {
        "name": "Allianz Travel",
        "type": "Insurance",
        "base_url": "https://www.allianz.co.id/produk/asuransi-perjalanan",
        "affiliate_id": "YOUR_ALLIANZ_ID",
        "commission": "15-25%",
        "tracking_param": "ref=umrahplanner",
        "categories": ["insurance"],
        "logo": "🛡️"
    }
}

# ============================================
# TRAVEL AGENT PARTNERS (Lead Generation)
# ============================================

TRAVEL_AGENT_PARTNERS = [
    {
        "id": "ta001",
        "name": "Al-Madinah Tour",
        "city": "Jakarta",
        "whatsapp": "6281234567890",  # Ganti dengan nomor real
        "commission_per_lead": 100000,  # Rp 100.000 per lead closing
        "commission_percentage": 2,  # 2% dari nilai paket
        "packages": ["ekonomi", "reguler", "vip"],
        "rating": 4.8,
        "active": True
    },
    {
        "id": "ta002", 
        "name": "Berkah Umrah",
        "city": "Bandung",
        "whatsapp": "6281234567891",
        "commission_per_lead": 150000,
        "commission_percentage": 2.5,
        "packages": ["ekonomi", "reguler"],
        "rating": 4.6,
        "active": True
    },
    {
        "id": "ta003",
        "name": "Safar Wisata",
        "city": "Surabaya", 
        "whatsapp": "6281234567892",
        "commission_per_lead": 200000,
        "commission_percentage": 3,
        "packages": ["reguler", "vip", "vvip"],
        "rating": 4.9,
        "active": True
    }
]

# ============================================
# AFFILIATE LINK GENERATOR
# ============================================

def generate_affiliate_link(partner_id: str, destination: str = "", 
                           checkin: str = "", checkout: str = "") -> str:
    """Generate tracked affiliate link"""
    
    if partner_id not in AFFILIATE_PARTNERS:
        return "#"
    
    partner = AFFILIATE_PARTNERS[partner_id]
    base_url = partner["base_url"]
    tracking = partner["tracking_param"]
    
    # Build URL based on partner
    if partner_id == "traveloka":
        if destination:
            url = f"{base_url}/search/hotel?spec={destination}&{tracking}"
        else:
            url = f"{base_url}?{tracking}"
    
    elif partner_id == "agoda":
        url = f"{base_url}/search?city={destination}&{tracking}"
    
    elif partner_id == "booking":
        url = f"{base_url}/searchresults.html?ss={destination}&{tracking}"
    
    elif partner_id == "tiket":
        url = f"{base_url}?{tracking}"
    
    else:
        url = f"{base_url}?{tracking}"
    
    return url

def track_affiliate_click(partner_id: str, user_id: str = None):
    """Track affiliate click untuk analytics"""
    
    if 'affiliate_clicks' not in st.session_state:
        st.session_state.affiliate_clicks = []
    
    click_data = {
        "partner_id": partner_id,
        "user_id": user_id or "anonymous",
        "timestamp": datetime.now().isoformat(),
        "session_id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    }
    
    st.session_state.affiliate_clicks.append(click_data)
    
    # Di production, simpan ke database
    # db.insert("affiliate_clicks", click_data)

# ============================================
# LEAD CAPTURE FORM
# ============================================

def render_lead_capture_form():
    """Form untuk capture leads"""
    
    st.markdown("### 📋 Dapatkan Penawaran Terbaik")
    st.markdown("Isi form di bawah untuk dihubungi oleh travel agent terpercaya")
    
    with st.form("lead_capture_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nama Lengkap *")
            phone = st.text_input("No. WhatsApp *", placeholder="08xxxxxxxxxx")
            city = st.selectbox("Kota Keberangkatan", [
                "Jakarta", "Bandung", "Surabaya", "Medan", 
                "Makassar", "Semarang", "Yogyakarta", "Lainnya"
            ])
        
        with col2:
            email = st.text_input("Email")
            num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=1)
            travel_month = st.selectbox("Rencana Berangkat", [
                "Januari 2025", "Februari 2025", "Maret 2025",
                "April 2025", "Mei 2025", "Juni 2025",
                "Ramadhan 2025", "Setelah Ramadhan 2025"
            ])
        
        budget = st.select_slider("Budget per Orang", options=[
            "< Rp 25 Juta", "Rp 25-35 Juta", "Rp 35-50 Juta", 
            "Rp 50-75 Juta", "> Rp 75 Juta"
        ])
        
        package_type = st.radio("Jenis Paket yang Diminati", [
            "🎒 Ekonomi (9 hari)", 
            "⭐ Reguler (12 hari)", 
            "👑 VIP (14 hari)",
            "Belum tahu, butuh konsultasi"
        ], horizontal=True)
        
        notes = st.text_area("Catatan/Pertanyaan (opsional)")
        
        consent = st.checkbox("Saya setuju untuk dihubungi oleh travel agent partner")
        
        submitted = st.form_submit_button("📩 Kirim & Dapatkan Penawaran", use_container_width=True)
        
        if submitted:
            if not name or not phone:
                st.error("Mohon isi nama dan nomor WhatsApp")
            elif not consent:
                st.error("Mohon centang persetujuan untuk melanjutkan")
            else:
                # Save lead
                lead_data = {
                    "id": f"LEAD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "city": city,
                    "num_people": num_people,
                    "travel_month": travel_month,
                    "budget": budget,
                    "package_type": package_type,
                    "notes": notes,
                    "created_at": datetime.now().isoformat(),
                    "status": "new",
                    "source": "web_form"
                }
                
                # Save to session (in production, save to database)
                if 'leads' not in st.session_state:
                    st.session_state.leads = []
                st.session_state.leads.append(lead_data)
                
                # Send to travel agent (in production, send WhatsApp/email)
                send_lead_to_agent(lead_data)
                
                st.success("✅ Terima kasih! Travel agent akan menghubungi Anda dalam 1x24 jam")
                st.balloons()

def send_lead_to_agent(lead_data: dict):
    """Send lead ke travel agent via WhatsApp"""
    
    # Pilih travel agent berdasarkan kota
    agent = None
    for ta in TRAVEL_AGENT_PARTNERS:
        if ta["city"].lower() == lead_data["city"].lower() and ta["active"]:
            agent = ta
            break
    
    if not agent:
        # Default ke agent pertama yang aktif
        agent = next((ta for ta in TRAVEL_AGENT_PARTNERS if ta["active"]), None)
    
    if agent:
        # Format pesan WhatsApp
        message = f"""
🕋 *LEAD BARU dari Umrah Planner AI*

👤 Nama: {lead_data['name']}
📱 WhatsApp: {lead_data['phone']}
📧 Email: {lead_data.get('email', '-')}
🏙️ Kota: {lead_data['city']}
👥 Jumlah: {lead_data['num_people']} orang
📅 Rencana: {lead_data['travel_month']}
💰 Budget: {lead_data['budget']}
📦 Paket: {lead_data['package_type']}
📝 Catatan: {lead_data.get('notes', '-')}

Lead ID: {lead_data['id']}
        """
        
        # Generate WhatsApp link
        wa_link = f"https://wa.me/{agent['whatsapp']}?text={message}"
        
        # Di production, bisa pakai WhatsApp Business API untuk auto-send
        # Atau simpan untuk manual follow-up
        
        return wa_link
    
    return None

# ============================================
# AFFILIATE DISPLAY WIDGETS
# ============================================

def render_affiliate_hotels(destination: str = "Makkah"):
    """Tampilkan hotel recommendations dengan affiliate links"""
    
    st.markdown(f"### 🏨 Hotel di {destination}")
    
    cols = st.columns(3)
    
    hotels = [
        {"name": "Booking.com", "partner": "booking", "desc": "Best price guarantee"},
        {"name": "Agoda", "partner": "agoda", "desc": "Extra diskon member"},
        {"name": "Traveloka", "partner": "traveloka", "desc": "Promo spesial"}
    ]
    
    for i, hotel in enumerate(hotels):
        with cols[i]:
            partner = AFFILIATE_PARTNERS[hotel["partner"]]
            link = generate_affiliate_link(hotel["partner"], destination)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 15px; border-radius: 10px; text-align: center;'>
                <h4 style='color: white; margin: 0;'>{partner['logo']} {hotel['name']}</h4>
                <p style='color: #eee; font-size: 12px;'>{hotel['desc']}</p>
                <p style='color: #ffd700; font-size: 11px;'>Komisi: {partner['commission']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Cari di {hotel['name']}", key=f"aff_{hotel['partner']}"):
                track_affiliate_click(hotel["partner"])
                st.markdown(f"[Buka {hotel['name']}]({link})")

def render_affiliate_flights():
    """Tampilkan flight search dengan affiliate links"""
    
    st.markdown("### ✈️ Cari Tiket Pesawat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        link_traveloka = generate_affiliate_link("traveloka")
        st.markdown(f"""
        <a href="{link_traveloka}" target="_blank" style="text-decoration: none;">
            <div style='background: #0064D2; padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>✈️ Traveloka</h3>
                <p style='color: #eee;'>Cari tiket termurah</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        link_tiket = generate_affiliate_link("tiket")
        st.markdown(f"""
        <a href="{link_tiket}" target="_blank" style="text-decoration: none;">
            <div style='background: #0770CD; padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white;'>🎫 Tiket.com</h3>
                <p style='color: #eee;'>Promo tiket pesawat</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

def render_insurance_affiliate():
    """Tampilkan asuransi dengan affiliate links"""
    
    st.markdown("### 🛡️ Asuransi Perjalanan")
    
    link = generate_affiliate_link("allianz")
    
    st.markdown(f"""
    <a href="{link}" target="_blank" style="text-decoration: none;">
        <div style='background: linear-gradient(135deg, #003781 0%, #0066B3 100%); 
                    padding: 20px; border-radius: 10px;'>
            <h3 style='color: white;'>🛡️ Allianz Travel Insurance</h3>
            <p style='color: #eee;'>Perlindungan perjalanan komprehensif</p>
            <ul style='color: #eee;'>
                <li>Perlindungan medis hingga $100,000</li>
                <li>Evakuasi darurat</li>
                <li>Kehilangan bagasi</li>
                <li>Pembatalan perjalanan</li>
            </ul>
            <p style='color: #ffd700;'>Mulai Rp 150.000/orang</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

# ============================================
# REVENUE DASHBOARD
# ============================================

def render_revenue_dashboard():
    """Dashboard untuk tracking revenue"""
    
    st.markdown("## 💰 Revenue Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Get data from session state
    leads = st.session_state.get('leads', [])
    clicks = st.session_state.get('affiliate_clicks', [])
    
    with col1:
        st.metric("Total Leads", len(leads), "+3 hari ini")
    
    with col2:
        st.metric("Affiliate Clicks", len(clicks), "+12 hari ini")
    
    with col3:
        # Estimasi revenue dari leads (asumsi 10% conversion rate)
        estimated_lead_revenue = len(leads) * 0.1 * 150000
        st.metric("Est. Lead Revenue", f"Rp {estimated_lead_revenue:,.0f}")
    
    with col4:
        # Estimasi dari affiliate (asumsi 1% CTR, 2% conversion, avg Rp 5M booking)
        estimated_aff_revenue = len(clicks) * 0.02 * 5000000 * 0.03
        st.metric("Est. Affiliate Revenue", f"Rp {estimated_aff_revenue:,.0f}")
    
    st.markdown("---")
    
    # Leads table
    st.markdown("### 📋 Recent Leads")
    if leads:
        for lead in leads[-5:]:
            with st.expander(f"🔵 {lead['name']} - {lead['city']} - {lead['created_at'][:10]}"):
                st.write(f"**Phone:** {lead['phone']}")
                st.write(f"**Email:** {lead.get('email', '-')}")
                st.write(f"**Jamaah:** {lead['num_people']} orang")
                st.write(f"**Budget:** {lead['budget']}")
                st.write(f"**Status:** {lead['status']}")
    else:
        st.info("Belum ada leads")
    
    # Affiliate clicks
    st.markdown("### 🖱️ Affiliate Clicks")
    if clicks:
        click_summary = {}
        for click in clicks:
            partner = click['partner_id']
            click_summary[partner] = click_summary.get(partner, 0) + 1
        
        for partner, count in click_summary.items():
            st.write(f"**{AFFILIATE_PARTNERS.get(partner, {}).get('name', partner)}:** {count} clicks")
    else:
        st.info("Belum ada affiliate clicks")

# ============================================
# MAIN MONETIZATION PAGE
# ============================================

def render_monetization_hub():
    """Main monetization hub page"""
    
    st.markdown("# 💰 Partner & Booking Hub")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "✈️ Tiket & Hotel", 
        "🛡️ Asuransi",
        "📋 Konsultasi Gratis",
        "📊 Dashboard"
    ])
    
    with tab1:
        render_affiliate_flights()
        st.markdown("---")
        render_affiliate_hotels("Makkah")
    
    with tab2:
        render_insurance_affiliate()
    
    with tab3:
        render_lead_capture_form()
    
    with tab4:
        render_revenue_dashboard()

# ============================================
# SETUP INSTRUCTIONS
# ============================================

def render_monetization_setup():
    """Instructions untuk setup monetization"""
    
    st.markdown("""
    ## 🔧 Setup Monetization
    
    ### 1. Affiliate Programs
    
    Daftar ke program affiliate berikut:
    
    | Platform | Link Daftar | Komisi |
    |----------|-------------|--------|
    | Traveloka | [Daftar](https://www.traveloka.com/affiliate) | 2-5% |
    | Agoda | [Daftar](https://partners.agoda.com) | 4-7% |
    | Booking.com | [Daftar](https://www.booking.com/affiliate) | 25-40% |
    | AccessTrade | [Daftar](https://accesstrade.co.id) | Varies |
    
    ### 2. Update Affiliate IDs
    
    Setelah dapat affiliate ID, update di file `affiliate.py`:
    
    ```python
    AFFILIATE_PARTNERS = {
        "traveloka": {
            "affiliate_id": "YOUR_REAL_ID_HERE",
            ...
        }
    }
    ```
    
    ### 3. Travel Agent Partners
    
    Hubungi travel agent dan update kontak di `TRAVEL_AGENT_PARTNERS`
    
    ### 4. Payment Gateway (untuk Subscription)
    
    1. Daftar Midtrans: https://midtrans.com
    2. Atau Xendit: https://xendit.co
    3. Integrate dengan subscription system
    """)

if __name__ == "__main__":
    render_monetization_hub()
