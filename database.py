"""
Database access layer for AI-Based Personalized Travel Planner.
Provides modular SQLite storage, user authentication, profile management,
and persistent user-specific travel data (saved places, itineraries, preferences, history).
Designed for portability, parameterized security, and future PostgreSQL migration.
"""

import os
import sqlite3
import json
import re
import datetime
from typing import Optional, Tuple, List, Dict, Any

try:
    import bcrypt
    _HAS_BCRYPT = True
except ImportError:
    _HAS_BCRYPT = False
    import hashlib
    import secrets

# Default SQLite database path
_DEFAULT_DB_FILENAME = "travel_planner.db"
_DB_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(_DB_DIR, _DEFAULT_DB_FILENAME)


def get_db_path() -> str:
    """Returns database path configured via env or default."""
    return os.environ.get("TRAVEL_PLANNER_DB_PATH", DEFAULT_DB_PATH)


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Creates a sqlite3 connection with foreign keys enabled and Row factory."""
    path = db_path or get_db_path()
    conn = sqlite3.connect(path, timeout=15.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ============================================================
# PASSWORD HASHING UTILITIES
# ============================================================

def hash_password(password: str) -> str:
    """Hashes a password securely using bcrypt (or PBKDF2 fallback)."""
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string.")
    
    if _HAS_BCRYPT:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    else:
        # Secure fallback using PBKDF2-HMAC-SHA256
        salt = secrets.token_hex(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
        return f"pbkdf2:sha256:100000${salt}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password string."""
    if not plain_password or not hashed_password:
        return False
    try:
        if hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$"):
            if _HAS_BCRYPT:
                return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
            return False
        elif hashed_password.startswith("pbkdf2:"):
            parts = hashed_password.split("$")
            if len(parts) != 3:
                return False
            _, salt, key_hex = parts
            computed = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100_000)
            return secrets.compare_digest(computed.hex(), key_hex)
        else:
            return False
    except Exception:
        return False


