import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"c:\Users\gidug\Downloads\AI-Based-Personalized-Travel-Planner\AI-Based-Personalized-Travel-Planner")

print("==================================================")
print("TESTING REDESIGN REQUIREMENTS VERIFICATION")
print("==================================================")

# 1. Test Nepal data
from country_data import get_country_knowledge, get_attractions, get_food, get_culture, get_transportation, answer_travel_question
nepal_k = get_country_knowledge("Nepal")
print(f"Nepal Flag: {nepal_k['flag']}")
nepal_att_names = [a[0] if isinstance(a, (tuple, list)) else a['name'] for a in nepal_k['attractions']]
print(f"Nepal Attractions: {nepal_att_names}")
assert any("Everest" in a for a in nepal_att_names), "Everest must be in Nepal attractions"
assert any("Pashupatinath" in a for a in nepal_att_names), "Pashupatinath must be in Nepal attractions"
assert any("Boudhanath" in a for a in nepal_att_names), "Boudhanath must be in Nepal attractions"
assert any("Phewa" in a for a in nepal_att_names), "Phewa Lake must be in Nepal attractions"

nepal_food_names = [f[0] if isinstance(f, (tuple, list)) else f['name'] for f in nepal_k['food']]
print(f"Nepal Food: {nepal_food_names}")
assert any("Momo" in f for f in nepal_food_names), "Momo must be in Nepal food"
assert any("Dal Bhat" in f for f in nepal_food_names), "Dal Bhat must be in Nepal food"
assert any("Thukpa" in f for f in nepal_food_names), "Thukpa must be in Nepal food"
assert any("Sel Roti" in f for f in nepal_food_names), "Sel Roti must be in Nepal food"
print("✓ Nepal attractions and food verified!")

# 2. Test India and J&K
india_k = get_country_knowledge("India")
india_att_names = [a[0] if isinstance(a, (tuple, list)) else a['name'] for a in india_k['attractions']]
print(f"\nIndia Attractions ({len(india_att_names)}): {india_att_names}")
required_jk = [
    "Dal Lake",
    "Gulmarg",
    "Pahalgam",
    "Sonamarg",
    "Mughal Gardens",
    "Shankaracharya Temple"
]
for req in required_jk:
    assert any(req.lower() in a.lower() for a in india_att_names), f"Missing {req} in India attractions"
print("✓ All 7 Jammu & Kashmir required destinations verified for India!")

india_food_names = [f[0] if isinstance(f, (tuple, list)) else f['name'] for f in india_k['food']]
print(f"India Food: {india_food_names}")
assert any("Biryani" in f for f in india_food_names)
assert any("Dosa" in f for f in india_food_names)
assert any("Butter Chicken" in f for f in india_food_names)
assert any("Samosa" in f for f in india_food_names)
assert any("Rogan Josh" in f for f in india_food_names)
print("✓ India food verified!")

# 3. Test 30-day itinerary generation
from planner import generate_itinerary
test_countries = ["India", "Japan", "Nepal", "France", "Italy", "United States", "Australia"]
for c in test_countries:
    plan = generate_itinerary("New York", c, 30, 2, 100000, ["Culture", "Food"], "Relaxed")
    assert len(plan["days"]) == 30, f"Expected 30 days for {c}, got {len(plan['days'])}"
    assert plan["total_cost"] > 0
    assert "budget" in plan
    # Ensure no empty days
    for d in plan["days"]:
        assert len(d["activities"]) >= 1, f"Empty activities on day {d['day']} for {c}"
print("✓ 30-day itinerary generation verified for India, Japan, Nepal, France, Italy, USA, Australia!")

# 4. Test app.py functions
import app
prof_japan = app.get_country_profile("Japan")
assert prof_japan["capital"] == "Tokyo"
assert prof_japan["flag"] == "🇯🇵"

prof_india = app.get_country_profile("India")
assert prof_india["capital"] == "New Delhi"
assert prof_india["flag"] == "🇮🇳"

prof_nepal = app.get_country_profile("Nepal")
assert prof_nepal["capital"] == "Kathmandu"
assert prof_nepal["flag"] == "🇳🇵"

# Test globe generation
globe_nepal = app.create_globe("Nepal")
assert globe_nepal is not None
globe_india = app.create_globe("India")
assert globe_india is not None
globe_japan = app.create_globe("Japan")
assert globe_japan is not None
print("✓ 3D Globe generation verified for Japan, India, Nepal!")

# Test tourist cards
cards_india = app.get_tourist_cards("India")
assert len(cards_india) >= 6
card_names_india = [c["name"] for c in cards_india]
print(f"\nTourist cards for India ({len(cards_india)}): {card_names_india}")
assert any("Dal Lake" in n for n in card_names_india)
assert any("Gulmarg" in n for n in card_names_india)
assert any("Pahalgam" in n for n in card_names_india)
assert any("Sonamarg" in n for n in card_names_india)
assert any("Mughal Gardens" in n for n in card_names_india)
assert any("Shankaracharya" in n for n in card_names_india)
print("✓ Tourist place cards for India include all J&K locations!")

cards_nepal = app.get_tourist_cards("Nepal")
assert len(cards_nepal) >= 6
card_names_nepal = [c["name"] for c in cards_nepal]
print(f"Tourist cards for Nepal ({len(cards_nepal)}): {card_names_nepal}")
assert any("Everest" in n for n in card_names_nepal)
assert any("Pashupatinath" in n for n in card_names_nepal)
print("✓ Tourist place cards for Nepal include Everest & Pashupatinath!")

# 5. Check no deprecated use_container_width
with open(r"c:\Users\gidug\Downloads\AI-Based-Personalized-Travel-Planner\AI-Based-Personalized-Travel-Planner\app.py", "r", encoding="utf-8") as f:
    app_text = f.read()
assert "use_container_width" not in app_text, "app.py still has use_container_width"
print("✓ Zero use_container_width in app.py!")

print("\n==================================================")
print("ALL REDESIGN VERIFICATION TESTS PASSED SUCCESSFULLY!")
print("==================================================")
