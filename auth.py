"""
👥 User Management & Authentication System
==========================================
Multi-tier user system with role-based access control
Integrated with Supabase Database

Roles:
- Free User: Basic access
- Basic: Paid tier 1
- Premium: Paid tier 2
- VIP: Paid tier 3
- Admin: Manage users & content
- Super Admin: Full system access

Developer: MS Hadianto
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib
import json
import random
import string
import os

# Import Supabase database module
from database import get_db, SupabaseDB, render_supabase_setup

# ============================================
# USER ROLES & PERMISSIONS
# ============================================

USER_ROLES = {
    "free": {
        "name": "Free User",
        "level": 1,
        "badge": "🆓",
        "color": "#9e9e9e",
        "permissions": [
            "view_home",
            "cost_simulation_basic",
            "scenario_compare_2",
            "ai_chat_5_daily",
            "checklist_view",
            "currency_converter",
        ],
        "limits": {
            "ai_chat_daily": 5,
            "scenario_compare": 2,
            "saved_plans": 1,
            "export_pdf": False,
            "price_alert": False,
        }
    },
    "basic": {
        "name": "Basic Member",
        "level": 2,
        "badge": "🥉",
        "color": "#cd7f32",
        "price": 49000,
        "permissions": [
            "view_home",
            "cost_simulation_full",
            "scenario_compare_all",
            "ai_chat_50_daily",
            "checklist_full",
            "currency_converter",
            "booking_search",
            "hotel_search",
            "saved_plans_5",
        ],
        "limits": {
            "ai_chat_daily": 50,
            "scenario_compare": -1,
            "saved_plans": 5,
            "export_pdf": False,
            "price_alert": False,
        }
    },
    "premium": {
        "name": "Premium Member",
        "level": 3,
        "badge": "🥈",
        "color": "#c0c0c0",
        "price": 149000,
        "permissions": [
            "view_home",
            "cost_simulation_full",
            "scenario_compare_all",
            "ai_chat_unlimited",
            "checklist_full",
            "currency_converter",
            "booking_search",
            "hotel_search",
            "saved_plans_unlimited",
            "export_pdf",
            "price_alert",
            "partner_discount_10",
            "insurance_discount",
        ],
        "limits": {
            "ai_chat_daily": -1,
            "scenario_compare": -1,
            "saved_plans": -1,
            "export_pdf": True,
            "price_alert": True,
        }
    },
    "vip": {
        "name": "VIP Elite",
        "level": 4,
        "badge": "👑",
        "color": "#ffd700",
        "price": 499000,
        "permissions": [
            "view_home",
            "cost_simulation_full",
            "scenario_compare_all",
            "ai_chat_unlimited",
            "checklist_full",
            "currency_converter",
            "booking_search",
            "hotel_search",
            "saved_plans_unlimited",
            "export_pdf",
            "price_alert",
            "partner_discount_15",
            "insurance_discount",
            "dedicated_support",
            "priority_booking",
            "exclusive_deals",
            "cashback_5_percent",
        ],
        "limits": {
            "ai_chat_daily": -1,
            "scenario_compare": -1,
            "saved_plans": -1,
            "export_pdf": True,
            "price_alert": True,
        }
    },
    "admin": {
        "name": "Administrator",
        "level": 5,
        "badge": "🛡️",
        "color": "#2196f3",
        "permissions": [
            "*",  # All user permissions
            "admin_dashboard",
            "manage_users",
            "view_analytics",
            "manage_content",
            "manage_partners",
            "view_leads",
            "export_data",
        ],
        "limits": {
            "ai_chat_daily": -1,
            "scenario_compare": -1,
            "saved_plans": -1,
            "export_pdf": True,
            "price_alert": True,
        }
    },
    "superadmin": {
        "name": "Super Admin",
        "level": 6,
        "badge": "⚡",
        "color": "#f44336",
        "permissions": [
            "*",  # Everything
            "system_settings",
            "manage_admins",
            "financial_reports",
            "delete_users",
            "backup_restore",
            "api_management",
            "audit_logs",
        ],
        "limits": {
            "ai_chat_daily": -1,
            "scenario_compare": -1,
            "saved_plans": -1,
            "export_pdf": True,
            "price_alert": True,
        }
    }
}

# Default Super Admin credentials (change in production!)
DEFAULT_SUPERADMIN = {
    "username": "superadmin",
    "email": "sopian.hadianto@gmail.com",
    "password_hash": hashlib.sha256("Admin@123".encode()).hexdigest(),
    "role": "superadmin",
    "name": "MS Hadianto",
    "phone": "628159658833",
    "created_at": "2025-11-26",
    "status": "active"
}

# ============================================
# USER DATABASE (Supabase Integration)
# ============================================

def init_user_database():
    """Initialize user database connection"""
    if "db" not in st.session_state:
        st.session_state.db = get_db()
    
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = {}
    
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}


def hash_password(password: str) -> str:
    """Hash password with SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_user_id() -> str:
    """Generate unique user ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"USR-{timestamp}-{suffix}"


def generate_session_token() -> str:
    """Generate session token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


