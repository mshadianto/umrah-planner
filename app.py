"""
================================================================================
لَبَّيْكَ LABBAIK - Main Application
================================================================================

Labbaik Allahumma Labbaik - Aku Datang Memenuhi Panggilan-Mu

Copyright (c) 2025 MS Hadianto. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software is strictly prohibited.

See LICENSE and COPYRIGHT files for full terms.

================================================================================
Platform: AI-Powered Umrah Planning Platform
Version:  3.5.0
Codename: Labbaik
Author:   MS Hadianto
Email:    sopian.hadianto@gmail.com
Website:  labbaik.ai
GitHub:   https://github.com/mshadianto
================================================================================

Version: 3.5.0
Updated: 2025-12-03
Changes: 
- Engagement & Gamification System (Points, Levels, Badges, Streaks)
- Interactive Quiz & Learning Paths
- Viral/Social Sharing Features
- Referral System with Rewards
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Import modules
try:
    from config import (
        app_config, llm_config, SCENARIO_TEMPLATES, 
        DEPARTURE_CITIES, SEASONS
    )
except ImportError:
    # Fallback config
    from dataclasses import dataclass, field
    import os
    
    @dataclass
    class AppConfig:
        name: str = "LABBAIK"
        version: str = "3.5.0"
    
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
        "Bandung": {"code": "BDO", "multiplier": 1.08}
    }
    
    SEASONS = {
        "low": {"name": "Low Season", "multiplier": 0.85},
        "regular": {"name": "Regular", "multiplier": 1.0},
        "high": {"name": "High Season", "multiplier": 1.4}
    }

# ============================================
# ENGAGEMENT SYSTEM (INLINE - always works)
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
    """Initialize engagement state"""
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
    """Generate referral code from user ID"""
    import hashlib
    hash_str = hashlib.md5(str(user_id).encode()).hexdigest()[:8].upper()
    return f"LBK{hash_str}"

def award_points(amount, reason=""):
    """Award points to user"""
    init_engagement_state()
    st.session_state.engagement["points"] += amount

def check_daily_login():
    """Check daily login status"""
    init_engagement_state()
    return {"status": "available" if not st.session_state.engagement.get("daily_claimed") else "claimed"}

def render_daily_reward_popup():
    """Render daily reward popup"""
    pass  # Can be implemented later

def render_engagement_hub():
    """Main engagement hub with proper HTML rendering"""
    init_engagement_state()
    
    points = st.session_state.engagement.get("points", 0)
    streak = st.session_state.engagement.get("streak", 0)
    level = 1 + (points // 500)
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #D4AF37; font-size: 2rem; margin-bottom: 5px;">
            🎮 Pusat Reward & Engagement
        </h1>
        <p style="color: #C9A86C;">
            Kumpulkan poin, unlock badge, dan naik level!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
                    border-radius: 20px; padding: 25px; text-align: center;
                    border: 2px solid #D4AF3740;">
            <div style="font-size: 3rem; margin-bottom: 10px;">⭐</div>
            <div style="color: #D4AF37; font-size: 2.5rem; font-weight: 800;">{points:,}</div>
            <div style="color: #C9A86C;">LABBAIK Points</div>
            <div style="margin-top: 15px; color: #4CAF50; font-weight: 600;">Level {level}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1A1A1A 0%, #3D2817 100%);
                    border-radius: 20px; padding: 25px; text-align: center;
                    border: 2px solid #FF980040;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🔥</div>
            <div style="color: #FF9800; font-size: 2.5rem; font-weight: 800;">{streak}</div>
            <div style="color: #C9A86C;">Hari Berturut-turut</div>
            <div style="margin-top: 15px; color: #C9A86C; font-size: 0.85rem;">Login setiap hari!</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Daily claim button
    if not st.session_state.engagement.get("daily_claimed"):
        if st.button("🎁 Klaim Bonus Harian (+10 LP)", use_container_width=True):
            award_points(10, "Daily login")
            st.session_state.engagement["daily_claimed"] = True
            st.session_state.engagement["streak"] += 1
            st.success("✅ +10 LP diklaim!")
            st.rerun()
    else:
        st.info("✅ Bonus harian sudah diklaim. Kembali besok!")
    
    st.markdown("---")
    
    # Quick challenges
    st.markdown("### 📋 Tantangan Harian")
    
    challenges = [
        {"icon": "🔍", "title": "Lakukan 1x Simulasi", "points": 25, "done": False},
        {"icon": "📱", "title": "Share ke WhatsApp", "points": 50, "done": False},
        {"icon": "📚", "title": "Baca 1 Panduan Manasik", "points": 15, "done": False},
    ]
    
    for ch in challenges:
        status_color = "#4CAF50" if ch["done"] else "#666"
        status_icon = "✅" if ch["done"] else "⬜"
        st.markdown(f"""
        <div style="background: #1A1A1A; border-radius: 12px; padding: 15px; margin-bottom: 10px;
                    border: 1px solid #D4AF3730; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.5rem;">{ch['icon']}</span>
                <span style="color: white;">{ch['title']}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="color: #D4AF37; font-weight: 700;">+{ch['points']} LP</span>
                <span style="color: {status_color};">{status_icon}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

try:
    from social_viral import render_share_buttons
    SOCIAL_AVAILABLE = True
except ImportError:
    SOCIAL_AVAILABLE = False
    def render_share_buttons(*args, **kwargs): pass

# ALWAYS use local render_invite_modal to ensure unsafe_allow_html works
def render_invite_modal(referral_code):
    """Render invite modal with proper HTML rendering"""
    share_url = f"https://labbaik.streamlit.app?ref={referral_code}"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #1E3D2F 100%);
                border-radius: 25px; padding: 30px; margin: 20px 0;
                border: 2px solid #4CAF5040; text-align: center;">
        
        <div style="font-size: 3rem; margin-bottom: 15px;">🎁</div>
        <div style="color: white; font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">
            Ajak Teman, Dapat Bonus!
        </div>
        <div style="color: #C9A86C; margin-bottom: 25px;">
            Kamu dan temanmu masing-masing dapat <strong style="color: #D4AF37;">bonus LP!</strong>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 25px; flex-wrap: wrap;">
            <div style="background: #1A1A1A; border-radius: 15px; padding: 15px 25px;">
                <div style="color: #C9A86C; font-size: 0.8rem;">Kamu Dapat</div>
                <div style="color: #D4AF37; font-size: 1.5rem; font-weight: 700;">+200 LP</div>
            </div>
            <div style="background: #1A1A1A; border-radius: 15px; padding: 15px 25px;">
                <div style="color: #C9A86C; font-size: 0.8rem;">Teman Dapat</div>
                <div style="color: #4CAF50; font-size: 1.5rem; font-weight: 700;">+75 LP</div>
            </div>
        </div>
        
        <div style="background: #1A1A1A; border: 2px dashed #D4AF3750;
                    border-radius: 15px; padding: 15px; margin-bottom: 20px;">
            <div style="color: #C9A86C; font-size: 0.8rem; margin-bottom: 5px;">Kode Referral</div>
            <div style="color: #D4AF37; font-size: 2rem; font-weight: 800; letter-spacing: 4px;">
                {referral_code}
            </div>
        </div>
        
        <div style="background: #2D2D2D; border-radius: 10px; padding: 12px;
                    margin-bottom: 20px;">
            <span style="color: #C9A86C; font-size: 0.85rem; word-break: break-all;">
                {share_url}
            </span>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
            <a href="https://wa.me/?text=Yuk%20rencanakan%20umrah%20bareng%20LABBAIK!%20Pakai%20kode%20{referral_code}%20untuk%20bonus%20LP!%20{share_url}" 
               target="_blank" style="background: #25D366; color: white; padding: 10px 20px; 
               border-radius: 25px; text-decoration: none; font-weight: 600;">
                📱 WhatsApp
            </a>
            <a href="https://t.me/share/url?url={share_url}&text=Yuk%20rencanakan%20umrah%20bareng%20LABBAIK!" 
               target="_blank" style="background: #0088cc; color: white; padding: 10px 20px; 
               border-radius: 25px; text-decoration: none; font-weight: 600;">
                ✈️ Telegram
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

try:
    from quiz_learning import render_quiz_page, init_quiz_state
    QUIZ_AVAILABLE = True
except ImportError:
    QUIZ_AVAILABLE = False
    def render_quiz_page():
        import streamlit as st
        st.info("🧠 Quiz module coming soon!")
    def init_quiz_state(): pass

# ============================================
# AGENTS IMPORT (with fallback for compatibility)
# ============================================
try:
    from agents import AgentOrchestrator
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    
    # Inline fallback AgentOrchestrator
    class AgentOrchestrator:
        """Fallback Agent Orchestrator"""
        def __init__(self, provider="groq"):
            self.provider = provider
            self.conversation_history = []
            self.is_initialized = False
            
            # Try to init Groq client
            try:
                from groq import Groq
                import os
                api_key = os.getenv("GROQ_API_KEY", "")
                self.client = Groq(api_key=api_key) if api_key else None
            except:
                self.client = None
        
        def initialize(self):
            """Initialize the orchestrator"""
            self.is_initialized = True
            return {"status": "success", "message": "Orchestrator initialized"}
        
        def run(self, query, context=None):
            """Run query through LLM"""
            if not self.client:
                return type('Response', (), {
                    'content': "⚠️ API tidak tersedia. Pastikan GROQ_API_KEY sudah dikonfigurasi di Settings.",
                    'agent_name': 'System',
                    'success': False
                })()
            
            try:
                system_prompt = """Anda adalah asisten perencana umrah yang ahli. 
                Bantu pengguna merencanakan perjalanan umrah dengan informasi tentang:
                - Biaya dan budget
                - Manasik dan tata cara ibadah
                - Hotel dan transportasi
                - Visa dan regulasi
                Gunakan bahasa Indonesia yang ramah."""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
                
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    max_tokens=2000,
                    temperature=0.7
                )
                
                return type('Response', (), {
                    'content': response.choices[0].message.content,
                    'agent_name': 'Umrah Assistant',
                    'success': True
                })()
                
            except Exception as e:
                return type('Response', (), {
                    'content': f"Error: {str(e)}",
                    'agent_name': 'System',
                    'success': False
                })()
        
        def clear_history(self):
            self.conversation_history = []
        
        def get_agent_status(self):
            """Get status of all agents"""
            return {
                "status": "active" if self.client else "inactive",
                "provider": self.provider,
                "agents": ["planner", "budget", "manasik", "travel"],
                "api_connected": self.client is not None,
                "total_queries": len(self.conversation_history)
            }
        
        def create_complete_plan(self, scenario="standard", num_people=1, duration_days=9, 
                                  departure_month=None, special_requests=None):
            """Create a complete umrah plan"""
            planner = ScenarioPlanner()
            result = planner.create_scenario(
                scenario_type=scenario,
                num_people=num_people,
                duration_days=duration_days,
                departure_month=departure_month
            )
            
            # Build the plan
            plan = {
                "scenario": result,
                "itinerary": self._generate_itinerary(duration_days),
                "checklist": self._generate_checklist(),
                "special_notes": special_requests or "",
                "status": "success"
            }
            
            return type('Plan', (), plan)()
        
        def _generate_itinerary(self, duration_days):
            """Generate sample itinerary"""
            itinerary = []
            for day in range(1, duration_days + 1):
                if day == 1:
                    itinerary.append({"day": day, "title": "Keberangkatan", "activities": ["Check-in bandara", "Penerbangan ke Jeddah/Madinah"]})
                elif day == 2:
                    itinerary.append({"day": day, "title": "Tiba di Madinah", "activities": ["Check-in hotel", "Ziarah Masjid Nabawi"]})
                elif day <= 4:
                    itinerary.append({"day": day, "title": f"Madinah Hari {day-1}", "activities": ["Sholat di Masjid Nabawi", "Ziarah tempat bersejarah"]})
                elif day == 5:
                    itinerary.append({"day": day, "title": "Perjalanan ke Makkah", "activities": ["Miqat di Bir Ali", "Ihram", "Perjalanan ke Makkah"]})
                elif day == 6:
                    itinerary.append({"day": day, "title": "Umrah", "activities": ["Tawaf", "Sa'i", "Tahallul"]})
                elif day < duration_days:
                    itinerary.append({"day": day, "title": f"Makkah Hari {day-5}", "activities": ["Sholat di Masjidil Haram", "Ibadah sunnah"]})
                else:
                    itinerary.append({"day": day, "title": "Kepulangan", "activities": ["Check-out hotel", "Penerbangan pulang"]})
            return itinerary
        
        def _generate_checklist(self):
            """Generate preparation checklist"""
            return [
                {"category": "Dokumen", "items": ["Paspor (min 6 bulan)", "Visa Umrah", "Tiket pesawat", "Bukti hotel"]},
                {"category": "Pakaian", "items": ["Ihram (pria)", "Mukena (wanita)", "Pakaian harian", "Sandal nyaman"]},
                {"category": "Kesehatan", "items": ["Vaksin meningitis", "Obat pribadi", "Masker", "Hand sanitizer"]},
                {"category": "Lainnya", "items": ["Uang SAR", "Power bank", "Buku doa", "Sajadah travel"]}
            ]

# ============================================
# OTHER MODULE IMPORTS (with fallbacks)
# ============================================
try:
    from scenarios import ScenarioPlanner
except ImportError:
    pass  # Will use fallback below

