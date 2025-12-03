"""
LABBAIK Booking Features Module
Handles travel package booking simulation
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class TravelPackage:
    """Travel package data structure"""
    id: str
    name: str
    provider: str
    price: float
    duration_days: int
    hotel_makkah: str
    hotel_madinah: str
    includes: List[str]
    rating: float
    reviews: int


# Sample travel packages
SAMPLE_PACKAGES = [
    TravelPackage(
        id="pkg-001",
        name="Paket Ekonomis 9 Hari",
        provider="Al-Madinah Travel",
        price=22_500_000,
        duration_days=9,
        hotel_makkah="Elaf Ajyad Hotel ⭐⭐⭐",
        hotel_madinah="Al Eiman Taibah Hotel ⭐⭐⭐",
        includes=["Tiket PP", "Visa", "Hotel", "Transport Bandara", "City Tour"],
        rating=4.5,
        reviews=128
    ),
    TravelPackage(
        id="pkg-002",
        name="Paket Standard 12 Hari",
        provider="Nur Ramadhan Tour",
        price=28_000_000,
        duration_days=12,
        hotel_makkah="Pullman ZamZam ⭐⭐⭐⭐",
        hotel_madinah="Millennium Al Aqeeq ⭐⭐⭐⭐",
        includes=["Tiket PP", "Visa", "Hotel", "Makan 3x", "Guide", "Perlengkapan"],
        rating=4.7,
        reviews=256
    ),
    TravelPackage(
        id="pkg-003",
        name="Paket Premium 14 Hari",
        provider="Darul Hijrah Tours",
        price=38_500_000,
        duration_days=14,
        hotel_makkah="Makkah Clock Tower ⭐⭐⭐⭐⭐",
        hotel_madinah="Dar Al Taqwa Hotel ⭐⭐⭐⭐⭐",
        includes=["Tiket PP Business", "Visa", "Hotel Premium", "Makan 3x", "Handling VIP"],
        rating=4.9,
        reviews=89
    )
]


def get_available_packages(
    min_price: float = 0,
    max_price: float = 100_000_000,
    min_duration: int = 0,
    max_duration: int = 30
) -> List[TravelPackage]:
    """Get available packages with optional filters"""
    
    packages = [
        p for p in SAMPLE_PACKAGES
        if min_price <= p.price <= max_price
        and min_duration <= p.duration_days <= max_duration
    ]
    
    return sorted(packages, key=lambda x: x.price)


def render_package_card(package: TravelPackage, compact: bool = False):
    """Render a travel package card"""
    
    if compact:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                    border-radius: 10px; padding: 15px; margin-bottom: 10px;
                    border: 1px solid #D4AF3730;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="color: #D4AF37; font-weight: 700;">{package.name}</div>
                    <div style="color: #C9A86C; font-size: 0.8rem;">{package.provider}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #4CAF50; font-weight: 700; font-size: 1.1rem;">
                        Rp {package.price:,.0f}
                    </div>
                    <div style="color: #888; font-size: 0.8rem;">{package.duration_days} hari</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                    border-radius: 15px; padding: 20px; margin-bottom: 15px;
                    border: 1px solid #D4AF3750;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                <div>
                    <div style="color: #D4AF37; font-size: 1.2rem; font-weight: 700;">{package.name}</div>
                    <div style="color: #C9A86C; font-size: 0.9rem;">{package.provider}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #4CAF50; font-size: 1.4rem; font-weight: 700;">
                        Rp {package.price:,.0f}
                    </div>
                    <div style="color: #888; font-size: 0.85rem;">/orang</div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <div style="background: #1A1A1A80; padding: 10px; border-radius: 8px;">
                    <div style="color: #888; font-size: 0.75rem;">🕋 Makkah</div>
                    <div style="color: white; font-size: 0.85rem;">{package.hotel_makkah}</div>
                </div>
                <div style="background: #1A1A1A80; padding: 10px; border-radius: 8px;">
                    <div style="color: #888; font-size: 0.75rem;">🕌 Madinah</div>
                    <div style="color: white; font-size: 0.85rem;">{package.hotel_madinah}</div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    {"".join([f'<span style="background: #D4AF3720; color: #D4AF37; padding: 3px 8px; border-radius: 12px; font-size: 0.7rem;">{inc}</span>' for inc in package.includes[:4]])}
                </div>
                <div style="color: #FFD700; font-size: 0.9rem;">
                    ⭐ {package.rating} ({package.reviews})
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_booking_features():
    """Render the booking comparison feature"""
    
    st.markdown("### 📦 Bandingkan Paket Travel")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        price_range = st.slider(
            "💰 Range Harga (juta)",
            min_value=15,
            max_value=50,
            value=(15, 50),
            step=5
        )
    
    with col2:
        duration = st.slider(
            "📅 Durasi (hari)",
            min_value=7,
            max_value=21,
            value=(7, 21)
        )
    
    with col3:
        sort_by = st.selectbox(
            "🔄 Urutkan",
            ["Harga Terendah", "Harga Tertinggi", "Rating Tertinggi", "Durasi Terpendek"]
        )
    
    # Get packages
    packages = get_available_packages(
        min_price=price_range[0] * 1_000_000,
        max_price=price_range[1] * 1_000_000,
        min_duration=duration[0],
        max_duration=duration[1]
    )
    
    # Sort
    if sort_by == "Harga Tertinggi":
        packages = sorted(packages, key=lambda x: x.price, reverse=True)
    elif sort_by == "Rating Tertinggi":
        packages = sorted(packages, key=lambda x: x.rating, reverse=True)
    elif sort_by == "Durasi Terpendek":
        packages = sorted(packages, key=lambda x: x.duration_days)
    
    # Display
    st.markdown(f"**{len(packages)} paket ditemukan**")
    
    if packages:
        for pkg in packages:
            render_package_card(pkg)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"📋 Detail", key=f"detail_{pkg.id}"):
                    st.info(f"Detail paket {pkg.name} akan ditampilkan")
    else:
        st.info("Tidak ada paket yang sesuai dengan filter. Coba ubah kriteria pencarian.")


def render_booking_simulator():
    """Render booking cost simulator"""
    
    st.markdown("### 🧮 Simulator Booking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_people = st.number_input("👥 Jumlah Jamaah", min_value=1, max_value=50, value=1)
        departure_date = st.date_input("📅 Tanggal Berangkat")
    
    with col2:
        package_type = st.selectbox(
            "📦 Tipe Paket",
            ["Ekonomis", "Standard", "Premium", "VIP"]
        )
        
        add_ons = st.multiselect(
            "➕ Tambahan",
            ["Asuransi Perjalanan", "Handling Khusus", "Koper Umrah Set", "Kursi Roda"]
        )
    
    # Calculate
    base_prices = {
        "Ekonomis": 22_500_000,
        "Standard": 28_000_000,
        "Premium": 38_500_000,
        "VIP": 55_000_000
    }
    
    add_on_prices = {
        "Asuransi Perjalanan": 500_000,
        "Handling Khusus": 1_500_000,
        "Koper Umrah Set": 750_000,
        "Kursi Roda": 2_000_000
    }
    
    base_price = base_prices.get(package_type, 28_000_000)
    add_on_total = sum(add_on_prices.get(a, 0) for a in add_ons)
    per_person = base_price + add_on_total
    total = per_person * num_people
    
    # Display result
    st.markdown("---")
    st.markdown("#### 💰 Estimasi Biaya")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); 
                border-radius: 15px; padding: 20px; border: 1px solid #D4AF3750;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #C9A86C;">Paket {package_type}</span>
            <span style="color: white;">Rp {base_price:,.0f}</span>
        </div>
        {"".join([f'<div style="display: flex; justify-content: space-between; margin-bottom: 5px;"><span style="color: #888;">+ {a}</span><span style="color: #4CAF50;">Rp {add_on_prices.get(a, 0):,.0f}</span></div>' for a in add_ons])}
        <div style="border-top: 1px solid #D4AF3730; margin: 15px 0; padding-top: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: #C9A86C;">Per Orang</span>
                <span style="color: white; font-weight: 600;">Rp {per_person:,.0f}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #C9A86C;">× {num_people} jamaah</span>
                <span style="color: #D4AF37; font-size: 1.3rem; font-weight: 700;">Rp {total:,.0f}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📧 Kirim Inquiry", use_container_width=True, type="primary"):
        st.success("✅ Inquiry telah dikirim! Tim kami akan menghubungi Anda.")