def validate_email(email: str) -> bool:
    """Validates standard email address format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))


# ============================================================
# DATABASE INITIALIZATION & SCHEMA MIGRATION
# ============================================================

def init_db(db_path: Optional[str] = None) -> None:
    """
    Initializes database tables and indexes safely without deleting existing data.
    Enforces foreign keys, indexes, and unique constraints.
    """
    path = db_path or get_db_path()
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = get_connection(path)
    with conn:
        cursor = conn.cursor()

        # 1. Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                display_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")

        # 2. User Profiles Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                preferred_travel_style TEXT DEFAULT 'Relaxed',
                budget_preference INTEGER DEFAULT 80000,
                favourite_destinations TEXT DEFAULT '[]',
                travel_interests TEXT DEFAULT '["Culture", "Food"]',
                preferred_language TEXT DEFAULT 'English',
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # 3. Saved Places Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                country TEXT NOT NULL,
                category TEXT DEFAULT '',
                description TEXT DEFAULT '',
                image_url TEXT DEFAULT '',
                metadata_json TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, name, country)
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_saved_places_user ON saved_places(user_id);")

        # 4. Itineraries Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itineraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                destination TEXT NOT NULL,
                starting_location TEXT DEFAULT '',
                days_count INTEGER DEFAULT 7,
                travelers_count INTEGER DEFAULT 1,
                budget INTEGER DEFAULT 80000,
                total_cost INTEGER DEFAULT 0,
                style TEXT DEFAULT 'Relaxed',
                interests_json TEXT DEFAULT '[]',
                itinerary_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_itineraries_user ON itineraries(user_id);")

        # 5. Itinerary Stops Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itinerary_stops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                itinerary_id INTEGER NOT NULL,
                day_number INTEGER NOT NULL,
                city TEXT DEFAULT '',
                title TEXT DEFAULT '',
                activities_json TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stops_itinerary ON itinerary_stops(itinerary_id);")

        # 6. Travel Preferences Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS travel_preferences (
                user_id INTEGER PRIMARY KEY,
                default_starting_location TEXT DEFAULT '',
                default_days INTEGER DEFAULT 7,
                default_travelers INTEGER DEFAULT 1,
                default_budget INTEGER DEFAULT 80000,
                default_style TEXT DEFAULT 'Relaxed',
                default_interests_json TEXT DEFAULT '["Culture", "Food"]',
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # 7. Trip History Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trip_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                destination TEXT NOT NULL,
                starting_location TEXT DEFAULT '',
                days INTEGER DEFAULT 7,
                travelers INTEGER DEFAULT 1,
                budget INTEGER DEFAULT 80000,
                total_cost INTEGER DEFAULT 0,
                style TEXT DEFAULT 'Relaxed',
                status TEXT DEFAULT 'planned',
                itinerary_summary_json TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_user ON trip_history(user_id);")

    conn.close()


# ============================================================
# USER AUTHENTICATION & MANAGEMENT
# ============================================================

def create_user(
    email: str,
    password: str,
    display_name: str,
    db_path: Optional[str] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Registers a new user with password hashing and validates requirements.
    Returns (success: bool, message: str, user_dict: dict|None).
    """
    email_clean = (email or "").strip().lower()
    name_clean = (display_name or "").strip()
    
    if not name_clean:
        return False, "Display name is required.", None
    if not email_clean or not validate_email(email_clean):
        return False, "Please enter a valid email address.", None
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long.", None

    conn = get_connection(db_path)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with conn:
            cursor = conn.cursor()
            # Check duplicate email
            cursor.execute("SELECT id FROM users WHERE email = ?;", (email_clean,))
            if cursor.fetchone():
                return False, "An account with this email already exists.", None

            pw_hash = hash_password(password)
            cursor.execute(
                """
                INSERT INTO users (email, password_hash, display_name, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?);
                """,
                (email_clean, pw_hash, name_clean, now_iso, now_iso)
            )
            user_id = cursor.lastrowid

            # Initialize user profile
            cursor.execute(
                """
                INSERT INTO user_profiles (user_id, preferred_travel_style, budget_preference,
                                           favourite_destinations, travel_interests, preferred_language, updated_at)
                VALUES (?, 'Relaxed', 80000, '[]', '["Culture", "Food"]', 'English', ?);
                """,
                (user_id, now_iso)
            )

            # Initialize travel preferences
            cursor.execute(
                """
                INSERT INTO travel_preferences (user_id, default_starting_location, default_days,
                                               default_travelers, default_budget, default_style,
                                               default_interests_json, updated_at)
                VALUES (?, '', 7, 1, 80000, 'Relaxed', '["Culture", "Food"]', ?);
                """,
                (user_id, now_iso)
            )

            user_data = {
                "id": user_id,
                "email": email_clean,
                "display_name": name_clean,
                "created_at": now_iso
            }
            return True, "Registration successful!", user_data

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists.", None
    except Exception as e:
        return False, f"Registration error: {str(e)}", None
    finally:
        conn.close()