# Always use this ScenarioPlanner to ensure compatibility
class ScenarioPlanner:
    """ScenarioPlanner with all required methods for app.py"""
    
    BASE_PRICES = {
        "flight": 8000000,
        "visa": 1500000,
        "hotel_3star": 800000,
        "hotel_4star": 1500000,
        "hotel_5star": 3000000,
        "transport": 500000,
        "meals": 300000,
    }
    
    SCENARIO_CONFIGS = {
        "ekonomis": {
            "multiplier": 1.0,
            "hotel_star": 3,
            "features": [
                "Hotel bintang 3 (±500m dari Masjidil Haram)",
                "Penerbangan ekonomi (transit)",
                "Bus transportasi bersama",
                "Makan 3x sehari (catering)",
                "Visa umrah standar",
                "Muthawwif berbahasa Indonesia"
            ]
        },
        "standard": {
            "multiplier": 1.3,
            "hotel_star": 4,
            "features": [
                "Hotel bintang 4 (±300m dari Masjidil Haram)",
                "Penerbangan ekonomi (direct)",
                "Bus AC eksklusif",
                "Makan 3x sehari (prasmanan)",
                "Visa umrah + handling bandara",
                "Muthawwif berpengalaman"
            ]
        },
        "premium": {
            "multiplier": 1.8,
            "hotel_star": 5,
            "features": [
                "Hotel bintang 5 (±100m dari Masjidil Haram)",
                "Penerbangan bisnis class",
                "Private car per keluarga",
                "Makan 3x sehari (fine dining)",
                "Visa umrah + fast track imigrasi",
                "Muthawwif pribadi"
            ]
        },
        "vip": {
            "multiplier": 2.5,
            "hotel_star": 5,
            "features": [
                "Hotel bintang 5 (view Masjidil Haram)",
                "Penerbangan first class",
                "Limousine service",
                "Makan premium + room service",
                "Visa VIP + CIP lounge",
                "Muthawwif eksklusif 24 jam"
            ]
        }
    }
    
    def __init__(self):
        self.scenarios = []
    
    def calculate_budget(self, **kwargs):
        scenario = kwargs.get("scenario_type", kwargs.get("package_type", "standard"))
        num_people = kwargs.get("num_people", 1)
        duration = kwargs.get("duration_days", 9)
        
        config = self.SCENARIO_CONFIGS.get(scenario, self.SCENARIO_CONFIGS["standard"])
        multiplier = config["multiplier"]
        hotel_star = config["hotel_star"]
        
        flight = self.BASE_PRICES["flight"] * multiplier
        visa = self.BASE_PRICES["visa"]
        hotel_key = f"hotel_{hotel_star}star"
        hotel = self.BASE_PRICES.get(hotel_key, self.BASE_PRICES["hotel_4star"]) * duration
        transport = self.BASE_PRICES["transport"] * duration * (0.8 if multiplier > 1.5 else 1)
        meals = self.BASE_PRICES["meals"] * duration * multiplier
        
        per_person = flight + visa + hotel + transport + meals
        total = per_person * num_people
        
        return type('Budget', (), {
            'total': total,
            'per_person': per_person,
            'flight': flight * num_people,
            'visa': visa * num_people,
            'hotel_makkah': hotel * 0.6 * num_people,
            'hotel_madinah': hotel * 0.4 * num_people,
            'transport': transport * num_people,
            'meals': meals * num_people,
            'misc': per_person * 0.05 * num_people,
            'breakdown': {
                'flight': flight * num_people,
                'visa': visa * num_people,
                'hotel': hotel * num_people,
                'transport': transport * num_people,
                'meals': meals * num_people
            }
        })()
    
    def create_scenario(self, scenario_type="standard", num_people=1, duration_days=9, departure_month=None, **kwargs):
        """Create a budget scenario - handles both positional and keyword args"""
        # Handle positional args (scenario_type might be passed as first positional arg)
        if isinstance(scenario_type, str) and scenario_type in self.SCENARIO_CONFIGS:
            pass  # scenario_type is already correct
        
        config = self.SCENARIO_CONFIGS.get(scenario_type, self.SCENARIO_CONFIGS["standard"])
        budget = self.calculate_budget(
            scenario_type=scenario_type,
            num_people=num_people,
            duration_days=duration_days
        )
        
        scenario_names = {
            "ekonomis": "Paket Ekonomis",
            "standard": "Paket Standard", 
            "premium": "Paket Premium",
            "vip": "Paket VIP"
        }
        
        # Season adjustment
        season_multiplier = 1.0
        if departure_month:
            if departure_month in [1, 2, 3]:  # Ramadan period (approximate)
                season_multiplier = 1.4
            elif departure_month in [6, 7, 8]:  # Summer/high season
                season_multiplier = 1.2
            elif departure_month in [4, 5, 10, 11]:  # Shoulder season
                season_multiplier = 1.0
            else:  # Low season
                season_multiplier = 0.9
        
        estimated_base = budget.total * season_multiplier
        
        # Return object with all expected attributes
        return type('ScenarioResult', (), {
            'name': scenario_names.get(scenario_type, "Paket Standard"),
            'scenario_type': scenario_type,
            'num_people': num_people,
            'duration_days': duration_days,
            'total': estimated_base,
            'per_person': estimated_base / num_people,
            'estimated_min': estimated_base * 0.9,
            'estimated_max': estimated_base * 1.1,
            'breakdown': budget.breakdown,
            'monthly_savings': int(estimated_base / 12),
            'features': config["features"],
            'recommendations': [
                "Booking hotel 3-6 bulan sebelumnya untuk harga terbaik",
                "Pilih penerbangan transit untuk hemat biaya",
                "Gunakan travel agent terpercaya dan berizin resmi"
            ],
            'flight': budget.flight,
            'visa': budget.visa,
            'hotel_makkah': budget.hotel_makkah,
            'hotel_madinah': budget.hotel_madinah,
            'transport': budget.transport,
            'meals': budget.meals,
            'misc': budget.misc,
            'package_type': scenario_type,
            'description': f"Estimasi biaya {scenario_names.get(scenario_type, 'Standard')} untuk {num_people} orang, {duration_days} hari",
            # Additional attributes for comparison view
            'hotel_star_makkah': config["hotel_star"],
            'hotel_star_madinah': config["hotel_star"],
            'hotel_distance_makkah': {"ekonomis": "500-800m", "standard": "200-400m", "premium": "50-150m", "vip": "< 50m (View Haram)"}.get(scenario_type, "200-400m"),
            'meal_type': {"ekonomis": "tanpa_makan", "standard": "makan_3x", "premium": "makan_premium", "vip": "all_inclusive"}.get(scenario_type, "makan_3x")
        })()
    
    def compare_scenarios(self, scenarios_list=None, num_people=1, duration_days=9):
        """Compare multiple scenarios"""
        if scenarios_list is None:
            scenarios_list = ["ekonomis", "standard", "premium", "vip"]
        
        results = []
        for scenario in scenarios_list:
            result = self.create_scenario(scenario, num_people, duration_days)
            results.append(result)
        return results
    
    def get_recommendations(self, budget):
        """Get recommendations based on budget"""
        recs = []
        for scenario_type in ["ekonomis", "standard", "premium", "vip"]:
            result = self.create_scenario(scenario_type, 1, 9)
            if result.total <= budget:
                recs.append({
                    "scenario": scenario_type,
                    "name": result.name,
                    "total": result.total,
                    "features": result.features
                })
        return recs
    
    def analyze_best_time(self, priority="balanced"):
        """Analyze best time to perform umrah based on priority"""
        months_data = [
            {"month": 1, "month_name": "Januari", "weather": "Sejuk", "price_multiplier": 0.85, "crowd_level": "Rendah", "recommendation_score": 85},
            {"month": 2, "month_name": "Februari", "weather": "Sejuk", "price_multiplier": 0.85, "crowd_level": "Rendah", "recommendation_score": 85},
            {"month": 3, "month_name": "Maret", "weather": "Hangat", "price_multiplier": 1.6, "crowd_level": "Sangat Tinggi (Ramadan)", "recommendation_score": 60},
            {"month": 4, "month_name": "April", "weather": "Hangat", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 75},
            {"month": 5, "month_name": "Mei", "weather": "Panas", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 70},
            {"month": 6, "month_name": "Juni", "weather": "Panas", "price_multiplier": 1.3, "crowd_level": "Tinggi (Liburan)", "recommendation_score": 55},
            {"month": 7, "month_name": "Juli", "weather": "Sangat Panas", "price_multiplier": 1.4, "crowd_level": "Tinggi (Liburan)", "recommendation_score": 50},
            {"month": 8, "month_name": "Agustus", "weather": "Sangat Panas", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 60},
            {"month": 9, "month_name": "September", "weather": "Hangat", "price_multiplier": 0.85, "crowd_level": "Rendah", "recommendation_score": 90},
            {"month": 10, "month_name": "Oktober", "weather": "Sejuk", "price_multiplier": 0.85, "crowd_level": "Rendah", "recommendation_score": 95},
            {"month": 11, "month_name": "November", "weather": "Sejuk", "price_multiplier": 1.0, "crowd_level": "Sedang", "recommendation_score": 80},
            {"month": 12, "month_name": "Desember", "weather": "Sejuk", "price_multiplier": 1.3, "crowd_level": "Tinggi (Liburan)", "recommendation_score": 65},
        ]
        
        # Adjust scores based on priority
        if priority == "cost":
            for m in months_data:
                m["recommendation_score"] = int(100 - (m["price_multiplier"] * 50))
        elif priority == "crowd":
            crowd_scores = {"Rendah": 100, "Sedang": 70, "Tinggi (Liburan)": 40, "Sangat Tinggi (Ramadan)": 30}
            for m in months_data:
                m["recommendation_score"] = crowd_scores.get(m["crowd_level"], 50)
        
        # Sort by recommendation score
        sorted_months = sorted(months_data, key=lambda x: x["recommendation_score"], reverse=True)
        
        return {
            "best_months": sorted_months[:3],
            "avoid_months": sorted_months[-3:],
            "analysis": months_data,
            "notes": [
                "Oktober-November adalah waktu terbaik untuk biaya dan kenyamanan",
                "Hindari Juni-Juli jika ingin menghindari panas ekstrem",
                "Ramadan (Maret/April) sangat ramai tapi bernilai pahala lebih",
                "Booking 3-6 bulan sebelumnya untuk harga terbaik"
            ],
            "priority": priority
        }

try:
    from utils import format_currency, format_duration
except ImportError:
    def format_currency(amount, currency="Rp"):
        return f"{currency} {amount:,.0f}".replace(",", ".")
    def format_duration(days):
        return f"{days} hari"

try:
    from features import render_additional_features
except ImportError:
    def render_additional_features():
        st.info("Features module not available")

try:
    from booking import render_booking_features
except ImportError:
    def render_booking_features():
        st.info("Booking module not available")

# Version module
try:
    from version import (
        __version__, DEVELOPER, APP_INFO, CHANGELOG, TECH_STACK,
        get_version_badge, get_developer_card, get_changelog_markdown, get_app_age
    )
except ImportError:
    __version__ = "3.5.0"
    DEVELOPER = {"name": "KIM Consulting", "role": "Developer"}
    APP_INFO = {"name": "LABBAIK", "version": __version__}
    CHANGELOG = []
    TECH_STACK = []
    def get_version_badge(): return f"v{__version__}"
    def get_developer_card(): return ""
    def get_changelog_markdown(): return ""
    def get_app_age(): return "0 days"

# Monetization module
try:
    from monetization import (
        render_monetization_page, render_monetization_sidebar,
        render_quick_quote_widget, init_monetization_state, PRICING_TIERS
    )
except ImportError:
    def render_monetization_page(): st.info("Monetization module coming soon")
    def render_monetization_sidebar(): pass
    def render_quick_quote_widget(): pass
    def init_monetization_state(): pass
    PRICING_TIERS = {}

# Auth module
try:
    from auth import (
        init_user_database, is_logged_in, get_current_user, get_user_role_info,
        render_login_page, render_user_badge, render_upgrade_prompt,
        render_admin_dashboard, has_permission, check_limit, increment_usage,
        USER_ROLES, logout_user
    )
except ImportError:
    def init_user_database(): pass
    def is_logged_in(): return False
    def get_current_user(): return None
    def get_user_role_info(role): return {"name": role, "icon": "👤"}
    def render_login_page(): 
        st.warning("Auth module not available")
    def render_user_badge(user): pass
    def render_upgrade_prompt(feature): pass
    def render_admin_dashboard(): pass
    def has_permission(user, perm): return True
    def check_limit(user, limit): return True
    def increment_usage(user, usage): pass
    USER_ROLES = {}
    def logout_user(): pass

# Visitor tracker module
try:
    from visitor_tracker import (
        track_page_view, get_visitor_count, get_page_view_count,
        get_visitor_stats, render_visitor_stats, render_analytics_dashboard
    )
except ImportError:
    def track_page_view(page): pass
    def get_visitor_count(): return 0
    def get_page_view_count(): return 0
    def get_visitor_stats(): return {}
    def render_visitor_stats(): pass
    def render_analytics_dashboard(): st.info("Analytics not available")

# ============================================
# PWA (Progressive Web App) SUPPORT
# ============================================
try:
    from pwa_component import init_pwa, render_install_card, render_pwa_status
    PWA_AVAILABLE = True
except ImportError:
    PWA_AVAILABLE = False
    def init_pwa(): pass
    def render_install_card(): pass
    def render_pwa_status(): pass

# ============================================
# DATABASE INTEGRATION (Neon PostgreSQL)
# ============================================
try:
    from db_integration import (
        is_db_available, hybrid_login, hybrid_register,
        db_get_open_trips, db_create_trip, db_get_user_trips,
        db_update_trip_status, db_delete_trip,
        db_get_forum_posts, db_create_post, db_get_post_comments,
        db_add_comment, db_like_post, db_increment_views,
        db_log_visit, db_get_stats
    )
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

# ============================================
# LABBAIK BRAND CONSTANTS
# ============================================

BRAND = {
    "name": "LABBAIK",
    "arabic": "لَبَّيْكَ",
    "talbiyah": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ",
    "tagline": "Panggilan-Nya, Langkahmu",
    "description": "Platform AI Perencanaan Umrah #1 Indonesia",
    "full_tagline": "Labbaik Allahumma Labbaik - Aku Datang Memenuhi Panggilan-Mu",
    "version": "3.5.0",
}

COLORS = {
    "black": "#1A1A1A",
    "gold": "#D4AF37",
    "gold_light": "#F5E6C8",
    "green": "#006B3C",
    "white": "#FFFFFF",
    "sand": "#C9A86C",
    "blue": "#1E3A5F",
    "gray": "#666666",
}

CONTACT = {
    "email": "sopian.hadianto@gmail.com",
    "whatsapp": "+62 815 9658 833",
    "website": "labbaik.ai",
}

# ============================================
# HOTEL PRICES CONFIGURATION (for Buat Rencana)
# ============================================

HOTEL_PRICES = {
    "ekonomis": {
        "makkah": {"name": "Hotel Bintang 2-3 (1-2 km dari Haram)", "price": 800000},
        "madinah": {"name": "Hotel Bintang 2-3 (500m-1 km dari Nabawi)", "price": 600000}
    },
    "standard": {
        "makkah": {"name": "Hotel Bintang 3-4 (500m-1 km dari Haram)", "price": 1500000},
        "madinah": {"name": "Hotel Bintang 3-4 (300-500m dari Nabawi)", "price": 1000000}
    },
    "premium": {
        "makkah": {"name": "Hotel Bintang 4-5 (200-500m dari Haram)", "price": 2500000},
        "madinah": {"name": "Hotel Bintang 4-5 (100-300m dari Nabawi)", "price": 1800000}
    },
    "vip": {
        "makkah": {"name": "Hotel Bintang 5 (View Ka'bah, <200m)", "price": 5000000},
        "madinah": {"name": "Hotel Bintang 5 (View Masjid Nabawi, <100m)", "price": 3500000}
    }
}

ADDITIONAL_COSTS = {
    "ekonomis": {"flight": 8000000, "visa": 500000, "transport": 500000, "meals": 300000},
    "standard": {"flight": 12000000, "visa": 500000, "transport": 800000, "meals": 500000},
    "premium": {"flight": 18000000, "visa": 500000, "transport": 1200000, "meals": 800000},
    "vip": {"flight": 30000000, "visa": 500000, "transport": 2000000, "meals": 1500000}
}