# ============================================
# AUTHENTICATION FUNCTIONS (Supabase)
# ============================================

def register_user(username: str, email: str, password: str, name: str, phone: str = "") -> Dict:
    """Register new user using Supabase"""
    init_user_database()
    db = get_db()
    
    # Validation
    if len(password) < 6:
        return {"success": False, "error": "Password minimal 6 karakter"}
    
    if len(username) < 3:
        return {"success": False, "error": "Username minimal 3 karakter"}
    
    if "@" not in email:
        return {"success": False, "error": "Email tidak valid"}
    
    # Create user via database
    result = db.create_user(
        username=username,
        email=email,
        password=password,
        name=name,
        phone=phone,
        role="free"
    )
    
    return result


def do_login(username: str, password: str):
    """Perform login - called as callback"""
    if not username or not password:
        st.session_state.login_error = "Masukkan username dan password"
        return
    
    # Initialize if not done
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = {}
    
    db = get_db()
    
    # Check login attempts (brute force protection)
    attempts_key = f"attempts_{username}"
    if attempts_key in st.session_state.login_attempts:
        attempts = st.session_state.login_attempts[attempts_key]
        if attempts["count"] >= 5 and (datetime.now() - attempts["last_attempt"]).seconds < 300:
            st.session_state.login_error = "Terlalu banyak percobaan. Coba lagi dalam 5 menit."
            return
    
    # Get user from database
    user = db.get_user_by_username(username)
    
    if not user:
        st.session_state.login_error = "Username tidak ditemukan"
        return
    
    # Verify password
    if not db.verify_password(username, password):
        # Track failed attempts
        if attempts_key not in st.session_state.login_attempts:
            st.session_state.login_attempts[attempts_key] = {"count": 0, "last_attempt": datetime.now()}
        st.session_state.login_attempts[attempts_key]["count"] += 1
        st.session_state.login_attempts[attempts_key]["last_attempt"] = datetime.now()
        st.session_state.login_error = "Password salah"
        return
    
    if user.get("status") != "active":
        st.session_state.login_error = "Akun dinonaktifkan. Hubungi admin."
        return
    
    # Successful login - store in session state
    st.session_state.current_user = user
    st.session_state.login_error = None
    st.session_state.login_success = f"Selamat datang, {user.get('name', username)}!"
    
    # Reset login attempts
    if attempts_key in st.session_state.login_attempts:
        del st.session_state.login_attempts[attempts_key]


def login_user(username: str, password: str) -> Dict:
    """Login user - wrapper for compatibility"""
    do_login(username, password)
    
    if st.session_state.get("login_error"):
        return {"success": False, "error": st.session_state.login_error}
    else:
        return {"success": True, "user": st.session_state.current_user, "message": st.session_state.get("login_success", "Login berhasil!")}


def logout_user():
    """Logout current user"""
    st.session_state.current_user = None


def get_current_user() -> Optional[Dict]:
    """Get current logged in user"""
    return st.session_state.get("current_user")


def is_logged_in() -> bool:
    """Check if user is logged in"""
    return st.session_state.get("current_user") is not None


def has_permission(permission: str) -> bool:
    """Check if current user has permission"""
    user = get_current_user()
    if not user:
        return False
    
    role = user.get("role", "free")
    role_info = USER_ROLES.get(role, USER_ROLES["free"])
    permissions = role_info.get("permissions", [])
    
    return "*" in permissions or permission in permissions


