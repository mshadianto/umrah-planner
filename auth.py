"""
LABBAIK Authentication Module
Complete authentication system with roles and permissions
"""

import streamlit as st
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# Try to import bcrypt, fallback to hashlib
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False


# ============================================
# USER ROLES CONFIGURATION
# ============================================

USER_ROLES = {
    "guest": {
        "name": "Tamu",
        "icon": "👤",
        "color": "#888888",
        "permissions": ["view_public"],
        "limits": {
            "simulations_per_day": 3,
            "ai_queries_per_day": 5
        }
    },
    "user": {
        "name": "Member",
        "icon": "⭐",
        "color": "#4CAF50",
        "permissions": ["view_public", "use_simulator", "use_ai", "save_plans"],
        "limits": {
            "simulations_per_day": 20,
            "ai_queries_per_day": 50,
            "saved_plans": 10
        }
    },
    "premium": {
        "name": "Premium",
        "icon": "💎",
        "color": "#2196F3",
        "permissions": ["view_public", "use_simulator", "use_ai", "save_plans", "export_pdf", "priority_support"],
        "limits": {
            "simulations_per_day": 100,
            "ai_queries_per_day": 200,
            "saved_plans": 50
        }
    },
    "admin": {
        "name": "Admin",
        "icon": "👑",
        "color": "#D4AF37",
        "permissions": ["all"],
        "limits": {
            "simulations_per_day": -1,
            "ai_queries_per_day": -1,
            "saved_plans": -1
        }
    }
}


# ============================================
# PASSWORD UTILITIES
# ============================================

def hash_password(password: str) -> str:
    """Hash a password securely"""
    if BCRYPT_AVAILABLE:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    else:
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{hashed}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    if BCRYPT_AVAILABLE:
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except:
            return False
    else:
        try:
            salt, stored_hash = hashed.split(":")
            check_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return check_hash == stored_hash
        except:
            return False


# ============================================
# STATE INITIALIZATION
# ============================================

def init_auth_state():
    """Initialize authentication state"""
    if "auth" not in st.session_state:
        st.session_state.auth = {
            "logged_in": False,
            "user": None,
            "token": None,
            "login_time": None
        }
    
    if "users_db" not in st.session_state:
        st.session_state.users_db = {}
    
    if "usage_tracking" not in st.session_state:
        st.session_state.usage_tracking = {}


def init_user_database():
    """Initialize user database with demo users"""
    init_auth_state()
    
    # Add demo users if not exists
    demo_users = {
        "demo@labbaik.id": {
            "id": "demo001",
            "email": "demo@labbaik.id",
            "name": "Demo User",
            "phone": "081234567890",
            "password_hash": hash_password("demo123"),
            "created_at": "2024-01-01T00:00:00",
            "is_active": True,
            "role": "user"
        },
        "admin@labbaik.id": {
            "id": "admin001",
            "email": "admin@labbaik.id",
            "name": "Admin LABBAIK",
            "phone": "081234567891",
            "password_hash": hash_password("admin123"),
            "created_at": "2024-01-01T00:00:00",
            "is_active": True,
            "role": "admin"
        },
        "superadmin@labbaik.id": {
            "id": "superadmin001",
            "email": "superadmin@labbaik.id",
            "name": "Super Admin",
            "phone": "081234567892",
            "password_hash": hash_password("super123"),
            "created_at": "2024-01-01T00:00:00",
            "is_active": True,
            "role": "admin"
        },
        "premium@labbaik.id": {
            "id": "premium001",
            "email": "premium@labbaik.id",
            "name": "Premium User",
            "phone": "081234567893",
            "password_hash": hash_password("premium123"),
            "created_at": "2024-01-01T00:00:00",
            "is_active": True,
            "role": "premium"
        }
    }
    
    # Add demo users to database if not exists
    for email, user_data in demo_users.items():
        if email not in st.session_state.users_db:
            st.session_state.users_db[email] = user_data


# ============================================
# USER MANAGEMENT
# ============================================

def register_user(email: str, password: str, name: str, phone: str = "") -> Dict[str, Any]:
    """Register a new user"""
    init_auth_state()
    
    if email.lower() in st.session_state.users_db:
        return {"success": False, "error": "Email sudah terdaftar"}
    
    user_id = secrets.token_hex(8)
    user = {
        "id": user_id,
        "email": email.lower(),
        "name": name,
        "phone": phone,
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "is_active": True,
        "role": "user"
    }
    
    st.session_state.users_db[email.lower()] = user
    return {"success": True, "user_id": user_id}