# Page configuration
st.set_page_config(
    page_title=f"{BRAND['name']} - {BRAND['description']}",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LABBAIK Brand CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap');
    
    /* ===== CSS Variables ===== */
    :root {{
        --brand-black: {COLORS['black']};
        --brand-gold: {COLORS['gold']};
        --brand-gold-light: {COLORS['gold_light']};
        --brand-green: {COLORS['green']};
        --brand-white: {COLORS['white']};
        --brand-sand: {COLORS['sand']};
        --brand-blue: {COLORS['blue']};
        --brand-gray: {COLORS['gray']};
    }}
    
    /* ===== Sidebar ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['black']} 0%, #2D2D2D 100%);
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] hr {{
        border-color: #333 !important;
    }}
    
    /* ===== Buttons ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%);
        color: {COLORS['black']};
        border: none;
        border-radius: 25px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }}
    
    .stButton > button[kind="secondary"] {{
        background: transparent;
        border: 2px solid {COLORS['gold']};
        color: {COLORS['gold']};
    }}
    
    /* ===== Metrics ===== */
    [data-testid="stMetricValue"] {{
        color: {COLORS['gold']} !important;
        font-weight: 700;
    }}
    
    /* ===== Tabs ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS['gold']};
        color: {COLORS['black']};
    }}
    
    /* ===== Headers ===== */
    .main-header {{
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: bold;
        color: {COLORS['black']};
        text-align: center;
        padding: 1rem;
    }}
    
    .sub-header {{
        font-size: 1.2rem;
        color: {COLORS['gray']};
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* ===== Brand Header ===== */
    .labbaik-hero {{
        background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 50%, {COLORS['black']} 100%);
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
    }}
    
    .labbaik-arabic {{
        font-family: 'Noto Naskh Arabic', serif;
        font-size: 3rem;
        color: {COLORS['gold']};
        text-shadow: 0 2px 15px rgba(212, 175, 55, 0.3);
        margin-bottom: 8px;
    }}
    
    .labbaik-name {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        letter-spacing: 0.3em;
        margin-bottom: 8px;
    }}
    
    .labbaik-tagline {{
        color: {COLORS['sand']};
        font-size: 1rem;
    }}
    
    /* ===== Cards ===== */
    .metric-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 2px solid #E0E0E0;
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        border-color: {COLORS['gold']};
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.15);
        transform: translateY(-3px);
    }}
    
    .metric-card h3 {{
        color: {COLORS['black']};
        margin-bottom: 0.5rem;
    }}
    
    .metric-card p {{
        color: {COLORS['gray']};
        font-size: 0.9rem;
    }}
    
    /* ===== Feature Card ===== */
    .feature-card {{
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 2px solid #E0E0E0;
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .feature-card:hover {{
        border-color: {COLORS['gold']};
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2);
        transform: translateY(-5px);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 12px;
    }}
    
    .feature-title {{
        font-weight: 700;
        color: {COLORS['black']};
        margin-bottom: 8px;
    }}
    
    .feature-desc {{
        color: {COLORS['gray']};
        font-size: 0.9rem;
    }}
    
    /* ===== Highlight Boxes ===== */
    .highlight-box {{
        background-color: rgba(212, 175, 55, 0.1);
        border-left: 4px solid {COLORS['gold']};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }}
    
    .warning-box {{
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }}
    
    .success-box {{
        background-color: rgba(0, 107, 60, 0.1);
        border-left: 4px solid {COLORS['green']};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }}
    
    /* ===== Gold Accent ===== */
    .gold-text {{
        color: {COLORS['gold']};
    }}
    
    .gold-bg {{
        background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%);
        color: {COLORS['black']};
    }}
    
    /* ===== Stats Bar ===== */
    .stats-bar {{
        background: {COLORS['black']};
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }}
    
    .stat-item {{
        text-align: center;
    }}
    
    .stat-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {COLORS['gold']};
    }}
    
    .stat-label {{
        font-size: 0.85rem;
        color: {COLORS['sand']};
    }}
    
    /* ===== Footer ===== */
    .labbaik-footer {{
        background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-top: 40px;
    }}
    
    /* ===== Animations ===== */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    .animate-fadeIn {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    .animate-pulse {{
        animation: pulse 2s infinite;
    }}
</style>
""", unsafe_allow_html=True)


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
        
        # Custom user badge with dark background for sidebar visibility
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
            
            # Logout button for logged-in users
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
            
            # Login button for guests
            if st.button("🔑 Login / Register", type="primary", use_container_width=True, key="sidebar_login_btn"):
                st.session_state.show_login_page = True
                st.rerun()
        
        st.markdown("---")
        
        user = get_current_user()
        
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
    <div style="font-size: 0.85rem; font-weight: 600; color: {COLORS['green']}; margin-bottom: 8px;">📊 Visitor Stats (Real-time)</div>
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


def render_home():
    """Render home page with LABBAIK branding"""
    track_page_view("Home")
    
    hero_html = f"""
<div class="labbaik-hero animate-fadeIn">
    <div class="labbaik-arabic">{BRAND['talbiyah']}</div>
    <div class="labbaik-name">{BRAND['name']}</div>
    <div class="labbaik-tagline">{BRAND['tagline']}</div>
    <p style="color: {COLORS['sand']}; margin-top: 15px; font-size: 1.1rem;">{BRAND['description']}</p>
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
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤖</div><div class="feature-title">AI Assistant 24/7</div><div class="feature-desc">Tanya apapun tentang umrah, AI siap membantu kapan saja</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="feature-card"><div class="feature-icon">💰</div><div class="feature-title">Simulasi Biaya</div><div class="feature-desc">Hitung estimasi biaya dengan berbagai skenario</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Bandingkan Paket</div><div class="feature-desc">Bandingkan opsi Ekonomis, Standard, Premium, VIP</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤝</div><div class="feature-title">Umrah Bareng</div><div class="feature-desc">Cari teman umrah dengan kriteria yang cocok</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🕋</div><div class="feature-title">Umrah Mandiri</div><div class="feature-desc">Panduan lengkap & forum sharing pengalaman</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="feature-card"><div class="feature-icon">✈️</div><div class="feature-title">Booking Terintegrasi</div><div class="feature-desc">Pesan tiket pesawat dan hotel dalam satu platform</div></div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: center; color: {COLORS['black']};'>🌟 Mengapa LABBAIK?</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">🤖</div><div style="font-weight: 700; color: #1A1A1A;">AI-Powered</div><div style="font-size: 0.85rem; color: #666;">Teknologi AI terdepan</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">📊</div><div style="font-weight: 700; color: #1A1A1A;">Data Akurat</div><div style="font-size: 0.85rem; color: #666;">Estimasi biaya real</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">🇮🇩</div><div style="font-weight: 700; color: #1A1A1A;">Lokal Indonesia</div><div style="font-size: 0.85rem; color: #666;">Untuk jamaah Indonesia</div></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown("""<div style="text-align: center; padding: 15px;"><div style="font-size: 2.5rem;">💯</div><div style="font-weight: 700; color: #1A1A1A;">100% Gratis</div><div style="font-size: 0.85rem; color: #666;">Daftar tanpa biaya</div></div>""", unsafe_allow_html=True)
        
    else:
        user = get_current_user()
        role_info = get_user_role_info(user.get("role", "user") if user else "guest")
        
        welcome_html = f"""
<div style="background: linear-gradient(135deg, {role_info['color']}22, {role_info['color']}11); border-left: 4px solid {role_info['color']}; padding: 15px 20px; border-radius: 0 10px 10px 0; margin-bottom: 20px;">
    <span style="font-size: 1.5rem;">{role_info['badge']}</span>
    <span style="font-weight: 600; margin-left: 10px;">Assalamualaikum, {user.get('name', 'User')}!</span>
    <span style="color: {COLORS['gray']}; margin-left: 10px;">({role_info['name']})</span>
</div>
"""
        st.markdown(welcome_html, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='color: {COLORS['black']}; margin: 20px 0;'>✨ Fitur Utama</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤖</div><div class="feature-title">AI Assistant</div><div class="feature-desc">Tanya apapun tentang umrah</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="feature-card"><div class="feature-icon">💰</div><div class="feature-title">Simulasi Biaya</div><div class="feature-desc">Hitung estimasi biaya</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="feature-card"><div class="feature-icon">💵</div><div class="feature-title">Cari by Budget</div><div class="feature-desc">Paket sesuai dana</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🤝</div><div class="feature-title">Umrah Bareng</div><div class="feature-desc">Cari teman perjalanan</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="feature-card"><div class="feature-icon">🕋</div><div class="feature-title">Umrah Mandiri</div><div class="feature-desc">Panduan & Forum</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Bandingkan</div><div class="feature-desc">Ekonomis - VIP</div></div>""", unsafe_allow_html=True)
        
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


def render_cost_simulation():
    """Render cost simulation page"""
    st.header("💰 Simulasi Biaya Umrah")
    
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            scenario = st.selectbox("Skenario Paket", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES[x]["name"])
            num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=2)
            duration = st.slider("Durasi (hari)", min_value=7, max_value=21, value=SCENARIO_TEMPLATES[scenario]["duration_days"])
        
        with col2:
            departure_city = st.selectbox("Kota Keberangkatan", DEPARTURE_CITIES)
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
        
        season_info = None
        for season in SEASONS.values():
            if departure_month in season["months"]:
                season_info = season
                break
        
        if season_info and season_info["multiplier"] > 1:
            st.markdown(f"""<div class="warning-box">⚠️ <strong>Perhatian:</strong> Bulan {departure_month} termasuk musim {season_info['name']} dengan kenaikan harga sekitar {int((season_info['multiplier']-1)*100)}%</div>""", unsafe_allow_html=True)
        
        st.markdown("### 📈 Visualisasi Biaya")
        
        components = [
            {"Komponen": "Tiket Pesawat", "Estimasi": result.estimated_max * 0.25},
            {"Komponen": "Hotel Makkah", "Estimasi": result.estimated_max * 0.30},
            {"Komponen": "Hotel Madinah", "Estimasi": result.estimated_max * 0.15},
            {"Komponen": "Makan", "Estimasi": result.estimated_max * 0.10},
            {"Komponen": "Transportasi", "Estimasi": result.estimated_max * 0.08},
            {"Komponen": "Visa & Handling", "Estimasi": result.estimated_max * 0.07},
            {"Komponen": "Lainnya", "Estimasi": result.estimated_max * 0.05},
        ]
        df = pd.DataFrame(components)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(df, values="Estimasi", names="Komponen", title="Distribusi Biaya", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(df, x="Komponen", y="Estimasi", title="Breakdown per Komponen", color="Komponen", color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### ✨ Fasilitas Termasuk")
        cols = st.columns(2)
        for i, feature in enumerate(result.features):
            cols[i % 2].markdown(f"✅ {feature}")
        
        if result.notes:
            st.markdown("### 📝 Catatan")
            for note in result.notes:
                st.markdown(note)


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
                "Jarak ke Haram": scenario.hotel_distance_makkah,
                "Makan": scenario.meal_type.replace("_", " ").title(),
                "Min (Rp)": scenario.estimated_min,
                "Max (Rp)": scenario.estimated_max,
            })
        
        df = pd.DataFrame(scenarios_data)
        
        st.markdown("### 📋 Tabel Perbandingan")
        st.dataframe(df.style.format({"Min (Rp)": "{:,.0f}", "Max (Rp)": "{:,.0f}"}), use_container_width=True)
        
        st.markdown("### 💰 Perbandingan Harga")
        fig = go.Figure()
        for scenario in scenarios_data:
            fig.add_trace(go.Bar(name=scenario["Skenario"], x=[scenario["Skenario"]], y=[(scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2], error_y=dict(type='data', symmetric=False, array=[scenario["Max (Rp)"] - (scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2], arrayminus=[(scenario["Min (Rp)"] + scenario["Max (Rp)"]) / 2 - scenario["Min (Rp)"]])))
        fig.update_layout(title="Range Harga per Skenario", yaxis_title="Estimasi Biaya (Rp)", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""<div class="highlight-box"><h4>💡 Rekomendasi</h4><ul><li><strong>Budget < Rp 35 juta:</strong> Pilih Ekonomis</li><li><strong>Keseimbangan:</strong> Pilih Standard</li><li><strong>Prioritas Kenyamanan:</strong> Pilih Premium</li><li><strong>Pengalaman Terbaik:</strong> Pilih VIP</li></ul></div>""", unsafe_allow_html=True)


def render_time_analysis():
    """Render time analysis page"""
    st.header("📅 Analisis Waktu Terbaik Umrah")
    
    priority = st.selectbox("Prioritas Anda", ["balanced", "cost", "crowd"], format_func=lambda x: {"balanced": "🎯 Seimbang (Harga & Keramaian)", "cost": "💰 Prioritas Hemat Biaya", "crowd": "👥 Prioritas Hindari Keramaian"}[x])
    
    if st.button("📊 Analisis Waktu Terbaik", use_container_width=True):
        planner = st.session_state.scenario_planner
        analysis = planner.analyze_best_time(priority)
        
        st.markdown("### ✅ Bulan Terbaik untuk Umrah")
        cols = st.columns(3)
        for i, month_data in enumerate(analysis["best_months"]):
            with cols[i]:
                st.markdown(f"""<div class="success-box"><h4>#{i+1} {month_data['month_name']}</h4><p>🌡️ Cuaca: {month_data['weather']}</p><p>💰 Multiplier: {month_data['price_multiplier']}x</p><p>👥 Keramaian: {month_data['crowd_level']}</p></div>""", unsafe_allow_html=True)
        
        st.markdown("### ⚠️ Bulan yang Perlu Dipertimbangkan")
        cols = st.columns(3)
        for i, month_data in enumerate(analysis["avoid_months"]):
            with cols[i]:
                st.markdown(f"""<div class="warning-box"><h4>{month_data['month_name']}</h4><p>🌡️ Cuaca: {month_data['weather']}</p><p>💰 Multiplier: {month_data['price_multiplier']}x</p><p>👥 Keramaian: {month_data['crowd_level']}</p></div>""", unsafe_allow_html=True)
        
        st.markdown("### 📈 Analisis Sepanjang Tahun")
        df = pd.DataFrame(analysis["analysis"])
        fig = px.line(df, x="month_name", y="recommendation_score", title="Skor Rekomendasi per Bulan", markers=True)
        fig.update_layout(xaxis_title="Bulan", yaxis_title="Skor Rekomendasi")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 💡 Tips")
        for note in analysis["notes"]:
            st.markdown(f"• {note}")


def render_ai_chat():
    """Render AI chat page"""
    st.header("🤖 Chat dengan AI Assistant")
    
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Sistem AI belum diinisialisasi.")
        if st.button("🔄 Inisialisasi Sistem"):
            initialize_system()
            st.rerun()
        return
    
    st.markdown("Tanyakan apa saja tentang umrah kepada AI Assistant!")
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    if prompt := st.chat_input("Ketik pertanyaan Anda..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("🤔 AI sedang berpikir..."):
            try:
                response = st.session_state.orchestrator.chat(prompt)
                ai_response = response["response"]
            except Exception as e:
                ai_response = f"Maaf, terjadi error: {str(e)}"
        
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").write(ai_response)
    
    st.markdown("---")
    st.markdown("### 💡 Pertanyaan Cepat")
    
    quick_questions = ["Apa saja rukun umrah?", "Bagaimana tips hemat biaya umrah?", "Kapan waktu terbaik untuk umrah?", "Apa yang harus dipersiapkan sebelum umrah?", "Bagaimana memilih travel umrah yang terpercaya?"]
    
    cols = st.columns(2)
    for i, q in enumerate(quick_questions):
        if cols[i % 2].button(q, key=f"quick_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.rerun()
    
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.chat_history = []
        if st.session_state.orchestrator:
            st.session_state.orchestrator.reset_conversations()
        st.rerun()


def render_create_plan():
    """Render create plan page with Makkah/Madinah duration selection - v3.1.0"""
    st.header("📋 Buat Rencana Umrah Lengkap")
    
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Sistem AI belum diinisialisasi.")
        if st.button("🔄 Inisialisasi Sistem"):
            initialize_system()
            st.rerun()
        return
    
    st.markdown("### 📝 Detail Perjalanan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario = st.selectbox("Skenario Paket", ["ekonomis", "standard", "premium", "vip"], format_func=lambda x: SCENARIO_TEMPLATES[x]["name"], key="plan_scenario")
        num_people = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=2, key="plan_num_people")
        departure_month = st.selectbox("Bulan Keberangkatan", range(1, 13), format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1], key="plan_departure_month")
    
    with col2:
        st.markdown("#### 🕋 Durasi Menginap")
        nights_makkah = st.slider("🕋 Lama di Mekkah (malam)", min_value=2, max_value=10, value=4, key="nights_makkah", help="Pilih jumlah malam menginap di Mekkah")
        nights_madinah = st.slider("🕌 Lama di Madinah (malam)", min_value=2, max_value=10, value=3, key="nights_madinah", help="Pilih jumlah malam menginap di Madinah")
        total_duration = nights_makkah + nights_madinah + 2
        st.info(f"📅 **Total Durasi:** {total_duration} hari ({nights_makkah} malam Mekkah + {nights_madinah} malam Madinah + 2 hari transit)")
    
    st.markdown("---")
    st.markdown("### 💰 Preview Biaya Akomodasi")
    
    hotel_makkah = HOTEL_PRICES[scenario]["makkah"]
    hotel_madinah = HOTEL_PRICES[scenario]["madinah"]
    additional = ADDITIONAL_COSTS[scenario]
    
    cost_makkah = hotel_makkah["price"] * nights_makkah
    cost_madinah = hotel_madinah["price"] * nights_madinah
    cost_accommodation = cost_makkah + cost_madinah
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #3D2817 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #FF8F00;"><div style="font-weight: 700; color: #FF8F00; margin-bottom: 8px;">🕋 Hotel Mekkah</div><div style="font-size: 0.85rem; color: #C9A86C; margin-bottom: 5px;">{hotel_makkah['name']}</div><div style="font-size: 0.8rem; color: #999;">Rp {hotel_makkah['price']:,}/malam × {nights_makkah} malam</div><div style="font-size: 1.2rem; font-weight: 700; color: #FF8F00; margin-top: 8px;">Rp {cost_makkah:,}</div></div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #1E3D2F 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #4CAF50;"><div style="font-weight: 700; color: #4CAF50; margin-bottom: 8px;">🕌 Hotel Madinah</div><div style="font-size: 0.85rem; color: #C9A86C; margin-bottom: 5px;">{hotel_madinah['name']}</div><div style="font-size: 0.8rem; color: #999;">Rp {hotel_madinah['price']:,}/malam × {nights_madinah} malam</div><div style="font-size: 1.2rem; font-weight: 700; color: #4CAF50; margin-top: 8px;">Rp {cost_madinah:,}</div></div>""", unsafe_allow_html=True)
    
    with col3:
        total_accommodation = cost_accommodation * num_people
        st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 15px; border-radius: 10px;"><div style="font-weight: 700; color: #D4AF37; margin-bottom: 8px;">💰 Total Akomodasi</div><div style="font-size: 0.85rem; color: #C9A86C; margin-bottom: 5px;">Per orang: Rp {cost_accommodation:,}</div><div style="font-size: 0.8rem; color: #888;">× {num_people} jamaah</div><div style="font-size: 1.2rem; font-weight: 700; color: #D4AF37; margin-top: 8px;">Rp {total_accommodation:,}</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    special_requests = st.text_area("Permintaan Khusus", placeholder="Misal: jamaah lansia, butuh kursi roda, vegetarian, dll.", key="plan_special_requests")
    
    if st.button("🚀 Buat Rencana Lengkap", use_container_width=True, type="primary"):
        with st.spinner("⏳ AI sedang menyusun rencana lengkap..."):
            try:
                duration_info = f"\n\nDurasi menginap:\n- Mekkah: {nights_makkah} malam\n- Madinah: {nights_madinah} malam\n- Total: {total_duration} hari"
                enhanced_requests = (special_requests or "") + duration_info
                
                result = st.session_state.orchestrator.create_complete_plan(scenario=scenario, num_people=num_people, duration_days=total_duration, departure_month=departure_month, special_requests=enhanced_requests if enhanced_requests.strip() else None)
                
                st.markdown("---")
                st.success("✅ Rencana berhasil dibuat!")
                
                st.markdown("### 📊 Ringkasan Perjalanan")
                sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
                with sum_col1:
                    st.metric("👥 Jamaah", f"{num_people} orang")
                with sum_col2:
                    st.metric("🕋 Mekkah", f"{nights_makkah} malam")
                with sum_col3:
                    st.metric("🕌 Madinah", f"{nights_madinah} malam")
                with sum_col4:
                    st.metric("📅 Total", f"{total_duration} hari")
                
                st.markdown("### 💰 Rincian Biaya Per Orang")
                
                flight_cost = additional["flight"]
                visa_cost = additional["visa"]
                transport_cost = additional["transport"]
                meals_cost = additional["meals"] * total_duration
                
                total_per_person = cost_accommodation + flight_cost + visa_cost + transport_cost + meals_cost
                grand_total = total_per_person * num_people
                
                cost_items = [("✈️ Tiket Pesawat PP", flight_cost), ("🕋 Hotel Mekkah", cost_makkah), ("🕌 Hotel Madinah", cost_madinah), ("📄 Visa & Handling", visa_cost), ("🚐 Transportasi Lokal", transport_cost), (f"🍽️ Makan ({total_duration} hari)", meals_cost)]
                
                for item_name, item_cost in cost_items:
                    st.markdown(f"""<div style="display: flex; justify-content: space-between; padding: 8px 12px; background: #f9f9f9; border-radius: 5px; margin: 4px 0;"><span>{item_name}</span><span style="font-weight: 600;">Rp {item_cost:,}</span></div>""", unsafe_allow_html=True)
                
                st.markdown("---")
                total_col1, total_col2 = st.columns(2)
                with total_col1:
                    st.markdown(f"""<div style="background: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center;"><div style="font-size: 0.9rem; color: #1565c0;">Per Orang</div><div style="font-size: 1.8rem; font-weight: 700; color: #1565c0;">Rp {total_per_person:,}</div></div>""", unsafe_allow_html=True)
                with total_col2:
                    st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 20px; border-radius: 10px; text-align: center;"><div style="font-size: 0.9rem; color: #D4AF37;">GRAND TOTAL ({num_people} orang)</div><div style="font-size: 1.8rem; font-weight: 700; color: #D4AF37;">Rp {grand_total:,}</div></div>""", unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 💡 Analisis AI - Keuangan")
                if "calculation" in result["results"]["financial"]:
                    calc = result["results"]["financial"]["calculation"]
                    ai_col1, ai_col2 = st.columns(2)
                    with ai_col1:
                        st.metric("Estimasi AI Min", format_currency(calc["total_min"]))
                    with ai_col2:
                        st.metric("Estimasi AI Max", format_currency(calc["total_max"]))
                st.markdown(result["results"]["financial"]["response"])
                
                st.markdown("### 📅 Itinerary")
                st.markdown(result["results"]["itinerary"]["response"])
                
                st.markdown("### 📋 Persyaratan")
                st.markdown(result["results"]["requirements"]["response"])
                
                st.markdown("### 💡 Tips")
                st.markdown(result["results"]["tips"]["response"])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")


def render_budget_finder():
    """Render budget finder page - Find packages based on available budget v3.1.0"""
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
    
    # Package thresholds (minimum budget per person for each scenario)
    PACKAGE_THRESHOLDS = {
        "ekonomis": {
            "min_budget": 20_000_000,
            "max_budget": 35_000_000,
            "base_duration": 9,  # minimum days
            "max_duration": 12,
        },
        "standard": {
            "min_budget": 35_000_000,
            "max_budget": 50_000_000,
            "base_duration": 9,
            "max_duration": 14,
        },
        "premium": {
            "min_budget": 50_000_000,
            "max_budget": 80_000_000,
            "base_duration": 10,
            "max_duration": 14,
        },
        "vip": {
            "min_budget": 80_000_000,
            "max_budget": 200_000_000,
            "base_duration": 12,
            "max_duration": 21,
        }
    }
    
    available_packages = []
    partial_packages = []
    
    # Hotel star mapping for each scenario
    HOTEL_STARS = {
        "ekonomis": "2-3",
        "standard": "3-4", 
        "premium": "4-5",
        "vip": "5"
    }
    
    for scenario_key, threshold in PACKAGE_THRESHOLDS.items():
        template = SCENARIO_TEMPLATES[scenario_key]
        hotel_makkah = HOTEL_PRICES[scenario_key]["makkah"]
        hotel_madinah = HOTEL_PRICES[scenario_key]["madinah"]
        additional = ADDITIONAL_COSTS[scenario_key]
        hotel_star = HOTEL_STARS.get(scenario_key, "3")
        
        # Calculate minimum cost for this package (base duration)
        base_nights_makkah = 4
        base_nights_madinah = 3
        base_total_days = base_nights_makkah + base_nights_madinah + 2
        
        min_accommodation = (hotel_makkah["price"] * base_nights_makkah) + (hotel_madinah["price"] * base_nights_madinah)
        min_total = min_accommodation + additional["flight"] + additional["visa"] + additional["transport"] + (additional["meals"] * base_total_days)
        
        # Calculate maximum possible duration with this budget
        if budget_per_person >= min_total:
            # Calculate how many extra nights can be afforded
            remaining_budget = budget_per_person - min_total
            extra_night_cost = hotel_makkah["price"] + additional["meals"]  # Cost per extra night
            extra_nights = int(remaining_budget / extra_night_cost)
            max_possible_nights = min(base_nights_makkah + base_nights_madinah + extra_nights, threshold["max_duration"] - 2)
            
            # Distribute extra nights
            extra_makkah = min(extra_nights // 2, 6)  # Max 10 nights in Makkah
            extra_madinah = min(extra_nights - extra_makkah, 7)  # Max 10 nights in Madinah
            
            final_makkah = base_nights_makkah + extra_makkah
            final_madinah = base_nights_madinah + extra_madinah
            final_duration = final_makkah + final_madinah + 2
            
            # Recalculate actual cost
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
                "meals": "Prasmanan" if scenario_key in ["ekonomis"] else "Buffet Hotel" if scenario_key == "standard" else "Full Board Premium",
            })
        elif budget_per_person >= threshold["min_budget"] * 0.7:
            # Partial - almost enough
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
            # Determine card color based on scenario
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
            
            # Package details in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                **🕋 Mekkah**  
                {pkg['nights_makkah']} malam  
                _{pkg['hotel_makkah'][:30]}..._
                """)
            
            with col2:
                st.markdown(f"""
                **🕌 Madinah**  
                {pkg['nights_madinah']} malam  
                _{pkg['hotel_madinah'][:30]}..._
                """)
            
            with col3:
                st.markdown(f"""
                **📅 Durasi**  
                {pkg['duration']} hari  
                _Termasuk transit_
                """)
            
            with col4:
                if pkg['remaining'] > 0:
                    st.markdown(f"""
                    **💰 Sisa Budget**  
                    Rp {pkg['remaining']:,.0f}  
                    _Untuk oleh-oleh_
                    """)
                else:
                    st.markdown(f"""
                    **💰 Status**  
                    Pas Budget  
                    _Sesuai dana_
                    """)
            
            # Expandable details
            with st.expander(f"📋 Lihat Detail Paket {pkg['name']}"):
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("**✈️ Penerbangan**")
                    st.markdown(f"- Kelas: {pkg['flight_class']}")
                    st.markdown(f"- Rute: PP Indonesia - Jeddah/Madinah")
                    
                    st.markdown("**🏨 Akomodasi**")
                    st.markdown(f"- Hotel Bintang: ⭐ {pkg['hotel_star']}")
                    st.markdown(f"- Mekkah: {pkg['hotel_makkah']}")
                    st.markdown(f"- Madinah: {pkg['hotel_madinah']}")
                
                with detail_col2:
                    st.markdown("**🍽️ Konsumsi**")
                    st.markdown(f"- Tipe: {pkg['meals']}")
                    st.markdown(f"- {pkg['duration']} hari full board")
                    
                    st.markdown("**📦 Termasuk**")
                    st.markdown("- ✅ Visa Umrah")
                    st.markdown("- ✅ Transportasi lokal")
                    st.markdown("- ✅ Muthawwif/Guide")
                    st.markdown("- ✅ Air Zamzam 5L")
                
                # Cost breakdown
                st.markdown("---")
                st.markdown("**💰 Rincian Biaya Per Orang:**")
                
                additional = ADDITIONAL_COSTS[pkg["scenario"]]
                hotel_m = HOTEL_PRICES[pkg["scenario"]]["makkah"]["price"] * pkg["nights_makkah"]
                hotel_d = HOTEL_PRICES[pkg["scenario"]]["madinah"]["price"] * pkg["nights_madinah"]
                
                breakdown_data = [
                    ("✈️ Tiket Pesawat PP", additional["flight"]),
                    ("🕋 Hotel Mekkah", hotel_m),
                    ("🕌 Hotel Madinah", hotel_d),
                    ("📄 Visa & Handling", additional["visa"]),
                    ("🚐 Transportasi", additional["transport"]),
                    (f"🍽️ Makan ({pkg['duration']} hari)", additional["meals"] * pkg["duration"]),
                ]
                
                for item, cost in breakdown_data:
                    st.markdown(f"- {item}: **Rp {cost:,.0f}**")
                
                st.markdown(f"**TOTAL: Rp {pkg['total_cost']:,.0f}**")
            
            st.markdown("---")
        
        # Summary for multiple people
        if num_people > 1:
            best_pkg = available_packages[0]  # Recommend the first available (usually ekonomis)
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
        
        # Show what's needed
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
            st.markdown("""
**💰 Tambah Tabungan**
- Target tambahan: Rp {:,.0f}
- Jika menabung Rp 1 juta/bulan: {} bulan lagi
- Jika menabung Rp 2 juta/bulan: {} bulan lagi
""".format(
            shortage,
            int(shortage / 1_000_000) + 1,
            int(shortage / 2_000_000) + 1
            ))

        with col2:
            st.markdown("""
            **🤝 Opsi Lain**
            - Cari promo early bird
            - Berangkat di low season (Januari-Februari)
            - Gabung dengan grup besar untuk diskon
            - Cicilan dari travel agent
            """)

# Show partial packages (almost affordable)
        if partial_packages:
            st.markdown("### 📦 Paket yang Hampir Terjangkau")
            for pkg in partial_packages:
                st.info(f"**{pkg['name']}** - Kurang Rp {pkg['shortage']:,.0f} (Minimum: Rp {pkg['min_required']:,.0f})")

# Tips section
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
# UMRAH BARENG - OPEN TRIP FEATURE
# ============================================

def init_umrah_bareng_state():
    """Initialize Umrah Bareng session state - load from database if available"""
    if "open_trips" not in st.session_state:
        # Try to load from database first
        if DB_AVAILABLE and is_db_available():
            try:
                db_trips = db_get_open_trips()
                if db_trips:
                    st.session_state.open_trips = db_trips
                    st.session_state.trips_from_db = True
                    return
            except:
                pass

        # Fallback to sample data for demonstration
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
                "special_notes": "Fokus ibadah, tidak banyak shopping. Ada anak kecil.",
                "amenities": ["Muthawwif Indonesia", "Kursi Roda Tersedia", "Menu Indonesia"],
                "status": "open",
                "created_at": "2025-01-15",
                "whatsapp_group": "https://chat.whatsapp.com/xxx",
            },
            {
                "id": "OT002",
                "creator_name": "Hj. Siti Aminah",
                "creator_phone": "+62813xxxx5678",
                "creator_city": "Surabaya",
                "title": "Umrah Khusus Ibu-Ibu",
                "departure_date": "2025-04-10",
                "departure_city": "Surabaya (SUB)",
                "package_type": "premium",
                "budget_per_person": 55000000,
                "duration_days": 14,
                "nights_makkah": 6,
                "nights_madinah": 5,
                "current_members": 8,
                "max_members": 15,
                "gender_preference": "Wanita Only",
                "age_preference": "40+ tahun",
                "special_notes": "Tempo santai, banyak ziarah. Cocok untuk lansia.",
                "amenities": ["Ustadzah Pendamping", "Hotel Dekat Haram", "Wheelchair Friendly"],
                "status": "open",
                "created_at": "2025-01-10",
                "whatsapp_group": "https://chat.whatsapp.com/yyy",
            },
            {
                "id": "OT003",
                "creator_name": "Rizky Pratama",
                "creator_phone": "+62857xxxx9012",
                "creator_city": "Bandung",
                "title": "Umrah Backpacker Style",
                "departure_date": "2025-02-20",
                "departure_city": "Jakarta (CGK)",
                "package_type": "ekonomis",
                "budget_per_person": 25000000,
                "duration_days": 9,
                "nights_makkah": 4,
                "nights_madinah": 3,
                "current_members": 3,
                "max_members": 8,
                "gender_preference": "Pria Only",
                "age_preference": "20-35 tahun",
                "special_notes": "Budget terbatas tapi semangat tinggi! Siap jalan kaki.",
                "amenities": ["Guide Lokal", "Sharing Room"],
                "status": "open",
                "created_at": "2025-01-20",
                "whatsapp_group": "https://chat.whatsapp.com/zzz",
            },
        ]
        st.session_state.trips_from_db = False


def render_umrah_bareng():
    """Render Umrah Bareng (Open Trip) feature"""
    init_umrah_bareng_state()

    st.header("🤝 Umrah Bareng - Open Trip")
    st.markdown("Cari teman perjalanan umrah atau buat open trip sendiri!")

    # Stats bar
    total_trips = len(st.session_state.open_trips)
    open_trips = len([t for t in st.session_state.open_trips if t["status"] == "open"])
    total_slots = sum([t["max_members"] - t["current_members"] for t in st.session_state.open_trips if t["status"] == "open"])

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
    <table style="width: 100%; color: white;">
    <tr>
    <td style="text-align: center; padding: 10px;">
    <div style="font-size: 2rem; font-weight: 700; color: #D4AF37;">{total_trips}</div>
    <div style="font-size: 0.85rem; color: #C9A86C;">Total Open Trip</div>
    </td>
    <td style="text-align: center; padding: 10px;">
    <div style="font-size: 2rem; font-weight: 700; color: #4CAF50;">{open_trips}</div>
    <div style="font-size: 0.85rem; color: #C9A86C;">Masih Tersedia</div>
    </td>
    <td style="text-align: center; padding: 10px;">
    <div style="font-size: 2rem; font-weight: 700; color: #2196F3;">{total_slots}</div>
    <div style="font-size: 0.85rem; color: #C9A86C;">Slot Kosong</div>
    </td>
    </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Cari Open Trip", "➕ Buat Open Trip", "📋 Trip Saya"])
    
    # ===== TAB 1: CARI OPEN TRIP =====
    with tab1:
        st.markdown("### 🔍 Cari Open Trip yang Cocok")
        
        # Filters
        with st.expander("🎯 Filter Pencarian", expanded=True):
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
            
            with filter_col1:
                filter_budget = st.select_slider(
                    "💰 Budget Maksimal",
                    options=[20, 30, 40, 50, 60, 80, 100],
                    value=50,
                    format_func=lambda x: f"Rp {x} juta"
                )
            
            with filter_col2:
                filter_package = st.selectbox(
                    "📦 Tipe Paket",
                    options=["Semua", "ekonomis", "standard", "premium", "vip"],
                    format_func=lambda x: "Semua Paket" if x == "Semua" else SCENARIO_TEMPLATES.get(x, {}).get("name", x.title())
                )
            
            with filter_col3:
                filter_gender = st.selectbox(
                    "👥 Preferensi Gender",
                    options=["Semua", "Campuran (Keluarga)", "Pria Only", "Wanita Only"]
                )
            
            with filter_col4:
                filter_city = st.selectbox(
                    "🏙️ Kota Keberangkatan",
                    options=["Semua"] + list(DEPARTURE_CITIES.keys())
                )
        
        # Filter results
        filtered_trips = st.session_state.open_trips.copy()
        
        if filter_budget:
            filtered_trips = [t for t in filtered_trips if t["budget_per_person"] <= filter_budget * 1_000_000]
        
        if filter_package != "Semua":
            filtered_trips = [t for t in filtered_trips if t["package_type"] == filter_package]
        
        if filter_gender != "Semua":
            filtered_trips = [t for t in filtered_trips if t["gender_preference"] == filter_gender]
        
        if filter_city != "Semua":
            filtered_trips = [t for t in filtered_trips if filter_city in t["departure_city"]]
        
        # Only show open trips
        filtered_trips = [t for t in filtered_trips if t["status"] == "open"]
        
        st.markdown(f"**Ditemukan {len(filtered_trips)} open trip**")
        st.markdown("---")
        
        # Display trips
        if filtered_trips:
            for trip in filtered_trips:
                slots_left = trip["max_members"] - trip["current_members"]
                progress = trip["current_members"] / trip["max_members"]
                
                # Package colors
                pkg_colors = {
                    "ekonomis": ("#4CAF50", "🟢"),
                    "standard": ("#2196F3", "🔵"),
                    "premium": ("#FF9800", "🟠"),
                    "vip": ("#D4AF37", "🟡"),
                }
                pkg_color, pkg_emoji = pkg_colors.get(trip["package_type"], ("#666", "⚪"))
                
                st.markdown(f"""
                <div style="background: white; border: 2px solid {pkg_color}; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                        <div>
                            <span style="background: {pkg_color}; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;">
                                {pkg_emoji} {SCENARIO_TEMPLATES.get(trip['package_type'], {}).get('name', trip['package_type'].title())}
                            </span>
                            <h3 style="margin: 10px 0 5px 0; color: #1A1A1A;">{trip['title']}</h3>
                            <p style="color: #666; margin: 0; font-size: 0.9rem;">oleh {trip['creator_name']} • {trip['creator_city']}</p>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.8rem; color: #888;">Budget/Orang</div>
                            <div style="font-size: 1.4rem; font-weight: 700; color: {pkg_color};">Rp {trip['budget_per_person']:,}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Trip details
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"📅 **Berangkat**\n\n{trip['departure_date']}")
                
                with col2:
                    st.markdown(f"✈️ **Dari**\n\n{trip['departure_city']}")
                
                with col3:
                    st.markdown(f"⏱️ **Durasi**\n\n{trip['duration_days']} hari")
                
                with col4:
                    st.markdown(f"👥 **Slot**\n\n{trip['current_members']}/{trip['max_members']} ({slots_left} sisa)")
                
                # Progress bar
                st.progress(progress)
                
                # Expandable details
                with st.expander("📋 Lihat Detail & Gabung"):
                    detail_col1, detail_col2 = st.columns(2)
                    
                    with detail_col1:
                        st.markdown("**🕋 Itinerary:**")
                        st.markdown(f"- Mekkah: {trip['nights_makkah']} malam")
                        st.markdown(f"- Madinah: {trip['nights_madinah']} malam")
                        
                        st.markdown("**👥 Preferensi:**")
                        st.markdown(f"- Gender: {trip['gender_preference']}")
                        st.markdown(f"- Usia: {trip['age_preference']}")
                    
                    with detail_col2:
                        st.markdown("**✨ Fasilitas Khusus:**")
                        for amenity in trip["amenities"]:
                            st.markdown(f"- ✅ {amenity}")
                        
                        st.markdown("**📝 Catatan:**")
                        st.markdown(f"_{trip['special_notes']}_")
                    
                    st.markdown("---")
                    
                    # Contact buttons
                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    
                    with btn_col1:
                        st.markdown(f"[💬 Hubungi via WhatsApp](https://wa.me/{trip['creator_phone'].replace('+', '')}?text=Halo%20kak,%20saya%20tertarik%20dengan%20open%20trip%20{trip['title']})")
                    
                    with btn_col2:
                        if trip.get("whatsapp_group"):
                            st.markdown(f"[👥 Join Grup WA]({trip['whatsapp_group']})")
                    
                    with btn_col3:
                        if st.button(f"❤️ Simpan Trip", key=f"save_{trip['id']}"):
                            st.success("Trip disimpan!")
                
                st.markdown("---")
        else:
            st.info("🔍 Tidak ada open trip yang sesuai filter. Coba ubah kriteria pencarian atau buat open trip sendiri!")
    
    # ===== TAB 2: BUAT OPEN TRIP =====
    with tab2:
        st.markdown("### ➕ Buat Open Trip Baru")
        st.markdown("Ajak jamaah lain untuk umrah bareng dengan kriteria yang Anda tentukan!")
        
        with st.form("create_open_trip"):
            st.markdown("#### 📝 Informasi Dasar")
            
            col1, col2 = st.columns(2)
            
            with col1:
                trip_title = st.text_input(
                    "Judul Open Trip *",
                    placeholder="Contoh: Umrah Bareng Keluarga Muda"
                )
                
                creator_name = st.text_input(
                    "Nama Anda *",
                    placeholder="Nama yang akan ditampilkan"
                )
                
                creator_phone = st.text_input(
                    "No. WhatsApp *",
                    placeholder="+62812xxxxxxxx"
                )
            
            with col2:
                creator_city = st.selectbox(
                    "Kota Anda *",
                    options=["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar", "Semarang", "Yogyakarta", "Lainnya"]
                )
                
                departure_city = st.selectbox(
                    "Kota Keberangkatan *",
                    options=DEPARTURE_CITIES
                )
                
                departure_date = st.date_input(
                    "Tanggal Keberangkatan *",
                    min_value=datetime.now()
                )
            
            st.markdown("---")
            st.markdown("#### 📦 Detail Paket")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                package_type = st.selectbox(
                    "Tipe Paket *",
                    options=["ekonomis", "standard", "premium", "vip"],
                    format_func=lambda x: SCENARIO_TEMPLATES[x]["name"]
                )
                
                budget_per_person = st.number_input(
                    "Budget per Orang (Rp) *",
                    min_value=20_000_000,
                    max_value=200_000_000,
                    value=35_000_000,
                    step=1_000_000
                )
            
            with col2:
                duration_days = st.number_input(
                    "Durasi (hari) *",
                    min_value=7,
                    max_value=21,
                    value=12
                )
                
                nights_makkah = st.number_input(
                    "Malam di Mekkah *",
                    min_value=2,
                    max_value=10,
                    value=5
                )
            
            with col3:
                nights_madinah = st.number_input(
                    "Malam di Madinah *",
                    min_value=2,
                    max_value=10,
                    value=4
                )
                
                max_members = st.number_input(
                    "Maksimal Peserta *",
                    min_value=2,
                    max_value=50,
                    value=10
                )
            
            st.markdown("---")
            st.markdown("#### 👥 Preferensi Peserta")
            
            col1, col2 = st.columns(2)
            
            with col1:
                gender_preference = st.selectbox(
                    "Preferensi Gender",
                    options=["Campuran (Keluarga)", "Pria Only", "Wanita Only"]
                )
                
                age_preference = st.selectbox(
                    "Rentang Usia",
                    options=["Semua Usia", "20-35 tahun", "25-40 tahun", "35-50 tahun", "40+ tahun", "50+ tahun"]
                )
            
            with col2:
                amenities = st.multiselect(
                    "Fasilitas Khusus",
                    options=[
                        "Muthawwif Indonesia",
                        "Ustadz/Ustadzah Pendamping",
                        "Hotel Dekat Haram",
                        "Kursi Roda Tersedia",
                        "Wheelchair Friendly",
                        "Menu Indonesia",
                        "Sharing Room",
                        "Private Room",
                        "City Tour",
                        "Oleh-oleh Tour"
                    ]
                )
            
            special_notes = st.text_area(
                "Catatan Khusus",
                placeholder="Jelaskan lebih detail tentang trip Anda...",
                max_chars=500
            )
            
            whatsapp_group = st.text_input(
                "Link Grup WhatsApp (opsional)",
                placeholder="https://chat.whatsapp.com/..."
            )
            
            st.markdown("---")
            
            submitted = st.form_submit_button("🚀 Buat Open Trip", use_container_width=True)
            
            if submitted:
                if trip_title and creator_name and creator_phone:
                    # Prepare trip data
                    trip_data = {
                        "title": trip_title,
                        "departure_date": str(departure_date),
                        "departure_city": departure_city,
                        "package_type": package_type,
                        "budget_per_person": budget_per_person,
                        "duration_days": duration_days,
                        "nights_makkah": nights_makkah,
                        "nights_madinah": nights_madinah,
                        "max_members": max_members,
                        "gender_preference": gender_preference,
                        "age_preference": age_preference,
                        "special_notes": special_notes,
                        "amenities": amenities,
                        "whatsapp_group": whatsapp_group,
                    }
                    
                    user = get_current_user()
                    user_id = user.get("id") if user else None
                    trip_code = None
                    
                    # Try database first
                    if DB_AVAILABLE and is_db_available() and user_id:
                        try:
                            result = db_create_trip(user_id, trip_data)
                            if result.get("success"):
                                trip_code = result.get("trip_code")
                                st.success(f"✅ Open Trip berhasil dibuat! Kode: {trip_code}")
                                st.balloons()
                                # Refresh trips from database
                                st.session_state.open_trips = db_get_open_trips()
                            else:
                                st.error(f"❌ Gagal menyimpan ke database: {result.get('error')}")
                        except Exception as e:
                            st.warning(f"Database error, menyimpan secara lokal: {e}")
                    
                    # Fallback to session state if database fails or not available
                    if not trip_code:
                        new_trip = {
                            "id": f"OT{len(st.session_state.open_trips) + 1:03d}",
                            "creator_name": creator_name,
                            "creator_phone": creator_phone,
                            "creator_city": creator_city,
                            "current_members": 1,
                            "status": "open",
                            "created_at": str(datetime.now().date()),
                            **trip_data
                        }
                        st.session_state.open_trips.append(new_trip)
                        trip_code = new_trip['id']
                        st.success("✅ Open Trip berhasil dibuat!")
                        st.balloons()
                    
                    st.markdown(f"""
                    <div style="background: #e8f5e9; border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; margin-top: 20px;">
                        <h4 style="color: #2e7d32; margin-top: 0;">🎉 Open Trip Anda Sudah Live!</h4>
                        <p><strong>ID:</strong> {trip_code}</p>
                        <p><strong>Judul:</strong> {trip_title}</p>
                        <p>Jamaah lain sekarang bisa melihat dan bergabung dengan open trip Anda.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Mohon lengkapi semua field yang wajib (*)")
    
    # ===== TAB 3: TRIP SAYA =====
    with tab3:
        st.markdown("### 📋 Open Trip yang Saya Buat")
        
        user = get_current_user()
        
        if user:
            # Filter trips created by current user (by name for demo)
            my_trips = [t for t in st.session_state.open_trips if t["creator_name"] == user.get("name", "")]
            
            if my_trips:
                for trip in my_trips:
                    slots_left = trip["max_members"] - trip["current_members"]
                    
                    st.markdown(f"""
                    <div style="background: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong>{trip['title']}</strong><br>
                                <small>📅 {trip['departure_date']} • 👥 {trip['current_members']}/{trip['max_members']} peserta</small>
                            </div>
                            <div>
                                <span style="background: {'#4CAF50' if trip['status'] == 'open' else '#666'}; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem;">
                                    {'🟢 Open' if trip['status'] == 'open' else '⚫ Closed'}
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{trip['id']}"):
                            st.info("Fitur edit akan segera hadir!")
                    with col2:
                        if st.button("🔴 Tutup", key=f"close_{trip['id']}"):
                            # Try database first
                            if DB_AVAILABLE and is_db_available() and isinstance(trip.get('id'), int):
                                db_update_trip_status(trip['id'], 'closed')
                            trip["status"] = "closed"
                            st.success("Trip ditutup")
                            st.rerun()
                    with col3:
                        if st.button("🗑️ Hapus", key=f"delete_{trip['id']}"):
                            # Try database first
                            if DB_AVAILABLE and is_db_available() and isinstance(trip.get('id'), int):
                                db_delete_trip(trip['id'])
                            if trip in st.session_state.open_trips:
                                st.session_state.open_trips.remove(trip)
                            st.success("Trip dihapus")
                            st.rerun()
            else:
                st.info("Anda belum membuat open trip. Buat sekarang di tab 'Buat Open Trip'!")
        else:
            st.warning("🔐 Login untuk melihat open trip yang Anda buat.")
    
    # Info section
    st.markdown("---")
    st.markdown("### 💡 Tentang Umrah Bareng")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🤝 Apa itu Umrah Bareng?**
        
        Platform untuk mencari teman perjalanan umrah dengan kriteria yang cocok:
        - Budget yang sama
        - Jadwal yang sesuai
        - Preferensi yang mirip
        - Dapat diskon grup
        """)
    
    with col2:
        st.markdown("""
        **✨ Keuntungan:**
        
        - 💰 Lebih hemat dengan grup
        - 👥 Dapat teman perjalanan
        - 🕋 Ibadah lebih nyaman
        - 📱 Koordinasi mudah via WhatsApp
        """)
    
    st.markdown("""
<div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); border-left: 4px solid #FF9800; border-radius: 10px; padding: 20px; margin-top: 20px;">
<div style="color: #E65100; font-weight: 700; font-size: 1rem; margin-bottom: 10px;">⚠️ Disclaimer - Umrah Bareng</div>
<div style="color: #5D4037; font-size: 0.9rem; line-height: 1.7;">
<p style="margin-bottom: 10px;"><strong>LABBAIK hanya memfasilitasi pertemuan antar calon jamaah.</strong></p>
<ul style="margin: 0; padding-left: 20px;">
<li>Segala transaksi dilakukan langsung antar peserta</li>
<li>Verifikasi identitas peserta secara mandiri</li>
<li>Pilih travel agent resmi berizin Kemenag RI</li>
<li>Cek legalitas di: <strong>siskopatuh.kemenag.go.id</strong></li>
</ul>
<p style="margin-top: 10px; font-style: italic; color: #795548;">"Bertawakkal setelah berikhtiar dengan maksimal"</p>
</div>
</div>
""", unsafe_allow_html=True)


# ============================================
# UMRAH MANDIRI - INDEPENDENT UMRAH GUIDE
# ============================================

def init_forum_state():
    """Initialize Forum Umrah Mandiri session state - load from database if available"""
    if "forum_posts" not in st.session_state:
        # Try to load from database first
        if DB_AVAILABLE and is_db_available():
            try:
                db_posts = db_get_forum_posts()
                if db_posts:
                    st.session_state.forum_posts = db_posts
                    st.session_state.posts_from_db = True
                    return
            except:
                pass
        
        # Fallback to sample data
        st.session_state.forum_posts = [
            {
                "id": "F001",
                "author": "Pak Hendra",
                "author_city": "Jakarta",
                "avatar": "👨‍💼",
                "title": "Pengalaman Umrah Mandiri Pertama Kali - Total Rp 18 Juta!",
                "category": "Pengalaman",
                "content": """Alhamdulillah baru pulang dari umrah mandiri perdana. Sharing pengalaman ya:

**Budget Total (1 orang, 9 hari):**
- Tiket PP Jakarta-Jeddah (Saudi Airlines): Rp 8.5 juta
- Visa Umrah (via agen visa): Rp 600rb
- Hotel Makkah (4 malam, 800m dari Haram): Rp 3.2 juta
- Hotel Madinah (3 malam, 500m dari Nabawi): Rp 2.4 juta
- Transport Jeddah-Makkah-Madinah-Jeddah: Rp 1.5 juta
- Makan & lain-lain: Rp 1.8 juta
**TOTAL: Rp 18 juta**

**Tips dari saya:**
1. Book tiket 3 bulan sebelumnya, dapat harga murah
2. Hotel pilih yang ada dapur, bisa masak sendiri
3. Download app Careem/Uber Saudi untuk transport
4. Bawa bekal mie instan & bumbu dari Indonesia 😄

Kalau ada yang mau tanya-tanya, silakan!""",
                "likes": 47,
                "comments": [
                    {"author": "Bu Ani", "text": "MasyaAllah, sangat membantu! Gimana caranya dapat visa pak?", "time": "2 jam lalu"},
                    {"author": "Rizki", "text": "Wah murah banget! Saya kemarin via travel agent Rp 28 juta", "time": "5 jam lalu"},
                    {"author": "Pak Hendra", "text": "@Bu Ani: Visa bisa via agen visa online, processing 3-5 hari kerja", "time": "1 jam lalu"},
                ],
                "created_at": "2025-01-20",
                "views": 324,
            },
            {
                "id": "F002",
                "author": "Mbak Fatimah",
                "author_city": "Surabaya",
                "avatar": "👩‍🦱",
                "title": "Tips Umrah Mandiri untuk Wanita Solo - Aman & Nyaman!",
                "category": "Tips & Trik",
                "content": """Salam ukhti semua! Saya baru saja umrah mandiri sendirian sebagai wanita. Banyak yang tanya, aman nggak? AMAN BANGET!

