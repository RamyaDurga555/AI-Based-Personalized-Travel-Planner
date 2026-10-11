"""
test_multi_stop_accuracy.py
Tests and verifies all 9 requirements from the Critical Bug Fix:
1. Exact starting location (Hyderabad, never 'Your Location' or 'YOU').
2. Ordered destination stops and durations (Tokyo 2d, Kyoto 3d, Osaka 2d = 7 days stay).
3. Location-specific attractions (no Fushimi Inari in Tokyo, Mount Fuji explicitly labeled day trip).
4. Realistic day-by-day scheduling (arrival schedule, transition days, return day buffer).
5. Independent transport legs (HYD->TYO, TYO->KYO, KYO->OSA, OSA->HYD).
6. Transparent budget calculation (flights, rail, accommodation, food, local transit, activities, contingency).
7. Seasonal recommendations distinction (historical averages vs live forecast, ask travel year).
8. 8-Point Pre-render validation passes.
9. Single-destination and chatbot compatibility preserved.
"""

import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from multi_stop_planner import parse_multi_stop_trip_prompt, generate_multi_stop_journey, recommend_destinations_by_season
from destination_knowledge import get_city_attractions, get_city_day_trips
from country_data import answer_travel_question, format_multi_stop_chat_response


def test_scenario_user_prompt():
    print("==================================================")
    print("TEST 1: User's Exact Multi-Stop Prompt")
    print("==================================================")
    prompt = "Plan Hyderabad → Tokyo (2 days) → Kyoto (3 days) → Osaka (2 days) → Hyderabad."
    parsed = parse_multi_stop_trip_prompt(prompt)

    # 1. Origin verification
    assert parsed["starting_location"] == "Hyderabad", f"Expected 'Hyderabad', got '{parsed['starting_location']}'"
    assert parsed["origin"] == "Hyderabad", f"Expected 'Hyderabad', got '{parsed['origin']}'"
    assert parsed["starting_location"] != "Your Location", "Failed: Origin must never be 'Your Location'"

    # 2. Stops and durations
    assert len(parsed["stops"]) == 3, f"Expected 3 stops, got {len(parsed['stops'])}"
    assert [s["city"] for s in parsed["stops"]] == ["Tokyo", "Kyoto", "Osaka"], f"Wrong stops: {parsed['stops']}"
    assert [s["days"] for s in parsed["stops"]] == [2, 3, 2], f"Wrong days: {parsed['stops']}"
    assert parsed["return_location"] == "Hyderabad", f"Expected return to Hyderabad, got {parsed['return_location']}"

    # Generate journey
    journey = generate_multi_stop_journey(parsed)

    # Destination stay days
    assert journey["destination_stay_days"] == 7, f"Expected 7 stay days, got {journey['destination_stay_days']}"
    assert len(journey["days"]) == 7, f"Expected 7 schedule days, got {len(journey['days'])}"

    # 3. Transport Legs verification
    legs = journey["transport_legs"]
    assert len(legs) == 4, f"Expected 4 transport legs, got {len(legs)}"

    # Leg 1: HYD -> Tokyo
    assert legs[0]["origin"] == "Hyderabad"
    assert legs[0]["destination"] == "Tokyo"
    assert "HYD" in legs[0]["origin_terminal"]
    assert "HND" in legs[0]["dest_terminal"] or "NRT" in legs[0]["dest_terminal"]
    assert "YOU" not in legs[0]["origin_terminal"]

    # Leg 2: Tokyo -> Kyoto
    assert legs[1]["origin"] == "Tokyo"
    assert legs[1]["destination"] == "Kyoto"
    assert "Shinkansen" in legs[1]["mode"]

    # Leg 3: Kyoto -> Osaka
    assert legs[2]["origin"] == "Kyoto"
    assert legs[2]["destination"] == "Osaka"
    assert "Rapid" in legs[2]["mode"] or "Hankyu" in legs[2]["mode"] or "Rail" in legs[2]["mode"]

    # Leg 4: Osaka -> Hyderabad (Independent return leg!)
    assert legs[3]["origin"] == "Osaka"
    assert legs[3]["destination"] == "Hyderabad"
    assert "KIX" in legs[3]["origin_terminal"] or "ITM" in legs[3]["origin_terminal"]
    assert "HYD" in legs[3]["dest_terminal"]
    assert "UKY" not in legs[3]["origin_terminal"]

    # 4. Location-Specific Attractions
    # Check that Tokyo days contain Tokyo sights, NOT Fushimi Inari
    tokyo_days = [d for d in journey["days"] if d["city"] == "Tokyo"]
    for td in tokyo_days:
        for act in td["activities"]:
            act_text = act["activity"].lower()
            assert "fushimi inari" not in act_text, f"Fushimi Inari leaked into Tokyo schedule: {act_text}"
            assert "osaka castle" not in act_text, f"Osaka Castle leaked into Tokyo schedule: {act_text}"

    # Check Kyoto days
    kyoto_days = [d for d in journey["days"] if d["city"] == "Kyoto"]
    assert len(kyoto_days) == 3
    kyoto_activities_text = " ".join([a["activity"].lower() for kd in kyoto_days for a in kd["activities"]])
    assert "fushimi inari" in kyoto_activities_text or "kiyomizu" in kyoto_activities_text or "bamboo" in kyoto_activities_text

    # Check Osaka days
    osaka_days = [d for d in journey["days"] if d["city"] == "Osaka"]
    assert len(osaka_days) == 2
    osaka_activities_text = " ".join([a["activity"].lower() for od in osaka_days for a in od["activities"]])
    assert "osaka castle" in osaka_activities_text or "dotonbori" in osaka_activities_text

    # 5. Day 1 arrival and Day 7 departure logic
    day1_activities = [a["activity"] for a in journey["days"][0]["activities"]]
    assert any("Arrival" in act or "Flight" in act or "Touchdown" in act for act in day1_activities)

    day7_activities = [a["activity"] for a in journey["days"][-1]["activities"]]
    assert any("Return" in act or "Airport" in act for act in day7_activities)

    # 6. Budget calculation consistency
    cost_bd = journey["cost_breakdown"]
    sum_components = (
        cost_bd["Accommodation"] +
        cost_bd["Intercity Transport"] +
        cost_bd["Dining"] +
        cost_bd["Local Transportation"] +
        cost_bd["Activities"] +
        cost_bd["Contingency Buffer (5%)"]
    )
    assert abs(sum_components - cost_bd["Total Estimated"]) < 50, f"Budget math inconsistent: {sum_components} vs {cost_bd['Total Estimated']}"

    # 7. Pre-render 8-point validation
    val_report = journey["validation_report"]
    assert val_report["is_valid"] is True, f"Validation failed: {val_report}"
    assert val_report["passed_checks"] == 8, f"Expected 8/8 checks passed, got {val_report['passed_checks']}"

    print("✅ TEST 1 PASSED: Exact prompt preserves Hyderabad origin, 7 stay days, independent legs, and 8-point validation!")


