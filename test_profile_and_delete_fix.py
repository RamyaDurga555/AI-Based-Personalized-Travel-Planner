"""
Automated Test Suite: Profile Updates and Saved Place Removal Verification
Validates:
1. Profile updates (display name, travel style, budget, language, favourite destinations, travel interests).
2. Saved place removal by primary key ID and authenticated user ID.
3. Strict cross-user isolation and ownership enforcement (User A cannot delete User B's places).
4. Persistence across logout/login, page re-initialization, and seed_demo_account reruns.
5. Demo traveler modification persistence without default overwrite.
"""

import unittest
import os
import tempfile
import database


class TestProfileUpdatesAndSavedPlaceRemoval(unittest.TestCase):

    def setUp(self):
        # Create a dedicated temporary database file for isolation
        self.tmp_fd, self.tmp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.tmp_fd)
        database.init_db(self.tmp_db_path)

    def tearDown(self):
        if os.path.exists(self.tmp_db_path):
            try:
                os.remove(self.tmp_db_path)
            except Exception:
                pass

    def test_01_profile_updates_and_summary_reflection(self):
        """Test updating all profile fields and confirming they are saved and retrievable."""
        ok, msg, user = database.create_user("traveler1@example.com", "Password123!", "Original Name", db_path=self.tmp_db_path)
        self.assertTrue(ok)
        u_id = user["id"]

        # Update profile with comprehensive fields
        up_ok, up_msg = database.update_user_profile(
            u_id,
            display_name="Elena Rostova",
            preferred_travel_style="Fast-Paced",
            budget_preference=150000,
            favourite_destinations=["Japan", "France", "Switzerland"],
            travel_interests=["Photography", "Adventure", "Food"],
            preferred_language="French",
            db_path=self.tmp_db_path
        )
        self.assertTrue(up_ok)

        # Update user preferences
        pref_ok, _ = database.update_user_preferences(
            u_id,
            budget=150000,
            style="Fast-Paced",
            interests=["Photography", "Adventure", "Food"],
            db_path=self.tmp_db_path
        )
        self.assertTrue(pref_ok)

        # Retrieve profile summary and user record
        profile = database.get_user_profile(u_id, db_path=self.tmp_db_path)
        user_rec = database.get_user_by_id(u_id, db_path=self.tmp_db_path)
        prefs = database.get_user_preferences(u_id, db_path=self.tmp_db_path)

        # Verify all updated values
        self.assertEqual(user_rec["display_name"], "Elena Rostova")
        self.assertEqual(profile["display_name"], "Elena Rostova")
        self.assertEqual(profile["preferred_travel_style"], "Fast-Paced")
        self.assertEqual(profile["budget_preference"], 150000)
        self.assertEqual(profile["favourite_destinations"], ["Japan", "France", "Switzerland"])
        self.assertEqual(profile["travel_interests"], ["Photography", "Adventure", "Food"])
        self.assertEqual(profile["preferred_language"], "French")
        self.assertEqual(prefs["budget"], 150000)
        self.assertEqual(prefs["style"], "Fast-Paced")
        self.assertEqual(prefs["interests"], ["Photography", "Adventure", "Food"])

    def test_02_saved_place_removal_by_id_and_count_decrement(self):
        """Test deleting a saved place by primary key ID and checking immediate count decrement."""
        ok, _, user = database.create_user("place_user@example.com", "Password123!", "Place User", db_path=self.tmp_db_path)
        self.assertTrue(ok)
        u_id = user["id"]

        # Add 3 saved places
        database.save_place_db(u_id, {"name": "Place One", "country": "Japan", "category": "Shrine"}, db_path=self.tmp_db_path)
        database.save_place_db(u_id, {"name": "Place Two", "country": "France", "category": "Museum"}, db_path=self.tmp_db_path)
        database.save_place_db(u_id, {"name": "Place Three", "country": "Italy", "category": "Plaza"}, db_path=self.tmp_db_path)

        places = database.get_saved_places(u_id, db_path=self.tmp_db_path)
        self.assertEqual(len(places), 3)

        # Target place two for removal by ID
        place_two = next(p for p in places if p["name"] == "Place Two")
        target_id = place_two["id"]
        self.assertIsNotNone(target_id)

        # Delete by ID
        del_result = database.delete_saved_place_by_id(u_id, target_id, db_path=self.tmp_db_path)
        self.assertTrue(del_result)

        # Verify count decreased to 2 and place is gone
        remaining = database.get_saved_places(u_id, db_path=self.tmp_db_path)
        self.assertEqual(len(remaining), 2)
        remaining_names = [p["name"] for p in remaining]
        self.assertNotIn("Place Two", remaining_names)
        self.assertIn("Place One", remaining_names)
        self.assertIn("Place Three", remaining_names)

        # Deleting again should return False
        self.assertFalse(database.delete_saved_place_by_id(u_id, target_id, db_path=self.tmp_db_path))

    def test_03_ownership_enforcement_cross_user_isolation(self):
        """Ensure User A CANNOT delete User B's saved places."""
        ok1, _, user1 = database.create_user("user1@example.com", "Password123!", "User One", db_path=self.tmp_db_path)
        ok2, _, user2 = database.create_user("user2@example.com", "Password123!", "User Two", db_path=self.tmp_db_path)
        self.assertTrue(ok1 and ok2)

        # User 1 saves a place
        database.save_place_db(user1["id"], {"name": "User 1 Secret Spot", "country": "Norway"}, db_path=self.tmp_db_path)
        u1_places = database.get_saved_places(user1["id"], db_path=self.tmp_db_path)
        self.assertEqual(len(u1_places), 1)
        u1_place_id = u1_places[0]["id"]

        # User 2 attempts to delete User 1's place using its ID
        hack_attempt = database.delete_saved_place_by_id(user2["id"], u1_place_id, db_path=self.tmp_db_path)
        self.assertFalse(hack_attempt)

        # Verify User 1's place is completely untouched
        u1_places_after = database.get_saved_places(user1["id"], db_path=self.tmp_db_path)
        self.assertEqual(len(u1_places_after), 1)
        self.assertEqual(u1_places_after[0]["name"], "User 1 Secret Spot")

    def test_04_multi_user_profile_isolation(self):
        """Ensure updates to User 1's profile do not modify User 2's profile."""
        _, _, user1 = database.create_user("alice@example.com", "Password123!", "Alice", db_path=self.tmp_db_path)
        _, _, user2 = database.create_user("bob@example.com", "Password123!", "Bob", db_path=self.tmp_db_path)

        database.update_user_profile(
            user1["id"],
            display_name="Alice Explorer",
            preferred_travel_style="Luxury & Comfort",
            budget_preference=350000,
            db_path=self.tmp_db_path
        )

        p1 = database.get_user_profile(user1["id"], db_path=self.tmp_db_path)
        p2 = database.get_user_profile(user2["id"], db_path=self.tmp_db_path)

        self.assertEqual(p1["display_name"], "Alice Explorer")
        self.assertEqual(p1["preferred_travel_style"], "Luxury & Comfort")
        self.assertEqual(p1["budget_preference"], 350000)

        # Bob's profile should remain intact and untouched
        self.assertEqual(p2["display_name"], "Bob")
        self.assertEqual(p2["preferred_travel_style"], "Relaxed")
        self.assertEqual(p2["budget_preference"], 80000)

    def test_05_demo_account_persistence_without_startup_overwrite(self):
        """Ensure demo account edits persist across repeated seed_demo_account calls."""
        # Initial seed
        seed_res = database.seed_demo_account(db_path=self.tmp_db_path)
        demo_id = seed_res["id"]

        # Modify demo user profile and preferences
        database.update_user_profile(
            demo_id,
            display_name="Alex Custom Traveler",
            preferred_travel_style="Cultural & Deep-Dive",
            budget_preference=220000,
            favourite_destinations=["Nepal", "India"],
            travel_interests=["Architecture", "Heritage"],
            preferred_language="Hindi",
            db_path=self.tmp_db_path
        )
        database.update_user_preferences(
            demo_id,
            budget=220000,
            style="Cultural & Deep-Dive",
            interests=["Architecture", "Heritage"],
            db_path=self.tmp_db_path
        )

        # Remove 1 saved place from demo user
        demo_places = database.get_saved_places(demo_id, db_path=self.tmp_db_path)
        orig_count = len(demo_places)
        self.assertGreater(orig_count, 0)
        del_target = demo_places[0]
        del_ok = database.delete_saved_place_by_id(demo_id, del_target["id"], db_path=self.tmp_db_path)
        self.assertTrue(del_ok)
        self.assertEqual(len(database.get_saved_places(demo_id, db_path=self.tmp_db_path)), orig_count - 1)

        # Simulate app restarts by repeatedly running seed_demo_account()
        for _ in range(3):
            database.seed_demo_account(db_path=self.tmp_db_path, force_reset=False)

        # Verify demo modifications were NOT overwritten!
        prof_after = database.get_user_profile(demo_id, db_path=self.tmp_db_path)
        prefs_after = database.get_user_preferences(demo_id, db_path=self.tmp_db_path)
        places_after = database.get_saved_places(demo_id, db_path=self.tmp_db_path)

        self.assertEqual(prof_after["display_name"], "Alex Custom Traveler")
        self.assertEqual(prof_after["preferred_travel_style"], "Cultural & Deep-Dive")
        self.assertEqual(prof_after["budget_preference"], 220000)
        self.assertEqual(prof_after["favourite_destinations"], ["Nepal", "India"])
        self.assertEqual(prof_after["travel_interests"], ["Architecture", "Heritage"])
        self.assertEqual(prof_after["preferred_language"], "Hindi")
        self.assertEqual(prefs_after["budget"], 220000)
        self.assertEqual(prefs_after["style"], "Cultural & Deep-Dive")
        self.assertEqual(len(places_after), orig_count - 1)
        self.assertNotIn(del_target["name"], [p["name"] for p in places_after])


if __name__ == "__main__":
    unittest.main()
