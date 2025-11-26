"""
Booking Features for Umrah Planner AI
=====================================
Flight, Hotel, Transportation, Visa, and Package Booking Features
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

# ============================================
# 1. FLIGHT SEARCH & BOOKING
# ============================================

FLIGHT_DATA = {
    "airlines": [
        {
            "name": "Garuda Indonesia",
            "code": "GA",
            "logo": "🇮🇩",
            "type": "Premium",
            "rating": 4.8,
            "direct": True,
            "base_price": 12000000,
            "baggage": "30kg + 7kg cabin",
            "meal": "Halal meal included"
        },
        {
            "name": "Saudi Arabian Airlines",
            "code": "SV",
            "logo": "🇸🇦",
            "type": "Premium",
            "rating": 4.5,
            "direct": True,
            "base_price": 10000000,
            "baggage": "25kg + 7kg cabin",
            "meal": "Halal meal included"
        },
        {
            "name": "Emirates",
            "code": "EK",
            "logo": "🇦🇪",
            "type": "Luxury",
            "rating": 4.9,
            "direct": False,
            "transit": "Dubai (DXB)",
            "base_price": 15000000,
            "baggage": "35kg + 7kg cabin",
            "meal": "Halal gourmet"
        },
        {
            "name": "Qatar Airways",
            "code": "QR",
            "logo": "🇶🇦",
            "type": "Luxury",
            "rating": 4.9,
            "direct": False,
            "transit": "Doha (DOH)",
            "base_price": 14000000,
            "baggage": "35kg + 7kg cabin",
            "meal": "Halal gourmet"
        },
        {
            "name": "Etihad Airways",
            "code": "EY",
            "logo": "🇦🇪",
            "type": "Luxury",
            "rating": 4.7,
            "direct": False,
            "transit": "Abu Dhabi (AUH)",
            "base_price": 13000000,
            "baggage": "30kg + 7kg cabin",
            "meal": "Halal meal included"
        },
        {
            "name": "Lion Air",
            "code": "JT",
            "logo": "🦁",
            "type": "Budget",
            "rating": 3.5,
            "direct": True,
            "base_price": 7000000,
            "baggage": "20kg + 7kg cabin",
            "meal": "Buy on board"
        },
        {
            "name": "Batik Air",
            "code": "ID",
            "logo": "🛫",
            "type": "Premium Economy",
            "rating": 4.2,
            "direct": True,
            "base_price": 9000000,
            "baggage": "25kg + 7kg cabin",
            "meal": "Halal meal included"
        },
        {
            "name": "Citilink",
            "code": "QG",
            "logo": "🟢",
            "type": "Budget",
            "rating": 3.8,
            "direct": True,
            "base_price": 6500000,
            "baggage": "20kg + 7kg cabin",
            "meal": "Buy on board"
        }
    ],
    "departure_cities": {
        "Jakarta (CGK)": {"add_price": 0, "flight_time": "10h 30m"},
        "Surabaya (SUB)": {"add_price": 500000, "flight_time": "11h 15m"},
        "Medan (KNO)": {"add_price": 1000000, "flight_time": "9h 45m"},
        "Makassar (UPG)": {"add_price": 1500000, "flight_time": "12h 30m"},
        "Denpasar (DPS)": {"add_price": 1200000, "flight_time": "12h"},
        "Bandung (BDO)": {"add_price": 300000, "flight_time": "11h"},
        "Yogyakarta (JOG)": {"add_price": 400000, "flight_time": "11h 30m"},
        "Semarang (SRG)": {"add_price": 350000, "flight_time": "11h 15m"},
        "Palembang (PLM)": {"add_price": 800000, "flight_time": "10h"},
        "Pekanbaru (PKU)": {"add_price": 900000, "flight_time": "9h 30m"},
        "Balikpapan (BPN)": {"add_price": 1800000, "flight_time": "13h"},
        "Aceh (BTJ)": {"add_price": 1100000, "flight_time": "8h 45m"},
    },
    "destinations": {
        "Jeddah (JED)": {"label": "King Abdulaziz International Airport"},
        "Madinah (MED)": {"label": "Prince Mohammad bin Abdulaziz Airport"},
    }
}


def render_flight_search():
    """Render flight search interface"""
    st.markdown("### ✈️ Cari & Booking Tiket Pesawat")
    st.markdown("Bandingkan harga tiket dari berbagai maskapai penerbangan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        departure = st.selectbox(
            "🛫 Kota Keberangkatan",
            options=list(FLIGHT_DATA["departure_cities"].keys()),
            index=0
        )
        
        travel_date = st.date_input(
            "📅 Tanggal Berangkat",
            value=datetime.now() + timedelta(days=30),
            min_value=datetime.now() + timedelta(days=7)
        )
    
    with col2:
        destination = st.selectbox(
            "🛬 Bandara Tujuan",
            options=list(FLIGHT_DATA["destinations"].keys()),
            index=0
        )
        
        passengers = st.number_input(
            "👥 Jumlah Penumpang",
            min_value=1,
            max_value=50,
            value=1
        )
    
    flight_class = st.radio(
        "💺 Kelas Penerbangan",
        options=["Economy", "Business", "First Class"],
        horizontal=True
    )
    
    class_multiplier = {"Economy": 1.0, "Business": 2.5, "First Class": 5.0}
    
    if st.button("🔍 Cari Penerbangan", use_container_width=True, type="primary"):
        st.markdown("---")
        st.markdown("### 📋 Hasil Pencarian")
        
        # Calculate seasonal multiplier
        month = travel_date.month
        if month in [3, 4]:  # Ramadhan
            season_mult = 1.8
            season_label = "🔴 High Season (Ramadhan)"
        elif month in [6, 7, 12]:  # School holiday
            season_mult = 1.4
            season_label = "🟡 Peak Season (Liburan)"
        else:
            season_mult = 1.0
            season_label = "🟢 Regular Season"
        
        st.info(f"**Musim:** {season_label}")
        
        city_data = FLIGHT_DATA["departure_cities"][departure]
        
        # Sort airlines by some logic
        airlines = sorted(FLIGHT_DATA["airlines"], key=lambda x: x["base_price"])
        
        for airline in airlines:
            base = airline["base_price"]
            city_add = city_data["add_price"]
            total = (base + city_add) * class_multiplier[flight_class] * season_mult
            total_all = total * passengers
            
            # Random time variation
            dep_hour = random.randint(1, 23)
            dep_time = f"{dep_hour:02d}:{random.choice(['00', '15', '30', '45'])}"
            
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    **{airline['logo']} {airline['name']}**  
                    {airline['code']} • {airline['type']}  
                    ⭐ {airline['rating']}/5.0
                    """)
                
                with col2:
                    st.markdown(f"""
                    **{dep_time}** → {destination.split()[0]}  
                    ⏱️ {city_data['flight_time']}  
                    {"✈️ Direct" if airline['direct'] else f"🔄 Transit: {airline.get('transit', 'N/A')}"}
                    """)
                
                with col3:
                    st.markdown(f"""
                    🧳 {airline['baggage']}  
                    🍽️ {airline['meal']}
                    """)
                
                with col4:
                    st.markdown(f"""
                    **Rp {total:,.0f}**/org  
                    Total: **Rp {total_all:,.0f}**  
                    """)
                    if st.button(f"Pilih", key=f"book_{airline['code']}", type="secondary"):
                        st.success(f"✅ {airline['name']} dipilih! Lanjutkan ke pembayaran.")
                
                st.markdown("---")
        
        st.caption("*Harga bersifat estimasi dan dapat berubah. Hubungi travel agent untuk konfirmasi.")