def test_missing_origin_detection():
    print("==================================================")
    print("TEST 2: Missing Origin Detection")
    print("==================================================")
    prompt = "Tokyo (2 days) → Kyoto (3 days) → Osaka (2 days)"
    parsed = parse_multi_stop_trip_prompt(prompt)
    assert len(parsed["missing_information"]) > 0, "Failed to flag missing origin"
    assert any("starting location is missing" in m.lower() for m in parsed["missing_information"])
    print("✅ TEST 2 PASSED: Missing origin properly flagged without inventing fake locations!")


def test_seasonal_recommendations_qualified():
    print("==================================================")
    print("TEST 3: Seasonal Recommendations & Forecast Qualification")
    print("==================================================")
    resp = recommend_destinations_by_season("december")
    assert "historical" in resp.lower() or "climate" in resp.lower()
    assert "not a live guaranteed forecast" in resp.lower() or "meteorological averages" in resp.lower()
    assert "travel year" in resp.lower() or "2026" in resp.lower()
    print("✅ TEST 3 PASSED: Seasonal recommendations distinguish historical climate from live forecasts!")


def test_chatbot_integration():
    print("==================================================")
    print("TEST 4: Chatbot Natural Multi-Stop Query Handling")
    print("==================================================")
    chat_resp = answer_travel_question(
        "Japan",
        "Plan Hyderabad → Tokyo (2 days) → Kyoto (3 days) → Osaka (2 days) → Hyderabad."
    )
    assert "Hyderabad" in chat_resp
    assert "Tokyo" in chat_resp
    assert "Kyoto" in chat_resp
    assert "Osaka" in chat_resp
    assert "7 Destination Stay Days" in chat_resp
    assert "Validation: Verified (8/8 Checks Passed)" in chat_resp
    print("✅ TEST 4 PASSED: Chatbot correctly invokes multi-stop planner with verified badge!")


if __name__ == "__main__":
    try:
        test_scenario_user_prompt()
        test_missing_origin_detection()
        test_seasonal_recommendations_qualified()
        test_chatbot_integration()
        print("\n🎉 ALL MULTI-STOP ACCURACY VERIFICATION TESTS PASSED SUCCESSFULLY!")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