def get_user_role_info() -> Dict:
    """Get current user's role info"""
    user = get_current_user()
    if not user:
        return USER_ROLES["free"]
    
    role = user.get("role", "free")
    return USER_ROLES.get(role, USER_ROLES["free"])


def check_limit(limit_type: str) -> bool:
    """Check if user is within limits"""
    user = get_current_user()
    if not user:
        return False
    
    role_info = get_user_role_info()
    limits = role_info.get("limits", {})
    limit_value = limits.get(limit_type, 0)
    
    if limit_value == -1:  # Unlimited
        return True
    
    if limit_type == "ai_chat_daily":
        return user["stats"]["ai_chat_today"] < limit_value
    
    return True


def increment_usage(usage_type: str):
    """Increment usage counter"""
    user = get_current_user()
    if not user:
        return
    
    if usage_type == "ai_chat":
        user["stats"]["ai_chat_today"] += 1


# ============================================
# SUBSCRIPTION MANAGEMENT (Supabase)
# ============================================

def upgrade_subscription(username: str, plan: str, months: int = 1) -> Dict:
    """Upgrade user subscription using Supabase"""
    init_user_database()
    db = get_db()
    
    if plan not in ["basic", "premium", "vip"]:
        return {"success": False, "error": "Paket tidak valid"}
    
    # Get user
    user = db.get_user_by_username(username)
    if not user:
        return {"success": False, "error": "User tidak ditemukan"}
    
    # Get price
    prices = {"basic": 49000, "premium": 149000, "vip": 499000}
    amount = prices.get(plan, 0) * months
    
    # Create subscription
    result = db.create_subscription(
        user_id=user["id"],
        plan=plan,
        months=months,
        amount=amount
    )
    
    if result.get("success"):
        # Update current user if same
        if st.session_state.current_user and st.session_state.current_user.get("username") == username:
            st.session_state.current_user["role"] = plan
        
        # Log action
        db.log_action(user["id"], "upgrade_subscription", "subscription", None, 
                     {"old_plan": user.get("role")}, {"new_plan": plan})
    
    return result


def downgrade_to_free(username: str) -> Dict:
    """Downgrade user to free"""
    init_user_database()
    db = get_db()
    
    user = db.get_user_by_username(username)
    if not user:
        return {"success": False, "error": "User tidak ditemukan"}
    
    # Update user role
    result = db.update_user(user["id"], {"role": "free"})
    
    if result.get("success"):
        # Update current user if same
        if st.session_state.current_user and st.session_state.current_user.get("username") == username:
            st.session_state.current_user["role"] = "free"
    
    return {"success": True, "message": "Downgrade ke Free berhasil"}


# ============================================
# ADMIN FUNCTIONS (Supabase)
# ============================================

def get_all_users() -> List[Dict]:
    """Get all users from Supabase"""
    init_user_database()
    db = get_db()
    return db.get_all_users()


def update_user_role(username: str, new_role: str, by_admin: str) -> Dict:
    """Update user role using Supabase"""
    init_user_database()
    db = get_db()
    
    if new_role not in USER_ROLES:
        return {"success": False, "error": "Role tidak valid"}
    
    # Only superadmin can create admins
    current_user = get_current_user()
    if new_role in ["admin", "superadmin"] and current_user.get("role") != "superadmin":
        return {"success": False, "error": "Hanya Super Admin yang bisa membuat Admin"}
    
    # Get user
    user = db.get_user_by_username(username)
    if not user:
        return {"success": False, "error": "User tidak ditemukan"}
    
    old_role = user.get("role")
    
    # Update role
    result = db.update_user(user["id"], {"role": new_role})
    
    if result.get("success"):
        # Log action
        db.log_action(
            current_user.get("id"),
            "update_user_role",
            "user",
            user["id"],
            {"role": old_role},
            {"role": new_role}
        )
        return {"success": True, "message": f"Role {username} diubah ke {new_role}"}
    
    return result


