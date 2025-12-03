# engagement.py - LABBAIK Engagement & Gamification System
# Version: 1.0.0
# Updated: 2025-12-03
# Author: MS Hadianto

"""
================================================================================
🎮 LABBAIK ENGAGEMENT SYSTEM
================================================================================

Comprehensive gamification and engagement features to drive exponential growth:

1. 🏆 GAMIFICATION
   - Points System (Labbaik Points / LP)
   - Levels & Ranks (Jamaah → Haji Mabrur)
   - Badges & Achievements
   - Daily Streaks
   
2. 🎁 REWARDS
   - Daily Login Rewards
   - Streak Bonuses
   - Referral Rewards
   - Challenge Rewards

3. 📊 LEADERBOARDS
   - Weekly Top Contributors
   - Most Helpful Users
   - Streak Champions

4. 🔥 VIRAL MECHANICS
   - Referral System
   - Social Sharing
   - Group Challenges
   - Community Events

5. 📈 PROGRESS TRACKING
   - Umrah Readiness Score
   - Learning Progress
   - Savings Progress

================================================================================
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import json
import hashlib

# ============================================
# BRAND COLORS
# ============================================
COLORS = {
    "gold": "#D4AF37",
    "gold_light": "#F4E4BA",
    "dark": "#1A1A1A",
    "dark_light": "#2D2D2D",
    "green": "#4CAF50",
    "green_dark": "#2E7D32",
    "blue": "#2196F3",
    "purple": "#9C27B0",
    "orange": "#FF9800",
    "red": "#F44336",
    "sand": "#C9A86C",
    "cream": "#FFF8E7",
}

# ============================================
# POINTS SYSTEM CONFIGURATION
# ============================================
POINTS_CONFIG = {
    # Daily Actions
    "daily_login": 10,
    "daily_streak_bonus": 5,  # Per day streak
    "complete_profile": 50,
    
    # Content Engagement
    "read_article": 5,
    "complete_quiz": 20,
    "share_content": 15,
    "leave_review": 25,
    
    # Planning Actions
    "use_simulator": 10,
    "create_plan": 30,
    "compare_packages": 10,
    "save_favorite": 5,
    
    # Social Actions
    "invite_friend": 100,
    "friend_joins": 200,
    "post_experience": 50,
    "helpful_answer": 30,
    "receive_like": 5,
    
    # Achievements
    "first_simulation": 50,
    "first_plan": 100,
    "first_referral": 150,
    "complete_learning": 200,
}

# ============================================
# LEVELS & RANKS
# ============================================
LEVELS = [
    {"level": 1, "name": "Jamaah Pemula", "min_points": 0, "icon": "🌱", "color": "#8BC34A"},
    {"level": 2, "name": "Jamaah Aktif", "min_points": 100, "icon": "🌿", "color": "#4CAF50"},
    {"level": 3, "name": "Jamaah Setia", "min_points": 300, "icon": "🌳", "color": "#2E7D32"},
    {"level": 4, "name": "Calon Mutawwif", "min_points": 600, "icon": "⭐", "color": "#FFC107"},
    {"level": 5, "name": "Mutawwif", "min_points": 1000, "icon": "🌟", "color": "#FF9800"},
    {"level": 6, "name": "Mutawwif Senior", "min_points": 1500, "icon": "💫", "color": "#FF5722"},
    {"level": 7, "name": "Jamaah Berpengalaman", "min_points": 2500, "icon": "🏅", "color": "#9C27B0"},
    {"level": 8, "name": "Pakar Umrah", "min_points": 4000, "icon": "🎖️", "color": "#673AB7"},
    {"level": 9, "name": "Mentor Jamaah", "min_points": 6000, "icon": "👑", "color": "#3F51B5"},
    {"level": 10, "name": "Haji Mabrur", "min_points": 10000, "icon": "🕋", "color": "#D4AF37"},
]

# ============================================
# BADGES & ACHIEVEMENTS
# ============================================
BADGES = {
    # Starter Badges
    "first_steps": {
        "name": "Langkah Pertama",
        "description": "Mulai perjalanan di LABBAIK",
        "icon": "👣",
        "category": "starter",
        "points": 50,
        "secret": False
    },
    "profile_complete": {
        "name": "Profil Lengkap",
        "description": "Melengkapi semua data profil",
        "icon": "📝",
        "category": "starter",
        "points": 100,
        "secret": False
    },
    
    # Planning Badges
    "first_simulation": {
        "name": "Perencana Cerdas",
        "description": "Melakukan simulasi biaya pertama",
        "icon": "💰",
        "category": "planning",
        "points": 75,
        "secret": False
    },
    "budget_master": {
        "name": "Ahli Anggaran",
        "description": "Melakukan 10 simulasi biaya",
        "icon": "📊",
        "category": "planning",
        "points": 150,
        "secret": False
    },
    "plan_creator": {
        "name": "Arsitek Perjalanan",
        "description": "Membuat rencana umrah lengkap",
        "icon": "📋",
        "category": "planning",
        "points": 100,
        "secret": False
    },
    
    # Streak Badges
    "streak_7": {
        "name": "Istiqomah Seminggu",
        "description": "Login 7 hari berturut-turut",
        "icon": "🔥",
        "category": "streak",
        "points": 100,
        "secret": False
    },
    "streak_30": {
        "name": "Istiqomah Sebulan",
        "description": "Login 30 hari berturut-turut",
        "icon": "💎",
        "category": "streak",
        "points": 500,
        "secret": False
    },
    "streak_100": {
        "name": "Istiqomah 100 Hari",
        "description": "Login 100 hari berturut-turut",
        "icon": "🏆",
        "category": "streak",
        "points": 2000,
        "secret": False
    },
    
    # Social Badges
    "first_share": {
        "name": "Penyebar Kebaikan",
        "description": "Membagikan konten pertama kali",
        "icon": "📤",
        "category": "social",
        "points": 50,
        "secret": False
    },
    "influencer": {
        "name": "Influencer Umrah",
        "description": "Mengajak 10 teman bergabung",
        "icon": "🌟",
        "category": "social",
        "points": 1000,
        "secret": False
    },
    "community_hero": {
        "name": "Pahlawan Komunitas",
        "description": "Membantu 50 jamaah dengan tips",
        "icon": "🦸",
        "category": "social",
        "points": 750,
        "secret": False
    },
    
    # Learning Badges
    "doa_master": {
        "name": "Hafidz Doa",
        "description": "Mempelajari semua doa umrah",
        "icon": "📖",
        "category": "learning",
        "points": 200,
        "secret": False
    },
    "manasik_complete": {
        "name": "Lulus Manasik",
        "description": "Menyelesaikan semua materi manasik",
        "icon": "🎓",
        "category": "learning",
        "points": 300,
        "secret": False
    },
    
    # Secret Badges
    "early_bird": {
        "name": "Early Adopter",
        "description": "Bergabung di 1000 user pertama",
        "icon": "🐦",
        "category": "secret",
        "points": 500,
        "secret": True
    },
    "night_owl": {
        "name": "Qiyamul Lail",
        "description": "Menggunakan LABBAIK setelah jam 2 malam",
        "icon": "🌙",
        "category": "secret",
        "points": 100,
        "secret": True
    },
    "perfect_score": {
        "name": "Nilai Sempurna",
        "description": "Mendapat skor 100% di quiz",
        "icon": "💯",
        "category": "secret",
        "points": 200,
        "secret": True
    },
}

# ============================================
# DAILY REWARDS
# ============================================
DAILY_REWARDS = [
    {"day": 1, "reward": "10 LP", "points": 10, "icon": "🎁"},
    {"day": 2, "reward": "15 LP", "points": 15, "icon": "🎁"},
    {"day": 3, "reward": "20 LP", "points": 20, "icon": "🎁"},
    {"day": 4, "reward": "25 LP", "points": 25, "icon": "🎁"},
    {"day": 5, "reward": "30 LP", "points": 30, "icon": "🎁"},
    {"day": 6, "reward": "40 LP", "points": 40, "icon": "🎁"},
    {"day": 7, "reward": "100 LP + Badge", "points": 100, "icon": "🏆", "badge": "streak_7"},
]

# ============================================
# CHALLENGES
# ============================================
DAILY_CHALLENGES = [
    {
        "id": "simulate_budget",
        "title": "Simulasi Budget",
        "description": "Lakukan 1x simulasi biaya umrah",
        "points": 20,
        "icon": "💰",
        "action": "simulation"
    },
    {
        "id": "read_tips",
        "title": "Pembaca Aktif",
        "description": "Baca 3 tips persiapan umrah",
        "points": 15,
        "icon": "📚",
        "action": "read"
    },
    {
        "id": "share_app",
        "title": "Berbagi Kebaikan",
        "description": "Share LABBAIK ke 1 platform sosial",
        "points": 25,
        "icon": "📤",
        "action": "share"
    },
    {
        "id": "complete_quiz",
        "title": "Uji Pengetahuan",
        "description": "Selesaikan 1 quiz manasik",
        "points": 30,
        "icon": "❓",
        "action": "quiz"
    },
    {
        "id": "help_others",
        "title": "Bantu Sesama",
        "description": "Jawab 1 pertanyaan di forum",
        "points": 35,
        "icon": "🤝",
        "action": "answer"
    },
]

WEEKLY_CHALLENGES = [
    {
        "id": "weekly_streak",
        "title": "Istiqomah Mingguan",
        "description": "Login 7 hari berturut-turut",
        "points": 150,
        "icon": "🔥",
        "progress_max": 7
    },
    {
        "id": "social_butterfly",
        "title": "Kupu-Kupu Sosial",
        "description": "Ajak 3 teman bergabung LABBAIK",
        "points": 500,
        "icon": "🦋",
        "progress_max": 3
    },
    {
        "id": "planning_pro",
        "title": "Pro Planner",
        "description": "Buat 5 simulasi berbeda",
        "points": 100,
        "icon": "📊",
        "progress_max": 5
    },
    {
        "id": "community_star",
        "title": "Bintang Komunitas",
        "description": "Dapat 10 likes di forum",
        "points": 200,
        "icon": "⭐",
        "progress_max": 10
    },
]

# ============================================
# REFERRAL SYSTEM
# ============================================
REFERRAL_REWARDS = {
    "inviter": {
        "signup": 100,  # Friend signs up
        "first_simulation": 50,  # Friend does first simulation
        "first_plan": 100,  # Friend creates first plan
    },
    "invitee": {
        "signup": 50,  # Bonus for using referral
        "welcome": 25,  # Welcome bonus
    },
    "milestones": {
        5: {"reward": 500, "badge": "recruiter", "title": "Rekruter Jamaah"},
        10: {"reward": 1000, "badge": "influencer", "title": "Influencer Umrah"},
        25: {"reward": 2500, "badge": "ambassador", "title": "Duta LABBAIK"},
        50: {"reward": 5000, "badge": "legend", "title": "Legenda LABBAIK"},
    }
}


# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def init_engagement_state():
    """Initialize engagement system in session state"""
    if "engagement" not in st.session_state:
        st.session_state.engagement = {
            "points": 0,
            "level": 1,
            "badges": ["first_steps"],
            "streak": 0,
            "last_login": None,
            "daily_claimed": False,
            "daily_challenges": [],
            "weekly_challenges": [],
            "referral_code": None,
            "referrals": [],
            "achievements": [],
            "stats": {
                "simulations": 0,
                "plans_created": 0,
                "shares": 0,
                "forum_posts": 0,
                "quiz_completed": 0,
                "articles_read": 0,
            }
        }


def get_user_level(points):
    """Get user level based on points"""
    current_level = LEVELS[0]
    for level in LEVELS:
        if points >= level["min_points"]:
            current_level = level
        else:
            break
    return current_level


def get_next_level(current_level):
    """Get next level info"""
    for i, level in enumerate(LEVELS):
        if level["level"] == current_level["level"]:
            if i < len(LEVELS) - 1:
                return LEVELS[i + 1]
    return None


def calculate_level_progress(points, current_level):
    """Calculate progress to next level"""
    next_level = get_next_level(current_level)
    if next_level is None:
        return 100
    
    current_min = current_level["min_points"]
    next_min = next_level["min_points"]
    
    progress = (points - current_min) / (next_min - current_min) * 100
    return min(100, max(0, progress))


def generate_referral_code(user_id):
    """Generate unique referral code"""
    hash_input = f"{user_id}-labbaik-{datetime.now().timestamp()}"
    code = hashlib.md5(hash_input.encode()).hexdigest()[:8].upper()
    return f"LBK{code}"


def award_points(amount, reason=""):
    """Award points to user"""
    init_engagement_state()
    st.session_state.engagement["points"] += amount
    
    # Check for level up
    old_level = st.session_state.engagement["level"]
    new_level = get_user_level(st.session_state.engagement["points"])
    
    if new_level["level"] > old_level:
        st.session_state.engagement["level"] = new_level["level"]
        return {"points": amount, "level_up": True, "new_level": new_level}
    
    return {"points": amount, "level_up": False}


def award_badge(badge_id):
    """Award badge to user"""
    init_engagement_state()
    if badge_id not in st.session_state.engagement["badges"]:
        st.session_state.engagement["badges"].append(badge_id)
        badge = BADGES.get(badge_id, {})
        if badge:
            award_points(badge.get("points", 0), f"Badge: {badge.get('name', '')}")
        return True
    return False


def check_daily_login():
    """Check and process daily login"""
    init_engagement_state()
    today = datetime.now().date()
    last_login = st.session_state.engagement.get("last_login")
    
    if last_login:
        last_login = datetime.strptime(last_login, "%Y-%m-%d").date()
        days_diff = (today - last_login).days
        
        if days_diff == 0:
            # Already logged in today
            return {"status": "already_claimed", "streak": st.session_state.engagement["streak"]}
        elif days_diff == 1:
            # Consecutive day - increase streak
            st.session_state.engagement["streak"] += 1
        else:
            # Streak broken
            st.session_state.engagement["streak"] = 1
    else:
        # First login
        st.session_state.engagement["streak"] = 1
    
    st.session_state.engagement["last_login"] = today.strftime("%Y-%m-%d")
    st.session_state.engagement["daily_claimed"] = False
    
    return {
        "status": "new_day",
        "streak": st.session_state.engagement["streak"]
    }


def claim_daily_reward():
    """Claim daily reward based on streak"""
    init_engagement_state()
    
    if st.session_state.engagement.get("daily_claimed", False):
        return {"success": False, "message": "Reward sudah diklaim hari ini"}
    
    streak = st.session_state.engagement["streak"]
    day_index = min(streak - 1, len(DAILY_REWARDS) - 1)
    reward = DAILY_REWARDS[day_index]
    
    result = award_points(reward["points"], "Daily Login Reward")
    st.session_state.engagement["daily_claimed"] = True
    
    # Check for streak badges
    if streak == 7:
        award_badge("streak_7")
    elif streak == 30:
        award_badge("streak_30")
    elif streak == 100:
        award_badge("streak_100")
    
    return {
        "success": True,
        "reward": reward,
        "level_up": result.get("level_up", False),
        "new_level": result.get("new_level")
    }


# ============================================
# UI COMPONENTS
# ============================================

def render_points_display():
    """Render compact points and level display"""
    init_engagement_state()
    
    points = st.session_state.engagement["points"]
    level = get_user_level(points)
    progress = calculate_level_progress(points, level)
    next_level = get_next_level(level)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['dark_light']} 100%); 
                padding: 15px 20px; border-radius: 15px; margin-bottom: 20px;
                border: 1px solid {COLORS['gold']}30;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.8rem;">{level['icon']}</span>
                <div>
                    <div style="color: {level['color']}; font-weight: 700; font-size: 1rem;">{level['name']}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Level {level['level']}</div>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="color: {COLORS['gold']}; font-weight: 700; font-size: 1.5rem;">{points:,}</div>
                <div style="color: {COLORS['sand']}; font-size: 0.75rem;">Labbaik Points</div>
            </div>
        </div>
        <div style="background: {COLORS['dark']}; border-radius: 10px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, {COLORS['gold']} 0%, {level['color']} 100%); 
                        height: 100%; width: {progress}%; transition: width 0.5s ease;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
            <span style="color: {COLORS['sand']}; font-size: 0.7rem;">{level['min_points']} LP</span>
            <span style="color: {COLORS['sand']}; font-size: 0.7rem;">
                {f"{next_level['min_points']} LP" if next_level else "MAX"}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_streak_display():
    """Render streak fire display"""
    init_engagement_state()
    streak = st.session_state.engagement["streak"]
    
    # Generate flame intensity based on streak
    flame_size = min(2.5, 1.5 + (streak * 0.1))
    flame_color = COLORS['orange'] if streak < 7 else (COLORS['red'] if streak < 30 else COLORS['gold'])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD700 100%);
                padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);">
        <div style="font-size: {flame_size}rem; margin-bottom: 5px; 
                    text-shadow: 0 0 20px {flame_color}, 0 0 40px {flame_color};">🔥</div>
        <div style="color: white; font-size: 2rem; font-weight: 800;">{streak}</div>
        <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; font-weight: 600;">Hari Berturut-turut</div>
        <div style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin-top: 5px;">
            {f"+{streak * 5} LP bonus streak!" if streak > 1 else "Mulai streak-mu!"}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_daily_reward_popup():
    """Render daily reward claim UI"""
    init_engagement_state()
    
    login_status = check_daily_login()
    streak = login_status["streak"]
    
    if login_status["status"] == "already_claimed":
        return
    
    if st.session_state.engagement.get("daily_claimed", False):
        return
    
    # Show reward popup
    day_index = min(streak - 1, len(DAILY_REWARDS) - 1)
    today_reward = DAILY_REWARDS[day_index]
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #2D1F3D 100%);
                border: 2px solid {COLORS['gold']}; border-radius: 20px; padding: 25px;
                text-align: center; margin-bottom: 20px;
                animation: pulse 2s infinite;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🎁</div>
        <div style="color: {COLORS['gold']}; font-size: 1.3rem; font-weight: 700; margin-bottom: 5px;">
            Hadiah Harian Hari ke-{streak}!
        </div>
        <div style="color: white; font-size: 1.8rem; font-weight: 800; margin: 15px 0;">
            {today_reward['icon']} {today_reward['reward']}
        </div>
        <div style="color: {COLORS['sand']}; font-size: 0.85rem; margin-bottom: 15px;">
            Klaim sekarang untuk melanjutkan streak-mu!
        </div>
    </div>
    <style>
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.4); }}
        50% {{ transform: scale(1.02); box-shadow: 0 0 20px 10px rgba(212, 175, 55, 0.2); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("🎁 Klaim Hadiah!", use_container_width=True, type="primary"):
        result = claim_daily_reward()
        if result["success"]:
            st.balloons()
            st.success(f"✅ Berhasil klaim {result['reward']['reward']}!")
            if result.get("level_up"):
                st.success(f"🎉 LEVEL UP! Kamu sekarang {result['new_level']['name']}!")
            st.rerun()


def render_badges_showcase():
    """Render user badges"""
    init_engagement_state()
    user_badges = st.session_state.engagement["badges"]
    
    st.markdown(f"""
    <div style="background: {COLORS['dark']}; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
        <div style="color: {COLORS['gold']}; font-size: 1.1rem; font-weight: 700; margin-bottom: 15px;">
            🏆 Koleksi Badge ({len(user_badges)}/{len([b for b in BADGES.values() if not b['secret']])})
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
    """, unsafe_allow_html=True)
    
    cols = st.columns(6)
    col_idx = 0
    
    for badge_id, badge in BADGES.items():
        if badge["secret"] and badge_id not in user_badges:
            continue
        
        owned = badge_id in user_badges
        with cols[col_idx % 6]:
            opacity = "1" if owned else "0.3"
            st.markdown(f"""
            <div style="background: {'linear-gradient(135deg, #2D2D2D 0%, #3D3D3D 100%)' if owned else '#1A1A1A'};
                        border-radius: 12px; padding: 15px; text-align: center;
                        opacity: {opacity}; border: 1px solid {COLORS['gold'] if owned else '#333'};
                        cursor: pointer;" title="{badge['description']}">
                <div style="font-size: 1.8rem; margin-bottom: 5px;">{badge['icon']}</div>
                <div style="color: {COLORS['gold'] if owned else '#666'}; font-size: 0.7rem; font-weight: 600;">
                    {badge['name']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        col_idx += 1
    
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_daily_challenges():
    """Render daily challenges"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #1E3A2F 100%);
                border-radius: 15px; padding: 20px; margin-bottom: 20px;
                border: 1px solid {COLORS['green']}40;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="color: {COLORS['green']}; font-size: 1.1rem; font-weight: 700;">
                📋 Tantangan Harian
            </div>
            <div style="background: {COLORS['green']}20; color: {COLORS['green']}; padding: 5px 12px; 
                        border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                Reset dalam 12:34:56
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    for challenge in DAILY_CHALLENGES[:3]:  # Show 3 daily challenges
        completed = random.choice([True, False])  # Placeholder
        st.markdown(f"""
        <div style="background: {'#2E7D3220' if completed else '#FFFFFF10'}; 
                    border-radius: 10px; padding: 12px 15px; margin-bottom: 8px;
                    display: flex; justify-content: space-between; align-items: center;
                    border-left: 3px solid {COLORS['green'] if completed else COLORS['gold']};">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.3rem;">{challenge['icon']}</span>
                <div>
                    <div style="color: white; font-weight: 600; font-size: 0.9rem;">
                        {challenge['title']} {'✅' if completed else ''}
                    </div>
                    <div style="color: {COLORS['sand']}; font-size: 0.75rem;">
                        {challenge['description']}
                    </div>
                </div>
            </div>
            <div style="background: {COLORS['gold']}; color: {COLORS['dark']}; padding: 5px 12px;
                        border-radius: 15px; font-weight: 700; font-size: 0.8rem;">
                +{challenge['points']} LP
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_referral_section():
    """Render referral system UI"""
    init_engagement_state()
    
    # Generate referral code if not exists
    if not st.session_state.engagement.get("referral_code"):
        st.session_state.engagement["referral_code"] = generate_referral_code("user123")
    
    ref_code = st.session_state.engagement["referral_code"]
    referrals = len(st.session_state.engagement.get("referrals", []))
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
                border-radius: 20px; padding: 25px; margin-bottom: 20px;
                border: 1px solid {COLORS['blue']}50;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🎁</div>
            <div style="color: white; font-size: 1.3rem; font-weight: 700; margin-bottom: 5px;">
                Ajak Teman, Dapat Bonus!
            </div>
            <div style="color: {COLORS['sand']}; font-size: 0.9rem;">
                Dapatkan <strong style="color: {COLORS['gold']};">200 LP</strong> untuk setiap teman yang bergabung
            </div>
        </div>
        
        <div style="background: {COLORS['dark']}; border-radius: 15px; padding: 15px; text-align: center;
                    margin-bottom: 20px; border: 2px dashed {COLORS['gold']}50;">
            <div style="color: {COLORS['sand']}; font-size: 0.8rem; margin-bottom: 5px;">Kode Referral Kamu</div>
            <div style="color: {COLORS['gold']}; font-size: 1.8rem; font-weight: 800; letter-spacing: 3px;">
                {ref_code}
            </div>
        </div>
        
        <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 20px;">
            <div style="background: #25D366; color: white; padding: 10px 20px; border-radius: 25px;
                        font-weight: 600; cursor: pointer; font-size: 0.9rem;">
                📱 WhatsApp
            </div>
            <div style="background: #1877F2; color: white; padding: 10px 20px; border-radius: 25px;
                        font-weight: 600; cursor: pointer; font-size: 0.9rem;">
                📘 Facebook
            </div>
            <div style="background: #1DA1F2; color: white; padding: 10px 20px; border-radius: 25px;
                        font-weight: 600; cursor: pointer; font-size: 0.9rem;">
                🐦 Twitter
            </div>
        </div>
        
        <div style="background: {COLORS['dark']}50; border-radius: 10px; padding: 15px;">
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <div style="color: {COLORS['gold']}; font-size: 1.5rem; font-weight: 700;">{referrals}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.75rem;">Teman Diajak</div>
                </div>
                <div style="width: 1px; background: {COLORS['gold']}30;"></div>
                <div>
                    <div style="color: {COLORS['green']}; font-size: 1.5rem; font-weight: 700;">{referrals * 200}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.75rem;">LP Didapat</div>
                </div>
                <div style="width: 1px; background: {COLORS['gold']}30;"></div>
                <div>
                    <div style="color: {COLORS['blue']}; font-size: 1.5rem; font-weight: 700;">{5 - referrals if referrals < 5 else 0}</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.75rem;">Lagi untuk Badge</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_leaderboard():
    """Render weekly leaderboard"""
    # Sample leaderboard data
    leaders = [
        {"rank": 1, "name": "Ahmad Fauzi", "city": "Jakarta", "points": 15420, "avatar": "👳"},
        {"rank": 2, "name": "Siti Aisyah", "city": "Surabaya", "points": 12850, "avatar": "👩"},
        {"rank": 3, "name": "Muhammad Rizki", "city": "Bandung", "points": 11200, "avatar": "👨"},
        {"rank": 4, "name": "Fatimah Zahra", "city": "Medan", "points": 9800, "avatar": "👩"},
        {"rank": 5, "name": "Ibrahim Hassan", "city": "Makassar", "points": 8500, "avatar": "👨"},
    ]
    
    medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32", COLORS['dark_light'], COLORS['dark_light']]
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #2D1F3D 100%);
                border-radius: 20px; padding: 25px; margin-bottom: 20px;
                border: 1px solid {COLORS['purple']}40;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 1.3rem; color: {COLORS['gold']}; font-weight: 700;">
                🏆 Leaderboard Mingguan
            </div>
            <div style="color: {COLORS['sand']}; font-size: 0.85rem;">
                Top kontributor minggu ini
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    for i, leader in enumerate(leaders):
        is_top3 = i < 3
        rank_display = ["🥇", "🥈", "🥉"][i] if is_top3 else f"#{leader['rank']}"
        
        st.markdown(f"""
        <div style="background: {medal_colors[i]}10; border-radius: 12px; padding: 12px 15px;
                    margin-bottom: 8px; display: flex; align-items: center; gap: 15px;
                    border: 1px solid {medal_colors[i]}30;
                    {'transform: scale(1.02);' if is_top3 else ''}">
            <div style="font-size: {'1.5rem' if is_top3 else '1rem'}; width: 35px; text-align: center;">
                {rank_display}
            </div>
            <div style="font-size: 1.5rem;">{leader['avatar']}</div>
            <div style="flex: 1;">
                <div style="color: white; font-weight: 600;">{leader['name']}</div>
                <div style="color: {COLORS['sand']}; font-size: 0.75rem;">📍 {leader['city']}</div>
            </div>
            <div style="text-align: right;">
                <div style="color: {COLORS['gold']}; font-weight: 700;">{leader['points']:,}</div>
                <div style="color: {COLORS['sand']}; font-size: 0.7rem;">LP</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-top: 15px;">
            <div style="color: #888; font-size: 0.8rem; padding: 10px; background: #FFFFFF10; 
                        border-radius: 10px; display: inline-block;">
                📊 Kamu peringkat <strong style="color: #D4AF37;">#42</strong> minggu ini
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_umrah_readiness_score():
    """Render Umrah readiness progress tracker"""
    # Sample readiness data
    readiness = {
        "knowledge": 75,  # Manasik knowledge
        "financial": 60,  # Savings progress
        "physical": 85,  # Physical preparation
        "spiritual": 70,  # Spiritual preparation
        "documents": 40,  # Document preparation
    }
    
    overall = sum(readiness.values()) // len(readiness)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #1E3D2F 100%);
                border-radius: 20px; padding: 25px; margin-bottom: 20px;
                border: 1px solid {COLORS['green']}40;">
        <div style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 1.1rem; color: {COLORS['gold']}; font-weight: 700; margin-bottom: 10px;">
                🕋 Skor Kesiapan Umrah
            </div>
            
            <!-- Circular Progress -->
            <div style="position: relative; width: 150px; height: 150px; margin: 0 auto;">
                <svg viewBox="0 0 36 36" style="transform: rotate(-90deg);">
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none" stroke="{COLORS['dark']}" stroke-width="3"/>
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none" stroke="{COLORS['green']}" stroke-width="3"
                          stroke-dasharray="{overall}, 100"/>
                </svg>
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                            text-align: center;">
                    <div style="color: {COLORS['green']}; font-size: 2rem; font-weight: 800;">{overall}%</div>
                    <div style="color: {COLORS['sand']}; font-size: 0.7rem;">SIAP</div>
                </div>
            </div>
        </div>
        
        <!-- Progress Bars -->
        <div style="display: flex; flex-direction: column; gap: 12px;">
    """, unsafe_allow_html=True)
    
    categories = [
        ("📚 Pengetahuan Manasik", readiness["knowledge"], COLORS['blue']),
        ("💰 Keuangan & Tabungan", readiness["financial"], COLORS['gold']),
        ("🏃 Persiapan Fisik", readiness["physical"], COLORS['green']),
        ("🤲 Persiapan Spiritual", readiness["spiritual"], COLORS['purple']),
        ("📄 Dokumen & Visa", readiness["documents"], COLORS['orange']),
    ]
    
    for name, value, color in categories:
        st.markdown(f"""
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: white; font-size: 0.85rem;">{name}</span>
                <span style="color: {color}; font-weight: 600;">{value}%</span>
            </div>
            <div style="background: {COLORS['dark']}; border-radius: 5px; height: 8px; overflow: hidden;">
                <div style="background: {color}; height: 100%; width: {value}%; 
                            transition: width 0.5s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <div style="background: #FFFFFF10; padding: 10px 20px; border-radius: 10px; 
                        display: inline-block; color: #AAA; font-size: 0.85rem;">
                💡 Tingkatkan skor dengan menyelesaikan tantangan!
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_engagement_hub():
    """Main engagement hub - combines all engagement features"""
    init_engagement_state()
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: {COLORS['gold']}; font-size: 2rem; margin-bottom: 5px;">
            🎮 Pusat Reward & Engagement
        </h1>
        <p style="color: {COLORS['sand']};">
            Kumpulkan poin, unlock badge, dan naik level!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Daily reward popup
    render_daily_reward_popup()
    
    # Main stats row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_points_display()
    
    with col2:
        render_streak_display()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Tantangan", 
        "🏆 Badge", 
        "📊 Leaderboard",
        "🎁 Referral",
        "🕋 Kesiapan"
    ])
    
    with tab1:
        render_daily_challenges()
        st.markdown("### 📅 Tantangan Mingguan")
        for challenge in WEEKLY_CHALLENGES[:2]:
            progress = random.randint(0, challenge["progress_max"])
            st.markdown(f"""
            <div style="background: {COLORS['dark']}; border-radius: 12px; padding: 15px; margin-bottom: 10px;
                        border: 1px solid {COLORS['gold']}30;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.5rem;">{challenge['icon']}</span>
                        <div>
                            <div style="color: white; font-weight: 600;">{challenge['title']}</div>
                            <div style="color: {COLORS['sand']}; font-size: 0.8rem;">{challenge['description']}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {COLORS['gold']}; font-weight: 700;">+{challenge['points']} LP</div>
                        <div style="color: {COLORS['sand']}; font-size: 0.75rem;">{progress}/{challenge['progress_max']}</div>
                    </div>
                </div>
                <div style="background: {COLORS['dark_light']}; border-radius: 5px; height: 6px; margin-top: 10px; overflow: hidden;">
                    <div style="background: {COLORS['gold']}; height: 100%; width: {(progress/challenge['progress_max'])*100}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        render_badges_showcase()
    
    with tab3:
        render_leaderboard()
    
    with tab4:
        render_referral_section()
    
    with tab5:
        render_umrah_readiness_score()


# ============================================
# MINI WIDGETS FOR SIDEBAR/OTHER PAGES
# ============================================

def render_sidebar_engagement_widget():
    """Compact engagement widget for sidebar"""
    init_engagement_state()
    
    points = st.session_state.engagement["points"]
    level = get_user_level(points)
    streak = st.session_state.engagement["streak"]
    
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['dark_light']} 100%);
                border-radius: 12px; padding: 15px; margin-bottom: 15px;
                border: 1px solid {COLORS['gold']}30;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 1.2rem;">{level['icon']}</span>
                <span style="color: {COLORS['gold']}; font-weight: 700; margin-left: 8px;">{points:,} LP</span>
            </div>
            <div style="display: flex; align-items: center; gap: 5px;">
                <span style="font-size: 1rem;">🔥</span>
                <span style="color: {COLORS['orange']}; font-weight: 700;">{streak}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_points_earned_toast(points, reason=""):
    """Show toast notification for points earned"""
    st.toast(f"🎉 +{points} LP! {reason}", icon="⭐")


