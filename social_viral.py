# social_viral.py - LABBAIK Social & Viral Features
# Version: 1.0.0
# Updated: 2025-12-03
# Author: MS Hadianto

"""
================================================================================
🚀 LABBAIK VIRAL & SOCIAL FEATURES
================================================================================

Features to drive viral growth and social engagement:

1. 🔗 SHAREABLE CONTENT
   - Trip Plans as shareable cards
   - Budget simulations as images
   - Achievement cards
   - Referral cards

2. 📱 SOCIAL INTEGRATION
   - WhatsApp sharing
   - Instagram stories
   - Facebook posts
   - Twitter/X threads

3. 🎯 VIRAL MECHANICS
   - "Share to Unlock" features
   - Group challenges
   - Community goals
   - Viral badges

4. 📊 SOCIAL PROOF
   - Live activity feed
   - Success stories
   - Testimonials carousel

================================================================================
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import urllib.parse

# ============================================
# BRAND COLORS
# ============================================
COLORS = {
    "gold": "#D4AF37",
    "gold_light": "#F4E4BA",
    "dark": "#1A1A1A",
    "dark_light": "#2D2D2D",
    "green": "#4CAF50",
    "blue": "#2196F3",
    "purple": "#9C27B0",
    "orange": "#FF9800",
    "red": "#F44336",
    "sand": "#C9A86C",
    "whatsapp": "#25D366",
    "facebook": "#1877F2",
    "twitter": "#1DA1F2",
    "instagram": "#E4405F",
}

# ============================================
# SHARE TEMPLATES
# ============================================
SHARE_TEMPLATES = {
    "app_invite": {
        "whatsapp": "🕋 Assalamualaikum! Aku pakai LABBAIK untuk planning umrah. Gratis & ada AI-nya! Coba yuk: {url} 🤲",
        "twitter": "Planning umrah jadi mudah pakai @LABBAIK_AI! 🕋✨ Simulasi biaya, AI assistant, & panduan lengkap. Gratis! 👇 {url}",
        "facebook": "Alhamdulillah nemu platform bagus untuk planning umrah! 🕋 LABBAIK punya AI assistant, simulasi biaya real-time, dan panduan lengkap. Recommended banget! {url}",
    },
    "budget_result": {
        "whatsapp": "✨ Hasil Simulasi Umrah dari LABBAIK:\n\n📦 Paket: {package}\n💰 Estimasi: Rp {budget}\n📅 Waktu: {duration}\n\nCoba simulasi sendiri: {url}",
        "twitter": "Baru simulasi biaya umrah di @LABBAIK_AI! 🕋\n\n📦 {package}\n💰 Rp {budget}\n\nSimulasi gratis: {url}",
    },
    "plan_created": {
        "whatsapp": "🕋 Alhamdulillah! Rencana umrah-ku sudah jadi!\n\n📅 {departure_date}\n📦 Paket {package}\n💰 Budget: Rp {budget}\n\nBuat rencana kamu juga di LABBAIK: {url}",
    },
    "achievement": {
        "whatsapp": "🏆 Alhamdulillah! Dapat badge '{badge_name}' di LABBAIK!\n\n{badge_desc}\n\nYuk ikutan: {url}",
        "twitter": "Just unlocked '{badge_name}' badge on @LABBAIK_AI! 🏆✨\n\n{url}",
    },
    "referral": {
        "whatsapp": "Assalamualaikum! 🕋\n\nAku mau ajak kamu pakai LABBAIK - platform AI untuk planning umrah.\n\nPakai kode referral: *{code}*\nKamu dapat 50 LP bonus! 🎁\n\nDownload: {url}",
    },
    "group_trip": {
        "whatsapp": "🕋 Open Trip Umrah!\n\n📅 Berangkat: {date}\n📦 Paket: {package}\n💰 Budget: Rp {budget}/orang\n👥 Slot tersisa: {slots}\n\nGabung di LABBAIK: {url}",
    },
}


# ============================================
# SHARE FUNCTIONS
# ============================================

def generate_share_url(platform, template_type, **kwargs):
    """Generate share URL for different platforms"""
    base_url = "https://labbaik.streamlit.app"
    
    # Get template
    template = SHARE_TEMPLATES.get(template_type, {}).get(platform, "")
    if not template:
        template = SHARE_TEMPLATES.get(template_type, {}).get("whatsapp", "Check out LABBAIK! {url}")
    
    # Add URL to kwargs
    kwargs["url"] = base_url
    
    # Format message
    message = template.format(**kwargs)
    
    # Generate platform-specific URL
    encoded_message = urllib.parse.quote(message)
    
    if platform == "whatsapp":
        return f"https://wa.me/?text={encoded_message}"
    elif platform == "twitter":
        return f"https://twitter.com/intent/tweet?text={encoded_message}"
    elif platform == "facebook":
        return f"https://www.facebook.com/sharer/sharer.php?quote={encoded_message}&u={urllib.parse.quote(base_url)}"
    elif platform == "telegram":
        return f"https://t.me/share/url?url={urllib.parse.quote(base_url)}&text={encoded_message}"
    elif platform == "linkedin":
        return f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(base_url)}"
    else:
        return base_url


def render_share_buttons(template_type="app_invite", size="medium", **kwargs):
    """Render social share buttons"""
    
    button_configs = {
        "small": {"padding": "8px 12px", "font_size": "0.8rem", "icon_size": "1rem"},
        "medium": {"padding": "10px 16px", "font_size": "0.9rem", "icon_size": "1.2rem"},
        "large": {"padding": "12px 20px", "font_size": "1rem", "icon_size": "1.4rem"},
    }
    
    config = button_configs.get(size, button_configs["medium"])
    
    platforms = [
        ("whatsapp", "📱 WhatsApp", COLORS["whatsapp"]),
        ("facebook", "📘 Facebook", COLORS["facebook"]),
        ("twitter", "🐦 Twitter", COLORS["twitter"]),
        ("telegram", "📨 Telegram", "#0088cc"),
    ]
    
    cols = st.columns(len(platforms))
    
    for i, (platform, label, color) in enumerate(platforms):
        with cols[i]:
            share_url = generate_share_url(platform, template_type, **kwargs)
            st.markdown(f"""
            <a href="{share_url}" target="_blank" style="text-decoration: none;">
                <div style="background: {color}; color: white; padding: {config['padding']};
                            border-radius: 25px; text-align: center; font-weight: 600;
                            font-size: {config['font_size']}; cursor: pointer;
                            transition: transform 0.2s, box-shadow 0.2s;"
                     onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 4px 15px {color}50';"
                     onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';">
                    {label}
                </div>
            </a>
            """, unsafe_allow_html=True)


def render_share_card(card_type, data):
    """Render shareable card preview"""
    
    if card_type == "budget_result":
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #1E3D2F 100%);
                    border-radius: 20px; padding: 25px; margin: 20px 0;
                    border: 2px solid {COLORS['gold']};">
            <!-- Header -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div>
                    <div style="color: {COLORS['gold']}; font-size: 0.8rem; font-weight: 600;">LABBAIK</div>
                    <div style="color: white; font-size: 1.3rem; font-weight: 700;">Simulasi Biaya Umrah</div>
                </div>
                <div style="font-size: 2rem;">🕋</div>
            </div>
            
            <!-- Content -->
            <div style="background: {COLORS['dark']}80; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Paket</div>
                        <div style="color: white; font-size: 1.1rem; font-weight: 600;">{data.get('package', 'Standard')}</div>
                    </div>
                    <div>
                        <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Estimasi Biaya</div>
                        <div style="color: {COLORS['gold']}; font-size: 1.3rem; font-weight: 700;">
                            Rp {data.get('budget', 0):,.0f}
                        </div>
                    </div>
                    <div>
                        <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Durasi</div>
                        <div style="color: white; font-size: 1.1rem; font-weight: 600;">{data.get('duration', '9')} Hari</div>
                    </div>
                    <div>
                        <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Keberangkatan</div>
                        <div style="color: white; font-size: 1.1rem; font-weight: 600;">{data.get('departure', 'Jakarta')}</div>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; color: {COLORS['sand']}; font-size: 0.85rem;">
                Simulasi gratis di <strong style="color: {COLORS['gold']};">labbaik.ai</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif card_type == "achievement":
        badge = data.get("badge", {})
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2D1F3D 0%, {COLORS['dark']} 100%);
                    border-radius: 20px; padding: 30px; margin: 20px 0; text-align: center;
                    border: 2px solid {COLORS['purple']};">
            <div style="font-size: 4rem; margin-bottom: 15px;">{badge.get('icon', '🏆')}</div>
            <div style="color: {COLORS['gold']}; font-size: 0.9rem; font-weight: 600; margin-bottom: 5px;">
                ACHIEVEMENT UNLOCKED
            </div>
            <div style="color: white; font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">
                {badge.get('name', 'Badge Name')}
            </div>
            <div style="color: {COLORS['sand']}; font-size: 0.9rem; margin-bottom: 20px;">
                {badge.get('description', 'Badge description')}
            </div>
            <div style="background: {COLORS['gold']}; color: {COLORS['dark']}; padding: 8px 20px;
                        border-radius: 20px; display: inline-block; font-weight: 700;">
                +{badge.get('points', 0)} LP
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# VIRAL MECHANICS
# ============================================

def render_share_to_unlock(feature_name, unlock_action="share"):
    """Render share-to-unlock feature gate"""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #1E2A3A 100%);
                border: 2px dashed {COLORS['gold']}50; border-radius: 20px; padding: 30px;
                text-align: center; margin: 20px 0;">
        <div style="font-size: 3rem; margin-bottom: 15px;">🔒</div>
        <div style="color: white; font-size: 1.2rem; font-weight: 700; margin-bottom: 10px;">
            {feature_name}
        </div>
        <div style="color: {COLORS['sand']}; font-size: 0.9rem; margin-bottom: 20px;">
            Share LABBAIK untuk membuka fitur ini!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    render_share_buttons("app_invite")
    
    # Check if shared (simplified - in real app would track actual shares)
    if st.button("✅ Sudah Share!", use_container_width=True):
        st.session_state[f"unlocked_{feature_name}"] = True
        st.success("🎉 Fitur berhasil dibuka!")
        st.rerun()


def render_community_goal():
    """Render community goal progress"""
    
    # Sample community goal
    goal = {
        "title": "10,000 Jamaah Baru",
        "description": "Ajak teman untuk mencapai target komunitas!",
        "current": 7823,
        "target": 10000,
        "reward": "Semua member dapat 500 LP!",
        "deadline": "31 Desember 2025"
    }
    
    progress = (goal["current"] / goal["target"]) * 100
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #2D1F3D 100%);
                border-radius: 20px; padding: 25px; margin-bottom: 20px;
                border: 1px solid {COLORS['purple']}40;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div>
                <div style="color: {COLORS['gold']}; font-size: 0.85rem; font-weight: 600;">🎯 GOAL KOMUNITAS</div>
                <div style="color: white; font-size: 1.2rem; font-weight: 700;">{goal['title']}</div>
            </div>
            <div style="background: {COLORS['purple']}30; color: {COLORS['purple']}; padding: 5px 12px;
                        border-radius: 15px; font-size: 0.8rem;">
                Deadline: {goal['deadline']}
            </div>
        </div>
        
        <div style="color: {COLORS['sand']}; font-size: 0.9rem; margin-bottom: 15px;">
            {goal['description']}
        </div>
        
        <!-- Progress Bar -->
        <div style="position: relative; background: {COLORS['dark']}; border-radius: 10px; 
                    height: 25px; overflow: hidden; margin-bottom: 10px;">
            <div style="background: linear-gradient(90deg, {COLORS['purple']} 0%, {COLORS['gold']} 100%);
                        height: 100%; width: {progress}%; transition: width 0.5s ease;"></div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                        color: white; font-weight: 700; font-size: 0.9rem;">
                {goal['current']:,} / {goal['target']:,}
            </div>
        </div>
        
        <!-- Reward Info -->
        <div style="background: {COLORS['gold']}20; border-radius: 10px; padding: 12px; text-align: center;">
            <span style="color: {COLORS['gold']};">🎁 Reward: </span>
            <span style="color: white; font-weight: 600;">{goal['reward']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# SOCIAL PROOF
# ============================================

def render_live_activity_feed():
    """Render live activity feed showing recent user actions"""
    
    # Sample activities (in real app, would come from database)
    activities = [
        {"user": "Ahmad F.", "city": "Jakarta", "action": "bergabung dengan LABBAIK", "time": "2 menit lalu", "icon": "👋"},
        {"user": "Siti A.", "city": "Surabaya", "action": "membuat rencana umrah", "time": "5 menit lalu", "icon": "📋"},
        {"user": "Muhammad R.", "city": "Bandung", "action": "mendapat badge 'Perencana Cerdas'", "time": "8 menit lalu", "icon": "🏆"},
        {"user": "Fatimah Z.", "city": "Medan", "action": "mengajak 3 teman bergabung", "time": "12 menit lalu", "icon": "🎁"},
        {"user": "Ibrahim H.", "city": "Makassar", "action": "menyelesaikan simulasi biaya", "time": "15 menit lalu", "icon": "💰"},
    ]
    
    st.markdown(f"""
    <div style="background: {COLORS['dark']}; border-radius: 15px; padding: 15px; margin-bottom: 20px;
                max-height: 300px; overflow-y: auto;">
        <div style="color: {COLORS['gold']}; font-weight: 700; margin-bottom: 15px; 
                    display: flex; align-items: center; gap: 8px;">
            <span style="width: 8px; height: 8px; background: {COLORS['green']}; border-radius: 50%;
                        animation: pulse 1s infinite;"></span>
            Live Activity
        </div>
    """, unsafe_allow_html=True)
    
    for activity in activities:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0;
                    border-bottom: 1px solid {COLORS['dark_light']};">
            <span style="font-size: 1.3rem;">{activity['icon']}</span>
            <div style="flex: 1;">
                <div style="color: white; font-size: 0.85rem;">
                    <strong>{activity['user']}</strong> dari {activity['city']} {activity['action']}
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.75rem;">{activity['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    </div>
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    </style>
    """, unsafe_allow_html=True)


