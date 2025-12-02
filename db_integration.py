# db_integration.py - LABBAIK Database Integration
# Wrapper to integrate Neon PostgreSQL with existing session-based auth
# Version: 1.0.0

import streamlit as st
import hashlib
import secrets
from datetime import datetime
from typing import Optional, Dict, List, Any

# ============================================
# DATABASE CONNECTION
# ============================================

def get_db_connection():
    """Get database connection - returns None if not configured"""
    try:
        conn = st.connection("neon", type="sql")
        return conn
    except Exception as e:
        # Database not configured - fall back to session state
        return None


def is_db_available() -> bool:
    """Check if database is available"""
    conn = get_db_connection()
    return conn is not None


# ============================================
# PASSWORD HASHING
# ============================================

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash"""
    try:
        # Handle old format (plain SHA256) and new format (salt:hash)
        if ':' in stored_hash:
            salt, hash_value = stored_hash.split(':')
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return password_hash == hash_value
        else:
            # Old format - direct comparison (for migration)
            return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    except:
        return False


# ============================================
# USER MANAGEMENT - DATABASE
# ============================================

def db_create_user(email: str, password: str, name: str, phone: str = None, city: str = None) -> Dict:
    """Create new user in database"""
    conn = get_db_connection()
    if not conn:
        return {"success": False, "error": "Database not available", "use_session": True}
    
    try:
        # Check if email exists
        existing = conn.query(
            "SELECT id FROM users WHERE email = :email",
            params={"email": email.lower()},
            ttl=0
        )
        
        if len(existing) > 0:
            return {"success": False, "error": "Email sudah terdaftar"}
        
        password_hash = hash_password(password)
        
        with conn.session as session:
            session.execute(
                """
                INSERT INTO users (email, password_hash, name, phone, city, role, created_at)
                VALUES (:email, :password_hash, :name, :phone, :city, 'user', CURRENT_TIMESTAMP)
                """,
                {
                    "email": email.lower(),
                    "password_hash": password_hash,
                    "name": name,
                    "phone": phone or "",
                    "city": city or ""
                }
            )
            session.commit()
        
        return {"success": True, "message": "Akun berhasil dibuat!"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def db_authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate user from database"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        result = conn.query(
            "SELECT * FROM users WHERE email = :email",
            params={"email": email.lower()},
            ttl=0
        )
        
        if len(result) == 0:
            return None
        
        user = result.to_dict('records')[0]
        
        if verify_password(password, user['password_hash']):
            # Update last login
            try:
                with conn.session as session:
                    session.execute(
                        """
                        UPDATE users 
                        SET last_login = CURRENT_TIMESTAMP, login_count = COALESCE(login_count, 0) + 1
                        WHERE id = :id
                        """,
                        {"id": user['id']}
                    )
                    session.commit()
            except:
                pass
            
            # Return user data (without password)
            return {
                "id": user['id'],
                "email": user['email'],
                "name": user['name'],
                "phone": user.get('phone', ''),
                "city": user.get('city', ''),
                "role": user.get('role', 'user'),
                "avatar": user.get('avatar', '👤'),
                "created_at": str(user.get('created_at', '')),
            }
        
        return None
        
    except Exception as e:
        st.error(f"Auth error: {e}")
        return None


def db_get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        result = conn.query(
            """SELECT id, email, name, phone, city, role, avatar, created_at 
               FROM users WHERE email = :email""",
            params={"email": email.lower()},
            ttl=60
        )
        
        if len(result) > 0:
            return result.to_dict('records')[0]
        return None
    except:
        return None


def db_update_user(user_id: int, **kwargs) -> bool:
    """Update user profile"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        updates = []
        params = {"id": user_id}
        
        for key, value in kwargs.items():
            if value is not None and key in ['name', 'phone', 'city', 'avatar']:
                updates.append(f"{key} = :{key}")
                params[key] = value
        
        if updates:
            with conn.session as session:
                session.execute(
                    f"UPDATE users SET {', '.join(updates)} WHERE id = :id",
                    params
                )
                session.commit()
            return True
        return False
    except:
        return False


# ============================================
# OPEN TRIPS - DATABASE
# ============================================