**Kenapa aman:**
1. Saudi sekarang sangat aman, banyak CCTV & polisi
2. Jamaah dari seluruh dunia, suasana sangat religius
3. Hotel-hotel sangat kooperatif dengan solo traveler

**Tips khusus wanita:**
- Pilih hotel yang ada staff wanita
- Simpan nomor darurat kedutaan Indonesia
- Join grup WA jamaah Indonesia (banyak di FB)
- Bawa obat-obatan pribadi yang cukup
- Pakai gamis/abaya yang nyaman untuk jalan jauh

**Pengalaman spiritual:**
Justru umrah mandiri itu lebih khusyuk! Kita bisa atur pace sendiri, mau lama di Raudhah bisa, mau thawaf malam-malam juga bebas.

Semoga bermanfaat! 💚""",
                "likes": 89,
                "comments": [
                    {"author": "Rina", "text": "MasyaAllah inspiring sekali mbak! Jadi pengen coba", "time": "1 hari lalu"},
                    {"author": "Dewi", "text": "Kalau mahram gimana mbak? Perlu nggak?", "time": "12 jam lalu"},
                ],
                "created_at": "2025-01-18",
                "views": 512,
            },
            {
                "id": "F003",
                "author": "Ustadz Farid",
                "author_city": "Bandung",
                "avatar": "👳",
                "title": "Panduan Lengkap Manasik Umrah Mandiri - Step by Step",
                "category": "Panduan",
                "content": """Bismillah, saya ingin berbagi panduan manasik untuk yang umrah mandiri:

**PERSIAPAN SEBELUM BERANGKAT:**
1. Niat yang ikhlas lillahi ta'ala
2. Pelajari tata cara umrah (video, buku, atau ikut kajian)
3. Hafal doa-doa: niat ihram, talbiyah, doa thawaf, doa sa'i
4. Siapkan fisik - biasakan jalan kaki

**SAAT DI MIQAT (Bir Ali/Bandara):**
- Mandi sunnah (kalau memungkinkan)
- Pakai pakaian ihram
- Niat umrah & baca talbiyah

**DI MASJIDIL HARAM:**
1. **Thawaf** - 7 putaran, mulai dari Hajar Aswad
2. **Sholat 2 rakaat** di belakang Maqam Ibrahim
3. **Minum air zamzam**
4. **Sa'i** - 7 kali antara Shafa dan Marwa
5. **Tahallul** - potong/cukur rambut

**TIPS PENTING:**
- Jangan panik, ikuti arus jamaah
- Kalau bingung, tanya jamaah Indonesia lain
- Bawa buku saku doa-doa
- Pakai sandal yang nyaman!

Semoga Allah memudahkan perjalanan umrah kita semua. Aamiin.""",
                "likes": 156,
                "comments": [
                    {"author": "Ahmad", "text": "Jazakallah khair ustadz, sangat lengkap!", "time": "3 hari lalu"},
                    {"author": "Siti", "text": "Alhamdulillah dapat ilmu, bookmark dulu", "time": "2 hari lalu"},
                ],
                "created_at": "2025-01-15",
                "views": 789,
            },
            {
                "id": "F004",
                "author": "Keluarga Santoso",
                "author_city": "Yogyakarta",
                "avatar": "👨‍👩‍👧‍👦",
                "title": "Umrah Mandiri Sekeluarga (4 Orang) - Hemat Rp 40 Juta!",
                "category": "Pengalaman",
                "content": """Assalamualaikum, mau sharing pengalaman umrah mandiri sekeluarga:

**Komposisi:** Saya, istri, 2 anak (12 & 8 tahun)

**Perbandingan Biaya:**
- Travel Agent: Rp 35 juta x 4 = **Rp 140 juta**
- Umrah Mandiri: **Rp 100 juta** (untuk 4 orang!)
- **HEMAT: Rp 40 juta!**

**Rincian Biaya Mandiri (4 orang):**
- Tiket PP x 4: Rp 32 juta
- Visa x 4: Rp 2.4 juta
- Hotel Makkah (family room, 5 malam): Rp 18 juta
- Hotel Madinah (family room, 4 malam): Rp 12 juta
- Sewa mobil + driver 10 hari: Rp 15 juta
- Makan & misc: Rp 20 juta

**Tips dengan Anak-anak:**
1. Pilih waktu yang tidak terlalu panas (Januari-Februari)
2. Hotel HARUS dekat Haram, anak-anak capek jalan jauh
3. Bawa stroller untuk anak kecil
4. Siapkan snack kesukaan anak
5. Thawaf & sa'i waktu malam, lebih sejuk & sepi

**Momen Terindah:**
Melihat anak-anak excited di depan Ka'bah, priceless! 💚

Silakan tanya-tanya ya!""",
                "likes": 203,
                "comments": [
                    {"author": "Bunda Maya", "text": "MasyaAllah! Ini yang saya cari. Pengen ajak anak tapi budget terbatas", "time": "6 jam lalu"},
                    {"author": "Pak Budi", "text": "Mantap pak! Sewa mobil dimana ya?", "time": "1 hari lalu"},
                ],
                "created_at": "2025-01-22",
                "views": 634,
            },
            {
                "id": "F005",
                "author": "Via LABBAIK.AI",
                "author_city": "Platform",
                "avatar": "🤖",
                "title": "Testimoni: Planning Umrah Mandiri Pakai LABBAIK - Mudah Banget!",
                "category": "Testimoni LABBAIK",
                "content": """Halo semuanya! Saya mau share pengalaman pakai LABBAIK.AI untuk planning umrah mandiri:

**Kenapa pakai LABBAIK?**
1. Bisa simulasi biaya dengan berbagai skenario
2. AI-nya pinter, bisa jawab semua pertanyaan tentang umrah
3. Ada rekomendasi hotel dan maskapai
4. Bisa bandingkan paket Ekonomis vs Premium

**Yang saya suka:**
- Fitur "Cari Paket by Budget" - masukin budget, langsung keluar opsi
- Chat AI 24 jam, tanya manasik dijawab lengkap
- Perbandingan skenario sangat membantu decide

**Hasil:**
Dari awalnya bingung mau arrange sendiri, sekarang jadi PD! LABBAIK bantu breakdown semua:
- Estimasi biaya realistis
- Timeline persiapan
- Checklist dokumen

Recommended banget buat yang mau umrah mandiri tapi bingung mulai dari mana! 🌟

#LABBAIK #UmrahMandiri #TestimoniAsli""",
                "likes": 78,
                "comments": [
                    {"author": "Nana", "text": "Wah baru tau ada platform kayak gini, keren!", "time": "4 jam lalu"},
                    {"author": "Rudi", "text": "Link nya mana nih? Mau coba juga", "time": "2 jam lalu"},
                ],
                "created_at": "2025-01-25",
                "views": 445,
            },
        ]
        st.session_state.posts_from_db = False


