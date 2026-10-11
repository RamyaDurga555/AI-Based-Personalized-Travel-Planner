"""
Automated Unit Tests for Database and Authentication System
Tests User Registration, Duplicate Prevention, Password Hashing, Login,
Profile Updates, Preferences, Saved Places, Itineraries, Trip History,
Multi-user Data Isolation, and Safe Database Re-initialization.
"""

import os
import unittest
import tempfile
import json
import sqlite3

# Ensure local imports work
import sys
_test_dir = os.path.dirname(os.path.abspath(__file__))
if _test_dir not in sys.path:
    sys.path.insert(0, _test_dir)

import database


class TestDatabaseAndAuth(unittest.TestCase):

    def setUp(self):
        # Use a fresh temporary SQLite database for each test
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)
        database.init_db(self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except Exception:
                pass

    def test_01_init_db_creates_all_tables(self):
        """Verify that all 7 required tables are created in the database."""
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        required_tables = {
            "users",
            "user_profiles",
            "saved_places",
            "itineraries",
            "itinerary_stops",
            "travel_preferences",
            "trip_history"
        }
        for tbl in required_tables:
            self.assertIn(tbl, tables, f"Expected table '{tbl}' to exist.")

    def test_02_reinitialization_preserves_data(self):
        """Verify that re-initializing the database does NOT delete existing user data."""
        ok, msg, user = database.create_user(
            "persistent@test.com", "SecretPass123", "Persistent User", db_path=self.temp_db_path
        )
        self.assertTrue(ok)
        self.assertIsNotNone(user)

        # Call init_db again
        database.init_db(self.temp_db_path)

        # Verify user still exists
        loaded = database.get_user_by_id(user["id"], db_path=self.temp_db_path)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["email"], "persistent@test.com")

    def test_03_registration_success_and_password_hashing(self):
        """Test successful registration and ensure password is never stored in plain text."""
        ok, msg, user = database.create_user(
            "alice@example.com", "MySecurePassword2026", "Alice Wonderland", db_path=self.temp_db_path
        )
        self.assertTrue(ok)
        self.assertEqual(user["email"], "alice@example.com")
        self.assertEqual(user["display_name"], "Alice Wonderland")
        self.assertNotIn("password", user)
        self.assertNotIn("password_hash", user)

        # Inspect raw row in database to ensure hashing
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE id = ?;", (user["id"],))
        stored_hash = cursor.fetchone()[0]
        conn.close()

        self.assertNotEqual(stored_hash, "MySecurePassword2026")
        self.assertTrue(stored_hash.startswith("$2b$") or stored_hash.startswith("pbkdf2:"))

    def test_04_duplicate_registration_rejected(self):
        """Verify duplicate email registration is rejected."""
        ok1, msg1, _ = database.create_user(
            "bob@example.com", "Password123", "Bob Original", db_path=self.temp_db_path
        )
        self.assertTrue(ok1)

        ok2, msg2, user2 = database.create_user(
            "bob@example.com", "DifferentPass456", "Bob Duplicate", db_path=self.temp_db_path
        )
        self.assertFalse(ok2)
        self.assertIsNone(user2)
        self.assertIn("already exists", msg2.lower())

        # Also case-insensitive check
        ok3, _, _ = database.create_user(
            "BOB@EXAMPLE.COM", "AnotherPass789", "Bob Caps", db_path=self.temp_db_path
        )
        self.assertFalse(ok3)

    def test_05_invalid_registration_fields(self):
        """Verify validation for empty names, invalid emails, and short passwords."""
        # Empty display name
        ok, msg, _ = database.create_user("test@example.com", "Pass1234", "", db_path=self.temp_db_path)
        self.assertFalse(ok)

        # Invalid email format
        ok, msg, _ = database.create_user("not-an-email", "Pass1234", "Name", db_path=self.temp_db_path)
        self.assertFalse(ok)

        # Password too short (< 6)
        ok, msg, _ = database.create_user("valid@example.com", "12345", "Name", db_path=self.temp_db_path)
        self.assertFalse(ok)

    def test_06_authentication_success_and_failure(self):
        """Verify login credentials check and generic error messages."""
        database.create_user(
            "charlie@test.com", "CorrectPassword123", "Charlie Brown", db_path=self.temp_db_path
        )

        # Correct login
        ok, msg, user = database.authenticate_user(
            "charlie@test.com", "CorrectPassword123", db_path=self.temp_db_path
        )
        self.assertTrue(ok)
        self.assertEqual(user["display_name"], "Charlie Brown")

        # Case-insensitive email login
        ok_caps, _, _ = database.authenticate_user(
            "CHARLIE@TEST.COM", "CorrectPassword123", db_path=self.temp_db_path
        )
        self.assertTrue(ok_caps)

        # Wrong password
        ok_wrong, msg_wrong, user_wrong = database.authenticate_user(
            "charlie@test.com", "WrongPassword999", db_path=self.temp_db_path
        )
        self.assertFalse(ok_wrong)
        self.assertIsNone(user_wrong)
        self.assertEqual(msg_wrong, "Invalid email or password.")

        # Nonexistent email
        ok_none, msg_none, user_none = database.authenticate_user(
            "unknown@test.com", "AnyPassword", db_path=self.temp_db_path
        )
        self.assertFalse(ok_none)
        self.assertIsNone(user_none)
        self.assertEqual(msg_none, "Invalid email or password.")

    def test_07_demo_account_seeding(self):
        """Verify demo account creation and pre-seeded contents."""
        demo = database.seed_demo_account(db_path=self.temp_db_path)
        self.assertIn("email", demo)
        self.assertIn("password", demo)

        # Verify demo user can authenticate
        ok, msg, user = database.authenticate_user(demo["email"], demo["password"], db_path=self.temp_db_path)
        self.assertTrue(ok)

        # Verify demo saved places exist
        places = database.get_saved_places(user["id"], db_path=self.temp_db_path)
        self.assertGreater(len(places), 0)

        # Verify demo itineraries exist
        itins = database.get_user_itineraries(user["id"], db_path=self.temp_db_path)
        self.assertGreater(len(itins), 0)

    def test_08_profile_updates_and_persistence(self):
        """Verify updating and persisting user profile data."""
        _, _, user = database.create_user("diana@test.com", "Pass123456", "Diana Prince", db_path=self.temp_db_path)
        u_id = user["id"]

        # Initial profile
        prof = database.get_user_profile(u_id, db_path=self.temp_db_path)
        self.assertEqual(prof["preferred_travel_style"], "Relaxed")

        # Update profile
        ok, msg = database.update_user_profile(
            u_id,
            display_name="Princess Diana",
            preferred_travel_style="Luxury & Comfort",
            budget_preference=150000,
            favourite_destinations=["Japan", "France", "Greece"],
            travel_interests=["Culture", "Architecture", "Fine Dining"],
            preferred_language="French",
            db_path=self.temp_db_path
        )
        self.assertTrue(ok)

        # Reload and check
        updated = database.get_user_profile(u_id, db_path=self.temp_db_path)
        self.assertEqual(updated["display_name"], "Princess Diana")
        self.assertEqual(updated["preferred_travel_style"], "Luxury & Comfort")
        self.assertEqual(updated["budget_preference"], 150000)
        self.assertEqual(updated["favourite_destinations"], ["Japan", "France", "Greece"])
        self.assertEqual(updated["travel_interests"], ["Culture", "Architecture", "Fine Dining"])
        self.assertEqual(updated["preferred_language"], "French")

    def test_09_saved_places_toggle_and_clear(self):
        """Verify saving, toggling, and clearing saved places."""
        _, _, user = database.create_user("eve@test.com", "Pass123456", "Eve", db_path=self.temp_db_path)
        u_id = user["id"]

        place = {"name": "Tokyo Tower", "country": "Japan", "category": "Observation", "description": "Iconic tower"}

        # 1. First toggle saves
        is_saved = database.toggle_save_place_db(u_id, place, db_path=self.temp_db_path)
        self.assertTrue(is_saved)
        self.assertTrue(database.is_place_saved_db(u_id, "Tokyo Tower", "Japan", db_path=self.temp_db_path))

        # 2. Second toggle removes
        is_saved_again = database.toggle_save_place_db(u_id, place, db_path=self.temp_db_path)
        self.assertFalse(is_saved_again)
        self.assertFalse(database.is_place_saved_db(u_id, "Tokyo Tower", "Japan", db_path=self.temp_db_path))

        # 3. Add two places and clear
        database.save_place_db(u_id, {"name": "Place 1", "country": "India"}, db_path=self.temp_db_path)
        database.save_place_db(u_id, {"name": "Place 2", "country": "India"}, db_path=self.temp_db_path)
        self.assertEqual(len(database.get_saved_places(u_id, db_path=self.temp_db_path)), 2)

        database.clear_saved_places_db(u_id, db_path=self.temp_db_path)
        self.assertEqual(len(database.get_saved_places(u_id, db_path=self.temp_db_path)), 0)

    def test_10_itineraries_save_retrieve_and_delete(self):
        """Verify saving itineraries, relational stops, trip history logging, and deletion."""
        _, _, user = database.create_user("frank@test.com", "Pass123456", "Frank", db_path=self.temp_db_path)
        u_id = user["id"]

        sample_itin = {
            "destination": "Nepal",
            "starting": "Kathmandu",
            "days": [
                {
                    "day": 1,
                    "city": "Kathmandu",
                    "title": "Day 1: Durbar Square",
                    "activities": [{"time": "10:00 AM", "activity": "Heritage walk", "cost": 500}]
                }
            ],
            "total_cost": 25000,
            "budget": {"Accommodation": 10000, "Food": 5000, "Transport": 5000, "Activities": 5000}
        }

        itin_id = database.save_itinerary_db(
            u_id, sample_itin, title="Nepal Himalayan Escape", db_path=self.temp_db_path
        )
        self.assertIsNotNone(itin_id)

        # Retrieve list
        itins = database.get_user_itineraries(u_id, db_path=self.temp_db_path)
        self.assertEqual(len(itins), 1)
        self.assertEqual(itins[0]["title"], "Nepal Himalayan Escape")
        self.assertEqual(itins[0]["destination"], "Nepal")

        # Retrieve by ID
        single = database.get_itinerary_by_id(u_id, itin_id, db_path=self.temp_db_path)
        self.assertIsNotNone(single)
        self.assertEqual(single["total_cost"], 25000)

        # Trip history was automatically logged
        history = database.get_trip_history(u_id, db_path=self.temp_db_path)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["destination"], "Nepal")

        # Delete itinerary
        deleted = database.delete_itinerary_db(u_id, itin_id, db_path=self.temp_db_path)
        self.assertTrue(deleted)
        self.assertIsNone(database.get_itinerary_by_id(u_id, itin_id, db_path=self.temp_db_path))

    def test_11_multi_user_data_isolation(self):
        """Verify that two different users cannot access or modify each other's data."""
        _, _, user_a = database.create_user("user_a@test.com", "Pass123456", "User A", db_path=self.temp_db_path)
        _, _, user_b = database.create_user("user_b@test.com", "Pass123456", "User B", db_path=self.temp_db_path)

        # User A saves place A
        database.save_place_db(user_a["id"], {"name": "Colosseum", "country": "Italy"}, db_path=self.temp_db_path)
        # User B saves place B
        database.save_place_db(user_b["id"], {"name": "Taj Mahal", "country": "India"}, db_path=self.temp_db_path)

        # User A should only see Colosseum
        places_a = database.get_saved_places(user_a["id"], db_path=self.temp_db_path)
        self.assertEqual(len(places_a), 1)
        self.assertEqual(places_a[0]["name"], "Colosseum")

        # User B should only see Taj Mahal
        places_b = database.get_saved_places(user_b["id"], db_path=self.temp_db_path)
        self.assertEqual(len(places_b), 1)
        self.assertEqual(places_b[0]["name"], "Taj Mahal")

        # User A creates an itinerary
        sample_itin = {"destination": "Italy", "days": [], "total_cost": 50000}
        itin_id_a = database.save_itinerary_db(user_a["id"], sample_itin, title="Italy Trip", db_path=self.temp_db_path)

        # User B cannot access User A's itinerary
        itin_b_lookup = database.get_itinerary_by_id(user_b["id"], itin_id_a, db_path=self.temp_db_path)
        self.assertIsNone(itin_b_lookup)

        # User B cannot delete User A's itinerary
        del_attempt = database.delete_itinerary_db(user_b["id"], itin_id_a, db_path=self.temp_db_path)
        self.assertFalse(del_attempt)

        # User A's itinerary still safely exists
        itin_a_lookup = database.get_itinerary_by_id(user_a["id"], itin_id_a, db_path=self.temp_db_path)
        self.assertIsNotNone(itin_a_lookup)


if __name__ == "__main__":
    unittest.main()
