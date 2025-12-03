"""
LABBAIK Configuration Module
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
    """Application configuration"""
    name: str = "LABBAIK"
    version: str = "3.5.0"
    description: str = "Platform Perencanaan Umrah Cerdas"
    debug: bool = False

@dataclass  
class LLMConfig:
    """LLM Provider configuration"""
    provider: str = "groq"
    groq_api_key: str = ""
    openai_api_key: str = ""
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    def __post_init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")

# Scenario templates for budget simulation
SCENARIO_TEMPLATES = {
    "ekonomis": {
        "name": "Ekonomis",
        "description": "Budget hemat, hotel 3-star, tanpa makan",
        "flight_class": "economy",
        "hotel_star": 3,
        "include_meals": False,
        "multiplier": 1.0
    },
    "standard": {
        "name": "Standard", 
        "description": "Kelas menengah, hotel 4-star, dengan makan",
        "flight_class": "economy",
        "hotel_star": 4,
        "include_meals": True,
        "multiplier": 1.3
    },
    "premium": {
        "name": "Premium",
        "description": "Kenyamanan ekstra, hotel 5-star dekat Masjid",
        "flight_class": "business",
        "hotel_star": 5,
        "include_meals": True,
        "multiplier": 1.8
    },
    "vip": {
        "name": "VIP",
        "description": "Layanan terbaik, hotel bintang 5 premium",
        "flight_class": "business",
        "hotel_star": 5,
        "include_meals": True,
        "multiplier": 2.5
    }
}

# Departure cities with price multipliers
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

# Season price multipliers
SEASONS = {
    "low": {
        "name": "Low Season",
        "months": [1, 2, 6, 7],
        "multiplier": 0.85,
        "description": "Harga lebih murah, masjid tidak terlalu ramai"
    },
    "regular": {
        "name": "Regular Season",
        "months": [3, 4, 5, 8, 9, 10, 11],
        "multiplier": 1.0,
        "description": "Harga normal, keramaian sedang"
    },
    "high": {
        "name": "High Season",
        "months": [12],
        "multiplier": 1.4,
        "description": "Harga tinggi, sangat ramai (liburan)"
    },
    "ramadan": {
        "name": "Ramadan",
        "months": [],  # Dynamic based on Islamic calendar
        "multiplier": 1.6,
        "description": "Harga tertinggi, pahala berlipat"
    }
}

# Initialize configs
app_config = AppConfig()
llm_config = LLMConfig()