def render_umrah_mandiri():
    """Render Umrah Mandiri Guide and Forum"""
    init_forum_state()
    
    st.header("🕋 Umrah Mandiri")
    st.markdown("Panduan lengkap umrah mandiri & forum sharing pengalaman!")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📖 Apa itu Umrah Mandiri?", "💬 Forum Diskusi", "✍️ Tulis Pengalaman"])
    
    # ===== TAB 1: APA ITU UMRAH MANDIRI =====
    with tab1:
        # Hero Section
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
        
        # What is Umrah Mandiri
        st.markdown("### 🤔 Apa Sih Umrah Mandiri Itu?")
        
        st.markdown("""
        **Umrah Mandiri** adalah ibadah umrah yang kamu atur sendiri tanpa menggunakan jasa travel agent. 
        Mulai dari tiket pesawat, hotel, visa, sampai transportasi di Arab Saudi - semuanya kamu yang handle!
        
        *"Lho, memangnya boleh?"* 
        
        **Boleh banget!** Sejak tahun 2019, Arab Saudi membuka **visa umrah elektronik (e-visa)** yang bisa diajukan 
        secara online. Jadi sekarang siapa aja bisa umrah mandiri dengan legal dan aman. 👍
        """)
        
        # Comparison Box
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1A1A 0%, #1A2744 100%); border: 2px solid #2196F3; border-radius: 15px; padding: 20px;">
                <h4 style="color: #64B5F6; margin-top: 0;">🏢 Via Travel Agent</h4>
                <ul style="color: #E8E8E8;">
                    <li>Semua diurus travel</li>
                    <li>Ada muthawwif/guide</li>
                    <li>Jadwal sudah fix</li>
                    <li>Berangkat rombongan</li>
                    <li style="color: #FF9800; font-weight: 600;">Biaya: Rp 25-50 juta</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1A1A 0%, #1E3D2F 100%); border: 2px solid #4CAF50; border-radius: 15px; padding: 20px;">
                <h4 style="color: #81C784; margin-top: 0;">🎒 Umrah Mandiri</h4>
                <ul style="color: #E8E8E8;">
                    <li>Atur sendiri semuanya</li>
                    <li>Belajar manasik sendiri</li>
                    <li>Jadwal fleksibel</li>
                    <li>Bisa solo/keluarga/grup kecil</li>
                    <li style="color: #4CAF50; font-weight: 600;">Biaya: Rp 15-25 juta ✨</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Legal Basis Section
        st.markdown("### 📜 Dasar Hukum & Regulasi")
        
        st.markdown("""
        Tenang, umrah mandiri itu **100% legal**! Ini dasar hukumnya:
        """)
        
        with st.expander("🇸🇦 Regulasi Arab Saudi", expanded=True):
            st.markdown("""
            **1. Saudi Vision 2030 - Tourism Sector**
            - Arab Saudi membuka diri untuk wisatawan termasuk jamaah umrah independen
            - E-visa umrah bisa diajukan online sejak September 2019
            - Processing time: 24-48 jam
            - Biaya visa: ~SAR 300 (sekitar Rp 1.2 juta)
            
            **2. Nusuk Platform (Resmi dari Kemenag Saudi)**
            - Platform resmi pemerintah Saudi untuk booking umrah
            - Website: nusuk.sa
            - Bisa booking hotel & paket umrah langsung
            
            **3. Syarat Visa Umrah Elektronik:**
            - Paspor valid minimal 6 bulan
            - Bukti akomodasi (hotel booking)
            - Tiket pesawat PP
            - Asuransi perjalanan
            - Foto digital sesuai ketentuan
            """)
        
        with st.expander("🇮🇩 Regulasi Indonesia"):
            st.markdown("""
            **1. Kementerian Agama RI**
            - Tidak ada larangan untuk umrah mandiri
            - Yang diatur ketat adalah **penyelenggara travel umrah** (harus berizin)
            - Jamaah bebas memilih umrah via travel atau mandiri
            
            **2. Tips Legal di Indonesia:**
            - Pastikan paspor masih berlaku > 6 bulan
            - Daftar ke Siskohat (Sistem Komputerisasi Haji Terpadu) tidak wajib untuk umrah
            - Simpan semua bukti booking sebagai dokumen perjalanan
            
            **3. Perlindungan Konsumen:**
            - Jika umrah mandiri, tanggung jawab sepenuhnya di jamaah
            - Disarankan beli asuransi perjalanan yang cover medical
            - Simpan nomor KBRI Riyadh: +966-11-488-2800
            """)
        
        with st.expander("✈️ Regulasi Penerbangan"):
            st.markdown("""
            **Maskapai yang Terbang Langsung ke Arab Saudi:**
            - Garuda Indonesia (CGK-JED)
            - Saudi Airlines (CGK/SUB-JED/MED)
            - Emirates (via Dubai)
            - Qatar Airways (via Doha)
            - Etihad (via Abu Dhabi)
            
            **Tips Booking Tiket:**
            - Bisa langsung ke website maskapai
            - Atau via online travel agent (Traveloka, Tiket.com, dll)
            - Tidak perlu surat keterangan dari travel agent
            """)
        
        st.markdown("---")
        
        # Pros and Cons
        st.markdown("### ⚖️ Kelebihan & Pertimbangan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **✅ Kelebihan Umrah Mandiri:**
            
            1. **💰 Lebih Hemat**
               - Bisa hemat 30-50% dari travel agent
               - Pilih hotel sesuai budget
            
            2. **⏰ Fleksibel**
               - Tentukan tanggal sendiri
               - Durasi sesuai keinginan
               - Pace ibadah sesuai kemampuan
            
            3. **🕋 Lebih Khusyuk**
               - Tidak terikat jadwal rombongan
               - Bisa lama di Raudhah/Multazam
               - Quality time dengan keluarga
            
            4. **📚 Pengalaman Belajar**
               - Belajar manasik lebih dalam
               - Lebih appreciate prosesnya
               - Skill traveling meningkat
            """)
        
        with col2:
            st.markdown("""
            **⚠️ Yang Perlu Dipertimbangkan:**
            
            1. **📋 Perlu Persiapan Matang**
               - Riset hotel, tiket, visa sendiri
               - Pelajari manasik dengan baik
            
            2. **🗣️ Kendala Bahasa**
               - Bahasa Arab tidak semua paham
               - Tapi banyak yang bisa Inggris
            
            3. **🚗 Transportasi**
               - Perlu arrange sendiri
               - Opsi: taksi, Uber/Careem, sewa mobil
            
            4. **👥 Tidak Ada Guide**
               - Perlu hafal doa-doa sendiri
               - Tapi banyak app & buku panduan
            
            5. **🆘 Handle Masalah Sendiri**
               - Jika ada kendala, solve sendiri
               - Tapi ada KBRI & komunitas Indonesia
            """)
        
        st.markdown("---")
        
        # Step by Step Guide
        st.markdown("### 📝 Langkah-Langkah Umrah Mandiri")
        
        steps = [
            ("1️⃣", "Persiapan Dokumen", "Pastikan paspor valid > 6 bulan, siapkan foto digital, KTP"),
            ("2️⃣", "Booking Tiket Pesawat", "Cari tiket PP ke Jeddah/Madinah, book 2-3 bulan sebelumnya untuk harga terbaik"),
            ("3️⃣", "Booking Hotel", "Pesan via Booking.com, Agoda, atau langsung ke hotel. Pilih dekat Masjidil Haram/Nabawi"),
            ("4️⃣", "Apply Visa Umrah", "Via platform resmi atau agen visa terpercaya. Processing 1-5 hari kerja"),
            ("5️⃣", "Beli Asuransi Perjalanan", "Wajib! Cover minimal medical emergency di luar negeri"),
            ("6️⃣", "Pelajari Manasik", "Hafal niat, talbiyah, doa thawaf, doa sa'i. Bisa via YouTube/buku/kajian"),
            ("7️⃣", "Siapkan Perlengkapan", "Pakaian ihram, sandal nyaman, obat-obatan, adaptor colokan"),
            ("8️⃣", "Berangkat & Nikmati!", "Bismillah, berangkat dengan niat lillahi ta'ala 🕋"),
        ]
        
        for icon, title, desc in steps:
            st.markdown(f"""
            <div style="display: flex; align-items: flex-start; margin-bottom: 15px; padding: 15px; background: #f9f9f9; border-radius: 10px; border-left: 4px solid {COLORS['gold']};">
                <div style="font-size: 1.5rem; margin-right: 15px;">{icon}</div>
                <div>
                    <div style="font-weight: 700; color: #1A1A1A;">{title}</div>
                    <div style="color: #666; font-size: 0.9rem;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Cost Estimation
        st.markdown("### 💰 Estimasi Biaya Umrah Mandiri")
        
        st.markdown("""
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); border: 2px solid #D4AF37; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
<h4 style="color: #D4AF37; margin-top: 0;">💡 Perkiraan Budget (1 orang, 9-10 hari)</h4>
<table style="width: 100%; color: #E8E8E8;">
<tr style="border-bottom: 1px solid #D4AF3740;">
<td style="padding: 8px 0; color: #C9A86C;"><strong>Item</strong></td>
<td style="text-align: right; color: #C9A86C;"><strong>Estimasi</strong></td>
</tr>
<tr style="border-bottom: 1px solid #D4AF3730;">
<td style="padding: 8px 0; color: #E8E8E8;">✈️ Tiket Pesawat PP</td>
<td style="text-align: right; color: #4CAF50; font-weight: 600;">Rp 7-12 juta</td>
</tr>
<tr style="border-bottom: 1px solid #D4AF3730;">
<td style="padding: 8px 0; color: #E8E8E8;">📄 Visa Umrah</td>
<td style="text-align: right; color: #4CAF50; font-weight: 600;">Rp 500rb - 1.5 juta</td>
</tr>
<tr style="border-bottom: 1px solid #D4AF3730;">
<td style="padding: 8px 0; color: #E8E8E8;">🏨 Hotel Makkah (4-5 malam)</td>
<td style="text-align: right; color: #4CAF50; font-weight: 600;">Rp 2-5 juta</td>
</tr>
<tr style="border-bottom: 1px solid #D4AF3730;">
<td style="padding: 8px 0; color: #E8E8E8;">🏨 Hotel Madinah (3-4 malam)</td>
<td style="text-align: right; color: #4CAF50; font-weight: 600;">Rp 1.5-4 juta</td>
</tr>
<tr style="border-bottom: 1px solid #D4AF3730;">
<td style="padding: 8px 0; color: #E8E8E8;">🚗 Transportasi Lokal</td>
<td style="text-align: right; color: #4CAF50; font-weight: 600;">Rp 1-2 juta</td>
</tr>
<tr style="border-bottom: 1px solid #D4AF3730;">
<td style="padding: 8px 0; color: #E8E8E8;">🍽️ Makan & Lain-lain</td>
<td style="text-align: right; color: #4CAF50; font-weight: 600;">Rp 1.5-3 juta</td>
</tr>
<tr>
<td style="padding: 12px 0;"><strong style="color: #D4AF37; font-size: 1.1rem;">TOTAL ESTIMASI</strong></td>
<td style="text-align: right;"><strong style="color: #D4AF37; font-size: 1.1rem;">Rp 15-25 juta</strong></td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)
        
        st.info("💡 **Tips:** Gunakan fitur **Simulasi Biaya** LABBAIK untuk hitung estimasi lebih akurat sesuai preferensi kamu!")
        
        # FAQ
        st.markdown("### ❓ FAQ Umrah Mandiri")
        
        with st.expander("Apakah wanita boleh umrah mandiri sendirian?"):
            st.markdown("""
            **Ya, boleh!** Sejak 2021, Arab Saudi sudah menghapus aturan mahram untuk wanita berusia 18+. 
            Wanita dewasa bisa umrah/haji sendiri tanpa ditemani mahram.
            
            Tips untuk wanita solo:
            - Pilih hotel yang aman dan dekat Masjid
            - Join grup WA jamaah Indonesia untuk support
            - Simpan nomor darurat KBRI
            """)
        
        with st.expander("Bagaimana cara dapat visa umrah tanpa travel agent?"):
            st.markdown("""
            Ada beberapa cara:
            1. **Via Nusuk.sa** - Platform resmi Saudi (self-apply)
            2. **Via Agen Visa Online** - Banyak yang melayani, processing 1-5 hari
            3. **Via VFS Global** - Partner resmi Kedutaan Saudi
            
            Syarat: Paspor valid, bukti hotel, tiket pesawat, foto digital.
            """)
        
        with st.expander("Apakah perlu sertifikat vaksin?"):
            st.markdown("""
            Per 2024, persyaratan vaksin COVID-19 sudah **tidak wajib** untuk umrah.
            Namun vaksin meningitis **tetap diwajibkan**. Bisa vaksin di Kantor Kesehatan Pelabuhan (KKP).
            """)
        
        with st.expander("Bagaimana kalau tidak bisa bahasa Arab?"):
            st.markdown("""
            **Tidak masalah!** 
            - Banyak petugas di Masjidil Haram yang bisa Inggris
            - Jamaah Indonesia banyak, bisa minta bantuan
            - Gunakan Google Translate untuk situasi darurat
            - Yang penting: hafal doa-doa dalam bahasa Arab
            """)
    
    # ===== TAB 2: FORUM DISKUSI =====
    with tab2:
        st.markdown("### 💬 Forum Umrah Mandiri")
        st.markdown("Tempat sharing pengalaman, tips, dan tanya jawab seputar umrah mandiri!")
        
        # Stats
        total_posts = len(st.session_state.forum_posts)
        total_views = sum([p["views"] for p in st.session_state.forum_posts])
        total_likes = sum([p["likes"] for p in st.session_state.forum_posts])
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        with stat_col1:
            st.metric("📝 Total Post", total_posts)
        with stat_col2:
            st.metric("👀 Total Views", f"{total_views:,}")
        with stat_col3:
            st.metric("❤️ Total Likes", f"{total_likes:,}")
        with stat_col4:
            st.metric("💬 Diskusi Aktif", len([p for p in st.session_state.forum_posts if len(p["comments"]) > 0]))
        
        st.markdown("---")
        
        # Filter
        filter_col1, filter_col2 = st.columns([2, 1])
        with filter_col1:
            category_filter = st.selectbox(
                "🏷️ Filter Kategori",
                options=["Semua", "Pengalaman", "Tips & Trik", "Panduan", "Testimoni LABBAIK", "Tanya Jawab"]
            )
        with filter_col2:
            sort_by = st.selectbox(
                "📊 Urutkan",
                options=["Terbaru", "Paling Populer", "Paling Banyak Dilihat"]
            )
        
        # Filter and sort posts
        filtered_posts = st.session_state.forum_posts.copy()
        
        if category_filter != "Semua":
            filtered_posts = [p for p in filtered_posts if p["category"] == category_filter]
        
        if sort_by == "Paling Populer":
            filtered_posts.sort(key=lambda x: x["likes"], reverse=True)
        elif sort_by == "Paling Banyak Dilihat":
            filtered_posts.sort(key=lambda x: x["views"], reverse=True)
        else:
            filtered_posts.sort(key=lambda x: x["created_at"], reverse=True)
        
        st.markdown(f"**Menampilkan {len(filtered_posts)} postingan**")
        st.markdown("---")
        
        # Display posts
        for post in filtered_posts:
            # Category colors
            cat_colors = {
                "Pengalaman": ("#4CAF50", "#E8F5E9"),
                "Tips & Trik": ("#2196F3", "#E3F2FD"),
                "Panduan": ("#9C27B0", "#F3E5F5"),
                "Testimoni LABBAIK": ("#D4AF37", "#FFF8E1"),
                "Tanya Jawab": ("#FF5722", "#FBE9E7"),
            }
            cat_color, cat_bg = cat_colors.get(post["category"], ("#666", "#f5f5f5"))
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e0e0e0; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 2rem; margin-right: 12px;">{post['avatar']}</span>
                        <div>
                            <span style="font-weight: 600; color: #1A1A1A;">{post['author']}</span>
                            <span style="color: #888; font-size: 0.85rem; margin-left: 8px;">• {post['author_city']}</span>
                            <div style="font-size: 0.8rem; color: #999;">{post['created_at']}</div>
                        </div>
                    </div>
                    <span style="background: {cat_bg}; color: {cat_color}; padding: 4px 12px; border-radius: 15px; font-size: 0.75rem; font-weight: 600;">
                        {post['category']}
                    </span>
                </div>
                <h4 style="color: #1A1A1A; margin: 0 0 10px 0; line-height: 1.4;">{post['title']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Content preview
            with st.expander("📖 Baca Selengkapnya"):
                st.markdown(post["content"])
                
                st.markdown("---")
                
                # Engagement stats
                eng_col1, eng_col2, eng_col3, eng_col4 = st.columns(4)
                with eng_col1:
                    if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                        post["likes"] += 1
                        st.rerun()
                with eng_col2:
                    st.markdown(f"👀 {post['views']} views")
                with eng_col3:
                    st.markdown(f"💬 {len(post['comments'])} komentar")
                with eng_col4:
                    st.button("🔗 Share", key=f"share_{post['id']}")
                
                # Comments
                if post["comments"]:
                    st.markdown("**💬 Komentar:**")
                    for comment in post["comments"]:
                        st.markdown(f"""
                        <div style="background: #f5f5f5; padding: 10px 15px; border-radius: 10px; margin-bottom: 8px;">
                            <strong>{comment['author']}</strong> • <span style="color: #888; font-size: 0.85rem;">{comment['time']}</span>
                            <div style="margin-top: 5px;">{comment['text']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Add comment
                new_comment = st.text_input("Tulis komentar...", key=f"comment_input_{post['id']}")
                if st.button("Kirim Komentar", key=f"send_comment_{post['id']}"):
                    if new_comment:
                        user = get_current_user()
                        post["comments"].append({
                            "author": user.get("name", "Guest") if user else "Guest",
                            "text": new_comment,
                            "time": "Baru saja"
                        })
                        st.success("Komentar terkirim!")
                        st.rerun()
    
    # ===== TAB 3: TULIS PENGALAMAN =====
    with tab3:
        st.markdown("### ✍️ Bagikan Pengalaman Umrah Mandiri Kamu!")
        st.markdown("Ceritakan pengalamanmu untuk menginspirasi jamaah lainnya.")
        
        user = get_current_user()
        
        if not user:
            st.warning("🔐 Silakan login untuk menulis pengalaman.")
        else:
            with st.form("new_forum_post"):
                post_title = st.text_input(
                    "📌 Judul Postingan *",
                    placeholder="Contoh: Pengalaman Umrah Mandiri Pertama Kali!"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    post_category = st.selectbox(
                        "🏷️ Kategori *",
                        options=["Pengalaman", "Tips & Trik", "Panduan", "Testimoni LABBAIK", "Tanya Jawab"]
                    )
                with col2:
                    author_city = st.text_input(
                        "🏙️ Kota Kamu",
                        value=user.get("city", "Indonesia")
                    )
                
                post_content = st.text_area(
                    "📝 Isi Postingan *",
                    placeholder="Ceritakan pengalamanmu... Tips, biaya, momen berkesan, dll.",
                    height=300
                )
                
                st.markdown("""
**💡 Tips menulis yang menarik:**
- Ceritakan detail biaya untuk membantu jamaah lain
- Share tips praktis yang berguna
- Tambahkan momen berkesan untuk inspirasi
- Gunakan format yang mudah dibaca (poin-poin, emoji)
""")

                submitted = st.form_submit_button("🚀 Publikasikan", use_container_width=True)

                if submitted:
                    if post_title and post_content:
                        user_id = user.get("id") if user else None
                        post_saved = False

                        # Try database first
                        if DB_AVAILABLE and is_db_available() and user_id:
                            try:
                                result = db_create_post(user_id, post_title, post_category, post_content)
                                if result.get("success"):
                                    st.success("✅ Postingan berhasil dipublikasikan!")
                                    st.balloons()
                                    post_saved = True
                                    # Refresh posts from database
                                    st.session_state.forum_posts = db_get_forum_posts()
                                else:
                                    st.warning(f"Database error: {result.get('error')}")
                            except Exception as e:
                                st.warning(f"Database error, menyimpan secara lokal: {e}")

                        # Fallback to session state if database fails
                        if not post_saved:
                            new_post = {
                                "id": f"F{len(st.session_state.forum_posts) + 1:03d}",
                                "author": user.get("name", "Anonymous"),
                                "author_city": author_city,
                                "avatar": "👤",
                                "title": post_title,
                                "category": post_category,
                                "content": post_content,
                                "likes": 0,
                                "comments": [],
                                "created_at": str(datetime.now().date()),
                                "views": 0,
                                }
                            st.session_state.forum_posts.insert(0, new_post)
                            st.success("✅ Postingan berhasil dipublikasikan!")
                            st.balloons()
                    else:
                        st.error("❌ Mohon isi judul dan konten postingan.")

    # Guidelines
    st.markdown("---")
    st.markdown("### 📋 Panduan Komunitas")

    st.markdown("""
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #1E3D2F 100%); border-radius: 15px; padding: 20px; border: 1px solid #4CAF5040;">
<h4 style="color: #4CAF50; margin-top: 0;">✅ Yang Boleh Diposting:</h4>
<ul style="color: #E8E8E8;">
<li>Pengalaman umrah mandiri (positif maupun tantangan)</li>
<li>Tips & trik hemat biaya</li>
<li>Panduan manasik dan doa-doa</li>
<li>Rekomendasi hotel, transportasi, kuliner</li>
<li>Pertanyaan seputar umrah mandiri</li>
</ul>

<h4 style="color: #EF5350; margin-top: 20px;">❌ Yang Tidak Diperbolehkan:</h4>
<ul style="color: #E8E8E8;">
<li>Promosi travel agent atau jasa komersial</li>
<li>Konten yang mengandung SARA</li>
<li>Informasi yang menyesatkan</li>
<li>Spam atau postingan berulang</li>
</ul>
</div>
""", unsafe_allow_html=True)
    
    # Bottom Section
    st.markdown("---")
    st.markdown(f"""
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1A1A1A 0%, #333 100%); border-radius: 15px;">
<div style="color: {COLORS['gold']}; font-size: 1.3rem; margin-bottom: 10px;">🕋 Siap Umrah Mandiri?</div>
<div style="color: white; margin-bottom: 15px;">Gunakan LABBAIK untuk planning umrah mandiri yang terencana dan hemat!</div>
<div style="color: {COLORS['sand']}; font-size: 0.9rem;">💰 Simulasi Biaya • 🤖 AI Assistant • 📊 Perbandingan Paket</div>
</div>
""", unsafe_allow_html=True)
    
    # DYOR Disclaimer for Umrah Mandiri
    st.markdown("""
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #1A2744 100%); border: 2px solid #2196F3; border-radius: 15px; padding: 25px; margin-top: 25px;">
<div style="text-align: center; margin-bottom: 15px;">
<span style="background: #2196F3; color: white; padding: 8px 20px; border-radius: 20px; font-weight: 700; font-size: 0.9rem;">📋 DYOR - Do Your Own Research</span>
</div>
<div style="color: #E8E8E8; font-size: 0.95rem; line-height: 1.8;">
<p style="text-align: center; font-weight: 600; margin-bottom: 15px;">Informasi di halaman ini bersifat <strong style="color: #64B5F6;">panduan umum</strong> dan <strong style="color: #64B5F6;">estimasi</strong>.<br>BUKAN pengganti riset pribadi Anda.</p>
</div>
</div>
""", unsafe_allow_html=True)
    
    # Use columns for the two info boxes
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
<div style="background: #1A1A1A; padding: 15px; border-radius: 10px; border-left: 4px solid #4CAF50; margin-bottom: 15px;">
<div style="font-weight: 700; color: #4CAF50; margin-bottom: 8px;">✅ Verifikasi Sumber Resmi:</div>
<ul style="margin: 0; padding-left: 18px; color: #E8E8E8; font-size: 0.9rem;">
<li><strong style="color: #C9A86C;">Arab Saudi:</strong> nusuk.sa</li>
<li><strong style="color: #C9A86C;">Indonesia:</strong> kemenag.go.id</li>
<li><strong style="color: #C9A86C;">KBRI Riyadh:</strong> +966-11-488-2800</li>
</ul>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
<div style="background: #1A1A1A; padding: 15px; border-radius: 10px; border-left: 4px solid #FF9800; margin-bottom: 15px;">
<div style="font-weight: 700; color: #FF9800; margin-bottom: 8px;">⚠️ Perlu Diingat:</div>
<ul style="margin: 0; padding-left: 18px; color: #E8E8E8; font-size: 0.9rem;">
<li>Harga dapat berubah sewaktu-waktu</li>
<li>Regulasi visa dapat berubah</li>
<li>Anda bertanggung jawab penuh</li>
</ul>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("""
<div style="text-align: center; color: #C9A86C; font-style: italic; padding: 15px; background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); border-radius: 10px; margin-top: 10px; border: 1px solid #D4AF3730;">
"Sebaik-baik persiapan adalah ilmu, sebaik-baik bekal adalah taqwa" 🤲
</div>
""", unsafe_allow_html=True)


def render_settings():
    """Render settings page"""
    st.header("⚙️ Pengaturan")
    
    st.markdown("### 🔑 Konfigurasi API")
    
    provider = st.selectbox("LLM Provider", ["groq", "openai"], index=0 if llm_config.provider == "groq" else 1)
    
    if provider == "groq":
        api_key = st.text_input("Groq API Key", type="password", value=llm_config.groq_api_key[:10] + "..." if llm_config.groq_api_key else "")
        st.info("💡 Dapatkan API key gratis di https://console.groq.com")
    else:
        api_key = st.text_input("OpenAI API Key", type="password", value=llm_config.openai_api_key[:10] + "..." if llm_config.openai_api_key else "")
        st.info("💡 Dapatkan API key di https://platform.openai.com")
    
    st.markdown("### 📊 Status Sistem")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status Inisialisasi", "✅ Aktif" if st.session_state.initialized else "❌ Belum Aktif")
    with col2:
        if st.session_state.orchestrator:
            stats = st.session_state.orchestrator.get_agent_status()
            st.metric("Dokumen Knowledge Base", stats["rag_retriever"]["total_documents"])
    
    if st.button("🔄 Reinisialisasi Sistem"):
        st.session_state.orchestrator = None
        st.session_state.initialized = False
        initialize_system()
        st.rerun()
    
    st.markdown("### ℹ️ Informasi Aplikasi")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""**{APP_INFO['name']}** v{__version__}\n\n{APP_INFO['tagline']}\n\n**Developer:** {DEVELOPER['name']}\n**Email:** {DEVELOPER['email']}""")
    with col2:
        st.info(f"""**Repository:**\n{APP_INFO['repository']}\n\n**Demo:**\n{APP_INFO['demo_url']}\n\n**License:** {APP_INFO['license']}""")


def render_about():
    """Render about page with LABBAIK branding"""
    
    about_header = f"""
<div style="background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 50%, {COLORS['black']} 100%); color: white; padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
    <div style="font-family: 'Noto Naskh Arabic', serif; font-size: 2.5rem; color: {COLORS['gold']}; text-shadow: 0 2px 15px rgba(212, 175, 55, 0.4);">{BRAND['talbiyah']}</div>
    <div style="font-size: 2rem; font-weight: 700; letter-spacing: 0.3em; margin: 15px 0;">{BRAND['name']}</div>
    <div style="color: {COLORS['sand']}; font-size: 1.1rem; margin-bottom: 15px;">{BRAND['tagline']}</div>
    <div style="color: {COLORS['sand']}; font-size: 0.95rem;">{BRAND['description']}</div>
    <div style="margin-top: 20px;"><span style="background: linear-gradient(135deg, {COLORS['gold']} 0%, {COLORS['sand']} 100%); color: {COLORS['black']}; padding: 8px 20px; border-radius: 20px; font-weight: 700;">Version {BRAND['version']}</span></div>
</div>
"""
    st.markdown(about_header, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["👨‍💻 Developer", "📋 Changelog", "🗺️ Roadmap", "🔧 Tech Stack", "📊 Stats", "⚖️ Legal & Disclaimer", "📱 Install App"])
    
    with tab1:
        st.markdown(get_developer_card(), unsafe_allow_html=True)
        st.markdown("### 📧 Kontak")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"📧 **Email**\n\n{DEVELOPER['email']}")
        with col2:
            st.markdown(f"💬 **WhatsApp**\n\n[Chat](https://wa.me/{DEVELOPER['whatsapp']})")
        with col3:
            st.markdown(f"🔗 **GitHub**\n\n[mshadianto]({DEVELOPER['github']})")
        with col4:
            st.markdown(f"💼 **LinkedIn**\n\n[Profile]({DEVELOPER['linkedin']})")
    
    with tab2:
        st.markdown(get_changelog_markdown())
    
    with tab3:
        st.markdown("### 🗺️ Roadmap - Rencana Pengembangan")
        
        st.markdown(f"""
<div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); border-radius: 15px; padding: 20px; margin-bottom: 20px;">
<h4 style="color: #2E7D32; margin-top: 0;">📱 Q1 2026 - Mobile App</h4>
<ul style="color: #333; line-height: 1.8;">
<li>🤖 <strong>Android App</strong> - Play Store release</li>
<li>🍎 <strong>iOS App</strong> - App Store release</li>
<li>🔔 <strong>Push Notifications</strong> - Reminder ibadah & updates</li>
<li>📴 <strong>Offline Mode</strong> - Akses tanpa internet</li>
</ul>
</div>

<div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); border-radius: 15px; padding: 20px; margin-bottom: 20px;">
<h4 style="color: #1565C0; margin-top: 0;">💳 Q2 2026 - Payment & Partnership</h4>
<ul style="color: #333; line-height: 1.8;">
<li>💰 <strong>Payment Gateway</strong> - Bayar langsung via app</li>
<li>🤝 <strong>Travel Agent Portal</strong> - Partnership dashboard</li>
<li>📍 <strong>Live Tracking</strong> - Track perjalanan real-time</li>
<li>🎫 <strong>E-Ticket</strong> - Tiket digital terintegrasi</li>
</ul>
</div>

<div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); border-radius: 15px; padding: 20px; margin-bottom: 20px;">
<h4 style="color: #E65100; margin-top: 0;">🌐 Q3 2026 - Global Expansion</h4>
<ul style="color: #333; line-height: 1.8;">
<li>🗣️ <strong>Multi-language</strong> - Arabic, English, Malay</li>
<li>🎤 <strong>Voice Assistant</strong> - Tanya dengan suara</li>
<li>📸 <strong>Photo Gallery</strong> - Share pengalaman visual</li>
<li>🌍 <strong>Regional Expansion</strong> - Malaysia, Singapore, Brunei</li>
</ul>
</div>

<div style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%); border-radius: 15px; padding: 20px;">
<h4 style="color: #7B1FA2; margin-top: 0;">🚀 Q4 2026 - Advanced Features</h4>
<ul style="color: #333; line-height: 1.8;">
<li>🧠 <strong>AI Travel Planner</strong> - Personalized itinerary</li>
<li>👥 <strong>Group Management</strong> - Kelola rombongan</li>
<li>📊 <strong>Analytics Dashboard</strong> - Insights perjalanan</li>
<li>🏆 <strong>Gamification</strong> - Badges & rewards</li>
</ul>
</div>
""", unsafe_allow_html=True)
        
        st.info("💡 **Ingin fitur tertentu diprioritaskan?** Hubungi kami via WhatsApp atau email!")
    
    with tab4:
        st.markdown("### 🔧 Technology Stack")
        for category, techs in TECH_STACK.items():
            st.markdown(f"#### {category.replace('_', ' ').title()}")
            for name, version, desc in techs:
                st.markdown(f"- **{name}** `{version}` - {desc}")
    
    with tab5:
        st.markdown("### 📊 Application Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Released", get_app_age())
        with col2:
            st.metric("🔄 Version", __version__)
        with col3:
            st.metric("📦 Modules", "8+")
    
    with tab6:
        st.markdown("### ⚖️ Legal & Disclaimer")
        
        st.markdown(f"""