# ============================================
# 2. HOTEL BOOKING
# ============================================

HOTEL_DATA = {
    "makkah": [
        {
            "name": "Raffles Makkah Palace",
            "star": 5,
            "distance": "50m dari Haram",
            "view": "Kaabah View",
            "price_min": 8000000,
            "price_max": 25000000,
            "rating": 4.9,
            "amenities": ["🍽️ Restaurant", "🏊 Pool", "💆 Spa", "🅿️ Parking", "📶 WiFi"],
            "breakfast": True,
            "image": "https://images.unsplash.com/photo-1590073242678-70ee3fc28e8e?w=400"
        },
        {
            "name": "Fairmont Makkah Clock Tower",
            "star": 5,
            "distance": "100m dari Haram",
            "view": "Haram View",
            "price_min": 4000000,
            "price_max": 15000000,
            "rating": 4.8,
            "amenities": ["🍽️ Restaurant", "💆 Spa", "🛒 Mall Access", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Swissôtel Makkah",
            "star": 5,
            "distance": "200m dari Haram",
            "view": "City View",
            "price_min": 2500000,
            "price_max": 8000000,
            "rating": 4.7,
            "amenities": ["🍽️ Restaurant", "🛒 Mall Access", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Hilton Suites Makkah",
            "star": 5,
            "distance": "300m dari Haram",
            "view": "City View",
            "price_min": 1800000,
            "price_max": 5000000,
            "rating": 4.6,
            "amenities": ["🍽️ Restaurant", "📶 WiFi", "🏋️ Gym"],
            "breakfast": True
        },
        {
            "name": "Makkah Towers",
            "star": 4,
            "distance": "400m dari Haram",
            "view": "City View",
            "price_min": 800000,
            "price_max": 2500000,
            "rating": 4.3,
            "amenities": ["🍽️ Restaurant", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Al Marwa Rayhaan",
            "star": 4,
            "distance": "500m dari Haram",
            "view": "City View",
            "price_min": 600000,
            "price_max": 1800000,
            "rating": 4.2,
            "amenities": ["🍽️ Restaurant", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Elaf Ajyad Hotel",
            "star": 3,
            "distance": "800m dari Haram",
            "view": "City View",
            "price_min": 350000,
            "price_max": 900000,
            "rating": 4.0,
            "amenities": ["📶 WiFi", "🍽️ Breakfast"],
            "breakfast": True
        },
        {
            "name": "Grand Zamzam Hotel",
            "star": 3,
            "distance": "1km dari Haram",
            "view": "City View",
            "price_min": 300000,
            "price_max": 700000,
            "rating": 3.8,
            "amenities": ["📶 WiFi"],
            "breakfast": False
        }
    ],
    "madinah": [
        {
            "name": "The Oberoi Madinah",
            "star": 5,
            "distance": "100m dari Masjid Nabawi",
            "view": "Masjid Nabawi View",
            "price_min": 5000000,
            "price_max": 15000000,
            "rating": 4.9,
            "amenities": ["🍽️ Restaurant", "💆 Spa", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Dar Al Taqwa Hotel",
            "star": 5,
            "distance": "150m dari Masjid Nabawi",
            "view": "Masjid Nabawi View",
            "price_min": 2500000,
            "price_max": 8000000,
            "rating": 4.7,
            "amenities": ["🍽️ Restaurant", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Crowne Plaza Madinah",
            "star": 5,
            "distance": "300m dari Masjid Nabawi",
            "view": "City View",
            "price_min": 1500000,
            "price_max": 4500000,
            "rating": 4.5,
            "amenities": ["🍽️ Restaurant", "🏋️ Gym", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Millennium Al Aqeeq",
            "star": 4,
            "distance": "400m dari Masjid Nabawi",
            "view": "City View",
            "price_min": 700000,
            "price_max": 2000000,
            "rating": 4.3,
            "amenities": ["🍽️ Restaurant", "📶 WiFi"],
            "breakfast": True
        },
        {
            "name": "Dallah Taibah Hotel",
            "star": 3,
            "distance": "700m dari Masjid Nabawi",
            "view": "City View",
            "price_min": 300000,
            "price_max": 800000,
            "rating": 4.0,
            "amenities": ["📶 WiFi"],
            "breakfast": False
        }
    ]
}


def render_hotel_booking():
    """Render hotel booking interface"""
    st.markdown("### 🏨 Cari & Booking Hotel")
    st.markdown("Temukan hotel terbaik di Makkah dan Madinah")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        city = st.selectbox(
            "📍 Kota",
            options=["Makkah", "Madinah"],
            index=0
        )
    
    with col2:
        check_in = st.date_input(
            "📅 Check-in",
            value=datetime.now() + timedelta(days=30)
        )
    
    with col3:
        nights = st.number_input(
            "🌙 Jumlah Malam",
            min_value=1,
            max_value=30,
            value=5
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        rooms = st.number_input("🚪 Jumlah Kamar", min_value=1, max_value=20, value=1)
    
    with col2:
        star_filter = st.multiselect(
            "⭐ Filter Bintang",
            options=[3, 4, 5],
            default=[3, 4, 5]
        )
    
    sort_by = st.radio(
        "Urutkan berdasarkan",
        options=["Harga Terendah", "Rating Tertinggi", "Jarak Terdekat"],
        horizontal=True
    )
    
    if st.button("🔍 Cari Hotel", use_container_width=True, type="primary"):
        st.markdown("---")
        st.markdown(f"### 🏨 Hotel di {city}")
        
        hotels = HOTEL_DATA[city.lower()]
        
        # Filter by star
        hotels = [h for h in hotels if h["star"] in star_filter]
        
        # Sort
        if sort_by == "Harga Terendah":
            hotels = sorted(hotels, key=lambda x: x["price_min"])
        elif sort_by == "Rating Tertinggi":
            hotels = sorted(hotels, key=lambda x: x["rating"], reverse=True)
        else:
            # Sort by distance (extract number from distance string)
            hotels = sorted(hotels, key=lambda x: int(''.join(filter(str.isdigit, x["distance"][:5]))))
        
        for hotel in hotels:
            with st.container():
                col1, col2, col3 = st.columns([3, 3, 2])
                
                with col1:
                    stars = "⭐" * hotel["star"]
                    st.markdown(f"""
                    ### {hotel['name']}
                    {stars} • ⭐ {hotel['rating']}/5.0  
                    📍 {hotel['distance']}  
                    🏙️ {hotel['view']}
                    """)
                
                with col2:
                    st.markdown("**Fasilitas:**")
                    st.markdown(" ".join(hotel["amenities"]))
                    if hotel["breakfast"]:
                        st.markdown("✅ Termasuk sarapan")
                
                with col3:
                    price_per_night = (hotel["price_min"] + hotel["price_max"]) // 2
                    total_price = price_per_night * nights * rooms
                    
                    st.markdown(f"""
                    **Rp {price_per_night:,.0f}**/malam  
                    {nights} malam × {rooms} kamar  
                    
                    **Total: Rp {total_price:,.0f}**
                    """)
                    
                    if st.button(f"Booking", key=f"hotel_{hotel['name'][:10]}", type="secondary"):
                        st.success(f"✅ {hotel['name']} dipilih!")
                
                st.markdown("---")
        
        st.caption("*Harga bersifat estimasi. Hubungi travel agent untuk ketersediaan dan harga aktual.")


# ============================================
# 3. GROUND TRANSPORTATION
# ============================================

TRANSPORT_DATA = {
    "types": [
        {
            "name": "Bus AC Standard",
            "icon": "🚌",
            "capacity": "40-45 orang",
            "price_per_day": 150000,
            "features": ["AC", "Reclining Seat"],
            "suitable_for": "Rombongan besar"
        },
        {
            "name": "Bus VIP Executive",
            "icon": "🚍",
            "capacity": "25-30 orang",
            "price_per_day": 300000,
            "features": ["AC", "Leg Room Extra", "Snack", "WiFi"],
            "suitable_for": "Premium package"
        },
        {
            "name": "Hiace / Minibus",
            "icon": "🚐",
            "capacity": "10-14 orang",
            "price_per_day": 250000,
            "features": ["AC", "Fleksibel"],
            "suitable_for": "Keluarga / grup kecil"
        },
        {
            "name": "Mobil Sedan (Private)",
            "icon": "🚗",
            "capacity": "3-4 orang",
            "price_per_day": 400000,
            "features": ["AC", "Private", "Fleksibel"],
            "suitable_for": "Keluarga kecil / VIP"
        },
        {
            "name": "SUV Premium (Private)",
            "icon": "🚙",
            "capacity": "5-6 orang",
            "price_per_day": 600000,
            "features": ["AC", "Private", "Spacious", "Luggage"],
            "suitable_for": "VIP / Jamaah senior"
        },
        {
            "name": "GMC / Van Mewah",
            "icon": "🛻",
            "capacity": "7-8 orang",
            "price_per_day": 800000,
            "features": ["AC", "Luxury Interior", "Captain Seat"],
            "suitable_for": "VIP Exclusive"
        }
    ],
    "routes": [
        {"name": "Jeddah Airport → Makkah Hotel", "distance": "80 km", "duration": "1.5 jam"},
        {"name": "Makkah → Madinah", "distance": "450 km", "duration": "5 jam"},
        {"name": "Madinah Hotel → Madinah Airport", "distance": "15 km", "duration": "30 menit"},
        {"name": "City Tour Makkah", "distance": "Full day", "duration": "8 jam"},
        {"name": "City Tour Madinah", "distance": "Full day", "duration": "8 jam"},
        {"name": "Ziarah Jabal Nur & Jabal Tsur", "distance": "Half day", "duration": "4 jam"},
    ]
}


def render_transport_booking():
    """Render ground transportation booking"""
    st.markdown("### 🚐 Booking Transportasi Darat")
    st.markdown("Sewa kendaraan untuk mobilitas selama di tanah suci")
    
    col1, col2 = st.columns(2)
    
    with col1:
        transport_type = st.selectbox(
            "🚗 Jenis Kendaraan",
            options=[t["name"] for t in TRANSPORT_DATA["types"]],
            index=0
        )
        
        selected_transport = next(t for t in TRANSPORT_DATA["types"] if t["name"] == transport_type)
        
        st.info(f"""
        **{selected_transport['icon']} {selected_transport['name']}**  
        👥 Kapasitas: {selected_transport['capacity']}  
        ✅ {', '.join(selected_transport['features'])}  
        📋 Cocok untuk: {selected_transport['suitable_for']}
        """)
    
    with col2:
        route = st.selectbox(
            "📍 Rute Perjalanan",
            options=[r["name"] for r in TRANSPORT_DATA["routes"]],
            index=0
        )
        
        selected_route = next(r for r in TRANSPORT_DATA["routes"] if r["name"] == route)
        
        st.info(f"""
        **{route}**  
        📏 Jarak: {selected_route['distance']}  
        ⏱️ Estimasi: {selected_route['duration']}
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        travel_date = st.date_input(
            "📅 Tanggal",
            value=datetime.now() + timedelta(days=30)
        )
    
    with col2:
        num_passengers = st.number_input(
            "👥 Jumlah Penumpang",
            min_value=1,
            max_value=50,
            value=4
        )
    
    # Calculate price
    price = selected_transport["price_per_day"]
    
    st.markdown("---")
    st.markdown(f"""
    ### 💰 Estimasi Biaya
    
    | Item | Harga |
    |------|-------|
    | {selected_transport['name']} | Rp {price:,.0f}/hari |
    | Rute: {route} | - |
    | **Total** | **Rp {price:,.0f}** |
    """)
    
    if st.button("📝 Booking Sekarang", use_container_width=True, type="primary"):
        st.success("✅ Request booking berhasil! Tim kami akan menghubungi Anda.")
        st.balloons()


# ============================================
# 4. TRAVEL PACKAGE COMPARISON
# ============================================

TRAVEL_PACKAGES = [
    {
        "agent": "PT. Patuna Mekar Jaya",
        "package": "Umrah Reguler 9 Hari",
        "type": "Ekonomis",
        "price": 28000000,
        "rating": 4.5,
        "reviews": 1250,
        "includes": [
            "✈️ Tiket pesawat PP",
            "🏨 Hotel *3 Makkah & Madinah",
            "🚌 Transportasi AC",
            "🍽️ Makan 3x sehari",
            "📋 Visa & handling",
            "👤 Muthawwif berpengalaman"
        ],
        "departure": ["Januari", "Februari", "Maret"]
    },
    {
        "agent": "PT. Al Khalid",
        "package": "Umrah Plus 12 Hari",
        "type": "Standard",
        "price": 38000000,
        "rating": 4.6,
        "reviews": 890,
        "includes": [
            "✈️ Tiket Garuda Indonesia",
            "🏨 Hotel *4 (300m dari Haram)",
            "🚐 Bus VIP Executive",
            "🍽️ Makan menu Indonesia",
            "📋 Visa & asuransi premium",
            "👤 Tour leader dari Indonesia",
            "🎒 Perlengkapan umrah lengkap"
        ],
        "departure": ["Februari", "April", "Juni"]
    },
    {
        "agent": "PT. Arminareka Perdana",
        "package": "Umrah Premium 14 Hari",
        "type": "Premium",
        "price": 55000000,
        "rating": 4.8,
        "reviews": 2100,
        "includes": [
            "✈️ Tiket Garuda (kelas bisnis)",
            "🏨 Hotel *5 (View Haram)",
            "🚙 Private car 24 jam",
            "🍽️ Fine dining halal",
            "📋 Fast track airport",
            "👨‍⚕️ Pendamping medis",
            "📿 Umrah plus ziarah lengkap"
        ],
        "departure": ["Setiap bulan"]
    },
    {
        "agent": "PT. Maktour",
        "package": "Umrah VIP Exclusive",
        "type": "VIP",
        "price": 95000000,
        "rating": 4.9,
        "reviews": 450,
        "includes": [
            "✈️ First Class / Business",
            "🏨 Fairmont/Raffles (Haram View)",
            "🛻 GMC Private",
            "🍽️ Private chef menu pilihan",
            "🏥 Dokter & perawat pribadi",
            "👤 Personal assistant 24/7",
            "🎁 Gift exclusive"
        ],
        "departure": ["Fleksibel"]
    },
    {
        "agent": "PT. Ebad Al-Rahman",
        "package": "Umrah Ramadhan 14 Hari",
        "type": "Ramadhan Special",
        "price": 65000000,
        "rating": 4.7,
        "reviews": 780,
        "includes": [
            "✈️ Tiket Saudi Airlines",
            "🏨 Hotel *4 dekat Haram",
            "🚌 Transportasi VIP",
            "🍽️ Sahur & Iftar di hotel",
            "📿 Tarawih di Masjidil Haram",
            "📋 Handling lengkap"
        ],
        "departure": ["Ramadhan"]
    }
]


def render_package_comparison():
    """Render travel package comparison"""
    st.markdown("### 📦 Bandingkan Paket Travel Umrah")
    st.markdown("Temukan paket terbaik dari travel agent terpercaya")
    
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.slider(
            "💰 Budget (Juta Rupiah)",
            min_value=20,
            max_value=150,
            value=(25, 80),
            step=5
        )
    
    with col2:
        package_type = st.multiselect(
            "📦 Tipe Paket",
            options=["Ekonomis", "Standard", "Premium", "VIP", "Ramadhan Special"],
            default=["Ekonomis", "Standard", "Premium"]
        )
    
    sort_by = st.radio(
        "Urutkan",
        options=["Harga Terendah", "Rating Tertinggi", "Review Terbanyak"],
        horizontal=True
    )
    
    if st.button("🔍 Cari Paket", use_container_width=True, type="primary"):
        st.markdown("---")
        
        # Filter
        packages = [p for p in TRAVEL_PACKAGES 
                   if budget[0] * 1000000 <= p["price"] <= budget[1] * 1000000
                   and p["type"] in package_type]
        
        # Sort
        if sort_by == "Harga Terendah":
            packages = sorted(packages, key=lambda x: x["price"])
        elif sort_by == "Rating Tertinggi":
            packages = sorted(packages, key=lambda x: x["rating"], reverse=True)
        else:
            packages = sorted(packages, key=lambda x: x["reviews"], reverse=True)
        
        if not packages:
            st.warning("Tidak ada paket yang sesuai filter. Coba ubah kriteria pencarian.")
            return
        
        for pkg in packages:
            with st.container():
                col1, col2, col3 = st.columns([3, 3, 2])
                
                with col1:
                    st.markdown(f"""
                    ### {pkg['package']}
                    **{pkg['agent']}**  
                    📦 {pkg['type']} • ⭐ {pkg['rating']}/5.0 ({pkg['reviews']} reviews)
                    """)
                
                with col2:
                    st.markdown("**Termasuk:**")
                    for item in pkg["includes"][:5]:
                        st.markdown(f"• {item}")
                    if len(pkg["includes"]) > 5:
                        st.markdown(f"• +{len(pkg['includes'])-5} lainnya...")
                
                with col3:
                    st.markdown(f"""
                    ### Rp {pkg['price']/1000000:.0f} Juta
                    per orang
                    
                    📅 Keberangkatan:  
                    {', '.join(pkg['departure'][:2])}
                    """)
                    
                    if st.button("📞 Hubungi", key=f"pkg_{pkg['agent'][:10]}", type="secondary"):
                        st.info(f"Hubungi {pkg['agent']} untuk info lebih lanjut")
                
                st.markdown("---")


# ============================================
# 5. VISA PROCESSING TRACKER
# ============================================

def render_visa_tracker():
    """Render visa processing tracker"""
    st.markdown("### 🛂 Tracker Proses Visa Umrah")
    st.markdown("Pantau status pemrosesan visa umrah Anda")
    
    # Simulated visa tracking
    st.markdown("#### 📋 Masukkan Data Visa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        passport_no = st.text_input("🛂 Nomor Paspor", placeholder="A1234567")
        name = st.text_input("👤 Nama Lengkap (sesuai paspor)", placeholder="JOHN DOE")
    
    with col2:
        travel_agent = st.selectbox(
            "🏢 Travel Agent",
            options=["PT. Patuna Mekar Jaya", "PT. Al Khalid", "PT. Arminareka Perdana", 
                    "PT. Maktour", "PT. Ebad Al-Rahman", "Lainnya"]
        )
        submission_date = st.date_input("📅 Tanggal Pengajuan", value=datetime.now() - timedelta(days=7))
    
    if st.button("🔍 Cek Status", use_container_width=True, type="primary"):
        st.markdown("---")
        
        # Simulate status (random for demo)
        days_elapsed = (datetime.now().date() - submission_date).days
        
        if days_elapsed < 3:
            current_step = 1
            status = "📝 Dokumen Diterima"
            status_color = "blue"
        elif days_elapsed < 5:
            current_step = 2
            status = "🔍 Verifikasi Dokumen"
            status_color = "blue"
        elif days_elapsed < 7:
            current_step = 3
            status = "📤 Dikirim ke Kedutaan"
            status_color = "orange"
        elif days_elapsed < 10:
            current_step = 4
            status = "⏳ Proses di Kedutaan Saudi"
            status_color = "orange"
        elif days_elapsed < 14:
            current_step = 5
            status = "✅ Visa Disetujui"
            status_color = "green"
        else:
            current_step = 6
            status = "🎉 Visa Siap Diambil"
            status_color = "green"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #4CAF50, #2196F3);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        ">
            <h3 style="margin: 0;">Status: {status}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 📊 Progress Visa")
        
        steps = [
            ("📝 Dokumen Diterima", "Dokumen telah diterima oleh travel agent"),
            ("🔍 Verifikasi", "Pengecekan kelengkapan dokumen"),
            ("📤 Pengiriman", "Dokumen dikirim ke KJRI/Kedutaan"),
            ("⏳ Proses Kedutaan", "Visa diproses oleh pihak Saudi Arabia"),
            ("✅ Approval", "Visa telah disetujui"),
            ("🎉 Selesai", "Visa siap diambil/dikirim"),
        ]
        
        for i, (step_name, step_desc) in enumerate(steps, 1):
            if i < current_step:
                st.markdown(f"✅ **{step_name}** - Selesai")
            elif i == current_step:
                st.markdown(f"🔄 **{step_name}** - _Sedang diproses_")
            else:
                st.markdown(f"⬜ {step_name}")
        
        st.progress(current_step / 6)
        
        st.markdown("---")
        st.markdown("""
        #### 📞 Butuh Bantuan?
        - Hubungi travel agent Anda untuk info lebih detail
        - Estimasi proses visa: 7-14 hari kerja
        - Pastikan semua dokumen sudah lengkap
        """)


# ============================================
# 6. PAYMENT CALCULATOR WITH INSTALLMENTS
# ============================================

def render_payment_calculator():
    """Render payment installment calculator"""
    st.markdown("### 💳 Kalkulator Cicilan Pembayaran")
    st.markdown("Hitung skema cicilan untuk pembayaran paket umrah")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_cost = st.number_input(
            "💰 Total Biaya Paket (Rp)",
            min_value=20000000,
            max_value=200000000,
            value=35000000,
            step=1000000,
            format="%d"
        )
        
        dp_percent = st.slider(
            "📊 Down Payment (%)",
            min_value=10,
            max_value=50,
            value=30,
            step=5
        )
    
    with col2:
        num_installments = st.selectbox(
            "📅 Jumlah Cicilan (Bulan)",
            options=[3, 6, 9, 12],
            index=1
        )
        
        departure_date = st.date_input(
            "✈️ Tanggal Keberangkatan",
            value=datetime.now() + timedelta(days=180)
        )
    
    # Calculate
    dp_amount = total_cost * dp_percent / 100
    remaining = total_cost - dp_amount
    monthly_installment = remaining / num_installments
    
    # Check if enough time
    days_until_departure = (departure_date - datetime.now().date()).days
    months_until_departure = days_until_departure // 30
    
    st.markdown("---")
    st.markdown("### 📋 Rincian Pembayaran")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Down Payment", f"Rp {dp_amount:,.0f}", f"{dp_percent}%")
    
    with col2:
        st.metric("Cicilan/Bulan", f"Rp {monthly_installment:,.0f}", f"{num_installments}x")
    
    with col3:
        st.metric("Total Bayar", f"Rp {total_cost:,.0f}")
    
    # Payment schedule
    st.markdown("---")
    st.markdown("### 📆 Jadwal Pembayaran")
    
    schedule_data = []
    current_date = datetime.now().date()
    
    # DP
    schedule_data.append({
        "Pembayaran": "Down Payment",
        "Tanggal": current_date.strftime("%d %b %Y"),
        "Jumlah": f"Rp {dp_amount:,.0f}",
        "Status": "🔴 Belum Bayar"
    })
    
    # Installments
    for i in range(num_installments):
        pay_date = current_date + timedelta(days=30 * (i + 1))
        schedule_data.append({
            "Pembayaran": f"Cicilan {i+1}",
            "Tanggal": pay_date.strftime("%d %b %Y"),
            "Jumlah": f"Rp {monthly_installment:,.0f}",
            "Status": "⬜ Pending"
        })
    
    import pandas as pd
    df = pd.DataFrame(schedule_data)
    st.table(df)
    
    # Warnings
    if months_until_departure < num_installments:
        st.error(f"""
        ⚠️ **Perhatian:** Waktu tidak cukup!
        
        Anda memilih cicilan {num_installments} bulan, tapi keberangkatan hanya {months_until_departure} bulan lagi.
        Silakan pilih tenor yang lebih pendek atau ubah tanggal keberangkatan.
        """)
    else:
        st.success(f"""
        ✅ **Jadwal OK!**
        
        Pelunasan akan selesai {num_installments} bulan sebelum keberangkatan.
        Anda masih punya {months_until_departure - num_installments} bulan buffer.
        """)
    
    st.markdown("---")
    st.info("""
    💡 **Tips:**
    - Beberapa travel agent menawarkan cicilan 0% dengan kartu kredit tertentu
    - Tanyakan promo early bird untuk diskon tambahan
    - Pastikan memiliki dana darurat selain cicilan umrah
    """)


# ============================================
# 7. PACKING WEIGHT CALCULATOR
# ============================================

def render_packing_calculator():
    """Render packing weight calculator"""
    st.markdown("### 🧳 Kalkulator Berat Koper")
    st.markdown("Pastikan bagasi Anda tidak overweight!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        baggage_limit = st.selectbox(
            "✈️ Batas Bagasi Maskapai",
            options=[20, 23, 25, 30, 35, 40],
            index=2,
            format_func=lambda x: f"{x} kg"
        )
    
    with col2:
        num_people = st.number_input("👥 Jumlah Jamaah", min_value=1, max_value=10, value=1)
    
    st.markdown("---")
    st.markdown("### 📦 Estimasi Berat Barang")
    
    items = {
        "Pakaian (per set)": {"unit_weight": 0.5, "default_qty": 7},
        "Ihram/Mukena (set)": {"unit_weight": 0.8, "default_qty": 2},
        "Perlengkapan mandi": {"unit_weight": 1.5, "default_qty": 1},
        "Obat-obatan": {"unit_weight": 0.5, "default_qty": 1},
        "Sepatu/sandal": {"unit_weight": 1.0, "default_qty": 2},
        "Buku doa/Al-Quran": {"unit_weight": 0.5, "default_qty": 2},
        "Snack dari Indonesia": {"unit_weight": 2.0, "default_qty": 1},
        "Air Zamzam (untuk pulang)": {"unit_weight": 5.0, "default_qty": 1},
        "Oleh-oleh (pulang)": {"unit_weight": 5.0, "default_qty": 1},
        "Elektronik (HP, charger, dll)": {"unit_weight": 1.0, "default_qty": 1},
    }
    
    total_weight = 0
    weights_detail = []
    
    for item, data in items.items():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(item)
        
        with col2:
            qty = st.number_input(
                "Qty",
                min_value=0,
                max_value=20,
                value=data["default_qty"],
                key=f"qty_{item}",
                label_visibility="collapsed"
            )
        
        weight = qty * data["unit_weight"]
        total_weight += weight
        
        with col3:
            st.write(f"{weight:.1f} kg")
        
        if weight > 0:
            weights_detail.append({"Item": item, "Berat": weight})
    
    st.markdown("---")
    
    # Result
    total_allowed = baggage_limit * num_people
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Berat", f"{total_weight:.1f} kg")
    
    with col2:
        st.metric("Batas Bagasi", f"{total_allowed} kg", f"{num_people} orang")
    
    with col3:
        remaining = total_allowed - total_weight
        delta_color = "normal" if remaining >= 0 else "inverse"
        st.metric(
            "Sisa Kapasitas", 
            f"{remaining:.1f} kg",
            delta="OK" if remaining >= 0 else "OVERWEIGHT!"
        )
    
    # Progress bar
    usage = total_weight / total_allowed
    st.progress(min(usage, 1.0))
    
    if usage > 1:
        st.error(f"""
        ⚠️ **OVERWEIGHT {total_weight - total_allowed:.1f} kg!**
        
        Tips:
        - Kurangi barang yang tidak perlu
        - Pertimbangkan beli oleh-oleh di Saudi (biasanya lebih murah)
        - Bawa Air Zamzam di tas jinjing (free 5L per orang)
        """)
    elif usage > 0.9:
        st.warning("⚠️ Hampir penuh! Sisakan ruang untuk oleh-oleh pulang.")
    else:
        st.success("✅ Berat bagasi aman!")


# ============================================
# MAIN RENDER FUNCTION
# ============================================

def render_booking_features():
    """Main function to render all booking features"""
    
    feature = st.selectbox(
        "🎯 Pilih Fitur Booking",
        options=[
            "✈️ Cari Penerbangan",
            "🏨 Booking Hotel",
            "🚐 Transportasi Darat",
            "📦 Bandingkan Paket Travel",
            "🛂 Tracker Visa",
            "💳 Kalkulator Cicilan",
            "🧳 Kalkulator Berat Koper",
        ],
        index=0
    )
    
    st.markdown("---")
    
    if "Penerbangan" in feature:
        render_flight_search()
    elif "Hotel" in feature:
        render_hotel_booking()
    elif "Transportasi" in feature:
        render_transport_booking()
    elif "Paket" in feature:
        render_package_comparison()
    elif "Visa" in feature:
        render_visa_tracker()
    elif "Cicilan" in feature:
        render_payment_calculator()
    elif "Berat" in feature:
        render_packing_calculator()