def login_user(email: str, password: str) -> Dict[str, Any]:
    """Login a user"""
    init_auth_state()
    
    user = st.session_state.users_db.get(email.lower())
    
    if not user:
        return {"success": False, "error": "Email tidak ditemukan"}
    
    if not verify_password(password, user["password_hash"]):
        return {"success": False, "error": "Password salah"}
    
    token = secrets.token_hex(32)
    
    st.session_state.auth = {
        "logged_in": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "phone": user.get("phone", ""),
            "role": user.get("role", "user")
        },
        "token": token,
        "login_time": datetime.now().isoformat()
    }
    
    return {"success": True, "token": token}


def logout_user():
    """Logout current user"""
    init_auth_state()
    st.session_state.auth = {
        "logged_in": False,
        "user": None,
        "token": None,
        "login_time": None
    }


def is_logged_in() -> bool:
    """Check if user is logged in"""
    init_auth_state()
    return st.session_state.auth.get("logged_in", False)


def get_current_user() -> Optional[Dict]:
    """Get current logged in user"""
    init_auth_state()
    if is_logged_in():
        return st.session_state.auth.get("user")
    return None


def get_user_role_info(role: str) -> Dict:
    """Get role information"""
    return USER_ROLES.get(role, USER_ROLES["guest"])


# ============================================
# PERMISSIONS & LIMITS
# ============================================

def has_permission(user: Optional[Dict], permission: str) -> bool:
    """Check if user has a specific permission"""
    if not user:
        role_info = USER_ROLES["guest"]
    else:
        role_info = USER_ROLES.get(user.get("role", "guest"), USER_ROLES["guest"])
    
    if "all" in role_info["permissions"]:
        return True
    
    return permission in role_info["permissions"]


def check_limit(user: Optional[Dict], limit_type: str) -> bool:
    """Check if user is within usage limits"""
    init_auth_state()
    
    if not user:
        role_info = USER_ROLES["guest"]
        user_id = "guest"
    else:
        role_info = USER_ROLES.get(user.get("role", "guest"), USER_ROLES["guest"])
        user_id = user.get("id", "guest")
    
    limit = role_info["limits"].get(limit_type, 0)
    
    if limit == -1:
        return True
    
    today = datetime.now().strftime("%Y-%m-%d")
    tracking_key = f"{user_id}_{limit_type}_{today}"
    
    current_usage = st.session_state.usage_tracking.get(tracking_key, 0)
    
    return current_usage < limit


def increment_usage(user: Optional[Dict], usage_type: str):
    """Increment usage counter"""
    init_auth_state()
    
    user_id = user.get("id", "guest") if user else "guest"
    today = datetime.now().strftime("%Y-%m-%d")
    tracking_key = f"{user_id}_{usage_type}_{today}"
    
    current = st.session_state.usage_tracking.get(tracking_key, 0)
    st.session_state.usage_tracking[tracking_key] = current + 1


# ============================================
# UI COMPONENTS
# ============================================

