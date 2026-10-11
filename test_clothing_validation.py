"""
Comprehensive Validation Tests for Traditional Clothing Image Selection & Validation System.
Tests across curated and synthesized countries, verifying:
1. Adult male attire photos & rejection of child/boy images.
2. Adult female attire photos & rejection of child/girl images.
3. Gender alignment (no female-only in male attire, no male-only in female attire).
4. Metadata inspection & non-photographic media rejection.
5. Nepal specific verification (adult man in Daura Suruwal, adult woman in Gunyo Cholo).
6. Multi-country verification (India, Japan, Thailand, Vietnam, France, Germany, etc.).
7. Safe fallback when authentic adult photo is unavailable.
"""

import sys
import re
from country_data import (
    CURATED_TRADITIONAL_CLOTHING,
    get_traditional_clothing,
    format_traditional_clothing_markdown,
)
from app import (
    is_valid_attire_image,
    get_attire_image,
    resolve_card_image_url,
    CHILD_TERMS,
)


def test_child_rejection_rules():
    print("Running test_child_rejection_rules...")
    test_cases = [
        ("NepalBoy_ST_10.JPG", "Daura Suruwal", "Nepal", "men"),
        ("A_Nepali_girl_in_cultural_dress.jpg", "Gunyo Cholo", "Nepal", "women"),
        ("Schoolboy in traditional kilt.jpg", "Kilt", "United Kingdom", "men"),
        ("Little girl wearing kimono.jpg", "Kimono", "Japan", "women"),
        ("Children dancing in lederhosen.jpg", "Lederhosen", "Germany", "men"),
        ("Bambino in costume sardo.jpg", "Costume Sardo", "Italy", "men"),
        ("Fillette en costume alsacien.jpg", "Costume d'Alsace", "France", "women"),
        ("Toddler in hanbok.jpg", "Hanbok", "South Korea", "women"),
        ("Young kids in sombrero.jpg", "Charro", "Mexico", "men"),
    ]

    for title, attire, country, gender in test_cases:
        url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{title.replace(' ', '_')}"
        valid = is_valid_attire_image(
            title=title,
            extract="",
            image_url=url,
            attire_name=attire,
            country=country,
            gender=gender,
        )
        assert not valid, f"Expected {title} to be REJECTED for {gender} attire, but got valid=True"
    print("  -> Passed: All child/minor images successfully rejected across countries.")


def test_gender_alignment_rules():
    print("Running test_gender_alignment_rules...")
    # Female-only should be rejected for men
    female_case = is_valid_attire_image(
        title="Female Hanbok from South Korea.jpg",
        extract="A Korean woman wearing colorful traditional dress.",
        image_url="https://upload.wikimedia.org/female_hanbok.jpg",
        attire_name="Baji Jeogori",
        country="South Korea",
        gender="men"
    )
    assert not female_case, "Expected female-only portrait to be rejected for Men's attire"

    # Male-only should be rejected for women
    male_case = is_valid_attire_image(
        title="Bavarian man in Lederhosen.jpg",
        extract="German gentleman wearing authentic Bavarian leather shorts.",
        image_url="https://upload.wikimedia.org/bavarian_man.jpg",
        attire_name="Dirndl",
        country="Germany",
        gender="women"
    )
    assert not male_case, "Expected male-only portrait to be rejected for Women's attire"

    # Couple/wedding/pair should be accepted for both
    couple_case_men = is_valid_attire_image(
        title="Bride and Groom in Traditional Attire.jpg",
        extract="Indian wedding couple wearing sherwani and lehenga.",
        image_url="https://upload.wikimedia.org/couple.jpg",
        attire_name="Sherwani",
        country="India",
        gender="men"
    )
    assert couple_case_men, "Expected wedding couple to be accepted for Men's attire"

    couple_case_women = is_valid_attire_image(
        title="Bride and Groom in Traditional Attire.jpg",
        extract="Indian wedding couple wearing sherwani and lehenga.",
        image_url="https://upload.wikimedia.org/couple.jpg",
        attire_name="Lehenga",
        country="India",
        gender="women"
    )
    assert couple_case_women, "Expected wedding couple to be accepted for Women's attire"
    print("  -> Passed: Gender alignment rules strictly enforced.")