<div style="background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); border: 2px solid #D32F2F; border-radius: 15px; padding: 25px; margin-bottom: 20px;">
<h4 style="color: #B71C1C; margin-top: 0;">⚠️ DISCLAIMER - HARAP DIBACA</h4>
<div style="color: #5D4037; line-height: 1.8;">
<p><strong>LABBAIK</strong> adalah platform berbasis AI untuk <strong>simulasi dan perencanaan</strong> umrah.
Platform ini:</p>
<ul>
<li>BUKAN travel agent dan tidak menjual paket umrah</li>
<li>BUKAN pengganti konsultasi dengan travel agent resmi</li>
<li>BUKAN sumber informasi resmi pemerintah</li>
<li>Dikembangkan oleh MS Hadianto dengan bantuan AI</li>
</ul>
</div>
</div>
""", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: #E8F5E9; border-radius: 15px; padding: 20px; height: 100%;">
                <h4 style="color: #2E7D32; margin-top: 0;">📌 Untuk Umrah via Travel Agent</h4>
                <ul style="color: #333; line-height: 1.8;">
                    <li>Pilih travel agent berizin <strong>Kemenag RI</strong></li>
                    <li>Verifikasi di: <strong>siskopatuh.kemenag.go.id</strong></li>
                    <li>Minta kontrak tertulis sebelum bayar</li>
                    <li>Simpan bukti pembayaran</li>
                    <li>Pahami hak & kewajiban Anda</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: #E3F2FD; border-radius: 15px; padding: 20px; height: 100%;">
                <h4 style="color: #1565C0; margin-top: 0;">🕋 Untuk Umrah Mandiri (DYOR)</h4>
                <ul style="color: #333; line-height: 1.8;">
                    <li><strong>Do Your Own Research</strong> - riset mandiri</li>
                    <li>Verifikasi regulasi di <strong>nusuk.sa</strong></li>
                    <li>Cek update di <strong>kemenag.go.id</strong></li>
                    <li>Simpan kontak KBRI Riyadh</li>
                    <li>Anda bertanggung jawab penuh atas keputusan</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"""
<div style="background: #FFF8E1; border-radius: 15px; padding: 20px; margin-top: 10px;">
<h4 style="color: #F57F17; margin-top: 0;">📋 Sumber Informasi Resmi</h4>
<table style="width: 100%; border-collapse: collapse;">
<tr style="border-bottom: 1px solid #FFE082;">
<td style="padding: 10px;"><strong>🇸🇦 Arab Saudi</strong></td>
<td style="padding: 10px;">nusuk.sa - Portal resmi visa & umrah</td>
</tr>
<tr style="border-bottom: 1px solid #FFE082;">
<td style="padding: 10px;"><strong>🇮🇩 Indonesia</strong></td>
<td style="padding: 10px;">kemenag.go.id - Kementerian Agama RI</td>
</tr>
<tr style="border-bottom: 1px solid #FFE082;">
<td style="padding: 10px;"><strong>✅ Verifikasi Travel</strong></td>
<td style="padding: 10px;">siskopatuh.kemenag.go.id</td>
</tr>
<tr>
<td style="padding: 10px;"><strong>🏛️ KBRI Riyadh</strong></td>
<td style="padding: 10px;">+966-11-488-2800</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)
        
        st.markdown(f"""
<div style="background: #F3E5F5; border-radius: 15px; padding: 20px; margin-top: 20px; text-align: center;">
<h4 style="color: #7B1FA2; margin-top: 0;">🤖 Tentang Pengembangan</h4>
<p style="color: #4A148C; line-height: 1.8;">
Platform ini dikembangkan oleh <strong>MS Hadianto</strong> dengan memanfaatkan teknologi AI
(<strong>Claude by Anthropic</strong> & <strong>Gemini by Google</strong>).<br><br>
Tujuannya adalah membantu calon jamaah dalam <strong>simulasi biaya</strong> dan
<strong>perencanaan perjalanan umrah</strong>.<br><br>
<em>"Sebaik-baik persiapan adalah ilmu, sebaik-baik bekal adalah taqwa"</em> 🤲
</p>
</div>
""", unsafe_allow_html=True)
    
    with tab7:
        st.markdown("### 📱 Install LABBAIK sebagai Aplikasi")
        
        # Install instructions - use st.columns for better rendering
        st.markdown("""
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); border: 2px solid rgba(212, 175, 55, 0.25); border-radius: 20px; padding: 25px; margin: 10px 0;">
<div style="text-align: center; margin-bottom: 20px;">
<span style="font-size: 3rem;">📱</span>
<h3 style="color: #D4AF37; margin: 10px 0 5px 0;">Install LABBAIK di HP Anda</h3>
<p style="color: #888; font-size: 0.9rem; margin: 0;">Akses LABBAIK langsung dari home screen - seperti aplikasi native!</p>
</div>
</div>
""", unsafe_allow_html=True)
        
        # Use columns for Android and iPhone instructions
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
<div style="background: #1E1E1E; border-radius: 15px; padding: 20px; border: 1px solid #333; height: 100%;">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
<span style="font-size: 1.5rem;">🤖</span>
<span style="color: #4CAF50; font-weight: 700; font-size: 1.1rem;">Android</span>
</div>
<div style="color: #aaa; font-size: 0.9rem; line-height: 2;">
1. Buka di <strong style="color: #4CAF50;">Chrome</strong><br>
2. Tap menu <strong style="color: #4CAF50;">⋮</strong> (kanan atas)<br>
3. Pilih "<strong style="color: #4CAF50;">Add to Home screen</strong>"<br>
4. Tap "<strong style="color: #4CAF50;">Add</strong>"
</div>
<div style="margin-top: 15px; padding: 10px; background: rgba(76, 175, 80, 0.15); border-radius: 8px; text-align: center;">
<span style="color: #4CAF50; font-size: 0.85rem;">✓ Gratis & Instant</span>
</div>
</div>
""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
<div style="background: #1E1E1E; border-radius: 15px; padding: 20px; border: 1px solid #333; height: 100%;">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
<span style="font-size: 1.5rem;">🍎</span>
<span style="color: #007AFF; font-weight: 700; font-size: 1.1rem;">iPhone / iPad</span>
</div>
<div style="color: #aaa; font-size: 0.9rem; line-height: 2;">
1. Buka di <strong style="color: #007AFF;">Safari</strong><br>
2. Tap tombol <strong style="color: #007AFF;">Share</strong> 📤<br>
3. Scroll, pilih "<strong style="color: #007AFF;">Add to Home Screen</strong>"<br>
4. Tap "<strong style="color: #007AFF;">Add</strong>"
</div>
<div style="margin-top: 15px; padding: 10px; background: rgba(0, 122, 255, 0.15); border-radius: 8px; text-align: center;">
<span style="color: #007AFF; font-size: 0.85rem;">✓ No App Store needed</span>
</div>
</div>
""", unsafe_allow_html=True)
        
        # Benefits section
        st.markdown("""
<div style="margin-top: 20px; padding: 15px; background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 10px; text-align: center;">
<div style="color: #D4AF37; font-weight: 600; margin-bottom: 5px;">💡 Keuntungan Install:</div>
<div style="color: #888; font-size: 0.9rem;">Akses cepat • Layar penuh • Hemat data • Seperti app native</div>
</div>
""", unsafe_allow_html=True)
        
        # Coming soon features
        st.markdown("---")
        st.markdown("### 🚀 Coming Soon")
        st.info("""
        **Play Store & App Store (Q1 2026)**
        
        Kami sedang mengembangkan aplikasi native untuk pengalaman yang lebih optimal:
        - 🤖 Android App di Google Play Store
        - 🍎 iOS App di Apple App Store
        - 🔔 Push Notifications
        - 📴 Full Offline Mode
        
        Stay tuned! 🎉
        """)


def render_labbaik_footer():
    """Render LABBAIK branded footer"""
    stats = get_visitor_stats()
    visitor_str = f"{stats['total_visitors']:,}"
    views_str = f"{stats['total_views']:,}"
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 40px 40px 0 40px; border-radius: 20px 20px 0 0; text-align: center; margin-top: 50px;"><div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.8rem; color: #D4AF37;">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div><div style="font-size: 1.3rem; font-weight: 700; color: white; letter-spacing: 0.25em; margin: 12px 0;">LABBAIK</div><div style="color: #C9A86C; font-size: 0.95rem; margin-bottom: 20px;">Panggilan-Nya, Langkahmu</div></div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 0 40px; text-align: center;"><table style="margin: 0 auto; border-collapse: separate; border-spacing: 20px 0;"><tr><td style="background: rgba(212, 175, 55, 0.15); padding: 12px 24px; border-radius: 20px; text-align: center;"><div style="color: #D4AF37; font-size: 0.75rem; opacity: 0.8;">Total Pengunjung</div><div style="color: #D4AF37; font-size: 1.5rem; font-weight: 700;">{visitor_str}</div></td><td style="background: rgba(0, 107, 60, 0.15); padding: 12px 24px; border-radius: 20px; text-align: center;"><div style="color: #C9A86C; font-size: 0.75rem; opacity: 0.8;">Total Page Views</div><div style="color: #C9A86C; font-size: 1.5rem; font-weight: 700;">{views_str}</div></td></tr></table></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 20px 40px; text-align: center;"><div style="color: #888; font-size: 0.85rem;">📧 sopian.hadianto@gmail.com | 📱 +62 815 9658 833 | 🌐 labbaik.ai</div></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 0 40px; text-align: center;"><div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px 25px; margin: 0 auto; max-width: 700px;"><div style="color: #D4AF37; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;">⚠️ Disclaimer & DYOR</div><div style="color: #bbb; font-size: 0.78rem; line-height: 1.7; text-align: left;"><p style="margin-bottom: 8px;">Platform ini menyediakan <strong>simulasi & estimasi</strong> untuk perencanaan umrah. Informasi bukan pengganti riset pribadi.</p><p style="margin-bottom: 8px;">📌 <strong>Travel Agent:</strong> Pastikan berizin resmi Kemenag RI (cek: siskopatuh.kemenag.go.id)</p><p style="margin-bottom: 8px;">📌 <strong>Umrah Mandiri:</strong> Verifikasi regulasi terbaru di nusuk.sa & kemenag.go.id</p><p style="margin: 0; color: #888; font-style: italic;">🤖 Dikembangkan dengan bantuan AI (Claude & Gemini) oleh MS Hadianto.</p></div></div></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); padding: 20px 40px 40px 40px; border-radius: 0 0 20px 20px; text-align: center;"><div style="border-top: 1px solid #333; padding-top: 20px; color: #666; font-size: 0.8rem;">© 2025 LABBAIK. Hak Cipta Dilindungi.<br><span style="color: #D4AF37;">Made with ❤️ &amp; AI by MS Hadianto</span><br><span style="color: #555; font-size: 0.7rem;">v3.4.1 Beta • Powered by Streamlit &amp; Groq AI</span></div></div>""", unsafe_allow_html=True)


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
        st.markdown(f"""<div style="background: linear-gradient(135deg, {role_info['color']}88, {role_info['color']}44); padding: 2rem; border-radius: 15px; text-align: center; border: 3px solid {role_info['color']};"><div style="font-size: 4rem;">{role_info['badge']}</div><h2>{user.get('name', 'User')}</h2><p style="color: {role_info['color']}; font-weight: bold;">{role_info['name']}</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("### 📋 Informasi Akun")
        username = user.get('username', user.get('email', '').split('@')[0])
        created_at = user.get('created_at', '-')
        created_display = created_at[:10] if created_at and created_at != '-' else '-'
        last_login = user.get('last_login', '')
        last_login_display = last_login[:16] if last_login else '-'
        status = '✅ Active' if user.get('status', 'active') == 'active' else '❌ Inactive'
        
        st.markdown(f"""
| Field | Value |
|-------|-------|
| **Username** | @{username} |
| **Email** | {user.get('email', '-')} |
| **Phone** | {user.get('phone', '-')} |
| **Member Since** | {created_display} |
| **Last Login** | {last_login_display} |
| **Status** | {status} |
""")
    
    st.markdown("---")
    if st.button("🚪 Logout", type="secondary"):
        logout_user()
        st.rerun()


# ============================================
# ENGAGEMENT PAGE - REWARDS & QUIZ
# ============================================

def render_engagement_page():
    """Render the engagement hub with rewards, quiz, and referral"""
    # Check daily login for streak
    check_daily_login()
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); border-radius: 15px; margin-bottom: 20px;">
        <div style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1.5rem;">{BRAND['arabic']}</div>
        <h2 style="color: white; margin: 10px 0;">🎮 Rewards & Quiz Center</h2>
        <p style="color: {COLORS['sand']};">Kumpulkan poin, unlock badge, dan naik level!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if engagement modules are available
    if not ENGAGEMENT_AVAILABLE:
        st.warning("⚠️ Modul engagement belum tersedia. Fitur ini akan segera hadir!")
        st.info("""
        **🎮 Fitur yang Akan Hadir:**
        - 🏆 Points & Levels System
        - 🔥 Daily Streak Rewards
        - 🏅 Badges & Achievements
        - 🧠 Interactive Quiz
        - 🎁 Referral Program
        """)
        return
    
    # Show daily reward popup if applicable
    render_daily_reward_popup()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🏆 Rewards & Gamification", "🧠 Quiz & Learning", "🎁 Ajak Teman"])
    
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
        
        # Share buttons
        st.markdown("---")
        st.markdown("### 📤 Share LABBAIK")
        render_share_buttons("app_invite")


def main():
    """Main application entry point"""
    init_session_state()
    init_engagement_state()  # Initialize engagement/gamification system
    
    # Initialize PWA support
    if PWA_AVAILABLE:
        init_pwa()
    
    if "show_login_page" not in st.session_state:
        st.session_state.show_login_page = False
    
    if st.session_state.get("nav_to_login"):
        st.session_state.nav_to_login = False
        st.session_state.show_login_page = True
    
    if st.session_state.show_login_page and not is_logged_in():
        st.markdown(f"""<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {COLORS['black']} 0%, #2D2D2D 100%); border-radius: 10px; margin-bottom: 20px;"><div style="font-family: 'Noto Naskh Arabic', serif; font-size: 1.5rem; color: {COLORS['gold']};">{BRAND['arabic']}</div><div style="font-size: 1rem; font-weight: 700; color: white; letter-spacing: 0.2em;">{BRAND['name']}</div></div>""", unsafe_allow_html=True)
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
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
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
            st.markdown(f"""<div style="text-align: center; margin-bottom: 20px;"><span style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1.5rem;">{BRAND['arabic']}</span><span style="font-weight: 700; letter-spacing: 0.15em; margin-left: 10px;">{BRAND['name']}</span></div>""", unsafe_allow_html=True)
            st.header("✈️ Booking & Reservasi")
            render_booking_features()
    elif "Tools" in page:
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
        else:
            track_page_view("Tools")
            st.markdown(f"""<div style="text-align: center; margin-bottom: 20px;"><span style="font-family: 'Noto Naskh Arabic', serif; color: {COLORS['gold']}; font-size: 1.5rem;">{BRAND['arabic']}</span><span style="font-weight: 700; letter-spacing: 0.15em; margin-left: 10px;">{BRAND['name']}</span></div>""", unsafe_allow_html=True)
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
            st.header("📊 Analytics Dashboard")
            render_analytics_dashboard()
    elif "Business" in page:
        user = get_current_user()
        if not user or user.get("role") not in ["admin", "superadmin"]:
            st.error("🚫 Akses Ditolak")
        else:
            track_page_view("Business Hub")
            st.header("💼 Business Hub")
            render_monetization_page()
    elif "Login" in page:
        track_page_view("Login")
        render_login_page()
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
