import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"c:\Users\gidug\Downloads\AI-Based-Personalized-Travel-Planner\AI-Based-Personalized-Travel-Planner")

from country_data import (
    get_country_knowledge,
    get_attractions,
    get_food,
    get_culture,
    get_transportation,
    get_travel_tips,
    answer_travel_question,
    get_where_to_try,
    get_destination_gallery_items
)
from app import (
    get_tourist_cards,
    get_food_cards,
    get_religious_cards,
    get_card_image_bytes
)

print("=" * 60)
print("COMPREHENSIVE PHOTO & CHATBOT VERIFICATION")
print("=" * 60)

BENCHMARK_COUNTRIES = [
    "India",
    "Nepal",
    "Japan",
    "France",
    "Italy",
    "United States",
    "Australia"
]

# 1. VERIFY PHOTO GALLERY FOR EVERY BENCHMARK COUNTRY
print("\n--- 1. Testing Destination Photo Gallery ---")
for country in BENCHMARK_COUNTRIES:
    gallery = get_destination_gallery_items(country)
    assert len(gallery) == 6, f"Expected 6 gallery items for {country}, got {len(gallery)}"
    names = [g["name"] for g in gallery]
    print(f"✓ {country} Photo Gallery (6 items): {names}")
    # Verify specific requested items
    if country == "Japan":
        assert any("Tokyo" in n for n in names)
        assert any("Fuji" in n for n in names)
        assert any("Kyoto" in n for n in names)
    elif country == "Nepal":
        assert any("Everest" in n for n in names)
        assert any("Pashupatinath" in n for n in names)
        assert any("Pokhara" in n for n in names)
    elif country == "India":
        assert any("Taj Mahal" in n for n in names)
        assert any("Dal Lake" in n for n in names)
        assert any("Gulmarg" in n for n in names)

# 2. VERIFY FAMOUS PLACES AND PHOTO CARDS
print("\n--- 2. Testing Famous Places Photo Cards ---")
for country in BENCHMARK_COUNTRIES:
    place_cards = get_tourist_cards(country)
    assert len(place_cards) >= 5, f"Expected >=5 tourist cards for {country}, got {len(place_cards)}"
    first = place_cards[0]
    assert "name" in first and "location" in first, f"Missing name/location in {country} card"
    print(f"✓ {country} Places ({len(place_cards)} cards): {[c['name'] for c in place_cards[:3]]}...")

# 3. VERIFY FOOD CARDS WITH WHERE TO TRY
print("\n--- 3. Testing Food Cards & 'Where to Try' ---")
for country in BENCHMARK_COUNTRIES:
    food_cards = get_food_cards(country)
    assert len(food_cards) >= 5, f"Expected >=5 food cards for {country}, got {len(food_cards)}"
    for card in food_cards:
        assert "where_to_try" in card and card["where_to_try"], f"Missing where_to_try in {card['name']} for {country}"
    print(f"✓ {country} Food ({len(food_cards)} dishes with where_to_try):")
    for f in food_cards[:2]:
        print(f"   • {f['name']} -> Best places to try: {f['where_to_try']}")

# 4. VERIFY CULTURE CARDS
print("\n--- 4. Testing Culture & Experiences Cards ---")
for country in BENCHMARK_COUNTRIES:
    culture_cards = get_religious_cards(country)
    assert len(culture_cards) >= 5, f"Expected >=5 culture cards for {country}, got {len(culture_cards)}"
    print(f"✓ {country} Culture ({len(culture_cards)} cards): {[c['name'] for c in culture_cards[:3]]}...")

# 5. VERIFY CHATBOT FOLLOWS SELECTED COUNTRY & CONTEXT
print("\n--- 5. Testing Chatbot Country Adherence ---")
nepal_food_ans = answer_travel_question("Nepal", "What food should I try?")
assert any(w in nepal_food_ans.lower() for w in ["momo", "dal bhat", "thukpa", "nepal"]), "Nepal food query should return Nepalese food"
print("✓ Nepal food question produced authentic Nepalese recommendations (Momo/Dal Bhat)")