def render_success_stories_carousel():
    """Render success stories carousel"""
    
    stories = [
        {
            "name": "Keluarga Bapak Hasan",
            "city": "Jakarta",
            "story": "Alhamdulillah berkat LABBAIK, kami bisa merencanakan umrah keluarga dengan budget pas. Hemat hampir Rp 5 juta!",
            "savings": "Rp 5 Juta",
            "avatar": "👨‍👩‍👧‍👦",
            "rating": 5
        },
        {
            "name": "Ibu Aisyah",
            "city": "Surabaya", 
            "story": "Fitur simulasi biayanya sangat membantu. Bisa compare berbagai paket dengan mudah.",
            "savings": "Rp 3.5 Juta",
            "avatar": "👩",
            "rating": 5
        },
        {
            "name": "Komunitas Pengajian Al-Hikmah",
            "city": "Bandung",
            "story": "Kami pakai fitur Umrah Bareng untuk mengorganisir perjalanan 15 jamaah. Sangat praktis!",
            "savings": "Rp 8 Juta",
            "avatar": "👥",
            "rating": 5
        },
    ]
    
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="color: {COLORS['gold']}; font-size: 1.2rem; font-weight: 700;">
                💬 Cerita Sukses Jamaah
            </div>
            <div style="color: {COLORS['sand']}; font-size: 0.9rem;">
                Lihat bagaimana LABBAIK membantu jamaah lain
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(stories))
    for i, story in enumerate(stories):
        with cols[i]:
            stars = "⭐" * story["rating"]
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['dark_light']} 100%);
                        border-radius: 15px; padding: 20px; height: 100%;
                        border: 1px solid {COLORS['gold']}20;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <span style="font-size: 2rem;">{story['avatar']}</span>
                    <div>
                        <div style="color: white; font-weight: 600;">{story['name']}</div>
                        <div style="color: {COLORS['sand']}; font-size: 0.75rem;">📍 {story['city']}</div>
                    </div>
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.85rem; line-height: 1.5; margin-bottom: 15px;">
                    "{story['story']}"
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="color: {COLORS['gold']}; font-size: 0.8rem;">{stars}</div>
                    <div style="background: {COLORS['green']}20; color: {COLORS['green']}; padding: 5px 10px;
                                border-radius: 10px; font-size: 0.75rem; font-weight: 600;">
                        Hemat {story['savings']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_social_proof_banner():
    """Render social proof statistics banner"""
    
    stats = {
        "users": 15000,
        "simulations": 45000,
        "savings": 2500000000,  # Total savings in Rupiah
        "rating": 4.9
    }
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['gold']}20 0%, {COLORS['dark']} 100%);
                border-radius: 20px; padding: 25px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="color: {COLORS['gold']}; font-size: 2rem; font-weight: 800;">
                    {stats['users']:,}+
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.85rem;">Jamaah Terdaftar</div>
            </div>
            <div style="width: 1px; background: {COLORS['gold']}30;"></div>
            <div>
                <div style="color: {COLORS['green']}; font-size: 2rem; font-weight: 800;">
                    {stats['simulations']:,}+
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.85rem;">Simulasi Dibuat</div>
            </div>
            <div style="width: 1px; background: {COLORS['gold']}30;"></div>
            <div>
                <div style="color: {COLORS['blue']}; font-size: 2rem; font-weight: 800;">
                    Rp {stats['savings']/1000000000:.1f}M+
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.85rem;">Total Penghematan</div>
            </div>
            <div style="width: 1px; background: {COLORS['gold']}30;"></div>
            <div>
                <div style="color: {COLORS['orange']}; font-size: 2rem; font-weight: 800;">
                    ⭐ {stats['rating']}
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.85rem;">Rating Pengguna</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# INVITE FRIENDS MODAL
# ============================================

