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
    get_images,
    generate_itinerary,
    answer_travel_question
)
import pycountry

print("============================================================")
print("COMPREHENSIVE GLOBAL SYSTEM VERIFICATION TEST")
print("============================================================")

BENCHMARK_COUNTRIES = [
    "India", "Japan", "France", "United States", "United Kingdom",
    "Australia", "Brazil", "Egypt", "South Africa", "Canada",
    "Italy", "Thailand", "Mexico", "Norway"
]

TEST_QUESTIONS = [
    "What should I pack?",
    "What food should I try?",
    "How should I get around?",
    "What are the must-see places?",
    "Is public transportation good?",
    "What cultural rules should I know?",
    "Give me a budget itinerary.",
    "What should I do for 10 days?",
    "What are some hidden places?",
    "How do I travel between these cities?",
    "What should I avoid?",
    "Give me family-friendly recommendations."
]

# 1. VERIFY JAMMU & KASHMIR RULE
print("\n--- 1. Testing Jammu & Kashmir Rule ---")
india_k = get_country_knowledge("India")
jk_city = [c for c in india_k["cities"] if "Jammu" in c or "Kashmir" in c]
print(f"Jammu & Kashmir in India cities: {jk_city}")
assert len(jk_city) > 0, "Jammu & Kashmir must be represented under India"
assert "Jammu & Kashmir" in india_k["travel_tips"]["safety"], "Jammu & Kashmir must be featured in India safety tips"

jk_country_check = [c.name for c in pycountry.countries if "kashmir" in c.name.lower()]
assert len(jk_country_check) == 0, "Jammu & Kashmir must NOT be a separate country in pycountry"
print("✓ Jammu & Kashmir verified correctly as an Indian Union Territory/region!")

# 2. VERIFY REQUIRED TOP-LEVEL FUNCTIONS FOR ALL BENCHMARKS
print("\n--- 2. Testing Required Top-Level Functions & Dynamic Data ---")
for country in BENCHMARK_COUNTRIES:
    k = get_country_knowledge(country)
    att = get_attractions(country)
    food = get_food(country)
    cult = get_culture(country)
    trans = get_transportation(country)
    tips = get_travel_tips(country)
    
    # Assertions
    assert len(att) >= 4, f"Failed attractions count for {country}"
    assert len(food) >= 3, f"Failed food count for {country}"
    assert len(cult) >= 3, f"Failed culture count for {country}"
    assert len(trans.get("modes", [])) >= 3, f"Failed transport modes for {country}"
    assert tips.get("tipping"), f"Failed tipping info for {country}"
    assert tips.get("currency_tips"), f"Failed currency info for {country}"
    assert tips.get("etiquette"), f"Failed etiquette for {country}"
    assert tips.get("best_season"), f"Failed season info for {country}"
    assert tips.get("safety"), f"Failed safety info for {country}"

    # Verify get_images includes country context
    img_meta = get_images(country, att[0]["name"])
    assert country.lower() in img_meta["query"].lower(), f"Image query missing country context: {img_meta['query']}"
    assert att[0]["name"].lower() in img_meta["query"].lower(), f"Image query missing attraction name: {img_meta['query']}"

    print(f"✓ [{country}] Flag: {k['flag']} | Cities: {len(k['cities'])} | Attractions: {len(att)} | Food: {len(food)} | Transit: {len(trans['modes'])} modes")

# 3. VERIFY 1, 7, 14, 30 DAY ITINERARIES FOR ALL BENCHMARKS
print("\n--- 3. Testing 1 to 30 Day Itineraries ---")
for country in BENCHMARK_COUNTRIES:
    for days in [1, 7, 14, 30]:
        plan = generate_itinerary(country, duration=days)
        assert len(plan["days"]) == days, f"Expected {days} days for {country}, got {len(plan['days'])}"
        for d in plan["days"]:
            assert len(d["activities"]) >= 1, f"Empty day found in {country} day {d['day']}"
            assert d["title"], f"Empty title in {country} day {d['day']}"
            for a in d["activities"]:
                assert a["activity"], f"Empty activity in {country} day {d['day']}"
                assert a["place"], f"Empty place in {country} day {d['day']}"

    cities_covered = len(set(d['title'].split(':')[0] for d in plan['days']))
    print(f"✓ [{country}] 1, 7, 14, 30 days complete! 30-day itinerary spans {cities_covered} cities/regions.")

# 4. VERIFY AI ASSISTANT ANSWERS FOR ALL 12 QUESTIONS
print("\n--- 4. Testing AI Assistant Dynamic Answers Across All 12 Questions ---")
for q in TEST_QUESTIONS:
    ans_india = answer_travel_question("India", q)
    ans_japan = answer_travel_question("Japan", q)
    ans_france = answer_travel_question("France", q)
    ans_brazil = answer_travel_question("Brazil", q)
    
    # Verify answers are grounded in the specific country and distinct
    assert "India" in ans_india, f"India answer missing 'India': {q}"
    assert "Japan" in ans_japan, f"Japan answer missing 'Japan': {q}"
    assert "France" in ans_france, f"France answer missing 'France': {q}"
    assert "Brazil" in ans_brazil, f"Brazil answer missing 'Brazil': {q}"
    assert ans_india != ans_japan, f"Answers should be country-specific, but matched for: {q}"
    print(f"✓ AI Assistant: \"{q}\" validated for multiple distinct countries.")

print("\n============================================================")
print("SUCCESS: ALL REQUIREMENTS AND 14 BENCHMARK COUNTRIES PASSED!")
print("============================================================")