def test_metadata_rejection():
    print("Running test_metadata_rejection...")
    # Rejection via metadata ImageDescription containing child term
    meta_child = {
        "ImageDescription": {"value": "Young schoolboy demonstrating national costume"},
        "Categories": {"value": "Folk costumes|Students"},
    }
    res = is_valid_attire_image(
        title="Costume_display_01.jpg",
        extract="",
        image_url="https://upload.wikimedia.org/img.jpg",
        attire_name="Traditional Attire",
        country="Norway",
        gender="men",
        metadata=meta_child
    )
    assert not res, "Expected metadata with 'schoolboy' to be rejected"

    # Rejection via metadata mannequin
    meta_mannequin = {
        "ImageDescription": {"value": "Museum exhibition showcase with mannequin wearing historical jacket"},
        "Categories": {"value": "Museum exhibits"},
    }
    res_m = is_valid_attire_image(
        title="Exhibit_123.jpg",
        extract="",
        image_url="https://upload.wikimedia.org/img.jpg",
        attire_name="Traditional Attire",
        country="Sweden",
        gender="men",
        metadata=meta_mannequin
    )
    assert not res_m, "Expected metadata with 'mannequin' to be rejected"
    print("  -> Passed: Metadata inspection correctly flags non-conforming images.")


def test_nepal_traditional_clothing():
    print("Running test_nepal_traditional_clothing...")
    nepal_data = get_traditional_clothing("Nepal")
    men_data = nepal_data["men"]
    women_data = nepal_data["women"]

    # Check men's image
    men_img = men_data.get("image", "")
    assert "NepalBoy" not in men_img, f"Found NepalBoy in Nepal men's attire: {men_img}"
    assert "boy" not in men_img.lower(), f"Found boy in Nepal men's attire: {men_img}"
    assert men_img, "Nepal men attire must have an image"

    # Check women's image
    women_img = women_data.get("image", "")
    assert "girl" not in women_img.lower(), f"Found girl in Nepal women's attire: {women_img}"
    assert women_img, "Nepal women attire must have an image"

    # Validate with is_valid_attire_image
    assert is_valid_attire_image("Daura Suruwal", "", men_img, "Daura-Suruwal", "Nepal", gender="men")
    assert is_valid_attire_image("Gunyo Cholo", "", women_img, "Gunyo Cholo", "Nepal", gender="women")

    # Check attires array
    for att in nepal_data.get("attires", []):
        img = att.get("image")
        if img:
            assert "NepalBoy" not in img
            assert "girl" not in img.lower()
            assert is_valid_attire_image(att["name"], "", img, att["name"], "Nepal", gender=att.get("gender", "unisex"))
    print("  -> Passed: Nepal attire features verified adult photographs.")


def test_multi_country_curated_clothing():
    print("Running test_multi_country_curated_clothing...")
    countries = ["India", "Japan", "Thailand", "Vietnam", "South Korea"]
    for c in countries:
        data = get_traditional_clothing(c)
        assert data, f"Missing data for {c}"
        for role in ["men", "women"]:
            att = data.get(role)
            if att and att.get("image"):
                img = att["image"]
                # Must be adult photograph
                assert is_valid_attire_image(att["name"], "", img, att["name"], c, gender=role), \
                    f"Curated image failed validation for {c} - {role}: {img}"
    print("  -> Passed: Multiple benchmark countries verified.")


def test_safe_fallback():
    print("Running test_safe_fallback...")
    # France women has no verified photo (None), triggering safe fallback
    france_data = get_traditional_clothing("France")
    f_women_img = france_data["women"].get("image")
    assert f_women_img is None, f"Expected France women attire image to be None, got {f_women_img}"

    # Formatting markdown should include the safe fallback notice
    md = format_traditional_clothing_markdown(france_data)
    assert "Authentic adult attire photo unavailable" in md, "Expected fallback notice in markdown"
    print("  -> Passed: Safe fallback triggered correctly.")


if __name__ == "__main__":
    test_child_rejection_rules()
    test_gender_alignment_rules()
    test_metadata_rejection()
    test_nepal_traditional_clothing()
    test_multi_country_curated_clothing()
    test_safe_fallback()
    print("\nALL CLOTHING VALIDATION TESTS PASSED SUCCESSFULLY!")