def render_invite_modal(referral_code):
    """Render invite friends modal/section"""
    
    share_url = f"https://labbaik.streamlit.app?ref={referral_code}"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #1E3D2F 100%);
                border-radius: 25px; padding: 30px; margin: 20px 0;
                border: 2px solid {COLORS['green']}40; text-align: center;">
        
        <!-- Header -->
        <div style="font-size: 3rem; margin-bottom: 15px;">🎁</div>
        <div style="color: white; font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">
            Ajak Teman, Dapat Bonus!
        </div>
        <div style="color: {COLORS['sand']}; margin-bottom: 25px;">
            Kamu dan temanmu masing-masing dapat <strong style="color: {COLORS['gold']};">bonus LP!</strong>
        </div>
        
        <!-- Rewards Breakdown -->
        <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 25px;">
            <div style="background: {COLORS['dark']}; border-radius: 15px; padding: 15px 25px;">
                <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Kamu Dapat</div>
                <div style="color: {COLORS['gold']}; font-size: 1.5rem; font-weight: 700;">+200 LP</div>
            </div>
            <div style="background: {COLORS['dark']}; border-radius: 15px; padding: 15px 25px;">
                <div style="color: {COLORS['sand']}; font-size: 0.8rem;">Teman Dapat</div>
                <div style="color: {COLORS['green']}; font-size: 1.5rem; font-weight: 700;">+75 LP</div>
            </div>
        </div>
        
        <!-- Referral Code -->
        <div style="background: {COLORS['dark']}; border: 2px dashed {COLORS['gold']}50;
                    border-radius: 15px; padding: 15px; margin-bottom: 20px;">
            <div style="color: {COLORS['sand']}; font-size: 0.8rem; margin-bottom: 5px;">Kode Referral</div>
            <div style="color: {COLORS['gold']}; font-size: 2rem; font-weight: 800; letter-spacing: 4px;">
                {referral_code}
            </div>
        </div>
        
        <!-- Link -->
        <div style="background: {COLORS['dark_light']}; border-radius: 10px; padding: 12px;
                    margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 10px;">
            <span style="color: {COLORS['sand']}; font-size: 0.85rem; word-break: break-all;">
                {share_url}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Share buttons
    render_share_buttons("referral", size="large", code=referral_code)