def toggle_user_status(username: str) -> Dict:
    """Toggle user active/inactive using Supabase"""
    init_user_database()
    db = get_db()
    
    if username == "superadmin":
        return {"success": False, "error": "Tidak bisa menonaktifkan Super Admin"}
    
    user = db.get_user_by_username(username)
    if not user:
        return {"success": False, "error": "User tidak ditemukan"}
    
    new_status = "inactive" if user.get("status") == "active" else "active"
    
    result = db.update_user(user["id"], {"status": new_status})
    
    if result.get("success"):
        current_user = get_current_user()
        db.log_action(
            current_user.get("id"),
            "toggle_user_status",
            "user",
            user["id"],
            {"status": user.get("status")},
            {"status": new_status}
        )
        return {"success": True, "message": f"Status {username}: {new_status}"}
    
    return result


def delete_user(username: str) -> Dict:
    """Delete user using Supabase"""
    init_user_database()
    db = get_db()
    
    if username == "superadmin":
        return {"success": False, "error": "Tidak bisa menghapus Super Admin"}
    
    user = db.get_user_by_username(username)
    if not user:
        return {"success": False, "error": "User tidak ditemukan"}
    
    current_user = get_current_user()
    
    result = db.delete_user(user["id"])
    
    if result.get("success"):
        db.log_action(
            current_user.get("id"),
            "delete_user",
            "user",
            user["id"],
            {"username": username},
            None
        )
    
    return result


def get_user_stats() -> Dict:
    """Get user statistics from Supabase"""
    init_user_database()
    db = get_db()
    return db.get_user_stats_summary()


# ============================================
# UI COMPONENTS
# ============================================

def render_login_page():
    """Render login page"""
    
    # Initialize session state for login
    if "login_error" not in st.session_state:
        st.session_state.login_error = None
    if "login_success" not in st.session_state:
        st.session_state.login_success = None
    
    # Check if already logged in
    if is_logged_in():
        user = get_current_user()
        st.success(f"✅ Anda sudah login sebagai **{user.get('name')}** ({user.get('role')})")
        st.info("Silakan pilih menu di sidebar untuk mengakses fitur.")
        return
    
    st.markdown("## 🔐 Login")
    
    # Show messages
    if st.session_state.login_error:
        st.error(st.session_state.login_error)
    if st.session_state.login_success:
        st.success(st.session_state.login_success)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        # Use form to prevent auto-rerun on input
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                remember = st.checkbox("Ingat saya")
            with col2:
                st.markdown("[Lupa password?](#)")
            
            submitted = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
        
        # Handle form submission OUTSIDE the form
        if submitted:
            # Clear previous messages
            st.session_state.login_error = None
            st.session_state.login_success = None
            
            if username and password:
                # Perform login
                do_login(username, password)
                
                # Check result and show feedback
                if is_logged_in():
                    user = get_current_user()
                    st.success(f"✅ Login berhasil! Selamat datang, {user.get('name')}!")
                    st.balloons()
                    # Clear show_login_page to go back to main navigation
                    st.session_state.show_login_page = False
                    st.rerun()
                elif st.session_state.login_error:
                    st.error(st.session_state.login_error)
            else:
                st.error("Masukkan username dan password")
    
    with tab2:
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                reg_name = st.text_input("Nama Lengkap *")
                reg_username = st.text_input("Username *")
                reg_email = st.text_input("Email *")
            with col2:
                reg_phone = st.text_input("No. WhatsApp")
                reg_password = st.text_input("Password *", type="password")
                reg_confirm = st.text_input("Konfirmasi Password *", type="password")
            
            agree = st.checkbox("Saya setuju dengan syarat & ketentuan")
            
            if st.form_submit_button("📝 Daftar", type="primary", use_container_width=True):
                if not all([reg_name, reg_username, reg_email, reg_password]):
                    st.error("Lengkapi semua field wajib")
                elif reg_password != reg_confirm:
                    st.error("Password tidak cocok")
                elif not agree:
                    st.error("Anda harus menyetujui syarat & ketentuan")
                else:
                    result = register_user(reg_username, reg_email, reg_password, reg_name, reg_phone)
                    if result["success"]:
                        st.success(result["message"])
                        st.info("Silakan login dengan akun baru Anda")
                    else:
                        st.error(result["error"])
    
    # Registration success message area
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>🔐 Belum punya akun? Daftar di tab <strong>Register</strong></p>
        <p>💡 Gratis untuk fitur dasar perencanaan umrah</p>
    </div>
    """, unsafe_allow_html=True)


def render_user_badge():
    """Render user badge in sidebar"""
    user = get_current_user()
    
    if user:
        role_info = get_user_role_info()
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {role_info['color']}88, {role_info['color']}44);
            padding: 0.75rem;
            border-radius: 10px;
            text-align: center;
            border: 2px solid {role_info['color']};
        ">
            <div style="font-size: 1.5rem;">{role_info['badge']}</div>
            <div style="font-weight: bold;">{user['name']}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">{role_info['name']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
    else:
        st.markdown("""
        <div style="
            background: #f5f5f5;
            padding: 0.75rem;
            border-radius: 10px;
            text-align: center;
        ">
            <div style="font-size: 1.5rem;">👤</div>
            <div>Guest User</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔑 Login / Register", use_container_width=True):
            st.session_state.show_login = True