def render_login_form():
    """Render login form"""
    init_auth_state()
    
    with st.form("login_form"):
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        submit = st.form_submit_button("🚀 Masuk", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("Mohon isi email dan password")
            else:
                result = login_user(email, password)
                if result["success"]:
                    st.success("✅ Login berhasil!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")


def render_register_form():
    """Render registration form"""
    init_auth_state()
    
    with st.form("register_form"):
        name = st.text_input("👤 Nama Lengkap")
        email = st.text_input("📧 Email")
        phone = st.text_input("📱 No. HP (opsional)")
        password = st.text_input("🔑 Password", type="password")
        confirm = st.text_input("🔑 Konfirmasi Password", type="password")
        
        submit = st.form_submit_button("📝 Daftar", use_container_width=True)
        
        if submit:
            if not name or not email or not password:
                st.error("Mohon isi semua field wajib")
            elif password != confirm:
                st.error("Password tidak cocok")
            elif len(password) < 6:
                st.error("Password minimal 6 karakter")
            else:
                result = register_user(email, password, name, phone)
                if result["success"]:
                    st.success("✅ Registrasi berhasil! Silakan login.")
                else:
                    st.error(f"❌ {result['error']}")


def render_login_page():
    """Render complete login/register page"""
    init_auth_state()
    init_user_database()  # Ensure demo users exist
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2rem; color: #D4AF37;">🔐</div>
            <h2 style="color: white; margin: 10px 0;">Masuk ke LABBAIK</h2>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🚪 Masuk", "📝 Daftar"])
        
        with tab1:
            render_login_form()
            
            st.markdown("---")
            
            # Demo credentials info
            with st.expander("🔑 Demo Login Credentials", expanded=False):
                st.markdown("""
                <div style="background: #1A1A1A; padding: 15px; border-radius: 10px; font-size: 0.85rem;">
                    <div style="margin-bottom: 10px;">
                        <strong style="color: #4CAF50;">👤 Demo User:</strong><br>
                        <code>demo@labbaik.id</code> / <code>demo123</code>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong style="color: #2196F3;">💎 Premium:</strong><br>
                        <code>premium@labbaik.id</code> / <code>premium123</code>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong style="color: #D4AF37;">👑 Admin:</strong><br>
                        <code>admin@labbaik.id</code> / <code>admin123</code>
                    </div>
                    <div>
                        <strong style="color: #9C27B0;">🔮 Super Admin:</strong><br>
                        <code>superadmin@labbaik.id</code> / <code>super123</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            render_register_form()


def render_user_badge(user: Optional[Dict]):
    """Render user badge with role info"""
    if not user:
        return
    
    role = user.get("role", "user")
    role_info = get_user_role_info(role)
    
    st.markdown(f"""
    <div style="display: inline-flex; align-items: center; gap: 8px; 
                background: {role_info['color']}20; padding: 5px 12px; 
                border-radius: 20px; border: 1px solid {role_info['color']}50;">
        <span>{role_info['icon']}</span>
        <span style="color: {role_info['color']}; font-weight: 600; font-size: 0.85rem;">
            {role_info['name']}
        </span>
    </div>
    """, unsafe_allow_html=True)


def render_upgrade_prompt(feature_name: str):
    """Render upgrade prompt for locked features"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1A1A1A 0%, #2D1F3D 100%);
                border-radius: 15px; padding: 20px; text-align: center;
                border: 2px dashed #9C27B050; margin: 20px 0;">
        <div style="font-size: 2rem; margin-bottom: 10px;">🔒</div>
        <div style="color: white; font-size: 1.1rem; font-weight: 600; margin-bottom: 10px;">
            Fitur {feature_name} Terkunci
        </div>
        <div style="color: #C9A86C; margin-bottom: 15px;">
            Upgrade ke Premium untuk mengakses fitur ini
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_user_menu():
    """Render user menu for logged in users"""
    user = get_current_user()
    
    if user:
        with st.expander(f"👤 {user['name']}", expanded=False):
            st.write(f"📧 {user['email']}")
            render_user_badge(user)
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()


def render_admin_dashboard():
    """Render admin dashboard"""
    user = get_current_user()
    
    if not user or user.get("role") != "admin":
        st.error("⛔ Akses ditolak. Halaman ini hanya untuk admin.")
        return
    
    st.header("👑 Admin Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", len(st.session_state.get("users_db", {})))
    
    with col2:
        st.metric("Active Sessions", 1)
    
    with col3:
        st.metric("Today's Queries", sum(
            v for k, v in st.session_state.get("usage_tracking", {}).items()
            if datetime.now().strftime("%Y-%m-%d") in k
        ))
    
    st.markdown("---")
    
    st.subheader("📊 User List")
    
    users = st.session_state.get("users_db", {})
    if users:
        for email, user_data in users.items():
            with st.expander(f"👤 {user_data['name']} ({email})"):
                st.write(f"**Role:** {user_data.get('role', 'user')}")
                st.write(f"**Created:** {user_data.get('created_at', 'N/A')}")
                st.write(f"**Active:** {'✅' if user_data.get('is_active', True) else '❌'}")
    else:
        st.info("Belum ada user terdaftar.")


def require_login(func):
    """Decorator to require login for a function"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            return None
        return func(*args, **kwargs)
    return wrapper