# ============================================
# NOTIFICATION TRIGGERS
# ============================================

def trigger_viral_notification(notification_type, data=None):
    """Trigger viral notification based on user action"""
    
    notifications = {
        "friend_joined": {
            "title": "🎉 Temanmu Bergabung!",
            "message": f"{data.get('friend_name', 'Seseorang')} bergabung pakai kode referralmu. +200 LP!",
            "type": "success"
        },
        "almost_badge": {
            "title": "🏆 Hampir Dapat Badge!",
            "message": f"Kamu tinggal {data.get('remaining', 1)} langkah lagi untuk badge {data.get('badge_name', '')}!",
            "type": "info"
        },
        "streak_reminder": {
            "title": "🔥 Jaga Streak-mu!",
            "message": "Jangan lupa login hari ini untuk menjaga streak-mu!",
            "type": "warning"
        },
        "community_milestone": {
            "title": "🎯 Goal Komunitas Tercapai!",
            "message": "Selamat! Komunitas LABBAIK mencapai 10,000 jamaah. Check reward-mu!",
            "type": "success"
        }
    }
    
    notif = notifications.get(notification_type, {})
    if notif:
        if notif["type"] == "success":
            st.success(f"**{notif['title']}** - {notif['message']}")
        elif notif["type"] == "info":
            st.info(f"**{notif['title']}** - {notif['message']}")
        elif notif["type"] == "warning":
            st.warning(f"**{notif['title']}** - {notif['message']}")


# ============================================
# EXPORT
# ============================================
__all__ = [
    # Share Functions
    "generate_share_url",
    "render_share_buttons",
    "render_share_card",
    
    # Viral Mechanics
    "render_share_to_unlock",
    "render_community_goal",
    
    # Social Proof
    "render_live_activity_feed",
    "render_success_stories_carousel",
    "render_social_proof_banner",
    
    # Invite
    "render_invite_modal",
    
    # Notifications
    "trigger_viral_notification",
    
    # Constants
    "SHARE_TEMPLATES",
]
