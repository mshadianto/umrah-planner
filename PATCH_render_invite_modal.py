# ============================================
# PATCH: Fix render_invite_modal() HTML Rendering
# ============================================
# File: app.py
# Line: ~253-305
# Issue: HTML tidak ter-render di tab "Ajak Teman"
# Fix: Ensure unsafe_allow_html=True is properly set

# REPLACE the entire render_invite_modal function (line ~253-305) with this:

def render_invite_modal(referral_code):
    """Render invite modal with proper HTML rendering - FIXED VERSION"""
    share_url = f"https://labbaik.streamlit.app?ref={referral_code}"
    
    # Build HTML string first
    html_content = f"""
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
"""
    
    # CRITICAL: Use st.markdown with unsafe_allow_html=True
    st.markdown(html_content, unsafe_allow_html=True)


# ============================================
# VERIFICATION CHECKLIST:
# ============================================
# ✅ 1. HTML string is properly formatted as f-string
# ✅ 2. st.markdown() is called with unsafe_allow_html=True
# ✅ 3. No triple quotes inside f-string
# ✅ 4. All style attributes are properly closed
# ✅ 5. Function returns nothing (just renders)

# ============================================
# HOW TO APPLY THIS PATCH:
# ============================================
# 1. Open app.py
# 2. Find function render_invite_modal (around line 253-305)
# 3. Delete the entire old function
# 4. Copy-paste this fixed version
# 5. Save and restart Streamlit
# 6. Test tab "Ajak Teman" - should render beautifully now!

# ============================================
# EXPECTED RESULT:
# ============================================
# Tab "🎁 Ajak Teman" will show:
# - 🎁 emoji at top
# - "Ajak Teman, Dapat Bonus!" heading
# - Two cards showing +200 LP and +75 LP
# - Referral code in gold color
# - Share URL
# - WhatsApp and Telegram buttons

# NO MORE RAW HTML TEXT! ✅