def render_upgrade_prompt():
    """Render upgrade prompt for free users"""
    user = get_current_user()
    if not user or user["role"] != "free":
        return
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    ">
        <strong>🚀 Upgrade ke Premium</strong><br>
        <small>Unlock semua fitur + Diskon 20%</small>
    </div>
    """, unsafe_allow_html=True)


def render_access_denied():
    """Render access denied message"""
    st.error("🚫 Akses Ditolak")
    st.markdown("""
    Anda tidak memiliki akses ke fitur ini.
    
    **Upgrade paket Anda untuk membuka fitur ini:**
    """)
    
    # Show upgrade options
    cols = st.columns(3)
    for i, (role_id, role) in enumerate(list(USER_ROLES.items())[1:4]):
        with cols[i]:
            price = role.get("price", 0)
            st.markdown(f"""
            <div style="border:1px solid #ddd;padding:1rem;border-radius:10px;text-align:center;">
                <h3>{role['badge']} {role['name']}</h3>
                <h4>Rp {price:,}/bln</h4>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Pilih {role['name']}", key=f"upgrade_{role_id}", use_container_width=True)


# ============================================
# ADMIN DASHBOARD
# ============================================

def render_admin_dashboard():
    """Render admin dashboard"""
    user = get_current_user()
    
    if not user or user.get("role") not in ["admin", "superadmin"]:
        render_access_denied()
        return
    
    st.markdown("## 🛡️ Admin Dashboard")
    
    # Database status
    db = get_db()
    if db.is_connected:
        st.success("✅ Database: Supabase Connected")
    else:
        st.warning("⚠️ Database: Fallback Mode (In-Memory)")
    
    # Stats overview
    stats = get_user_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Users", stats.get("total", 0))
    with col2:
        st.metric("📈 New Today", stats.get("new_today", 0))
    with col3:
        st.metric("📅 This Month", stats.get("new_this_month", 0))
    with col4:
        st.metric("✅ Active", stats.get("by_status", {}).get("active", 0))
    
    st.markdown("---")
    
    # Admin tabs
    if user.get("role") == "superadmin":
        tabs = st.tabs(["👥 Users", "📊 Analytics", "⚙️ Settings", "🔐 Security", "🗄️ Database", "💰 Revenue"])
    else:
        tabs = st.tabs(["👥 Users", "📊 Analytics", "💰 Revenue"])
    
    # Users Tab
    with tabs[0]:
        render_user_management()
    
    # Analytics Tab
    with tabs[1]:
        render_admin_analytics(stats)
    
    # Revenue Tab (for both admin and superadmin)
    if user.get("role") == "superadmin":
        with tabs[2]:
            render_system_settings()
        with tabs[3]:
            render_security_settings()
        with tabs[4]:
            render_supabase_setup()  # Database setup page
        with tabs[5]:
            render_revenue_analytics()
    else:
        with tabs[2]:
            render_revenue_analytics()


