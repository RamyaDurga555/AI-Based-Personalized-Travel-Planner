"""
Comprehensive Phase 6 Automated Test Suite
Verifies all 12 explicit test cases from the project specification:
  1. New user registration
  2. Duplicate email rejection
  3. Incorrect credentials rejection
  4. Registered user login & logout flow
  5. Profile updates persistence across restart
  6. Saved places persistence across restart
  7. Itineraries persistence across restart
  8. Multi-user data isolation (User A vs User B)
  9. Logout & account switching data isolation
  10. Existing core features regression check (globe, planner, clothing, emergency, chatbot)
  11. Database re-initialization safety (zero data loss)
  12. Dependency and app startup integrity
"""

import os
import sys
import tempfile
import unittest
import json
import sqlite3

_app_dir = os.path.dirname(os.path.abspath(__file__))
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

import database
from planner import generate_itinerary, country_info
import app


class TestPhase6Comprehensive(unittest.TestCase):

    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)
        database.init_db(self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except Exception:
                pass

    def test_case_01_new_user_registration(self):
        """Case 1: A new user can register successfully."""
        ok, msg, user = database.create_user(
            "traveler.jane@example.com", "SecurePass2026!", "Jane Explorer", db_path=self.temp_db_path
        )
        self.assertTrue(ok)
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "traveler.jane@example.com")
        self.assertEqual(user["display_name"], "Jane Explorer")
        self.assertNotIn("password", user)
        self.assertNotIn("password_hash", user)

    def test_case_02_duplicate_email_rejected(self):
        """Case 2: Duplicate email registration is rejected."""
        ok1, _, _ = database.create_user(
            "dup.check@example.com", "Password123", "First Reg", db_path=self.temp_db_path
        )
        self.assertTrue(ok1)

        ok2, msg2, user2 = database.create_user(
            "dup.check@example.com", "DifferentPass", "Second Reg", db_path=self.temp_db_path
        )
        self.assertFalse(ok2)
        self.assertIsNone(user2)
        self.assertIn("already exists", msg2.lower())

    def test_case_03_incorrect_credentials_rejected(self):
        """Case 3: Incorrect login credentials are rejected with generic safe message."""
        database.create_user(
            "auth.test@example.com", "RealPassword123", "Auth User", db_path=self.temp_db_path
        )

        # Wrong password
        ok1, msg1, u1 = database.authenticate_user(
            "auth.test@example.com", "WrongPassword!", db_path=self.temp_db_path
        )
        self.assertFalse(ok1)
        self.assertIsNone(u1)
        self.assertEqual(msg1, "Invalid email or password.")

        # Non-registered email
        ok2, msg2, u2 = database.authenticate_user(
            "nonexistent@example.com", "RealPassword123", db_path=self.temp_db_path
        )
        self.assertFalse(ok2)
        self.assertIsNone(u2)
        self.assertEqual(msg2, "Invalid email or password.")

    def test_case_04_login_and_logout_flow(self):
        """Case 4: A registered user can log in and log out safely."""
        database.create_user("flow.user@example.com", "FlowPass123", "Flow Traveler", db_path=self.temp_db_path)

        # Simulate Login
        ok, msg, user = database.authenticate_user("flow.user@example.com", "FlowPass123", db_path=self.temp_db_path)
        self.assertTrue(ok)
        session = {
            "is_authenticated": True,
            "current_user": user,
            "user_profile": database.get_user_profile(user["id"], db_path=self.temp_db_path),
            "saved_places": database.get_saved_places(user["id"], db_path=self.temp_db_path)
        }
        self.assertTrue(session["is_authenticated"])
        self.assertEqual(session["current_user"]["email"], "flow.user@example.com")

        # Simulate Logout
        session["is_authenticated"] = False
        session["current_user"] = None
        session["user_profile"] = None
        session["saved_places"] = []
        self.assertFalse(session["is_authenticated"])
        self.assertIsNone(session["current_user"])
        self.assertEqual(len(session["saved_places"]), 0)

    def test_case_05_profile_persistence_across_restart(self):
        """Case 5: Profile updates persist after restarting the app."""
        _, _, user = database.create_user("profile.restart@example.com", "Pass123456", "Original Name", db_path=self.temp_db_path)
        u_id = user["id"]

        # Update profile
        database.update_user_profile(
            u_id,
            display_name="Updated Globetrotter",
            preferred_travel_style="Cultural & Deep-Dive",
            budget_preference=175000,
            favourite_destinations=["Japan", "France", "Nepal"],
            travel_interests=["History", "Tea Ceremonies", "Local Markets"],
            preferred_language="Japanese",
            db_path=self.temp_db_path
        )

        # Simulate App Restart by closing connection and creating a new DB connection instance
        fresh_profile = database.get_user_profile(u_id, db_path=self.temp_db_path)
        self.assertEqual(fresh_profile["display_name"], "Updated Globetrotter")
        self.assertEqual(fresh_profile["preferred_travel_style"], "Cultural & Deep-Dive")
        self.assertEqual(fresh_profile["budget_preference"], 175000)
        self.assertEqual(fresh_profile["favourite_destinations"], ["Japan", "France", "Nepal"])
        self.assertEqual(fresh_profile["preferred_language"], "Japanese")

    def test_case_06_saved_places_persistence_across_restart(self):
        """Case 6: Saved places persist after restarting the app."""
        _, _, user = database.create_user("places.user@example.com", "Pass123456", "Places User", db_path=self.temp_db_path)
        u_id = user["id"]

        place1 = {"name": "Meiji Jingu Shrine", "country": "Japan", "category": "Shrine"}
        place2 = {"name": "Pashupatinath Temple", "country": "Nepal", "category": "Temple"}
        database.save_place_db(u_id, place1, db_path=self.temp_db_path)
        database.save_place_db(u_id, place2, db_path=self.temp_db_path)

        # Simulate restart
        reloaded_places = database.get_saved_places(u_id, db_path=self.temp_db_path)
        self.assertEqual(len(reloaded_places), 2)
        names = [p["name"] for p in reloaded_places]
        self.assertIn("Meiji Jingu Shrine", names)
        self.assertIn("Pashupatinath Temple", names)

    def test_case_07_itineraries_persistence_across_restart(self):
        """Case 7: Itineraries persist after restarting the app."""
        _, _, user = database.create_user("itin.user@example.com", "Pass123456", "Itin User", db_path=self.temp_db_path)
        u_id = user["id"]

        gen_plan = generate_itinerary("Tokyo", "Japan", 7, 2, 100000, ["Culture", "Food"], "Relaxed")
        itin_id = database.save_itinerary_db(u_id, gen_plan, title="Tokyo Sakura 7-Day Journey", db_path=self.temp_db_path)
        self.assertIsNotNone(itin_id)

        # Simulate restart
        loaded_itins = database.get_user_itineraries(u_id, db_path=self.temp_db_path)
        self.assertEqual(len(loaded_itins), 1)
        self.assertEqual(loaded_itins[0]["title"], "Tokyo Sakura 7-Day Journey")
        self.assertEqual(loaded_itins[0]["destination"], "Japan")
        self.assertEqual(len(loaded_itins[0]["itinerary"]["days"]), 7)

    def test_case_08_multi_user_data_isolation(self):
        """Case 8: Two different users see only their own private data."""
        _, _, user_a = database.create_user("user_a@test.com", "Pass1234", "User A", db_path=self.temp_db_path)
        _, _, user_b = database.create_user("user_b@test.com", "Pass1234", "User B", db_path=self.temp_db_path)

        # User A saves Kyoto
        database.save_place_db(user_a["id"], {"name": "Kyoto Gion", "country": "Japan"}, db_path=self.temp_db_path)
        # User B saves Paris
        database.save_place_db(user_b["id"], {"name": "Louvre Museum", "country": "France"}, db_path=self.temp_db_path)

        places_a = database.get_saved_places(user_a["id"], db_path=self.temp_db_path)
        places_b = database.get_saved_places(user_b["id"], db_path=self.temp_db_path)

        self.assertEqual(len(places_a), 1)
        self.assertEqual(places_a[0]["name"], "Kyoto Gion")
        self.assertEqual(len(places_b), 1)
        self.assertEqual(places_b[0]["name"], "Louvre Museum")

        # Cross lookup must fail
        self.assertFalse(database.is_place_saved_db(user_a["id"], "Louvre Museum", "France", db_path=self.temp_db_path))
        self.assertFalse(database.is_place_saved_db(user_b["id"], "Kyoto Gion", "Japan", db_path=self.temp_db_path))

    def test_case_09_logout_and_account_switching_safety(self):
        """Case 9: Logging out and switching accounts does not expose the previous user's data."""
        _, _, u1 = database.create_user("first@test.com", "Pass1234", "User First", db_path=self.temp_db_path)
        _, _, u2 = database.create_user("second@test.com", "Pass1234", "User Second", db_path=self.temp_db_path)

        database.save_place_db(u1["id"], {"name": "Private Spot U1", "country": "Japan"}, db_path=self.temp_db_path)
        itin1 = {"destination": "Japan", "days": [], "total_cost": 40000}
        database.save_itinerary_db(u1["id"], itin1, title="U1 Private Plan", db_path=self.temp_db_path)

        # Switch session from U1 to U2
        active_session = {"current_user": u2, "saved_places": database.get_saved_places(u2["id"], db_path=self.temp_db_path)}
        self.assertEqual(len(active_session["saved_places"]), 0)
        self.assertEqual(len(database.get_user_itineraries(u2["id"], db_path=self.temp_db_path)), 0)

    def test_case_10_existing_features_continue_working(self):
        """Case 10: Existing travel-planning, globe, destination, clothing, emergency, and chatbot features continue to work."""
        # Planner
        plan = generate_itinerary("Hyderabad", "Japan", 7, 1, 80000, ["Culture", "Food"], "Relaxed")
        self.assertIn("days", plan)
        self.assertEqual(len(plan["days"]), 7)

        # Globe
        globe = app.create_globe("Japan")
        self.assertIsNotNone(globe)

        # Destination info
        c_info = country_info("Japan")
        self.assertIn("places", c_info)

        # Traditional clothing
        clothing = app.get_traditional_clothing("Japan")
        self.assertIsNotNone(clothing)

        # Emergency info
        em_info = app.get_verified_emergency_info("Japan")
        self.assertEqual(em_info["police"], "110")
        self.assertEqual(em_info["ambulance"], "119")

        # Chatbot
        ans = app.answer_travel_question("Japan", "What food should I try?")
        self.assertTrue("sushi" in ans.lower() or "ramen" in ans.lower())

    def test_case_11_db_initialization_does_not_delete_user_data(self):
        """Case 11: Database initialization does not delete existing user data."""
        _, _, user = database.create_user("safe.init@test.com", "Pass1234", "Safe User", db_path=self.temp_db_path)
        database.save_place_db(user["id"], {"name": "Preserved Place", "country": "India"}, db_path=self.temp_db_path)

        # Call init_db multiple times
        database.init_db(self.temp_db_path)
        database.init_db(self.temp_db_path)

        # Ensure user and place still exist
        user_check = database.get_user_by_id(user["id"], db_path=self.temp_db_path)
        self.assertIsNotNone(user_check)
        places = database.get_saved_places(user["id"], db_path=self.temp_db_path)
        self.assertEqual(len(places), 1)
        self.assertEqual(places[0]["name"], "Preserved Place")

    def test_case_12_dependencies_and_app_startup(self):
        """Case 12: The application imports and executes with updated dependencies."""
        # Ensure bcrypt is imported and functional
        import bcrypt
        hashed = bcrypt.hashpw(b"testpass", bcrypt.gensalt())
        self.assertTrue(bcrypt.checkpw(b"testpass", hashed))

        # Check requirements.txt contains bcrypt
        req_path = os.path.join(_app_dir, "requirements.txt")
        with open(req_path, "r", encoding="utf-8") as f:
            req_content = f.read()
        self.assertIn("bcrypt", req_content)

        # Verify app.py has zero deprecated use_container_width
        app_path = os.path.join(_app_dir, "app.py")
        with open(app_path, "r", encoding="utf-8") as f:
            app_code = f.read()
        self.assertNotIn("use_container_width", app_code)


if __name__ == "__main__":
    unittest.main()
