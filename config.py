"""
Configuration Module for Umrah Planner
======================================
Centralized configuration management using environment variables
"""

import os
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)


class LLMConfig(BaseModel):
    """LLM Configuration"""
    provider: Literal["groq", "openai"] = Field(
        default=os.getenv("LLM_PROVIDER", "groq")
    )
    groq_api_key: str = Field(default=os.getenv("GROQ_API_KEY", ""))
    openai_api_key: str = Field(default=os.getenv("OPENAI_API_KEY", ""))
    groq_model: str = Field(
        default=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    )
    openai_model: str = Field(
        default=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    temperature: float = 0.7
    max_tokens: int = 4096


class EmbeddingConfig(BaseModel):
    """Embedding Configuration"""
    model_name: str = Field(
        default=os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    )
    chunk_size: int = 500
    chunk_overlap: int = 50


class CurrencyConfig(BaseModel):
    """Currency Configuration"""
    default_currency: str = Field(
        default=os.getenv("DEFAULT_CURRENCY", "IDR")
    )
    usd_to_idr: float = Field(
        default=float(os.getenv("USD_TO_IDR_RATE", "15500"))
    )
    sar_to_idr: float = Field(default=4130.0)  # Saudi Riyal to IDR


class AppConfig(BaseModel):
    """Application Configuration"""
    debug: bool = Field(
        default=os.getenv("APP_DEBUG", "false").lower() == "true"
    )
    enable_cache: bool = Field(
        default=os.getenv("ENABLE_CACHE", "true").lower() == "true"
    )
    app_name: str = "🕋 Umrah Planner AI"
    version: str = "1.0.0"


# Scenario Templates
SCENARIO_TEMPLATES = {
    "ekonomis": {
        "name": "Ekonomis",
        "description": "Paket hemat dengan fasilitas standar",
        "duration_days": 9,
        "hotel_star_makkah": 3,
        "hotel_star_madinah": 3,
        "hotel_distance_makkah": "800-1500m",
        "hotel_distance_madinah": "500-1000m",
        "meal_type": "prasmanan",
        "transport_type": "bus",
        "price_range_min": 25000000,
        "price_range_max": 32000000,
    },
    "standard": {
        "name": "Standard",
        "description": "Paket menengah dengan kenyamanan lebih",
        "duration_days": 12,
        "hotel_star_makkah": 4,
        "hotel_star_madinah": 4,
        "hotel_distance_makkah": "300-500m",
        "hotel_distance_madinah": "200-500m",
        "meal_type": "prasmanan_plus",
        "transport_type": "bus_ac",
        "price_range_min": 35000000,
        "price_range_max": 45000000,
    },
    "premium": {
        "name": "Premium",
        "description": "Paket mewah dengan fasilitas terbaik",
        "duration_days": 14,
        "hotel_star_makkah": 5,
        "hotel_star_madinah": 5,
        "hotel_distance_makkah": "50-200m",
        "hotel_distance_madinah": "100-300m",
        "meal_type": "menu_pilihan",
        "transport_type": "vip_bus",
        "price_range_min": 55000000,
        "price_range_max": 85000000,
    },
    "vip": {
        "name": "VIP/Exclusive",
        "description": "Paket eksklusif dengan layanan personal",
        "duration_days": 14,
        "hotel_star_makkah": 5,
        "hotel_star_madinah": 5,
        "hotel_distance_makkah": "0-50m (view Masjidil Haram)",
        "hotel_distance_madinah": "0-100m (view Masjid Nabawi)",
        "meal_type": "fine_dining",
        "transport_type": "private_car",
        "price_range_min": 100000000,
        "price_range_max": 200000000,
    },
}

# Cost Components (Base prices in IDR)
COST_COMPONENTS = {
    "visa": {
        "base_price": 2500000,
        "description": "Visa umrah termasuk handling",
    },
    "tiket_pesawat": {
        "ekonomis": {"min": 8000000, "max": 12000000},
        "standard": {"min": 10000000, "max": 15000000},
        "premium": {"min": 15000000, "max": 25000000},
        "vip": {"min": 25000000, "max": 50000000},
    },
    "hotel_makkah_per_night": {
        "bintang_3": {"min": 400000, "max": 800000},
        "bintang_4": {"min": 800000, "max": 1500000},
        "bintang_5": {"min": 1500000, "max": 4000000},
        "bintang_5_premium": {"min": 4000000, "max": 15000000},
    },
    "hotel_madinah_per_night": {
        "bintang_3": {"min": 300000, "max": 600000},
        "bintang_4": {"min": 600000, "max": 1200000},
        "bintang_5": {"min": 1200000, "max": 3000000},
        "bintang_5_premium": {"min": 3000000, "max": 10000000},
    },
    "transportasi": {
        "bus": {"per_day": 100000},
        "bus_ac": {"per_day": 150000},
        "vip_bus": {"per_day": 250000},
        "private_car": {"per_day": 500000},
    },
    "makan_per_day": {
        "prasmanan": {"min": 150000, "max": 200000},
        "prasmanan_plus": {"min": 200000, "max": 300000},
        "menu_pilihan": {"min": 300000, "max": 500000},
        "fine_dining": {"min": 500000, "max": 1000000},
    },
    "muthawwif": {
        "base_per_group": 5000000,
        "premium_per_group": 10000000,
    },
    "perlengkapan": {
        "basic": {"min": 500000, "max": 1000000},
        "standard": {"min": 1000000, "max": 2000000},
        "premium": {"min": 2000000, "max": 5000000},
    },
    "asuransi": {
        "basic": 300000,
        "standard": 500000,
        "premium": 1000000,
    },
    "handling_bandara": {
        "standard": 500000,
        "vip": 1500000,
    },
}

# Airlines commonly used for Umrah
AIRLINES = [
    {"name": "Garuda Indonesia", "code": "GA", "rating": 5, "direct": True},
    {"name": "Saudi Arabian Airlines", "code": "SV", "rating": 4, "direct": True},
    {"name": "Emirates", "code": "EK", "rating": 5, "direct": False},
    {"name": "Qatar Airways", "code": "QR", "rating": 5, "direct": False},
    {"name": "Etihad", "code": "EY", "rating": 5, "direct": False},
    {"name": "Lion Air", "code": "JT", "rating": 3, "direct": True},
    {"name": "Batik Air", "code": "ID", "rating": 4, "direct": True},
]

# Popular Hotels in Makkah
HOTELS_MAKKAH = [
    {
        "name": "Raffles Makkah Palace",
        "star": 5,
        "distance": "50m",
        "price_range": "15000000-25000000",
        "view": "Kaabah View",
    },
    {
        "name": "Fairmont Makkah Clock Tower",
        "star": 5,
        "distance": "100m",
        "price_range": "8000000-15000000",
        "view": "Haram View",
    },
    {
        "name": "Swissotel Al Maqam",
        "star": 5,
        "distance": "200m",
        "price_range": "5000000-10000000",
        "view": "City View",
    },
    {
        "name": "Hilton Suites Makkah",
        "star": 5,
        "distance": "300m",
        "price_range": "3000000-6000000",
        "view": "City View",
    },
    {
        "name": "Makkah Towers",
        "star": 4,
        "distance": "400m",
        "price_range": "1500000-3000000",
        "view": "City View",
    },
    {
        "name": "Al Marwa Rayhaan",
        "star": 4,
        "distance": "500m",
        "price_range": "1000000-2000000",
        "view": "City View",
    },
    {
        "name": "Elaf Ajyad Hotel",
        "star": 3,
        "distance": "800m",
        "price_range": "500000-1000000",
        "view": "City View",
    },
]

# Popular Hotels in Madinah
HOTELS_MADINAH = [
    {
        "name": "The Oberoi Madinah",
        "star": 5,
        "distance": "100m",
        "price_range": "10000000-20000000",
        "view": "Masjid Nabawi View",
    },
    {
        "name": "Dar Al Taqwa Hotel",
        "star": 5,
        "distance": "150m",
        "price_range": "4000000-8000000",
        "view": "Masjid Nabawi View",
    },
    {
        "name": "Crowne Plaza Madinah",
        "star": 5,
        "distance": "300m",
        "price_range": "2500000-5000000",
        "view": "City View",
    },
    {
        "name": "Millennium Al Aqeeq",
        "star": 4,
        "distance": "400m",
        "price_range": "1200000-2500000",
        "view": "City View",
    },
    {
        "name": "Frontel Al Harithia",
        "star": 4,
        "distance": "500m",
        "price_range": "800000-1500000",
        "view": "City View",
    },
    {
        "name": "Dallah Taibah Hotel",
        "star": 3,
        "distance": "700m",
        "price_range": "400000-800000",
        "view": "City View",
    },
]

# Departure cities in Indonesia
DEPARTURE_CITIES = [
    "Jakarta (CGK)",
    "Surabaya (SUB)",
    "Medan (KNO)",
    "Makassar (UPG)",
    "Denpasar (DPS)",
    "Bandung (BDO)",
    "Semarang (SRG)",
    "Yogyakarta (JOG)",
    "Palembang (PLM)",
    "Pekanbaru (PKU)",
    "Balikpapan (BPN)",
    "Banjarmasin (BDJ)",
    "Padang (PDG)",
    "Solo (SOC)",
]

# Umrah seasons and pricing multipliers
SEASONS = {
    "ramadhan": {
        "name": "Ramadhan",
        "months": [3, 4],  # Approximate Gregorian months
        "multiplier": 1.8,
        "demand": "Sangat Tinggi",
    },
    "liburan_sekolah": {
        "name": "Liburan Sekolah",
        "months": [6, 7, 12],
        "multiplier": 1.4,
        "demand": "Tinggi",
    },
    "regular": {
        "name": "Regular",
        "months": [1, 2, 5, 8, 9, 10, 11],
        "multiplier": 1.0,
        "demand": "Normal",
    },
}

# Initialize config instances
llm_config = LLMConfig()
embedding_config = EmbeddingConfig()
currency_config = CurrencyConfig()
app_config = AppConfig()