def authenticate_user(
    email: str,
    password: str,
    db_path: Optional[str] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Authenticates a user via email and password.
    Returns (success: bool, message: str, user_dict: dict|None).
    Avoids revealing account existence on failed credentials.
    """
    email_clean = (email or "").strip().lower()
    if not email_clean or not password:
        return False, "Invalid email or password.", None

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, password_hash, display_name, created_at FROM users WHERE email = ?;",
            (email_clean,)
        )
        row = cursor.fetchone()
        if not row:
            return False, "Invalid email or password.", None

        if not verify_password(password, row["password_hash"]):
            return False, "Invalid email or password.", None

        user_data = {
            "id": row["id"],
            "email": row["email"],
            "display_name": row["display_name"],
            "created_at": row["created_at"]
        }
        return True, "Login successful!", user_data

    except Exception:
        return False, "An error occurred during authentication.", None
    finally:
        conn.close()


def get_user_by_id(user_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieves safe user information by user ID without password hash."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, display_name, created_at FROM users WHERE id = ?;",
            (user_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def seed_demo_account(db_path: Optional[str] = None, force_reset: bool = False) -> Dict[str, Any]:
    """
    Safely seeds the clearly labelled demo account with sample data.
    If the demo user already exists, preserves their saved modifications unless force_reset=True.
    Uses environment variable DEMO_ACCOUNT_PASSWORD if set, otherwise a deterministic secure demo pass.
    """
    demo_email = "demo.traveler@example.com"
    demo_pass = os.environ.get("DEMO_ACCOUNT_PASSWORD", "DemoTraveler2026!")
    demo_name = "Alex Rivera (Demo Traveler)"

    conn = get_connection(db_path)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, display_name FROM users WHERE email = ?;", (demo_email,))
            existing = cursor.fetchone()

            if existing:
                demo_id = existing["id"]
                demo_display_name = existing["display_name"] or demo_name
                if force_reset:
                    pw_hash = hash_password(demo_pass)
                    cursor.execute(
                        "UPDATE users SET password_hash = ?, display_name = ?, updated_at = ? WHERE id = ?;",
                        (pw_hash, demo_name, now_iso, demo_id)
                    )
            else:
                pw_hash = hash_password(demo_pass)
                cursor.execute(
                    """
                    INSERT INTO users (email, password_hash, display_name, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    (demo_email, pw_hash, demo_name, now_iso, now_iso)
                )
                demo_id = cursor.lastrowid
                demo_display_name = demo_name

            # Check if user profile exists
            cursor.execute("SELECT user_id FROM user_profiles WHERE user_id = ?;", (demo_id,))
            has_profile = cursor.fetchone() is not None

            if not has_profile or force_reset:
                cursor.execute(
                    """
                    INSERT INTO user_profiles (user_id, preferred_travel_style, budget_preference,
                                               favourite_destinations, travel_interests, preferred_language, updated_at)
                    VALUES (?, 'Balanced', 120000, '["Japan", "India", "France"]', '["Culture", "Food", "Heritage"]', 'English', ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        preferred_travel_style = excluded.preferred_travel_style,
                        budget_preference = excluded.budget_preference,
                        favourite_destinations = excluded.favourite_destinations,
                        travel_interests = excluded.travel_interests,
                        preferred_language = excluded.preferred_language,
                        updated_at = excluded.updated_at;
                    """,
                    (demo_id, now_iso)
                )

            # Check if travel preferences exist
            cursor.execute("SELECT user_id FROM travel_preferences WHERE user_id = ?;", (demo_id,))
            has_prefs = cursor.fetchone() is not None

            if not has_prefs or force_reset:
                cursor.execute(
                    """
                    INSERT INTO travel_preferences (user_id, default_starting_location, default_days,
                                                   default_travelers, default_budget, default_style,
                                                   default_interests_json, updated_at)
                    VALUES (?, 'Tokyo', 7, 2, 120000, 'Balanced', '["Culture", "Food", "Heritage"]', ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        default_starting_location = excluded.default_starting_location,
                        default_days = excluded.default_days,
                        default_travelers = excluded.default_travelers,
                        default_budget = excluded.default_budget,
                        default_style = excluded.default_style,
                        default_interests_json = excluded.default_interests_json,
                        updated_at = excluded.updated_at;
                    """,
                    (demo_id, now_iso)
                )

            # Seed demo saved places if fresh demo account or forced
            if (not existing) or force_reset:
                cursor.execute("SELECT COUNT(*) AS count FROM saved_places WHERE user_id = ?;", (demo_id,))
                if cursor.fetchone()["count"] == 0:
                    demo_places = [
                        ("Fushimi Inari-taisha", "Japan", "Shrine", "Iconic shrine with thousands of vermilion torii gates.", ""),
                        ("Taj Mahal", "India", "Monument", "UNESCO World Heritage ivory-white marble mausoleum in Agra.", ""),
                        ("Eiffel Tower", "France", "Landmark", "World famous wrought-iron lattice tower on the Champ de Mars.", "")
                    ]
                    for name, country, cat, desc, img in demo_places:
                        cursor.execute(
                            """
                            INSERT OR IGNORE INTO saved_places (user_id, name, country, category, description, image_url, metadata_json, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, '{}', ?);
                            """,
                            (demo_id, name, country, cat, desc, img, now_iso)
                        )

            # Seed a demo itinerary if fresh demo account or forced
            if (not existing) or force_reset:
                cursor.execute("SELECT COUNT(*) AS count FROM itineraries WHERE user_id = ?;", (demo_id,))
                if cursor.fetchone()["count"] == 0:
                    sample_itin = {
                        "destination": "Japan",
                        "starting": "Tokyo",
                        "days": [
                            {
                                "day": 1,
                                "city": "Tokyo",
                                "title": "Tokyo: Arrival & City Highlights",
                                "activities": [
                                    {"time": "10:00 AM", "activity": "Senso-ji Temple & Asakusa Walk", "cost": 1500},
                                    {"time": "01:00 PM", "activity": "Authentic Ramen Lunch", "cost": 1200},
                                    {"time": "04:00 PM", "activity": "Tokyo Skytree Sunset Panorama", "cost": 2500}
                                ]
                            },
                            {
                                "day": 2,
                                "city": "Kyoto",
                                "title": "Kyoto: Historic Temples & Shrines",
                                "activities": [
                                    {"time": "09:30 AM", "activity": "Fushimi Inari Torii Gate Trail", "cost": 1000},
                                    {"time": "01:30 PM", "activity": "Traditional Kaiseki Cuisine", "cost": 3000},
                                    {"time": "05:00 PM", "activity": "Gion Evening Heritage Walk", "cost": 800}
                                ]
                            }
                        ],
                        "total_cost": 42000,
                        "budget": {"Accommodation": 15000, "Transport": 12000, "Food": 10000, "Activities": 5000}
                    }
                    cursor.execute(
                        """
                        INSERT INTO itineraries (user_id, title, destination, starting_location, days_count,
                                                travelers_count, budget, total_cost, style, interests_json,
                                                itinerary_json, created_at, updated_at)
                        VALUES (?, 'Iconic Japan 7-Day Journey', 'Japan', 'Tokyo', 7, 2, 120000, 42000, 'Balanced',
                                '["Culture", "Food"]', ?, ?, ?);
                        """,
                        (demo_id, json.dumps(sample_itin), now_iso, now_iso)
                    )
                    itin_id = cursor.lastrowid
                    cursor.execute(
                        """
                        INSERT INTO trip_history (user_id, destination, starting_location, days, travelers,
                                                 budget, total_cost, style, status, itinerary_summary_json, created_at)
                        VALUES (?, 'Japan', 'Tokyo', 7, 2, 120000, 42000, 'Balanced', 'planned', ?, ?);
                        """,
                        (demo_id, json.dumps({"itinerary_id": itin_id, "title": "Iconic Japan 7-Day Journey"}), now_iso)
                    )

        return {
            "id": demo_id,
            "email": demo_email,
            "password": demo_pass,
            "display_name": demo_display_name
        }
    finally:
        conn.close()


# ============================================================
# USER PROFILES
# ============================================================

def get_user_profile(user_id: int, db_path: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves full profile for a specific user ID."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT u.display_name, u.email, u.created_at,
                   p.preferred_travel_style, p.budget_preference,
                   p.favourite_destinations, p.travel_interests,
                   p.preferred_language, p.updated_at
            FROM users u
            LEFT JOIN user_profiles p ON u.id = p.user_id
            WHERE u.id = ?;
            """,
            (user_id,)
        )
        row = cursor.fetchone()
        if not row:
            return {}

        fav_dest = []
        try:
            fav_dest = json.loads(row["favourite_destinations"] or "[]")
        except Exception:
            fav_dest = []

        interests = []
        try:
            interests = json.loads(row["travel_interests"] or "[]")
        except Exception:
            interests = ["Culture", "Food"]

        return {
            "user_id": user_id,
            "display_name": row["display_name"],
            "email": row["email"],
            "preferred_travel_style": row["preferred_travel_style"] or "Relaxed",
            "budget_preference": row["budget_preference"] or 80000,
            "favourite_destinations": fav_dest,
            "travel_interests": interests,
            "preferred_language": row["preferred_language"] or "English",
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    finally:
        conn.close()


def update_user_profile(
    user_id: int,
    display_name: Optional[str] = None,
    preferred_travel_style: Optional[str] = None,
    budget_preference: Optional[int] = None,
    favourite_destinations: Optional[List[str]] = None,
    travel_interests: Optional[List[str]] = None,
    preferred_language: Optional[str] = None,
    db_path: Optional[str] = None
) -> Tuple[bool, str]:
    """Validates and updates user profile data."""
    conn = get_connection(db_path)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with conn:
            cursor = conn.cursor()
            # Update display name if supplied
            if display_name is not None:
                d_name = display_name.strip()
                if not d_name:
                    return False, "Display name cannot be empty."
                cursor.execute(
                    "UPDATE users SET display_name = ?, updated_at = ? WHERE id = ?;",
                    (d_name, now_iso, user_id)
                )

            # Ensure profile row exists
            cursor.execute("SELECT user_id FROM user_profiles WHERE user_id = ?;", (user_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO user_profiles (user_id, updated_at) VALUES (?, ?);",
                    (user_id, now_iso)
                )

            # Prepare update fields
            updates = []
            params = []
            if preferred_travel_style is not None:
                updates.append("preferred_travel_style = ?")
                params.append(preferred_travel_style)
            if budget_preference is not None:
                updates.append("budget_preference = ?")
                params.append(max(5000, int(budget_preference)))
            if favourite_destinations is not None:
                updates.append("favourite_destinations = ?")
                params.append(json.dumps(favourite_destinations))
            if travel_interests is not None:
                updates.append("travel_interests = ?")
                params.append(json.dumps(travel_interests))
            if preferred_language is not None:
                updates.append("preferred_language = ?")
                params.append(preferred_language)

            if updates:
                updates.append("updated_at = ?")
                params.append(now_iso)
                params.append(user_id)
                query = f"UPDATE user_profiles SET {', '.join(updates)} WHERE user_id = ?;"
                cursor.execute(query, tuple(params))

        return True, "Profile updated successfully!"
    except Exception as e:
        return False, f"Failed to update profile: {str(e)}"
    finally:
        conn.close()


# ============================================================
# TRAVEL PREFERENCES
# ============================================================

def get_user_preferences(user_id: int, db_path: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves travel preferences for a user."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT default_starting_location, default_days, default_travelers,
                   default_budget, default_style, default_interests_json, updated_at
            FROM travel_preferences
            WHERE user_id = ?;
            """,
            (user_id,)
        )
        row = cursor.fetchone()
        if not row:
            return {
                "starting_location": "",
                "days": 7,
                "travelers": 1,
                "budget": 80000,
                "style": "Relaxed",
                "interests": ["Culture", "Food"]
            }

        interests = ["Culture", "Food"]
        try:
            interests = json.loads(row["default_interests_json"] or "[]")
        except Exception:
            pass

        return {
            "starting_location": row["default_starting_location"] or "",
            "days": row["default_days"] or 7,
            "travelers": row["default_travelers"] or 1,
            "budget": row["default_budget"] or 80000,
            "style": row["default_style"] or "Relaxed",
            "interests": interests,
            "updated_at": row["updated_at"]
        }
    finally:
        conn.close()


def update_user_preferences(
    user_id: int,
    starting_location: Optional[str] = None,
    days: Optional[int] = None,
    travelers: Optional[int] = None,
    budget: Optional[int] = None,
    style: Optional[str] = None,
    interests: Optional[List[str]] = None,
    db_path: Optional[str] = None
) -> Tuple[bool, str]:
    """Saves updated default trip preferences for a user."""
    conn = get_connection(db_path)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO travel_preferences (user_id, default_starting_location, default_days,
                                               default_travelers, default_budget, default_style,
                                               default_interests_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    default_starting_location = COALESCE(?, default_starting_location),
                    default_days = COALESCE(?, default_days),
                    default_travelers = COALESCE(?, default_travelers),
                    default_budget = COALESCE(?, default_budget),
                    default_style = COALESCE(?, default_style),
                    default_interests_json = COALESCE(?, default_interests_json),
                    updated_at = excluded.updated_at;
                """,
                (
                    user_id,
                    starting_location or "",
                    days or 7,
                    travelers or 1,
                    budget or 80000,
                    style or "Relaxed",
                    json.dumps(interests if interests is not None else ["Culture", "Food"]),
                    now_iso,
                    # Updates on conflict:
                    starting_location,
                    days,
                    travelers,
                    budget,
                    style,
                    json.dumps(interests) if interests is not None else None
                )
            )
        return True, "Preferences updated successfully."
    except Exception as e:
        return False, f"Error saving preferences: {str(e)}"
    finally:
        conn.close()


# ============================================================
# SAVED PLACES (USER SPECIFIC)
# ============================================================

def get_saved_places(user_id: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all saved places for a specific user ID."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, country, category, description, image_url, metadata_json, created_at
            FROM saved_places
            WHERE user_id = ?
            ORDER BY created_at DESC;
            """,
            (user_id,)
        )
        places = []
        for row in cursor.fetchall():
            meta = {}
            try:
                meta = json.loads(row["metadata_json"] or "{}")
            except Exception:
                pass
            p_dict = {
                "id": row["id"],
                "name": row["name"],
                "country": row["country"],
                "category": row["category"],
                "description": row["description"],
                "image_url": row["image_url"],
                "created_at": row["created_at"],
                **meta
            }
            places.append(p_dict)
        return places
    finally:
        conn.close()


def is_place_saved_db(user_id: int, name: str, country: str, db_path: Optional[str] = None) -> bool:
    """Checks whether a specific place is saved by a given user."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM saved_places WHERE user_id = ? AND name = ? AND country = ? LIMIT 1;",
            (user_id, name.strip(), country.strip())
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def save_place_db(user_id: int, place_dict: Dict[str, Any], db_path: Optional[str] = None) -> bool:
    """Saves a place for a user in the database."""
    name = str(place_dict.get("name", "")).strip()
    country = str(place_dict.get("country", "")).strip()
    if not name or not country:
        return False

    cat = str(place_dict.get("category", "")).strip()
    desc = str(place_dict.get("description", "")).strip()
    img = str(place_dict.get("image_url", place_dict.get("image", ""))).strip()
    
    # Store other fields in metadata
    exclude_keys = {"name", "country", "category", "description", "image_url", "image", "id", "created_at"}
    meta = {k: v for k, v in place_dict.items() if k not in exclude_keys}
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO saved_places (user_id, name, country, category, description,
                                                    image_url, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (user_id, name, country, cat, desc, img, json.dumps(meta), now_iso)
            )
        return True
    except Exception:
        return False
    finally:
        conn.close()


def delete_saved_place_by_id(user_id: int, place_id: int, db_path: Optional[str] = None) -> bool:
    """
    Removes a saved place using its stable primary key ID and authenticated user ID.
    Enforces strict ownership check so users can only remove their own records.
    """
    if not isinstance(user_id, int) or not isinstance(place_id, int):
        try:
            user_id = int(user_id)
            place_id = int(place_id)
        except (ValueError, TypeError):
            return False

    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM saved_places WHERE id = ? AND user_id = ?;",
                (place_id, user_id)
            )
            return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def delete_saved_place_db(user_id: int, name: str, country: str, db_path: Optional[str] = None) -> bool:
    """Removes a saved place for a given user with strict ownership enforcement."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM saved_places WHERE user_id = ? AND (TRIM(LOWER(name)) = TRIM(LOWER(?)) AND TRIM(LOWER(country)) = TRIM(LOWER(?)));",
                (user_id, name.strip(), country.strip())
            )
            return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def toggle_save_place_db(user_id: int, place_dict: Dict[str, Any], db_path: Optional[str] = None) -> bool:
    """
    Toggles a saved place for a user in the database.
    Returns True if now saved, False if deleted.
    """
    name = str(place_dict.get("name", "")).strip()
    country = str(place_dict.get("country", "")).strip()
    if not name or not country:
        return False

    if is_place_saved_db(user_id, name, country, db_path=db_path):
        delete_saved_place_db(user_id, name, country, db_path=db_path)
        return False
    else:
        save_place_db(user_id, place_dict, db_path=db_path)
        return True


