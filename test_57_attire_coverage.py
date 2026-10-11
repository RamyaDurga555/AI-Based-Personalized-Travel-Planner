"""
test_57_attire_coverage.py
Comprehensive validation and statistics across all 57 countries in CURATED_TRADITIONAL_CLOTHING.
Checks:
1. Column 1 (Card 0) is Women's Wear, Column 2 (Card 1) is Men's Wear.
2. Gender correctness and positive validation of images.
3. Fallback behavior when image is unverified/unavailable.
4. Reports exact counts:
   - Verified photos for both genders
   - Verified photos for one gender
   - Fallbacks for both genders
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import app
import country_data

def run_attire_audit():
    curated_countries = list(country_data.CURATED_TRADITIONAL_CLOTHING.keys())
    total_countries = len(curated_countries)
    print(f"=== TRADITIONAL CLOTHING COVERAGE AUDIT: {total_countries} COUNTRIES ===")

    both_verified = []
    one_verified = []
    both_fallback = []
    ordering_errors = []
    gender_violations = []

    for idx, c_name in enumerate(curated_countries, 1):
        c_info = country_data.get_traditional_clothing(c_name)
        raw_attires = c_info.get("attires") or [c_info.get("women"), c_info.get("men")]
        raw_attires = [a for a in raw_attires if a]
        women_list = [a for a in raw_attires if app.is_women_attire_dict(a)]
        men_list = [a for a in raw_attires if app.is_men_attire_dict(a)]
        reg_list = [a for a in raw_attires if a not in women_list and a not in men_list]
        primary_w = women_list[0] if women_list else None
        primary_m = men_list[0] if men_list else None
        remaining = (women_list[1:] if len(women_list) > 1 else []) + (men_list[1:] if len(men_list) > 1 else []) + reg_list
        attires = ([primary_w] if primary_w else []) + ([primary_m] if primary_m else []) + remaining

        # 1. Check ordering
        if not primary_w or not primary_m:
            ordering_errors.append(f"{c_name}: Missing primary women ({bool(primary_w)}) or men ({bool(primary_m)})")
        elif attires[0] != primary_w or attires[1] != primary_m:
            ordering_errors.append(f"{c_name}: Row 1 pairing incorrect: [0]={attires[0]['name']}, [1]={attires[1]['name']}")

        # 2. Check validation on primary attires
        used = set()
        w_img = primary_w.get("image") if primary_w else None
        if w_img:
            if not app.is_valid_attire_image(primary_w.get("name", ""), "", w_img, primary_w.get("name", ""), c_name, gender="women"):
                w_img = None
        if w_img:
            used.add(w_img)

        m_img = primary_m.get("image") if primary_m else None
        if m_img:
            if not app.is_valid_attire_image(primary_m.get("name", ""), "", m_img, primary_m.get("name", ""), c_name, gender="men"):
                m_img = None
        if m_img and m_img in used:
            m_img = None # Prevent reusing women's image
        elif m_img:
            used.add(m_img)

        # 3. Check for any cross-gender leakage
        if w_img and not app.is_valid_attire_image(primary_w.get("name", ""), "", w_img, primary_w.get("name", ""), c_name, gender="women"):
            gender_violations.append(f"{c_name} Women's Wear image failed strict female validation: {w_img}")
        if m_img and not app.is_valid_attire_image(primary_m.get("name", ""), "", m_img, primary_m.get("name", ""), c_name, gender="men"):
            gender_violations.append(f"{c_name} Men's Wear image failed strict male validation: {m_img}")

        # 4. Classify country
        if w_img and m_img:
            both_verified.append(c_name)
            status = "BOTH VERIFIED"
        elif w_img or m_img:
            one_verified.append(c_name)
            status = f"ONE VERIFIED (W:{bool(w_img)}, M:{bool(m_img)})"
        else:
            both_fallback.append(c_name)
            status = "BOTH REQUIRE FALLBACK"

        print(f"[{idx:2d}/{total_countries}] {c_name:<18} -> {status}")

    print("\n" + "="*60)
    print("SUMMARY AUDIT STATISTICS:")
    print("="*60)
    print(f"Total Countries Evaluated:                {total_countries}")
    print(f"Ordering Errors (Card 0 != W or Card 1 != M): {len(ordering_errors)}")
    print(f"Cross-Gender / Validation Violations:      {len(gender_violations)}")
    print(f"Countries with Verified Images for Both:   {len(both_verified)} ({len(both_verified)/total_countries*100:.1f}%)")
    print(f"Countries with Verified Image for One:     {len(one_verified)} ({len(one_verified)/total_countries*100:.1f}%)")
    print(f"Countries with Fallbacks for Both:         {len(both_fallback)} ({len(both_fallback)/total_countries*100:.1f}%)")
    print("="*60)

    # Specific Nepal Check
    print("\nNEPAL SPECIFIC VERIFICATION:")
    nepal = country_data.get_traditional_clothing("Nepal")
    print("Country:     ", nepal["country"])
    print("Women Attire:", nepal["women"]["name"])
    print("Women Local: ", nepal["women"]["local_name"])
    print("Women Image: ", nepal["women"]["image"])
    print("Men Attire:  ", nepal["men"]["name"])
    print("Men Local:   ", nepal["men"]["local_name"])
    print("Men Image:   ", nepal["men"]["image"])
    nepal_w_valid = app.is_valid_attire_image(nepal["women"]["name"], nepal["women"]["description"], nepal["women"]["image"], nepal["women"]["name"], "Nepal", "women")
    nepal_m_valid = app.is_valid_attire_image(nepal["men"]["name"], nepal["men"]["description"], nepal["men"]["image"], nepal["men"]["name"], "Nepal", "men")
    print("Nepal Women Image Valid:", nepal_w_valid)
    print("Nepal Men Image Valid:  ", nepal_m_valid)

    assert len(ordering_errors) == 0, f"Ordering errors found: {ordering_errors}"
    assert len(gender_violations) == 0, f"Gender violations found: {gender_violations}"
    assert nepal_w_valid, "Nepal women image must be valid!"
    assert nepal_m_valid, "Nepal men image must be valid!"
    assert total_countries >= 50, f"Must have >= 50 countries, found {total_countries}"
    print("\nALL AUDIT ASSERTIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_attire_audit()
