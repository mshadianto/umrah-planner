# db_integration.py - LABBAIK Database Integration v1.1.0
# Matching Neon PostgreSQL schema: page_views, users, open_trips, forum_posts
# Lightweight wrapper for Streamlit Cloud deployment

import streamlit as st
import hashlib
import secrets
from datetime import datetime
from typing import Optional, Dict, List

# ═══════════════════════════════════════════════════════════════════
# 🗄️ DATABASE CONNECTION
# ═══════════════════════════════════════════════════════════════════
def get_db_connection():
    """Get database connection - returns None if not configured"""
    try:
        return st.connection("neon", type="sql")
    except:
        return None

def is_db_available() -> bool:
    return get_db_connection() is not None

# ═══════════════════════════════════════════════════════════════════
# 🔐 PASSWORD UTILITIES
# ═══════════════════════════════════════════════════════════════════
def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    return f"{salt}:{hashlib.sha256((password + salt).encode()).hexdigest()}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash"""
    try:
        if ':' in stored_hash:
            salt, hash_value = stored_hash.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hash_value
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    except:
        return False

# ═══════════════════════════════════════════════════════════════════
# 👤 USER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════
def db_create_user(email: str, password: str, name: str, phone: str = "", city: str = "") -> Dict:
    """Create new user in database"""
    conn = get_db_connection()
    if not conn:
        return {"success": False, "error": "Database not available", "use_session": True}
    
    try:
        existing = conn.query("SELECT id FROM users WHERE email = :email", 
                             params={"email": email.lower()}, ttl=0)
        if len(existing) > 0:
            return {"success": False, "error": "Email sudah terdaftar"}
        
        role = "admin" if "admin" in email.lower() else "user"
        
        with conn.session as session:
            session.execute("""
                INSERT INTO users (email, password_hash, name, phone, city, role, created_at)
                VALUES (:email, :password_hash, :name, :phone, :city, :role, CURRENT_TIMESTAMP)
            """, {
                "email": email.lower(), "password_hash": hash_password(password),
                "name": name, "phone": phone, "city": city, "role": role
            })
            session.commit()
        
        return {"success": True, "message": f"Akun berhasil dibuat! Role: {role.upper()}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def db_authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate user from database"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        result = conn.query("SELECT * FROM users WHERE email = :email",
                           params={"email": email.lower()}, ttl=0)
        if len(result) == 0:
            return None
        
        user = result.to_dict('records')[0]
        if verify_password(password, user.get('password_hash', '')):
            try:
                with conn.session as session:
                    session.execute("""
                        UPDATE users SET last_login = CURRENT_TIMESTAMP, 
                        login_count = COALESCE(login_count, 0) + 1 WHERE id = :id
                    """, {"id": user['id']})
                    session.commit()
            except: pass
            
            return {
                "id": user['id'], "email": user['email'], "name": user['name'],
                "phone": user.get('phone', ''), "city": user.get('city', ''),
                "role": user.get('role', 'user'), "avatar": user.get('avatar', '👤')
            }
        return None
    except:
        return None

# ═══════════════════════════════════════════════════════════════════
# 📊 PAGE VIEWS (Matching: page_views table)
# Schema: id, page_name, visitor_id, viewed_at
# ═══════════════════════════════════════════════════════════════════
def db_log_page_view(page_name: str, visitor_id: str):
    """Log page view to database"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.session as session:
            session.execute("""
                INSERT INTO page_views (page_name, visitor_id, viewed_at)
                VALUES (:page_name, :visitor_id, CURRENT_TIMESTAMP)
            """, {"page_name": page_name, "visitor_id": visitor_id})
            session.commit()
    except: pass

def db_get_visitor_stats(base_visitors: int = 966) -> Dict:
    """Get visitor statistics with historical base"""
    conn = get_db_connection()
    base = {"total_visitors": base_visitors, "total_views": base_visitors * 5, 
            "today_visitors": 0, "today_views": 0}
    if not conn:
        return base
    
    try:
        # Unique visitors from page_views
        r = conn.query("SELECT COUNT(DISTINCT visitor_id) as c FROM page_views", ttl=60)
        db_visitors = r.to_dict('records')[0]['c'] or 0
        base["total_visitors"] = base_visitors + db_visitors
        
        # Total views
        r = conn.query("SELECT COUNT(*) as c FROM page_views", ttl=60)
        base["total_views"] = (base_visitors * 5) + (r.to_dict('records')[0]['c'] or 0)
        
        # Today's unique visitors
        r = conn.query("SELECT COUNT(DISTINCT visitor_id) as c FROM page_views WHERE DATE(viewed_at) = CURRENT_DATE", ttl=60)
        base["today_visitors"] = r.to_dict('records')[0]['c'] or 0
        
        # Today's views
        r = conn.query("SELECT COUNT(*) as c FROM page_views WHERE DATE(viewed_at) = CURRENT_DATE", ttl=60)
        base["today_views"] = r.to_dict('records')[0]['c'] or 0
        
        return base
    except:
        return base

def db_get_page_stats() -> Dict:
    """Get per-page view statistics"""
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        r = conn.query("""
            SELECT page_name, COUNT(*) as views 
            FROM page_views GROUP BY page_name ORDER BY views DESC
        """, ttl=60)
        return {row['page_name']: row['views'] for row in r.to_dict('records')}
    except:
        return {}

# ═══════════════════════════════════════════════════════════════════
# 🤝 OPEN TRIPS
# ═══════════════════════════════════════════════════════════════════
def db_create_trip(creator_id: int, trip_data: Dict) -> Dict:
    """Create new open trip"""
    conn = get_db_connection()
    if not conn:
        return {"success": False, "error": "Database not available"}
    
    try:
        trip_code = f"OT{secrets.token_hex(4).upper()}"
        with conn.session as session:
            session.execute("""
                INSERT INTO open_trips (creator_id, trip_code, title, departure_date, departure_city,
                    package_type, budget_per_person, duration_days, nights_makkah, nights_madinah,
                    max_members, gender_preference, age_preference, special_notes, amenities, 
                    whatsapp_group, status, created_at)
                VALUES (:creator_id, :trip_code, :title, :departure_date, :departure_city,
                    :package_type, :budget_per_person, :duration_days, :nights_makkah, :nights_madinah,
                    :max_members, :gender_preference, :age_preference, :special_notes, :amenities,
                    :whatsapp_group, 'open', CURRENT_TIMESTAMP)
            """, {
                "creator_id": creator_id, "trip_code": trip_code,
                "title": trip_data.get("title", ""), "departure_date": trip_data.get("departure_date"),
                "departure_city": trip_data.get("departure_city", ""),
                "package_type": trip_data.get("package_type", "standard"),
                "budget_per_person": trip_data.get("budget_per_person", 0),
                "duration_days": trip_data.get("duration_days", 9),
                "nights_makkah": trip_data.get("nights_makkah", 4),
                "nights_madinah": trip_data.get("nights_madinah", 3),
                "max_members": trip_data.get("max_members", 10),
                "gender_preference": trip_data.get("gender_preference", "Campuran"),
                "age_preference": trip_data.get("age_preference", "Semua Usia"),
                "special_notes": trip_data.get("special_notes", ""),
                "amenities": ",".join(trip_data.get("amenities", [])),
                "whatsapp_group": trip_data.get("whatsapp_group", "")
            })
            session.commit()
        return {"success": True, "trip_code": trip_code}
    except Exception as e:
        return {"success": False, "error": str(e)}

def db_get_open_trips(filters: Dict = None) -> List[Dict]:
    """Get open trips from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        query = """
            SELECT t.*, u.name as creator_name, u.city as creator_city, u.avatar as creator_avatar
            FROM open_trips t LEFT JOIN users u ON t.creator_id = u.id
            WHERE t.status = 'open'
        """
        params = {}
        
        if filters:
            if filters.get("max_budget"):
                query += " AND t.budget_per_person <= :max_budget"
                params["max_budget"] = filters["max_budget"]
            if filters.get("package_type") and filters["package_type"] not in ["Semua", ""]:
                query += " AND t.package_type = :package_type"
                params["package_type"] = filters["package_type"]
        
        query += " ORDER BY t.created_at DESC LIMIT 50"
        result = conn.query(query, params=params, ttl=30)
        trips = result.to_dict('records')
        
        for trip in trips:
            trip['amenities'] = trip.get('amenities', '').split(',') if trip.get('amenities') else []
        return trips
    except:
        return []

# ═══════════════════════════════════════════════════════════════════
# 💬 FORUM POSTS
# ═══════════════════════════════════════════════════════════════════
def db_create_post(author_id: int, title: str, category: str, content: str) -> Dict:
    """Create forum post"""
    conn = get_db_connection()
    if not conn:
        return {"success": False, "error": "Database not available"}
    
    try:
        with conn.session as session:
            session.execute("""
                INSERT INTO forum_posts (author_id, title, category, content, likes, views, created_at)
                VALUES (:author_id, :title, :category, :content, 0, 0, CURRENT_TIMESTAMP)
            """, {"author_id": author_id, "title": title, "category": category, "content": content})
            session.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def db_get_forum_posts(category: str = None) -> List[Dict]:
    """Get forum posts"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        query = """
            SELECT p.*, u.name as author_name, u.avatar as author_avatar,
                   (SELECT COUNT(*) FROM forum_comments WHERE post_id = p.id) as comment_count
            FROM forum_posts p LEFT JOIN users u ON p.author_id = u.id
        """
        params = {}
        
        if category and category not in ["Semua", ""]:
            query += " WHERE p.category = :category"
            params["category"] = category
        
        query += " ORDER BY p.created_at DESC LIMIT 50"
        result = conn.query(query, params=params, ttl=30)
        return result.to_dict('records')
    except:
        return []

# ═══════════════════════════════════════════════════════════════════
# 🔄 HYBRID AUTH (Fallback to session_state)
# ═══════════════════════════════════════════════════════════════════
def hybrid_register(email: str, password: str, name: str, phone: str = "", city: str = "") -> Dict:
    """Register - database first, session fallback"""
    result = db_create_user(email, password, name, phone, city)
    
    if result.get("success"):
        return result
    elif result.get("use_session"):
        if "users_db" not in st.session_state:
            st.session_state.users_db = {}
        
        if email.lower() in st.session_state.users_db:
            return {"success": False, "error": "Email sudah terdaftar"}
        
        st.session_state.users_db[email.lower()] = {
            "email": email.lower(), "password_hash": hash_password(password),
            "name": name, "phone": phone, "city": city,
            "role": "admin" if "admin" in email.lower() else "user",
            "created_at": datetime.now().isoformat()
        }
        return {"success": True, "message": "Akun berhasil dibuat! (Offline Mode)"}
    return result

def hybrid_login(email: str, password: str) -> Optional[Dict]:
    """Login - database first, session fallback"""
    user = db_authenticate_user(email, password)
    if user:
        return user
    
    if "users_db" in st.session_state:
        user_data = st.session_state.users_db.get(email.lower())
        if user_data and verify_password(password, user_data.get("password_hash", "")):
            return {
                "id": hash(email), "email": user_data["email"], "name": user_data["name"],
                "phone": user_data.get("phone", ""), "city": user_data.get("city", ""),
                "role": user_data.get("role", "user"), "avatar": "👤"
            }
    return None