def render_user_management():
    """Render user management section"""
    st.markdown("### 👥 User Management")
    
    users = get_all_users()
    current_user = get_current_user()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_role = st.selectbox("Filter Role", ["All"] + list(USER_ROLES.keys()))
    with col2:
        filter_status = st.selectbox("Filter Status", ["All", "active", "inactive"])
    with col3:
        search = st.text_input("🔍 Search", placeholder="Username atau email")
    
    # Filter users
    filtered_users = users
    if filter_role != "All":
        filtered_users = [u for u in filtered_users if u.get("role") == filter_role]
    if filter_status != "All":
        filtered_users = [u for u in filtered_users if u.get("status") == filter_status]
    if search:
        search_lower = search.lower()
        filtered_users = [u for u in filtered_users if 
                        search_lower in u.get("username", "").lower() or 
                        search_lower in u.get("email", "").lower()]
    
    st.markdown(f"**Showing {len(filtered_users)} users**")
    
    # User table
    for user in filtered_users:
        role_info = USER_ROLES.get(user.get("role", "free"), USER_ROLES["free"])
        status_color = "#4caf50" if user.get("status") == "active" else "#f44336"
        
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 2])
        
        with col1:
            st.markdown(f"""
            **{role_info['badge']} {user.get('name', 'N/A')}**<br>
            <small>@{user.get('username', 'N/A')}</small>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            {user.get('email', 'N/A')}<br>
            <small>{user.get('phone', '-')}</small>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <span style="color:{status_color};">●</span> {user.get('status', 'active')}
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"**{role_info['name']}**")
        
        with col5:
            if user.get("username") != "superadmin":
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("✏️", key=f"edit_{user['username']}", help="Edit"):
                        st.session_state[f"editing_{user['username']}"] = True
                with col_b:
                    if st.button("🔄", key=f"toggle_{user['username']}", help="Toggle Status"):
                        result = toggle_user_status(user["username"])
                        st.toast(result["message"])
                        st.rerun()
                with col_c:
                    if current_user["role"] == "superadmin":
                        if st.button("🗑️", key=f"del_{user['username']}", help="Delete"):
                            result = delete_user(user["username"])
                            st.toast(result["message"])
                            st.rerun()
        
        # Edit modal
        if st.session_state.get(f"editing_{user['username']}"):
            with st.expander(f"Edit {user['username']}", expanded=True):
                new_role = st.selectbox(
                    "Role",
                    list(USER_ROLES.keys()),
                    index=list(USER_ROLES.keys()).index(user.get("role", "free")),
                    key=f"role_select_{user['username']}"
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("💾 Save", key=f"save_{user['username']}"):
                        result = update_user_role(user["username"], new_role, current_user["username"])
                        st.toast(result["message"])
                        st.session_state[f"editing_{user['username']}"] = False
                        st.rerun()
                with col_b:
                    if st.button("❌ Cancel", key=f"cancel_{user['username']}"):
                        st.session_state[f"editing_{user['username']}"] = False
                        st.rerun()
        
        st.markdown("---")
    
    # Add new user (admin function)
    with st.expander("➕ Tambah User Baru"):
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Nama")
                new_username = st.text_input("Username")
                new_email = st.text_input("Email")
            with col2:
                new_phone = st.text_input("Phone")
                new_password = st.text_input("Password", type="password")
                new_role = st.selectbox("Role", list(USER_ROLES.keys()))
            
            if st.form_submit_button("➕ Tambah User"):
                result = register_user(new_username, new_email, new_password, new_name, new_phone)
                if result["success"]:
                    # Update role if not free
                    if new_role != "free":
                        update_user_role(new_username, new_role, current_user["username"])
                    st.success("User berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error(result["error"])


def render_admin_analytics(stats: Dict):
    """Render admin analytics"""
    st.markdown("### 📊 User Analytics")
    
    # Role distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Users by Role")
        for role, count in stats["by_role"].items():
            role_info = USER_ROLES.get(role, {})
            pct = (count / stats["total"] * 100) if stats["total"] > 0 else 0
            st.markdown(f"""
            {role_info.get('badge', '')} **{role_info.get('name', role)}**: {count} ({pct:.1f}%)
            """)
            st.progress(pct / 100)
    
    with col2:
        st.markdown("#### Users by Status")
        for status, count in stats["by_status"].items():
            color = "#4caf50" if status == "active" else "#f44336"
            pct = (count / stats["total"] * 100) if stats["total"] > 0 else 0
            st.markdown(f"""
            <span style="color:{color};">●</span> **{status.title()}**: {count} ({pct:.1f}%)
            """, unsafe_allow_html=True)
            st.progress(pct / 100)


def render_revenue_analytics():
    """Render revenue analytics"""
    st.markdown("### 💰 Revenue Analytics")
    
    # Simulated revenue data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Revenue MTD", "Rp 45.8 Jt", "+12%")
    with col2:
        st.metric("📦 Subscriptions", "156", "+23")
    with col3:
        st.metric("🤝 Affiliate", "Rp 12.3 Jt", "+8%")
    with col4:
        st.metric("📝 Leads", "234", "+45")
    
    st.markdown("---")
    
    # Revenue breakdown
    st.markdown("#### Revenue by Stream")
    streams = [
        ("Subscription", 15800000, "#4caf50"),
        ("Lead Generation", 12500000, "#2196f3"),
        ("Affiliate", 8700000, "#ff9800"),
        ("Insurance", 5400000, "#9c27b0"),
        ("Merchandise", 3400000, "#f44336"),
    ]
    
    for name, amount, color in streams:
        st.markdown(f"**{name}**: Rp {amount:,}")
        st.progress(amount / 20000000)


def render_system_settings():
    """Render system settings (superadmin only)"""
    st.markdown("### ⚙️ System Settings")
    
    st.warning("⚠️ Hati-hati! Perubahan di sini mempengaruhi seluruh sistem.")
    
    with st.form("system_settings"):
        st.markdown("#### General")
        app_name = st.text_input("App Name", "Umrah Planner AI")
        maintenance_mode = st.checkbox("Maintenance Mode")
        
        st.markdown("#### Limits")
        free_chat_limit = st.number_input("Free User Chat Limit/Day", 1, 100, 5)
        basic_chat_limit = st.number_input("Basic User Chat Limit/Day", 10, 500, 50)
        
        st.markdown("#### Pricing")
        basic_price = st.number_input("Basic Price (Rp)", 10000, 500000, 49000)
        premium_price = st.number_input("Premium Price (Rp)", 50000, 1000000, 149000)
        vip_price = st.number_input("VIP Price (Rp)", 100000, 2000000, 499000)
        
        if st.form_submit_button("💾 Save Settings"):
            st.success("Settings saved!")


def render_security_settings():
    """Render security settings (superadmin only)"""
    st.markdown("### 🔐 Security Settings")
    
    st.markdown("#### Change Super Admin Password")
    with st.form("change_password"):
        current_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("🔐 Change Password"):
            if new_pass != confirm_pass:
                st.error("Password tidak cocok")
            elif len(new_pass) < 6:
                st.error("Password minimal 6 karakter")
            else:
                # Verify current password
                user = get_current_user()
                if hash_password(current_pass) == user["password_hash"]:
                    user["password_hash"] = hash_password(new_pass)
                    st.session_state.users_db[user["username"]] = user
                    st.success("Password berhasil diubah!")
                else:
                    st.error("Password saat ini salah")
    
    st.markdown("---")
    
    st.markdown("#### Audit Log")
    st.info("Recent admin activities will be shown here")
    
    # Simulated audit log
    logs = [
        {"time": "2025-11-26 10:30", "user": "superadmin", "action": "Changed user role", "target": "user123"},
        {"time": "2025-11-26 10:25", "user": "superadmin", "action": "Login", "target": "-"},
        {"time": "2025-11-26 09:15", "user": "admin1", "action": "Viewed users", "target": "-"},
    ]
    
    for log in logs:
        st.markdown(f"`{log['time']}` **{log['user']}** - {log['action']} ({log['target']})")


# ============================================
# MAIN FUNCTION
# ============================================

def render_auth_page():
    """Main auth page render function"""
    init_user_database()
    
    if is_logged_in():
        user = get_current_user()
        if user["role"] in ["admin", "superadmin"]:
            render_admin_dashboard()
        else:
            st.success(f"Welcome, {user['name']}!")
            st.info("Anda sudah login. Silakan explore fitur-fitur yang tersedia.")
    else:
        render_login_page()


def require_login(func):
    """Decorator to require login"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            render_login_page()
            return
        return func(*args, **kwargs)
    return wrapper


def require_role(min_role: str):
    """Decorator to require minimum role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_logged_in():
                st.warning("🔐 Silakan login untuk mengakses fitur ini")
                render_login_page()
                return
            
            user = get_current_user()
            user_level = USER_ROLES.get(user["role"], {}).get("level", 0)
            required_level = USER_ROLES.get(min_role, {}).get("level", 0)
            
            if user_level < required_level:
                render_access_denied()
                return
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