def render_level_up_celebration(new_level):
    """Show level up celebration"""
    st.balloons()
    st.markdown(f"""
    <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: linear-gradient(135deg, {COLORS['dark']} 0%, #2D1F3D 100%);
                border: 3px solid {COLORS['gold']}; border-radius: 25px; padding: 40px;
                text-align: center; z-index: 9999; box-shadow: 0 0 50px {COLORS['gold']}50;">
        <div style="font-size: 4rem; margin-bottom: 15px;">{new_level['icon']}</div>
        <div style="color: {COLORS['gold']}; font-size: 1.5rem; font-weight: 800; margin-bottom: 10px;">
            🎉 LEVEL UP!
        </div>
        <div style="color: white; font-size: 1.2rem; margin-bottom: 5px;">
            Selamat! Kamu sekarang
        </div>
        <div style="color: {new_level['color']}; font-size: 1.8rem; font-weight: 700;">
            {new_level['name']}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# EXPORT ALL FUNCTIONS
# ============================================
__all__ = [
    # State
    "init_engagement_state",
    
    # Core Functions
    "get_user_level",
    "award_points",
    "award_badge",
    "check_daily_login",
    "claim_daily_reward",
    "generate_referral_code",
    
    # UI Components
    "render_engagement_hub",
    "render_points_display",
    "render_streak_display",
    "render_daily_reward_popup",
    "render_badges_showcase",
    "render_daily_challenges",
    "render_referral_section",
    "render_leaderboard",
    "render_umrah_readiness_score",
    
    # Widgets
    "render_sidebar_engagement_widget",
    "render_points_earned_toast",
    "render_level_up_celebration",
    
    # Constants
    "POINTS_CONFIG",
    "LEVELS",
    "BADGES",
    "DAILY_REWARDS",
    "DAILY_CHALLENGES",
    "WEEKLY_CHALLENGES",
    "REFERRAL_REWARDS",
]