def db_create_trip(creator_id: int, trip_data: Dict) -> Dict:
    """Create new open trip in database"""
    conn = get_db_connection()
    if not conn:
        return {"success": False, "error": "Database not available"}
    
    try:
        trip_code = f"OT{secrets.token_hex(4).upper()}"
        
        with conn.session as session:
            session.execute(
                """
                INSERT INTO open_trips (
                    creator_id, trip_code, title, departure_date, departure_city,
                    package_type, budget_per_person, duration_days, nights_makkah,
                    nights_madinah, max_members, gender_preference, age_preference,
                    special_notes, amenities, whatsapp_group, status, created_at
                ) VALUES (
                    :creator_id, :trip_code, :title, :departure_date, :departure_city,
                    :package_type, :budget_per_person, :duration_days, :nights_makkah,
                    :nights_madinah, :max_members, :gender_preference, :age_preference,
                    :special_notes, :amenities, :whatsapp_group, 'open', CURRENT_TIMESTAMP
                )
                """,
                {
                    "creator_id": creator_id,
                    "trip_code": trip_code,
                    "title": trip_data.get("title", ""),
                    "departure_date": trip_data.get("departure_date"),
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
                }
            )
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
            FROM open_trips t
            LEFT JOIN users u ON t.creator_id = u.id
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
            if filters.get("gender") and filters["gender"] not in ["Semua", ""]:
                query += " AND t.gender_preference = :gender"
                params["gender"] = filters["gender"]
            if filters.get("departure_city") and filters["departure_city"] not in ["Semua", ""]:
                query += " AND t.departure_city LIKE :city"
                params["city"] = f"%{filters['departure_city']}%"
        
        query += " ORDER BY t.created_at DESC LIMIT 50"
        
        result = conn.query(query, params=params, ttl=30)
        trips = result.to_dict('records')
        
        # Convert amenities string back to list
        for trip in trips:
            if trip.get('amenities'):
                trip['amenities'] = trip['amenities'].split(',') if trip['amenities'] else []
            else:
                trip['amenities'] = []
        
        return trips
        
    except Exception as e:
        st.error(f"Error loading trips: {e}")
        return []


def db_get_user_trips(user_id: int) -> List[Dict]:
    """Get trips created by user"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        result = conn.query(
            """
            SELECT * FROM open_trips 
            WHERE creator_id = :user_id 
            ORDER BY created_at DESC
            """,
            params={"user_id": user_id},
            ttl=30
        )
        return result.to_dict('records')
    except:
        return []


def db_update_trip_status(trip_id: int, status: str) -> bool:
    """Update trip status"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.session as session:
            session.execute(
                "UPDATE open_trips SET status = :status WHERE id = :id",
                {"status": status, "id": trip_id}
            )
            session.commit()
        return True
    except:
        return False


def db_delete_trip(trip_id: int) -> bool:
    """Delete a trip"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.session as session:
            session.execute("DELETE FROM trip_members WHERE trip_id = :id", {"id": trip_id})
            session.execute("DELETE FROM saved_trips WHERE trip_id = :id", {"id": trip_id})
            session.execute("DELETE FROM open_trips WHERE id = :id", {"id": trip_id})
            session.commit()
        return True
    except:
        return False


# ============================================
# FORUM POSTS - DATABASE
# ============================================

def db_create_post(author_id: int, title: str, category: str, content: str) -> Dict:
    """Create forum post in database"""
    conn = get_db_connection()
    if not conn:
        return {"success": False, "error": "Database not available"}
    
    try:
        with conn.session as session:
            session.execute(
                """
                INSERT INTO forum_posts (author_id, title, category, content, likes, views, created_at)
                VALUES (:author_id, :title, :category, :content, 0, 0, CURRENT_TIMESTAMP)
                """,
                {
                    "author_id": author_id,
                    "title": title,
                    "category": category,
                    "content": content
                }
            )
            session.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def db_get_forum_posts(category: str = None, sort_by: str = "newest") -> List[Dict]:
    """Get forum posts from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        query = """
            SELECT p.*, u.name as author_name, u.city as author_city, u.avatar as author_avatar,
                   (SELECT COUNT(*) FROM forum_comments WHERE post_id = p.id) as comment_count
            FROM forum_posts p
            LEFT JOIN users u ON p.author_id = u.id
        """
        params = {}
        
        if category and category not in ["Semua", ""]:
            query += " WHERE p.category = :category"
            params["category"] = category
        
        if sort_by == "popular":
            query += " ORDER BY p.likes DESC"
        elif sort_by == "views":
            query += " ORDER BY p.views DESC"
        else:
            query += " ORDER BY p.created_at DESC"
        
        query += " LIMIT 50"
        
        result = conn.query(query, params=params, ttl=30)
        return result.to_dict('records')
    except Exception as e:
        st.error(f"Error loading posts: {e}")
        return []


def db_get_post_comments(post_id: int) -> List[Dict]:
    """Get comments for a post"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        result = conn.query(
            """
            SELECT c.*, u.name as author_name, u.avatar as author_avatar
            FROM forum_comments c
            LEFT JOIN users u ON c.author_id = u.id
            WHERE c.post_id = :post_id
            ORDER BY c.created_at ASC
            """,
            params={"post_id": post_id},
            ttl=30
        )
        return result.to_dict('records')
    except:
        return []


def db_add_comment(post_id: int, author_id: int, content: str) -> bool:
    """Add comment to post"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.session as session:
            session.execute(
                """
                INSERT INTO forum_comments (post_id, author_id, content, created_at)
                VALUES (:post_id, :author_id, :content, CURRENT_TIMESTAMP)
                """,
                {"post_id": post_id, "author_id": author_id, "content": content}
            )
            session.commit()
        return True
    except:
        return False