def clear_saved_places_db(user_id: int, db_path: Optional[str] = None) -> bool:
    """Clears all saved places for the specified user."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM saved_places WHERE user_id = ?;", (user_id,))
            return True
    except Exception:
        return False
    finally:
        conn.close()


# ============================================================
# ITINERARIES & ITINERARY STOPS (USER SPECIFIC)
# ============================================================

def save_itinerary_db(
    user_id: int,
    itinerary_data: Dict[str, Any],
    title: Optional[str] = None,
    db_path: Optional[str] = None
) -> Optional[int]:
    """
    Saves an itinerary for a user, populates itinerary_stops,
    and logs an entry in trip_history. Returns itinerary ID.
    """
    if not itinerary_data or not isinstance(itinerary_data, dict):
        return None

    dest = str(itinerary_data.get("destination", "Destination")).strip()
    starting = str(itinerary_data.get("starting", "")).strip()
    days_list = itinerary_data.get("days", [])
    days_count = len(days_list) if days_list else 7
    total_cost = int(itinerary_data.get("total_cost", 0))
    budget_raw = itinerary_data.get("budget", {})
    budget_total = sum(budget_raw.values()) if isinstance(budget_raw, dict) else 80000

    itin_title = (title or "").strip()
    if not itin_title:
        itin_title = f"{days_count}-Day Journey to {dest}"

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO itineraries (user_id, title, destination, starting_location, days_count,
                                        travelers_count, budget, total_cost, style, interests_json,
                                        itinerary_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?, 'Relaxed', '[]', ?, ?, ?);
                """,
                (
                    user_id, itin_title, dest, starting, days_count,
                    budget_total, total_cost, json.dumps(itinerary_data),
                    now_iso, now_iso
                )
            )
            itinerary_id = cursor.lastrowid

            # Populate itinerary stops for relational queries
            if days_list and isinstance(days_list, list):
                for day_obj in days_list:
                    d_num = day_obj.get("day", 1)
                    city = day_obj.get("city", dest)
                    d_title = day_obj.get("title", f"Day {d_num} in {city}")
                    acts = json.dumps(day_obj.get("activities", []))
                    cursor.execute(
                        """
                        INSERT INTO itinerary_stops (itinerary_id, day_number, city, title, activities_json, created_at)
                        VALUES (?, ?, ?, ?, ?, ?);
                        """,
                        (itinerary_id, d_num, city, d_title, acts, now_iso)
                    )

            # Record in trip_history
            summary_info = {
                "itinerary_id": itinerary_id,
                "title": itin_title,
                "days_count": days_count,
                "total_cost": total_cost
            }
            cursor.execute(
                """
                INSERT INTO trip_history (user_id, destination, starting_location, days, travelers,
                                         budget, total_cost, style, status, itinerary_summary_json, created_at)
                VALUES (?, ?, ?, ?, 1, ?, ?, 'Relaxed', 'planned', ?, ?);
                """,
                (user_id, dest, starting, days_count, budget_total, total_cost, json.dumps(summary_info), now_iso)
            )

            return itinerary_id
    except Exception as e:
        print(f"Error saving itinerary: {e}")
        return None
    finally:
        conn.close()


