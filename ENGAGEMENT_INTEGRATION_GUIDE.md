# ENGAGEMENT_INTEGRATION_GUIDE.md
# Panduan Integrasi Sistem Engagement LABBAIK

## 🎮 Overview

Sistem engagement LABBAIK terdiri dari 3 modul utama:

1. **engagement.py** - Gamification & Rewards System
2. **social_viral.py** - Viral & Social Sharing Features  
3. **quiz_learning.py** - Interactive Quiz & Learning

---

## 📦 File yang Perlu Ditambahkan

```
umrah-planner/
├── engagement.py       # NEW - Gamification system
├── social_viral.py     # NEW - Viral/social features
├── quiz_learning.py    # NEW - Quiz system
├── app.py              # UPDATE - Add engagement menu
└── requirements.txt    # No changes needed
```

---

## 🔧 Cara Integrasi ke app.py

### Step 1: Import Modules

Tambahkan di bagian import (sekitar line 30-60):

```python
# Import engagement modules
from engagement import (
    init_engagement_state,
    render_engagement_hub,
    render_sidebar_engagement_widget,
    award_points,
    check_daily_login,
    POINTS_CONFIG
)
from social_viral import (
    render_share_buttons,
    render_social_proof_banner,
    render_live_activity_feed,
    render_invite_modal
)
from quiz_learning import (
    render_quiz_page,
    init_quiz_state
)
```

### Step 2: Tambah Menu di Sidebar

Di fungsi `render_sidebar()`, tambahkan menu baru:

```python
# Di bagian menu/navigation (sekitar line 570-580)
menu_items = {
    "🏠 Home": "home",
    "💰 Simulasi Biaya": "simulation",
    "📋 Buat Rencana": "create_plan",
    "💵 Cari Paket": "budget_finder",
    "🤝 Umrah Bareng": "umrah_bareng",
    "📝 Umrah Mandiri": "umrah_mandiri",
    "🎮 Rewards & Quiz": "engagement",    # NEW
    "🤖 AI Chat": "ai_chat",
    "ℹ️ Tentang": "about",
}
```

### Step 3: Tambah Engagement Widget di Sidebar

Di dalam fungsi `render_sidebar()`, setelah branding:

```python
def render_sidebar():
    with st.sidebar:
        # ... existing branding code ...
        
        # Add engagement widget
        render_sidebar_engagement_widget()
        
        # ... rest of sidebar code ...
```

### Step 4: Tambah Route untuk Engagement Page

Di fungsi `main()`, tambahkan route:

```python
def main():
    # ... existing code ...
    
    # Initialize engagement
    init_engagement_state()
    check_daily_login()
    
    # Route pages
    if page == "engagement":
        render_engagement_page()  # New function
    elif page == "home":
        render_home()
    # ... other routes ...
```

### Step 5: Buat Engagement Page Function

Tambahkan fungsi baru:

```python
def render_engagement_page():
    """Render engagement hub with tabs"""
    init_engagement_state()
    init_quiz_state()
    
    tab1, tab2, tab3 = st.tabs(["🎮 Rewards", "🧠 Quiz", "🎁 Referral"])
    
    with tab1:
        render_engagement_hub()
    
    with tab2:
        render_quiz_page()
    
    with tab3:
        from engagement import generate_referral_code
        ref_code = generate_referral_code("user123")
        render_invite_modal(ref_code)
```

---

## 🎯 Integrasi Points di Fitur Existing

### Award Points Saat Simulasi

Di `render_cost_simulation()`:

```python
def render_cost_simulation():
    # ... existing code ...
    
    if st.button("Hitung Simulasi"):
        # ... calculation code ...
        
        # Award points
        award_points(POINTS_CONFIG["use_simulator"], "Simulasi biaya")
        
        # Track stats
        if "engagement" in st.session_state:
            st.session_state.engagement["stats"]["simulations"] += 1
```

### Award Points Saat Buat Rencana

Di `render_create_plan()`:

```python
def render_create_plan():
    # ... existing code ...
    
    if plan_created:
        award_points(POINTS_CONFIG["create_plan"], "Membuat rencana")
        
        # Check for first plan badge
        from engagement import award_badge
        award_badge("plan_creator")
```

### Tambah Share Buttons di Hasil Simulasi

```python
from social_viral import render_share_buttons, render_share_card

# Setelah menampilkan hasil simulasi
render_share_card("budget_result", {
    "package": selected_package,
    "budget": total_cost,
    "duration": duration,
    "departure": departure_city
})

st.markdown("### 📤 Bagikan Hasil Simulasi")
render_share_buttons("budget_result", 
    package=selected_package,
    budget=f"{total_cost:,.0f}",
    duration=str(duration)
)
```

---

## 🔥 Fitur Engagement Highlights

### 1. Daily Login Rewards
- 7-day streak cycle
- Increasing rewards per day
- Streak badges at 7, 30, 100 days

### 2. Points System (Labbaik Points / LP)
- Earn LP from various actions
- 10 levels: Jamaah Pemula → Haji Mabrur
- Visual progress tracking

### 3. Badges & Achievements
- 15+ unique badges
- Categories: Starter, Planning, Streak, Social, Learning, Secret
- Secret badges for special achievements

### 4. Referral System
- Unique referral codes
- 200 LP per successful referral
- Milestone rewards at 5, 10, 25, 50 referrals

### 5. Quiz System
- 3 quiz categories: Manasik, Doa, Sejarah
- Timed challenges
- Learning paths with certificates

### 6. Social Proof
- Live activity feed
- Success stories carousel
- Community statistics

### 7. Viral Features
- WhatsApp/Facebook/Twitter sharing
- Share-to-unlock mechanics
- Community goals

---

## 📊 Database Integration (Optional)

Untuk menyimpan data engagement ke database:

```python
# Di db_integration.py, tambahkan:

def db_save_engagement(user_id, engagement_data):
    """Save engagement data to database"""
    # ... implementation
    
def db_get_engagement(user_id):
    """Get engagement data from database"""
    # ... implementation
    
def db_get_leaderboard(limit=10):
    """Get top users for leaderboard"""
    # ... implementation
```

SQL Schema:
```sql
CREATE TABLE user_engagement (
    user_id TEXT PRIMARY KEY,
    points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    badges TEXT DEFAULT '[]',
    streak INTEGER DEFAULT 0,
    last_login DATE,
    referral_code TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE referrals (
    id SERIAL PRIMARY KEY,
    inviter_id TEXT REFERENCES user_engagement(user_id),
    invitee_id TEXT REFERENCES user_engagement(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Quick Start

1. Copy 3 file engagement ke repository
2. Import di app.py
3. Tambah menu "🎮 Rewards & Quiz"
4. Tambah `init_engagement_state()` di `main()`
5. Deploy dan test!

---

## 📈 Expected Impact

| Metric | Expected Increase |
|--------|------------------|
| Daily Active Users | +40-60% |
| Session Duration | +30-50% |
| Return Rate | +50-70% |
| Referral Sign-ups | +200-400% |
| Feature Adoption | +35-55% |

---

## 💡 Tips Optimasi

1. **A/B Test Rewards**: Test different point values
2. **Seasonal Events**: Add limited-time challenges during Ramadan
3. **Push Notifications**: Remind users about streaks
4. **Social Proof**: Show "X users online now" 
5. **Personalization**: Recommend quizzes based on user level

---

Dibuat dengan ❤️ untuk LABBAIK
