"""
LABBAIK Authentication Module
Simple session-based authentication
"""

import streamlit as st
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json

# Try to import bcrypt, fallback to hashlib
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False


def hash_password(password: str) -> str:
    """Hash a password securely"""
    if BCRYPT_AVAILABLE:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    else:
        # Fallback to SHA256 with salt
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
        # Fallback verification
        try:
            salt, stored_hash = hashed.split(":")
            check_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return check_hash == stored_hash
        except:
            return False


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
        # Simple in-memory user store (for demo purposes)
        st.session_state.users_db = {}


def register_user(email: str, password: str, name: str, phone: str = "") -> Dict[str, Any]:
    """Register a new user"""
    init_auth_state()
    
    # Check if email already exists
    if email.lower() in st.session_state.users_db:
        return {"success": False, "error": "Email sudah terdaftar"}
    
    # Create user
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
    
    # Find user
    user = st.session_state.users_db.get(email.lower())
    
    if not user:
        return {"success": False, "error": "Email tidak ditemukan"}
    
    # Verify password
    if not verify_password(password, user["password_hash"]):
        return {"success": False, "error": "Password salah"}
    
    # Create session
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


def require_login(func):
    """Decorator to require login for a function"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.warning("🔐 Silakan login untuk mengakses fitur ini")
            return None
        return func(*args, **kwargs)
    return wrapper


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
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🔐 Masuk ke LABBAIK")
        
        tab1, tab2 = st.tabs(["Masuk", "Daftar"])
        
        with tab1:
            render_login_form()
        
        with tab2:
            render_register_form()


def render_user_menu():
    """Render user menu for logged in users"""
    user = get_current_user()
    
    if user:
        with st.expander(f"👤 {user['name']}", expanded=False):
            st.write(f"📧 {user['email']}")
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