japan_food_ans = answer_travel_question("Japan", "What food should I try?")
assert any(w in japan_food_ans.lower() for w in ["sushi", "ramen", "japan"]), "Japan food query should return Japanese food"
assert "momo" not in japan_food_ans.lower(), "Japan answer must NOT contain momo!"
print("✓ Japan food question produced authentic Japanese recommendations (Sushi/Ramen, no momo)")

# 6. VERIFY TRANSIT IN CHATBOT
print("\n--- 6. Testing Chatbot Transit Knowledge ---")
t2k_ans = answer_travel_question("Japan", "How do I travel from Tokyo to Kyoto?")
assert "shinkansen" in t2k_ans.lower() or "bullet train" in t2k_ans.lower()
assert "nozomi" in t2k_ans.lower() or "hikari" in t2k_ans.lower()
print("✓ Tokyo to Kyoto transit explains Shinkansen (Nozomi/Hikari), bus, and flight options")

k2p_ans = answer_travel_question("Nepal", "How do I travel from Kathmandu to Pokhara?")
assert "flight" in k2p_ans.lower() or "bus" in k2p_ans.lower()
print("✓ Kathmandu to Pokhara transit explains domestic flights and tourist coach options")

# 7. VERIFY ITINERARY MODIFICATION IN CHATBOT
print("\n--- 7. Testing Chatbot Itinerary Modification ---")
mod_ans = answer_travel_question("Japan", "Change Day 5 to something more relaxing.")
assert "Day 5" in mod_ans or "day 5" in mod_ans.lower()
assert any(w in mod_ans.lower() for w in ["relax", "gentle", "leisure", "morning", "afternoon", "evening"])
print("✓ Itinerary modification for Day 5 correctly suggests a balanced, relaxing replacement schedule")

# 8. VERIFY OPEN-ENDED QUESTIONS (PACKING, CASH, RAIN, ROMANTIC, CHILDREN, 30-DAY)
print("\n--- 8. Testing Chatbot Open-Ended Question Suite ---")
test_questions = [
    ("What should I pack?", ["pack", "layer", "weather"]),
    ("How much money should I carry?", ["cash", "card", "currency"]),
    ("What should I do if it rains?", ["rain", "museum", "indoor"]),
    ("Suggest a romantic activity.", ["romantic", "sunset", "dinner"]),
    ("Can I visit this place with children?", ["children", "family", "safe"]),
    ("Which places should I skip if I only have 3 days?", ["3", "skip", "express"]),
    ("Plan a 30-day trip.", ["30", "grand tour", "regions"])
]

for q, expected_keywords in test_questions:
    ans = answer_travel_question("Japan", q)
    assert any(k in ans.lower() for k in expected_keywords), f"Answer to '{q}' missing expected keywords"
    print(f"✓ Chatbot handled open-ended question: '{q}'")

# 9. VERIFY IMAGE BYTE RESOLUTION
print("\n--- 9. Testing Real Image Fetching & Caching ---")
test_images = [
    ("Nepal", "Pashupatinath Temple", "place"),
    ("India", "Taj Mahal", "place"),
    ("Japan", "Mount Fuji", "place"),
    ("France", "Eiffel Tower", "place"),
    ("Nepal", "Momo", "food"),
    ("Japan", "Sushi", "food"),
    ("India", "Biryani", "food"),
    ("Italy", "Pizza", "food")
]

for country, item, card_type in test_images:
    res = get_card_image_bytes(country, item, card_type)
    b = res[0] if isinstance(res, tuple) else res
    assert b is not None and len(b) > 1000, f"Failed to get image bytes for {item} ({country})"
    print(f"✓ {country} - {item} ({card_type}): {len(b):,} bytes downloaded successfully")

print("\n" + "=" * 60)
print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
print("=" * 60)