def db_like_post(post_id: int, user_id: int) -> bool:
    """Like a post"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.session as session:
            # Insert like (ignore if already exists)
            session.execute(
                """
                INSERT INTO post_likes (post_id, user_id, created_at)
                VALUES (:post_id, :user_id, CURRENT_TIMESTAMP)
                ON CONFLICT (post_id, user_id) DO NOTHING
                """,
                {"post_id": post_id, "user_id": user_id}
            )
            
            # Update like count
            session.execute(
                """
                UPDATE forum_posts 
                SET likes = (SELECT COUNT(*) FROM post_likes WHERE post_id = :post_id)
                WHERE id = :post_id
                """,
                {"post_id": post_id}
            )
            session.commit()
        return True
    except:
        return False


def db_increment_views(post_id: int) -> bool:
    """Increment post views"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.session as session:
            session.execute(
                "UPDATE forum_posts SET views = views + 1 WHERE id = :id",
                {"id": post_id}
            )
            session.commit()
        return True
    except:
        return False


# ============================================
# ANALYTICS - DATABASE
# ============================================

def db_log_visit(session_id: str, page: str, user_id: int = None):
    """Log page visit to database"""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.session as session:
            session.execute(
                """
                INSERT INTO visitor_logs (session_id, user_id, page, visited_at)
                VALUES (:session_id, :user_id, :page, CURRENT_TIMESTAMP)
                """,
                {"session_id": session_id, "user_id": user_id, "page": page}
            )
            session.commit()
    except:
        pass


def db_get_stats() -> Dict:
    """Get visitor statistics"""
    conn = get_db_connection()
    if not conn:
        return {"total_visitors": 0, "total_views": 0, "today_visitors": 0, "total_users": 0, "total_trips": 0, "total_posts": 0}
    
    try:
        stats = {}
        
        # Total unique visitors
        result = conn.query("SELECT COUNT(DISTINCT session_id) as count FROM visitor_logs", ttl=300)
        stats["total_visitors"] = result.to_dict('records')[0]['count'] or 0
        
        # Total page views
        result = conn.query("SELECT COUNT(*) as count FROM visitor_logs", ttl=300)
        stats["total_views"] = result.to_dict('records')[0]['count'] or 0
        
        # Today's visitors
        result = conn.query(
            "SELECT COUNT(DISTINCT session_id) as count FROM visitor_logs WHERE DATE(visited_at) = CURRENT_DATE",
            ttl=60
        )
        stats["today_visitors"] = result.to_dict('records')[0]['count'] or 0
        
        # Total users
        result = conn.query("SELECT COUNT(*) as count FROM users", ttl=300)
        stats["total_users"] = result.to_dict('records')[0]['count'] or 0
        
        # Total trips
        result = conn.query("SELECT COUNT(*) as count FROM open_trips WHERE status = 'open'", ttl=300)
        stats["total_trips"] = result.to_dict('records')[0]['count'] or 0
        
        # Total posts
        result = conn.query("SELECT COUNT(*) as count FROM forum_posts", ttl=300)
        stats["total_posts"] = result.to_dict('records')[0]['count'] or 0
        
        return stats
        
    except Exception as e:
        return {"total_visitors": 0, "total_views": 0, "today_visitors": 0, "total_users": 0, "total_trips": 0, "total_posts": 0}


# ============================================
# HYBRID AUTH FUNCTIONS
# Fallback ke session_state jika database tidak tersedia
# ============================================

def hybrid_register(email: str, password: str, name: str, phone: str = None, city: str = None) -> Dict:
    """Register user - try database first, fallback to session"""
    # Try database first
    result = db_create_user(email, password, name, phone, city)
    
    if result.get("success"):
        return result
    elif result.get("use_session"):
        # Database not available - use session state
        if "users_db" not in st.session_state:
            st.session_state.users_db = {}
        
        if email.lower() in st.session_state.users_db:
            return {"success": False, "error": "Email sudah terdaftar"}
        
        st.session_state.users_db[email.lower()] = {
            "email": email.lower(),
            "password_hash": hash_password(password),
            "name": name,
            "phone": phone or "",
            "city": city or "",
            "role": "user",
            "created_at": datetime.now().isoformat()
        }
        return {"success": True, "message": "Akun berhasil dibuat! (Mode Offline)"}
    
    return result


def hybrid_login(email: str, password: str) -> Optional[Dict]:
    """Login user - try database first, fallback to session"""
    # Try database first
    user = db_authenticate_user(email, password)
    
    if user:
        return user
    
    # Fallback to session state
    if "users_db" in st.session_state:
        user_data = st.session_state.users_db.get(email.lower())
        if user_data and verify_password(password, user_data.get("password_hash", "")):
            return {
                "id": hash(email)[:8],
                "email": user_data["email"],
                "name": user_data["name"],
                "phone": user_data.get("phone", ""),
                "city": user_data.get("city", ""),
                "role": user_data.get("role", "user"),
                "avatar": "👤"
            }
    
    return None


def init_sample_data():
    """Initialize sample data if database is empty"""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # Check if we have any trips
        result = conn.query("SELECT COUNT(*) as count FROM open_trips", ttl=0)
        if result.to_dict('records')[0]['count'] == 0:
            # Add sample trips (optional)
            pass
        
        # Check if we have any posts
        result = conn.query("SELECT COUNT(*) as count FROM forum_posts", ttl=0)
        if result.to_dict('records')[0]['count'] == 0:
            # Add sample posts (optional)
            pass
            
    except:
        pass