def get_user_itineraries(user_id: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all saved itineraries belonging to the user."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, destination, starting_location, days_count,
                   travelers_count, budget, total_cost, style, itinerary_json, created_at, updated_at
            FROM itineraries
            WHERE user_id = ?
            ORDER BY updated_at DESC;
            """,
            (user_id,)
        )
        results = []
        for row in cursor.fetchall():
            itin_data = {}
            try:
                itin_data = json.loads(row["itinerary_json"])
            except Exception:
                pass
            results.append({
                "id": row["id"],
                "title": row["title"],
                "destination": row["destination"],
                "starting_location": row["starting_location"],
                "days_count": row["days_count"],
                "travelers_count": row["travelers_count"],
                "budget": row["budget"],
                "total_cost": row["total_cost"],
                "style": row["style"],
                "itinerary": itin_data,
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })
        return results
    finally:
        conn.close()


def get_itinerary_by_id(user_id: int, itinerary_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieves a specific itinerary with strict user ownership validation."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, destination, starting_location, days_count,
                   travelers_count, budget, total_cost, style, itinerary_json, created_at, updated_at
            FROM itineraries
            WHERE id = ? AND user_id = ?;
            """,
            (itinerary_id, user_id)
        )
        row = cursor.fetchone()
        if not row:
            return None
        itin_data = {}
        try:
            itin_data = json.loads(row["itinerary_json"])
        except Exception:
            pass
        return {
            "id": row["id"],
            "title": row["title"],
            "destination": row["destination"],
            "starting_location": row["starting_location"],
            "days_count": row["days_count"],
            "travelers_count": row["travelers_count"],
            "budget": row["budget"],
            "total_cost": row["total_cost"],
            "style": row["style"],
            "itinerary": itin_data,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    finally:
        conn.close()


def get_latest_user_itinerary(user_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieves the most recent itinerary for a given user."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, destination, starting_location, days_count,
                   travelers_count, budget, total_cost, style, itinerary_json, created_at, updated_at
            FROM itineraries
            WHERE user_id = ?
            ORDER BY updated_at DESC LIMIT 1;
            """,
            (user_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        itin_data = {}
        try:
            itin_data = json.loads(row["itinerary_json"])
        except Exception:
            pass
        return {
            "id": row["id"],
            "title": row["title"],
            "destination": row["destination"],
            "starting_location": row["starting_location"],
            "days_count": row["days_count"],
            "travelers_count": row["travelers_count"],
            "budget": row["budget"],
            "total_cost": row["total_cost"],
            "style": row["style"],
            "itinerary": itin_data,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    finally:
        conn.close()


def delete_itinerary_db(user_id: int, itinerary_id: int, db_path: Optional[str] = None) -> bool:
    """Deletes an itinerary with ownership verification."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM itineraries WHERE id = ? AND user_id = ?;",
                (itinerary_id, user_id)
            )
            return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


# ============================================================
# TRIP HISTORY (USER SPECIFIC)
# ============================================================

def get_trip_history(user_id: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all trip history records for a user."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, destination, starting_location, days, travelers,
                   budget, total_cost, style, status, itinerary_summary_json, created_at
            FROM trip_history
            WHERE user_id = ?
            ORDER BY created_at DESC;
            """,
            (user_id,)
        )
        results = []
        for row in cursor.fetchall():
            summary = {}
            try:
                summary = json.loads(row["itinerary_summary_json"] or "{}")
            except Exception:
                pass
            results.append({
                "id": row["id"],
                "destination": row["destination"],
                "starting_location": row["starting_location"],
                "days": row["days"],
                "travelers": row["travelers"],
                "budget": row["budget"],
                "total_cost": row["total_cost"],
                "style": row["style"],
                "status": row["status"],
                "summary": summary,
                "created_at": row["created_at"]
            })
        return results
    finally:
        conn.close()


def add_trip_history_entry(
    user_id: int,
    destination: str,
    starting_location: str = "",
    days: int = 7,
    travelers: int = 1,
    budget: int = 80000,
    total_cost: int = 0,
    style: str = "Relaxed",
    status: str = "planned",
    summary: Optional[Dict[str, Any]] = None,
    db_path: Optional[str] = None
) -> Optional[int]:
    """Adds a trip record to user's history."""
    conn = get_connection(db_path)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO trip_history (user_id, destination, starting_location, days,
                                         travelers, budget, total_cost, style, status,
                                         itinerary_summary_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    user_id, destination.strip(), starting_location.strip(), days,
                    travelers, budget, total_cost, style, status,
                    json.dumps(summary or {}), now_iso
                )
            )
            return cursor.lastrowid
    except Exception:
        return None
    finally:
        conn.close()


def delete_trip_history_entry(user_id: int, history_id: int, db_path: Optional[str] = None) -> bool:
    """Deletes a trip history entry with ownership verification."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM trip_history WHERE id = ? AND user_id = ?;",
                (history_id, user_id)
            )
            return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()
