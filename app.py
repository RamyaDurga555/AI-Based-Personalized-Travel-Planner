import streamlit as st
import html
import json
import os
import sys
_app_dir = os.path.dirname(os.path.abspath(__file__))
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)
import plotly.graph_objects as go
import pycountry
import requests
import re
from urllib.parse import quote

from planner import (
    COUNTRIES,
    generate_itinerary,
    country_info,
    recommend_destinations,
    update_itinerary
)

import importlib
import country_data
try:
    importlib.reload(country_data)
except Exception:
    pass

from country_data import (
    get_country_knowledge,
    get_attractions,
    get_food,
    get_culture,
    get_transportation,
    get_travel_tips,
    answer_travel_question,
    LANGUAGE_VOICE_CODES
)

try:
    from country_data import get_traditional_clothing
except ImportError:
    try:
        importlib.reload(country_data)
        from country_data import get_traditional_clothing
    except ImportError:
        def get_traditional_clothing(country_name: str):
            if hasattr(country_data, "get_traditional_clothing"):
                return country_data.get_traditional_clothing(country_name)
            prof = country_data.get_country_knowledge(country_name) if hasattr(country_data, "get_country_knowledge") else {}
            c_name = prof.get("name", country_name)
            return {
                "country": c_name,
                "men": {
                    "name": f"{c_name} Traditional Wear",
                    "local_name": f"{c_name} Attire",
                    "description": f"Authentic traditional garments worn for cultural ceremonies and celebrations in {c_name}.",
                    "fabrics": "Natural cotton, silk, and woven fabrics",
                    "cost_inr": "₹3,500 – ₹10,000",
                    "cost_local": "Local currency equivalent",
                    "rental_price": "₹800 – ₹1,800 per day",
                    "where_to_buy": "Central markets and traditional tailors"
                },
                "women": {
                    "name": f"{c_name} Traditional Dress",
                    "local_name": f"{c_name} Dress",
                    "description": f"Graceful traditional dress and decorative wrap worn for festivals and special occasions in {c_name}.",
                    "fabrics": "Fine embroidered silk, linen, or brocade",
                    "cost_inr": "₹4,500 – ₹14,000",
                    "cost_local": "Local currency equivalent",
                    "rental_price": "₹1,000 – ₹2,200 per day",
                    "where_to_buy": "Heritage boutiques and traditional craft centers"
                },
                "cultural_significance": f"Reflects the rich cultural heritage and artisanal textile history of {c_name}.",
                "rental_note": "Costume rentals are commonly available near historical landmarks and cultural centers for photography."
            }

try:
    from country_data import get_where_to_try, get_destination_gallery_items
except ImportError:
    try:
        importlib.reload(country_data)
        from country_data import get_where_to_try, get_destination_gallery_items
    except ImportError:
        def get_where_to_try(country: str, dish_name: str) -> str:
            return f"Authentic local restaurants and traditional markets in {country}"

        def get_destination_gallery_items(country_name: str):
            prof = get_country_knowledge(country_name)
            cities = prof.get("cities", [country_name])
            items = []
            for c in cities[:6]:
                items.append({
                    "name": c,
                    "query": f"{c} {country_name} landmark travel",
                    "caption": f"Explore {c} in {country_name}"
                })
            return items

try:
    from country_data import get_conversational_onboarding_greeting
except ImportError:
    try:
        importlib.reload(country_data)
        from country_data import get_conversational_onboarding_greeting
    except ImportError:
        def get_conversational_onboarding_greeting(role_or_name="guide", destination="", assistant_name="Maya", **kwargs):
            if hasattr(country_data, "get_conversational_onboarding_greeting"):
                return country_data.get_conversational_onboarding_greeting(role_or_name, destination, assistant_name, **kwargs)
            name = assistant_name or ("Maya" if "guide" in str(role_or_name).lower() else "Alex")
            role_label = "Travel Guide" if "guide" in str(role_or_name).lower() else "AI Travel Companion"
            if not destination:
                return f"Hi! 👋 I'm **{name}**, your personal {role_label} from the **AI-Based Personalized Travel Planner**.\n\nWhere do you want to go? Do you already have a destination in mind, or would you like me to suggest one based on this season?"
            return f"Hello! I'm **{name}**, your {role_label} for **{destination}** ✈️.\n\nWhere will you be starting your journey from, and when are you planning to travel?"

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI-Based Personalized Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global Full-Page Styling: completely hide the sidebar application-wide
st.markdown(
    """
    <style>
    /* Full-Page Application: Hide Streamlit Sidebar & Control button everywhere */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    iframe[title="st.iframe"], iframe.stIFrame {
        border: none !important;
        outline: none !important;
    }
    .main .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1400px !important;
    }

    /* Persistent Top Navigation Bar */
    .top-nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 14px 22px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    .top-nav-brand-title {
        font-size: 20px;
        font-weight: 900;
        letter-spacing: -0.3px;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .top-nav-brand-tagline {
        font-size: 12.5px;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 2px;
    }
    .top-nav-dest-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 999px;
        padding: 5px 14px;
        font-size: 13px;
        font-weight: 700;
    }

    /* Landing Page Hero & Characters */
    .hero-character-card {
        text-align: center;
        margin-bottom: 8px;
    }
    .hero-character-badge {
        display: inline-block;
        background: rgba(236, 72, 153, 0.18);
        border: 1px solid rgba(236, 72, 153, 0.45);
        color: #f472b6;
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .hero-character-footer {
        font-size: 12px;
        color: #94a3b8;
        font-style: italic;
        text-align: center;
        margin-top: 6px;
        line-height: 1.4;
    }
    .landing-hero-center {
        text-align: center;
        padding: 10px 18px;
    }
    .landing-plane-icon {
        font-size: 32px;
        margin-bottom: 6px;
    }
    .landing-pre-badge {
        display: inline-block;
        font-size: 11.5px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 999px;
        padding: 4px 14px;
        margin-bottom: 10px;
    }
    .landing-main-title {
        font-size: 42px !important;
        font-weight: 900 !important;
        line-height: 1.15 !important;
        color: #f8fafc !important;
        margin-bottom: 10px !important;
    }
    .landing-subtitle {
        font-size: 18px;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 6px;
    }
    .landing-description {
        font-size: 14.5px;
        color: #cbd5e1;
        line-height: 1.5;
        max-width: 580px;
        margin: 0 auto 16px auto;
    }
    .landing-feature-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        min-height: 125px;
        margin-bottom: 8px;
    }
    .landing-feature-icon {
        font-size: 26px;
        margin-bottom: 6px;
    }
    .landing-feature-title {
        font-size: 15px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
    }
    .landing-feature-desc {
        font-size: 12px;
        color: #94a3b8;
        line-height: 1.4;
    }

    /* Page Header Box */
    .page-header-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 20px;
    }
    .page-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    .page-title {
        font-size: 28px !important;
        font-weight: 900 !important;
        color: #f8fafc !important;
        margin: 4px 0 !important;
    }
    .page-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin: 0;
    }

    /* Shared Country Metric Cards */
    .country-info-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 6px;
    }
    .country-info-label {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .country-info-value {
        font-size: 15px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE INITIALIZATION & MULTI-PAGE NAVIGATION
# ============================================================

# Multi-Page Navigation Modes (10 Pages):
# 1. landing   -> PAGE 1: Home (Welcome & Traveler Characters Hero)
# 2. plan      -> PAGE 2: Plan My Trip (Guided & Natural-Language Planner)
# 3. explore   -> PAGE 3: Explore the World (Interactive 3D Globe & Destinations)
# 4. discover  -> PAGE 4: Discover (Destination Attractions, Food & Culture)
# 5. guide     -> PAGE 5: Travel Guide (Dynamic Categorized Destination Guide)
# 6. itinerary -> PAGE 6: My Itinerary (Day-by-Day Journey & Cost Engine)
# 7. companion -> PAGE 7: AI Travel Companion (Local Travel Intelligence Engine + Voice Synthesis)
# 8. safety    -> PAGE 8: Safety & Emergency (Verified Official Contacts & Guidelines)
# 9. saved     -> PAGE 9: Saved Places (Functional Favorites & Stash)
# 10. summary  -> PAGE 10: Trip Summary (Comprehensive Travel Blueprint)

if "app_mode" not in st.session_state:
    st.session_state.app_mode = "landing"

# Backward compatibility normalization for legacy session states
if st.session_state.app_mode in ("dashboard", "explore_globe"):
    st.session_state.app_mode = "explore"
elif st.session_state.app_mode == "clothing":
    st.session_state.app_mode = "discover"
elif st.session_state.app_mode == "assistant":
    st.session_state.app_mode = "companion"

if "starting_location" not in st.session_state:
    st.session_state.starting_location = ""

if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Japan"

if "globe_country" not in st.session_state:
    st.session_state.globe_country = "Japan"

if "selected_globe_place" not in st.session_state:
    st.session_state.selected_globe_place = None

if "guide_tab" not in st.session_state:
    st.session_state.guide_tab = "Places"

if "destination_country_select" not in st.session_state:
    st.session_state.destination_country_select = "Japan"

if "saved_places" not in st.session_state:
    st.session_state.saved_places = []

if "days" not in st.session_state:
    st.session_state.days = 7

if "travelers" not in st.session_state:
    st.session_state.travelers = 1

if "budget" not in st.session_state:
    st.session_state.budget = 80000

if "interests" not in st.session_state:
    st.session_state.interests = ["Culture", "Food"]

if "style" not in st.session_state:
    st.session_state.style = "Relaxed"

if "itinerary" not in st.session_state:
    st.session_state.itinerary = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "guide_chat_history" not in st.session_state:
    st.session_state.guide_chat_history = []

def sanitize_chat_message_content(text: str) -> str:
    """Ensures no outdated or misclassified images appear in rendered chat messages."""
    if not text or not isinstance(text, str):
        return text
    if "in_a_traditional_magar_attire_02" in text.lower():
        text = re.sub(
            r'https://thumb\.wikimedia\.org/wikipedia/commons/thumb/[^\s\)]*in_a_traditional_magar_attire_02[^\s\)]*',
            'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/64/Traditional_Dress111.jpg/960px-Traditional_Dress111.jpg',
            text,
            flags=re.IGNORECASE
        )
    return text

# Immediately cleanse active in-memory session chat histories
for _hist_key in ["chat_history", "guide_chat_history"]:
    if _hist_key in st.session_state and isinstance(st.session_state[_hist_key], list):
        for _msg in st.session_state[_hist_key]:
            if isinstance(_msg, dict) and "content" in _msg:
                _msg["content"] = sanitize_chat_message_content(_msg["content"])

if "asst_response_lang" not in st.session_state:
    st.session_state.asst_response_lang = "Auto Detect"

if "custom_assistant_name" not in st.session_state:
    st.session_state.custom_assistant_name = ""

if "multi_stop_plan" not in st.session_state:
    st.session_state.multi_stop_plan = None

if "multi_stops_list" not in st.session_state:
    st.session_state.multi_stops_list = [
        {"city": "Tokyo", "country": "Japan", "days": 2},
        {"city": "Kyoto", "country": "Japan", "days": 3},
        {"city": "Osaka", "country": "Japan", "days": 2}
    ]

def get_assistant_name(character="guide"):
    custom = st.session_state.get("custom_assistant_name", "").strip()
    if custom:
        return custom
    return "Maya" if character == "guide" else "Alex"


# ============================================================
# LOCAL ASSETS CONFIGURATION (TRAVELER CHARACTERS)
# ============================================================

import shutil

ASSETS_DIR = os.path.join(_app_dir, "assets")
try:
    os.makedirs(ASSETS_DIR, exist_ok=True)
except Exception:
    pass

FEMALE_TRAVELER_IMG = os.path.join(ASSETS_DIR, "female_traveler.jpg")
MALE_TRAVELER_IMG = os.path.join(ASSETS_DIR, "male_traveler.jpg")

_SOURCE_FEMALE = r"C:\Users\gidug\.gemini\antigravity-ide\brain\0d7fbddd-f429-479b-8ab3-d02a69a2161e\female_traveler_1791387235115.jpg"
_SOURCE_MALE = r"C:\Users\gidug\.gemini\antigravity-ide\brain\0d7fbddd-f429-479b-8ab3-d02a69a2161e\male_traveler_1791387264257.jpg"

if os.path.exists(_SOURCE_FEMALE) and (not os.path.exists(FEMALE_TRAVELER_IMG) or os.path.getsize(FEMALE_TRAVELER_IMG) == 0):
    try:
        shutil.copy2(_SOURCE_FEMALE, FEMALE_TRAVELER_IMG)
    except Exception:
        pass

if os.path.exists(_SOURCE_MALE) and (not os.path.exists(MALE_TRAVELER_IMG) or os.path.getsize(MALE_TRAVELER_IMG) == 0):
    try:
        shutil.copy2(_SOURCE_MALE, MALE_TRAVELER_IMG)
    except Exception:
        pass


def get_character_image(gender="female"):
    """Returns absolute path to local female or male traveler character illustration."""
    target = FEMALE_TRAVELER_IMG if gender == "female" else MALE_TRAVELER_IMG
    fallback = _SOURCE_FEMALE if gender == "female" else _SOURCE_MALE
    if os.path.exists(target) and os.path.getsize(target) > 0:
        return target
    if os.path.exists(fallback) and os.path.getsize(fallback) > 0:
        return fallback
    return None


# ============================================================
# CURATED 30 FEATURED TRAVEL DESTINATIONS
# ============================================================

CURATED_30_DESTINATIONS = {
    "Japan": {
        "flag": "🇯🇵",
        "tagline": "Where ancient tradition meets neon-lit tomorrow.",
        "capital": "Tokyo",
        "currency": "Japanese Yen (JPY ¥)",
        "languages": "Japanese",
        "region": "East Asia",
        "best_season": "March–May (Cherry Blossoms) & Oct–Nov (Autumn Foliage)",
        "suggested_duration": "7–14 Days",
        "est_budget": "₹9,500 / day",
        "cities": ["Tokyo", "Kyoto", "Osaka", "Hakone", "Hiroshima", "Nara"],
        "highlights": ["Mount Fuji", "Fushimi Inari Shrine", "Senso-ji Temple", "Arashiyama Bamboo Grove"],
        "food": ["Sushi & Sashimi", "Ramen", "Tempura", "Okonomiyaki", "Matcha Sweets"],
        "attire": "Kimono & Yukata (Rental: ¥3,000–¥6,000 / day)"
    },
    "India": {
        "flag": "🇮🇳",
        "tagline": "A kaleidoscopic land of timeless heritage and vibrant colors.",
        "capital": "New Delhi",
        "currency": "Indian Rupee (INR ₹)",
        "languages": "Hindi, English & 22 Official Languages",
        "region": "South Asia",
        "best_season": "October–March (Pleasant Winters across most regions)",
        "suggested_duration": "10–21 Days",
        "est_budget": "₹3,500 / day",
        "cities": ["New Delhi", "Agra", "Jaipur", "Srinagar (Jammu & Kashmir)", "Goa", "Varanasi", "Kerala"],
        "highlights": ["Taj Mahal", "Golden Temple", "Dal Lake & Gulmarg", "Amber Fort", "Hawa Mahal"],
        "food": ["Biryani", "Masala Dosa", "Butter Chicken", "Rogan Josh", "Gulab Jamun"],
        "attire": "Silk Saree & Royal Sherwani (Rental: ₹1,500–₹5,000 / day)"
    },
    "France": {
        "flag": "🇫🇷",
        "tagline": "The pinnacle of romance, haute cuisine, and iconic art.",
        "capital": "Paris",
        "currency": "Euro (EUR €)",
        "languages": "French",
        "region": "Western Europe",
        "best_season": "April–June & September–November",
        "suggested_duration": "7–12 Days",
        "est_budget": "₹12,000 / day",
        "cities": ["Paris", "Nice", "Lyon", "Marseille", "Bordeaux", "Strasbourg"],
        "highlights": ["Eiffel Tower", "Louvre Museum", "Palace of Versailles", "French Riviera", "Mont Saint-Michel"],
        "food": ["Croissants & Baguettes", "Boeuf Bourguignon", "Crème Brûlée", "Ratatouille"],
        "attire": "Breton Striped Marinière & Haute Parisian Couture"
    },
    "Italy": {
        "flag": "🇮🇹",
        "tagline": "Living history, breathtaking coastlines, and culinary passion.",
        "capital": "Rome",
        "currency": "Euro (EUR €)",
        "languages": "Italian",
        "region": "Southern Europe",
        "best_season": "April–June & September–October",
        "suggested_duration": "8–14 Days",
        "est_budget": "₹11,000 / day",
        "cities": ["Rome", "Florence", "Venice", "Milan", "Amalfi", "Naples"],
        "highlights": ["Colosseum", "Vatican Museums", "Venice Grand Canal", "Florence Duomo", "Amalfi Coast"],
        "food": ["Neapolitan Pizza", "Fresh Pasta Carbonara", "Gelato", "Tiramisu", "Espresso"],
        "attire": "Venetian Carnival Attire & Classic Italian Tailoring"
    },
    "Switzerland": {
        "flag": "🇨🇭",
        "tagline": "Pristine Alpine peaks, crystalline lakes, and scenic railways.",
        "capital": "Bern",
        "currency": "Swiss Franc (CHF)",
        "languages": "German, French, Italian, Romansh",
        "region": "Central Europe",
        "best_season": "June–September (Hiking) & Dec–March (Skiing)",
        "suggested_duration": "6–10 Days",
        "est_budget": "₹16,000 / day",
        "cities": ["Zurich", "Geneva", "Lucerne", "Interlaken", "Zermatt"],
        "highlights": ["Matterhorn", "Jungfraujoch", "Lake Geneva", "Mount Pilatus", "Chapel Bridge"],
        "food": ["Swiss Cheese Fondue", "Raclette", "Rösti", "Swiss Chocolate"],
        "attire": "Traditional Swiss Tracht with Edelweiss embroidery"
    },
    "Greece": {
        "flag": "🇬🇷",
        "tagline": "The cradle of democracy surrounded by sun-drenched Aegean isles.",
        "capital": "Athens",
        "currency": "Euro (EUR €)",
        "languages": "Greek",
        "region": "Southern Europe",
        "best_season": "May–June & September–October",
        "suggested_duration": "7–12 Days",
        "est_budget": "₹8,500 / day",
        "cities": ["Athens", "Santorini", "Mykonos", "Crete", "Rhodes", "Thessaloniki"],
        "highlights": ["Acropolis of Athens", "Santorini Caldera & Oia", "Parthenon", "Delphi", "Meteora Monasteries"],
        "food": ["Moussaka", "Souvlaki & Gyros", "Greek Salad with Feta", "Baklava", "Spanakopita"],
        "attire": "Traditional Foustanella & Aegean Island Costumes"
    },
    "Spain": {
        "flag": "🇪🇸",
        "tagline": "Fiery flamenco, architectural wonders, and sun-soaked tapas life.",
        "capital": "Madrid",
        "currency": "Euro (EUR €)",
        "languages": "Spanish",
        "region": "Southwestern Europe",
        "best_season": "April–June & September–October",
        "suggested_duration": "7–14 Days",
        "est_budget": "₹8,800 / day",
        "cities": ["Barcelona", "Madrid", "Seville", "Granada", "Valencia"],
        "highlights": ["Sagrada Família", "Alhambra Palace", "Park Güell", "Prado Museum", "Plaza de España"],
        "food": ["Paella Valenciana", "Tapas & Pintxos", "Churros con Chocolate", "Gazpacho", "Jamón Ibérico"],
        "attire": "Traje de Flamenca (Flamenco Dress) & Cordobés Hat"
    },
    "Turkey": {
        "flag": "🇹🇷",
        "tagline": "Where continents collide in ancient bazaars and fairy chimneys.",
        "capital": "Ankara",
        "currency": "Turkish Lira (TRY ₺)",
        "languages": "Turkish",
        "region": "Eurasia",
        "best_season": "April–May & September–October",
        "suggested_duration": "7–12 Days",
        "est_budget": "₹6,000 / day",
        "cities": ["Istanbul", "Cappadocia", "Antalya", "Izmir", "Bodrum"],
        "highlights": ["Hagia Sophia", "Cappadocia Hot Air Balloons", "Blue Mosque", "Grand Bazaar", "Pamukkale Terraces"],
        "food": ["Kebabs & Doner", "Turkish Baklava", "Pide", "Turkish Delight (Lokum)", "Turkish Tea & Coffee"],
        "attire": "Ottoman Kaftan & Traditional Turkish Shalvar"
    },
    "Thailand": {
        "flag": "🇹🇭",
        "tagline": "The Land of Smiles: golden temples, islands, and street food feasts.",
        "capital": "Bangkok",
        "currency": "Thai Baht (THB ฿)",
        "languages": "Thai",
        "region": "Southeast Asia",
        "best_season": "November–February (Cool & Dry)",
        "suggested_duration": "6–12 Days",
        "est_budget": "₹4,200 / day",
        "cities": ["Bangkok", "Phuket", "Chiang Mai", "Krabi", "Pattaya", "Ayutthaya"],
        "highlights": ["Grand Palace Bangkok", "Wat Arun", "Phi Phi Islands", "Chiang Mai Old City", "Railay Beach"],
        "food": ["Pad Thai", "Tom Yum Goong", "Green Curry", "Mango Sticky Rice", "Som Tum"],
        "attire": "Chut Thai Silk Attire (Rental: 200–500 THB / day)"
    },
    "Indonesia": {
        "flag": "🇮🇩",
        "tagline": "Emerald rice terraces, mystical volcanoes, and tropical beaches.",
        "capital": "Jakarta",
        "currency": "Indonesian Rupiah (IDR Rp)",
        "languages": "Indonesian",
        "region": "Southeast Asia",
        "best_season": "May–September (Dry Season)",
        "suggested_duration": "7–14 Days",
        "est_budget": "₹4,000 / day",
        "cities": ["Bali (Ubud & Seminyak)", "Jakarta", "Yogyakarta", "Lombok", "Komodo Island"],
        "highlights": ["Borobudur Temple", "Ubud Rice Terraces", "Tanah Lot Temple", "Komodo National Park", "Mount Bromo"],
        "food": ["Nasi Goreng", "Beef Rendang", "Chicken Satay", "Gado-Gado", "Mie Goreng"],
        "attire": "Batik Shirt & Traditional Kebaya with Sarong"
    },
    "Vietnam": {
        "flag": "🇻🇳",
        "tagline": "Emerald waters, limestone pinnacles, and timeless street culture.",
        "capital": "Hanoi",
        "currency": "Vietnamese Dong (VND ₫)",
        "languages": "Vietnamese",
        "region": "Southeast Asia",
        "best_season": "February–April & September–November",
        "suggested_duration": "7–12 Days",
        "est_budget": "₹3,800 / day",
        "cities": ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hoi An", "Ha Long Bay"],
        "highlights": ["Ha Long Bay Cruise", "Hoi An Ancient Town", "Old Quarter Hanoi", "Golden Bridge Ba Na Hills"],
        "food": ["Pho Bo & Pho Ga", "Banh Mi Baguette", "Bun Cha", "Vietnamese Egg Coffee", "Spring Rolls"],
        "attire": "Ao Dai Silk Tunic with Non La Conical Hat"
    },
    "Singapore": {
        "flag": "🇸🇬",
        "tagline": "Futuristic garden metropolis with world-class gastronomic fusion.",
        "capital": "Singapore",
        "currency": "Singapore Dollar (SGD S$)",
        "languages": "English, Mandarin, Malay, Tamil",
        "region": "Southeast Asia",
        "best_season": "November–January & June–August",
        "suggested_duration": "4–6 Days",
        "est_budget": "₹11,000 / day",
        "cities": ["Marina Bay", "Sentosa Island", "Chinatown", "Little India", "Orchard Road"],
        "highlights": ["Gardens by the Bay", "Marina Bay Sands", "Jewel Changi Airport", "Sentosa Island", "Merlion Park"],
        "food": ["Hainanese Chicken Rice", "Chili Crab", "Laksa", "Satay", "Kaya Toast with Soft Eggs"],
        "attire": "Modern Peranakan Nyonya Kebaya & Sarong"
    },
    "Malaysia": {
        "flag": "🇲🇾",
        "tagline": "Towering skylines, ancient rainforests, and multicultural heritage.",
        "capital": "Kuala Lumpur",
        "currency": "Malaysian Ringgit (MYR RM)",
        "languages": "Malay, English",
        "region": "Southeast Asia",
        "best_season": "December–February & May–August",
        "suggested_duration": "6–10 Days",
        "est_budget": "₹4,800 / day",
        "cities": ["Kuala Lumpur", "Penang (George Town)", "Langkawi", "Malacca", "Kota Kinabalu"],
        "highlights": ["Petronas Twin Towers", "Batu Caves", "George Town Street Art", "Langkawi Sky Bridge", "Kinabalu Park"],
        "food": ["Nasi Lemak", "Roti Canai with Dhal", "Char Kway Teow", "Laksa", "Teh Tarik"],
        "attire": "Baju Melayu (Men) & Baju Kurung (Women)"
    },
    "South Korea": {
        "flag": "🇰🇷",
        "tagline": "Dynastic palaces, cutting-edge K-culture, and tantalizing cuisine.",
        "capital": "Seoul",
        "currency": "South Korean Won (KRW ₩)",
        "languages": "Korean",
        "region": "East Asia",
        "best_season": "March–May & September–November",
        "suggested_duration": "7–12 Days",
        "est_budget": "₹8,500 / day",
        "cities": ["Seoul", "Busan", "Jeju Island", "Gyeongju", "Incheon"],
        "highlights": ["Gyeongbokgung Palace", "Bukchon Hanok Village", "N Seoul Tower", "Haeundae Beach", "Jeju Hallasan"],
        "food": ["Korean BBQ (Samgyeopsal)", "Bibimbap", "Kimchi Jjigae", "Tteokbokki", "Crispy Korean Fried Chicken"],
        "attire": "Hanbok Royal Silk Dress (Free entry to Seoul palaces in Hanbok!)"
    },
    "China": {
        "flag": "🇨🇳",
        "tagline": "Millennia of imperial history, Great Walls, and dramatic landscapes.",
        "capital": "Beijing",
        "currency": "Chinese Yuan (CNY ¥)",
        "languages": "Mandarin Chinese",
        "region": "East Asia",
        "best_season": "April–May & September–October",
        "suggested_duration": "8–16 Days",
        "est_budget": "₹7,200 / day",
        "cities": ["Beijing", "Shanghai", "Xi'an", "Chengdu", "Guilin", "Hangzhou"],
        "highlights": ["Great Wall of China", "Forbidden City", "Terracotta Warriors", "The Bund Shanghai", "Li River Karst Peaks"],
        "food": ["Peking Duck", "Dim Sum", "Sichuan Hotpot", "Xiao Long Bao Soup Dumplings", "Kung Pao Chicken"],
        "attire": "Hanfu Traditional Robe & Qipao (Cheongsam)"
    },
    "Nepal": {
        "flag": "🇳🇵",
        "tagline": "Crown of the Himalayas, sacred stupas, and peaceful mountain spirit.",
        "capital": "Kathmandu",
        "currency": "Nepalese Rupee (NPR ₨)",
        "languages": "Nepali",
        "region": "South Asia",
        "best_season": "October–December & March–May",
        "suggested_duration": "7–14 Days",
        "est_budget": "₹3,200 / day",
        "cities": ["Kathmandu", "Pokhara", "Lumbini", "Chitwan", "Bhaktapur", "Nagarkot"],
        "highlights": ["Mount Everest Region", "Pashupatinath Temple", "Boudhanath Stupa", "Phewa Lake Pokhara", "Swayambhunath"],
        "food": ["Steamed Momo with Achar", "Dal Bhat Power Platter", "Thukpa Noodle Soup", "Sel Roti", "Juju Dhau"],
        "attire": "Daura Suruwal (Men) & Gunyo Cholo Saree (Women)"
    },
    "United Arab Emirates": {
        "flag": "🇦🇪",
        "tagline": "Architectural marvels rising from Arabian desert dunes.",
        "capital": "Abu Dhabi",
        "currency": "UAE Dirham (AED د.إ)",
        "languages": "Arabic, English",
        "region": "Middle East",
        "best_season": "November–March (Pleasant Warmth)",
        "suggested_duration": "5–8 Days",
        "est_budget": "₹12,500 / day",
        "cities": ["Dubai", "Abu Dhabi", "Sharjah", "Ras Al Khaimah"],
        "highlights": ["Burj Khalifa", "Sheikh Zayed Grand Mosque", "Palm Jumeirah", "Louvre Abu Dhabi", "Desert Dune Safari"],
        "food": ["Shawarma", "Al Harees", "Machboos", "Luqaimat Sweet Dumplings", "Arabic Coffee & Dates"],
        "attire": "Kandura (Men) & Elegant Embroidered Abaya (Women)"
    },
    "Israel": {
        "flag": "🇮🇱",
        "tagline": "Sacred crossroad of ancient faith, vibrant coastlines, and desert oasis.",
        "capital": "Jerusalem",
        "currency": "Israeli New Shekel (ILS ₪)",
        "languages": "Hebrew, Arabic",
        "region": "Middle East",
        "best_season": "March–May & October–November",
        "suggested_duration": "7–10 Days",
        "est_budget": "₹11,000 / day",
        "cities": ["Jerusalem", "Tel Aviv", "Haifa", "Dead Sea", "Eilat"],
        "highlights": ["Old City of Jerusalem & Western Wall", "Church of the Holy Sepulchre", "Dead Sea Floating", "Tel Aviv Promenade"],
        "food": ["Fresh Hummus & Pita", "Falafel", "Shakshuka", "Sabich", "Knafeh"],
        "attire": "Traditional Mediterranean & Levantine Linens"
    },
    "Egypt": {
        "flag": "🇪🇬",
        "tagline": "Timeless pharaonic pyramids along the legendary Nile River.",
        "capital": "Cairo",
        "currency": "Egyptian Pound (EGP E£)",
        "languages": "Arabic",
        "region": "North Africa",
        "best_season": "October–April (Comfortable desert climate)",
        "suggested_duration": "7–12 Days",
        "est_budget": "₹4,500 / day",
        "cities": ["Cairo", "Giza", "Luxor", "Aswan", "Alexandria", "Sharm El Sheikh"],
        "highlights": ["Great Pyramids of Giza & Sphinx", "Valley of the Kings Luxor", "Karnak Temple", "Nile River Felucca Cruise"],
        "food": ["Koshari", "Ful Medames", "Molokhia with Rice", "Shawarma", "Hawawshi"],
        "attire": "Traditional Galabeya Robe & Linen Tunics"
    },
    "South Africa": {
        "flag": "🇿🇦",
        "tagline": "The Rainbow Nation: thrilling safaris, Table Mountain, and coastal vineyards.",
        "capital": "Pretoria / Cape Town",
        "currency": "South African Rand (ZAR R)",
        "languages": "11 Official Languages (incl. English, Zulu, Xhosa)",
        "region": "Southern Africa",
        "best_season": "May–September (Safari Wildlife) & Nov–March (Cape Town Summer)",
        "suggested_duration": "8–15 Days",
        "est_budget": "₹7,500 / day",
        "cities": ["Cape Town", "Johannesburg", "Kruger National Park", "Durban", "Garden Route"],
        "highlights": ["Table Mountain Aerial Cableway", "Kruger Big Five Safari", "Cape of Good Hope", "Robben Island", "Stellenbosch Vineyards"],
        "food": ["Braai Barbecue", "Bobotie Spiced Casserole", "Biltong", "Bunny Chow", "Malva Pudding"],
        "attire": "Shweshwe Fabric Dresses & Traditional Zulu Beaded Attire"
    },
    "Australia": {
        "flag": "🇦🇺",
        "tagline": "Sun-kissed harbors, the Great Barrier Reef, and ancient Outback wonder.",
        "capital": "Canberra",
        "currency": "Australian Dollar (AUD A$)",
        "languages": "English",
        "region": "Oceania",
        "best_season": "September–November & March–May",
        "suggested_duration": "10–20 Days",
        "est_budget": "₹12,000 / day",
        "cities": ["Sydney", "Melbourne", "Brisbane", "Cairns", "Perth", "Gold Coast"],
        "highlights": ["Sydney Opera House & Harbor Bridge", "Great Barrier Reef", "Bondi Beach", "Great Ocean Road", "Uluru"],
        "food": ["Aussie Meat Pies", "Barramundi", "Avocado Toast & Flat White Coffee", "Pavlova", "Lamingtons"],
        "attire": "Australian Akubra Hat, Driza-Bone & Outback Bushwear"
    },
    "New Zealand": {
        "flag": "🇳🇿",
        "tagline": "Middle-earth fiords, dramatic glaciers, and geothermal marvels.",
        "capital": "Wellington",
        "currency": "New Zealand Dollar (NZD NZ$)",
        "languages": "English, Māori",
        "region": "Oceania",
        "best_season": "December–March (Summer Warmth) & June–August (Snow Sports)",
        "suggested_duration": "10–18 Days",
        "est_budget": "₹13,000 / day",
        "cities": ["Auckland", "Queenstown", "Rotorua", "Wellington", "Christchurch"],
        "highlights": ["Milford Sound Fiord", "Queenstown Adventure Hub", "Hobbiton Movie Set", "Rotorua Geothermal Parks", "Mount Cook"],
        "food": ["Hāngī Earth Oven Feast", "New Zealand Lamb", "Green-lipped Mussels", "Pavlova", "Hokey Pokey Ice Cream"],
        "attire": "Traditional Māori Korowai Cloak & Pure Merino Woolens"
    },
    "United States": {
        "flag": "🇺🇸",
        "tagline": "Epic national parks, legendary coastlines, and world-class metropolises.",
        "capital": "Washington, D.C.",
        "currency": "US Dollar (USD $)",
        "languages": "English",
        "region": "North America",
        "best_season": "May–September",
        "suggested_duration": "10–21 Days",
        "est_budget": "₹15,000 / day",
        "cities": ["New York City", "San Francisco", "Los Angeles", "Las Vegas", "Chicago", "Miami"],
        "highlights": ["Statue of Liberty & Manhattan", "Grand Canyon", "Yellowstone National Park", "Golden Gate Bridge", "Yosemite"],
        "food": ["Classic Cheeseburger", "New York Style Pizza", "Texas Slow-Smoked BBQ", "Clam Chowder", "Apple Pie"],
        "attire": "Denim Jeans & Jacket, Western Leather Boots, Stetson"
    },
    "Canada": {
        "flag": "🇨🇦",
        "tagline": "Turquoise glacial lakes, towering Rockies, and welcoming multicultural cities.",
        "capital": "Ottawa",
        "currency": "Canadian Dollar (CAD C$)",
        "languages": "English, French",
        "region": "North America",
        "best_season": "June–August (Lakes & Hiking) & Dec–March (Winter Sports)",
        "suggested_duration": "8–16 Days",
        "est_budget": "₹12,500 / day",
        "cities": ["Vancouver", "Toronto", "Montreal", "Banff", "Calgary", "Quebec City"],
        "highlights": ["Banff & Lake Louise", "Niagara Falls", "CN Tower Toronto", "Old Quebec City", "Whistler Blackcomb"],
        "food": ["Poutine with Cheese Curds", "Maple Syrup Treats", "Tourtière Meat Pie", "Nanaimo Bars", "Montreal Smoked Meat"],
        "attire": "Canadian Cowichan Wool Sweater & Heritage Plaid Flannel"
    },
    "Mexico": {
        "flag": "🇲🇽",
        "tagline": "Mayan ruins, vibrant mariachi heritage, and world-renowned gastronomy.",
        "capital": "Mexico City",
        "currency": "Mexican Peso (MXN $)",
        "languages": "Spanish",
        "region": "North America",
        "best_season": "November–April (Dry & Sunny)",
        "suggested_duration": "7–14 Days",
        "est_budget": "₹5,500 / day",
        "cities": ["Mexico City", "Cancun", "Oaxaca", "Guadalajara", "Playa del Carmen"],
        "highlights": ["Chichen Itza Mayan Pyramid", "Teotihuacan Pyramids", "Cenotes of Yucatan", "Frida Kahlo Museum", "Zocalo"],
        "food": ["Tacos al Pastor", "Mole Poblano", "Guacamole with Tortilla Chips", "Enchiladas", "Churros"],
        "attire": "Traje de Charro (Mariachi Attire) & Embroidered Huipil"
    },
    "Brazil": {
        "flag": "🇧🇷",
        "tagline": "Carnival rhythm, Amazonian wilderness, and sun-soaked golden sands.",
        "capital": "Brasília",
        "currency": "Brazilian Real (BRL R$)",
        "languages": "Portuguese",
        "region": "South America",
        "best_season": "December–March (Summer & Carnival) & May–Sept (Amazon & Pantanal)",
        "suggested_duration": "8–16 Days",
        "est_budget": "₹6,800 / day",
        "cities": ["Rio de Janeiro", "São Paulo", "Salvador", "Iguazu Falls", "Manaus"],
        "highlights": ["Christ the Redeemer", "Copacabana & Ipanema Beaches", "Sugarloaf Mountain", "Iguazu Falls", "Amazon Rainforest"],
        "food": ["Feijoada Black Bean Stew", "Pão de Queijo", "Churrasco Grilled Picanha", "Açaí Bowls", "Brigadeiro"],
        "attire": "Baiana de Acarajé Dress & Rio Carnival Costumes"
    },
    "United Kingdom": {
        "flag": "🇬🇧",
        "tagline": "Historic royal castles, rolling countryside, and cosmopolitan London.",
        "capital": "London",
        "currency": "British Pound (GBP £)",
        "languages": "English",
        "region": "Western Europe",
        "best_season": "May–September (Mild Weather)",
        "suggested_duration": "7–14 Days",
        "est_budget": "₹13,500 / day",
        "cities": ["London", "Edinburgh", "Oxford", "Bath", "Manchester", "York"],
        "highlights": ["Big Ben & Parliament", "Tower of London", "Edinburgh Castle", "Stonehenge", "Roman Baths"],
        "food": ["Traditional Fish & Chips", "Sunday Roast with Yorkshire Pudding", "Full English Breakfast", "Afternoon Tea & Scones"],
        "attire": "Scottish Highland Kilt & Tartan / Savile Row Wool Tweed"
    },
    "Germany": {
        "flag": "🇩🇪",
        "tagline": "Fairytale castles, historic Rhine valleys, and Bavarian culture.",
        "capital": "Berlin",
        "currency": "Euro (EUR €)",
        "languages": "German",
        "region": "Central Europe",
        "best_season": "May–September & December (Christmas Markets)",
        "suggested_duration": "7–12 Days",
        "est_budget": "₹9,800 / day",
        "cities": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne", "Dresden"],
        "highlights": ["Neuschwanstein Castle", "Brandenburg Gate", "Cologne Cathedral", "Black Forest", "Museum Island Berlin"],
        "food": ["Bratwurst & Currywurst", "Schnitzel", "Pretzels (Brezeln)", "Sauerbraten", "Black Forest Gateau"],
        "attire": "Bavarian Lederhosen (Men) & Dirndl Dress (Women)"
    },
    "Netherlands": {
        "flag": "🇳🇱",
        "tagline": "Picturesque canal networks, historic windmills, and vibrant art heritage.",
        "capital": "Amsterdam",
        "currency": "Euro (EUR €)",
        "languages": "Dutch, English",
        "region": "Western Europe",
        "best_season": "April–May (Tulip Season) & June–August",
        "suggested_duration": "5–8 Days",
        "est_budget": "₹10,500 / day",
        "cities": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Haarlem"],
        "highlights": ["Amsterdam Canal Ring", "Van Gogh Museum", "Rijksmuseum", "Zaanse Schans Windmills", "Keukenhof Gardens"],
        "food": ["Stroopwafels", "Bitterballen", "Gouda Cheese", "Haring (Pickled Herring)", "Poffertjes Pancakes"],
        "attire": "Traditional Dutch Volendam Klederdracht with Wooden Klompen Clogs"
    },
    "Portugal": {
        "flag": "🇵🇹",
        "tagline": "Sunlit cobblestone alleys, coastal castles, and soulful Fado music.",
        "capital": "Lisbon",
        "currency": "Euro (EUR €)",
        "languages": "Portuguese",
        "region": "Southern Europe",
        "best_season": "March–May & September–October",
        "suggested_duration": "6–10 Days",
        "est_budget": "₹7,800 / day",
        "cities": ["Lisbon", "Porto", "Sintra", "Algarve", "Coimbra"],
        "highlights": ["Pena Palace Sintra", "Belem Tower Lisbon", "Dom Luís I Bridge Porto", "Benagil Sea Caves Algarve", "Jerónimos Monastery"],
        "food": ["Pastéis de Nata Custard Tarts", "Bacalhau à Brás (Salt Cod)", "Francesinha Sandwich", "Sardinhas Assadas", "Port Wine"],
        "attire": "Minho Regional Traje à Vianesa with Filigree Gold Jewelry"
    }
}

CURATED_COUNTRIES = list(CURATED_30_DESTINATIONS.keys())


# ============================================================
# VERIFIED OFFICIAL EMERGENCY CONTACTS & SAFETY DIRECTORY
# Critical Rule: Never invent emergency numbers.
# Every number below is verified with official government & tourism sources.
# ============================================================

VERIFIED_EMERGENCY_CONTACTS = {
    "Japan": {
        "police": "110",
        "ambulance": "119",
        "fire": "119",
        "tourist_assistance": "0570-000-911 (JNTO Tourist Hotline) / +81 3 3201 3331",
        "source": "Japan National Police Agency & Japan National Tourism Organization (JNTO)",
        "source_url": "https://www.japan.travel/en/plan/emergency-assistance/",
        "verification_notes": "Police is 110; Fire and Ambulance is 119. English interpretation available in major prefectures.",
        "local_phrases": [
            ("Tasukete kudasai", "助けてください", "Please help me!"),
            ("Kyukyusha o yonde kudasai", "救急車を呼んでください", "Please call an ambulance!"),
            ("Keisatsu o yonde kudasai", "警察を呼んでください", "Please call the police!"),
            ("Kaji desu", "火事です", "There is a fire!")
        ]
    },
    "India": {
        "police": "112 / 100",
        "ambulance": "102 / 108",
        "fire": "101",
        "tourist_assistance": "1363 (24x7 Multi-lingual Tourist Infoline) / 1800 11 1363",
        "source": "Ministry of Home Affairs ERSS (Emergency Response Support System) & Ministry of Tourism, Govt of India",
        "source_url": "https://112.gov.in",
        "verification_notes": "112 is India's unified national emergency number active across all states and Union Territories. Tourist Helpline 1363 provides English and 10 foreign languages.",
        "local_phrases": [
            ("Madad kijiye", "मदद कीजिए", "Please help!"),
            ("Ambulance bulaiye", "एम्बुलेंस बुलाइए", "Please call an ambulance!"),
            ("Police ko bulaiye", "पुलिस को बुलाइए", "Please call the police!")
        ]
    },
    "France": {
        "police": "17 (Police Nationale)",
        "ambulance": "15 (SAMU - Medical Emergencies)",
        "fire": "18 (Sapeurs-Pompiers)",
        "tourist_assistance": "112 (European Universal Emergency)",
        "source": "Gouvernement de la République Française & European Emergency Number Association (EENA)",
        "source_url": "https://www.service-public.fr/particuliers/vosdroits/F33954",
        "verification_notes": "Dial 112 from any mobile or landline across France. Dial 15 directly for acute medical emergencies (SAMU).",
        "local_phrases": [
            ("Aidez-moi, s'il vous plaît", "Aidez-moi", "Help me please!"),
            ("Appelez une ambulance", "Appelez une ambulance", "Call an ambulance!"),
            ("Appelez la police", "Appelez la police", "Call the police!")
        ]
    },
    "Italy": {
        "police": "112 (Carabinieri / State Police 113)",
        "ambulance": "118 (Emergenza Sanitaria)",
        "fire": "115 (Vigili del Fuoco)",
        "tourist_assistance": "112 (Universal Emergency Service)",
        "source": "Ministero dell'Interno & EENA",
        "source_url": "https://www.interno.gov.it/it/servizi-e-linee-guida/linee-guida-e-normative/numero-unico-europeo-emergenza-112",
        "verification_notes": "112 is the Single European Emergency Number active across all regions in Italy with multilingual dispatch.",
        "local_phrases": [
            ("Aiuto!", "Aiuto!", "Help!"),
            ("Chiamate un'ambulanza", "Chiamate un'ambulanza", "Call an ambulance!"),
            ("Chiamate la polizia", "Chiamate la polizia", "Call the police!")
        ]
    },
    "Switzerland": {
        "police": "117",
        "ambulance": "144",
        "fire": "118",
        "tourist_assistance": "1414 (Swiss Alpine Air Rescue - REGA) / 112",
        "source": "Federal Department of Justice and Police (fedpol) & ch.ch",
        "source_url": "https://www.ch.ch/en/safety-and-justice/emergency-numbers/",
        "verification_notes": "112 works throughout Switzerland. 144 connects to medical ambulance dispatch. For mountain rescue, dial 1414.",
        "local_phrases": [
            ("Hilfe!", "Hilfe!", "Help! (German)"),
            ("Au secours!", "Au secours!", "Help! (French)"),
            ("Aiuto!", "Aiuto!", "Help! (Italian)")
        ]
    },
    "Greece": {
        "police": "100 / 112",
        "ambulance": "166 (EKAB - National Medical Ambulance)",
        "fire": "199",
        "tourist_assistance": "1571 (Hellenic Tourist Police)",
        "source": "Hellenic Police (astynomia.gr) & Ministry of Climate Crisis and Civil Protection",
        "source_url": "https://www.astynomia.gr",
        "verification_notes": "1571 is the Tourist Police helpline operating in English, French, and Greek. 112 operates nationwide.",
        "local_phrases": [
            ("Voithia!", "Βοήθεια!", "Help!"),
            ("Kalese ena asthenoforo", "Καλέστε ασθενοφόρο", "Call an ambulance!"),
            ("Kalese tin astynomia", "Καλέστε την αστυνομία", "Call the police!")
        ]
    },
    "Spain": {
        "police": "091 (Policía Nacional) / 062 (Guardia Civil)",
        "ambulance": "061 / 112 (Emergencias Médicas)",
        "fire": "080 / 085",
        "tourist_assistance": "112 (Universal Emergency) / +34 902 102 112 (SATE Tourist Care)",
        "source": "Ministerio del Interior & Dirección General de Protección Civil y Emergencias",
        "source_url": "https://www.proteccioncivil.es",
        "verification_notes": "112 is the primary multi-lingual emergency number in all autonomous communities of Spain.",
        "local_phrases": [
            ("¡Ayuda!", "¡Ayuda!", "Help!"),
            ("Llame a una ambulancia", "Llame a una ambulancia", "Call an ambulance!"),
            ("Llame a la policía", "Llame a la policía", "Call the police!")
        ]
    },
    "Turkey": {
        "police": "112 (Unified Emergency Service)",
        "ambulance": "112 (Acil Çağrı)",
        "fire": "112 (İtfaiye)",
        "tourist_assistance": "+90 212 527 4503 (Istanbul Tourist Police) / 112",
        "source": "Ministry of Interior Republic of Turkey (İçişleri Bakanlığı 112 Acil Çağrı Merkezi)",
        "source_url": "https://www.112.gov.tr",
        "verification_notes": "Turkey merged all emergency numbers (Police 155, Ambulance 112, Fire 110) into single unified 112 dispatch.",
        "local_phrases": [
            ("İmdat!", "İmdat!", "Help!"),
            ("Ambulans çağırın", "Ambulans çağırın", "Call an ambulance!"),
            ("Polis çağırın", "Polis çağırın", "Call the police!")
        ]
    },
    "Thailand": {
        "police": "191",
        "ambulance": "1669 (Medical Emergency & Rescue)",
        "fire": "199",
        "tourist_assistance": "1155 (Royal Thai Tourist Police - 24/7 English/Multi-language)",
        "source": "Tourist Police Bureau of Thailand & Tourism Authority of Thailand (TAT)",
        "source_url": "https://www.touristpolice.go.th",
        "verification_notes": "1155 is the primary hotline for international tourists in Thailand with English-speaking dispatchers.",
        "local_phrases": [
            ("Chuai duai!", "ช่วยด้วย", "Help!"),
            ("Riak rot phayaban", "เรียกรถพยาบาล", "Call an ambulance!"),
            ("Riak tamruat", "เรียกตำรวจ", "Call the police!")
        ]
    },
    "Indonesia": {
        "police": "110",
        "ambulance": "118 / 119",
        "fire": "113",
        "tourist_assistance": "112 (National Integrated Emergency Call) / 115 (Search & Rescue / BASARNAS)",
        "source": "Ministry of Communication and Information Technology & Kepolisian Negara Republik Indonesia (Polri)",
        "source_url": "https://layanan112.kominfo.go.id",
        "verification_notes": "112 is being phased across Indonesia for all services; 110 connects directly to Police dispatch.",
        "local_phrases": [
            ("Tolong!", "Tolong!", "Help!"),
            ("Panggil ambulans", "Panggil ambulans", "Call an ambulance!"),
            ("Panggil polisi", "Panggil polisi", "Call the police!")
        ]
    },
    "Vietnam": {
        "police": "113",
        "ambulance": "115 (Cấp cứu)",
        "fire": "114",
        "tourist_assistance": "113 (Police) / +84 24 3825 2246 (Hanoi Tourist Support)",
        "source": "Vietnam National Authority of Tourism & Ministry of Public Security (BCA)",
        "source_url": "https://vietnam.travel",
        "verification_notes": "Standard nationwide emergency numbers: 113 for police, 114 for fire, 115 for medical emergency.",
        "local_phrases": [
            ("Cứu tôi với!", "Cứu tôi với!", "Help me!"),
            ("Gọi cấp cứu", "Gọi cấp cứu", "Call an ambulance!"),
            ("Gọi công an", "Gọi công an", "Call the police!")
        ]
    },
    "Singapore": {
        "police": "999",
        "ambulance": "995 (SCDF Emergency Ambulance)",
        "fire": "995",
        "tourist_assistance": "1800 736 2000 (Singapore Tourism Board) / 1777 (Non-emergency Ambulance)",
        "source": "Singapore Civil Defence Force (SCDF) & Singapore Police Force (SPF)",
        "source_url": "https://www.scdf.gov.sg",
        "verification_notes": "995 is strictly for emergency ambulances and fire; non-emergency calls should use 1777. 999 for Police.",
        "local_phrases": [
            ("Help!", "Help!", "Universal language in Singapore is English.")
        ]
    },
    "Malaysia": {
        "police": "999",
        "ambulance": "999",
        "fire": "994 / 999",
        "tourist_assistance": "+60 3 2149 6590 (Kuala Lumpur Tourist Police)",
        "source": "Royal Malaysia Police (Polis Diraja Malaysia) & Ministry of Health Malaysia",
        "source_url": "https://www.rmp.gov.my",
        "verification_notes": "999 is the Malaysian Emergency Response Service (MERS) routing calls to police, ambulance, fire, and maritime rescue.",
        "local_phrases": [
            ("Tolong!", "Tolong!", "Help!"),
            ("Panggil ambulans", "Panggil ambulans", "Call an ambulance!"),
            ("Panggil polis", "Panggil polis", "Call the police!")
        ]
    },
    "South Korea": {
        "police": "112",
        "ambulance": "119",
        "fire": "119",
        "tourist_assistance": "1330 (Korea Travel Hotline - 24/7 in English, Japanese, Chinese)",
        "source": "Korea Tourism Organization (KTO) & National Police Agency",
        "source_url": "https://english.visitkorea.or.kr",
        "verification_notes": "1330 is an outstanding free 24/7 service operated by the tourism ministry offering live translation and emergency routing.",
        "local_phrases": [
            ("Dowajuseyo!", "도와주세요!", "Please help me!"),
            ("Gu-geup-cha bulleo juseyo", "구급차 불러주세요", "Please call an ambulance!"),
            ("Gyeongchal bulleo juseyo", "경찰 불러주세요", "Please call the police!")
        ]
    },
    "China": {
        "police": "110",
        "ambulance": "120",
        "fire": "119",
        "tourist_assistance": "12301 (National Tourism Service Hotline) / 122 (Traffic Accident)",
        "source": "Ministry of Public Security of the People's Republic of China",
        "source_url": "https://www.gov.cn",
        "verification_notes": "Police is 110; medical emergency is 120. English-speaking operators are present in major metropolitan centers like Beijing and Shanghai.",
        "local_phrases": [
            ("Jiù mìng a!", "救命啊！", "Help! (Save life!)"),
            ("Jiào jiù hù chē", "叫救护车", "Call an ambulance!"),
            ("Bào jǐng", "报警", "Call the police!")
        ]
    },
    "Nepal": {
        "police": "100",
        "ambulance": "102",
        "fire": "101",
        "tourist_assistance": "+977 1 4247041 / 1144 (Nepal Tourist Police Hotline, Bhrikutimandap)",
        "source": "Nepal Tourist Police & Nepal Tourism Board",
        "source_url": "https://nepalpolice.gov.np",
        "verification_notes": "Tourist Police (Hotline 1144) operates offices at Kathmandu Durbar Square, Thamel, Airport, and Pokhara.",
        "local_phrases": [
            ("Madat garnuhos!", "मद्दत गर्नुहोस्!", "Help me please!"),
            ("Ambulance bolaunuhos", "एम्बुलेन्स बोलाउनुहोस्", "Call an ambulance!"),
            ("Prahari bolaunuhos", "प्रहरी बोलाउनुहोस्", "Call the police!")
        ]
    },
    "United Arab Emirates": {
        "police": "999",
        "ambulance": "998",
        "fire": "997",
        "tourist_assistance": "901 (Dubai Police Non-Emergency & Tourist Security) / 800 4888",
        "source": "UAE Government Official Portal & Dubai Police General HQ",
        "source_url": "https://u.ae/en/information-and-services/justice-safety-and-the-law/emergency-services",
        "verification_notes": "Dial 999 for police, 998 for ambulance, 997 for fire. Coast Guard is 996. English and Arabic dispatched seamlessly.",
        "local_phrases": [
            ("Sa'idni!", "ساعدني!", "Help me!"),
            ("Ittasil bil-is'af", "اتصل بالإسعاف", "Call an ambulance!"),
            ("Ittasil bish-shurtah", "اتصل بالشرطة", "Call the police!")
        ]
    },
    "Israel": {
        "police": "100",
        "ambulance": "101 (Magen David Adom)",
        "fire": "102 (Israel Fire & Rescue)",
        "tourist_assistance": "112 / *3888 (Ministry of Tourism Tourist Info)",
        "source": "Israel Police (police.gov.il) & Magen David Adom (mdais.org)",
        "source_url": "https://www.gov.il/en/departments/israel_police",
        "verification_notes": "100 for police, 101 for medical emergency (Magen David Adom), 102 for fire. Mobile 112 connects directly.",
        "local_phrases": [
            ("Hatzilu!", "הצילו!", "Help!"),
            ("Hazminu ambulans", "הזמיنو אמבולנס", "Call an ambulance!"),
            ("Hazminu mishtara", "הזמינו משטרה", "Call the police!")
        ]
    },
    "Egypt": {
        "police": "122",
        "ambulance": "123",
        "fire": "180",
        "tourist_assistance": "126 (Egyptian Tourist Police Hotline)",
        "source": "Egyptian Tourism Authority & Ministry of Interior",
        "source_url": "https://www.experienceegypt.eg",
        "verification_notes": "126 connects directly to Tourist Police stationed at archaeological zones, airports, and tourist routes.",
        "local_phrases": [
            ("El-nagda!", "النجدة!", "Help!"),
            ("Ettasel bel-is'af", "اتصل بالإسعاف", "Call an ambulance!"),
            ("Ettasel bel-bolis", "اتصل بالبوليس", "Call the police!")
        ]
    },
    "South Africa": {
        "police": "10111 (Nationwide Police Flying Squad)",
        "ambulance": "10177 (Public Ambulance) / 084 124 (ER24) / 082 911 (Netcare)",
        "fire": "10177",
        "tourist_assistance": "112 (Universal Free Mobile Emergency) / 083 123 2345 (Tourism Safety Initiative)",
        "source": "South African Police Service (SAPS) & Department of Health",
        "source_url": "https://www.saps.gov.za",
        "verification_notes": "112 dials free from any cellphone on all networks and routes to the nearest dispatch center. 10111 is the national police response.",
        "local_phrases": [
            ("Help!", "Help!", "English is widely spoken across South Africa."),
            ("Gevaar!", "Gevaar!", "Danger! (Afrikaans)"),
            ("Siza!", "Siza!", "Help! (Zulu)")
        ]
    },
    "Australia": {
        "police": "000 (Triple Zero)",
        "ambulance": "000 (Triple Zero)",
        "fire": "000 (Triple Zero)",
        "tourist_assistance": "112 (from mobile phones) / 131 444 (Non-emergency Police)",
        "source": "Australian Government Emergency Services (Triple Zero)",
        "source_url": "https://www.triplezero.gov.au",
        "verification_notes": "Triple Zero (000) is Australia's primary emergency service number. 112 can also be dialed from digital mobile phones.",
        "local_phrases": [
            ("Help!", "Help!", "English is the national language of Australia.")
        ]
    },
    "New Zealand": {
        "police": "111",
        "ambulance": "111 (St John / Wellington Free Ambulance)",
        "fire": "111",
        "tourist_assistance": "105 (Non-Emergency Police Reporting) / 111",
        "source": "New Zealand Police (Ngā Pirihimana o Aotearoa) & Fire and Emergency New Zealand",
        "source_url": "https://www.police.govt.nz",
        "verification_notes": "Dial 111 in an emergency. For non-emergencies (lost passports, theft after the fact), dial 105 or go to 105.police.govt.nz.",
        "local_phrases": [
            ("Help!", "Help!", "English is standard."),
            ("Āwhina!", "Āwhina!", "Help! (Te Reo Māori)")
        ]
    },
    "United States": {
        "police": "911",
        "ambulance": "911",
        "fire": "911",
        "tourist_assistance": "311 (Non-Emergency Municipal Services) / 1-800-222-1222 (Poison Control)",
        "source": "Federal Communications Commission (FCC) & National 911 Program (911.gov)",
        "source_url": "https://www.911.gov",
        "verification_notes": "911 covers all police, medical ambulance, and fire rescue operations across all 50 states, DC, and territories.",
        "local_phrases": [
            ("Help!", "Help!", "English is the predominant language in the US.")
        ]
    },
    "Canada": {
        "police": "911",
        "ambulance": "911",
        "fire": "911",
        "tourist_assistance": "811 (Health Information Link) / 311 (Municipal Information)",
        "source": "Canadian Radio-television and Telecommunications Commission (CRTC) & Public Safety Canada",
        "source_url": "https://www.canada.ca/en/public-safety-canada.html",
        "verification_notes": "911 operates across Canada with dual-language service in English and French.",
        "local_phrases": [
            ("Help!", "Help!", "Help! (English)"),
            ("Au secours!", "Au secours!", "Help! (French)")
        ]
    },
    "Mexico": {
        "police": "911",
        "ambulance": "911 (Cruz Roja Mexicana)",
        "fire": "911",
        "tourist_assistance": "078 (Ángeles Verdes - Tourist Highway & Roadside Assistance)",
        "source": "Secretaría de Turismo (SECTUR) & Gobierno de México 911",
        "source_url": "https://www.gob.mx/sectur",
        "verification_notes": "911 is Mexico's nationwide emergency number. 078 connects to Green Angels (Ángeles Verdes) for bilingual tourist vehicle and medical roadside assistance.",
        "local_phrases": [
            ("¡Ayuda!", "¡Ayuda!", "Help!"),
            ("Llame a una ambulancia", "Llame a una ambulancia", "Call an ambulance!"),
            ("Llame a la policía", "Llame a la policía", "Call the police!")
        ]
    },
    "Brazil": {
        "police": "190 (Polícia Militar)",
        "ambulance": "192 (SAMU - Serviço de Atendimento Móvel de Urgência)",
        "fire": "193 (Corpo de Bombeiros)",
        "tourist_assistance": "190 / +55 21 2332 2924 (DEAT - Delegacia Especial de Apoio ao Turismo, Rio)",
        "source": "Ministério da Justiça e Segurança Pública do Brasil",
        "source_url": "https://www.gov.br/mj",
        "verification_notes": "190 connects directly to Military Police. Dial 192 for medical ambulances (SAMU). In Rio, DEAT provides specialized tourist police assistance.",
        "local_phrases": [
            ("Socorro!", "Socorro!", "Help!"),
            ("Chame uma ambulância", "Chame uma ambulância", "Call an ambulance!"),
            ("Chame a polícia", "Chame a polícia", "Call the police!")
        ]
    },
    "United Kingdom": {
        "police": "999 (Emergency) / 101 (Non-Emergency)",
        "ambulance": "999 (Emergency) / 111 (NHS Non-Emergency Health Advice)",
        "fire": "999",
        "tourist_assistance": "112 (European/Universal Emergency on any phone) / 101",
        "source": "UK Home Office & National Health Service (NHS)",
        "source_url": "https://www.police.uk",
        "verification_notes": "999 is the world's oldest automated emergency service. 112 connects to the same UK dispatch. Dial 111 for urgent but non-life-threatening medical guidance.",
        "local_phrases": [
            ("Help!", "Help!", "English is the national language of the UK.")
        ]
    },
    "Germany": {
        "police": "110 (Polizei)",
        "ambulance": "112 (Feuerwehr & Rettungsdienst)",
        "fire": "112",
        "tourist_assistance": "116 117 (Non-Emergency Medical On-Call Service) / 112",
        "source": "Bundesministerium des Innern und für Heimat & Bundespolizei",
        "source_url": "https://www.bmi.bund.de",
        "verification_notes": "110 connects directly to Police. 112 connects to Fire & Medical Ambulance. 116 117 provides out-of-hours doctor visits without an emergency room.",
        "local_phrases": [
            ("Hilfe!", "Hilfe!", "Help!"),
            ("Rufen Sie einen Krankenwagen", "Rufen Sie einen Krankenwagen", "Call an ambulance!"),
            ("Rufen Sie die Polizei", "Rufen Sie die Polizei", "Call the police!")
        ]
    },
    "Netherlands": {
        "police": "112 (Emergency) / 0900-8844 (Geen spoed, wel politie)",
        "ambulance": "112",
        "fire": "112",
        "tourist_assistance": "112 (Universal Emergency) / 0900-8844",
        "source": "Government of the Netherlands (Rijksoverheid) & Politie.nl",
        "source_url": "https://www.government.nl/topics/emergency-services",
        "verification_notes": "112 for all life-threatening emergencies. 0900-8844 for police matters that do not require sirens or immediate urgency.",
        "local_phrases": [
            ("Help!", "Help!", "Help! (Dutch)"),
            ("Bel een ambulance", "Bel een ambulance", "Call an ambulance!"),
            ("Bel de politie", "Bel de politie", "Call the police!")
        ]
    },
    "Portugal": {
        "police": "112 (PSP / GNR)",
        "ambulance": "112 (INEM - Instituto Nacional de Emergência Médica)",
        "fire": "112 (Bombeiros)",
        "tourist_assistance": "808 24 24 24 (SNS 24 - 24/7 Health Service Line) / 112",
        "source": "Ministério da Administração Interna & EENA",
        "source_url": "https://www.mai.gov.pt",
        "verification_notes": "112 is the Single National Emergency Number across Portugal, Azores, and Madeira islands with multilingual support.",
        "local_phrases": [
            ("Socorro!", "Socorro!", "Help!"),
            ("Chame uma ambulância", "Chame uma ambulância", "Call an ambulance!"),
            ("Chame a polícia", "Chame a polícia", "Call the police!")
        ]
    }
}


def get_verified_emergency_info(country_name: str) -> dict:
    """Returns reliably verified emergency services numbers and official source citations."""
    norm = normalize_country_name(country_name)
    if norm in VERIFIED_EMERGENCY_CONTACTS:
        return VERIFIED_EMERGENCY_CONTACTS[norm]
    for k, v in VERIFIED_EMERGENCY_CONTACTS.items():
        if k.lower() == country_name.lower() or k.lower() in country_name.lower():
            return v
    # Truthful global fallback: never invent numbers
    return {
        "police": "112 (GSM Mobile Universal Standard) or local station",
        "ambulance": "112 (GSM Mobile Universal Standard) or regional clinic",
        "fire": "112 (GSM Mobile Universal Standard) or local emergency services",
        "tourist_assistance": "Contact nearest Embassy, Consulate, or National Tourist Board",
        "source": "International Telecommunication Union (ITU) Standard GSM 112 & National Consular Services",
        "source_url": "https://www.itu.int",
        "verification_notes": "112 is recognized internationally on digital GSM mobile phones without a local SIM. For landline numbers in this destination, please consult official municipal listings or your accommodation host upon arrival.",
        "local_phrases": [
            ("Help me please!", "Help me please!", "Universal emergency phrase in English.")
        ]
    }


# ============================================================
# SAVED PLACES & FAVORITES MANAGEMENT
# ============================================================

def is_place_saved(name: str, country: str) -> bool:
    """Checks whether a destination or attraction is in saved_places."""
    saved = st.session_state.get("saved_places", [])
    return any(p.get("name") == name and p.get("country") == country for p in saved)


def toggle_save_place(place_dict: dict) -> bool:
    """Toggles saving a place in st.session_state.saved_places. Returns True if now saved, False if removed."""
    if "saved_places" not in st.session_state:
        st.session_state.saved_places = []
    name = place_dict.get("name")
    country = place_dict.get("country")
    existing_idx = next(
        (i for i, p in enumerate(st.session_state.saved_places) if p.get("name") == name and p.get("country") == country),
        None
    )
    if existing_idx is not None:
        st.session_state.saved_places.pop(existing_idx)
        return False
    else:
        st.session_state.saved_places.append(place_dict)
        return True


def add_place_to_itinerary(place_name: str, country: str, target_day: int = 1) -> bool:
    """Adds a custom attraction or saved place directly into the day-by-day itinerary."""
    if st.session_state.get("itinerary") is None:
        return False
    days_list = st.session_state.itinerary.get("days", [])
    if not days_list:
        return False
    day_idx = min(max(0, target_day - 1), len(days_list) - 1)
    new_act = {
        "time": "11:30",
        "activity": f"Visit {place_name}",
        "place": place_name,
        "cost": 500,
        "travel_time": "20 min",
        "transport": "Local transit"
    }
    days_list[day_idx].setdefault("activities", []).append(new_act)
    st.session_state.itinerary["total_cost"] = st.session_state.itinerary.get("total_cost", 0) + 500
    return True


# ============================================================
# NATURAL LANGUAGE TRIP REQUEST PARSER
# ============================================================

def parse_natural_language_trip(prompt_text: str) -> dict:
    """
    Parses natural language trip requests (e.g. 'Plan a 5-day trip to Japan under ₹80,000')
    into structured parameters that feed into the existing itinerary planner.
    """
    text = prompt_text.lower().strip()
    result = {}

    # Check for multi-stop journey prompt
    try:
        from multi_stop_planner import parse_multi_stop_trip_prompt, generate_multi_stop_journey
        parsed_multi = parse_multi_stop_trip_prompt(prompt_text)
        if parsed_multi and len(parsed_multi.get("stops", [])) >= 2:
            journey = generate_multi_stop_journey(parsed_multi)
            if journey:
                result["is_multi_stop"] = True
                result["multi_plan"] = journey
                result["destination"] = parsed_multi["stops"][0]["country"]
                result["days"] = journey["total_days"]
                result["budget"] = journey["budget"]
                result["travelers"] = journey["travelers"]
                result["style"] = journey["style"]
                return result
    except Exception:
        pass

    # Destination detection
    for c_name in CURATED_COUNTRIES:
        if c_name.lower() in text:
            result["destination"] = c_name
            break
    if "destination" not in result:
        for c_alias, c_canon in [
            ("usa", "United States"), ("america", "United States"), ("uk", "United Kingdom"),
            ("britain", "United Kingdom"), ("korea", "South Korea"), ("uae", "United Arab Emirates"),
            ("dubai", "United Arab Emirates"), ("england", "United Kingdom")
        ]:
            if c_alias in text:
                result["destination"] = c_canon
                break

    # Duration detection
    day_match = re.search(r'(\d+)\s*(?:-|–)?\s*(?:day|days)', text)
    if day_match:
        result["days"] = min(30, max(1, int(day_match.group(1))))
    elif any(w in text for w in ["one week", "1 week", "a week"]):
        result["days"] = 7
    elif any(w in text for w in ["two weeks", "2 weeks"]):
        result["days"] = 14
    elif any(w in text for w in ["a month", "one month"]):
        result["days"] = 30
    elif "weekend" in text:
        result["days"] = 3

    # Budget detection
    b_lakh = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|l)\b', text)
    if b_lakh:
        result["budget"] = int(float(b_lakh.group(1)) * 100000)
    else:
        b_k = re.search(r'(\d+(?:\.\d+)?)\s*k\b', text)
        if b_k:
            result["budget"] = int(float(b_k.group(1)) * 1000)
        else:
            b_num = re.search(r'(?:₹|rs\.?|inr)?\s*([0-9]{1,3}(?:,[0-9]{3})+|[0-9]{4,7})', text)
            if b_num:
                result["budget"] = int(b_num.group(1).replace(",", ""))

    # Travel style detection
    if any(w in text for w in ["relaxed", "peaceful", "slow", "honeymoon", "calm", "leisure"]):
        result["style"] = "Relaxed"
    elif any(w in text for w in ["packed", "fast", "action", "adventure", "maximize"]):
        result["style"] = "Packed"
    elif any(w in text for w in ["balanced", "moderate", "normal"]):
        result["style"] = "Balanced"

    # Travelers detection
    t_match = re.search(r'(\d+)\s*(?:traveler|traveller|person|people|adult)', text)
    if t_match:
        result["travelers"] = max(1, int(t_match.group(1)))
    elif any(w in text for w in ["couple", "honeymoon", "my partner", "my wife", "my husband"]):
        result["travelers"] = 2
    elif any(w in text for w in ["family", "with family"]):
        result["travelers"] = 4
    elif any(w in text for w in ["solo", "alone", "myself"]):
        result["travelers"] = 1

    # Interests detection
    interest_map = {
        "Food": ["food", "culinary", "dining", "cuisine", "dishes", "eat", "tasting", "ramen", "sushi"],
        "Culture": ["culture", "cultural", "heritage", "temple", "shrine", "monument", "historic", "history"],
        "Nature": ["nature", "scenery", "scenic", "mountains", "lakes", "parks", "hiking"],
        "Beaches": ["beach", "beaches", "coast", "island", "sea", "ocean"],
        "Photography": ["photography", "photos", "camera", "photogenic"],
        "Shopping": ["shopping", "markets", "souvenirs", "bazaar", "fashion"],
        "Adventure": ["adventure", "trekking", "rafting", "thrill", "skiing"],
        "Relaxation": ["peaceful", "relax", "spa", "wellness", "serene", "quiet"]
    }
    found_interests = [cat for cat, words in interest_map.items() if any(kw in text for kw in words)]
    if found_interests:
        result["interests"] = found_interests

    return result


# ============================================================
# API & IMAGE HEADERS CONFIGURATION
# ============================================================

WIKI_HEADERS = {
    "User-Agent": "AI-Based-Personalized-Travel-Planner/1.0 (contact@travelplanner.local)"
}

# Strict Quality Rule: No generic fallbacks or random stock images.
# Authentic verified photograph OR verified unavailable banner.


# ============================================================
# DISPLAY NAME CONVERSIONS (Formatting aliases for 17 formal ISO names)
# NOTE: The app supports all 249 countries via pycountry below.
# This dictionary ONLY shortens 17 formal bureaucratic UN names
# (e.g. "Russian Federation" -> "Russia", "Korea, Republic of" -> "South Korea").
# ============================================================

COUNTRY_DISPLAY_OVERRIDES = {
    "Russian Federation": "Russia",
    "Korea, Republic of": "South Korea",
    "Korea, Democratic People's Republic of": "North Korea",
    "Viet Nam": "Vietnam",
    "Lao People's Democratic Republic": "Laos",
    "Venezuela, Bolivarian Republic of": "Venezuela",
    "Bolivia, Plurinational State of": "Bolivia",
    "Tanzania, United Republic of": "Tanzania",
    "Iran, Islamic Republic of": "Iran",
    "Syrian Arab Republic": "Syria",
    "Moldova, Republic of": "Moldova",
    "Brunei Darussalam": "Brunei",
    "Palestine, State of": "Palestine",
    "Türkiye": "Turkey",
    "Czechia": "Czechia",
    "United States of America": "United States",
    "Micronesia, Federated States of": "Micronesia"
}


COUNTRY_ALIASES = {
    "United States": "United States",
    "Russia": "Russian Federation",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Vietnam": "Viet Nam",
    "Laos": "Lao People's Democratic Republic",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Bolivia": "Bolivia, Plurinational State of",
    "Tanzania": "Tanzania, United Republic of",
    "Iran": "Iran, Islamic Republic of",
    "Syria": "Syrian Arab Republic",
    "Moldova": "Moldova, Republic of",
    "Brunei": "Brunei Darussalam",
    "Palestine": "Palestine, State of",
    "Turkey": "Türkiye"
}


# ============================================================
# COUNTRY LIST
# ============================================================

country_records = []

for country in pycountry.countries:

    if not hasattr(country, "alpha_3"):
        continue

    display_name = COUNTRY_DISPLAY_OVERRIDES.get(
        country.name,
        country.name
    )

    country_records.append({
        "name": display_name,
        "iso3": country.alpha_3,
        "iso2": getattr(country, "alpha_2", None)
    })


# Remove duplicates
unique_records = {}

for record in country_records:
    unique_records[record["name"]] = record

country_records = sorted(
    unique_records.values(),
    key=lambda item: item["name"]
)

countries = [
    item["name"]
    for item in country_records
]

ISO3_TO_COUNTRY = {
    item["iso3"]: item["name"]
    for item in country_records
}

COUNTRY_TO_ISO3 = {
    item["name"]: item["iso3"]
    for item in country_records
}

COUNTRY_TO_ISO2 = {
    item["name"]: item["iso2"]
    for item in country_records
}

GLOBE_LOCATIONS = [
    record["iso3"]
    for record in country_records
    if record["iso3"]
]

GLOBE_DISPLAY_NAMES = [
    record["name"]
    for record in country_records
    if record["iso3"]
]

GLOBE_MARKER_LATS = []
GLOBE_MARKER_LONS = []
GLOBE_MARKER_NAMES = []

try:
    _data_path = os.path.join(os.path.dirname(__file__), "countries_data.json")
    if os.path.exists(_data_path):
        with open(_data_path, "r", encoding="utf-8") as _f:
            _local_db = json.load(_f)
        for _rec in country_records:
            _c_name = _rec["name"]
            _entry = _local_db.get(_c_name.lower())
            if not _entry:
                for _r in _local_db.values():
                    if _r.get("cca3") == _rec.get("iso3") or str(_r.get("name", "")).lower() == _c_name.lower():
                        _entry = _r
                        break
            if _entry and _entry.get("lat") is not None and _entry.get("lon") is not None:
                GLOBE_MARKER_LATS.append(float(_entry["lat"]))
                GLOBE_MARKER_LONS.append(float(_entry["lon"]))
                GLOBE_MARKER_NAMES.append(_c_name)
except Exception:
    pass



# ============================================================
# PAGE STYLING & MODERN TRAVEL DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #020817;
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Top Persistent Navigation Bar */
    .top-nav-bar {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(2, 6, 23, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 12px 20px;
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }

    .top-nav-brand-title {
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -0.3px;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .top-nav-brand-tagline {
        font-size: 11.5px;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 1px;
    }

    .top-nav-dest-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #38bdf8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Landing Screen Hero */
    .landing-hero {
        text-align: center;
        padding: 20px 10px 15px 10px;
    }

    .landing-hero-center {
        text-align: center;
        padding: 10px 14px;
    }

    .landing-plane-icon {
        font-size: 48px;
        margin-bottom: 8px;
        display: inline-block;
        filter: drop-shadow(0 4px 14px rgba(56, 189, 248, 0.45));
        animation: floatPlane 3.5s ease-in-out infinite;
    }

    @keyframes floatPlane {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-7px) rotate(2deg); }
    }

    .landing-pre-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .landing-main-title {
        font-size: 40px;
        font-weight: 900;
        letter-spacing: -0.5px;
        line-height: 1.15;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 6px 0 10px 0;
    }

    .landing-subtitle {
        font-size: 18px;
        color: #cbd5e1;
        font-weight: 600;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    .landing-description {
        font-size: 14.5px;
        color: #94a3b8;
        line-height: 1.6;
        max-width: 580px;
        margin: 0 auto 20px auto;
    }

    /* Hero Traveler Character Cards */
    .hero-character-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.7) 0%, rgba(2, 6, 23, 0.8) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 18px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        margin-bottom: 8px;
        transition: transform 0.25s ease;
    }

    .hero-character-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.45);
    }

    .hero-character-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #38bdf8;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .hero-character-footer {
        font-size: 12px;
        color: #94a3b8;
        font-style: italic;
        padding: 6px 4px;
        text-align: center;
    }

    /* Feature Highlights Grid */
    .landing-feature-card {
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 14px;
        text-align: center;
        transition: all 0.25s ease;
        height: 100%;
    }

    .landing-feature-card:hover {
        background: rgba(15, 23, 42, 0.85);
        border-color: rgba(56, 189, 248, 0.35);
        transform: translateY(-2px);
    }

    .landing-feature-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    .landing-feature-title {
        font-size: 15px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 6px;
    }

    .landing-feature-desc {
        font-size: 12.5px;
        color: #94a3b8;
        line-height: 1.45;
    }

    /* Page Header Box */
    .page-header-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }

    .page-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .page-title {
        font-size: 27px;
        font-weight: 800;
        color: #ffffff;
        margin: 2px 0 4px 0;
        letter-spacing: -0.3px;
    }

    .page-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin: 0;
        line-height: 1.45;
    }

    /* Dashboard Journey Header */
    .journey-header {
        text-align: center;
        padding: 10px 10px 5px 10px;
    }

    .journey-badge {
        display: inline-block;
        padding: 4px 16px;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #818cf8;
        font-size: 12.5px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .journey-title {
        font-size: 36px;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #f8fafc;
        margin: 4px 0;
    }

    .journey-cities {
        font-size: 15px;
        color: #94a3b8;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* Quick overview metric bar */
    .overview-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin: 14px 0 18px 0;
    }

    .overview-pill {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 7px 16px;
        border-radius: 30px;
        font-size: 13.5px;
        font-weight: 600;
        color: #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 10px;
        color: #f8fafc;
        letter-spacing: -0.2px;
    }

    .country-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .small-label {
        font-size: 12.5px;
        color: #9ca3af;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .country-info-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
        text-align: center;
    }

    .country-info-label {
        font-size: 11.5px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    .country-info-value {
        font-size: 14px;
        font-weight: 700;
        color: #f8fafc;
    }

    /* Streamlit widget polish */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 9px 22px !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
    }

    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.25) 0%, rgba(99, 102, 241, 0.25) 100%) !important;
        border-color: rgba(56, 189, 248, 0.45) !important;
        color: #38bdf8 !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .landing-main-title {
            font-size: 28px;
        }
        .landing-subtitle {
            font-size: 15px;
        }
        .journey-title {
            font-size: 26px;
        }
        .overview-bar {
            gap: 6px;
        }
        .overview-pill {
            font-size: 12px;
            padding: 5px 10px;
        }
        .top-nav-bar {
            flex-direction: column;
            gap: 8px;
            text-align: center;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# COUNTRY CODE HELPERS
# ============================================================

def get_country_code(country_name):

    if country_name in COUNTRY_TO_ISO3:
        return COUNTRY_TO_ISO3[country_name]

    lookup_name = COUNTRY_ALIASES.get(
        country_name,
        country_name
    )

    try:
        country = pycountry.countries.lookup(
            lookup_name
        )

        return country.alpha_3

    except Exception:
        return None


def get_country_alpha2(country_name):

    if country_name in COUNTRY_TO_ISO2:
        return COUNTRY_TO_ISO2[country_name]

    lookup_name = COUNTRY_ALIASES.get(
        country_name,
        country_name
    )

    try:

        country = pycountry.countries.lookup(
            lookup_name
        )

        return getattr(
            country,
            "alpha_2",
            None
        )

    except Exception:
        return None


def get_country_flag(country_name):
    alpha2 = get_country_alpha2(country_name)
    if alpha2 and len(alpha2) == 2:
        try:
            return chr(ord(alpha2[0].upper()) + 127397) + chr(ord(alpha2[1].upper()) + 127397)
        except Exception:
            pass
    return "🌍"


# ============================================================
# REST COUNTRIES & REGIONAL DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_local_countries_data():
    try:
        data_path = os.path.join(os.path.dirname(__file__), "countries_data.json")
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def get_country_api_data(country_name):
    lookup_name = COUNTRY_ALIASES.get(
        country_name,
        country_name
    )
    alpha2 = get_country_alpha2(country_name)

    # Comprehensive 250-country dataset (works offline without any API key)
    local_db = load_local_countries_data()
    if local_db:
        key = country_name.strip().lower()
        alias_key = lookup_name.strip().lower()
        matched = local_db.get(key) or local_db.get(alias_key)

        if not matched and alpha2:
            a2_upper = alpha2.upper()
            for rec in local_db.values():
                if rec.get("cca2", "").upper() == a2_upper:
                    matched = rec
                    break

        if not matched:
            iso3 = COUNTRY_TO_ISO3.get(country_name)
            if iso3:
                iso3_upper = iso3.upper()
                for rec in local_db.values():
                    if rec.get("cca3", "").upper() == iso3_upper:
                        matched = rec
                        break

        if matched:
            return matched

    return {}



# ============================================================
# COUNTRY INFORMATION
# ============================================================

COUNTRY_PROFILE_FALLBACKS = {
    "Nepal": {"flag":"🇳🇵","capital":"Kathmandu","currency":"Nepalese Rupee (NPR, रू)","languages":"Nepali","region":"Southern Asia (Asia)","duration":"5–10 days","budget":"₹25k–₹70k","season":"October–November / March–April"},
    "India": {"flag":"🇮🇳","capital":"New Delhi","currency":"Indian Rupee (INR, ₹)","languages":"Hindi, English and other regional languages","region":"Southern Asia (Asia)","duration":"7–14 days","budget":"₹30k–₹1.2L","season":"October–March"},
    "Israel": {"flag":"🇮🇱","capital":"Jerusalem","currency":"Israeli New Shekel (ILS, ₪)","languages":"Hebrew and Arabic","region":"Western Asia (Asia)","duration":"5–9 days","budget":"₹80k–₹1.8L","season":"March–May / September–November"},
    "Japan": {"flag":"🇯🇵","capital":"Tokyo","currency":"Japanese Yen (JPY, ¥)","languages":"Japanese","region":"Eastern Asia (Asia)","duration":"7–14 days","budget":"₹60k–₹1.8L","season":"March–May / October–November"},
    "China": {"flag":"🇨🇳","capital":"Beijing","currency":"Chinese Yuan (CNY, ¥)","languages":"Mandarin Chinese","region":"Eastern Asia (Asia)","duration":"7–14 days","budget":"₹60k–₹1.5L","season":"April–May / September–October"},
    "South Korea": {"flag":"🇰🇷","capital":"Seoul","currency":"South Korean Won (KRW, ₩)","languages":"Korean","region":"Eastern Asia (Asia)","duration":"6–10 days","budget":"₹60k–₹1.4L","season":"April–May / September–October"},
    "Thailand": {"flag":"🇹🇭","capital":"Bangkok","currency":"Thai Baht (THB, ฿)","languages":"Thai","region":"South-Eastern Asia (Asia)","duration":"5–10 days","budget":"₹35k–₹90k","season":"November–February"},
    "Vietnam": {"flag":"🇻🇳","capital":"Hanoi","currency":"Vietnamese Đồng (VND, ₫)","languages":"Vietnamese","region":"South-Eastern Asia (Asia)","duration":"7–12 days","budget":"₹35k–₹90k","season":"February–April / October–November"},
    "Indonesia": {"flag":"🇮🇩","capital":"Jakarta","currency":"Indonesian Rupiah (IDR, Rp)","languages":"Indonesian","region":"South-Eastern Asia (Asia)","duration":"7–12 days","budget":"₹35k–₹90k","season":"May–September"},
    "Malaysia": {"flag":"🇲🇾","capital":"Kuala Lumpur","currency":"Malaysian Ringgit (MYR, RM)","languages":"Malay, English and Chinese varieties","region":"South-Eastern Asia (Asia)","duration":"5–10 days","budget":"₹35k–₹90k","season":"December–March / June–August"},
    "Singapore": {"flag":"🇸🇬","capital":"Singapore","currency":"Singapore Dollar (SGD, S$)","languages":"English, Malay, Mandarin and Tamil","region":"South-Eastern Asia (Asia)","duration":"3–5 days","budget":"₹45k–₹1.1L","season":"February–April"},
    "Sri Lanka": {"flag":"🇱🇰","capital":"Sri Jayawardenepura Kotte","currency":"Sri Lankan Rupee (LKR, Rs)","languages":"Sinhala and Tamil","region":"Southern Asia (Asia)","duration":"6–10 days","budget":"₹30k–₹80k","season":"December–March / May–September"},
    "Bangladesh": {"flag":"🇧🇩","capital":"Dhaka","currency":"Bangladeshi Taka (BDT, ৳)","languages":"Bengali","region":"Southern Asia (Asia)","duration":"5–8 days","budget":"₹25k–₹60k","season":"November–February"},
    "Pakistan": {"flag":"🇵🇰","capital":"Islamabad","currency":"Pakistani Rupee (PKR, Rs)","languages":"Urdu and English","region":"Southern Asia (Asia)","duration":"6–10 days","budget":"₹30k–₹80k","season":"October–March"},
    "United Arab Emirates": {"flag":"🇦🇪","capital":"Abu Dhabi","currency":"UAE Dirham (AED, د.إ)","languages":"Arabic and English","region":"Western Asia (Asia)","duration":"4–7 days","budget":"₹60k–₹1.5L","season":"November–March"},
    "Saudi Arabia": {"flag":"🇸🇦","capital":"Riyadh","currency":"Saudi Riyal (SAR, ﷼)","languages":"Arabic","region":"Western Asia (Asia)","duration":"5–9 days","budget":"₹55k–₹1.3L","season":"October–March"},
    "Turkey": {"flag":"🇹🇷","capital":"Ankara","currency":"Turkish Lira (TRY, ₺)","languages":"Turkish","region":"Western Asia / Southern Europe","duration":"7–12 days","budget":"₹55k–₹1.3L","season":"April–June / September–October"},
    "Italy": {"flag":"🇮🇹","capital":"Rome","currency":"Euro (EUR, €)","languages":"Italian","region":"Southern Europe (Europe)","duration":"7–12 days","budget":"₹90k–₹2.2L","season":"April–June / September–October"},
    "France": {"flag":"🇫🇷","capital":"Paris","currency":"Euro (EUR, €)","languages":"French","region":"Western Europe (Europe)","duration":"7–12 days","budget":"₹90k–₹2.2L","season":"April–June / September–October"},
    "Spain": {"flag":"🇪🇸","capital":"Madrid","currency":"Euro (EUR, €)","languages":"Spanish and regional languages","region":"Southern Europe (Europe)","duration":"7–12 days","budget":"₹80k–₹1.8L","season":"April–June / September–October"},
    "Greece": {"flag":"🇬🇷","capital":"Athens","currency":"Euro (EUR, €)","languages":"Greek","region":"Southern Europe (Europe)","duration":"6–10 days","budget":"₹80k–₹1.8L","season":"April–June / September–October"},
    "Germany": {"flag":"🇩🇪","capital":"Berlin","currency":"Euro (EUR, €)","languages":"German","region":"Western Europe (Europe)","duration":"7–12 days","budget":"₹85k–₹2L","season":"May–September"},
    "United Kingdom": {"flag":"🇬🇧","capital":"London","currency":"Pound Sterling (GBP, £)","languages":"English and regional languages","region":"Northern Europe (Europe)","duration":"7–12 days","budget":"₹1L–₹2.3L","season":"May–September"},
    "United States": {"flag":"🇺🇸","capital":"Washington, D.C.","currency":"United States Dollar (USD, $)","languages":"English and many other languages","region":"Northern America (Americas)","duration":"10–21 days","budget":"₹1.2L–₹3L+","season":"April–June / September–October"},
    "Mexico": {"flag":"🇲🇽","capital":"Mexico City","currency":"Mexican Peso (MXN, $)","languages":"Spanish and Indigenous languages","region":"Central America (Americas)","duration":"7–14 days","budget":"₹60k–₹1.5L","season":"November–April"},
    "Brazil": {"flag":"🇧🇷","capital":"Brasília","currency":"Brazilian Real (BRL, R$)","languages":"Portuguese","region":"South America (Americas)","duration":"10–18 days","budget":"₹80k–₹2L","season":"May–October"},
    "Australia": {"flag":"🇦🇺","capital":"Canberra","currency":"Australian Dollar (AUD, A$)","languages":"English and many community languages","region":"Australia and New Zealand (Oceania)","duration":"10–21 days","budget":"₹1.3L–₹3L+","season":"September–November / March–May"},
    "Canada": {"flag":"🇨🇦","capital":"Ottawa","currency":"Canadian Dollar (CAD, C$)","languages":"English and French","region":"Northern America (Americas)","duration":"10–21 days","budget":"₹1.2L–₹2.8L+","season":"June–September"},
    "Egypt": {"flag":"🇪🇬","capital":"Cairo","currency":"Egyptian Pound (EGP, £)","languages":"Arabic","region":"Northern Africa (Africa)","duration":"6–10 days","budget":"₹45k–₹1L","season":"October–April"},
    "South Africa": {"flag":"🇿🇦","capital":"Pretoria / Cape Town / Bloemfontein","currency":"South African Rand (ZAR, R)","languages":"English, Afrikaans and African languages","region":"Southern Africa (Africa)","duration":"8–14 days","budget":"₹70k–₹1.5L","season":"May–September"},
    "Switzerland": {"flag":"🇨🇭","capital":"Bern","currency":"Swiss Franc (CHF, CHF)","languages":"German, French, Italian and Romansh","region":"Western Europe (Europe)","duration":"6–10 days","budget":"₹1L–₹2.3L","season":"June–September / December–February"}
}


def get_country_profile(country_name):

    api_data = get_country_api_data(country_name)
    planner_data = country_info(country_name) or {}
    fallback = COUNTRY_PROFILE_FALLBACKS.get(country_name, {})

    flag = api_data.get("flag") or fallback.get("flag") or planner_data.get("flag") or get_country_flag(country_name) or "🌍"

    capital_value = api_data.get("capital")
    if isinstance(capital_value, list):
        capital = ", ".join(str(item) for item in capital_value if item)
    elif isinstance(capital_value, str):
        capital = capital_value.strip()
    else:
        capital = ""
    capital = capital or fallback.get("capital") or "Capital information is unavailable."

    currencies = api_data.get("currencies") or api_data.get("currency")
    currency_names = []
    if isinstance(currencies, dict):
        for code, currency_data in currencies.items():
            if isinstance(currency_data, dict):
                name = currency_data.get("name") or code
                symbol = currency_data.get("symbol") or ""
                currency_names.append(
                    f"{name} ({code}, {symbol})" if symbol else f"{name} ({code})"
                )
            elif isinstance(currency_data, str):
                currency_names.append(f"{currency_data} ({code})")
    elif isinstance(currencies, str) and currencies.strip():
        currency_names = [currencies.strip()]
    elif isinstance(currencies, list):
        currency_names = [str(c) for c in currencies if c]

    currency = ", ".join(currency_names) if currency_names else fallback.get("currency")
    currency = currency or "Currency information is unavailable."

    languages = api_data.get("languages")
    if isinstance(languages, dict):
        language_names = list(languages.values())
    elif isinstance(languages, list):
        language_names = languages
    elif isinstance(languages, str) and languages.strip():
        language_names = [languages.strip()]
    else:
        language_names = []
    language_text = ", ".join(str(value) for value in language_names if value)
    language_text = language_text or fallback.get("languages") or "Language information is unavailable."

    region = str(api_data.get("region") or "").strip()
    subregion = str(api_data.get("subregion") or "").strip()
    if subregion and region and subregion.lower() not in region.lower():
        region_text = f"{subregion} ({region})"
    else:
        region_text = region or subregion or fallback.get("region") or "Regional information is unavailable."

    population = api_data.get("population")
    if isinstance(population, (int, float)) and population > 0:
        population_text = f"{int(population):,}"
    else:
        population_text = "Population information is unavailable."

    duration = planner_data.get("duration") or fallback.get("duration") or "5–10 days"
    budget = planner_data.get("budget") or fallback.get("budget") or "Varies by city, season and travel style"
    season = planner_data.get("season") or fallback.get("season") or "Depends on regional climate"

    area = subregion or region or fallback.get("region", "")
    description = (
        f"{country_name} is located in {area}. Its capital is {capital}. Explore its landmarks, "
        f"local cuisine, culture and natural attractions."
        if area and capital and capital != "Capital information is unavailable."
        else f"Explore the landmarks, local cuisine, culture and natural attractions of {country_name}."
    )

    return {
        "name": country_name,
        "flag": flag,
        "capital": capital,
        "currency": currency,
        "languages": language_text,
        "region": region_text,
        "population": population_text,
        "duration": duration,
        "budget": budget,
        "season": season,
        "description": description
    }



# ============================================================
# STARTING LOCATION SEARCH
# ============================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def search_locations(query):

    if not query or len(query.strip()) < 3:
        return []

    try:

        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "json",
                "addressdetails": 1,
                "limit": 8,
                "accept-language": "en"
            },
            headers={
                "User-Agent":
                    "AI-Based-Personalized-Travel-Planner/1.0"
            },
            timeout=10
        )

        if response.status_code != 200:
            return []

        results = response.json()

        locations = []

        for result in results:

            display_name = result.get(
                "display_name"
            )

            if display_name:
                locations.append(
                    display_name
                )

        return locations

    except Exception:
        return []


# ============================================================
# COUNTRY CENTER FOR GLOBE
# ============================================================

@st.cache_data(
    ttl=604800,
    show_spinner=False
)
def get_country_center(country_name):
    # 1. Instant centroid lookup from bundled 250-country database
    local_db = load_local_countries_data()
    if local_db:
        c_lower = country_name.strip().lower()
        rec = local_db.get(c_lower)
        if not rec:
            for r in local_db.values():
                if r.get("name", "").strip().lower() == c_lower or r.get("official_name", "").strip().lower() == c_lower:
                    rec = r
                    break
        if rec and rec.get("lat") is not None and rec.get("lon") is not None:
            return (float(rec["lon"]), float(rec["lat"]))

    # 2. Remote fallback with compliant user-agent
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": country_name,
                "format": "json",
                "limit": 1,
                "featuretype": "country",
                "accept-language": "en"
            },
            headers=WIKI_HEADERS,
            timeout=5
        )

        if response.status_code == 200:
            results = response.json()
            if results:
                return (
                    float(results[0]["lon"]),
                    float(results[0]["lat"])
                )

    except Exception:
        pass

    return (0, 20)


# ============================================================
# TOURIST PLACE DATA
# ============================================================

TOURIST_PLACES = {

    "India": [
        ("Taj Mahal", "Agra"),
        ("Golden Temple", "Amritsar"),
        ("India Gate", "New Delhi"),
        ("Meenakshi Temple", "Madurai"),
        ("Srinagar", "Jammu & Kashmir"),
        ("Dal Lake", "Srinagar (Jammu & Kashmir)"),
        ("Gulmarg", "Jammu & Kashmir"),
        ("Pahalgam", "Jammu & Kashmir"),
        ("Sonamarg", "Jammu & Kashmir"),
        ("Mughal Gardens", "Srinagar (Jammu & Kashmir)"),
        ("Shankaracharya Temple", "Srinagar (Jammu & Kashmir)"),
        ("Tirumala Temple", "Tirupati"),
        ("Jaipur", "Rajasthan"),
        ("Goa", "Goa"),
        ("Varanasi", "Uttar Pradesh"),
        ("Kerala Backwaters", "Kerala")
    ],

    "Nepal": [
        ("Mount Everest", "Solukhumbu"),
        ("Pashupatinath Temple", "Kathmandu"),
        ("Boudhanath Stupa", "Kathmandu"),
        ("Kathmandu Durbar Square", "Kathmandu"),
        ("Phewa Lake", "Pokhara"),
        ("Swayambhunath", "Kathmandu"),
        ("Chitwan National Park", "Chitwan"),
        ("Peace Pagoda (Shanti Stupa)", "Pokhara")
    ],

    "France": [
        ("Eiffel Tower", "Paris"),
        ("Louvre Museum", "Paris"),
        ("Palace of Versailles", "Versailles"),
        ("Nice", "French Riviera"),
        ("Mont Saint-Michel", "Normandy"),
        ("Lyon Old Town", "Lyon")
    ],

    "Japan": [
        ("Mount Fuji", "Yamanashi / Shizuoka"),
        ("Fushimi Inari Shrine", "Kyoto"),
        ("Tokyo Tower", "Tokyo"),
        ("Tokyo", "Tokyo"),
        ("Osaka", "Osaka"),
        ("Hiroshima Peace Memorial", "Hiroshima")
    ],

    "Italy": [
        ("Colosseum", "Rome"),
        ("Venice Grand Canal", "Venice"),
        ("Leaning Tower of Pisa", "Pisa"),
        ("Florence Cathedral", "Florence"),
        ("Trevi Fountain", "Rome"),
        ("Lake Como", "Lombardy")
    ],

    "Thailand": [
        ("Grand Palace", "Bangkok"),
        ("Wat Arun", "Bangkok"),
        ("Phuket", "Phuket"),
        ("Railay Beach", "Krabi"),
        ("Chiang Mai Old City", "Chiang Mai"),
        ("Phi Phi Islands", "Krabi")
    ],

    "Israel": [
        ("Old City of Jerusalem", "Jerusalem"),
        ("Dead Sea", "Dead Sea"),
        ("Tel Aviv", "Tel Aviv"),
        ("Masada", "Southern District"),
        ("Sea of Galilee", "Galilee"),
        ("Haifa", "Haifa")
    ],

    "United States": [
        ("Statue of Liberty", "New York"),
        ("Grand Canyon", "Arizona"),
        ("Times Square", "New York"),
        ("Yellowstone National Park", "Wyoming"),
        ("Golden Gate Bridge", "San Francisco"),
        ("Walt Disney World", "Florida")
    ],

    "United Kingdom": [
        ("Big Ben", "London"),
        ("Tower of London", "London"),
        ("Stonehenge", "Wiltshire"),
        ("Edinburgh Castle", "Edinburgh"),
        ("Lake District", "Cumbria"),
        ("Buckingham Palace", "London")
    ],

    "Spain": [
        ("Sagrada Família", "Barcelona"),
        ("Alhambra", "Granada"),
        ("Park Güell", "Barcelona"),
        ("Royal Palace of Madrid", "Madrid"),
        ("Seville Cathedral", "Seville"),
        ("Ibiza", "Balearic Islands")
    ],

    "Greece": [
        ("Acropolis of Athens", "Athens"),
        ("Santorini", "Cyclades"),
        ("Mykonos", "Cyclades"),
        ("Meteora", "Thessaly"),
        ("Delphi", "Central Greece"),
        ("Crete", "Crete")
    ],

    "Switzerland": [
        ("Matterhorn", "Zermatt"),
        ("Lake Geneva", "Geneva"),
        ("Jungfraujoch", "Bernese Alps"),
        ("Lucerne", "Lucerne"),
        ("Interlaken", "Bernese Oberland"),
        ("Rhine Falls", "Schaffhausen")
    ],

    "Germany": [
        ("Brandenburg Gate", "Berlin"),
        ("Neuschwanstein Castle", "Bavaria"),
        ("Cologne Cathedral", "Cologne"),
        ("Black Forest", "Baden-Württemberg"),
        ("Museum Island", "Berlin"),
        ("Hamburg Port", "Hamburg")
    ],

    "Australia": [
        ("Sydney Opera House", "Sydney"),
        ("Great Barrier Reef", "Queensland"),
        ("Uluru", "Northern Territory"),
        ("Bondi Beach", "Sydney"),
        ("Great Ocean Road", "Victoria"),
        ("Melbourne", "Victoria")
    ],

    "China": [
        ("Great Wall of China", "Beijing"),
        ("Forbidden City", "Beijing"),
        ("Terracotta Army", "Xi'an"),
        ("The Bund", "Shanghai"),
        ("Zhangjiajie", "Hunan"),
        ("West Lake", "Hangzhou")
    ],

    "South Korea": [
        ("Gyeongbokgung Palace", "Seoul"),
        ("N Seoul Tower", "Seoul"),
        ("Jeju Island", "Jeju"),
        ("Bukchon Hanok Village", "Seoul"),
        ("Busan", "Busan"),
        ("Changdeokgung Palace", "Seoul")
    ],

    "Singapore": [
        ("Marina Bay Sands", "Singapore"),
        ("Gardens by the Bay", "Singapore"),
        ("Sentosa Island", "Singapore"),
        ("Merlion Park", "Singapore"),
        ("Singapore Zoo", "Singapore"),
        ("Chinatown", "Singapore")
    ],

    "United Arab Emirates": [
        ("Burj Khalifa", "Dubai"),
        ("Sheikh Zayed Grand Mosque", "Abu Dhabi"),
        ("Palm Jumeirah", "Dubai"),
        ("Dubai Marina", "Dubai"),
        ("Louvre Abu Dhabi", "Abu Dhabi"),
        ("Dubai Creek", "Dubai")
    ],

    "Turkey": [
        ("Hagia Sophia", "Istanbul"),
        ("Blue Mosque", "Istanbul"),
        ("Cappadocia", "Nevşehir"),
        ("Pamukkale", "Denizli"),
        ("Topkapi Palace", "Istanbul"),
        ("Ephesus", "Selçuk")
    ],

    "Egypt": [
        ("Great Pyramid of Giza", "Giza"),
        ("Valley of the Kings", "Luxor"),
        ("Karnak Temple", "Luxor"),
        ("Abu Simbel", "Aswan"),
        ("Egyptian Museum", "Cairo"),
        ("Nile River", "Egypt")
    ],

    "Nepal": [
        ("Mount Everest", "Solukhumbu"),
        ("Kathmandu Durbar Square", "Kathmandu"),
        ("Pokhara", "Gandaki"),
        ("Phewa Lake", "Pokhara"),
        ("Chitwan National Park", "Chitwan"),
        ("Swayambhunath", "Kathmandu")
    ],

    "Vietnam": [
        ("Ha Long Bay", "Quang Ninh"),
        ("Hoi An Ancient Town", "Hoi An"),
        ("Ho Chi Minh City", "Ho Chi Minh City"),
        ("Hanoi Old Quarter", "Hanoi"),
        ("Da Nang", "Da Nang"),
        ("Phong Nha Caves", "Quang Binh")
    ],

    "Indonesia": [
        ("Bali", "Bali"),
        ("Borobudur", "Central Java"),
        ("Ubud", "Bali"),
        ("Komodo National Park", "East Nusa Tenggara"),
        ("Mount Bromo", "East Java"),
        ("Tanah Lot", "Bali")
    ],

    "Brazil": [
        ("Christ the Redeemer", "Rio de Janeiro"),
        ("Copacabana Beach", "Rio de Janeiro"),
        ("Iguazu Falls", "Paraná"),
        ("Amazon Rainforest", "Amazonas"),
        ("Sugarloaf Mountain", "Rio de Janeiro"),
        ("Salvador", "Bahia")
    ]
}


# ============================================================
# FOOD DATA
# ============================================================

FOOD_DATA = {

    "India": [
        ("Biryani", "Aromatic rice cooked with spices, herbs and meat or vegetables."),
        ("Masala Dosa", "A crisp South Indian fermented rice and lentil crepe served with sambar and coconut chutney."),
        ("Butter Chicken", "Creamy tomato-based chicken curry with rich Indian spices."),
        ("Idli", "Soft, fluffy steamed savory cakes made of fermented rice and black lentils, served with hot sambar and fresh coconut chutney."),
        ("Samosa", "Crispy golden fried pastry stuffed with spiced potatoes, green peas and herbs."),
        ("Rogan Josh", "Slow-cooked Kashmiri aromatic lamb curry infused with Kashmiri spices and saffron."),
        ("Kashmiri Kahwa", "Traditional green tea infused with saffron strands, crushed almonds and cardamom."),
        ("Chole Bhature", "Spiced chickpeas served with fluffy fried bread."),
        ("Gulab Jamun", "Soft milk-based sweets soaked in fragrant sugar syrup.")
    ],

    "Nepal": [
        ("Momo", "Steamed Nepali dumplings filled with spiced vegetables or minced meat, served with fiery tomato-sesame achar."),
        ("Dal Bhat", "Nutritious traditional platter with steamed rice, spiced lentil soup, seasonal vegetable curry, and pickles."),
        ("Thukpa", "Comforting Himalayan hot noodle soup with fresh vegetables, coriander, and mountain spices."),
        ("Sel Roti", "Traditional ring-shaped sweet fried rice-flour bread prepared during festive celebrations."),
        ("Choila & Newari Khaja", "Spicy grilled marinated meat paired with beaten rice and fermented mustard greens."),
        ("Juju Dhau", "Rich, creamy 'King Curd' sweet yogurt traditionally served in clay pots in Bhaktapur.")
    ],

    "France": [
        ("Croissant", "A buttery, flaky pastry commonly enjoyed for breakfast."),
        ("Baguette", "A long crusty French bread with a soft interior."),
        ("Crêpes", "Thin French pancakes served with sweet or savory fillings."),
        ("Ratatouille", "A vegetable dish made with tomato, zucchini, eggplant and herbs."),
        ("French Cheese", "France is famous for a wide variety of regional cheeses."),
        ("Macarons", "Delicate almond meringue cookies with flavorful fillings.")
    ],

    "Japan": [
        ("Sushi", "Vinegared rice paired with seafood, vegetables or other toppings."),
        ("Ramen", "Japanese noodle soup served with broth and different toppings."),
        ("Onigiri", "Rice balls commonly filled with savory ingredients."),
        ("Japanese Curry", "A mild and rich curry commonly served with rice."),
        ("Gyoza", "Pan-fried Japanese dumplings with a savory filling."),
        ("Tempura", "Seafood or vegetables lightly battered and fried.")
    ],

    "Italy": [
        ("Pizza", "Classic Italian flatbread topped with tomato, cheese and other ingredients."),
        ("Pasta", "A huge variety of Italian pasta dishes prepared with different sauces."),
        ("Gelato", "Italian-style frozen dessert known for its dense texture and flavor."),
        ("Risotto", "Creamy rice dish traditionally cooked slowly with broth."),
        ("Tiramisu", "Coffee-flavored Italian dessert layered with mascarpone."),
        ("Lasagna", "Layered pasta dish with sauce, cheese and other fillings.")
    ],

    "Thailand": [
        ("Pad Thai", "Stir-fried rice noodles with vegetables, sauce and optional protein."),
        ("Tom Yum", "A hot and sour Thai soup with aromatic herbs."),
        ("Mango Sticky Rice", "Sweet sticky rice served with ripe mango and coconut."),
        ("Green Curry", "Fragrant curry made with green curry paste and coconut milk."),
        ("Som Tam", "Spicy green papaya salad with a fresh, tangy flavor."),
        ("Tom Kha", "Creamy coconut soup flavored with galangal and herbs.")
    ],

    "Israel": [
        ("Falafel", "Crispy chickpea or fava-bean fritters commonly served in pita."),
        ("Hummus", "Creamy chickpea dip prepared with tahini, lemon and garlic."),
        ("Shakshuka", "Eggs cooked in a spiced tomato and pepper sauce."),
        ("Sabich", "Pita filled with eggplant, egg, salad and sauces."),
        ("Babka", "Sweet braided bread with rich chocolate or cinnamon filling."),
        ("Malabi", "Creamy milk pudding often served with syrup and nuts.")
    ],

    "Spain": [
        ("Paella", "A famous Spanish rice dish traditionally associated with Valencia."),
        ("Tapas", "Small savory dishes served in many Spanish dining settings."),
        ("Churros", "Fried dough pastries commonly served with chocolate."),
        ("Gazpacho", "Cold vegetable soup especially popular in southern Spain."),
        ("Tortilla Española", "Spanish omelette made mainly with potatoes and eggs.")
    ],

    "Germany": [
        ("Bratwurst", "Traditional grilled German pork sausage spiced with marjoram and caraway, served with mustard.", "Bratwurst"),
        ("Schnitzel", "Crispy pan-fried breaded cutlet served with lemon wedges and warm potato salad.", "Schnitzel"),
        ("Sauerbraten", "Tender pot roast marinated for days in wine, vinegar, and aromatics, served with red cabbage.", "Sauerbraten"),
        ("Pretzel", "Traditional Bavarian baked twisted knot pastry with a deep brown crust and coarse sea salt.", "Pretzel"),
        ("Black Forest Cake", "Rich layered chocolate sponge cake filled with whipped cream, sour cherries, and Kirsch.", "Black_Forest_gateau")
    ],

    "Greece": [
        ("Moussaka", "Layered baked dish commonly made with eggplant, meat and béchamel."),
        ("Souvlaki", "Grilled skewered meat served with bread or pita and sides."),
        ("Greek Salad", "Fresh salad with tomato, cucumber, olives and feta."),
        ("Baklava", "Sweet layered pastry with nuts and syrup."),
        ("Tzatziki", "Cool yogurt-based dip with cucumber, garlic and herbs.")
    ],

    "Turkey": [
        ("Kebab", "Grilled meat dishes prepared in many regional Turkish styles."),
        ("Baklava", "Layered pastry filled with nuts and sweet syrup."),
        ("Lahmacun", "Thin flatbread topped with seasoned minced meat and vegetables."),
        ("Menemen", "Egg dish cooked with tomatoes, peppers and spices."),
        ("Turkish Delight", "Soft confection traditionally flavored with fruits or nuts.")
    ],

    "China": [
        ("Dim Sum", "A collection of small steamed, fried or baked dishes."),
        ("Peking Duck", "Roasted duck traditionally served with thin pancakes and sauces."),
        ("Kung Pao Chicken", "Spicy stir-fried chicken with peanuts and vegetables."),
        ("Mapo Tofu", "Spicy tofu dish with a rich Sichuan-style sauce.", "Mapo_tofu"),
        ("Fried Rice", "Rice stir-fried with vegetables, eggs and other ingredients.")
    ],

    "South Korea": [
        ("Kimchi", "Fermented vegetables, especially cabbage, seasoned with spices."),
        ("Bibimbap", "Rice topped with vegetables, egg, meat and spicy sauce."),
        ("Bulgogi", "Thinly sliced marinated meat grilled or cooked over high heat."),
        ("Tteokbokki", "Chewy rice cakes cooked in a spicy sauce."),
        ("Japchae", "Glass noodles stir-fried with vegetables and other ingredients.")
    ],

    "Vietnam": [
        ("Pho", "Fragrant noodle soup usually served with herbs and meat."),
        ("Banh Mi", "Vietnamese baguette sandwich with savory fillings and herbs."),
        ("Bun Cha", "Grilled pork served with noodles, herbs and dipping sauce."),
        ("Goi Cuon", "Fresh rice-paper rolls with vegetables, herbs and fillings."),
        ("Cao Lau", "Regional noodle dish associated with Hoi An.")
    ],

    "Indonesia": [
        ("Nasi Goreng", "Indonesian-style fried rice with savory seasonings."),
        ("Satay", "Grilled skewers served with flavorful sauces."),
        ("Rendang", "Slow-cooked spiced meat dish associated with West Sumatra."),
        ("Gado-Gado", "Vegetable salad served with rich peanut sauce."),
        ("Soto", "A family of Indonesian soups with regional variations.")
    ],

    "Mexico": [
        ("Tacos", "Tortillas filled with meat, vegetables, salsa and other toppings."),
        ("Guacamole", "Avocado-based dip commonly served with Mexican dishes."),
        ("Enchiladas", "Filled tortillas covered with sauce and often cheese."),
        ("Churros", "Fried dough pastry often served with sugar and cinnamon."),
        ("Mole", "Complex sauce combining chilies, spices and other ingredients.")
    ],

    "United States": [
        ("Hamburger", "Classic sandwich made with a seasoned meat or plant-based patty."),
        ("Barbecue Ribs", "Slow-cooked ribs prepared with regional barbecue sauces."),
        ("Apple Pie", "Traditional baked dessert with spiced apple filling."),
        ("Pancakes", "Fluffy breakfast cakes commonly served with syrup."),
        ("Clam Chowder", "Creamy soup especially associated with New England.")
    ],

    "United Kingdom": [
        ("Fish and Chips", "Fried fish served with thick-cut chips."),
        ("Full English Breakfast", "Hearty breakfast with eggs, toast and several savory sides."),
        ("Shepherd's Pie", "Savory meat and vegetable filling topped with mashed potato."),
        ("Afternoon Tea", "Tea served with sandwiches, scones and small cakes."),
        ("Sticky Toffee Pudding", "Warm dessert served with rich toffee sauce.")
    ],

    "United Arab Emirates": [
        ("Machboos", "Spiced rice dish commonly prepared with meat or seafood."),
        ("Shawarma", "Seasoned roasted meat served in flatbread with sauces."),
        ("Luqaimat", "Small sweet dumplings served with syrup or date flavors."),
        ("Harees", "Slow-cooked wheat and meat dish with a soft texture."),
        ("Knafeh", "Sweet cheese-based dessert with crisp pastry and syrup.")
    ],

    "Argentina": [
        ("Asado Criollo", "Legendary Argentine barbecue featuring prime beef cuts (tira de asado, vacío) grilled over slow-burning wood embers.", "Asado"),
        ("Empanadas Argentinas", "Crisp baked crescent pastries stuffed with spiced knife-cut beef, sautéed onions, hard-boiled egg, and green olives.", "Empanada"),
        ("Milanesa Napolitana", "Thin, crispy breaded beef cutlet topped with rich tomato sauce, cooked ham, and melted mozzarella cheese.", "Milanesa"),
        ("Choripán con Chimichurri", "Grilled artisanal chorizo sausage served in a crusty bread roll with fresh, zesty garlic-herb chimichurri sauce.", "Chorip%C3%A1n"),
        ("Locro Criollo", "Thick traditional hearty stew made with white corn hominy, beans, squash, and varied cuts of beef and pork.", "Locro"),
        ("Dulce de Leche Alfajores", "Delicate crumbly shortbread sandwich cookies generously filled with thick dulce de leche caramel and rolled in coconut.", "Alfajor")
    ],

    "Peru": [
        ("Ceviche Tradicional", "Fresh raw corvina or sea bass cured in tangy key lime juice, tossed with red onion, ají limo pepper, sweet potato, and choclo.", "Ceviche"),
        ("Lomo Saltado", "Vibrant stir-fry combining tender beef tenderloin strips, red onions, and juicy tomatoes with crispy french fries and white rice.", "Lomo_saltado"),
        ("Causa Limeña", "Layered cold potato cake prepared with yellow ají amarillo paste and lime, layered with savory tuna or chicken salad and avocado.", "Causa_a_la_lime%C3%B1a"),
        ("Ají de Gallina", "Shredded chicken in a creamy, velvety sauce made from ají amarillo chilies, cream, evaporated milk, ground walnuts, and parmesan.", "Aj%C3%AD_de_gallina"),
        ("Anticuchos de Corazón", "Skewered, marinated beef heart grilled over charcoal, basted with ají panca chili sauce and garlic, served with boiled potatoes.", "Anticuchos"),
        ("Picarones con Miel de Chancaca", "Sweet potato and squash fried dough rings drizzled with warm, spiced molasses syrup (miel de chancaca).", "Picarones")
    ],

    "Morocco": [
        ("Tagine de Poulet aux Olives", "Tender chicken slow-simmered in a conical earthenware tagine with preserved lemons, green olives, ginger, and saffron.", "Tagine"),
        ("Couscous Royale", "Fluffy hand-rolled steamed semolina grains crowned with seven vegetables, tender lamb, and a flavorful saffron broth.", "Couscous"),
        ("Pastilla (Bastilla)", "Layers of paper-thin crispy pastry encasing tender spiced pigeon or chicken, toasted crushed almonds, cinnamon, and sugar.", "Pastilla"),
        ("Harira Soup", "Velvety traditional soup simmered with tomatoes, chickpeas, lentils, fresh coriander, and warm warming spices.", "Harira"),
        ("Zaalouk", "Smoky roasted eggplant and tomato cooked salad seasoned with garlic, cumin, sweet paprika, and olive oil.", "Zaalouk"),
        ("Moroccan Mint Tea & Pastries", "Sweet green tea brewed with fresh spearmint leaves, paired with crescent-shaped almond pastries.", "Maghrebi_mint_tea")
    ],

    "Saudi Arabia": [
        ("Kabsa", "The national dish of long-grain basmati rice cooked in rich spiced meat broth, topped with tender roasted lamb and toasted nuts.", "Kabsa"),
        ("Mandi", "Smoky, slow-cooked tender meat and spiced yellow rice prepared in a traditional underground tandoor oven.", "Mandi_(food)"),
        ("Shawarma", "Thin shavings of marinated chicken or beef carved from a vertical spit, wrapped in warm flatbread with creamy garlic sauce.", "Shawarma"),
        ("Harees", "Comforting ancient dish of slow-simmered cracked wheat and shredded tender meat, whipped to a smooth porridge with ghee.", "Harees"),
        ("Kunafa", "Shredded filo pastry soaked in fragrant orange blossom syrup, filled with warm melted cheese and topped with pistachios.", "Kanafeh"),
        ("Mutabbaq", "Crispy pan-fried folded square pastry filled with spiced minced meat, beaten egg, scallions, and green chilies.", "Murtabak")
    ],

    "Ireland": [
        ("Traditional Irish Stew", "Hearty slow-cooked stew of tender lamb or mutton neck, carrots, onions, and potatoes in rich savory broth.", "Irish_stew"),
        ("Boxty Potato Pancakes", "Traditional potato pancakes made from grated raw and mashed cooked potatoes, fried to a golden crisp.", "Boxty"),
        ("Shepherd's Pie", "Richly seasoned minced lamb cooked with peas and carrots in red wine gravy, topped with creamy piped mashed potatoes.", "Shepherd%27s_pie"),
        ("Colcannon", "Creamy buttery mashed potatoes folded with tender steamed kale or green cabbage and spring onions.", "Colcannon"),
        ("Irish Soda Bread", "Dense, crusty quick bread baked with stone-ground wholemeal flour, buttermilk, and butter, served warm.", "Soda_bread"),
        ("Sticky Toffee Pudding", "Moist date sponge cake soaked in rich toffee sauce, served warm with vanilla custard or cream.", "Sticky_toffee_pudding")
    ],

    "Norway": [
        ("Kjøttkaker (Norwegian Meatballs)", "Hearty, spiced minced beef and pork meatballs simmered in rich brown gravy, served with mushy peas and boiled potatoes.", "Kj%C3%B8ttkaker"),
        ("Fårikål", "The official national dish: slow-simmered mutton or lamb layered with green cabbage, whole black peppercorns, and pan juices.", "F%C3%A5rik%C3%A5l"),
        ("Gravlax with Mustard-Dill Sauce", "Delicate salt-and-sugar cured raw salmon seasoned with fresh dill, served thinly sliced on crisp rye bread.", "Gravlax"),
        ("Smoked Salmon Smørbrød", "Traditional open-faced sandwich on dense rye bread topped with Norwegian smoked salmon, scrambled eggs, and fresh dill.", "Sm%C3%B8rrebr%C3%B8d"),
        ("Brunost Waffles", "Hearty heart-shaped Scandinavian waffles topped with sweet caramelized brown goat's cheese (brunost) and jam.", "Brunost"),
        ("Klippfisk / Bacalao", "Dried and salted cod stewed with tomatoes, red peppers, onions, and olive oil in the coastal Norwegian style.", "Dried_and_salted_cod")
    ],

    "Sweden": [
        ("Köttbullar (Swedish Meatballs)", "Tender allspice-infused beef and pork meatballs served with creamy gravy, tart lingonberry jam, and buttery potatoes.", "K%C3%B6ttbullar"),
        ("Toast Skagen", "Classic Swedish appetizer featuring fresh peeled shrimp tossed in mayonnaise, sour cream, and dill on butter-fried toast.", "Toast_Skagen"),
        ("Gravlax", "Dill-cured Atlantic salmon sliced paper-thin, served with sweet hovmästarsås mustard sauce and boiled potatoes.", "Gravlax"),
        ("Janssons Frestelse", "Comforting potato gratin layered with tender julienned potatoes, onions, pickled sprats, and rich heavy cream.", "Janssons_frestelse"),
        ("Kanelbulle (Cinnamon Bun)", "Fluffy cardamom-infused yeast dough rolled with cinnamon sugar butter, topped with crunchy white pearl sugar.", "Cinnamon_roll"),
        ("Prinsesstårta (Princess Cake)", "Domed sponge cake layered with sweet raspberry jam, rich vanilla custard, and whipped cream under pastel green marzipan.", "Princess_cake")
    ],

    "Netherlands": [
        ("Stroopwafel", "Two thin, crisp waffle wafers filled with warm, gooey caramel cinnamon syrup, eaten over a hot cup of coffee.", "Stroopwafel"),
        ("Bitterballen", "Crispy, deep-fried breaded croquette balls filled with rich beef ragout, served hot with tangy Dijon mustard.", "Bitterballen"),
        ("Stamppot", "Traditional comfort food consisting of mashed potatoes mixed with curly kale or endive, crowned with smoked rookworst sausage.", "Stamppot"),
        ("Hollandse Nieuwe Haring", "Raw soused Atlantic herring served fresh with finely chopped raw onions and tangy gherkin pickles.", "Sous_herring"),
        ("Poffertjes", "Miniature fluffy, spongy yeast pancakes baked in special dimpled pans, served warm with melting butter and powdered sugar.", "Poffertjes"),
        ("Snert (Dutch Split Pea Soup)", "Thick, hearty green split pea soup slow-cooked with pork belly, celery root, leeks, and slices of rookworst.", "Pea_soup")
    ],

    "Poland": [
        ("Pierogi", "Handmade dumplings stuffed with savory potato and cheese (ruskie), braised meat, or wild mushrooms, pan-fried with onions.", "Pierogi"),
        ("Bigos (Hunter's Stew)", "Rich slow-cooked stew combining white sauerkraut, fresh cabbage, varied cuts of pork, venison, and wild mushrooms.", "Bigos"),
        ("Żurek", "Distinctive sour rye flour soup simmered with white Polish sausage, hard-boiled eggs, garlic, and fresh marjoram.", "%C5%BBurek"),
        ("Kotlet Schabowy", "Crispy breaded and pan-fried pork cutlet, served with buttery dill boiled potatoes and shredded cabbage salad.", "Kotlet_schabowy"),
        ("Gołąbki", "Tender white cabbage leaves stuffed with minced pork and seasoned rice, baked in a rich tomato sauce.", "Cabbage_roll"),
        ("Sernik", "Traditional Polish cheesecake baked with rich twaróg curd cheese, citrus peel, and sweet sultanas.", "Cheesecake")
    ],

    "Philippines": [
        ("Chicken Adobo", "The national dish: tender chicken braised slowly in vinegar, soy sauce, garlic, bay leaves, and black peppercorns.", "Philippine_adobo"),
        ("Sinigang na Baboy", "Sour and savory comforting soup featuring tender pork, kangkong, and radish in a tangy tamarind broth.", "Sinigang"),
        ("Lechon", "Whole roasted suckling pig slow-roasted over hot coals until the skin reaches an incomparable glass-like crunch.", "Lechon"),
        ("Pancit Canton", "Stir-fried egg wheat noodles cooked with sliced chicken, shrimp, shredded cabbage, carrots, and calamansi lime.", "Pancit"),
        ("Kare-Kare", "Rich and comforting stew of tender oxtail and tripe simmered in a thick, savory peanut sauce with bagoong shrimp paste.", "Kare-kare"),
        ("Halo-Halo", "Spectacular dessert of crushed ice, sweet condensed milk, ube halaya, leche flan, sago pearls, and sweet red beans.", "Halo-halo")
    ],

    "New Zealand": [
        ("Māori Hāngī", "Ancient traditional feast of pork, lamb, kumara (sweet potato), and pumpkin slow-steamed under earth and hot volcanic rocks.", "H%C4%81ng%C4%AB"),
        ("Traditional Kiwi Meat Pie", "Individual golden flaky pastry pie stuffed with slow-braised minced steak, rich onion gravy, and cheddar.", "Meat_pie"),
        ("Pavlova with Kiwifruit", "Airy meringue dessert with a crisp crust and soft, marshmallow-like center, topped with fresh whipped cream and sliced kiwi.", "Pavlova_(dessert)"),
        ("Fish and Chips", "Freshly caught local snapper or tarakihi deep-fried in golden batter, served with chips and lemon wedges.", "Fish_and_chips"),
        ("Whitebait Fritters", "Delicate golden egg patties studded with tiny, sweet coastal whitebait fish, seasoned with lemon and sea salt.", "Whitebait"),
        ("Lamingtons", "Light, fluffy sponge cake squares dipped in sweet chocolate glaze and generously coated in desiccated coconut.", "Lamington")
    ],

    "Canada": [
        ("Poutine", "Crispy hot French fries and fresh squeaky cheese curds smothered in savory brown gravy.", "Poutine"),
        ("Butter Tarts", "Classic Canadian flaky pastry tart filled with rich, gooey butter, sugar, syrup, and egg filling.", "Butter_tart"),
        ("Tourtière", "Traditional French-Canadian spiced minced pork, veal, or beef pie baked in a flaky golden pastry crust.", "Tourti%C3%A8re"),
        ("Nanaimo Bars", "Beloved Canadian no-bake layered dessert bar with coconut crumb base, custard icing, and chocolate ganache.", "Nanaimo_bar"),
        ("Montreal Smoked Meat", "Cured and spiced beef brisket smoked to perfection and steamed, sliced thin and served on rye bread with yellow mustard.", "Montreal-style_smoked_meat"),
        ("Peameal Bacon Sandwich", "Grilled thick slices of cured lean pork loin rolled in cornmeal, served hot on a soft bakery bun.", "Peameal_bacon")
    ],

    "Australia": [
        ("Aussie Meat Pie", "Iconic individual flaky pastry pie stuffed with slow-braised minced beef, rich gravy, and onions, served with tomato sauce.", "Meat_pie_(Australia_and_New_Zealand)"),
        ("Pavlova", "Crisp, airy meringue dessert topped with fresh whipped cream and colorful fresh passionfruit, kiwi, and berries.", "Pavlova_(dessert)"),
        ("Lamingtons", "Light and fluffy sponge cake squares coated in chocolate glaze and generously rolled in desiccated coconut.", "Lamington"),
        ("Barramundi", "Pan-seared Australian wild-caught barramundi fish served with crisp skin, lemon butter, and sea salt.", "Barramundi"),
        ("Chicken Parmigiana", "Crisp crumbed chicken breast schnitzel topped with rich napolitana tomato sauce, leg ham, and melted mozzarella.", "Chicken_parmigiana"),
        ("Anzac Biscuits", "Sweet, crunchy rolled oat and golden syrup drop biscuits traditionally baked since World War I.", "Anzac_biscuit")
    ],

    "Brazil": [
        ("Feijoada", "The national dish of Brazil: rich slow-simmered black bean stew with varied cuts of pork and beef, served with rice, farofa, and orange.", "Feijoada"),
        ("Moqueca", "Fragrant Afro-Brazilian seafood stew made with fresh fish, bell peppers, tomatoes, garlic, coconut milk, and golden dendê oil.", "Moqueca"),
        ("Pão de Queijo", "Chewy, warm baked cheese bread rolls made with tapioca cassava starch and savory cured Brazilian cheese.", "P%C3%A3o_de_queijo"),
        ("Brigadeiro", "Iconic Brazilian chocolate fudge truffles rolled in chocolate sprinkles, traditionally made with sweetened condensed milk and butter.", "Brigadeiro"),
        ("Coxinha", "Tear-drop shaped crispy deep-fried croquettes filled with shredded spiced chicken and creamy catupiry cheese.", "Coxinha"),
        ("Acarajé", "Crispy deep-fried peeled black-eyed pea fritters split open and stuffed with spicy vatapá paste, caruru, and dried shrimp.", "Acaraj%C3%A9")
    ],

    "Egypt": [
        ("Koshari", "Egypt's national comfort food: layered lentils, rice, macaroni, spiced chickpeas, crispy fried onions, and garlic-vinegar tomato sauce.", "Kushari"),
        ("Ful Medames", "Ancient staple of slow-cooked fava beans seasoned with extra virgin olive oil, lemon juice, crushed cumin, and fresh herbs.", "Ful_medames"),
        ("Molokhia", "Traditional green soup prepared from finely minced jute mallow leaves simmered in rich coriander-garlic broth with chicken.", "Mulukhiyah"),
        ("Egyptian Shawarma", "Thinly carved spiced beef or chicken wrapped in warm pita flatbread with tahini, tomatoes, and pickled turnip.", "Shawarma"),
        ("Umm Ali", "Traditional Egyptian bread pudding baked with flaky pastry, milk, sweetened cream, raisins, coconut flakes, and toasted nuts.", "Om_Ali"),
        ("Taameya", "Egyptian falafel made from crushed fava beans and fresh herbs, fried to a crisp golden exterior and sprinkled with sesame.", "Falafel")
    ],

    "South Africa": [
        ("Bobotie", "South Africa's national dish: spiced minced beef baked with an aromatic egg-and-milk custard topping, served with yellow turmeric rice.", "Bobotie"),
        ("Boerewors", "Traditional spiral farmer's beef and pork sausage spiced with roasted coriander seeds, black pepper, and nutmeg.", "Boerewors"),
        ("Bunny Chow", "Durban specialty consisting of a hollowed-out loaf of white bread filled with fiery slow-cooked lamb or chicken curry.", "Bunny_chow"),
        ("Biltong", "Traditional spiced and cured air-dried beef strips seasoned with vinegar, crushed coriander, black pepper, and brown sugar.", "Biltong"),
        ("Malva Pudding", "Sweet, spongy caramelized apricot jam pudding drenched in warm cream-butter sauce, served with vanilla custard.", "Malva_pudding"),
        ("Potjiekos", "Slow-cooked stew of meat and layered vegetables simmered outdoors in a traditional three-legged cast-iron pot over open embers.", "Potjiekos")
    ]
}

FOOD_DATA["USA"] = FOOD_DATA.get("United States", [])



# ============================================================
# RELIGIOUS PLACES
# ============================================================

RELIGIOUS_PLACES = {

    "India": [
        ("Tirumala Venkateswara Temple", "Tirupati"),
        ("Meenakshi Amman Temple", "Madurai"),
        ("Jagannath Temple", "Puri"),
        ("Kedarnath Temple", "Uttarakhand"),
        ("Golden Temple", "Amritsar")
    ],

    "Japan": [
        ("Fushimi Inari Shrine", "Kyoto"),
        ("Senso-ji", "Tokyo"),
        ("Kinkaku-ji", "Kyoto"),
        ("Todai-ji", "Nara"),
        ("Meiji Shrine", "Tokyo")
    ],

    "France": [
        ("Notre-Dame de Paris", "Paris"),
        ("Sacré-Cœur", "Paris"),
        ("Chartres Cathedral", "Chartres"),
        ("Reims Cathedral", "Reims"),
        ("Mont Saint-Michel Abbey", "Normandy")
    ],

    "Italy": [
        ("St. Peter's Basilica", "Vatican City / Rome"),
        ("Milan Cathedral", "Milan"),
        ("Basilica of Saint Francis", "Assisi"),
        ("St. Mark's Basilica", "Venice"),
        ("Pantheon", "Rome")
    ],

    "Thailand": [
        ("Wat Arun", "Bangkok"),
        ("Wat Pho", "Bangkok"),
        ("Temple of the Emerald Buddha", "Bangkok"),
        ("Wat Phra That Doi Suthep", "Chiang Mai"),
        ("White Temple", "Chiang Rai")
    ],

    "Israel": [
        ("Western Wall", "Jerusalem"),
        ("Church of the Holy Sepulchre", "Jerusalem"),
        ("Dome of the Rock", "Jerusalem"),
        ("Basilica of the Annunciation", "Nazareth"),
        ("Church of the Nativity", "Bethlehem")
    ],

    "Spain": [
        ("Sagrada Família", "Barcelona"),
        ("Córdoba Mosque-Cathedral", "Córdoba"),
        ("Santiago de Compostela Cathedral", "Santiago de Compostela"),
        ("Toledo Cathedral", "Toledo"),
        ("Almudena Cathedral", "Madrid")
    ],

    "Greece": [
        ("Parthenon", "Athens"),
        ("Meteora Monasteries", "Thessaly"),
        ("Temple of Apollo", "Delphi"),
        ("Church of Saint Demetrius", "Thessaloniki")
    ],

    "Turkey": [
        ("Hagia Sophia", "Istanbul"),
        ("Blue Mosque", "Istanbul"),
        ("Süleymaniye Mosque", "Istanbul"),
        ("Mevlana Museum", "Konya")
    ],

    "Egypt": [
        ("Al-Azhar Mosque", "Cairo"),
        ("Abu Simbel Temples", "Aswan"),
        ("Karnak Temple", "Luxor"),
        ("Philae Temple", "Aswan")
    ],

    "China": [
        ("Temple of Heaven", "Beijing"),
        ("Jokhang Temple", "Lhasa"),
        ("Lama Temple", "Beijing"),
        ("Longmen Grottoes", "Luoyang")
    ],

    "Nepal": [
        ("Pashupatinath Temple", "Kathmandu"),
        ("Swayambhunath", "Kathmandu"),
        ("Boudhanath Stupa", "Kathmandu"),
        ("Muktinath Temple", "Mustang")
    ],

    "Indonesia": [
        ("Borobudur Temple", "Central Java"),
        ("Prambanan Temple", "Central Java"),
        ("Tanah Lot", "Bali"),
        ("Besakih Temple", "Bali")
    ]
}


FALLBACK_FOOD_DATA = {
    "Nepal": [("Dal Bhat","Steamed rice served with lentil soup and vegetable or curry sides."),("Momo","Nepali dumplings filled with vegetables or meat and served with chutney."),("Thukpa","A warming noodle soup with vegetables, herbs and optional meat."),("Sel Roti","Traditional ring-shaped rice bread commonly prepared for festivals."),("Newari Khaja","Traditional Newar snacks and savory dishes from the Kathmandu Valley.")],
    "Malaysia": [("Nasi Lemak","Coconut rice served with sambal, peanuts, anchovies and accompaniments."),("Char Kway Teow","Stir-fried flat rice noodles with savory seasonings and varied toppings."),("Laksa","Spiced noodle soup with regional Malaysian varieties."),("Roti Canai","Flaky flatbread commonly served with curry."),("Satay","Grilled skewers served with peanut sauce.")],
    "Singapore": [("Hainanese Chicken Rice","Chicken served with fragrant seasoned rice."),("Chilli Crab","Crab cooked in a rich sweet and spicy sauce."),("Laksa","Spicy noodle soup with coconut milk and aromatic spices."),("Char Kway Teow","Stir-fried flat rice noodles with savory toppings."),("Kaya Toast","Toasted bread with coconut-egg jam, often served with eggs and tea.")],
    "Sri Lanka": [("Rice and Curry","Rice served with vegetable, lentil, meat or fish curries."),("Kottu Roti","Chopped flatbread stir-fried with vegetables, egg or meat."),("Hoppers","Bowl-shaped fermented rice-and-coconut pancakes."),("Pol Sambol","Fresh coconut relish flavored with chilli, onion and lime."),("Lamprais","Rice and accompaniments traditionally baked together in a banana leaf.")],
    "Bangladesh": [("Hilsa Curry","Hilsa fish prepared with Bengali spices and gravy."),("Dhaka Biryani","Fragrant rice dish prepared with meat and aromatic spices."),("Panta Bhat","Fermented rice dish traditionally eaten with savory accompaniments."),("Bhapa Pitha","Steamed rice cake commonly filled with coconut and jaggery."),("Fuchka","Crisp filled shells served with spiced water and tangy fillings.")],
    "Pakistan": [("Biryani","Fragrant spiced rice cooked with meat or vegetables."),("Nihari","Slow-cooked meat stew flavored with aromatic spices."),("Chapli Kebab","Spiced minced-meat kebab associated with Khyber Pakhtunkhwa."),("Haleem","Slow-cooked mixture of grains, lentils and meat."),("Sajji","Whole roasted meat seasoned with regional spices.")],
    "Saudi Arabia": [("Kabsa","Spiced rice dish commonly prepared with chicken or meat."),("Jareesh","Crushed wheat dish cooked with savory ingredients and spices."),("Mutabbaq","Stuffed folded flatbread with savory or sweet fillings."),("Saleeg","Creamy rice dish traditionally served with chicken or meat."),("Maamoul","Filled shortbread-style pastry commonly made for celebrations.")],
    "Germany": [("Bratwurst","German sausage traditionally grilled or pan-fried."),("Sauerbraten","Slow-marinated and braised beef dish with rich gravy."),("Pretzel","Twisted baked bread with a chewy crust and salty topping."),("Schnitzel","Breaded and fried cutlet served with traditional accompaniments."),("Black Forest Cake","Chocolate cake layered with cream and cherries.")],
    "Brazil": [("Feijoada","Slow-cooked black bean and meat stew associated with Brazil."),("Pão de Queijo","Small baked cheese breads with a chewy texture."),("Coxinha","Breaded snack filled with seasoned shredded chicken."),("Moqueca","Brazilian seafood stew cooked with coconut milk and regional seasonings."),("Brigadeiro","Soft chocolate confection made with condensed milk and cocoa.")],
    "Australia": [("Meat Pie","Savory pastry filled with minced meat and rich gravy."),("Pavlova","Meringue-based dessert topped with cream and fruit."),("Lamington","Sponge cake coated in chocolate and coconut."),("Vegemite on Toast","Toasted bread spread with yeast extract."),("Barramundi","Popular Australian fish often grilled or pan-seared.")],
    "Canada": [("Poutine","French fries topped with cheese curds and gravy."),("Butter Tarts","Small pastry tarts filled with a sweet buttery mixture."),("Tourtière","Savory meat pie associated with French Canadian cuisine."),("Nanaimo Bar","Layered chocolate, custard and coconut dessert."),("Montreal Bagel","Wood-fired bagel with a distinctive chewy texture.")],
    "Egypt": [("Koshari","Rice, lentils, pasta, chickpeas and tomato sauce topped with crispy onions."),("Ful Medames","Slow-cooked fava beans seasoned with oil, lemon and spices."),("Ta'ameya","Egyptian-style fava-bean falafel."),("Molokhia","Herb-based green soup commonly served with rice or bread."),("Basbousa","Semolina dessert soaked in sweet syrup.")],
    "South Africa": [("Bobotie","Spiced minced-meat bake topped with an egg-based custard."),("Bunny Chow","Hollowed bread loaf filled with curry."),("Boerewors","Traditional spiced sausage often grilled over an open fire."),("Malva Pudding","Warm sweet pudding commonly served with custard or cream."),("Chakalaka","Spicy vegetable relish often served with bread or grilled foods.")],
    "Switzerland": [("Fondue","Melted cheese dish traditionally eaten by dipping bread."),("Rösti","Crispy grated potato dish served as a side or main."),("Raclette","Melted cheese served with potatoes and accompaniments."),("Zürcher Geschnetzeltes","Sliced veal in a creamy sauce associated with Zurich."),("Bircher Muesli","Oat-based breakfast dish mixed with fruit and dairy.")]
}


# ============================================================
# COUNTRY-INDEPENDENT FOOD FALLBACK SUPPORT
# ============================================================

_FALLBACK_FOOD_COUNTRIES = [
    "Nepal", "India", "Israel", "Japan", "China", "South Korea",
    "Thailand", "Vietnam", "Indonesia", "Malaysia", "Singapore",
    "Sri Lanka", "Bangladesh", "Pakistan", "United Arab Emirates",
    "Saudi Arabia", "Turkey", "Italy", "France", "Spain", "Greece",
    "Germany", "United Kingdom", "United States", "Mexico", "Brazil",
    "Australia", "Canada", "Egypt", "South Africa", "Switzerland"
]

_FOOD_COUNTRY_ALIASES = {
    "usa": "United States",
    "us": "United States",
    "united states of america": "United States",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "uae": "United Arab Emirates",
    "u.a.e.": "United Arab Emirates",
    "south korea": "South Korea",
    "republic of korea": "South Korea",
    "korea, republic of": "South Korea",
    "viet nam": "Vietnam",
    "turkiye": "Turkey",
    "türkiye": "Turkey",
}


def normalize_country_name(country_name):
    """Return one stable country name for data/fallback lookups."""
    value = " ".join(str(country_name or "").strip().split())
    if not value:
        return "Unknown Country"

    alias = _FOOD_COUNTRY_ALIASES.get(value.casefold())
    if alias:
        return alias

    for canonical in set(_FALLBACK_FOOD_COUNTRIES) | set(FOOD_DATA) | set(TOURIST_PLACES) | set(RELIGIOUS_PLACES):
        if value.casefold() == canonical.casefold():
            return canonical

    return value


# Merge the original food data into the fallback table without destroying
# the existing data. This guarantees that every requested fallback country
# has at least five local foods.
for _country in _FALLBACK_FOOD_COUNTRIES:
    canonical = normalize_country_name(_country) if '_FOOD_COUNTRY_ALIASES' in globals() else _country
    current = list(FALLBACK_FOOD_DATA.get(canonical, []))
    for item in FOOD_DATA.get(canonical, []):
        if item and str(item[0]).strip().casefold() not in {str(x[0]).strip().casefold() for x in current if isinstance(x, (tuple, list)) and x}:
            current.append(item)
    FALLBACK_FOOD_DATA[canonical] = current


def make_generic_food_fallback(country_name):
    """Last-resort country-specific food cards for countries not in the table."""
    country = normalize_country_name(country_name)
    templates = [
        (f"Traditional cuisine of {country}", f"A representative local dish or cuisine style associated with {country}."),
        (f"Popular street food of {country}", f"A commonly enjoyed street-food style from {country}."),
        (f"Traditional rice dish of {country}", f"A local rice-based dish or preparation associated with {country}."),
        (f"Traditional bread of {country}", f"A traditional bread or flatbread style associated with {country}."),
        (f"Traditional dessert of {country}", f"A sweet dish or dessert associated with the cuisine of {country}.")
    ]
    return templates


# ============================================================
# WIKIPEDIA / WIKIMEDIA IMAGE LOOKUP
# ============================================================

DISCARD_TITLE_PREFIXES = [
    "tourism in ", "economy of ", "geography of ", "demographics of ",
    "list of ", "outline of ", "history of ", "culture of ", "politics of ",
    "administrative divisions", "flag of ", "coat of arms of ", "heist", "incident", "disaster", "earthquake"
]

BIO_KEYWORDS = {
    "politician", "actor", "actress", "singer", "cricketer", "footballer", "athlete",
    "model", "minister", "governor", "president", "statesman", "diplomat", "lawyer",
    "judge", "businessman", "businesswoman", "activist", "film director", "pageant"
}


INVALID_MEDIA_EXTENSIONS = (
    ".pdf", ".tif", ".tiff", ".svg", ".djvu", ".webm", ".ogg", ".ogv", ".mp4", ".gif", ".mid", ".midi"
)

GRAPHIC_NON_PHOTO_KEYWORDS = {
    "map", "locator", "diagram", "chart", "graph", "coat of arms", "flag of",
    "billboard", "poster", "receipt", "stamp", "coin", "banknote", "passport",
    "license", "document", "newspaper", "clipping", "signature", "autograph",
    "tombstone", "road sign", "street sign", "license plate", "wikimania",
    "conference", "meeting", "workshop", "presentation", "menu", "cow", "cattle", "livestock"
}


def is_valid_place_image(title, extract="", image_url="", place_name="", country=""):
    """
    Validate that an image strictly represents the actual PLACE / LANDMARK / ATTRACTION.
    Rejects:
    1. People, tourists, selfies, portraits, crowds, posing, bloggers, wedding parties.
    2. Hotel bedrooms, dining rooms, restaurant interiors, food dishes.
    3. Clothing, garments, mannequins.
    4. Non-photo graphics, maps, coats of arms, flags, coins, stamps, logos, diagrams.
    5. Discard generic country / political / biographical pages.
    6. Ensures semantic relevance to the place name.
    """
    t_lower = str(title or "").lower()
    ext_lower = str(extract or "").lower()
    img_lower = str(image_url or "").lower()
    place_clean = re.sub(r"\s*\(.*?\)", "", str(place_name or "")).strip().lower()

    # 1. Reject non-photo media files (.pdf, .svg, .tif, .webm, etc.)
    for ext in INVALID_MEDIA_EXTENSIONS:
        if img_lower.endswith(ext) or ext in img_lower.split("?")[0] or t_lower.endswith(ext):
            return False

    # 2. Reject graphics, diagrams, maps, coats of arms, flags, documents, coins, signs
    for kw in GRAPHIC_NON_PHOTO_KEYWORDS:
        pattern = r'(?<![a-z0-9])' + re.escape(kw) + r'(?![a-z0-9])'
        if re.search(pattern, t_lower) or re.search(pattern, img_lower):
            return False

    # 3. Discard country overview / statistics / event pages / disambiguations
    if any(t_lower.startswith(p) or f" {p}" in t_lower for p in DISCARD_TITLE_PREFIXES):
        return False
    if "disambiguation" in t_lower:
        return False

    # 4. Strictly reject people, tourists, selfies, portraits, crowds, bloggers, posing
    people_negative_keywords = [
        "tourist", "tourists", "selfie", "posing", "pose", "portrait", "headshot",
        "traveler", "travelers", "blogger", "influencer", "profile picture", "profile_picture",
        "official photo", "official_photo", "cropped face", "cropped_face", "mugshot",
        "group photo", "group_photo", "family photo", "wedding", "reception", "bride", "groom",
        "crowd", "spectators", "audience", "protest", "rally", "conference", "meeting",
        "politician", "minister", "president", "prime minister", "actor", "actress",
        "singer", "author", "cricketer", "footballer", "sportsman", "priest", "monk",
        "sadhu", "person", "people", "man posing", "woman posing", "girl posing", "boy posing"
    ]
    for pk in people_negative_keywords:
        pattern = r'(?<![a-z0-9])' + re.escape(pk) + r'(?![a-z0-9])'
        if re.search(pattern, t_lower) or re.search(pattern, img_lower):
            return False

    # 5. Check biography indicators in extract or parenthetical profession
    if "(" in str(title or "") and ")" in str(title or ""):
        paren = title[title.rfind("(")+1 : title.rfind(")")].lower()
        if any(w in paren for w in ["politician", "actor", "actress", "singer", "cricketer", "footballer", "model", "minister", "writer", "author"]):
            return False

    if ext_lower:
        first_sentence = ext_lower.split(".")[0]
        if any(marker in first_sentence for marker in [
            "(born ", "(born:", "born in ", " is an indian politician", " is an american politician",
            " is a politician", " was a politician", " is an actor", " was an actor",
            " is an actress", " was an actress", " is a cricketer", " is a footballer",
            " is an author", " was an author", " is a singer", " was a singer"
        ]):
            return False
        for marker in [" is an ", " is a ", " was an ", " was a "]:
            if marker in first_sentence:
                after_marker = first_sentence.split(marker, 1)[1]
                words = after_marker.split()[:6]
                if any(w.strip(",.;:") in BIO_KEYWORDS for w in words):
                    return False

    # 6. Reject venue interiors not representing the destination (hotel bedrooms, dining rooms, kitchens)
    venue_discards = [
        "hotel room", "bedroom", "hotel lobby", "dining room", "dining table",
        "restaurant interior", "kitchen counter", "office desk"
    ]
    if any(vd in t_lower or vd in img_lower or vd in ext_lower for vd in venue_discards):
        return False

    # 7. Cross-category contamination: Food & Clothing
    cross_discards = [
        "recipe", "salad", "curry", "soup", "stew", "dessert", "pastry", "noodles",
        "cooked dish", "mannequin", "fabric swatch", "textile store", "dressmaker"
    ]
    if any(cd in t_lower or cd in img_lower for cd in cross_discards):
        return False

    # 8. Place relevance check: candidate should relate to the requested place
    if place_clean:
        place_tokens = [
            tok for tok in re.findall(r"\b\w+\b", place_clean)
            if len(tok) >= 3 and tok not in {
                "the", "and", "of", "in", "national", "park", "temple", "gate",
                "bridge", "tower", "square", "palace", "fort", "center", "city",
                "lake", "mountain", "island", "falls", "river", "beach"
            }
        ]
        if not place_tokens:
            place_tokens = [tok for tok in re.findall(r"\b\w+\b", place_clean) if len(tok) >= 3]

        if place_tokens:
            in_title = any(tok in t_lower for tok in place_tokens)
            in_img = any(tok in img_lower for tok in place_tokens)
            in_ext = any(tok in ext_lower[:200] for tok in place_tokens)
            if not (in_title or in_img or in_ext):
                return False

    return True


def is_valid_food_image(title, extract="", image_url="", dish_name="", country=""):
    """
    Validate that an image strictly represents the PREPARED DISH.
    Rejects:
    1. Raw ingredients, raw meat, raw poultry, raw fish, uncooked vegetables.
    2. Spices, raw lentils/pulses, split pulses, grain sacks, flour, seed pods.
    3. Agricultural fields, paddies, livestock, cows, cattle.
    4. Restaurant facades, building exteriors, empty dining tables, menus, people eating.
    5. Landmarks, places, clothing.
    6. Generic overview pages.
    """
    t_lower = str(title or "").lower()
    ext_lower = str(extract or "").lower()
    img_lower = str(image_url or "").lower()
    dish_clean = re.sub(r"\s*\(.*?\)", "", str(dish_name or "")).strip().lower()

    # 1. Reject non-photos
    for ext in INVALID_MEDIA_EXTENSIONS:
        if img_lower.endswith(ext) or ext in img_lower.split("?")[0] or t_lower.endswith(ext):
            return False

    # 2. Reject graphics/maps/flags
    for kw in GRAPHIC_NON_PHOTO_KEYWORDS:
        pattern = r'(?<![a-z0-9])' + re.escape(kw) + r'(?![a-z0-9])'
        if re.search(pattern, t_lower) or re.search(pattern, img_lower):
            return False

    # 3. Discard generic overview pages
    generic_prefixes = (
        "cuisine of", "food of", "culture of", "history of", "geography of",
        "economy of", "agriculture in", "tourism in", "list of", "category:",
        "portal:", "index of"
    )
    if any(t_lower.startswith(gp) or f" {gp}" in t_lower for gp in generic_prefixes):
        if not any(gp in dish_clean for gp in generic_prefixes):
            return False

    # 4. Strict rejection of raw ingredients, non-prepared items, livestock, and venues
    strict_food_img_discards = [
        "raw_meat", "raw_beef", "raw_pork", "raw_chicken", "raw_mutton", "raw_lamb",
        "split_pulses", "raw_lentil", "raw_pulses", "dry_beans", "wheat_field", "paddy_field",
        "rice_field", "spice_rack", "raw_spice", "mortar_and_pestle", "restaurant_facade",
        "restaurant_exterior", "storefront", "building_facade", "dining_room", "empty_table",
        "menu_board", "billboard", "people_eating", "chef_posing", "supermarket_shelf",
        "photomontage", "montage", "collage", "panorama", "skyline", "aerial_view", "beach_view"
    ]
    for sd in strict_food_img_discards:
        if sd in img_lower or sd.replace("_", " ") in img_lower:
            return False

    # Discard non-prepared / venue / agricultural pages
    non_prepared_title_discards = [
        "restaurant facade", "restaurant exterior", "storefront", "building facade",
        "dining room", "empty table", "menu board", "billboard", "people eating",
        "species of plant", "genus of flowering", "cultivation of", "variety of rice",
        "types of lentil", "raw pulses", "legume seeds", "raw grain", "spice rack"
    ]
    for npt in non_prepared_title_discards:
        if npt in t_lower or npt in ext_lower[:150]:
            return False

    if "head cheese" in t_lower or "head cheese" in img_lower:
        if "head cheese" not in dish_clean:
            return False

    # Discard raw meat / raw fish unless it is a recognized marinated/raw delicacy (ceviche, sashimi, sushi, tartare, carpaccio, poke)
    is_cured_raw_dish = any(w in dish_clean for w in ["ceviche", "cebiche", "sashimi", "sushi", "tartare", "carpaccio", "poke"])
    if not is_cured_raw_dish:
        for r_item in ["raw meat", "raw beef", "raw pork", "raw chicken", "raw fish", "raw mutton"]:
            if r_item in img_lower or r_item in t_lower:
                return False

    # 5. Cross-category: Places & Clothing
    if any(k in t_lower or k in img_lower for k in [
        "monument", "cathedral", "church", "mosque", "temple", "shrine", "waterfall",
        "mountain peak", "canyon", "skyline", "saree", "kimono", "hanbok"
    ]):
        return False

    # 6. Distinctive token match
    stopwords = {
        "traditional", "classic", "authentic", "fresh", "popular", "regional",
        "national", "heritage", "signature", "style", "specialties", "specialty",
        "dish", "dishes", "platter", "food", "cooked", "and", "&", "with", "de",
        "la", "le", "el", "los", "al", "en", "the", "a", "an", "of", "in"
    }
    raw_tokens = re.findall(r"\b\w+\b", dish_clean)
    distinctive_tokens = [t for t in raw_tokens if len(t) >= 3 and t not in stopwords]
    if not distinctive_tokens:
        distinctive_tokens = [t for t in raw_tokens if len(t) >= 3]

    if distinctive_tokens:
        title_matches = any(t in t_lower for t in distinctive_tokens)
        img_matches = any(t in img_lower for t in distinctive_tokens)
        lead_ext = ext_lower[:180]
        ext_matches = any(t in lead_ext for t in distinctive_tokens)
        if not (title_matches or img_matches or ext_matches):
            return False

    return True


CHILD_TERMS = {
    # English child / minor terms
    "boy", "boys", "schoolboy", "schoolboys", "littleboy",
    "girl", "girls", "schoolgirl", "schoolgirls", "littlegirl",
    "child", "children", "kid", "kids",
    "toddler", "toddlers", "baby", "babies", "infant", "infants",
    "youth", "youths", "teen", "teens", "teenager", "teenagers",
    "kindergarten", "preschool", "elementary", "pupil", "pupils", "minor", "minors",
    # German
    "kind", "kinder", "junge", "jungen", "knabe", "knaben", "mädchen", "maedchen", "schulkind",
    # French
    "enfant", "enfants", "garçon", "garcon", "garçons", "garcons", "fillette", "fillettes", "écolier", "ecolier",
    # Spanish / Italian / Portuguese
    "niño", "nino", "niños", "ninos", "niña", "nina", "niñas", "ninas",
    "bambino", "bambini", "bambina", "bambine", "ragazzo", "ragazza", "fanciullo", "chico", "chica", "criança", "crianca"
}

FEMALE_SUBJECT_INDICATORS = {
    "woman", "women", "lady", "ladies", "female", "females",
    "bride", "brides", "bridesmaid", "bridesmaids",
    "femme", "femmes", "frau", "frauen", "dame", "damen",
    "mujer", "mujeres", "donna", "donne", "senhorita", "senhora",
    "sister", "mother", "wife", "daughter", "grandmother", "aunt",
    "queen", "princess", "empress", "danseuse", "actress", "geisha", "maiko",
    "poblana", "tehuana", "paisana"
}

FEMALE_GARMENT_INDICATORS = {
    "dress", "dresses", "skirt", "skirts", "saree", "saris", "sari",
    "dirndl", "dirndls", "cheongsam", "qipao", "ao dai", "hanbok",
    "chima", "blouse", "blouses", "apron", "aprons", "gown", "gowns",
    "rebozo", "pollera", "polleras", "huipil", "huipiles", "tehuana",
    "bunad", "bunader", "amalia", "isidwaba", "isicholo", "baladi",
    "milaya", "abaya", "abayas", "tarha", "hijab", "petticoat", "corset",
    "lehenga", "lehengas", "choli", "dupatta", "ghagra", "kebaya", "sarong",
    # Expanded authentic traditional garments across 50+ countries
    "gunyo", "cholo", "patuka", "osari", "kira", "wonju", "toego",
    "jamdani", "shalwar", "kameez", "anarkali", "deel", "uuuji",
    "baju kurung", "kurung", "terno", "baro", "saya", "thummy", "eingyi",
    "sampot", "tracht", "coiffe", "vianesa", "klederdracht", "sverigedräkten",
    "sverigedrakten", "krakowski", "vyshyvanka", "plakhta", "vinok",
    "takchita", "caftan", "kaftan", "kanga", "kitenge", "iro", "buba",
    "kaba", "habesha", "kemis", "netela", "sheila", "bindallı", "bindalli",
    "corte", "baiana", "crioula", "paisana", "lliclla", "cueca", "huasa",
    "piupiu", "korowai", "sulu jaba", "jaba"
}

MALE_SUBJECT_INDICATORS = {
    "man", "men", "male", "males", "gentleman", "gentlemen",
    "groom", "grooms", "groomsman", "guy", "guys", "gars",
    "homme", "hommes", "mann", "männer", "maenner", "herren",
    "hombre", "hombres", "uomo", "uomini", "senhor", "senhores",
    "brother", "father", "husband", "son", "grandfather", "uncle",
    "monk", "monks", "priest", "priests", "king", "prince", "emperor",
    "danseur", "actor", "gaucho", "gauchos", "drover", "drovers",
    "cowboy", "cowboys", "charro", "charros", "evzone", "evzones"
}

MALE_GARMENT_INDICATORS = {
    "kilt", "kilts", "sherwani", "kurta", "dhoti", "lungi",
    "lederhosen", "thobe", "dishdasha", "kandura", "charro",
    "fustanella", "galabeya", "bombachas", "rastra", "sombrero",
    "waistcoat", "trousers", "breeches", "fermeli", "ghutra", "agal",
    "emamah", "vraka",
    # Expanded authentic traditional garments across 50+ countries
    "daura", "suruwal", "topi", "dhaka topi", "nilame", "gho", "kera", "kabney",
    "panjabi", "pajama", "mujib", "peshawari", "wascoat", "montsuki", "hakama",
    "haori", "baji", "durumagi", "tangzhuang", "changshan", "malgai",
    "ao gam", "áo gấm", "khan dong", "khăn đóng", "suea phraratchathan",
    "chong kben", "beskap", "blangkon", "baju melayu", "melayu", "sampin",
    "songkok", "barong", "tagalog", "paso", "gaung baung", "steireranzug",
    "chüelederhosene", "chuelederhosene", "bragou braz", "bragou", "sporran",
    "traje corto", "herrebunad", "campino", "klompen", "folkdräkt", "folkdrakt",
    "rogatywka", "sharovary", "ibheshu", "amambatha", "shuka", "shúkà",
    "kanzu", "kofia", "agbada", "fila", "kente", "toga", "kidan", "gabi",
    "cepken", "zeybek", "keffiyeh", "shemagh", "massar", "khanjar", "chaps",
    "stetson", "ceinture", "fléchée", "flechee", "cofradía", "cofradia",
    "guaiaca", "poncho", "chullo", "alpaca poncho", "vueltiao", "ruana",
    "chamanto", "chupalla", "huaso", "moleskins", "akubra", "tatua",
    "sulu vakataga", "vakataga"
}

DUAL_GENDER_INDICATORS = {
    "couple", "couples", "pair", "wedding", "marriage", "dancers", "family", "group", "both", "partners"
}

CHILD_PHRASES = [
    r"\b(little|young|small|school)\s+(boy|girl|child|kid)\b",
    r"\b(elementary|primary)\s+school\b",
    r"\bchildren\s+wearing\b",
    r"\bkids\s+in\b",
    r"\bboys\s+in\b",
    r"\bgirls\s+in\b"
]

# Cross-cultural scope mapping: cultural term -> set of allowed country keywords
CROSS_CULTURAL_MAP = {
    "ukrainian": {"ukraine"},
    "ukraine": {"ukraine"},
    "russian": {"russia"},
    "russia": {"russia"},
    "ingush": {"russia", "georgia", "armenia", "azerbaijan"},
    "chechen": {"russia"},
    "dagestan": {"russia"},
    "japanese": {"japan"},
    "kimono": {"japan"},
    "yukata": {"japan"},
    "hakama": {"japan"},
    "chinese": {"china", "taiwan", "hong kong", "macau", "singapore"},
    "hanfu": {"china", "taiwan", "hong kong", "macau", "singapore"},
    "qipao": {"china", "taiwan", "hong kong", "macau", "singapore"},
    "cheongsam": {"china", "taiwan", "hong kong", "macau", "singapore"},
    "tangzhuang": {"china", "taiwan", "hong kong", "macau", "singapore"},
    "korean": {"south korea", "north korea", "korea"},
    "hanbok": {"south korea", "north korea", "korea"},
    "indian": {"india", "nepal", "bangladesh", "sri lanka", "pakistan"},
    "saree": {"india", "nepal", "bangladesh", "sri lanka"},
    "sari": {"india", "nepal", "bangladesh", "sri lanka"},
    "lehenga": {"india", "pakistan", "bangladesh"},
    "sherwani": {"india", "pakistan", "bangladesh"},
    "daura": {"nepal"},
    "suruwal": {"nepal"},
    "gunyo": {"nepal"},
    "cholo": {"nepal"},
    "maasai": {"kenya", "tanzania"},
    "masai": {"kenya", "tanzania"},
    "mexican": {"mexico"},
    "charro": {"mexico"},
    "sombrero": {"mexico"},
    "scottish": {"united kingdom", "scotland", "uk"},
    "kilt": {"united kingdom", "scotland", "uk", "ireland"},
    "bavarian": {"germany", "austria", "switzerland"},
    "dirndl": {"germany", "austria", "switzerland"},
    "lederhosen": {"germany", "austria", "switzerland"},
    "zulu": {"south africa", "eswatini", "lesotho", "zimbabwe"},
    "xhosa": {"south africa"},
    "saudi": {"saudi arabia"},
    "najdi": {"saudi arabia"},
    "norwegian": {"norway"},
    "bunad": {"norway"},
    "fustanella": {"greece", "albania"},
    "gaucho": {"argentina", "uruguay", "brazil"},
    "bombachas": {"argentina", "uruguay", "brazil"},
    "ao dai": {"vietnam"},
    "vietnamese": {"vietnam"},
    "moroccan": {"morocco"},
    "djellaba": {"morocco", "algeria", "tunisia"},
    "kaftan": {"morocco", "turkey", "algeria", "tunisia"},
    "chut thai": {"thailand"},
    "thai": {"thailand"},
    "kebaya": {"indonesia", "malaysia", "singapore"},
    "batik": {"indonesia", "malaysia"},
    "barong": {"philippines"},
    "filipino": {"philippines"},
    "philippine": {"philippines"}
}


def is_valid_attire_image(title, extract="", image_url="", attire_name="", country="", gender="unisex", metadata=None):
    """
    Validate that an image strictly represents ADULT TRADITIONAL ATTIRE worn by real adults.
    Enforces across ALL countries:
    1. Rejects children, boys, girls, toddlers, infants, school pupils in adult attire sections.
    2. Gender alignment: strictly rejects female-only portraits in male sections, and vice versa.
    3. Requires positive female/male confirmation for gender-specific attire.
    4. Rejects AI generation, synthetic art, 3D renders, drawings, anime, manga, paintings, sculptures.
    5. Rejects mannequins, store dummies, hangers, folded clothes, sewing machines, fabric rolls, looms.
    6. Rejects food dishes, recipes, cityscapes, skylines, flags, logos, maps.
    7. Cross-cultural misattributions (e.g. saree for Nepal, kimono for Korea, Ukrainian in Canada).
    8. Verifies available metadata (extmetadata: ImageDescription, Categories, ObjectName).
    """
    img_lower = str(image_url or "").lower()
    t_lower = str(title or "").lower()
    ext_lower = str(extract or "").lower()

    # Extract metadata context if available
    meta_text = ""
    if isinstance(metadata, dict):
        desc = metadata.get("ImageDescription", {}).get("value", "")
        cats = metadata.get("Categories", {}).get("value", "")
        obj = metadata.get("ObjectName", {}).get("value", "")
        artist = metadata.get("Artist", {}).get("value", "")
        meta_text = f"{desc} {cats} {obj} {artist}".lower()
    elif metadata:
        meta_text = str(metadata).lower()

    combined = f"{t_lower} {ext_lower} {img_lower} {meta_text}"

    # 1. Strictly reject all AI generation services & synthetic costumes
    if any(ai_kw in img_lower or ai_kw in t_lower for ai_kw in [
        "pollinations.ai", "lexica.art", "midjourney", "dall-e", "dalle",
        "stablediffusion", "craiyon", "generated", "ai_fallback", "artificial"
    ]):
        return False

    # 2. Reject non-image / invalid extensions
    for ext in INVALID_MEDIA_EXTENSIONS:
        if img_lower.endswith(ext) or ext in img_lower.split("?")[0] or t_lower.endswith(ext):
            return False

    # Tokenize combined text (handling CamelCase and punctuation)
    split_camel = re.sub(r'([a-z])([A-Z])', r'\1 \2', f"{title} {extract} {image_url} {meta_text}")
    tokens = set(re.findall(r'[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+', split_camel.lower()))

    # Attire-specific non-stopword tokens for positive confirmation
    attire_tokens = set(re.findall(r'[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+', str(attire_name or "").lower())) - {
        "and", "the", "with", "for", "traditional", "dress", "national", "costume", "attire", "wear", "suit", "clothing",
        "adult", "men", "mens", "women", "womens", "male", "female"
    }

    # 3. GLOBAL CHILD / MINOR REJECTION (Requirements 1, 2, 5, 6, 9)
    if tokens & CHILD_TERMS:
        return False
    for pat in CHILD_PHRASES:
        if re.search(pat, combined, re.IGNORECASE):
            return False

    # 4. GENDER ALIGNMENT & POSITIVE CONFIRMATION (Requirements 1, 2, 3, 5, 6)
    g_tokens = set(re.findall(r'[a-zA-Z]+', str(gender or "").lower()))
    is_men = bool(g_tokens & {"men", "male", "man", "groom", "gentleman"})
    is_women = bool(g_tokens & {"women", "female", "woman", "bride", "lady"})

    has_couple_context = bool(tokens & DUAL_GENDER_INDICATORS)

    if is_women and not is_men:
        # Explicit rejection of misclassified male images
        if any(bad_name in img_lower for bad_name in ["in_a_traditional_magar_attire_02", "traditional_magar_attire_02"]):
            return False
        # STRICT WOMEN'S WEAR VALIDATION:
        # A. Reject if male subject terms appear without couple context
        if (tokens & MALE_SUBJECT_INDICATORS) and not has_couple_context:
            return False
        # B. Reject if male garment terms appear without female context
        if (tokens & MALE_GARMENT_INDICATORS) and not (tokens & (FEMALE_SUBJECT_INDICATORS | FEMALE_GARMENT_INDICATORS | attire_tokens)):
            return False
        # C. POSITIVE CONFIRMATION: Must have female subject, female garment, or couple context
        has_female_subject = bool(tokens & FEMALE_SUBJECT_INDICATORS)
        has_female_garment = bool(tokens & (FEMALE_GARMENT_INDICATORS | attire_tokens))
        if not (has_female_subject or has_female_garment or has_couple_context):
            return False

    elif is_men and not is_women:
        # STRICT MEN'S WEAR VALIDATION:
        # A. Reject if female subject terms appear without couple context
        if (tokens & FEMALE_SUBJECT_INDICATORS) and not has_couple_context:
            return False
        # B. Reject if female garment terms appear without male context
        if (tokens & FEMALE_GARMENT_INDICATORS) and not (tokens & (MALE_SUBJECT_INDICATORS | MALE_GARMENT_INDICATORS | attire_tokens)):
            return False
        # C. POSITIVE CONFIRMATION: Must have male subject, male garment, or couple context
        has_male_subject = bool(tokens & MALE_SUBJECT_INDICATORS)
        has_male_garment = bool(tokens & (MALE_GARMENT_INDICATORS | attire_tokens))
        if not (has_male_subject or has_male_garment or has_couple_context):
            return False

    # 5. Reject mannequins, dummies, hangers, isolated clothes, fabric swatches, artwork
    clothing_discards = [
        "mannequin", "dummy", "hanger", "lying flat", "folded flat", "flat lay", "flat-lay",
        "cloth_only", "cloth only", "catalog", "product", "museum exhibit",
        "showcase", "display stand", "tailor shop", "textile store",
        "weaving loom", "sewing machine", "fabric roll", "fabric swatch",
        "swatch", "diagram", "cutting pattern", "sewing pattern", "shelf",
        "wardrobe", "shop dummy", "dress form", "dressmaker dummy", "tailor's dummy",
        "headless", "on a stand", "garment on display", "rack display", "clothes rack", "storefront",
        "vitrine", "wax figure",
        # Artworks / Non-photos
        "statue", "sculpture", "figurine", "bronze", "monument", "doll", "puppet",
        "marionette", "drawing", "illustration", "sketch", "painting", "engraving",
        "lithograph", "watercolour", "watercolor", "cartoon", "anime", "manga",
        "caricature", "comic", "clipart",
        # Unrelated modern professional / institutional subjects
        "poster", "advertisement", "billboard", "banking", "banker", "railway",
        "locomotive", "train station", "subway", "politician", "minister",
        "parliament", "prime minister", "president", "stamp", "postage stamp",
        "banknote", "coin", "medal", "trophy", "passport", "modern suit",
        "business suit", "tuxedo", "police", "firefighter", "laboratory",
        "stadium", "office"
    ]
    for cd in clothing_discards:
        if re.search(r'\b' + re.escape(cd) + r'\b', combined, re.IGNORECASE):
            return False

    # 6. Cross-category: Food & pure non-person landscapes
    if any(k in combined for k in [
        "recipe", "curry", "soup", "salad", "pizza", "noodles", "burger",
        "skyline", "aerial_view", "satellite_image", "topographic_map",
        "hotel room", "bedroom", "restaurant interior"
    ]):
        return False

    # 7. Global cross-cultural protection: reject mismatched cultural traditions
    if country:
        norm_c = normalize_country_name(country).lower()
        for cult_term, allowed_countries in CROSS_CULTURAL_MAP.items():
            if cult_term in combined:
                if not any(ac in norm_c for ac in allowed_countries):
                    return False

    return True


def is_women_attire_dict(att):
    if not isinstance(att, dict):
        return False
    g = str(att.get("gender", "")).strip().lower()
    c = str(att.get("category", "")).strip().lower()
    words = set(re.findall(r'[a-zA-Z]+', f"{g} {c}"))
    return bool(words & {"women", "female", "woman"})


def is_men_attire_dict(att):
    if not isinstance(att, dict):
        return False
    if is_women_attire_dict(att):
        return False
    g = str(att.get("gender", "")).strip().lower()
    c = str(att.get("category", "")).strip().lower()
    words = set(re.findall(r'[a-zA-Z]+', f"{g} {c}"))
    return bool(words & {"men", "male", "man"})


def is_portrait_or_person(title, extract="", image_url="", card_type="place"):
    """Compatibility wrapper delegating to category-specific validators."""
    if card_type == "food":
        return not is_valid_food_image(title, extract, image_url)
    elif card_type in ("clothing", "attire", "dress"):
        return not is_valid_attire_image(title, extract, image_url)
    else:
        return not is_valid_place_image(title, extract, image_url)


def validate_food_image_match(requested_dish, country, candidate_title, candidate_extract="", candidate_image_url=""):
    """
    Strict validation to guarantee accuracy first:
    1. Rejects raw ingredients (lentils, pulses, raw meat, spices, grains, seeds).
    2. Rejects restaurant facades, dining interiors, menus, empty tables, and people eating.
    3. Rejects generic overview pages (e.g. 'Cuisine of Thailand', 'Food of Quebec').
    4. Rejects unrelated dishes (e.g. Poutine for Maple Syrup, Meat Pie for Barramundi, Quail for Clam Chowder, Head Cheese for French Cheese).
    5. Requires candidate page/title/extract to have a concrete semantic match with the requested dish.
    """
    req_clean = re.sub(r"\s*\(.*?\)", "", str(requested_dish or "")).strip().lower()
    c_title = str(candidate_title or "").strip().lower()
    c_ext = str(candidate_extract or "").strip().lower()
    c_img = str(candidate_image_url or "").strip().lower()
    norm_country = normalize_country_name(country).lower() if country else ""

    # 1. Reject generic overview / portal / non-dish pages
    generic_prefixes = (
        "cuisine of", "food of", "culture of", "history of", "geography of",
        "economy of", "agriculture in", "tourism in", "list of", "category:",
        "portal:", "index of"
    )
    if any(c_title.startswith(gp) or f" {gp}" in c_title for gp in generic_prefixes):
        if not any(gp in req_clean for gp in generic_prefixes):
            return False

    # 2. Strict rejection of raw ingredients, non-prepared items, livestock, and venues
    strict_discards = [
        "raw meat", "raw beef", "raw pork", "raw chicken", "raw mutton", "raw lamb", "raw fish",
        "dried, split pulses", "dried split pulses", "split pulses", "pulses (e.g.",
        "types of lentil", "indian pulses", "raw lentil", "raw pulses", "dry beans",
        "legume seeds", "raw grain", "wheat field", "paddy field", "rice field",
        "spice rack", "spice stall", "raw spice", "raw spices", "mortar and pestle",
        "species of plant", "genus of flowering", "cultivation of", "variety of rice",
        "restaurant facade", "restaurant exterior", "storefront", "building facade",
        "dining room", "empty table", "menu board", "billboard", "people eating",
        "chef posing", "waiter serving", "customer seated", "supermarket shelf"
    ]
    for sd in strict_discards:
        if sd in c_ext or sd in c_img or sd in c_title:
            return False

    # 3. Head cheese rejection unless specifically requested
    if "head cheese" in c_title or "head cheese" in c_ext:
        if "head cheese" not in req_clean:
            return False

    # 4. Token extraction from requested dish
    stopwords = {
        "traditional", "classic", "authentic", "fresh", "popular", "regional",
        "national", "heritage", "signature", "style", "specialties", "specialty",
        "dish", "dishes", "platter", "food", "cooked", "and", "&", "with", "de",
        "la", "le", "el", "los", "al", "en", "the", "a", "an", "of", "in"
    }
    country_adjectives = {
        "indian", "nepali", "nepalese", "japanese", "thai", "chinese", "korean",
        "vietnamese", "indonesian", "french", "italian", "german", "spanish",
        "british", "english", "brazilian", "american", "canadian", "australian",
        "aussie", "mexican", "greek", "turkish", "moroccan", "peruvian", "irish",
        "norwegian", "swedish", "dutch", "polish", "filipino", "kiwi", "saudi",
        "egyptian", "african", norm_country
    }
    raw_tokens = re.findall(r"\b\w+\b", req_clean)
    distinctive_tokens = [
        t for t in raw_tokens
        if len(t) >= 3 and t not in stopwords and t not in country_adjectives
    ]

    if not distinctive_tokens:
        distinctive_tokens = [t for t in raw_tokens if len(t) >= 3]

    if not distinctive_tokens:
        return True

    # 5. Check if at least one distinctive token appears in candidate title or image
    title_matches = any(t in c_title for t in distinctive_tokens)
    img_matches = any(t in c_img for t in distinctive_tokens)

    if title_matches or img_matches:
        return True

    # 6. Check candidate extract:
    lead_ext = c_ext[:150]
    if any(t in lead_ext for t in distinctive_tokens):
        return True

    return False



def normalize_card_title(title, card_type="place"):
    """Normalize food or attraction title by removing conjunctions, parentheticals, and decorative adjectives."""
    t = str(title or "").strip()
    if not t:
        return ""
    # Strip parentheticals
    t_clean = re.sub(r"\s*\(.*?\)", "", t).strip()
    if not t_clean:
        t_clean = t

    # Conjunction handling
    if " & " in t_clean:
        parts = [p.strip() for p in t_clean.split(" & ") if p.strip()]
        if parts:
            t_clean = parts[0]
    elif " and " in t_clean.lower() and card_type == "food":
        parts = [p.strip() for p in re.split(r"\s+and\s+", t_clean, flags=re.IGNORECASE) if p.strip()]
        if len(parts) > 1 and parts[0].lower() not in ("rice", "fish"):
            t_clean = parts[0]

    # Strip subjective prefixes for food: "Artisan ", "Traditional ", "Classic ", "Authentic ", "Fresh ", "Popular "
    if card_type == "food":
        for prefix in ["Artisan ", "Traditional ", "Classic ", "Authentic ", "Fresh ", "Popular ", "Regional ", "National ", "Heritage ", "Signature "]:
            if t_clean.lower().startswith(prefix.lower()):
                t_clean = t_clean[len(prefix):].strip()
                break

    return t_clean


DESTINATION_CANONICAL_PAGES = {
    # India
    ("india", "taj mahal"): {
        "slug": "Taj_Mahal",
        "query": "Taj Mahal Agra India landmark tourism",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/960px-Taj_Mahal_%28Edited%29.jpeg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail"
    },
    ("india", "tirumala temple"): {
        "slug": "Venkateswara_Temple,_Tirumala",
        "query": "Tirumala Venkateswara Temple Tirupati Andhra Pradesh India",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4e/Tirumala_090615.jpg/960px-Tirumala_090615.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail"
    },
    ("india", "jaipur"): {
        "slug": "Jaipur",
        "query": "Hawa Mahal Jaipur Rajasthan India landmark tourism",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/41/East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg/960px-East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail"
    },
    ("india", "goa"): {
        "slug": "Goa",
        "query": "Goa beach coast India tourism landscape",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fc/BeachFun.jpg/960px-BeachFun.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail"
    },
    ("india", "varanasi"): {
        "slug": "Varanasi",
        "query": "Varanasi Ganges ghats temples Uttar Pradesh India tourism",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0e/Varanasi%2C_India%2C_Ghats%2C_Cremation_ceremony_in_progress.jpg/960px-Varanasi%2C_India%2C_Ghats%2C_Cremation_ceremony_in_progress.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail"
    },
    ("india", "kerala backwaters"): {
        "slug": "Kerala_backwaters",
        "query": "Kerala backwaters houseboat lagoon India tourism",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ee/House_Boat_DSW.jpg/960px-House_Boat_DSW.jpg?utm_source=en.wikipedia.org&utm_campaign=api&utm_content=thumbnail"
    },
    ("india", "dal lake"): {"slug": "Dal_Lake", "query": "Dal Lake Srinagar Kashmir shikara houseboat India", "safe_image": ""},
    ("india", "gulmarg"): {"slug": "Gulmarg", "query": "Gulmarg meadow gondola snow Kashmir India tourism", "safe_image": ""},
    ("india", "gulmarg gondola & meadows"): {"slug": "Gulmarg", "query": "Gulmarg gondola cable car ski meadow Kashmir India", "safe_image": ""},
    ("india", "pahalgam"): {"slug": "Pahalgam", "query": "Pahalgam valley Lidder river pine trees Kashmir India", "safe_image": ""},
    ("india", "pahalgam betaab valley"): {"slug": "Betaab_Valley", "query": "Betaab Valley Pahalgam Kashmir river mountains landscape India", "safe_image": ""},
    ("india", "sonamarg"): {"slug": "Sonamarg", "query": "Sonamarg Thajiwas glacier meadow golden Kashmir India", "safe_image": ""},
    ("india", "sonamarg thajiwas glacier"): {"slug": "Sonamarg", "query": "Sonamarg Thajiwas glacier snow peaks Kashmir India", "safe_image": ""},
    ("india", "mughal gardens (shalimar & nishat)"): {"slug": "Shalimar_Bagh,_Srinagar", "query": "Shalimar Bagh Nishat Mughal gardens fountains Dal Lake Srinagar Kashmir", "safe_image": ""},
    ("india", "shankaracharya temple"): {"slug": "Shankaracharya_Temple", "query": "Shankaracharya Temple hill shrine Srinagar Dal Lake Kashmir", "safe_image": ""},
    ("india", "srinagar"): {"slug": "Srinagar", "query": "Srinagar Dal Lake shikara houseboat Kashmir India", "safe_image": ""},

    # Nepal
    ("nepal", "mount everest"): {"slug": "Mount_Everest", "query": "Mount Everest peak Himalayas landscape snow Nepal", "safe_image": ""},
    ("nepal", "pashupatinath temple"): {"slug": "Pashupatinath_Temple", "query": "Pashupatinath Temple Kathmandu Bagmati river pagoda Nepal", "safe_image": ""},
    ("nepal", "boudhanath stupa"): {"slug": "Boudhanath", "query": "Boudhanath Stupa Kathmandu Buddhist stupa prayer flags Nepal", "safe_image": ""},
    ("nepal", "kathmandu durbar square"): {"slug": "Kathmandu_Durbar_Square", "query": "Kathmandu Durbar Square ancient palaces temples Nepal landmark", "safe_image": ""},
    ("nepal", "phewa lake"): {"slug": "Phewa_Lake", "query": "Phewa Lake Pokhara boat Annapurna reflection Nepal", "safe_image": ""},
    ("nepal", "swayambhunath (monkey temple)"): {"slug": "Swayambhunath", "query": "Swayambhunath Monkey Temple stupa Kathmandu valley Nepal", "safe_image": ""},
    ("nepal", "swayambhunath"): {"slug": "Swayambhunath", "query": "Swayambhunath Monkey Temple stupa Kathmandu valley Nepal", "safe_image": ""},
    ("nepal", "chitwan national park"): {"slug": "Chitwan_National_Park", "query": "Chitwan National Park rhino wildlife jungle Nepal", "safe_image": ""},
    ("nepal", "peace pagoda (shanti stupa)"): {"slug": "World_Peace_Pagoda,_Pokhara", "query": "World Peace Pagoda Shanti Stupa Pokhara lake Annapurna Nepal", "safe_image": ""},
    ("nepal", "dal bhat"): {
        "slug": "Dal_bhat",
        "query": "Nepali dal bhat tarkari brass thali authentic platter",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/60/Nepali_dal-bhat-tarkari.jpg/960px-Nepali_dal-bhat-tarkari.jpg",
        "description": "Nepal's iconic national dish and daily staple meal, featuring steamed white rice (Bhat) accompanied by slow-simmered spiced lentil soup (Dal), seasonal vegetable curry (Tarkari), sautéed greens (Saag), and spicy achar relish served together on a traditional brass thali platter."
    },
    ("nepal", "dal bhat (traditional thali)"): {
        "slug": "Dal_bhat",
        "query": "Nepali dal bhat tarkari brass thali authentic platter",
        "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/60/Nepali_dal-bhat-tarkari.jpg/960px-Nepali_dal-bhat-tarkari.jpg",
        "description": "Nepal's iconic national dish and daily staple meal, featuring steamed white rice (Bhat) accompanied by slow-simmered spiced lentil soup (Dal), seasonal vegetable curry (Tarkari), sautéed greens (Saag), and spicy achar relish served together on a traditional brass thali platter."
    },

    # France
    ("france", "eiffel tower"): {"slug": "Eiffel_Tower", "query": "Eiffel Tower Paris France landmark tourism", "safe_image": ""},
    ("france", "louvre museum"): {"slug": "Louvre", "query": "Louvre Museum Paris France tourism landmark", "safe_image": ""},
    ("france", "palace of versailles"): {"slug": "Palace_of_Versailles", "query": "Palace of Versailles France landmark", "safe_image": ""},
    ("france", "nice"): {"slug": "Nice", "query": "Nice French Riviera France coast tourism", "safe_image": ""},
    ("france", "mont saint-michel"): {"slug": "Mont-Saint-Michel", "query": "Mont Saint-Michel Normandy France landmark", "safe_image": ""},
    ("france", "lyon old town"): {"slug": "Vieux_Lyon", "query": "Vieux Lyon France historic tourism", "safe_image": ""},

    # Japan
    ("japan", "mount fuji"): {"slug": "Mount_Fuji", "query": "Mount Fuji volcano landscape Japan tourism", "safe_image": ""},
    ("japan", "tokyo"): {"slug": "Tokyo", "query": "Tokyo city skyline landmark Japan tourism", "safe_image": ""},
    ("japan", "kyoto"): {"slug": "Kyoto", "query": "Kyoto temples landmarks Japan tourism", "safe_image": ""},
    ("japan", "fushimi inari shrine"): {"slug": "Fushimi_Inari-taisha", "query": "Fushimi Inari shrine torii gates Kyoto Japan", "safe_image": ""},
    ("japan", "osaka"): {"slug": "Osaka", "query": "Osaka castle Dotonbori skyline Japan tourism", "safe_image": ""},
    ("japan", "hiroshima peace memorial"): {"slug": "Hiroshima_Peace_Memorial", "query": "Hiroshima Peace Memorial Genbaku Dome Japan", "safe_image": ""},

    # Italy
    ("italy", "colosseum"): {"slug": "Colosseum", "query": "Colosseum Rome Italy ancient amphitheatre landmark", "safe_image": ""},
    ("italy", "venice grand canal"): {"slug": "Grand_Canal_(Venice)", "query": "Grand Canal Venice Italy water gondola tourism", "safe_image": ""},
    ("italy", "leaning tower of pisa"): {"slug": "Leaning_Tower_of_Pisa", "query": "Leaning Tower of Pisa Italy bell tower landmark", "safe_image": ""},
    ("italy", "florence cathedral"): {"slug": "Florence_Cathedral", "query": "Florence Cathedral Duomo Santa Maria del Fiore Italy", "safe_image": ""},
    ("italy", "trevi fountain"): {"slug": "Trevi_Fountain", "query": "Trevi Fountain Rome Italy landmark tourism", "safe_image": ""},
    ("italy", "lake como"): {"slug": "Lake_Como", "query": "Lake Como Lombardy Italy mountains landscape tourism", "safe_image": ""},

    # Thailand
    ("thailand", "grand palace"): {"slug": "Grand_Palace", "query": "Grand Palace Bangkok Thailand landmark", "safe_image": ""},
    ("thailand", "wat arun"): {"slug": "Wat_Arun", "query": "Wat Arun temple Bangkok Thailand landmark tourism", "safe_image": ""},
    ("thailand", "phuket"): {"slug": "Phuket_province", "query": "Phuket island beach Thailand tourism coast", "safe_image": ""},
    ("thailand", "railay beach"): {"slug": "Railay_Beach", "query": "Railay Beach Krabi Thailand coast cliffs tourism", "safe_image": ""},
    ("thailand", "chiang mai old city"): {"slug": "Chiang_Mai", "query": "Chiang Mai temples old city Thailand tourism", "safe_image": ""},
    ("thailand", "phi phi islands"): {"slug": "Phi_Phi_Islands", "query": "Phi Phi Islands Maya Bay Krabi Thailand tourism", "safe_image": ""},

    # Israel
    ("israel", "old city of jerusalem"): {"slug": "Old_City_of_Jerusalem", "query": "Old City of Jerusalem Western Wall landmark", "safe_image": ""},
    ("israel", "dead sea"): {"slug": "Dead_Sea", "query": "Dead Sea salt lake landscape tourism", "safe_image": ""},
    ("israel", "tel aviv"): {"slug": "Tel_Aviv", "query": "Tel Aviv beach skyline promenade Israel", "safe_image": ""},
    ("israel", "masada"): {"slug": "Masada", "query": "Masada ancient fortress desert Israel landmark", "safe_image": ""},
    ("israel", "sea of galilee"): {"slug": "Sea_of_Galilee", "query": "Sea of Galilee lake Israel landscape tourism", "safe_image": ""},
    ("israel", "haifa"): {"slug": "Haifa", "query": "Bahai Gardens Haifa Israel terraces landmark", "safe_image": ""},

    # United States
    ("united states", "statue of liberty"): {"slug": "Statue_of_Liberty", "query": "Statue of Liberty New York harbor landmark", "safe_image": ""},
    ("united states", "grand canyon"): {"slug": "Grand_Canyon", "query": "Grand Canyon National Park Arizona landscape", "safe_image": ""},
    ("united states", "times square"): {"slug": "Times_Square", "query": "Times Square Manhattan New York landmark", "safe_image": ""},
    ("united states", "yellowstone national park"): {"slug": "Yellowstone_National_Park", "query": "Yellowstone National Park geyser landscape", "safe_image": ""},
    ("united states", "golden gate bridge"): {"slug": "Golden_Gate_Bridge", "query": "Golden Gate Bridge San Francisco landmark", "safe_image": ""},
    ("united states", "walt disney world"): {"slug": "Walt_Disney_World", "query": "Cinderella Castle Walt Disney World Magic Kingdom Florida", "safe_image": ""},

    # United Kingdom
    ("united kingdom", "big ben"): {"slug": "Big_Ben", "query": "Big Ben Elizabeth Tower Westminster London landmark", "safe_image": ""},
    ("united kingdom", "tower of london"): {"slug": "Tower_of_London", "query": "Tower of London castle historic landmark", "safe_image": ""},
    ("united kingdom", "stonehenge"): {"slug": "Stonehenge", "query": "Stonehenge Wiltshire prehistoric monument landmark", "safe_image": ""},
    ("united kingdom", "edinburgh castle"): {"slug": "Edinburgh_Castle", "query": "Edinburgh Castle Scotland historic fortress landmark", "safe_image": ""},
    ("united kingdom", "lake district"): {"slug": "Lake_District", "query": "Lake District National Park Cumbria landscape tourism", "safe_image": ""},
    ("united kingdom", "buckingham palace"): {"slug": "Buckingham_Palace", "query": "Buckingham Palace London royal residence landmark", "safe_image": ""},

    # Spain
    ("spain", "sagrada família"): {"slug": "Sagrada_Família", "query": "Sagrada Familia Barcelona Spain basilica landmark", "safe_image": ""},
    ("spain", "sagrada familia"): {"slug": "Sagrada_Família", "query": "Sagrada Familia Barcelona Spain basilica landmark", "safe_image": ""},
    ("spain", "alhambra"): {"slug": "Alhambra", "query": "Alhambra Granada Spain palace fortress landmark", "safe_image": ""},
    ("spain", "park güell"): {"slug": "Park_Güell", "query": "Park Guell Barcelona Spain Gaudi landmark", "safe_image": ""},
    ("spain", "park guell"): {"slug": "Park_Güell", "query": "Park Guell Barcelona Spain Gaudi landmark", "safe_image": ""},
    ("spain", "royal palace of madrid"): {"slug": "Royal_Palace_of_Madrid", "query": "Royal Palace of Madrid Spain historic landmark", "safe_image": ""},
    ("spain", "seville cathedral"): {"slug": "Seville_Cathedral", "query": "Seville Cathedral Giralda Spain landmark", "safe_image": ""},
    ("spain", "ibiza"): {"slug": "Ibiza", "query": "Ibiza Balearic Islands Spain coast beach landscape", "safe_image": ""},

    # Greece
    ("greece", "acropolis of athens"): {"slug": "Acropolis_of_Athens", "query": "Acropolis Parthenon Athens Greece landmark ancient", "safe_image": ""},
    ("greece", "santorini"): {"slug": "Santorini", "query": "Santorini Oia white houses caldera Greece tourism", "safe_image": ""},
    ("greece", "mykonos"): {"slug": "Mykonos", "query": "Mykonos windmills coast island Greece tourism", "safe_image": ""},
    ("greece", "meteora"): {"slug": "Meteora", "query": "Meteora monasteries rock pillars Greece landmark", "safe_image": ""},
    ("greece", "delphi"): {"slug": "Delphi", "query": "Delphi ancient ruins archaeological site Greece landmark", "safe_image": ""},
    ("greece", "crete"): {"slug": "Crete", "query": "Crete island coast beach Greece landscape tourism", "safe_image": ""},

    # Switzerland
    ("switzerland", "matterhorn"): {"slug": "Matterhorn", "query": "Matterhorn mountain Zermatt Swiss Alps landscape", "safe_image": ""},
    ("switzerland", "lake geneva"): {"slug": "Lake_Geneva", "query": "Lake Geneva Switzerland water mountains landscape", "safe_image": ""},
    ("switzerland", "jungfraujoch"): {"slug": "Jungfraujoch", "query": "Jungfraujoch Bernese Alps glacier Swiss landscape", "safe_image": ""},
    ("switzerland", "lucerne"): {"slug": "Lucerne", "query": "Lucerne Chapel Bridge Switzerland lake old town", "safe_image": ""},
    ("switzerland", "interlaken"): {"slug": "Interlaken", "query": "Interlaken Bernese Oberland Switzerland mountains landscape", "safe_image": ""},
    ("switzerland", "rhine falls"): {"slug": "Rhine_Falls", "query": "Rhine Falls Schaffhausen Switzerland waterfall landmark", "safe_image": ""},

    # Germany
    ("germany", "brandenburg gate"): {"slug": "Brandenburg_Gate", "query": "Brandenburg Gate Berlin Germany historic monument landmark", "safe_image": ""},
    ("germany", "neuschwanstein castle"): {"slug": "Neuschwanstein_Castle", "query": "Neuschwanstein Castle Bavaria Germany fairy tale landmark", "safe_image": ""},
    ("germany", "cologne cathedral"): {"slug": "Cologne_Cathedral", "query": "Cologne Cathedral Germany gothic church landmark", "safe_image": ""},
    ("germany", "black forest"): {"slug": "Black_Forest", "query": "Black Forest Baden-Wurttemberg Germany mountain forest landscape", "safe_image": ""},
    ("germany", "museum island"): {"slug": "Museum_Island", "query": "Museum Island Berlin Germany historic UNESCO landmark", "safe_image": ""},
    ("germany", "hamburg port"): {"slug": "Port_of_Hamburg", "query": "Port of Hamburg Elbe Germany harbour landmark", "safe_image": ""},

    # Australia
    ("australia", "sydney opera house"): {"slug": "Sydney_Opera_House", "query": "Sydney Opera House Harbour Australia landmark", "safe_image": ""},
    ("australia", "great barrier reef"): {"slug": "Great_Barrier_Reef", "query": "Great Barrier Reef coral Queensland Australia aerial", "safe_image": ""},
    ("australia", "uluru"): {"slug": "Uluru", "query": "Uluru Ayers Rock Northern Territory Australia landmark", "safe_image": ""},
    ("australia", "bondi beach"): {"slug": "Bondi_Beach", "query": "Bondi Beach Sydney Australia ocean coast", "safe_image": ""},
    ("australia", "great ocean road"): {"slug": "Great_Ocean_Road", "query": "Twelve Apostles Great Ocean Road Victoria Australia coast", "safe_image": ""},
    ("australia", "melbourne"): {"slug": "Melbourne", "query": "Melbourne skyline Yarra River Victoria Australia landmark", "safe_image": ""},

    # China
    ("china", "great wall of china"): {"slug": "Great_Wall_of_China", "query": "Great Wall of China Beijing historic monument landmark", "safe_image": ""},
    ("china", "forbidden city"): {"slug": "Forbidden_City", "query": "Forbidden City Beijing China imperial palace landmark", "safe_image": ""},
    ("china", "terracotta army"): {"slug": "Terracotta_Army", "query": "Terracotta Army Xi'an Shaanxi China archaeological site", "safe_image": ""},
    ("china", "the bund"): {"slug": "The_Bund", "query": "The Bund Shanghai skyline Huangpu River China landmark", "safe_image": ""},
    ("china", "zhangjiajie"): {"slug": "Zhangjiajie", "query": "Zhangjiajie National Forest Park sandstone pillars Hunan China", "safe_image": ""},
    ("china", "west lake"): {"slug": "West_Lake", "query": "West Lake Hangzhou Zhejiang China lake landscape", "safe_image": ""},

    # South Korea
    ("south korea", "gyeongbokgung palace"): {"slug": "Gyeongbokgung", "query": "Gyeongbokgung Palace Seoul South Korea royal landmark", "safe_image": ""},
    ("south korea", "n seoul tower"): {"slug": "N_Seoul_Tower", "query": "N Seoul Tower Namsan mountain South Korea landmark", "safe_image": ""},
    ("south korea", "jeju island"): {"slug": "Jeju_Island", "query": "Jeju Island volcanic landscape South Korea coast", "safe_image": ""},
    ("south korea", "bukchon hanok village"): {"slug": "Bukchon_Hanok_Village", "query": "Bukchon Hanok Village traditional houses Seoul South Korea", "safe_image": ""},
    ("south korea", "busan"): {"slug": "Busan", "query": "Busan Haeundae beach skyline South Korea coastal city", "safe_image": ""},
    ("south korea", "changdeokgung palace"): {"slug": "Changdeokgung", "query": "Changdeokgung Palace secret garden Seoul South Korea landmark", "safe_image": ""},

    # Singapore
    ("singapore", "marina bay sands"): {"slug": "Marina_Bay_Sands", "query": "Marina Bay Sands Singapore skyline architectural landmark", "safe_image": ""},
    ("singapore", "gardens by the bay"): {"slug": "Gardens_by_the_Bay", "query": "Gardens by the Bay Supertree Grove Singapore landmark", "safe_image": ""},
    ("singapore", "sentosa island"): {"slug": "Sentosa", "query": "Sentosa Island resort beach Singapore tourism", "safe_image": ""},
    ("singapore", "merlion park"): {"slug": "Merlion_Park", "query": "Merlion Park Singapore statue waterfront landmark", "safe_image": ""},
    ("singapore", "singapore zoo"): {"slug": "Singapore_Zoo", "query": "Singapore Zoo Mandai wildlife rainforest park", "safe_image": ""},
    ("singapore", "chinatown"): {"slug": "Chinatown,_Singapore", "query": "Chinatown Singapore historic district shophouses temples", "safe_image": ""},

    # United Arab Emirates
    ("united arab emirates", "burj khalifa"): {"slug": "Burj_Khalifa", "query": "Burj Khalifa Dubai skyscraper tallest building landmark", "safe_image": ""},
    ("united arab emirates", "sheikh zayed grand mosque"): {"slug": "Sheikh_Zayed_Grand_Mosque", "query": "Sheikh Zayed Grand Mosque Abu Dhabi white domes landmark", "safe_image": ""},
    ("united arab emirates", "palm jumeirah"): {"slug": "Palm_Jumeirah", "query": "Palm Jumeirah Dubai artificial archipelago aerial coast", "safe_image": ""},
    ("united arab emirates", "dubai marina"): {"slug": "Dubai_Marina", "query": "Dubai Marina skyscrapers canal waterfront UAE", "safe_image": ""},
    ("united arab emirates", "louvre abu dhabi"): {"slug": "Louvre_Abu_Dhabi", "query": "Louvre Abu Dhabi dome museum Saadiyat island", "safe_image": ""},
    ("united arab emirates", "dubai creek"): {"slug": "Dubai_Creek", "query": "Dubai Creek historic waterway abra traditional boats", "safe_image": ""},

    # Turkey
    ("turkey", "hagia sophia"): {"slug": "Hagia_Sophia", "query": "Hagia Sophia Istanbul Turkey dome historic landmark", "safe_image": ""},
    ("turkey", "blue mosque"): {"slug": "Blue_Mosque,_Istanbul", "query": "Blue Mosque Sultan Ahmed Mosque Istanbul Turkey landmark", "safe_image": ""},
    ("turkey", "cappadocia"): {"slug": "Cappadocia", "query": "Cappadocia fairy chimneys hot air balloons Turkey landscape", "safe_image": ""},
    ("turkey", "pamukkale"): {"slug": "Pamukkale", "query": "Pamukkale thermal terraces travertine pools Turkey landmark", "safe_image": ""},
    ("turkey", "topkapi palace"): {"slug": "Topkapı_Palace", "query": "Topkapi Palace Istanbul Ottoman imperial residence Turkey", "safe_image": ""},
    ("turkey", "ephesus"): {"slug": "Ephesus", "query": "Ephesus ancient Greek Roman ruins Library of Celsus Turkey", "safe_image": ""},

    # Egypt
    ("egypt", "great pyramid of giza"): {"slug": "Great_Pyramid_of_Giza", "query": "Great Pyramid of Giza Cairo Egypt ancient monument landmark", "safe_image": ""},
    ("egypt", "valley of the kings"): {"slug": "Valley_of_the_Kings", "query": "Valley of the Kings Luxor Egypt ancient tombs archaeological site", "safe_image": ""},
    ("egypt", "karnak temple"): {"slug": "Karnak", "query": "Karnak temple complex Luxor Egypt columns ancient ruins", "safe_image": ""},
    ("egypt", "abu simbel"): {"slug": "Abu_Simbel", "query": "Abu Simbel temples colossal statues Ramesses II Egypt", "safe_image": ""},
    ("egypt", "egyptian museum"): {"slug": "Egyptian_Museum", "query": "Egyptian Museum Tahrir Square Cairo antiquities museum", "safe_image": ""},
    ("egypt", "nile river"): {"slug": "Nile", "query": "Nile River Egypt felucca boat landscape waterway", "safe_image": ""},

    # Nepal
    ("nepal", "mount everest"): {"slug": "Mount_Everest", "query": "Mount Everest Himalayas mountain peak landscape Nepal", "safe_image": ""},
    ("nepal", "kathmandu durbar square"): {"slug": "Kathmandu_Durbar_Square", "query": "Kathmandu Durbar Square ancient palaces temples Nepal landmark", "safe_image": ""},
    ("nepal", "pokhara"): {"slug": "Pokhara", "query": "Pokhara Annapurna mountains lake view Nepal landscape", "safe_image": ""},
    ("nepal", "phewa lake"): {"slug": "Phewa_Lake", "query": "Phewa Lake Pokhara boat Annapurna reflection Nepal", "safe_image": ""},
    ("nepal", "chitwan national park"): {"slug": "Chitwan_National_Park", "query": "Chitwan National Park wildlife rhino jungle Nepal", "safe_image": ""},
    ("nepal", "swayambhunath"): {"slug": "Swayambhunath", "query": "Swayambhunath Monkey Temple stupa Kathmandu Nepal landmark", "safe_image": ""},

    # Vietnam
    ("vietnam", "ha long bay"): {"slug": "Hạ_Long_Bay", "query": "Ha Long Bay emerald water limestone islands Vietnam landscape", "safe_image": ""},
    ("vietnam", "hoi an ancient town"): {"slug": "Hội_An", "query": "Hoi An Ancient Town lantern canal street Vietnam historic", "safe_image": ""},
    ("vietnam", "ho chi minh city"): {"slug": "Ho_Chi_Minh_City", "query": "Ho Chi Minh City skyline Saigon Notre Dame cathedral Vietnam", "safe_image": ""},
    ("vietnam", "hanoi old quarter"): {"slug": "Old_Quarter,_Hanoi", "query": "Old Quarter Hanoi historic street Vietnam market tourism", "safe_image": ""},
    ("vietnam", "da nang"): {"slug": "Da_Nang", "query": "Golden Bridge Ba Na Hills Da Nang coastal city Vietnam", "safe_image": ""},
    ("vietnam", "phong nha caves"): {"slug": "Phong_Nha_Cave", "query": "Phong Nha Cave limestone karsts underground river Vietnam", "safe_image": ""},

    # Indonesia
    ("indonesia", "bali"): {"slug": "Bali", "query": "Bali island temples coast rice terraces Indonesia landscape", "safe_image": ""},
    ("indonesia", "borobudur"): {"slug": "Borobudur", "query": "Borobudur temple Buddhist monument Central Java Indonesia landmark", "safe_image": ""},
    ("indonesia", "ubud"): {"slug": "Ubud", "query": "Ubud Bali rice terraces cultural temple lush green Indonesia", "safe_image": ""},
    ("indonesia", "komodo national park"): {"slug": "Komodo_National_Park", "query": "Komodo National Park dragon island landscape East Nusa Tenggara", "safe_image": ""},
    ("indonesia", "mount bromo"): {"slug": "Mount_Bromo", "query": "Mount Bromo volcano crater East Java sunrise Indonesia", "safe_image": ""},
    ("indonesia", "tanah lot"): {"slug": "Tanah_Lot", "query": "Tanah Lot temple rock formation ocean sunset Bali Indonesia", "safe_image": ""},

    # Brazil
    ("brazil", "christ the redeemer"): {"slug": "Christ_the_Redeemer_(statue)", "query": "Christ the Redeemer statue Corcovado Rio de Janeiro Brazil landmark", "safe_image": ""},
    ("brazil", "copacabana beach"): {"slug": "Copacabana,_Rio_de_Janeiro", "query": "Copacabana beach promenade Rio de Janeiro Brazil coast", "safe_image": ""},
    ("brazil", "iguazu falls"): {"slug": "Iguazu_Falls", "query": "Iguazu Falls waterfalls rainforest border Parana Brazil landscape", "safe_image": ""},
    ("brazil", "amazon rainforest"): {"slug": "Amazon_rainforest", "query": "Amazon rainforest river basin jungle Brazil nature landscape", "safe_image": ""},
    ("brazil", "sugarloaf mountain"): {"slug": "Sugarloaf_Mountain", "query": "Sugarloaf Mountain cable car Guanabara Bay Rio de Janeiro Brazil", "safe_image": ""},
    ("brazil", "salvador"): {"slug": "Salvador,_Bahia", "query": "Pelourinho historic centre Salvador Bahia colorful architecture Brazil", "safe_image": ""},

    # Verified Authentic Signature Global Dishes (Cooked/Prepared Dishes)
    ("nepal", "dal bhat"): {"slug": "Dal_bhat", "query": "Nepali dal bhat tarkari meal Nagarkot plate", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fe/2015-03-18_Dal_Bhat_Tarkari%2CNagarkot_DSCF2218.jpg/960px-2015-03-18_Dal_Bhat_Tarkari%2CNagarkot_DSCF2218.jpg"},
    ("nepal", "momo"): {"slug": "Momo_(food)", "query": "Momo dumplings Nepal plate food", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a1/Momo_nepal.jpg/960px-Momo_nepal.jpg"},
    ("india", "biryani"): {"slug": "Biryani", "query": "Hyderabadi Dum Biryani pot dish India", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5a/%22Hyderabadi_Dum_Biryani%22.jpg/960px-%22Hyderabadi_Dum_Biryani%22.jpg"},
    ("india", "masala dosa"): {"slug": "Dosa", "query": "Dosa and ghee Indian breakfast plate", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0b/Dosa_and_ghee.jpg/960px-Dosa_and_ghee.jpg"},
    ("japan", "ramen"): {"slug": "Ramen", "query": "Shoyu Ramen noodle soup bowl Japan", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/dc/Shoyu_Ramen.jpg/960px-Shoyu_Ramen.jpg"},
    ("japan", "sushi"): {"slug": "Sushi", "query": "Sushi platter nigiri Japan plate", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/60/Sushi_platter.jpg/960px-Sushi_platter.jpg"},
    ("thailand", "pad thai"): {"slug": "Pad_thai", "query": "Phat Thai kung Chang Khian street stall Thailand", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/39/Phat_Thai_kung_Chang_Khian_street_stall.jpg/960px-Phat_Thai_kung_Chang_Khian_street_stall.jpg"},
    ("italy", "neapolitan pizza"): {"slug": "Neapolitan_pizza", "query": "Eq it-na pizza-margherita pizza Italy", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/960px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},

    # France
    ("france", "croissant & viennoiseries"): {"slug": "Croissant", "query": "Fresh baked French butter croissant pastry", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2a/Croissant-Petr_Kratochvil.jpg/960px-Croissant-Petr_Kratochvil.jpg"},
    ("france", "croissant"): {"slug": "Croissant", "query": "Fresh baked French butter croissant pastry", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2a/Croissant-Petr_Kratochvil.jpg/960px-Croissant-Petr_Kratochvil.jpg"},
    ("france", "french cheese"): {"slug": "French_cheese", "query": "Plateau de fromages assortis French cheese platter", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/36/Plateau_de_fromages_assortis.jpg/960px-Plateau_de_fromages_assortis.jpg"},
    ("france", "baguette"): {"slug": "Baguette", "query": "Baguettes in a basket French bread", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f5/Baguettes_in_a_basket.jpg/960px-Baguettes_in_a_basket.jpg"},
    ("france", "ratatouille"): {"slug": "Ratatouille", "query": "Ratatouille cooked vegetable dish France", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b3/Ratatouille_01.jpg/960px-Ratatouille_01.jpg"},
    ("france", "crêpes"): {"slug": "Cr%C3%AApe", "query": "Crepes suzette flambees French pancakes", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/13/Cr%C3%AApes_suzette_flamb%C3%A9es.jpg/960px-Cr%C3%AApes_suzette_flamb%C3%A9es.jpg"},
    ("france", "crepes"): {"slug": "Cr%C3%AApe", "query": "Crepes suzette flambees French pancakes", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/13/Cr%C3%AApes_suzette_flamb%C3%A9es.jpg/960px-Cr%C3%AApes_suzette_flamb%C3%A9es.jpg"},

    # Germany, Spain, UK
    ("germany", "bratwurst"): {"slug": "Bratwurst", "query": "German Bratwuerste grilled sausage Germany", "safe_image": "https://upload.wikimedia.org/wikipedia/commons/b/b0/German_Bratw%C3%BCrste.jpg"},
    ("spain", "paella"): {"slug": "Paella", "query": "Paella Valenciana original pan Spain", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ed/01_Paella_Valenciana_original.jpg/960px-01_Paella_Valenciana_original.jpg"},
    ("united kingdom", "fish and chips"): {"slug": "Fish_and_chips", "query": "Fish and chips Blackpool England plate", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/ff/Fish_and_chips_blackpool.jpg/960px-Fish_and_chips_blackpool.jpg"},

    # Brazil
    ("brazil", "feijoada"): {"slug": "Feijoada", "query": "Feijoada Brazilian dish Sao Luis Maranhao", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ca/Feijoada_%28Brazilian_dish%29%2C_S%C3%A3o_Lu%C3%ADs%2C_Maranh%C3%A3o.jpg/960px-Feijoada_%28Brazilian_dish%29%2C_S%C3%A3o_Lu%C3%ADs%2C_Maranh%C3%A3o.jpg"},
    ("brazil", "moqueca"): {"slug": "Moqueca", "query": "Moqueca de peixe em Arraial d Ajuda seafood stew", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d7/Moqueca_de_peixe_em_Arraial_d%27Ajuda.jpg/960px-Moqueca_de_peixe_em_Arraial_d%27Ajuda.jpg"},
    ("brazil", "brigadeiro"): {"slug": "Brigadeiro", "query": "Brigadeiro Brazilian chocolate fudge truffle", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6b/Brigadeiro.jpg/960px-Brigadeiro.jpg"},
    ("brazil", "pão de queijo"): {"slug": "P%C3%A3o_de_queijo", "query": "Pao de queijo Brazilian cheese bread", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5e/P%C3%A3o_de_queijo.jpg/960px-P%C3%A3o_de_queijo.jpg"},

    # USA
    ("usa", "classic cheeseburger"): {"slug": "Cheeseburger", "query": "Cheeseburger with fries American food", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4d/Cheeseburger.jpg/960px-Cheeseburger.jpg"},
    ("united states", "classic cheeseburger"): {"slug": "Cheeseburger", "query": "Cheeseburger with fries American food", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4d/Cheeseburger.jpg/960px-Cheeseburger.jpg"},
    ("usa", "hamburger"): {"slug": "Hamburger", "query": "Hamburger sandwich American food", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4d/Cheeseburger.jpg/960px-Cheeseburger.jpg"},
    ("united states", "hamburger"): {"slug": "Hamburger", "query": "Hamburger sandwich American food", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4d/Cheeseburger.jpg/960px-Cheeseburger.jpg"},
    ("usa", "clam chowder"): {"slug": "Clam_chowder", "query": "New England clam chowder bowl soup", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e3/Clam_chowder.jpg/960px-Clam_chowder.jpg"},
    ("united states", "clam chowder"): {"slug": "Clam_chowder", "query": "New England clam chowder bowl soup", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e3/Clam_chowder.jpg/960px-Clam_chowder.jpg"},
    ("usa", "apple pie"): {"slug": "Apple_pie", "query": "Baked apple pie slice American dessert", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4b/Apple_pie.jpg/960px-Apple_pie.jpg"},
    ("united states", "apple pie"): {"slug": "Apple_pie", "query": "Baked apple pie slice American dessert", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4b/Apple_pie.jpg/960px-Apple_pie.jpg"},

    # China
    ("china", "mapo tofu"): {"slug": "Mapo_tofu", "query": "Chen Mapo Tofu Sichuan dish China", "safe_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Chen_Mapo_Tofu.jpg/960px-Chen_Mapo_Tofu.jpg"},

    # Canada
    ("canada", "poutine"): {"slug": "Poutine", "query": "Poutine cheese curds fries gravy Canada", "safe_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Poutine.JPG/960px-Poutine.JPG"},
    ("canada", "butter tart"): {"slug": "Butter_tart", "query": "Butter tart Canadian dessert pastry", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/42/Butter_tart.jpg/960px-Butter_tart.jpg"},
    ("canada", "butter tarts"): {"slug": "Butter_tart", "query": "Butter tart Canadian dessert pastry", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/42/Butter_tart.jpg/960px-Butter_tart.jpg"},
    ("canada", "tourtière"): {"slug": "Tourti%C3%A8re", "query": "Tourtiere du Lac Saint Jean pie Canada", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/Tourti%C3%A8re_du_Lac-Saint-Jean.JPG/960px-Tourti%C3%A8re_du_Lac-Saint-Jean.JPG"},
    ("canada", "tourtiere"): {"slug": "Tourti%C3%A8re", "query": "Tourtiere du Lac Saint Jean pie Canada", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/Tourti%C3%A8re_du_Lac-Saint-Jean.JPG/960px-Tourti%C3%A8re_du_Lac-Saint-Jean.JPG"},
    ("canada", "nanaimo bar"): {"slug": "Nanaimo_bar", "query": "Nanaimo bar dessert Canada", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/14/Nanaimo_bar.jpg/960px-Nanaimo_bar.jpg"},
    ("canada", "nanaimo bars"): {"slug": "Nanaimo_bar", "query": "Nanaimo bar dessert Canada", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/14/Nanaimo_bar.jpg/960px-Nanaimo_bar.jpg"},

    # Australia
    ("australia", "aussie meat pie"): {"slug": "Meat_pie_(Australia_and_New_Zealand)", "query": "Four N Twenty Meat Pie Australia", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a9/Four%27N_Twenty_Pie_at_the_AFL.jpg/960px-Four%27N_Twenty_Pie_at_the_AFL.jpg"},
    ("australia", "meat pie"): {"slug": "Meat_pie_(Australia_and_New_Zealand)", "query": "Four N Twenty Meat Pie Australia", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a9/Four%27N_Twenty_Pie_at_the_AFL.jpg/960px-Four%27N_Twenty_Pie_at_the_AFL.jpg"},
    ("australia", "pavlova"): {"slug": "Pavlova_(dessert)", "query": "Pavlova dessert fresh fruit Australia", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/65/Pavlova_dessert.jpg/960px-Pavlova_dessert.jpg"},
    ("australia", "lamington"): {"slug": "Lamington", "query": "Lamingtons sponge cake chocolate coconut", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/cf/Lamingtons.jpg/960px-Lamingtons.jpg"},
    ("australia", "lamingtons"): {"slug": "Lamington", "query": "Lamingtons sponge cake chocolate coconut", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/cf/Lamingtons.jpg/960px-Lamingtons.jpg"},

    # South Korea, Vietnam, Indonesia
    ("south korea", "bibimbap"): {"slug": "Bibimbap", "query": "Dolsot bibimbap Korean bowl dish", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/44/Dolsot-bibimbap.jpg/960px-Dolsot-bibimbap.jpg"},
    ("vietnam", "pho"): {"slug": "Pho", "query": "Pho Beef Noodles Vietnam bowl dish", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/53/Pho-Beef-Noodles-2008.jpg/960px-Pho-Beef-Noodles-2008.jpg"},
    ("indonesia", "nasi goreng"): {"slug": "Nasi_goreng", "query": "Nasi Goreng Kampung Indonesian fried rice plate", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c7/Nasi_Goreng_Kampung_%2811967588375%29.jpg/960px-Nasi_Goreng_Kampung_%2811967588375%29.jpg"},

    # Additional Guaranteed Landmark Entries
    ("india", "varanasi ghats"): {"slug": "Ghats_in_Varanasi", "query": "Varanasi Ganges ghats temples Uttar Pradesh India tourism", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0e/Varanasi%2C_India%2C_Ghats%2C_Cremation_ceremony_in_progress.jpg/960px-Varanasi%2C_India%2C_Ghats%2C_Cremation_ceremony_in_progress.jpg"},
    ("india", "golden temple"): {"slug": "Harmandir_Sahib", "query": "Golden Temple Amritsar Punjab India landmark", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/94/The_Golden_Temple_of_Amrithsar_7.jpg/960px-The_Golden_Temple_of_Amrithsar_7.jpg"},
    ("india", "india gate"): {"slug": "India_Gate", "query": "India Gate New Delhi memorial landmark", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3b/India_Gate_front.jpg/960px-India_Gate_front.jpg"},
    ("japan", "fushimi inari shrine"): {"slug": "Fushimi_Inari-taisha", "query": "Fushimi Inari Taisha Kyoto Japan torii gates", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0e/Torii_path_with_lantern_at_Fushimi_Inari_Taisha_Shrine%2C_Kyoto%2C_Japan.jpg/960px-Torii_path_with_lantern_at_Fushimi_Inari_Taisha_Shrine%2C_Kyoto%2C_Japan.jpg"},
    ("japan", "mount fuji"): {"slug": "Mount_Fuji", "query": "Mount Fuji volcano landscape Japan tourism", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f8/View_of_Mount_Fuji_from_%C5%8Cwakudani_20211202.jpg/960px-View_of_Mount_Fuji_from_%C5%8Cwakudani_20211202.jpg"},
    ("nepal", "pashupatinath temple"): {"slug": "Pashupatinath_Temple", "query": "Pashupatinath Temple Kathmandu Bagmati river pagoda Nepal", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1f/Pashupatinath_Temple-2020.jpg/960px-Pashupatinath_Temple-2020.jpg"},
    ("nepal", "boudhanath stupa"): {"slug": "Boudhanath", "query": "Boudhanath Stupa Kathmandu Buddhist stupa prayer flags Nepal", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4d/Boudhanath_stupa_%2C_Kathmandu%2C_Nepal.jpg/960px-Boudhanath_stupa_%2C_Kathmandu%2C_Nepal.jpg"},
    ("thailand", "wat arun"): {"slug": "Wat_Arun", "query": "Wat Arun temple Bangkok Thailand landmark tourism", "safe_image": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2a/%E0%B9%80%E0%B8%88%E0%B8%94%E0%B8%B5%E0%B8%A2%E0%B9%8C%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%98%E0%B8%B2%E0%B8%99%E0%B8%97%E0%B8%A3%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B2%E0%B8%87%E0%B8%84%E0%B9%8C%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%AD%E0%B8%A3%E0%B8%B8%E0%B8%932.jpg/960px-%E0%B9%80%E0%B8%88%E0%B8%94%E0%B8%B5%E0%B8%A2%E0%B9%8C%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%98%E0%B8%B2%E0%B8%99%E0%B8%97%E0%B8%A3%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B2%E0%B8%87%E0%B8%84%E0%B9%8C%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%AD%E0%B8%A3%E0%B8%B8%E0%B8%932.jpg"}
}


# ============================================================
# SEARCH & RETRIEVAL HELPERS
# ============================================================

def _fetch_page_thumb_by_slug(target_slug, item_name, country, card_type, excluded, gender="unisex"):
    if not target_slug:
        return None
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "titles": target_slug,
                "prop": "pageimages|extracts|info",
                "piprop": "thumbnail",
                "pithumbsize": 960,
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url",
                "redirects": 1
            },
            headers=WIKI_HEADERS,
            timeout=8
        )
        if r.status_code == 200:
            pages = r.json().get("query", {}).get("pages", {})
            for page in pages.values():
                if page.get("pageid", -1) != -1:
                    thumb = page.get("thumbnail", {}).get("source")
                    p_title = page.get("title", "")
                    extract = page.get("extract", "")
                    if thumb and thumb not in excluded:
                        if card_type == "food" and is_valid_food_image(p_title, extract, thumb, item_name, country):
                            return thumb
                        elif card_type in ("clothing", "attire", "dress") and is_valid_attire_image(p_title, extract, thumb, item_name, country, gender=gender):
                            return thumb
                        elif card_type in ("place", "religious", "culture") and is_valid_place_image(p_title, extract, thumb, item_name, country):
                            return thumb
    except Exception:
        pass
    return None


def _search_wiki_page_image(query, item_name, country, card_type, excluded, gender="unisex"):
    if not query:
        return None
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": query,
                "gsrlimit": 6,
                "prop": "pageimages|extracts|info",
                "piprop": "thumbnail",
                "pithumbsize": 960,
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url"
            },
            headers=WIKI_HEADERS,
            timeout=7
        )
        if r.status_code == 200:
            pages = list(r.json().get("query", {}).get("pages", {}).values())
            pages.sort(key=lambda p: p.get("index", 999))
            for p in pages:
                thumb = p.get("thumbnail", {}).get("source")
                p_title = p.get("title", "")
                extract = p.get("extract", "")
                if thumb and thumb not in excluded:
                    if card_type == "food" and is_valid_food_image(p_title, extract, thumb, item_name, country):
                        return thumb
                    elif card_type in ("clothing", "attire", "dress") and is_valid_attire_image(p_title, extract, thumb, item_name, country, gender=gender):
                        return thumb
                    elif card_type in ("place", "religious", "culture") and is_valid_place_image(p_title, extract, thumb, item_name, country):
                        return thumb
    except Exception:
        pass
    return None


def _search_commons_image(query, item_name, country, card_type, excluded, gender="unisex"):
    if not query:
        return None
    try:
        r = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": query,
                "gsrnamespace": 6,
                "gsrlimit": 8,
                "prop": "imageinfo",
                "iiprop": "url|extmetadata",
                "iiurlwidth": 960
            },
            headers=WIKI_HEADERS,
            timeout=7
        )
        if r.status_code == 200:
            pages = list(r.json().get("query", {}).get("pages", {}).values())
            pages.sort(key=lambda p: p.get("index", 999))
            for p in pages:
                p_title = p.get("title", "")
                info = p.get("imageinfo", [])
                if info:
                    thumb = info[0].get("thumburl") or info[0].get("url")
                    extmeta = info[0].get("extmetadata", {})
                    if thumb and thumb not in excluded:
                        if card_type == "food" and is_valid_food_image(p_title, "", thumb, item_name, country):
                            return thumb
                        elif card_type in ("clothing", "attire", "dress") and is_valid_attire_image(p_title, "", thumb, item_name, country, gender=gender, metadata=extmeta):
                            return thumb
                        elif card_type in ("place", "religious", "culture") and is_valid_place_image(p_title, "", thumb, item_name, country):
                            return thumb
    except Exception:
        pass
    return None


def _get_place_aliases(clean_place, norm_place):
    aliases_map = {
        "taj mahal": ["Taj Mahal"],
        "golden temple": ["Harmandir Sahib", "Golden Temple"],
        "india gate": ["India Gate"],
        "meenakshi temple": ["Meenakshi Temple", "Meenakshi Amman Temple"],
        "tirumala temple": ["Venkateswara Temple, Tirumala"],
        "varanasi ghats": ["Ghats in Varanasi", "Varanasi"],
        "varanasi": ["Varanasi", "Ghats in Varanasi"],
        "dal lake": ["Dal Lake"],
        "qutub minar": ["Qutb Minar"],
        "mount everest": ["Mount Everest"],
        "pashupatinath temple": ["Pashupatinath Temple"],
        "boudhanath stupa": ["Boudhanath"],
        "kathmandu durbar square": ["Kathmandu Durbar Square"],
        "swayambhunath": ["Swayambhunath"],
        "swayambhunath (monkey temple)": ["Swayambhunath"],
        "peace pagoda (shanti stupa)": ["World Peace Pagoda, Pokhara"],
        "mount fuji": ["Mount Fuji"],
        "fushimi inari shrine": ["Fushimi Inari-taisha"],
        "kinkaku-ji": ["Kinkaku-ji"],
        "kinkaku-ji (golden pavilion)": ["Kinkaku-ji"],
        "todai-ji": ["Tōdai-ji"],
        "senso-ji": ["Sensō-ji"],
        "tokyo tower": ["Tokyo Tower"],
        "tokyo skytree & shibuya crossing": ["Tokyo Skytree", "Shibuya Crossing"],
        "wat arun": ["Wat Arun"],
        "wat arun (temple of dawn)": ["Wat Arun"],
        "grand palace": ["Grand Palace"],
        "grand palace & temple of the emerald buddha": ["Grand Palace", "Wat Phra Kaew"],
        "railay beach": ["Railay Beach"],
        "railay beach & krabi cliffs": ["Railay Beach"],
        "phi phi islands": ["Phi Phi Islands"],
        "phi phi islands & maya bay": ["Phi Phi Islands"],
        "great wall of china": ["Great Wall of China"],
        "forbidden city": ["Forbidden City"],
        "terracotta army": ["Terracotta Army"],
        "the bund": ["The Bund"],
        "zhangjiajie": ["Zhangjiajie National Forest Park", "Zhangjiajie"],
        "gyeongbokgung palace": ["Gyeongbokgung"],
        "n seoul tower": ["N Seoul Tower"],
        "bukchon hanok village": ["Bukchon Hanok Village"],
        "ha long bay": ["Hạ Long Bay"],
        "hoi an ancient town": ["Hội An"],
        "borobudur": ["Borobudur"],
        "tanah lot": ["Tanah Lot"],
        "eiffel tower": ["Eiffel Tower"],
        "louvre museum": ["Louvre Museum", "Louvre"],
        "palace of versailles": ["Palace of Versailles"],
        "mont saint-michel": ["Mont-Saint-Michel"],
        "colosseum": ["Colosseum"],
        "colosseum & roman forum": ["Colosseum"],
        "leaning tower of pisa": ["Leaning Tower of Pisa"],
        "florence cathedral": ["Florence Cathedral"],
        "florence cathedral (duomo)": ["Florence Cathedral"],
        "venice grand canal & st. mark's": ["Grand Canal (Venice)"],
        "brandenburg gate": ["Brandenburg Gate"],
        "neuschwanstein castle": ["Neuschwanstein Castle"],
        "cologne cathedral": ["Cologne Cathedral"],
        "sagrada família": ["Sagrada Família"],
        "alhambra": ["Alhambra"],
        "park güell": ["Park Güell"],
        "big ben": ["Big Ben"],
        "big ben & westminster palace": ["Big Ben", "Palace of Westminster"],
        "tower of london": ["Tower of London"],
        "tower of london & tower bridge": ["Tower of London", "Tower Bridge"],
        "stonehenge": ["Stonehenge"],
        "stonehenge prehistoric monument": ["Stonehenge"],
        "sydney opera house": ["Sydney Opera House"],
        "sydney opera house & harbour bridge": ["Sydney Opera House", "Sydney Harbour Bridge"],
        "great barrier reef": ["Great Barrier Reef"],
        "uluru": ["Uluru"],
        "uluru (ayers rock)": ["Uluru"],
        "bondi beach": ["Bondi Beach"],
        "bondi beach & coastal walk": ["Bondi Beach"],
        "great ocean road": ["Twelve Apostles (Victoria)", "Great Ocean Road"],
        "great ocean road (twelve apostles)": ["Twelve Apostles (Victoria)", "Great Ocean Road"],
        "christ the redeemer": ["Christ the Redeemer (statue)"],
        "christ the redeemer & corcovado": ["Christ the Redeemer (statue)", "Corcovado"],
        "copacabana beach": ["Copacabana, Rio de Janeiro", "Copacabana"],
        "copacabana & ipanema beaches": ["Copacabana", "Ipanema"],
        "iguazu falls": ["Iguazu Falls"],
        "iguazu falls (cataratas do iguaçu)": ["Iguazu Falls"],
        "amazon rainforest": ["Amazon rainforest"],
        "amazon rainforest & rio negro": ["Amazon rainforest"],
        "sugarloaf mountain": ["Sugarloaf Mountain"],
        "sugarloaf mountain (pão de açúcar)": ["Sugarloaf Mountain"],
        "statue of liberty": ["Statue of Liberty"],
        "grand canyon": ["Grand Canyon"],
        "grand canyon national park": ["Grand Canyon"],
        "yellowstone national park": ["Yellowstone National Park"],
        "times square": ["Times Square"],
        "times square & central park": ["Times Square", "Central Park"],
        "golden gate bridge": ["Golden Gate Bridge"],
        "niagara falls": ["Niagara Falls", "Horseshoe Falls"],
        "niagara falls (horseshoe falls)": ["Niagara Falls", "Horseshoe Falls"],
        "banff national park & lake louise": ["Banff National Park", "Lake Louise (Alberta)"]
    }
    c_l = clean_place.lower()
    n_l = norm_place.lower()
    results = []
    if c_l in aliases_map:
        results.extend(aliases_map[c_l])
    if n_l in aliases_map and n_l != c_l:
        for a in aliases_map[n_l]:
            if a not in results:
                results.append(a)
    return results


def _get_food_aliases(clean_dish, norm_dish):
    aliases_map = {
        "dal bhat": ["Dal bhat"],
        "ceviche": ["Ceviche"],
        "ceviche tradicional": ["Ceviche"],
        "momo": ["Momo (food)"],
        "thukpa": ["Thukpa"],
        "sel roti": ["Sel roti"],
        "choila": ["Choila"],
        "biryani": ["Biryani"],
        "masala dosa": ["Dosa"],
        "butter chicken": ["Butter chicken"],
        "idli": ["Idli (food)", "Idli"],
        "samosa": ["Samosa"],
        "rogan josh": ["Rogan josh"],
        "kashmiri kahwa": ["Kahwah"],
        "chole bhature": ["Chole bhature"],
        "gulab jamun": ["Gulab jamun"],
        "sushi": ["Sushi"],
        "sushi & sashimi": ["Sushi"],
        "ramen": ["Ramen"],
        "tempura": ["Tempura"],
        "pad thai": ["Pad thai"],
        "tom yum": ["Tom yum"],
        "tom yum goong": ["Tom yum"],
        "green curry": ["Green curry"],
        "green curry (gaeng keow wan)": ["Green curry"],
        "som tum": ["Som tum", "Papaya salad"],
        "som tum (papaya salad)": ["Som tum", "Papaya salad"],
        "pho": ["Pho"],
        "banh mi": ["Bánh mì"],
        "nasi goreng": ["Nasi goreng"],
        "satay": ["Satay"],
        "rendang": ["Rendang"],
        "bibimbap": ["Bibimbap"],
        "kimchi": ["Kimchi"],
        "bulgogi": ["Bulgogi"],
        "peking duck": ["Peking duck"],
        "mapo tofu": ["Mapo tofu"],
        "dim sum": ["Dim sum"],
        "neapolitan pizza": ["Neapolitan pizza", "Pizza"],
        "pizza": ["Neapolitan pizza", "Pizza"],
        "carbonara": ["Carbonara"],
        "pasta carbonara & cacio e pepe": ["Carbonara"],
        "risotto alla milanese": ["Risotto"],
        "tiramisu": ["Tiramisu"],
        "gelato": ["Gelato"],
        "croissant": ["Croissant"],
        "croissant & viennoiseries": ["Croissant"],
        "baguette": ["Baguette"],
        "ratatouille": ["Ratatouille"],
        "crêpes": ["Crêpe"],
        "crêpes & galettes": ["Crêpe"],
        "french cheese": ["French cheese"],
        "artisan french cheeses": ["French cheese"],
        "paella": ["Paella"],
        "tapas": ["Tapas"],
        "gazpacho": ["Gazpacho"],
        "bratwurst": ["Bratwurst"],
        "schnitzel": ["Schnitzel"],
        "sauerbraten": ["Sauerbraten"],
        "fish and chips": ["Fish and chips"],
        "sunday roast": ["Sunday roast"],
        "shepherd's pie": ["Shepherd's pie"],
        "feijoada": ["Feijoada"],
        "moqueca": ["Moqueca"],
        "brigadeiro": ["Brigadeiro"],
        "pão de queijo": ["Pão de queijo"],
        "cheeseburger": ["Cheeseburger"],
        "classic cheeseburger": ["Cheeseburger"],
        "clam chowder": ["Clam chowder"],
        "apple pie": ["Apple pie"],
        "poutine": ["Poutine"],
        "butter tarts": ["Butter tart"],
        "butter tart": ["Butter tart"],
        "tourtière": ["Tourtière"],
        "nanaimo bars": ["Nanaimo bar"],
        "aussie meat pie": ["Meat pie (Australia and New Zealand)"],
        "meat pie": ["Meat pie (Australia and New Zealand)"],
        "pavlova": ["Pavlova (cake)", "Pavlova (dessert)"],
        "lamington": ["Lamington"],
        "lamingtons": ["Lamington"],
        "koshari": ["Koshary"],
        "ful medames": ["Ful medames"],
        "bobotie": ["Bobotie"],
        "bunny chow": ["Bunny chow"]
    }
    c_l = clean_dish.lower()
    n_l = norm_dish.lower()
    results = []
    if c_l in aliases_map:
        results.extend(aliases_map[c_l])
    if n_l in aliases_map and n_l != c_l:
        for a in aliases_map[n_l]:
            if a not in results:
                results.append(a)
    return results


# ============================================================
# THREE STRICTLY SEPARATED RETRIEVAL PIPELINES
# ============================================================

@st.cache_data(ttl=604800, show_spinner=False)
def get_place_image(place_name, country, location="", slug="", exclude_images=()):
    """
    Verified image retrieval strictly for PLACE / LANDMARK / ATTRACTION.
    Guarantees:
    - Never returns people / tourists / selfies / portraits / crowds / posing / hotel rooms.
    - Uses exact place name + location/region + country.
    - Religious sites show the actual architectural site/complex.
    - If unverified, returns None (NO generic city/country fallbacks!).
    """
    clean_place = str(place_name or "").strip()
    norm_country = normalize_country_name(country) if country else ""
    loc_str = str(location or "").strip() if location and str(location).strip().lower() != norm_country.lower() else ""
    excluded = set(exclude_images) if exclude_images else set()
    norm_place = normalize_card_title(clean_place, "place")

    if not clean_place:
        return None

    # 1. Curated Canonical Place lookup
    for key in [
        (norm_country.casefold(), clean_place.casefold()),
        (norm_country.casefold(), norm_place.casefold()),
    ]:
        if key in DESTINATION_CANONICAL_PAGES:
            curated = DESTINATION_CANONICAL_PAGES[key]
            safe_img = curated.get("safe_image")
            if safe_img and safe_img not in excluded and is_valid_place_image(clean_place, "", safe_img, clean_place, norm_country):
                return safe_img
            c_slug = curated.get("slug")
            if c_slug:
                img = _fetch_page_thumb_by_slug(c_slug, clean_place, norm_country, "place", excluded)
                if img:
                    return img
            break

    # 2. Direct Slug
    if slug:
        img = _fetch_page_thumb_by_slug(slug, clean_place, norm_country, "place", excluded)
        if img:
            return img

    # 3. Known Aliases
    aliases = _get_place_aliases(clean_place, norm_place)
    for alt_slug in aliases:
        img = _fetch_page_thumb_by_slug(alt_slug, clean_place, norm_country, "place", excluded)
        if img:
            return img

    # 4. Wikipedia generator=search: EXACT PLACE NAME + CITY/REGION + COUNTRY
    search_queries = [
        f"{clean_place} {loc_str} {norm_country} landmark".strip() if loc_str else f"{clean_place} {norm_country} landmark".strip(),
        f"{clean_place} {norm_country}".strip(),
        f"{norm_place} {norm_country}".strip()
    ]
    for sq in filter(None, search_queries):
        img = _search_wiki_page_image(sq, clean_place, norm_country, "place", excluded)
        if img:
            return img

    # 5. Wikimedia Commons search
    commons_queries = [
        f"{clean_place} {norm_country} landmark".strip(),
        f"{clean_place} {loc_str}".strip() if loc_str else f"{clean_place} {norm_country}".strip()
    ]
    for cq in commons_queries:
        img = _search_commons_image(cq, clean_place, norm_country, "place", excluded)
        if img:
            return img

    return None


@st.cache_data(ttl=604800, show_spinner=False)
def get_food_image(dish_name, country, slug="", exclude_images=()):
    """
    Verified image retrieval strictly for PREPARED FOOD DISHES.
    Guarantees:
    - Never returns raw ingredients, raw meat, spices, grain sacks, empty tables, or people eating.
    - Uses exact dish name + country.
    - If unverified, returns None (NO generic food fallbacks!).
    """
    clean_dish = str(dish_name or "").strip()
    norm_country = normalize_country_name(country) if country else ""
    excluded = set(exclude_images) if exclude_images else set()
    norm_dish = normalize_card_title(clean_dish, "food")

    if not clean_dish:
        return None

    # 1. Curated Canonical Food lookup
    for key in [
        (norm_country.casefold(), clean_dish.casefold()),
        (norm_country.casefold(), norm_dish.casefold()),
    ]:
        if key in DESTINATION_CANONICAL_PAGES:
            curated = DESTINATION_CANONICAL_PAGES[key]
            safe_img = curated.get("safe_image")
            if safe_img and safe_img not in excluded and is_valid_food_image(clean_dish, "", safe_img, clean_dish, norm_country):
                return safe_img
            c_slug = curated.get("slug")
            if c_slug:
                img = _fetch_page_thumb_by_slug(c_slug, clean_dish, norm_country, "food", excluded)
                if img:
                    return img
            break

    # 2. Direct Slug
    if slug:
        img = _fetch_page_thumb_by_slug(slug, clean_dish, norm_country, "food", excluded)
        if img:
            return img

    # 3. Known Aliases
    aliases = _get_food_aliases(clean_dish, norm_dish)
    for alt_slug in aliases:
        img = _fetch_page_thumb_by_slug(alt_slug, clean_dish, norm_country, "food", excluded)
        if img:
            return img

    # 4. Wikipedia generator=search: EXACT DISH + COUNTRY
    search_queries = [
        f"{clean_dish} {norm_country} dish",
        f"{clean_dish} {norm_country}",
        f"{norm_dish} {norm_country} food",
        f"{clean_dish} prepared dish"
    ]
    for sq in filter(None, search_queries):
        img = _search_wiki_page_image(sq, clean_dish, norm_country, "food", excluded)
        if img:
            return img

    # 5. Wikimedia Commons search
    commons_queries = [
        f"{clean_dish} {norm_country} dish plate",
        f"{clean_dish} cooked dish food"
    ]
    for cq in commons_queries:
        img = _search_commons_image(cq, clean_dish, norm_country, "food", excluded)
        if img:
            return img

    return None


@st.cache_data(ttl=604800, show_spinner=False)
def get_attire_image(attire_name, country, gender="unisex", exclude_images=()):
    """
    Verified image retrieval strictly for ADULT TRADITIONAL ATTIRE across all countries.
    Guarantees:
    - Real adults wearing the authentic country-specific outfit.
    - Strictly rejects children, boys, girls, AI generation, mannequins, or fantasy costumes.
    - If no verified photo of an adult wearing the attire exists, returns None ('Authentic adult attire photo unavailable').
    """
    clean_attire = str(attire_name or "").strip()
    norm_country = normalize_country_name(country) if country else ""
    excluded = set(exclude_images) if exclude_images else set()

    if not clean_attire:
        return None

    g_toks = set(re.findall(r'[a-zA-Z]+', str(gender or "").lower()))
    is_men = bool(g_toks & {"men", "male", "man", "groom", "gentleman"})
    is_women = bool(g_toks & {"women", "female", "woman", "bride", "lady"})

    # 1. Check curated traditional clothing in country_data (accept only verified real adult photos)
    local_key = ""
    try:
        clothing_info = get_traditional_clothing(norm_country)
        attires = clothing_info.get("attires") or [clothing_info.get("women"), clothing_info.get("men")]
        for att in attires:
            if not att:
                continue
            a_name = str(att.get("name", "")).lower()
            l_name = str(att.get("local_name", "")).lower()
            att_gender = str(att.get("gender") or "").lower()

            # Strictly ensure att matches caller's requested gender
            if is_women and ("men" in att_gender or "male" in att_gender) and not ("women" in att_gender or "female" in att_gender):
                continue
            if is_men and ("women" in att_gender or "female" in att_gender) and not ("men" in att_gender or "male" in att_gender):
                continue

            if clean_attire.lower() in a_name or clean_attire.lower() in l_name or a_name in clean_attire.lower():
                img = att.get("image")
                if img and img not in excluded and is_valid_attire_image(a_name, "", img, clean_attire, norm_country, gender=gender):
                    return img
                local_key = str(att.get("local_name") or "")
                break
    except Exception:
        pass

    # 2. Dynamic check on Wikipedia for the specific traditional attire article
    core_name = re.sub(rf"^{norm_country}\s+", "", clean_attire, flags=re.IGNORECASE).strip()
    core_clean = re.sub(r"\(.*?\)", "", core_name).strip()
    for candidate in [core_clean, core_name, clean_attire, local_key]:
        if candidate and len(candidate) >= 3:
            slug = candidate.split("(")[0].strip().replace(" ", "_")
            w_thumb = _fetch_page_thumb_by_slug(slug, clean_attire, norm_country, "clothing", excluded, gender=gender)
            if w_thumb and w_thumb not in excluded:
                return w_thumb

    # 3. Dynamic search on Commons with country-specific queries including subject, garment, and clothing category
    queries = []
    garment_keys = [k for k in [core_clean, core_name] if k and len(k) >= 3]
    if local_key and "/" in local_key:
        garment_keys.extend([p.strip() for p in local_key.split("/") if len(p.strip()) >= 3])
    elif local_key and len(local_key) >= 3:
        garment_keys.append(local_key.strip())

    for gk in garment_keys:
        if is_women:
            queries.extend([
                f"{norm_country} {gk} traditional dress adult woman",
                f"{norm_country} adult woman {gk} traditional dress",
                f"{gk} {norm_country} traditional attire adult female",
                f"{norm_country} {gk} traditional dress woman",
                f"{gk} {norm_country} women traditional wear",
                f"{norm_country} female traditional clothing {gk}"
            ])
        elif is_men:
            queries.extend([
                f"{norm_country} {gk} traditional clothing adult man",
                f"{norm_country} adult man {gk} traditional attire",
                f"{gk} {norm_country} traditional attire adult male",
                f"{norm_country} {gk} traditional clothing man",
                f"{gk} {norm_country} men traditional wear",
                f"{norm_country} male traditional clothing {gk}"
            ])
        else:
            queries.extend([
                f"{norm_country} {gk} traditional attire adult",
                f"{gk} {norm_country} traditional clothing",
                f"{norm_country} {gk} traditional costume"
            ])

    # De-duplicate queries preserving order
    seen_q = set()
    dedup_queries = []
    for q in queries:
        q_clean = " ".join(q.split())
        if q_clean not in seen_q:
            seen_q.add(q_clean)
            dedup_queries.append(q_clean)

    for q in dedup_queries:
        img = _search_commons_image(q, core_clean or clean_attire, norm_country, "clothing", excluded, gender=gender)
        if img and is_valid_attire_image(q, "", img, clean_attire, norm_country, gender=gender):
            return img

    # CRITICAL: NO AI FALLBACK. If unverified, return None to display 'Authentic adult attire photo unavailable'.
    return None


@st.cache_data(ttl=604800, show_spinner=False)
def wikipedia_card(title, country="", card_type="place", location="", exclude_images=(), slug="", gender="unisex"):
    """
    Backwards-compatible gateway fetching verified image and description.
    Strictly separates:
    - card_type == 'food' -> get_food_image
    - card_type in ('clothing', 'attire', 'dress') -> get_attire_image
    - card_type in ('place', 'religious', 'culture') -> get_place_image
    """
    clean_title = str(title or "").strip()
    norm_country = normalize_country_name(country) if country else ""
    best_description = f"Explore {clean_title}" + (f" in {norm_country}." if norm_country else ".")

    if card_type == "food":
        image_url = get_food_image(clean_title, norm_country, slug=slug, exclude_images=exclude_images)
    elif card_type in ("clothing", "attire", "dress"):
        image_url = get_attire_image(clean_title, norm_country, gender=gender, exclude_images=exclude_images)
    else:
        image_url = get_place_image(clean_title, norm_country, location=location, slug=slug, exclude_images=exclude_images)

    # Fetch Wikipedia description if slug or title exists
    target_slug = slug or clean_title.replace(" ", "_")
    desc = best_description
    page_url = ""
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "titles": target_slug,
                "prop": "extracts|info",
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url",
                "redirects": 1
            },
            headers=WIKI_HEADERS,
            timeout=5
        )
        if r.status_code == 200:
            pages = r.json().get("query", {}).get("pages", {})
            for p in pages.values():
                if p.get("pageid", -1) != -1:
                    raw_ext = p.get("extract", "").replace("\n", " ").strip()
                    if raw_ext:
                        desc = raw_ext[:187] + "..." if len(raw_ext) > 190 else raw_ext
                    page_url = p.get("fullurl", "")
    except Exception:
        pass

    return {
        "image": image_url,
        "description": desc,
        "url": page_url or (f"https://en.wikipedia.org/wiki/{target_slug}" if target_slug else "")
    }




# ============================================================
# GENERIC WIKIPEDIA SEARCH HELPER
# ============================================================

@st.cache_data(ttl=604800, show_spinner=False)
def search_wikipedia_items(country_name, query_text, excluded_prefixes=None):
    excluded_prefixes = excluded_prefixes or []
    results = []
    seen = set()

    try:
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": query_text,
                "gsrnamespace": 0,
                "gsrlimit": 12,
                "prop": "extracts|pageimages|info",
                "piprop": "thumbnail",
                "pithumbsize": 700,
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url"
            },
            headers=WIKI_HEADERS,
            timeout=10
        )
        if response.status_code != 200:
            return []
        pages = response.json().get("query", {}).get("pages", {})
        for page in pages.values():
            name = str(page.get("title", "")).strip()
            if not name:
                continue
            lowered = name.lower()
            if any(lowered.startswith(prefix.lower()) for prefix in excluded_prefixes):
                continue
            if lowered in seen:
                continue
            seen.add(lowered)
            description = (page.get("extract") or "").replace("\n", " ").strip()
            if len(description) > 190:
                description = description[:187] + "..."
            results.append({
                "name": name,
                "location": country_name,
                "description": description
            })
            if len(results) >= 8:
                break
    except Exception:
        return []
    return results


# ============================================================
# LIVE TOURIST PLACES FALLBACK
# ============================================================

@st.cache_data(
    ttl=604800,
    show_spinner=False
)
def get_live_tourist_places(
    country_name
):

    alpha2 = get_country_alpha2(
        country_name
    )

    if not alpha2:
        return []

    queries = [
        f"tourist attraction, {country_name}",
        f"famous landmark, {country_name}",
        f"museum, {country_name}",
        f"historic site, {country_name}"
    ]

    results = []
    seen = set()

    for query in queries:

        try:

            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": query,
                    "format": "json",
                    "addressdetails": 1,
                    "limit": 8,
                    "countrycodes": alpha2.lower(),
                    "accept-language": "en"
                },
                headers={
                    "User-Agent":
                        "AI-Based-Personalized-Travel-Planner/1.0"
                },
                timeout=10
            )

            if response.status_code != 200:
                continue

            data = response.json()

            for item in data:

                name = item.get(
                    "name"
                )

                if not name:
                    continue

                key = name.lower()

                if key in seen:
                    continue

                seen.add(key)

                address = item.get(
                    "address",
                    {}
                )

                city = (
                    address.get("city")
                    or address.get("town")
                    or address.get("village")
                    or address.get("municipality")
                    or address.get("state")
                    or country_name
                )

                results.append({
                    "name": name,
                    "location": city
                })

                if len(results) >= 6:
                    return results

        except Exception:
            continue

    return results[:6]


# ============================================================
# TOURIST PLACE CARDS
# ============================================================

@st.cache_data(ttl=604800, show_spinner=False)
def get_tourist_cards(country_name):
    country = normalize_country_name(country_name)
    basic_places = []
    existing = set()

    # 1. Universal dynamic knowledge engine (curated + synthesized for all 250 countries)
    try:
        for att in get_attractions(country):
            name = str(att.get("name", "")).strip()
            slug = str(att.get("slug", "")).strip()
            if name and name.casefold() not in existing:
                basic_places.append({
                    "name": name,
                    "location": att.get("location") or country,
                    "slug": slug
                })
                existing.add(name.casefold())
    except Exception:
        pass

    for item in TOURIST_PLACES.get(country, []):
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            name = str(item[0]).strip()
            slug = item[2] if len(item) > 2 else ""
            if name and name.casefold() not in existing:
                basic_places.append({"name": name, "location": str(item[1]), "slug": slug})
                existing.add(name.casefold())

    if len(basic_places) < 6:
        dynamic_places = search_wikipedia_items(
            country,
            f"tourist attractions landmarks places to visit {country}",
            ["list of", "cuisine", "airport", "disambiguation"]
        )
        for item in dynamic_places:
            name = str(item.get("name", "")).strip()
            if not name or name.casefold() in existing:
                continue
            basic_places.append({"name": name, "location": item.get("location") or country, "slug": ""})
            existing.add(name.casefold())
            if len(basic_places) >= 6:
                break

    if len(basic_places) < 6:
        for item in get_live_tourist_places(country):
            name = str(item.get("name", "")).strip()
            if not name or name.casefold() in existing:
                continue
            basic_places.append({"name": name, "location": item.get("location") or country, "slug": ""})
            existing.add(name.casefold())
            if len(basic_places) >= 6:
                break

    # Last-resort country-specific entries keep the section populated even
    # when external place-search services are unavailable.
    if len(basic_places) < 5:
        profile = get_country_profile(country)
        fallback_places = [
            (f"Capital highlights of {country}", profile.get("capital", country)),
            (f"National Museum of {country}", profile.get("capital", country)),
            (f"Historic centre of {country}", country),
            (f"Natural attractions of {country}", country),
            (f"Cultural landmarks of {country}", country),
        ]
        for name, location in fallback_places:
            if name.casefold() in existing:
                continue
            basic_places.append({"name": name, "location": location, "slug": ""})
            existing.add(name.casefold())
            if len(basic_places) >= 6:
                break

    cards = []
    seen_images = set()
    for place in basic_places[:16]:
        name = place["name"]
        loc = place.get("location", country)
        slug = place.get("slug", "")
        wiki = wikipedia_card(name, country, "place", location=loc, slug=slug, exclude_images=tuple(seen_images))
        img = wiki.get("image")
        if img:
            seen_images.add(img)
        cards.append({
            "name": name,
            "location": loc,
            "image": img,
            "slug": slug,
            "description": wiki.get("description") or f"Explore {name} in {country}."
        })
    return cards




# ============================================================
# FOOD CARDS
# ============================================================

@st.cache_data(ttl=604800, show_spinner=False)
def get_food_cards(country_name, city=None):
    country = normalize_country_name(country_name)
    if not city and "," in str(country_name):
        parts = [p.strip() for p in str(country_name).split(",", 1)]
        city = parts[0]
        country = normalize_country_name(parts[1])

    cards = []
    seen = set()

    # 1. Primary: Grounded Destination & City food engine (destination_knowledge / country_data)
    try:
        raw_dishes = get_food(country, city=city)
        for d in raw_dishes:
            d_name = str(d.get("name", "")).strip()
            if not d_name or d_name.casefold() in seen:
                continue
            seen.add(d_name.casefold())
            cards.append({
                "name": d_name,
                "local_name": d.get("local_name", ""),
                "city": d.get("city", city or ""),
                "country": country,
                "description": d.get("description", ""),
                "ingredients": d.get("ingredients", ""),
                "preparation": d.get("preparation", ""),
                "taste_profile": d.get("taste_profile", ""),
                "dietary_type": d.get("dietary_type", ""),
                "is_vegetarian": d.get("is_vegetarian", False),
                "is_vegan": d.get("is_vegan", False),
                "contains_meat": d.get("contains_meat", False),
                "contains_seafood": d.get("contains_seafood", False),
                "is_halal": d.get("is_halal", True),
                "allergens": d.get("allergens", ""),
                "where_to_try": d.get("where_to_try") or get_where_to_try(country, d_name),
                "price_range": d.get("price_range", ""),
                "image": d.get("image"),
                "image_source": d.get("image_source", ""),
                "slug": d.get("slug", "")
            })
    except Exception:
        pass

    # 2. Curated Authentic Food Database (FOOD_DATA)
    if len(cards) < 6:
        for item in FOOD_DATA.get(country, []):
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                name = str(item[0]).strip()
                if name and name.casefold() not in seen:
                    seen.add(name.casefold())
                    s = item[2] if len(item) > 2 else ""
                    cards.append({
                        "name": name,
                        "description": str(item[1]).strip(),
                        "slug": s,
                        "country": country,
                        "city": city or "",
                        "image": None,
                        "where_to_try": get_where_to_try(country, name)
                    })

    # 3. Country-Specific Curated Fallbacks (FALLBACK_FOOD_DATA)
    if len(cards) < 6:
        for item in FALLBACK_FOOD_DATA.get(country, []):
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                name = str(item[0]).strip()
                if name and name.casefold() not in seen:
                    seen.add(name.casefold())
                    s = item[2] if len(item) > 2 else ""
                    cards.append({
                        "name": name,
                        "description": str(item[1]).strip(),
                        "slug": s,
                        "country": country,
                        "city": city or "",
                        "image": None,
                        "where_to_try": get_where_to_try(country, name)
                    })
            elif isinstance(item, dict):
                name = str(item.get("name", "")).strip()
                if name and name.casefold() not in seen:
                    seen.add(name.casefold())
                    cards.append({
                        "name": name,
                        "description": str(item.get("description", "")).strip(),
                        "slug": str(item.get("slug", "")).strip(),
                        "country": country,
                        "city": city or "",
                        "image": item.get("image"),
                        "where_to_try": item.get("where_to_try") or get_where_to_try(country, name)
                    })

    # 4. Resolve Wikipedia images for items missing images
    seen_images = {c["image"] for c in cards if c.get("image")}
    for c in cards:
        if not c.get("image"):
            wiki = wikipedia_card(c["name"], country, "food", slug=c.get("slug", ""), exclude_images=tuple(seen_images))
            if wiki.get("image"):
                c["image"] = wiki["image"]
                seen_images.add(wiki["image"])
            if not c.get("description") and wiki.get("description"):
                c["description"] = wiki["description"]

    # 5. Fallback for unrecognized countries
    if len(cards) < 5:
        for name, description in make_generic_food_fallback(country):
            if name.casefold() not in seen:
                seen.add(name.casefold())
                cards.append({
                    "name": name,
                    "image": None,
                    "description": description,
                    "country": country,
                    "where_to_try": get_where_to_try(country, name)
                })
            if len(cards) >= 5:
                break

    return cards[:8]


# ============================================================
# RELIGIOUS PLACE CARDS
# ============================================================

@st.cache_data(ttl=604800, show_spinner=False)
def get_live_religious_places(country_name):
    alpha2 = get_country_alpha2(country_name)
    if not alpha2:
        return []

    queries = [
        f"temple, {country_name}", f"shrine, {country_name}",
        f"church, {country_name}", f"mosque, {country_name}",
        f"monastery, {country_name}"
    ]
    results, seen = [], set()

    for query in queries:
        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": query, "format": "json", "addressdetails": 1,
                    "limit": 5, "countrycodes": alpha2.lower(),
                    "accept-language": "en"
                },
                headers={"User-Agent": "AI-Based-Personalized-Travel-Planner/1.0"},
                timeout=10
            )
            if response.status_code != 200:
                continue
            for item in response.json():
                name = str(item.get("name") or "").strip()
                if not name or name.casefold() in seen:
                    continue
                seen.add(name.casefold())
                address = item.get("address", {})
                city = (address.get("city") or address.get("town") or
                        address.get("village") or address.get("state") or country_name)
                results.append({"name": name, "location": city})
                if len(results) >= 6:
                    return results
        except Exception:
            continue
    return results[:6]


@st.cache_data(ttl=604800, show_spinner=False)
def get_religious_cards(country_name):
    country = normalize_country_name(country_name)
    places = []
    existing = set()

    # 1. Universal dynamic knowledge engine
    try:
        for c in get_culture(country):
            name = str(c.get("name", "")).strip()
            slug = str(c.get("slug", "")).strip()
            if name and name.casefold() not in existing:
                places.append({
                    "name": name,
                    "location": c.get("location") or country,
                    "description": c.get("description", ""),
                    "slug": slug
                })
                existing.add(name.casefold())
    except Exception:
        pass

    for item in RELIGIOUS_PLACES.get(country, []):
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            name = str(item[0]).strip()
            slug = item[2] if len(item) > 2 else ""
            if name and name.casefold() not in existing:
                places.append({"name": name, "location": str(item[1]), "slug": slug})
                existing.add(name.casefold())

    if len(places) < 5:
        for item in get_live_religious_places(country):
            name = str(item.get("name", "")).strip()
            if not name or name.casefold() in existing:
                continue
            places.append({"name": name, "location": item.get("location") or country, "slug": ""})
            existing.add(name.casefold())
            if len(places) >= 5:
                break

    if len(places) < 6:
        dynamic_places = search_wikipedia_items(
            country,
            f"temple shrine church mosque monastery cathedral religious cultural site {country}",
            ["list of", "religion in", "religions of"]
        )
        for item in dynamic_places:
            name = str(item.get("name", "")).strip()
            if not name or name.casefold() in existing:
                continue
            places.append({"name": name, "location": country, "slug": ""})
            existing.add(name.casefold())
            if len(places) >= 6:
                break

    if len(places) < 5:
        fallback_places = [
            (f"Historic religious sites of {country}", country),
            (f"Major cultural shrine of {country}", country),
            (f"Historic place of worship in {country}", country),
            (f"Heritage sacred site of {country}", country),
            (f"Traditional spiritual site of {country}", country),
        ]
        for name, location in fallback_places:
            if name.casefold() in existing:
                continue
            places.append({"name": name, "location": location, "slug": ""})
            existing.add(name.casefold())
            if len(places) >= 6:
                break

    cards = []
    seen_rel_images = set()
    for place in places[:6]:
        slug = place.get("slug", "")
        wiki = wikipedia_card(place["name"], country, "religious", slug=slug, exclude_images=tuple(seen_rel_images))
        img = wiki.get("image")
        if img:
            seen_rel_images.add(img)
        cards.append({
            "name": place["name"],
            "location": place.get("location", country),
            "image": img,
            "slug": slug,
            "description": wiki.get("description") or
                           f"A notable religious or cultural site associated with {country}."
        })
    return cards


# ============================================================
# DYNAMIC PLANNER REGISTRATION
# ============================================================

def register_country_for_planner(
    country_name,
    profile,
    tourist_cards,
    food_cards
):

    # Never replace your original detailed planner data.
    if country_name in COUNTRIES:
        return

    places = [
        card["name"]
        for card in tourist_cards
    ]

    if not places:

        places = [
            country_name
        ]

    activities = {}

    for index, place in enumerate(places):
        activities[place] = [
            ("09:00", f"Morning sightseeing & exploration of {place}", place, 600, 25),
            ("14:00", f"Visit cultural landmarks & viewpoints in {place}", place, 800, 30),
            ("19:00", f"Authentic dinner and evening atmosphere in {place}", place, 1100, 20)
        ]

    COUNTRIES[country_name] = {

        "flag": profile["flag"],

        "duration": profile[
            "duration"
        ],

        "budget": profile[
            "budget"
        ],

        "season": profile[
            "season"
        ],

        "places": places,

        "food": [
            item["name"]
            for item in food_cards
        ],

        "transport": [
            "Local transport",
            "Trains",
            "Buses",
            "Flights"
        ],

        "experiences": places[:4],

        "activities": activities
    }


# ============================================================
# GLOBE
# ============================================================

def create_globe(
    selected_country
):

    selected_code = get_country_code(
        selected_country
    )

    locations = GLOBE_LOCATIONS
    display_names = GLOBE_DISPLAY_NAMES

    # --------------------------------------------------------
    # Give different countries different colors
    # --------------------------------------------------------

    color_values = []

    for index, code in enumerate(
        locations
    ):

        color_values.append(
            index % 8
        )

    fig = go.Figure()

    # --------------------------------------------------------
    # Colorful base globe
    # --------------------------------------------------------

    fig.add_trace(
        go.Choropleth(
            locations=locations,

            z=color_values,

            locationmode="ISO-3",

            text=display_names,

            customdata=display_names,

            colorscale=[
                [0.00, "#16A085"],
                [0.125, "#27AE60"],
                [0.25, "#F1C40F"],
                [0.375, "#F39C12"],
                [0.50, "#E67E22"],
                [0.625, "#3498DB"],
                [0.75, "#5B5FEF"],
                [0.875, "#8E44AD"],
                [1.00, "#16A085"]
            ],

            showscale=False,

            marker_line_color="#E5F6FF",

            marker_line_width=0.65,

            selected=dict(marker=dict(opacity=1.0)),
            unselected=dict(marker=dict(opacity=1.0)),

            hovertemplate=(
                "<b>%{customdata}</b>"
                "<br>Click to select"
                "<extra></extra>"
            ),

            hoverlabel=dict(
                bgcolor="#FFD54F",
                bordercolor="#FFFFFF",
                font=dict(
                    color="#111827",
                    size=14
                )
            )
        )
    )

    # --------------------------------------------------------
    # Interactive Country Centroid Markers (Scattergeo)
    # Allows clicking any country pin directly on the 3D globe
    # --------------------------------------------------------

    fig.add_trace(
        go.Scattergeo(
            lat=GLOBE_MARKER_LATS,
            lon=GLOBE_MARKER_LONS,
            text=GLOBE_MARKER_NAMES,
            customdata=GLOBE_MARKER_NAMES,
            mode="markers",
            marker=dict(
                size=7,
                color="#FFD700",
                opacity=0.85,
                symbol="circle",
                line=dict(width=0.8, color="#FFFFFF")
            ),
            hovertemplate="<b>%{customdata}</b><br>👉 Click to select destination<extra></extra>",
            hoverlabel=dict(
                bgcolor="#FFD700",
                bordercolor="#FFFFFF",
                font=dict(
                    color="#111827",
                    size=14
                )
            ),
            selected=dict(marker=dict(opacity=1.0)),
            unselected=dict(marker=dict(opacity=0.85)),
            name="Destinations"
        )
    )

    # --------------------------------------------------------
    # Sovereign Territory Representation: Jammu, Kashmir & Ladakh (India)
    # Correctly represents northern Indian territory with proper geographical boundaries
    # --------------------------------------------------------
    is_india = (str(selected_country).strip().lower() == "india")
    jk_lats = [
        32.20, 32.45, 32.75, 33.20, 33.65, 34.10, 34.50, 35.10, 35.60, 36.20,
        36.70, 37.10, 36.85, 36.20, 35.70, 35.20, 34.50, 33.80, 33.20, 32.60,
        32.20
    ]
    jk_lons = [
        74.80, 74.40, 74.00, 73.80, 74.00, 74.50, 75.00, 75.50, 76.20, 77.00,
        77.60, 78.40, 79.30, 79.80, 79.50, 79.00, 78.40, 77.80, 76.80, 75.80,
        74.80
    ]
    jk_fill = "rgba(255, 215, 0, 0.9)" if is_india else "rgba(39, 174, 96, 0.75)"
    jk_line = "#FFF7AE" if is_india else "#E5F6FF"

    fig.add_trace(
        go.Scattergeo(
            lat=jk_lats,
            lon=jk_lons,
            mode="lines",
            fill="toself",
            fillcolor=jk_fill,
            line=dict(color=jk_line, width=1.8 if is_india else 1.0),
            text=["Jammu & Kashmir & Ladakh, India"] * len(jk_lats),
            customdata=["India"] * len(jk_lats),
            name="Jammu & Kashmir (India)",
            hoverinfo="text",
            hovertemplate="<b>Jammu & Kashmir & Ladakh (India)</b><br>👉 Click to select India<extra></extra>"
        )
    )

    # City markers in Jammu, Kashmir & Ladakh
    jk_city_lats = [34.0837, 32.7266, 34.1526, 34.0484, 34.5539]
    jk_city_lons = [74.7973, 74.8570, 77.5771, 74.3805, 76.1349]
    jk_city_names = ["Srinagar", "Jammu", "Leh", "Gulmarg", "Kargil"]
    fig.add_trace(
        go.Scattergeo(
            lat=jk_city_lats,
            lon=jk_city_lons,
            mode="markers+text",
            text=jk_city_names,
            textposition="top right",
            textfont=dict(size=10, color="#FFFFFF"),
            marker=dict(size=6, color="#FF9933", symbol="diamond", line=dict(width=1, color="#FFFFFF")),
            customdata=["India"] * len(jk_city_lats),
            hoverinfo="text",
            hovertemplate="<b>%{text}, Jammu & Kashmir (India)</b><br>👉 Click to select India<extra></extra>",
            name="J&K Cities"
        )
    )


    # --------------------------------------------------------
    # Selected country overlay
    # --------------------------------------------------------

    if selected_code:

        fig.add_trace(
            go.Choropleth(
                locations=[
                    selected_code
                ],

                z=[1],

                locationmode="ISO-3",

                text=[
                    selected_country
                ],

                customdata=[
                    selected_country
                ],

                colorscale=[
                    [0, "#FFD700"],
                    [1, "#FFB300"]
                ],

                showscale=False,

                marker_line_color="#FFF7AE",

                marker_line_width=2.8,

                selected=dict(marker=dict(opacity=1.0)),
                unselected=dict(marker=dict(opacity=1.0)),

                hoverinfo="skip"
            )
        )

    # Glowing pin marker on selected destination
    lon, lat = get_country_center(selected_country)

    fig.add_trace(
        go.Scattergeo(
            lat=[lat],
            lon=[lon],
            text=[selected_country],
            customdata=[selected_country],
            mode="markers+text",
            textposition="top center",
            textfont=dict(size=14, color="#FFD700", family="sans-serif"),
            marker=dict(
                size=16,
                color="#FF4B4B",
                symbol="star",
                line=dict(width=2, color="#FFFFFF")
            ),
            hovertemplate="<b>%{customdata}</b><br>★ Selected destination<extra></extra>",
            selected=dict(marker=dict(opacity=1.0)),
            unselected=dict(marker=dict(opacity=1.0)),
            name="Selected"
        )
    )

    # --------------------------------------------------------
    # Globe appearance
    # --------------------------------------------------------

    fig.update_geos(

        projection_type="orthographic",

        showcoastlines=True,

        coastlinecolor="#BDEBFF",

        coastlinewidth=1.2,

        showland=True,

        landcolor="#173B45",

        showocean=True,

        oceancolor="#061A2B",

        showlakes=True,

        lakecolor="#0B4057",

        showcountries=True,

        countrycolor="#D9F7FF",

        countrywidth=0.7,

        bgcolor="rgba(0,0,0,0)",

        projection_rotation=dict(
            lon=lon,
            lat=lat
        ),
        projection_scale=1.08
    )

    # --------------------------------------------------------
    # Premium dark-space background
    # --------------------------------------------------------

    fig.update_layout(

        height=680,

        margin={
            "l": 0,
            "r": 0,
            "t": 0,
            "b": 0
        },

        paper_bgcolor="#020817",

        plot_bgcolor="#020817",

        clickmode="event+select",

        showlegend=False,

        font=dict(
            color="#F8FAFC"
        )
    )

    return fig


# ============================================================
# COUNTRY CARD
# ============================================================

def show_information_card(
    label,
    value,
    icon
):

    with st.container():

        st.markdown(
            f"**{icon} {label}**"
        )

        if not value:
            value = "Information unavailable"

        st.write(
            value
        )


# ============================================================
# RELIABLE IMAGE RESOLUTION + CARD RENDERING
# ============================================================

@st.cache_data(ttl=604800, show_spinner=False)
def get_verified_image_url(title, country, card_type):
    """Find a real Wikimedia/Wikipedia image relevant to the actual item."""
    title = str(title or "").strip()
    country = normalize_country_name(country)
    if not title:
        return None

    # First choice: the actual item's Wikipedia image.
    try:
        image = wikipedia_card(title, country).get("image")
        if image:
            return image
    except Exception:
        pass

    category_terms = {
        "food": "traditional food dish cuisine",
        "place": "tourist landmark attraction travel",
        "religious": "temple shrine church mosque monastery religious heritage"
    }
    queries = [
        f"{title} {country}",
        f"{title} {category_terms.get(card_type, 'travel')} {country}",
        f"{category_terms.get(card_type, 'travel')} {country}"
    ]

    for query in queries:
        try:
            response = requests.get(
                "https://commons.wikimedia.org/w/api.php",
                params={
                    "action": "query", "format": "json",
                    "generator": "search", "gsrsearch": query,
                    "gsrnamespace": 6, "gsrlimit": 10,
                    "prop": "imageinfo", "iiprop": "url",
                    "iiurlwidth": 1000
                },
                timeout=10
            )
            if response.status_code != 200:
                continue
            pages = response.json().get("query", {}).get("pages", {})
            for page in pages.values():
                info = page.get("imageinfo", [])
                if not info:
                    continue
                image = info[0].get("thumburl") or info[0].get("url")
                if image:
                    return image
        except Exception:
            continue

    return None


@st.cache_data(ttl=604800, show_spinner=False)
def get_image_bytes(url):
    """Download and validate an image so the browser never receives a bad URL."""
    if not url:
        return None
    try:
        response = requests.get(
            url,
            timeout=15,
            headers=WIKI_HEADERS
        )
        content_type = response.headers.get("content-type", "").lower()
        if response.status_code == 200 and response.content and (
            content_type.startswith("image/") or response.content[:8].startswith(b"\x89PNG")
        ):
            return response.content
    except Exception:
        return None
    return None


@st.cache_data(ttl=604800, show_spinner=False)
def resolve_card_image_url(country, item_name, card_type="place", candidate_image=None, location=None, slug=None, exclude_images=(), gender="unisex"):
    """
    Finds a verified, authentic image URL matching the exact food dish or tourist landmark.
    Enforces strict anti-repetition: any URL in exclude_images is automatically rejected.
    """
    country = normalize_country_name(country)
    item_name = str(item_name or "").strip()
    slug = str(slug or "").strip()
    loc_str = str(location or "").strip() if location and str(location).strip().lower() != country.lower() else ""
    excluded = set(exclude_images) if exclude_images else set()

    # 1. Candidate image if provided and not excluded
    if candidate_image and candidate_image not in excluded:
        if card_type == "food":
            if is_valid_food_image(item_name, "", candidate_image, item_name, country):
                return candidate_image
        elif card_type in ("clothing", "attire", "dress"):
            if is_valid_attire_image(item_name, "", candidate_image, item_name, country, gender=gender):
                return candidate_image
        else:
            if is_valid_place_image(item_name, "", candidate_image, item_name, country):
                return candidate_image

    # 2. Strict pipeline delegation
    if card_type == "food":
        return get_food_image(item_name, country, slug=slug, exclude_images=tuple(excluded))
    elif card_type in ("clothing", "attire", "dress"):
        return get_attire_image(item_name, country, gender=gender, exclude_images=tuple(excluded))
    else:
        return get_place_image(item_name, country, location=loc_str, slug=slug, exclude_images=tuple(excluded))


def get_card_image_bytes(country, item_name, card_type="place", candidate_image=None, location=None, slug=None, exclude_images=(), gender="unisex"):
    url = resolve_card_image_url(
        country, item_name, card_type=card_type,
        candidate_image=candidate_image, location=location, slug=slug,
        exclude_images=tuple(exclude_images or ()), gender=gender
    )
    if url:
        return get_image_bytes(url), url
    return None, None


def show_image_card(card, card_type="place"):
    """Render attractive photo cards with Streamlit components and strict anti-repetition."""
    raw_name = str(card.get("name", "Untitled")).strip()
    raw_location = str(card.get("location", "")).strip()
    raw_description = str(card.get("description", "")).strip()
    slug = str(card.get("slug", "")).strip()
    country = normalize_country_name(card.get("country") or st.session_state.get("selected_country", ""))

    used_registry = st.session_state.setdefault("used_destination_image_urls", set())
    candidate_image = card.get("image")
    if candidate_image in used_registry:
        candidate_image = None

    image_bytes, chosen_url = get_card_image_bytes(
        country, raw_name, card_type,
        candidate_image=candidate_image, location=raw_location, slug=slug,
        exclude_images=tuple(used_registry)
    )
    if chosen_url:
        used_registry.add(chosen_url)

    with st.container(border=True):
        if card_type == "food" and not image_bytes:
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.75); border: 1px dashed rgba(245, 158, 11, 0.5); border-radius: 12px; padding: 32px 16px; text-align: center; margin-bottom: 12px;">
                    <div style="font-size: 32px; margin-bottom: 8px;">🍲</div>
                    <div style="font-weight: 700; color: #f59e0b; font-size: 14px; letter-spacing: 0.5px;">Verified Photo Unavailable</div>
                    <div style="color: #94a3b8; font-size: 12px; margin-top: 4px;">Showing only authentic, verified photographs of the cooked dish for {country}.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif not image_bytes and card_type in ("place", "religious", "culture"):
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.75); border: 1px dashed rgba(56, 189, 248, 0.5); border-radius: 12px; padding: 32px 16px; text-align: center; margin-bottom: 12px;">
                    <div style="font-size: 32px; margin-bottom: 8px;">🏛️</div>
                    <div style="font-weight: 700; color: #38bdf8; font-size: 14px; letter-spacing: 0.5px;">Verified Image Unavailable</div>
                    <div style="color: #94a3b8; font-size: 12px; margin-top: 4px;">Only authentic photographs of the actual location/landmark are displayed for {country}.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif image_bytes:
            st.image(image_bytes, width="stretch")

        st.markdown(f"### {raw_name}")

        if card_type == "food":
            city_val = card.get("city")
            loc_label = f"📍 {city_val}, {country}" if city_val and city_val != country else f"📍 {country}"
            st.caption(loc_label)
            if card.get("local_name"):
                st.markdown(f"**Native Script / Local Name:** `{card['local_name']}`")
            st.write(raw_description or f"Authentic culinary specialty of {loc_label}.")

            # Dietary Badges
            badges = []
            if card.get("is_vegan"):
                badges.append("🌿 Vegan")
            elif card.get("is_vegetarian"):
                badges.append("🌱 Vegetarian")
            elif card.get("contains_seafood"):
                badges.append("🦐 Seafood")
            elif card.get("contains_meat"):
                badges.append("🥩 Contains Meat")

            if card.get("is_halal"):
                badges.append("☪️ Halal-friendly")

            if badges:
                badge_html = " ".join([
                    f"<span style='background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.35); border-radius: 9999px; padding: 2px 8px; font-size: 11px; font-weight: 700;'>{b}</span>"
                    for b in badges
                ])
                st.markdown(badge_html, unsafe_allow_html=True)

            if card.get("taste_profile"):
                st.markdown(f"**👅 Taste Profile:** {card['taste_profile']}")

            if card.get("allergens"):
                st.markdown(f"**⚠️ Common Allergens:** {card['allergens']}")

            where_to_try = card.get("where_to_try") or get_where_to_try(country, raw_name)
            st.markdown(f"**🍽️ Best places to try:** {where_to_try}")

            if card.get("price_range"):
                st.markdown(f"**💰 Estimated Price:** `{card['price_range']}` *(estimate)*")

            if card.get("ingredients") or card.get("preparation"):
                with st.expander("🍲 Ingredients & Preparation"):
                    if card.get("ingredients"):
                        st.markdown(f"**Key Ingredients:** {card['ingredients']}")
                    if card.get("preparation"):
                        st.markdown(f"**Preparation:** {card['preparation']}")

            if card.get("image_source"):
                st.caption(f"📷 Photo: {card['image_source']}")

        elif card_type in ("religious", "culture"):
            if raw_location:
                st.caption(f"📍 {raw_location}, {country}")
            else:
                st.caption(f"📍 {country}")
            st.write(raw_description or f"Cultural and spiritual heritage of {country}.")
            with st.expander("🕊️ Cultural Significance & Etiquette"):
                st.markdown(f"**✨ Significance:** {card.get('significance') or f'A celebrated cultural and spiritual site reflecting the deep heritage of {country}.'}")
                st.markdown(f"**🙏 Etiquette:** {card.get('etiquette') or 'Dress respectfully with shoulders and knees covered, remove footwear before entering sanctums, and ask before taking photography.'}")

        else:
            # Place / Landmark card
            if raw_location:
                st.caption(f"📍 {raw_location}")
            else:
                st.caption(f"📍 {country}")
            st.write(raw_description or f"Explore {raw_name} in {country}.")
            with st.expander("🔍 Explore Details"):
                st.markdown(f"**✨ Highlights:** {card.get('highlights') or f'Iconic sightseeing destination and photography spot in {raw_location or country}.'}")
                st.markdown(f"**🕒 Best Time:** {card.get('best_time') or 'Morning / Early Afternoon (optimal lighting and fewer crowds)'}")
                st.markdown(f"**💡 Traveler Tip:** {card.get('tip') or f'Arrive early to avoid queues and experience the authentic atmosphere of {raw_name}.'}")

        st.write("")
        btn_c1, btn_c2 = st.columns(2)
        is_saved = is_place_saved(raw_name, country)
        safe_hash = abs(hash(f"{card_type}_{country}_{raw_name}")) % 1000000
        with btn_c1:
            save_label = "🔖 Saved" if is_saved else "🔖 Save Place"
            if st.button(save_label, key=f"card_save_{safe_hash}", type="primary" if is_saved else "secondary", width="stretch"):
                toggle_save_place({
                    "name": raw_name,
                    "country": country,
                    "type": card_type,
                    "location": raw_location or country,
                    "description": raw_description
                })
                st.rerun()
        with btn_c2:
            if st.button("➕ Add to Trip", key=f"card_itin_{safe_hash}", width="stretch"):
                if add_place_to_itinerary(raw_name, country, target_day=1):
                    st.success(f"Added {raw_name} to Day 1 of your trip!")
                else:
                    st.info("Please generate an itinerary first in Plan My Trip.")


def show_gallery_card(country, item):
    """Render an item in the Destination Photo Gallery with anti-duplicate registry."""
    name = item.get("name", "")
    caption = item.get("caption", f"Explore {name} in {country}")
    slug = item.get("slug", "")

    used_registry = st.session_state.setdefault("used_destination_image_urls", set())
    image_bytes, chosen_url = get_card_image_bytes(
        country, name, "place", location=name, slug=slug,
        exclude_images=tuple(used_registry)
    )
    if chosen_url:
        used_registry.add(chosen_url)

    with st.container(border=True):
        if image_bytes:
            st.image(image_bytes, width="stretch")
        else:
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.75); border: 1px dashed rgba(56, 189, 248, 0.5); border-radius: 12px; padding: 28px 14px; text-align: center; margin-bottom: 12px;">
                    <div style="font-size: 28px; margin-bottom: 6px;">📸</div>
                    <div style="font-weight: 700; color: #38bdf8; font-size: 13px;">Verified Image Unavailable</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown(f"**{name}**")
        st.caption(f"📍 {country} &bull; {caption}")



# ============================================================
# HELPER: DESTINATION SWITCH & ITINERARY REGENERATION
# ============================================================

def switch_country_and_regenerate(new_country):
    norm = normalize_country_name(new_country)
    if norm in countries and norm != st.session_state.selected_country:
        st.session_state.selected_country = norm
        st.session_state.globe_country = norm
        st.session_state["used_destination_image_urls"] = set()
        prof = get_country_profile(norm)
        tc = get_tourist_cards(norm)
        fc = get_food_cards(norm)
        register_country_for_planner(norm, prof, tc, fc)
        st.session_state.itinerary = generate_itinerary(
            st.session_state.get("starting_location", "Your Location"),
            norm,
            st.session_state.get("days", 7),
            st.session_state.get("travelers", 1),
            st.session_state.get("budget", 80000),
            st.session_state.get("interests", ["Culture", "Food"]),
            st.session_state.get("style", "Relaxed")
        )
        st.rerun()


# ============================================================
# APPLICATION FLOW: MULTI-PAGE NAVIGATION SYSTEM
# ============================================================

# Destination Language to Speech Voice Code Resolver
def get_destination_voice_code(dest_name: str) -> str:
    """Returns the ISO BCP-47 speech synthesis voice code for a destination country."""
    if not dest_name:
        return "en-US"
    norm = normalize_country_name(dest_name).lower()
    mapping = {
        "japan": "ja-JP",
        "india": "hi-IN",
        "france": "fr-FR",
        "italy": "it-IT",
        "spain": "es-ES",
        "germany": "de-DE",
        "thailand": "th-TH",
        "south korea": "ko-KR",
        "korea": "ko-KR",
        "china": "zh-CN",
        "nepal": "ne-NP",
        "russia": "ru-RU",
        "brazil": "pt-BR",
        "portugal": "pt-PT",
        "turkey": "tr-TR",
        "vietnam": "vi-VN",
        "indonesia": "id-ID",
        "greece": "el-GR",
        "egypt": "ar-EG",
        "israel": "he-IL",
        "netherlands": "nl-NL",
        "mexico": "es-MX",
        "united states": "en-US",
        "usa": "en-US",
        "united kingdom": "en-GB",
        "uk": "en-GB",
        "australia": "en-AU",
        "canada": "en-CA",
        "singapore": "en-SG",
        "malaysia": "ms-MY",
        "south africa": "en-ZA",
        "new zealand": "en-NZ",
    }
    for k, v in mapping.items():
        if k in norm:
            return v
    return "en-US"


# Shared Speech Controller
def render_assistant_speech_controller(msg_content, player_id, default_lang="en-US"):
    speech_match = re.search(r'<!-- SPEECH:([a-zA-Z\-]+):(.*?) -->', msg_content, re.DOTALL)
    if speech_match:
        voice_code = speech_match.group(1).strip()
        speech_text = speech_match.group(2).strip()
    else:
        voice_code = default_lang
        speech_text = re.sub(r'[*_#`\[\]]', '', msg_content)
        speech_text = re.sub(r'<!--.*?-->', '', speech_text, flags=re.DOTALL)
        speech_text = speech_text.replace("\n", " ").strip()
        if len(speech_text) > 280:
            speech_text = speech_text[:277] + "..."

    if not speech_text:
        return

    safe_text_json = json.dumps(speech_text)
    safe_voice_code = json.dumps(voice_code)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        background: transparent;
        overflow: hidden;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        user-select: none;
    }}
    .player-row {{
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        padding: 3px 0 5px 0;
    }}
    .btn-play {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%);
        color: #ffffff;
        border: none;
        border-radius: 18px;
        padding: 5px 14px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
        transition: all 0.15s ease;
    }}
    .btn-play:hover {{
        filter: brightness(1.1);
        transform: translateY(-1px);
    }}
    .btn-play:active {{
        transform: translateY(0);
    }}
    .btn-stop {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255, 255, 255, 0.06);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 18px;
        padding: 5px 11px;
        font-size: 11.5px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.15s ease;
    }}
    .btn-stop:hover {{
        background: rgba(255, 255, 255, 0.12);
        color: #ffffff;
    }}
    .voice-tag {{
        font-size: 11px;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.04);
        padding: 3px 8px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .status-span {{
        font-size: 11px;
        color: #94a3b8;
        font-style: italic;
    }}
    </style>
    </head>
    <body>
    <div class="player-row">
        <button id="btn_{player_id}" class="btn-play" onclick="playAudio_{player_id}()">
            🔊 Pronounce / Listen
        </button>
        <button id="stop_{player_id}" class="btn-stop" onclick="stopAudio_{player_id}()">
            ⏹️ Stop
        </button>
        <span class="voice-tag">
            🗣️ {voice_code}
        </span>
        <span id="status_{player_id}" class="status-span"></span>
    </div>
    <script>
    (function() {{
        // Remove unwanted st.iframe text and attributes from Streamlit iframe container
        function cleanIframe() {{
            try {{
                if (window.frameElement) {{
                    window.frameElement.removeAttribute('title');
                    window.frameElement.setAttribute('aria-label', 'Pronunciation player');
                    window.frameElement.style.border = 'none';
                    window.frameElement.style.outline = 'none';
                }}
                if (window.parent && window.parent.document) {{
                    var iframes = window.parent.document.querySelectorAll('iframe[title="st.iframe"]');
                    for (var i = 0; i < iframes.length; i++) {{
                        iframes[i].removeAttribute('title');
                        iframes[i].setAttribute('aria-label', 'Pronunciation player');
                        iframes[i].style.border = 'none';
                        iframes[i].style.outline = 'none';
                    }}
                }}
            }} catch(e) {{}}
        }}
        cleanIframe();
        setTimeout(cleanIframe, 150);
        setTimeout(cleanIframe, 600);

        var text = {safe_text_json};
        var targetLang = {safe_voice_code};
        var btn = document.getElementById("btn_{player_id}");
        var status = document.getElementById("status_{player_id}");

        function getSynth() {{
            if ('speechSynthesis' in window) return window.speechSynthesis;
            if (window.parent && 'speechSynthesis' in window.parent) return window.parent.speechSynthesis;
            return null;
        }}

        function getUtteranceClass() {{
            if ('SpeechSynthesisUtterance' in window) return window.SpeechSynthesisUtterance;
            if (window.parent && 'SpeechSynthesisUtterance' in window.parent) return window.parent.SpeechSynthesisUtterance;
            return null;
        }}

        var synth = getSynth();
        var cachedVoices = [];

        function findVoice() {{
            if (!synth) return null;
            cachedVoices = synth.getVoices() || [];
            if (!cachedVoices.length) return null;

            var tLang = targetLang.toLowerCase();
            var prefix = tLang.split(/[-_]/)[0];

            // 1. Exact match (e.g. ja-JP or ja_JP)
            var exact = cachedVoices.find(function(v) {{
                return v.lang && v.lang.replace('_', '-').toLowerCase() === tLang;
            }});
            if (exact) return exact;

            // 2. Prefix match (e.g. ja, ja-*)
            var pref = cachedVoices.find(function(v) {{
                return v.lang && v.lang.toLowerCase().startsWith(prefix);
            }});
            if (pref) return pref;

            // 3. Name match for Japanese voices
            if (prefix === 'ja') {{
                var jName = cachedVoices.find(function(v) {{
                    return v.name && /(japanese|japan|nihongo|kyoko|nanami|keita|ayumi|haruka|ichiro)/i.test(v.name);
                }});
                if (jName) return jName;
            }}

            return null;
        }}

        // Handle voices that load asynchronously
        if (synth) {{
            cachedVoices = synth.getVoices() || [];
            if (typeof synth.onvoiceschanged !== 'undefined') {{
                synth.onvoiceschanged = function() {{
                    cachedVoices = synth.getVoices() || [];
                }};
            }}
        }}

        window.playAudio_{player_id} = function() {{
            var s = getSynth();
            var UtterClass = getUtteranceClass();
            if (!s || !UtterClass) {{
                if (status) {{
                    status.innerText = "⚠️ Speech synthesis not supported in this browser.";
                    status.style.color = "#f87171";
                }}
                return;
            }}

            // Cancel previous speech before playing new phrase to prevent overlapping audio
            s.cancel();

            var utter = new UtterClass(text);
            utter.lang = targetLang;
            utter.rate = 0.92;

            var voice = findVoice();
            if (voice) {{
                utter.voice = voice;
            }}

            if (btn) btn.innerHTML = "🔊 Playing...";
            if (status) status.innerText = "";

            utter.onstart = function() {{
                if (btn) btn.innerHTML = "🔊 Playing...";
            }};

            utter.onend = function() {{
                if (btn) btn.innerHTML = "🔊 Replay";
            }};

            // If Japanese speech is unavailable or errors, show a clear message instead of silently doing nothing
            utter.onerror = function(ev) {{
                console.warn("Speech error:", ev);
                if (btn) btn.innerHTML = "🔊 Pronounce / Listen";
                if (status) {{
                    status.innerText = "⚠️ Playback unavailable for " + targetLang + " on this device.";
                    status.style.color = "#f59e0b";
                }}
            }};

            try {{
                s.speak(utter);
            }} catch(err) {{
                console.error("Speak error:", err);
                if (btn) btn.innerHTML = "🔊 Pronounce / Listen";
                if (status) {{
                    status.innerText = "⚠️ Playback failed: " + err.message;
                    status.style.color = "#f87171";
                }}
            }}
        }};

        window.stopAudio_{player_id} = function() {{
            var s = getSynth();
            if (s) {{
                s.cancel();
            }}
            if (btn) btn.innerHTML = "🔊 Pronounce / Listen";
            if (status) status.innerText = "";
        }};
    }})();
    </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=44, scrolling=False)



# Shared Speech Input (Microphone / Voice-to-Text) Controller
def render_speech_input_controller(player_id="voice_rec"):
    html_code = f"""
    <div style="display:flex; align-items:center; gap:8px; margin: 4px 0 10px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
        <button id="mic_btn_{player_id}" onclick="toggleSpeechRec_{player_id}()" style="display:inline-flex; align-items:center; gap:6px; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#ffffff; border:none; border-radius:18px; padding:6px 14px; font-size:12px; font-weight:700; cursor:pointer; box-shadow:0 2px 6px rgba(16,185,129,0.3); transition:all 0.15s ease;">
            🎙️ Speak Question
        </button>
        <span id="mic_status_{player_id}" style="font-size:12px; color:#94a3b8; background:rgba(255,255,255,0.04); padding:4px 10px; border-radius:10px; border:1px solid rgba(255,255,255,0.08);">
            Click to speak via browser microphone
        </span>
    </div>
    <script>
    var rec_{player_id} = null;
    var isRec_{player_id} = false;
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
        var SpeechAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
        rec_{player_id} = new SpeechAPI();
        rec_{player_id}.continuous = false;
        rec_{player_id}.interimResults = true;
        rec_{player_id}.lang = 'en-US';

        rec_{player_id}.onstart = function() {{
            isRec_{player_id} = true;
            var btn = document.getElementById('mic_btn_{player_id}');
            if (btn) {{
                btn.innerHTML = "🔴 Listening... Speak now";
                btn.style.background = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)";
            }}
            var st = document.getElementById('mic_status_{player_id}');
            if (st) st.innerHTML = "Listening to your voice...";
        }};

        rec_{player_id}.onresult = function(event) {{
            var text = "";
            for (var i = event.resultIndex; i < event.results.length; ++i) {{
                text += event.results[i][0].transcript;
            }}
            var st = document.getElementById('mic_status_{player_id}');
            if (st) st.innerHTML = "Captured: <em>" + text + "</em>";

            // Populate Streamlit chat input or textarea
            var inputs = window.parent.document.querySelectorAll('textarea, input[data-testid="stChatInputTextArea"]');
            if (inputs && inputs.length > 0) {{
                var inp = inputs[inputs.length - 1];
                inp.value = text;
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        }};

        rec_{player_id}.onend = function() {{
            isRec_{player_id} = false;
            var btn = document.getElementById('mic_btn_{player_id}');
            if (btn) {{
                btn.innerHTML = "🎙️ Speak Question";
                btn.style.background = "linear-gradient(135deg, #10b981 0%, #059669 100%)";
            }}
            var st = document.getElementById('mic_status_{player_id}');
            if (st) st.innerHTML = "Speech captured! Hit Enter to submit, or click Speak again.";
        }};

        rec_{player_id}.onerror = function(event) {{
            isRec_{player_id} = false;
            var btn = document.getElementById('mic_btn_{player_id}');
            if (btn) {{
                btn.innerHTML = "🎙️ Speak Question";
                btn.style.background = "linear-gradient(135deg, #10b981 0%, #059669 100%)";
            }}
            var st = document.getElementById('mic_status_{player_id}');
            if (st) st.innerHTML = "Microphone note: " + (event.error || "unavailable") + ". You can type your question.";
        }};
    }} else {{
        var st = document.getElementById('mic_status_{player_id}');
        if (st) st.innerHTML = "Web speech recognition ready in Chromium browsers. Type your questions below.";
    }}

    function toggleSpeechRec_{player_id}() {{
        if (!rec_{player_id}) return;
        if (isRec_{player_id}) {{
            rec_{player_id}.stop();
        }} else {{
            try {{
                rec_{player_id}.start();
            }} catch(e) {{
                console.log(e);
            }}
        }}
    }}
    </script>
    """
    st.components.v1.html(html_code, height=44, scrolling=False)


# Shared Country Metric Card
def render_country_info_card(column, label, value):
    with column:
        st.markdown(
            '<div class="country-info-card">'
            f'<div class="country-info-label">{html.escape(label)}</div>'
            f'<div class="country-info-value">{html.escape(str(value))}</div>'
            '</div>',
            unsafe_allow_html=True
        )


# Persistent Top Navigation Bar
def render_top_navigation(current_mode):
    dest = st.session_state.get("selected_country", "Japan")
    dest_flag = get_country_flag(dest)

    st.markdown(
        f"""
        <div class="top-nav-bar">
            <div>
                <div class="top-nav-brand-title">AI-Based Personalized Travel Planner</div>
                <div class="top-nav-brand-tagline">Your next adventure starts here.</div>
            </div>
            <div>
                <span class="top-nav-dest-badge">📍 {html.escape(dest)} {dest_flag}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    pages = [
        ("landing", "🏠 Home"),
        ("plan", "🧳 Plan My Trip"),
        ("explore", "🌍 Explore"),
        ("discover", "✨ Discover"),
        ("guide", "📖 Travel Guide"),
        ("itinerary", "📅 My Itinerary"),
        ("companion", "🤖 AI Companion"),
        ("safety", "🛡️ Safety"),
        ("saved", "🔖 Saved Places"),
        ("summary", "📋 Trip Summary")
    ]

    nav_cols = st.columns(len(pages))
    for idx, (mode_key, label) in enumerate(pages):
        is_active = (current_mode == mode_key)
        with nav_cols[idx]:
            if st.button(
                label,
                key=f"top_nav_tab_{mode_key}",
                type="primary" if is_active else "secondary",
                width="stretch"
            ):
                if not is_active:
                    st.session_state.app_mode = mode_key
                    st.rerun()


# Sidebar Controller disabled for modern full-page experience
def render_sidebar_controls():
    pass


# ------------------------------------------------------------
# SESSION & CONTEXT PREPARATION
# ------------------------------------------------------------

curr_mode = st.session_state.get("app_mode", "landing")
destination = st.session_state.get("selected_country", "Japan")
days = st.session_state.get("days", 7)
travelers = st.session_state.get("travelers", 1)
budget = st.session_state.get("budget", 80000)
interests = st.session_state.get("interests", ["Culture", "Food"])
style = st.session_state.get("style", "Relaxed")
starting_location = st.session_state.get("starting_location", "Your Location")

profile = get_country_profile(destination)
cities = profile.get("cities") or country_info(destination).get("places", [])
cities_str = " • ".join(cities[:5]) if cities else destination

# Ensure itinerary is generated
if st.session_state.itinerary is None:
    prof = get_country_profile(destination)
    tc = get_tourist_cards(destination)
    fc = get_food_cards(destination)
    register_country_for_planner(destination, prof, tc, fc)
    st.session_state.itinerary = generate_itinerary(
        starting_location,
        destination,
        days,
        travelers,
        budget,
        interests,
        style
    )

plan = st.session_state.itinerary
total_cost = plan.get("total_cost", 0) if plan else 0
remaining_budget = max(0, budget - total_cost)
interests_str = ", ".join(interests) if isinstance(interests, list) else str(interests)

# Initialize Assistant chat history
if "chat_history" not in st.session_state or not isinstance(st.session_state.chat_history, list):
    st.session_state.chat_history = []

if st.session_state.get("chat_destination") != destination:
    st.session_state.chat_destination = destination
    c_name = get_assistant_name("companion")
    welcome_text = (
        f"Hi! 👋 I'm **{c_name}**, your personal AI travel companion for **{destination}** {profile['flag']}.\n\n"
        f"I have loaded your personalized **{days}-day** trip plan for **{travelers} traveler{'s' if travelers > 1 else ''}**, "
        f"starting from **{starting_location}**, budget of **₹{budget:,}**, and **{interests_str}** preferences.\n\n"
        f"Ask me anything in **any language** about routes, visas, transit options, packing, food, places, or travel tips!"
    )
    st.session_state.chat_history = [
        {"role": "assistant", "content": welcome_text}
    ]

trip_context = {
    "starting": starting_location,
    "destination": destination,
    "days": days,
    "travelers": travelers,
    "budget": budget,
    "interests": interests,
    "style": style,
    "itinerary": plan,
    "transport": get_transportation(destination),
    "tips": get_travel_tips(destination)
}


# ============================================================
# PAGE 1: WELCOME / LANDING PAGE
# ============================================================

if curr_mode == "landing":

    # Hide sidebar on landing page to allow full-width hero presentation
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Hero Section with TWO TRAVELER CHARACTERS: Female on Left, Center Title/CTA, Male on Right
    guide_display_name = get_assistant_name("guide")
    companion_display_name = get_assistant_name("companion")

    char_col_f, hero_center_col, char_col_m = st.columns([1.15, 2.2, 1.15])

    with char_col_f:
        female_path = get_character_image("female")
        st.markdown(
            f"""
            <div class="hero-character-card">
                <span class="hero-character-badge">🎒 {html.escape(guide_display_name)} &bull; Travel Guide</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        if female_path:
            st.image(female_path, width="stretch")
        st.markdown(
            f"""
            <div class="hero-character-footer">
                &ldquo;Ready to uncover iconic destinations, authentic food, culture, and travel tips with {html.escape(guide_display_name)}!&rdquo;
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button(f"Explore with {guide_display_name} →", key="char_btn_female", type="primary", width="stretch"):
            st.session_state.app_mode = "guide"
            st.rerun()

    with hero_center_col:
        st.markdown(
            """
            <div class="landing-hero-center">
                <div class="landing-plane-icon">✈️</div>
                <div class="landing-pre-badge">AI-BASED PERSONALIZED TRAVEL PLANNER</div>
                <h1 class="landing-main-title">Your next adventure<br>starts here.</h1>
                <p class="landing-subtitle">Your next adventure starts here.</p>
                <p class="landing-description">
                    Discover beautiful places. Build your perfect trip. Travel your way.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("Plan My Trip", key="landing_cta_plan", type="primary", width="stretch"):
                st.session_state.app_mode = "plan"
                st.rerun()
        with btn_c2:
            if st.button("Explore Destinations", key="landing_cta_globe", type="secondary", width="stretch"):
                st.session_state.app_mode = "explore"
                st.rerun()

        # Onboarding Assistant Name Customizer
        with st.expander("✨ Personalize Assistant Name (e.g. Maya, Alex, Chinnu, Sofia)", expanded=False):
            asst_n_c1, asst_n_c2 = st.columns([3, 1.2])
            with asst_n_c1:
                cur_asst_custom = st.text_input(
                    "What would you like to call your travel assistant?",
                    value=st.session_state.get("custom_assistant_name", ""),
                    placeholder="Enter custom assistant name (e.g. Chinnu, Maya, Alex)...",
                    key="landing_name_input",
                    label_visibility="collapsed"
                )
            with asst_n_c2:
                if st.button("Save Name", key="landing_save_name_btn", width="stretch"):
                    st.session_state["custom_assistant_name"] = cur_asst_custom.strip()
                    st.rerun()

    with char_col_m:
        male_path = get_character_image("male")
        st.markdown(
            f"""
            <div class="hero-character-card">
                <span class="hero-character-badge" style="background: rgba(99,102,241,0.2); border-color: rgba(99,102,241,0.5); color: #818cf8;">🤖 {html.escape(companion_display_name)} &bull; AI Travel Companion</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        if male_path:
            st.image(male_path, width="stretch")
        st.markdown(
            f"""
            <div class="hero-character-footer">
                &ldquo;Ask {html.escape(companion_display_name)} anything about your trip or describe your travel preferences in free-form!&rdquo;
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button(f"Meet {companion_display_name} →", key="char_btn_male", type="primary", width="stretch"):
            st.session_state.app_mode = "companion"
            st.rerun()

    st.write("")
    st.markdown("---")

    # Feature Highlights Grid
    st.markdown("<div style='text-align: center; margin-bottom: 16px;'><span class='landing-pre-badge'>PLATFORM CAPABILITIES</span></div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)

    with f_col1:
        st.markdown(
            """
            <div class="landing-feature-card">
                <div class="landing-feature-icon">🌍</div>
                <div class="landing-feature-title">3D Interactive Globe</div>
                <div class="landing-feature-desc">Centerpiece 3D globe with country selection, zoom, hover, and instant trip synchronization.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Launch Globe →", key="feat_btn_globe", width="stretch"):
            st.session_state.app_mode = "explore"
            st.rerun()

    with f_col2:
        st.markdown(
            """
            <div class="landing-feature-card">
                <div class="landing-feature-icon">🎯</div>
                <div class="landing-feature-title">Personalized Itineraries</div>
                <div class="landing-feature-desc">1 to 30 day intelligent day-by-day itineraries tailored to your style, budget, and travel companions.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Configure Trip →", key="feat_btn_plan", width="stretch"):
            st.session_state.app_mode = "plan"
            st.rerun()

    with f_col3:
        st.markdown(
            """
            <div class="landing-feature-card">
                <div class="landing-feature-icon">🍜</div>
                <div class="landing-feature-title">Food & Heritage Attire</div>
                <div class="landing-feature-desc">Authentic regional culinary dishes with where to try them, plus traditional attire with rental costs.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Discover Culture →", key="feat_btn_disc", width="stretch"):
            st.session_state.app_mode = "discover"
            st.rerun()

    with f_col4:
        st.markdown(
            """
            <div class="landing-feature-card">
                <div class="landing-feature-icon">🤖</div>
                <div class="landing-feature-title">Multilingual AI Voice</div>
                <div class="landing-feature-desc">Interactive companion with Web Speech pronunciation, instant translations, and custom travel tips.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Ask Companion →", key="feat_btn_asst", width="stretch"):
            st.session_state.app_mode = "companion"
            st.rerun()

    # 30 Curated Featured Destinations Showcase
    st.write("")
    st.markdown(
        """
        <div style='text-align: center; margin-top: 15px; margin-bottom: 12px;'>
            <span class='landing-pre-badge'>CURATED COLLECTION</span>
            <div style='font-size: 20px; font-weight: 800; color: #f8fafc; margin-top: 4px;'>30 Hand-Crafted World Destinations</div>
            <div style='font-size: 13px; color: #94a3b8;'>Quality over quantity &bull; 100% authentic photography & verified cultural knowledge</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    feat_showcase = ["Japan", "France", "Italy", "Switzerland", "India", "Spain", "Greece", "Thailand"]
    q_cols = st.columns(len(feat_showcase))
    for q_idx, q_name in enumerate(feat_showcase):
        c_meta = CURATED_30_DESTINATIONS.get(q_name, {})
        with q_cols[q_idx]:
            if st.button(f"{c_meta.get('flag', '')} {q_name}", key=f"landing_quick_{q_name}", width="stretch"):
                switch_country_and_regenerate(q_name)
                st.session_state.app_mode = "plan"
                st.rerun()


# ============================================================
# PAGE 2: PLAN YOUR TRIP
# ============================================================

elif curr_mode == "plan":
    render_top_navigation("plan")

    st.markdown(
        """
        <div class="page-header-box">
            <span class="page-badge" style="background: rgba(56,189,248,0.18); color: #38bdf8; border: 1px solid rgba(56,189,248,0.35);">
                🧳 GUIDED TRIP PLANNER &bull; 5 PROGRESSIVE STEPS
            </span>
            <h1 class="page-title">Build Your Personalized Journey</h1>
            <p class="page-subtitle">Configure your destination, duration, companions, travel rhythm, and favorite passions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Planner Mode Toggle: Multi-Stop vs Single Destination
    plan_mode_choice = st.radio(
        "Trip Planning Experience:",
        [
            "🧳 Multi-Stop Journey Planner (Multi-City & Multi-Country)",
            "📍 Single-Destination 5-Step Planner"
        ],
        index=0 if st.session_state.get("multi_stop_plan") else 0,
        horizontal=True,
        key="planner_experience_toggle"
    )

    if plan_mode_choice.startswith("🧳"):
        # ========================================================
        # MULTI-STOP, MULTI-COUNTRY ITINERARY PLANNER
        # ========================================================
        from multi_stop_planner import parse_multi_stop_trip_prompt, generate_multi_stop_journey

        with st.container(border=True):
            st.markdown("### 🗺️ Natural-Language Multi-Stop Planner")
            st.caption("Describe a multi-city or multi-country trip in plain English (e.g., origin, destinations, duration per stop, and final return):")

            # Quick Example Chips
            st.markdown("<div style='font-size: 12px; color: #94a3b8; font-weight: 600; margin-bottom: 6px;'>💡 Quick Sample Multi-Stop Prompts:</div>", unsafe_allow_html=True)
            ex_cols = st.columns(3)
            sample_query = None
            with ex_cols[0]:
                if st.button("🇯🇵 Hyd → Tokyo (2d) → Kyoto (3d) → Osaka (2d) → Hyd", key="ex_btn_japan", width="stretch"):
                    sample_query = "I will start from Hyderabad on December 10. I want to travel to Japan, stay in Tokyo for 2 days, then go to Kyoto for 3 days, then visit Osaka for 2 days, and finally return to Hyderabad. Recommend the route, transportation, and a complete itinerary."
            with ex_cols[1]:
                if st.button("🇪🇺 Mumbai → Paris (3d) → Switzerland (3d) → Rome (3d) → Mumbai", key="ex_btn_europe", width="stretch"):
                    sample_query = "Starting from Mumbai, visit France with 3 days in Paris, then 3 days in Switzerland, then 3 days in Rome, and return to Mumbai. Budget 2.5L, balanced pace."
            with ex_cols[2]:
                if st.button("🌏 Delhi → Bangkok (3d) → Singapore (3d) → Delhi", key="ex_btn_asia", width="stretch"):
                    sample_query = "Start from Delhi, 3 days in Bangkok Thailand, 3 days in Singapore, return to Delhi. Budget 90000, relaxed pace."

            nl_input_val = sample_query or ""
            nl_query_box = st.text_area(
                "Describe your multi-stop journey:",
                value=nl_input_val,
                placeholder="Example: I will start from Hyderabad on December 10. I want to travel to Japan, stay in Tokyo for 2 days, then go to Kyoto for 3 days, then visit Osaka for 2 days, and finally return to Hyderabad. Recommend the route, transportation, and a complete itinerary.",
                height=90,
                key="plan_multi_nl_input"
            )

            nl_m_c1, nl_m_c2 = st.columns([3, 1.2])
            with nl_m_c2:
                if st.button("🚀 Plan Multi-Stop Route", key="plan_multi_gen_btn", type="primary", width="stretch"):
                    q_to_parse = nl_query_box.strip() if nl_query_box and nl_query_box.strip() else sample_query
                    if q_to_parse:
                        parsed_m = parse_multi_stop_trip_prompt(q_to_parse)
                        journey = generate_multi_stop_journey(parsed_m)
                        st.session_state.multi_stop_plan = journey
                        st.session_state.starting_location = journey.get("origin", "Hyderabad")
                        if journey.get("stops"):
                            st.session_state.selected_country = journey["stops"][0]["country"]
                            st.session_state.globe_country = journey["stops"][0]["country"]
                            st.session_state.days = journey["total_days"]
                            st.session_state.budget = journey["budget"]
                            st.session_state.travelers = journey["travelers"]
                            st.session_state.style = journey["style"]
                        st.success(f"Generated multi-stop journey across {len(journey['stops'])} destinations ({journey['total_days']} days)!")
                        st.session_state.app_mode = "itinerary"
                        st.rerun()
                    else:
                        st.warning("Please enter your journey details or click a sample prompt.")

        st.write("")

        # INTERACTIVE EDITABLE STOPS BUILDER
        with st.container(border=True):
            st.markdown("### 🎛️ Interactive Multi-Stop Builder")
            st.caption("Customize your starting city, dates, destinations, stay duration, transportation mode, and return trip:")

            meta_c1, meta_c2, meta_c3 = st.columns(3)
            with meta_c1:
                cur_start = st.text_input(
                    "🛫 Starting City / Address:",
                    value=st.session_state.get("starting_location", "Hyderabad") or "Hyderabad",
                    key="multi_builder_origin"
                )
                st.session_state.starting_location = cur_start
            with meta_c2:
                cur_dep_date = st.text_input(
                    "📅 Departure Date:",
                    value="December 10, 2026",
                    key="multi_builder_date"
                )
            with meta_c3:
                cur_return_city = st.text_input(
                    "🛬 Final Return Destination:",
                    value=cur_start,
                    key="multi_builder_return"
                )

            pref_c1, pref_c2, pref_c3 = st.columns(3)
            with pref_c1:
                cur_travelers = st.number_input(
                    "👥 Number of Travelers:",
                    min_value=1,
                    max_value=20,
                    value=st.session_state.get("travelers", 1),
                    key="multi_builder_travelers"
                )
                st.session_state.travelers = cur_travelers
            with pref_c2:
                cur_budget = st.number_input(
                    "💰 Total Approximate Budget (₹ INR):",
                    min_value=15000,
                    max_value=2000000,
                    step=5000,
                    value=st.session_state.get("budget", 150000),
                    key="multi_builder_budget"
                )
                st.session_state.budget = cur_budget
            with pref_c3:
                cur_trans_pref = st.selectbox(
                    "🚆 Preferred Transit Mode:",
                    [
                        "Balanced (High-Speed Rail & Flights)",
                        "High-Speed Rail Priority",
                        "Budget Flights & Local Transit",
                        "Scenic Overland & Express Coaches"
                    ],
                    key="multi_builder_trans_pref"
                )

            st.markdown("#### 📍 Ordered Destination Stops:")
            st.caption("Add, remove, or reorder cities and customize the number of days spent at each stop:")

            stops_list = st.session_state.setdefault("multi_stops_list", [
                {"city": "Tokyo", "country": "Japan", "days": 2},
                {"city": "Kyoto", "country": "Japan", "days": 3},
                {"city": "Osaka", "country": "Japan", "days": 2}
            ])

            for s_idx, stop in enumerate(stops_list):
                s_c1, s_c2, s_c3, s_c4 = st.columns([1.5, 1.5, 1, 0.8])
                with s_c1:
                    stop_city = st.text_input(
                        f"Stop #{s_idx + 1} City:",
                        value=stop.get("city", "Tokyo"),
                        key=f"stop_city_{s_idx}"
                    )
                    stop["city"] = stop_city
                with s_c2:
                    country_options = CURATED_COUNTRIES if stop.get("country") in CURATED_COUNTRIES else [stop.get("country", "Japan")] + [c for c in CURATED_COUNTRIES if c != stop.get("country")]
                    c_idx = country_options.index(stop.get("country", "Japan")) if stop.get("country", "Japan") in country_options else 0
                    stop_country = st.selectbox(
                        f"Country #{s_idx + 1}:",
                        country_options,
                        index=c_idx,
                        key=f"stop_country_{s_idx}"
                    )
                    stop["country"] = stop_country
                with s_c3:
                    stop_days = st.number_input(
                        f"Days #{s_idx + 1}:",
                        min_value=1,
                        max_value=30,
                        value=int(stop.get("days", 2)),
                        key=f"stop_days_{s_idx}"
                    )
                    stop["days"] = stop_days
                with s_c4:
                    st.write("")
                    st.write("")
                    if len(stops_list) > 1:
                        if st.button("🗑️ Remove", key=f"stop_del_{s_idx}"):
                            stops_list.pop(s_idx)
                            st.rerun()

            btn_add_col, btn_gen_col = st.columns([1.5, 2.5])
            with btn_add_col:
                if st.button("➕ Add Another Stop", key="multi_add_stop_btn", width="stretch"):
                    stops_list.append({"city": "New Destination", "country": stops_list[-1]["country"] if stops_list else "Japan", "days": 2})
                    st.rerun()
            with btn_gen_col:
                if st.button("🚀 Build Multi-Stop Itinerary from Config", key="multi_gen_table_btn", type="primary", width="stretch"):
                    structured_params = {
                        "origin": cur_start,
                        "departure_date": cur_dep_date,
                        "return_destination": cur_return_city,
                        "stops": stops_list,
                        "travelers": cur_travelers,
                        "budget": cur_budget,
                        "preferred_transport": cur_trans_pref,
                        "style": "Balanced"
                    }
                    journey = generate_multi_stop_journey(structured_params)
                    st.session_state.multi_stop_plan = journey
                    st.session_state.starting_location = cur_start
                    if stops_list:
                        st.session_state.selected_country = stops_list[0]["country"]
                        st.session_state.globe_country = stops_list[0]["country"]
                        st.session_state.days = journey["total_days"]
                    st.success(f"Multi-stop journey successfully generated with {len(stops_list)} stops!")
                    st.session_state.app_mode = "itinerary"
                    st.rerun()

    else:
        # ========================================================
        # SINGLE-DESTINATION 5-STEP GUIDED PLANNER
        # ========================================================
        # NATURAL-LANGUAGE TRIP PLANNING CONTAINER
        with st.container(border=True):
            st.markdown("### 💬 Natural-Language Trip Planner")
            st.caption("Describe your ideal journey in plain English (e.g. *'Plan a 5-day trip to Japan under ₹80,000 with a relaxed pace and focus on food & culture'*):")
            nl_input_col, nl_btn_col = st.columns([4, 1.2])
            with nl_input_col:
                nl_query = st.text_input(
                    "Describe your trip:",
                    placeholder="Example: Plan a relaxed 7-day trip to Italy for 2 travelers under ₹1.5L focusing on food and culture",
                    key="plan_nl_trip_input",
                    label_visibility="collapsed"
                )
            with nl_btn_col:
                if st.button("✨ Generate Plan", key="plan_nl_generate_btn", type="primary", width="stretch"):
                    if nl_query and nl_query.strip():
                        parsed = parse_natural_language_trip(nl_query)
                        if parsed.get("is_multi_stop"):
                            st.session_state.multi_stop_plan = parsed["multi_plan"]
                            st.session_state.selected_country = parsed.get("destination", "Japan")
                            st.session_state.days = parsed.get("days", 7)
                            st.session_state.app_mode = "itinerary"
                            st.success("Generated multi-stop journey!")
                            st.rerun()
                        if "destination" in parsed:
                            st.session_state.selected_country = parsed["destination"]
                            st.session_state.globe_country = parsed["destination"]
                        if "days" in parsed:
                            st.session_state.days = parsed["days"]
                        if "budget" in parsed:
                            st.session_state.budget = parsed["budget"]
                        if "travelers" in parsed:
                            st.session_state.travelers = parsed["travelers"]
                        if "style" in parsed:
                            st.session_state.style = parsed["style"]
                        if "interests" in parsed:
                            st.session_state.interests = parsed["interests"]

                        dest_name = st.session_state.selected_country
                        prof = get_country_profile(dest_name)
                        tc = get_tourist_cards(dest_name)
                        fc = get_food_cards(dest_name)
                        register_country_for_planner(dest_name, prof, tc, fc)
                        st.session_state.itinerary = generate_itinerary(
                            st.session_state.get("starting_location", "Your Location"),
                            dest_name,
                            st.session_state.days,
                            st.session_state.travelers,
                            st.session_state.budget,
                            st.session_state.interests,
                            st.session_state.style
                        )
                        st.success(f"Generated a {st.session_state.days}-day personalized itinerary for {dest_name}!")
                        st.session_state.app_mode = "itinerary"
                        st.rerun()
                    else:
                        st.warning("Please type your travel request.")

        st.write("")

    # STEP 01: WHERE DO YOU WANT TO GO?
    with st.container(border=True):
        st.markdown("### 📍 STEP 01: Where do you want to go?")
        st.caption("Select your starting point and pick from our 30 curated world travel destinations.")

        loc_c1, loc_c2 = st.columns([1, 1.2])
        with loc_c1:
            start_val = st.text_input(
                "Starting Location / City:",
                value=st.session_state.get("starting_location", ""),
                placeholder="Example: Hyderabad, New York, London, Tokyo...",
                key="plan_start_input"
            )
            final_start = start_val
            if start_val and len(start_val.strip()) >= 3:
                loc_res = search_locations(start_val)
                if loc_res:
                    final_start = st.selectbox(
                        "Suggested matching locations:",
                        loc_res,
                        key="plan_start_select"
                    )

        with loc_c2:
            curr_dest = st.session_state.get("selected_country", "Japan")
            dropdown_list = CURATED_COUNTRIES if curr_dest in CURATED_COUNTRIES else countries
            dest_idx = dropdown_list.index(curr_dest) if curr_dest in dropdown_list else 0

            chosen_dest = st.selectbox(
                "🌍 Destination Country (30 Featured Destinations):",
                dropdown_list,
                index=dest_idx,
                key=f"plan_dest_select_{curr_dest}"
            )

        # Quick Destination Chips for 30 Curated Countries
        st.markdown("<div style='font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 8px; margin-bottom: 6px;'>⚡ Quick Select Featured Destinations:</div>", unsafe_allow_html=True)
        top_dest_chips = ["Japan", "France", "Italy", "Switzerland", "Spain", "Greece", "India", "Thailand", "United States", "Nepal"]
        chip_cols = st.columns(len(top_dest_chips))
        for c_idx, c_name in enumerate(top_dest_chips):
            c_meta = CURATED_30_DESTINATIONS.get(c_name, {})
            with chip_cols[c_idx]:
                if st.button(f"{c_meta.get('flag', '')} {c_name}", key=f"chip_dest_{c_name}", width="stretch"):
                    chosen_dest = c_name
                    switch_country_and_regenerate(c_name)
                    st.rerun()

    step_grid1, step_grid2 = st.columns(2)

    # STEP 02: HOW LONG ARE YOU STAYING?
    with step_grid1:
        with st.container(border=True):
            st.markdown("### 📅 STEP 02: How long are you staying?")
            st.caption("Choose duration from 1 to 30 days:")

            dur_pill1, dur_pill2, dur_pill3, dur_pill4 = st.columns(4)
            preset_days = None
            with dur_pill1:
                if st.button("5 Days", key="pill_days_5", width="stretch"):
                    preset_days = 5
            with dur_pill2:
                if st.button("10 Days", key="pill_days_10", width="stretch"):
                    preset_days = 10
            with dur_pill3:
                if st.button("15 Days", key="pill_days_15", width="stretch"):
                    preset_days = 15
            with dur_pill4:
                if st.button("30 Days", key="pill_days_30", width="stretch"):
                    preset_days = 30

            current_duration = preset_days or st.session_state.get("days", 7)
            chosen_days = st.slider(
                "Trip Duration in Days:",
                min_value=1,
                max_value=30,
                value=current_duration,
                key="plan_days_slider"
            )

    # STEP 03: WHO ARE YOU TRAVELLING WITH?
    with step_grid2:
        with st.container(border=True):
            st.markdown("### 👥 STEP 03: Who are you travelling with?")
            st.caption("Select your travel party type and total budget:")

            comp_pill1, comp_pill2, comp_pill3, comp_pill4 = st.columns(4)
            preset_travelers = None
            with comp_pill1:
                if st.button("Solo (1)", key="pill_comp_solo", width="stretch"):
                    preset_travelers = 1
            with comp_pill2:
                if st.button("Couple (2)", key="pill_comp_couple", width="stretch"):
                    preset_travelers = 2
            with comp_pill3:
                if st.button("Friends (3)", key="pill_comp_friends", width="stretch"):
                    preset_travelers = 3
            with comp_pill4:
                if st.button("Family (4)", key="pill_comp_family", width="stretch"):
                    preset_travelers = 4

            t_col1, t_col2 = st.columns(2)
            with t_col1:
                chosen_travelers = st.number_input(
                    "Total Travelers:",
                    min_value=1,
                    max_value=15,
                    value=preset_travelers or st.session_state.get("travelers", 1),
                    key="plan_travelers_input"
                )
            with t_col2:
                chosen_budget = st.number_input(
                    "Total Budget (₹ INR):",
                    min_value=5000,
                    max_value=2500000,
                    value=st.session_state.get("budget", 80000),
                    step=5000,
                    key="plan_budget_input"
                )

    step_grid3, step_grid4 = st.columns(2)

    # STEP 04: CHOOSE YOUR TRAVEL STYLE
    with step_grid3:
        with st.container(border=True):
            st.markdown("### 🧳 STEP 04: Choose your travel style")
            st.caption("Select the tempo and rhythm that fits your vacation mood:")

            style_options = ["Packed", "Balanced", "Relaxed"]
            curr_style = st.session_state.get("style", "Relaxed")
            style_idx = style_options.index(curr_style) if curr_style in style_options else 0

            chosen_style = st.selectbox(
                "Travel Tempo & Rhythm:",
                style_options,
                index=style_idx,
                key="plan_style_select"
            )

            if chosen_style == "Packed":
                st.info("⚡ **Packed:** High-energy schedule with 3 curated activities daily covering maximum landmark sights.")
            elif chosen_style == "Balanced":
                st.info("⚖️ **Balanced:** Classic highlights with 2 daily activities, leisurely meals, and scenic strolls.")
            else:
                st.info("🌿 **Relaxed:** Leisurely morning starts with 1 major activity daily and plenty of free time.")

    # STEP 05: CHOOSE YOUR INTERESTS
    with step_grid4:
        with st.container(border=True):
            st.markdown("### ❤️ STEP 05: Choose your interests")
            st.caption("Pick activities that excite you to personalize daily themes:")

            interest_options = [
                "Culture", "Food", "Adventure", "Beaches",
                "Nature", "Shopping", "Photography", "History"
            ]
            default_interests = [i for i in st.session_state.get("interests", ["Culture", "Food"]) if i in interest_options]
            chosen_interests = st.multiselect(
                "Select Interests:",
                interest_options,
                default=default_interests if default_interests else ["Culture", "Food"],
                key="plan_interests_multi"
            )
            if not chosen_interests:
                chosen_interests = ["Culture", "Food"]

            with st.expander("🥗 Dietary Requirements & Cultural Focus (Optional)", expanded=False):
                diet_options = [
                    "🌱 Vegetarian",
                    "🌿 Vegan",
                    "☪️ Halal-friendly",
                    "🌾 Gluten-Free / Celiac",
                    "🥜 Nut Allergy",
                    "🌶️ Mild Food (Low Spice)",
                    "🔥 Spicy Food Welcome",
                    "🥢 Street Food & Night Markets",
                    "🍷 Fine & Traditional Dining"
                ]
                chosen_dietary = st.multiselect(
                    "Dietary Needs & Food Style:",
                    diet_options,
                    default=st.session_state.get("dietary_preferences", []),
                    key="plan_dietary_multi"
                )
                cult_options = [
                    "👘 Traditional Clothing & Kimono / Hanbok Experience",
                    "⛩️ Historic Temples, Shrines & Sacred Heritage",
                    "🍵 Tea Ceremonies & Traditional Workshops",
                    "🏮 Local Festivals & Traditional Folk Arts",
                    "🎨 Artisan Crafts, Ceramics & Markets",
                    "🏛️ Historic Architecture & Heritage Quarters"
                ]
                chosen_cultural = st.multiselect(
                    "Cultural Focus & Activities:",
                    cult_options,
                    default=st.session_state.get("cultural_preferences", []),
                    key="plan_cultural_multi"
                )

    # CTA BUTTON: BUILD MY TRIP
    st.write("")
    nav_btn_c1, nav_btn_c2 = st.columns([1, 2])
    with nav_btn_c1:
        if st.button("← 🏠 Back to Home", key="plan_back_home", width="stretch"):
            st.session_state.app_mode = "landing"
            st.rerun()

    with nav_btn_c2:
        if st.button("✨ Build My Trip", key="plan_build_trip_btn", type="primary", width="stretch"):
            resolved_start = (final_start or "").strip() or "Your Location"
            st.session_state.starting_location = resolved_start
            st.session_state.selected_country = chosen_dest
            st.session_state.globe_country = chosen_dest
            st.session_state.days = chosen_days
            st.session_state.travelers = chosen_travelers
            st.session_state.budget = chosen_budget
            st.session_state.interests = chosen_interests
            st.session_state.style = chosen_style
            st.session_state.dietary_preferences = chosen_dietary
            st.session_state.cultural_preferences = chosen_cultural

            # Register country & generate itinerary
            prof = get_country_profile(chosen_dest)
            tc = get_tourist_cards(chosen_dest)
            fc = get_food_cards(chosen_dest)
            register_country_for_planner(chosen_dest, prof, tc, fc)

            with st.spinner(f"Crafting personalized itinerary for {chosen_dest}..."):
                st.session_state.itinerary = generate_itinerary(
                    resolved_start,
                    chosen_dest,
                    chosen_days,
                    chosen_travelers,
                    chosen_budget,
                    chosen_interests,
                    chosen_style,
                    dietary_preferences=chosen_dietary,
                    cultural_preferences=chosen_cultural
                )

            st.session_state.app_mode = "itinerary"
            st.rerun()


# ============================================================
# PAGE 3: EXPLORE DESTINATION (3D GLOBE & COUNTRY PROFILE)
# ============================================================

elif curr_mode == "explore":
    render_top_navigation("explore")

    st.markdown(
        f"""
        <div class="page-header-box">
            <span class="page-badge" style="background: rgba(99,102,241,0.2); color: #818cf8; border: 1px solid rgba(99,102,241,0.4);">
                🌍 INTERACTIVE 3D GLOBE
            </span>
            <h1 class="page-title">Explore the World</h1>
            <p class="page-subtitle">30 curated destinations. Endless experiences.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3D Plotly Globe Centerpiece
    globe = create_globe(destination)
    globe_event = st.plotly_chart(
        globe,
        width="stretch",
        on_select="rerun",
        selection_mode="points",
        key=f"world_globe_{st.session_state.selected_country}",
        theme=None,
        config={
            "scrollZoom": True,
            "displaylogo": False,
            "responsive": True
        }
    )

    # Globe Click Detection
    try:
        if globe_event:
            selection = getattr(globe_event, "selection", None)
            if selection is None and isinstance(globe_event, dict):
                selection = globe_event.get("selection")

            if selection:
                points = getattr(selection, "points", None)
                if points is None and isinstance(selection, dict):
                    points = selection.get("points")

                if points and len(points) > 0:
                    for pt in points:
                        clicked_country = None

                        # 1. customdata has the exact display country name
                        cd = pt.get("customdata") if isinstance(pt, dict) else getattr(pt, "customdata", None)
                        if cd is not None:
                            while isinstance(cd, (list, tuple)) and len(cd) > 0:
                                cd = cd[0]
                            if cd and isinstance(cd, str) and cd.strip():
                                clicked_country = cd.strip()

                        # 2. Text attribute
                        if not clicked_country:
                            tv = pt.get("text") if isinstance(pt, dict) else getattr(pt, "text", None)
                            if tv is not None:
                                while isinstance(tv, (list, tuple)) and len(tv) > 0:
                                    tv = tv[0]
                                if tv and isinstance(tv, str) and tv.strip():
                                    if any(k in tv for k in ["Jammu", "Kashmir", "Ladakh", "Srinagar", "Gulmarg", "Leh", "Kargil"]):
                                        clicked_country = "India"
                                    else:
                                        clicked_country = tv.strip()

                        # 3. Fallback to ISO-3 location code
                        if not clicked_country:
                            location = pt.get("location") if isinstance(pt, dict) else getattr(pt, "location", None)
                            if location and location in ISO3_TO_COUNTRY:
                                clicked_country = ISO3_TO_COUNTRY[location]

                        # 4. Fallback to curve_number & point_number index
                        if not clicked_country:
                            curve_num = pt.get("curve_number") if isinstance(pt, dict) else getattr(pt, "curve_number", None)
                            pt_idx = pt.get("point_number") if isinstance(pt, dict) else getattr(pt, "point_number", None)
                            if pt_idx is not None:
                                if curve_num == 1 and 0 <= pt_idx < len(GLOBE_MARKER_NAMES):
                                    clicked_country = GLOBE_MARKER_NAMES[pt_idx]
                                elif 0 <= pt_idx < len(GLOBE_DISPLAY_NAMES):
                                    clicked_country = GLOBE_DISPLAY_NAMES[pt_idx]

                        if clicked_country:
                            st.session_state.selected_globe_place = None
                            switch_country_and_regenerate(clicked_country)
                            break
    except Exception:
        pass

    # Destination Switch Bar & Quick Destinations
    exp_sw1, exp_sw2 = st.columns([1, 2])
    with exp_sw1:
        dropdown_exp_list = CURATED_COUNTRIES if destination in CURATED_COUNTRIES else countries
        dash_country_idx = dropdown_exp_list.index(destination) if destination in dropdown_exp_list else 0
        dash_selected_country = st.selectbox(
            "📍 Switch Destination Country:",
            dropdown_exp_list,
            index=dash_country_idx,
            key=f"explore_dest_switch_{destination}"
        )
        if dash_selected_country != destination:
            st.session_state.selected_globe_place = None
            switch_country_and_regenerate(dash_selected_country)
            st.rerun()

    with exp_sw2:
        st.markdown("<div style='font-size: 13px; color: #94a3b8; font-weight: 600; margin-bottom: 5px;'>⚡ 30 Curated Quick Picks:</div>", unsafe_allow_html=True)
        quick_destinations = ["Japan", "France", "Italy", "Switzerland", "Spain", "Greece", "India", "Thailand"]
        q_cols = st.columns(len(quick_destinations))
        for q_idx, q_name in enumerate(quick_destinations):
            with q_cols[q_idx]:
                if st.button(q_name, key=f"exp_quick_{q_name}", width="stretch"):
                    st.session_state.selected_globe_place = None
                    switch_country_and_regenerate(q_name)
                    st.rerun()

    st.write("")

    # Two-Level Content Strategy (Curated vs Global Country Info)
    is_curated = destination in CURATED_30_DESTINATIONS
    c_meta = CURATED_30_DESTINATIONS.get(destination, {})
    flag_emoji = c_meta.get("flag", profile.get("flag", "🌍"))
    tagline_text = c_meta.get("tagline") or profile.get("description") or f"Discover the iconic sights and vibrant culture across {destination}."
    cap_val = c_meta.get("capital", profile.get("capital", "Capital City"))
    curr_val = c_meta.get("currency", profile.get("currency", "Local Currency"))
    season_val = c_meta.get("best_season", profile.get("best_time", "Spring / Autumn"))
    dur_val = c_meta.get("suggested_duration", f"{days} Days")

    # Resolve Important Places for this Country
    t_cards = get_tourist_cards(destination)
    places_list = []
    if t_cards:
        for tc in t_cards:
            p_n = tc.get("name")
            if p_n and p_n not in places_list:
                places_list.append(p_n)
    if is_curated:
        for item in c_meta.get("highlights", []) + c_meta.get("cities", []):
            if item not in places_list:
                places_list.append(item)
    if not places_list:
        places_list = profile.get("cities", [destination])
    places_list = places_list[:6]

    with st.container(border=True):
        st.markdown(
            f"""
            <div style="margin-bottom: 14px;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                    <span style="font-size: 28px; font-weight: 900; color: #f8fafc;">
                        {flag_emoji} {destination.upper()}
                    </span>
                    {"<span style='background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 999px; padding: 4px 12px; font-size: 11.5px; font-weight: 700;'>✨ FEATURED CURATED DESTINATION</span>" if is_curated else "<span style='background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); border-radius: 999px; padding: 4px 12px; font-size: 11.5px; font-weight: 600;'>🌐 GLOBAL DESTINATION</span>"}
                </div>
                <div style="font-size: 15px; color: #38bdf8; font-weight: 600; font-style: italic; margin-top: 3px;">
                    &ldquo;{tagline_text}&rdquo;
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Quick Facts
        prev_c1, prev_c2, prev_c3, prev_c4 = st.columns(4)
        render_country_info_card(prev_c1, "🏛️ Capital", cap_val)
        render_country_info_card(prev_c2, "💰 Currency", curr_val)
        render_country_info_card(prev_c3, "🌤️ Best Season", season_val)
        render_country_info_card(prev_c4, "📅 Duration", dur_val)

        st.markdown("---")

        # Country -> Destinations -> Experiences: Clickable Place Pills
        st.markdown(f"<div style='font-size: 13px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;'>📍 Top Destinations in {destination} (Click to inspect):</div>", unsafe_allow_html=True)
        if places_list:
            pl_cols = st.columns(min(len(places_list), 6))
            for pl_i, pl_name in enumerate(places_list):
                with pl_cols[pl_i % len(pl_cols)]:
                    curr_sel = st.session_state.get("selected_globe_place")
                    is_active_place = (curr_sel == pl_name)
                    if st.button(
                        f"📍 {pl_name}",
                        key=f"exp_place_pill_{destination}_{pl_name}_{pl_i}",
                        type="primary" if is_active_place else "secondary",
                        width="stretch"
                    ):
                        st.session_state.selected_globe_place = pl_name
                        st.rerun()

        # Place Spotlight Experience
        active_place = st.session_state.get("selected_globe_place")
        if active_place:
            match_tc = next((c for c in t_cards if c.get("name") == active_place), None) if t_cards else None
            p_desc = match_tc.get("description") if match_tc else f"Iconic highlight and sightseeing destination in {destination}."
            p_loc = match_tc.get("location") if match_tc else destination
            p_high = match_tc.get("highlights") if match_tc else "Photogenic scenery and cultural importance."
            p_tip = match_tc.get("tip") if match_tc else "Arrive early morning for best lighting and fewer visitors."

            st.write("")
            with st.container(border=True):
                spot_c1, spot_c2 = st.columns([1.1, 2])
                with spot_c1:
                    spot_img_bytes, _ = get_card_image_bytes(destination, active_place, "place", location=p_loc)
                    if spot_img_bytes:
                        st.image(spot_img_bytes, width="stretch")
                    else:
                        st.markdown(
                            f"""
                            <div style="background: rgba(15, 23, 42, 0.75); border: 1px dashed rgba(56, 189, 248, 0.4); border-radius: 10px; padding: 28px 12px; text-align: center;">
                                <div style="font-size: 28px; margin-bottom: 4px;">🏛️</div>
                                <div style="font-weight: 700; color: #38bdf8; font-size: 13px;">{active_place}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                with spot_c2:
                    st.markdown(f"### 📍 {active_place}")
                    st.caption(f"**Location:** {p_loc} &bull; **Destination:** {destination}")
                    st.write(p_desc)
                    st.markdown(f"**✨ Highlights:** {p_high}")
                    st.markdown(f"**💡 Traveler Tip:** {p_tip}")

                    btn_sp1, btn_sp2, btn_sp3, btn_sp4 = st.columns(4)
                    with btn_sp1:
                        if st.button(f"🔍 Discover", key=f"spot_go_disc_{active_place}", type="primary", width="stretch"):
                            st.session_state.app_mode = "discover"
                            st.rerun()
                    with btn_sp2:
                        if st.button(f"📖 Guide", key=f"spot_go_guide_{active_place}", width="stretch"):
                            st.session_state.app_mode = "guide"
                            st.rerun()
                    with btn_sp3:
                        is_sp_saved = is_place_saved(active_place, destination)
                        lbl_sp = "🔖 Saved" if is_sp_saved else "🔖 Save"
                        if st.button(lbl_sp, key=f"spot_save_{destination}_{active_place}", type="primary" if is_sp_saved else "secondary", width="stretch"):
                            toggle_save_place({
                                "name": active_place,
                                "country": destination,
                                "type": "place",
                                "location": p_loc,
                                "description": p_desc
                            })
                            st.rerun()
                    with btn_sp4:
                        if st.button("➕ Add to Trip", key=f"spot_itin_{destination}_{active_place}", width="stretch"):
                            if add_place_to_itinerary(active_place, destination, target_day=1):
                                st.success(f"Added {active_place} to your Day 1 itinerary!")
                            else:
                                st.info("Please generate an itinerary first in Plan My Trip.")

        st.write("")
        exp_cta1, exp_cta2, exp_cta3 = st.columns(3)
        with exp_cta1:
            if st.button(f"✨ Explore {destination}", key=f"exp_preview_discover_{destination}", type="primary", width="stretch"):
                st.session_state.app_mode = "discover"
                st.rerun()
        with exp_cta2:
            if st.button(f"🧳 Plan Trip to {destination}", key=f"exp_preview_plan_{destination}", width="stretch"):
                st.session_state.app_mode = "plan"
                st.rerun()
        with exp_cta3:
            if st.button(f"📖 Travel Guide", key=f"exp_preview_guide_{destination}", width="stretch"):
                st.session_state.app_mode = "guide"
                st.rerun()

        if not is_curated:
            st.caption(f"⭐ Note: Basic country information and custom itineraries are available for all nations. Deep-dive attire pricing and verified culinary guides are featured for our 30 Curated Destinations.")


# ============================================================
# PAGE 4: DISCOVER DESTINATION (PLACES, FOOD, ATTIRE, CULTURE)
# ============================================================

elif curr_mode == "discover":
    render_top_navigation("discover")

    st.markdown(
        f"""
        <div class="page-header-box">
            <span class="page-badge" style="background: rgba(236,72,153,0.2); color: #f472b6; border: 1px solid rgba(236,72,153,0.4);">
                ✨ DESTINATION DISCOVERY
            </span>
            <h1 class="page-title">Discover the World</h1>
            <p class="page-subtitle">Places, flavours, cultures and experiences worth remembering.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Country Detail Experience Banner (Section 11)
    c_meta_d = CURATED_30_DESTINATIONS.get(destination, {})
    d_tagline = c_meta_d.get("tagline") or profile.get("description") or f"Where authentic heritage and remarkable journeys meet."
    d_cities = c_meta_d.get("cities", profile.get("cities", [destination]))[:4]
    d_cities_str = " &bull; ".join(d_cities)

    with st.container(border=True):
        st.markdown(
            f"""
            <div style="margin-bottom: 12px;">
                <div style="font-size: 28px; font-weight: 900; color: #f8fafc;">
                    {profile['flag']} {destination.upper()}
                </div>
                <div style="font-size: 15px; color: #38bdf8; font-weight: 600; font-style: italic; margin-top: 2px;">
                    &ldquo;{d_tagline}&rdquo;
                </div>
                <div style="font-size: 13px; color: #cbd5e1; margin-top: 6px;">
                    🏙️ <strong>Key Hubs:</strong> {d_cities_str}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        d_q1, d_q2, d_q3, d_q4, d_q5, d_q6 = st.columns(6)
        with d_q1:
            st.metric("🏛️ Capital", c_meta_d.get("capital", profile.get("capital", "Capital")))
        with d_q2:
            st.metric("💰 Currency", c_meta_d.get("currency", profile.get("currency", "Currency")))
        with d_q3:
            st.metric("🗣️ Languages", profile.get("languages", "Local")[:14])
        with d_q4:
            st.metric("🌍 Region", profile.get("region", "Global")[:14])
        with d_q5:
            st.metric("🌤️ Best Time", c_meta_d.get("best_season", profile.get("best_time", "Spring / Autumn"))[:16])
        with d_q6:
            st.metric("📅 Suggested", c_meta_d.get("suggested_duration", f"{days} Days"))

        st.write("")
        d_cta1, d_cta2, d_cta3 = st.columns(3)
        with d_cta1:
            if st.button("🧳 Plan a Trip", key="disc_hero_plan", width="stretch"):
                st.session_state.app_mode = "plan"
                st.rerun()
        with d_cta2:
            if st.button("🗺️ Explore Places", key="disc_hero_explore", width="stretch"):
                st.session_state.app_mode = "explore"
                st.rerun()
        with d_cta3:
            if st.button("📖 Travel Guide", key="disc_hero_guide", type="primary", width="stretch"):
                st.session_state.app_mode = "guide"
                st.rerun()

    st.write("")

    disc_tabs = st.tabs([
        "🏛️ DESTINATIONS",
        "🍜 FOOD",
        "🛕 CULTURE",
        "👗 TRADITIONS",
        "✨ EXPERIENCES"
    ])

    # TAB 1: PLACES
    with disc_tabs[0]:
        st.markdown(
            f"""
            <div class="section-title">
                📍 FAMOUS PLACES IN {destination.upper()}
            </div>
            <div style="font-size: 14px; color: #94a3b8; margin-top: -6px; margin-bottom: 16px;">
                Hand-curated landmarks. Click <strong>Explore Details</strong> to reveal visitor tips, highlights, and prime visiting hours.
            </div>
            """,
            unsafe_allow_html=True
        )
        tourist_cards = get_tourist_cards(destination)
        if tourist_cards:
            place_columns = st.columns(3)
            for index, card in enumerate(tourist_cards):
                with place_columns[index % 3]:
                    show_image_card({**card, "country": destination}, "place")
        else:
            st.info(f"Explore the historic landmarks and scenic highlights across {destination}.")

    # TAB 2: LOCAL FOOD
    with disc_tabs[1]:
        st.markdown(
            f"""
            <div class="section-title">
                🍜 FAMOUS FOOD & CULINARY SPECIALTIES
            </div>
            <div style="font-size: 14px; color: #94a3b8; margin-top: -6px; margin-bottom: 16px;">
                Authentic regional dishes, street food delicacies, and traditional specialties with verified places to try them.
            </div>
            """,
            unsafe_allow_html=True
        )
        # City & Dietary filter controls
        f_col1, f_col2 = st.columns([1, 1])
        with f_col1:
            from destination_knowledge import CITY_FOOD_DATABASE
            avail_cities = sorted(list({c[1] for c in CITY_FOOD_DATABASE.keys() if c[0].lower() == destination.lower()}))
            city_filter_options = ["All Cities"] + avail_cities if avail_cities else ["All Cities"]
            selected_food_city = st.selectbox("🏙️ Filter by City / Region:", city_filter_options, key="disc_food_city_filter")
        with f_col2:
            diet_filter_options = ["All Diets", "🌱 Vegetarian", "🌿 Vegan", "🦐 Seafood", "🥩 Meat"]
            selected_diet = st.selectbox("🥗 Dietary Preference:", diet_filter_options, key="disc_food_diet_filter")

        target_city = None if selected_food_city == "All Cities" else selected_food_city
        food_cards = get_food_cards(destination, city=target_city)
        if selected_diet == "🌱 Vegetarian":
            food_cards = [c for c in food_cards if c.get("is_vegetarian") or c.get("is_vegan")]
        elif selected_diet == "🌿 Vegan":
            food_cards = [c for c in food_cards if c.get("is_vegan")]
        elif selected_diet == "🦐 Seafood":
            food_cards = [c for c in food_cards if c.get("contains_seafood")]
        elif selected_diet == "🥩 Meat":
            food_cards = [c for c in food_cards if c.get("contains_meat")]

        if food_cards:
            food_columns = st.columns(3)
            for index, card in enumerate(food_cards):
                with food_columns[index % 3]:
                    show_image_card({**card, "country": destination}, "food")
        else:
            st.info(f"No specific dishes matching your dietary filter for {selected_food_city or destination}. Try switching to 'All Diets'.")

    # TAB 3: TRADITIONAL ATTIRE
    with disc_tabs[2]:
        st.markdown(
            f"""
            <div class="section-title">
                👘 TRADITIONAL DRESSES & COSTS &bull; {destination.upper()} {profile['flag']}
            </div>
            <div style="font-size: 14px; color: #94a3b8; margin-top: -6px; margin-bottom: 16px;">
                Authentic heritage wear, native names, purchase costs in INR & local currency, daily rental rates, and recommended boutiques.
            </div>
            """,
            unsafe_allow_html=True
        )
        clothing_info = get_traditional_clothing(destination)
        raw_attires = clothing_info.get("attires") or [clothing_info.get("women"), clothing_info.get("men")]
        raw_attires = [a for a in raw_attires if a]
        women_list = [a for a in raw_attires if is_women_attire_dict(a)]
        men_list = [a for a in raw_attires if is_men_attire_dict(a)]
        reg_list = [a for a in raw_attires if a not in women_list and a not in men_list]
        primary_w = women_list[0] if women_list else None
        primary_m = men_list[0] if men_list else None
        remaining = (women_list[1:] if len(women_list) > 1 else []) + (men_list[1:] if len(men_list) > 1 else []) + reg_list
        attires = ([primary_w] if primary_w else []) + ([primary_m] if primary_m else []) + remaining

        used_registry = st.session_state.setdefault("used_destination_image_urls", set())
        for a in attires:
            att_gender = a.get("gender", "unisex")
            cur_img = a.get("image")
            if cur_img:
                if not is_valid_attire_image(a.get("name", ""), "", cur_img, a.get("name", ""), destination, gender=att_gender):
                    a["image"] = None
            if not a.get("image"):
                resolved_img = get_attire_image(
                    a.get("name"),
                    destination,
                    gender=att_gender,
                    exclude_images=tuple(used_registry)
                )
                if resolved_img:
                    a["image"] = resolved_img
            if a.get("image"):
                used_registry.add(a["image"])

        for idx in range(0, len(attires), 2):
            pair = attires[idx:idx + 2]
            cols = st.columns(len(pair))
            for c_idx, att in enumerate(pair):
                with cols[c_idx]:
                    with st.container(border=True):
                        badge = att.get("category", "👘 Traditional Attire")
                        st.markdown(
                            f"""<span style="background: rgba(236, 72, 153, 0.2); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.45); border-radius: 9999px; padding: 3px 12px; font-size: 11px; font-weight: 700;">{badge}</span>""",
                            unsafe_allow_html=True
                        )
                        img_url = att.get("image")
                        if img_url:
                            st.image(img_url, caption=att['name'], width="stretch")
                        else:
                            is_w = is_women_attire_dict(att)
                            is_m = is_men_attire_dict(att)
                            if is_w:
                                fb_title = "Authentic adult female attire photo unavailable"
                                fb_sub = f"Only verified authentic photographs of adult women wearing authentic traditional garments from {destination} are displayed."
                            elif is_m:
                                fb_title = "Authentic adult male attire photo unavailable"
                                fb_sub = f"Only verified authentic photographs of adult men wearing authentic traditional garments from {destination} are displayed."
                            else:
                                fb_title = "Authentic adult attire photo unavailable"
                                fb_sub = f"Only verified authentic photographs of adult subjects wearing authentic traditional garments from {destination} are displayed."
                            st.markdown(
                                f"""
                                <div style="background: rgba(15, 23, 42, 0.75); border: 1px dashed rgba(236, 72, 153, 0.45); border-radius: 10px; padding: 24px 14px; text-align: center; margin-bottom: 12px;">
                                    <div style="font-size: 26px; margin-bottom: 6px;">📸</div>
                                    <div style="font-weight: 700; color: #f472b6; font-size: 13px;">{fb_title}</div>
                                    <div style="color: #94a3b8; font-size: 11px; margin-top: 4px;">{fb_sub}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        st.markdown(f"### **{att['name']}**")
                        if att.get("local_name"):
                            st.markdown(f"**Native Script / Local Name:** `{att['local_name']}`")
                        if att.get("region"):
                            st.markdown(f"📍 **Region / Origin:** {att['region']}")
                        if att.get("description"):
                            st.write(att["description"])
                        if att.get("cultural_significance"):
                            st.markdown(f"🌟 **Cultural Significance:** {att['cultural_significance']}")
                        if att.get("fabrics"):
                            st.markdown(f"- **🧵 Authentic Fabrics:** {att['fabrics']}")
                        if att.get("cost_inr"):
                            st.markdown(f"- **💰 Estimated Purchase Cost (INR):** `{att['cost_inr']}`")
                        if att.get("cost_local"):
                            st.markdown(f"- **💵 Local Currency Cost:** `{att['cost_local']}`")
                        if att.get("rental_price"):
                            st.markdown(f"- **🏷️ Daily Rental Rate:** {att['rental_price']}")
                        if att.get("where_to_buy"):
                            st.markdown(f"- **🛍️ Recommended Shopping & Rental Spots:** {att['where_to_buy']}")

        if clothing_info.get("cultural_significance") or clothing_info.get("rental_note"):
            st.info(f"💡 **Cultural Heritage & Traveler Advice:** {clothing_info.get('cultural_significance', '')} {clothing_info.get('rental_note', '')}")

    # TAB 4: RELIGIOUS & CULTURE
    with disc_tabs[3]:
        st.markdown(
            f"""
            <div class="section-title">
                🎎 CULTURE, TEMPLES & SPIRITUAL HERITAGE IN {destination.upper()}
            </div>
            <div style="font-size: 14px; color: #94a3b8; margin-top: -6px; margin-bottom: 16px;">
                Sacred heritage, architectural treasures, festivals, and cultural etiquette in {destination}.
            </div>
            """,
            unsafe_allow_html=True
        )
        religious_cards = get_religious_cards(destination)
        if religious_cards:
            rel_cols = st.columns(3)
            for index, card in enumerate(religious_cards):
                with rel_cols[index % 3]:
                    show_image_card({**card, "country": destination}, "religious")

        st.markdown("---")
        st.markdown(
            f"""
            <div class="section-title">
                🕊️ 9-PILLAR CULTURAL TRADITIONS & LOCAL ETIQUETTE &bull; {destination.upper()}
            </div>
            <div style="font-size: 14px; color: #94a3b8; margin-top: -6px; margin-bottom: 16px;">
                Comprehensive behavioral guidelines, temple & shrine rituals, dining manners, transport courtesy, tipping customs, and community DOs & DONTs.
            </div>
            """,
            unsafe_allow_html=True
        )
        from destination_knowledge import get_destination_etiquette
        etq = get_destination_etiquette(destination)

        etq_col1, etq_col2, etq_col3 = st.columns(3)
        with etq_col1:
            with st.container(border=True):
                st.markdown("### 🤝 1. Greetings & Courtesy")
                g = etq.get("greetings", {})
                st.write(g.get("summary", ""))
                st.markdown(f"**How to Greet:** {g.get('action', '')}")
                if g.get("notes"):
                    st.caption(g["notes"])

            with st.container(border=True):
                st.markdown("### ⛩️ 4. Temples, Shrines & Sacred Sites")
                ts = etq.get("temples_and_shrines", {})
                st.write(ts.get("summary", ""))
                st.markdown(f"**Worship & Conduct:** {ts.get('action', '')}")
                if ts.get("notes"):
                    st.caption(ts["notes"])

            with st.container(border=True):
                st.markdown("### 📷 7. Photography & Respect")
                photo_etq = etq.get("photography", {})
                st.write(photo_etq.get("summary", ""))
                st.markdown(f"**Restrictions:** {photo_etq.get('action', '')}")
                if photo_etq.get("notes"):
                    st.caption(photo_etq["notes"])

        with etq_col2:
            with st.container(border=True):
                st.markdown("### 🥢 2. Dining & Table Manners")
                dm = etq.get("dining", {})
                st.write(dm.get("summary", ""))
                st.markdown(f"**Table Etiquette:** {dm.get('action', '')}")
                if dm.get("notes"):
                    st.caption(dm["notes"])

            with st.container(border=True):
                st.markdown("### 👟 5. Footwear & Shoe Removal")
                sr = etq.get("shoe_removal", {})
                st.write(sr.get("summary", ""))
                st.markdown(f"**Customs:** {sr.get('action', '')}")
                if sr.get("notes"):
                    st.caption(sr["notes"])

            with st.container(border=True):
                st.markdown("### 🏮 8. Celebrations & Festivals")
                fests = etq.get("festivals", [])
                if isinstance(fests, list):
                    for f in fests[:3]:
                        st.markdown(f"**🎉 {f.get('name', 'Festival')}** ({f.get('timing', '')})")
                        st.caption(f.get("cultural_note", ""))
                else:
                    st.write(str(fests))

        with etq_col3:
            with st.container(border=True):
                st.markdown("### 🚆 3. Public Transit Etiquette")
                pt = etq.get("public_transport", {})
                st.write(pt.get("summary", ""))
                st.markdown(f"**Transit Conduct:** {pt.get('action', '')}")
                if pt.get("notes"):
                    st.caption(pt["notes"])

            with st.container(border=True):
                st.markdown("### 🪙 6. Tipping Truth & Practices")
                tip = etq.get("tipping", {})
                st.write(tip.get("summary", ""))
                st.markdown(f"**Tipping Norm:** {tip.get('action', '')}")
                if tip.get("notes"):
                    st.caption(tip["notes"])

            with st.container(border=True):
                st.markdown("### 🏘️ 9. Community Respect (DOs & DONTs)")
                cr = etq.get("community_respect", {})
                st.write(cr.get("summary", ""))
                dos = cr.get("dos", [])
                donts = cr.get("donts", [])
                if dos:
                    st.markdown("**✅ DO:**")
                    for d in dos[:3]:
                        st.markdown(f"- {d}")
                if donts:
                    st.markdown("**❌ DON'T:**")
                    for nd in donts[:3]:
                        st.markdown(f"- {nd}")

        if etq.get("disclaimer"):
            st.info(f"💡 **Cultural Nuance & Respect:** {etq['disclaimer']}")

        # Practical Quick Advice
        tips_data = get_travel_tips(destination)
        if tips_data.get("currency_tips") or tips_data.get("best_season") or tips_data.get("safety"):
            with st.expander("💼 Additional Practical Details (Currency, Best Season & Health)"):
                tip_col1, tip_col2 = st.columns(2)
                with tip_col1:
                    if tips_data.get("currency_tips"):
                        st.markdown(f"**💵 Money & Currency Advice:**  \n{tips_data['currency_tips']}")
                    if tips_data.get("best_season"):
                        st.markdown(f"**🌤️ Best Season to Visit:**  \n{tips_data['best_season']}")
                with tip_col2:
                    if tips_data.get("safety"):
                        st.markdown(f"**🛡️ Health & Safety Advice:**  \n{tips_data['safety']}")

    # TAB 5: EXPERIENCES (Photo Gallery & Transit Tips)
    with disc_tabs[4]:
        st.markdown(
            f"""
            <div class="section-title">
                📸 DESTINATION PHOTO GALLERY &bull; {destination.upper()} {profile['flag']}
            </div>
            <div style="font-size: 14px; color: #94a3b8; margin-top: -6px; margin-bottom: 16px;">
                A showcase of iconic landmarks, celebrated cities, and natural wonders across {destination}.
            </div>
            """,
            unsafe_allow_html=True
        )
        gallery_items = get_destination_gallery_items(destination)
        if gallery_items:
            gal_cols = st.columns(3)
            for g_idx, g_item in enumerate(gallery_items):
                with gal_cols[g_idx % 3]:
                    show_gallery_card(destination, g_item)

        st.markdown("---")
        st.markdown(
            f"""
            <div class="section-title">
                🚆 TRANSPORTATION & CITY NAVIGATION IN {destination.upper()}
            </div>
            <div style="font-size: 14px; color: #94a3b8; margin-top: -6px; margin-bottom: 16px;">
                Airport arrivals, local transit, high-speed rail, regional passes, and expert navigation advice.
            </div>
            """,
            unsafe_allow_html=True
        )
        trans_data = get_transportation(destination)
        modes = trans_data.get("modes", []) if isinstance(trans_data, dict) else []
        trans_tips = trans_data.get("tips", "") if isinstance(trans_data, dict) else ""
        trans_pass = trans_data.get("pass", "") if isinstance(trans_data, dict) else ""

        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            with st.container(border=True):
                st.markdown("#### ✈️ Airport Arrivals")
                st.write(f"Direct international flights via main airports in {profile.get('capital', destination)}.")
                st.caption("Airport express trains, registered metered taxis, and official hotel transfer shuttles.")
        with t_col2:
            with st.container(border=True):
                st.markdown("#### 🚇 Local & City Transit")
                st.write(f"Subways, clean city buses, light rail, and walkable pedestrian streets across {destination}.")
                st.caption(f"Contactless travel passes: {trans_pass or 'Regional IC smartcards'}")
        with t_col3:
            with st.container(border=True):
                st.markdown("#### 🚅 Intercity & Regional")
                st.write(f"High-speed passenger rail, scenic tourist coaches, and regional connections.")
                st.caption(f"Advice: {trans_tips or 'Book long-distance tickets early for peak savings.'}")

        if modes:
            st.markdown("##### 🚗 Recommended Modes of Transit:")
            mode_cols = st.columns(min(len(modes), 4))
            for m_idx, m_name in enumerate(modes):
                with mode_cols[m_idx % len(mode_cols)]:
                    st.markdown(
                        f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 10px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); margin-bottom: 8px; text-align: center;">
                            <span style="font-size: 13px; font-weight: 600; color: #38bdf8;">✓ {html.escape(m_name)}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.write("")
    disc_nav1, disc_nav2, disc_nav3 = st.columns([1, 1.5, 1])
    with disc_nav1:
        if st.button("← 🌍 Back to Globe", key="disc_back_globe", width="stretch"):
            st.session_state.app_mode = "explore"
            st.rerun()
    with disc_nav2:
        if st.button("CONTINUE TO TRAVEL GUIDE →", key="disc_cont_guide", type="primary", width="stretch"):
            st.session_state.app_mode = "guide"
            st.rerun()
    with disc_nav3:
        if st.button("📅 View My Trip", key="disc_cont_itin", width="stretch"):
            st.session_state.app_mode = "itinerary"
            st.rerun()


# ============================================================
# PAGE 5: TRAVEL GUIDE (DYNAMIC & INTERACTIVE INTELLIGENCE)
# ============================================================

elif curr_mode == "guide":
    render_top_navigation("guide")

    st.markdown(
        f"""
        <div class="page-header-box">
            <span class="page-badge" style="background: rgba(14,165,233,0.2); color: #38bdf8; border: 1px solid rgba(14,165,233,0.4);">
                📖 CONVERSATIONAL TRAVEL GUIDE
            </span>
            <h1 class="page-title">TRAVEL GUIDE</h1>
            <p class="page-subtitle">Interactive destination advice, seasonal suggestions, traditional attire, and authentic discoveries.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    guide_display_name = get_assistant_name("guide")
    female_img = get_character_image("female")

    # Character Banner Card
    with st.container(border=True):
        g_c1, g_c2, g_c3 = st.columns([1.1, 2.5, 1.4])
        with g_c1:
            if female_img:
                st.image(female_img, width="stretch")
        with g_c2:
            st.markdown(
                f"""
                <div style="padding: 4px 0;">
                    <span class="hero-character-badge" style="margin-bottom: 6px;">🎒 {html.escape(guide_display_name)} &bull; Travel Guide</span>
                    <h3 style="margin: 4px 0 6px 0; color: #f8fafc;">Conversational Guide for {destination} {profile['flag']}</h3>
                    <p style="font-size: 13.5px; color: #cbd5e1; line-height: 1.5; margin: 0;">
                        I am your dedicated travel guide. Ask me where to travel, explore {destination}'s authentic sights, traditional attire, regional foods, seasonal weather, or tell me your travel month and budget for tailored ideas!
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with g_c3:
            guide_dest_list = CURATED_COUNTRIES if destination in CURATED_COUNTRIES else countries
            guide_idx = guide_dest_list.index(destination) if destination in guide_dest_list else 0
            new_guide_dest = st.selectbox(
                "🌍 Destination Focus:",
                guide_dest_list,
                index=guide_idx,
                key=f"guide_country_select_{destination}"
            )
            if new_guide_dest and new_guide_dest != destination:
                switch_country_and_regenerate(new_guide_dest)
                st.rerun()

    # Personalize Assistant Name Expander
    with st.expander(f"✨ Personalize Assistant Name (Currently: {guide_display_name})", expanded=False):
        g_rename_c1, g_rename_c2 = st.columns([3, 1])
        with g_rename_c1:
            new_g_name = st.text_input(
                "What would you like to call your travel assistant?",
                value=st.session_state.get("custom_assistant_name", ""),
                placeholder="e.g. Maya, Alex, Chinnu, Sofia...",
                key="guide_rename_input"
            )
        with g_rename_c2:
            st.write("")
            st.write("")
            if st.button("Save Name", key="guide_save_name_btn", width="stretch"):
                st.session_state["custom_assistant_name"] = new_g_name.strip()
                st.rerun()

    # Conversational Chat Section for Travel Guide
    st.markdown(f"### 💬 Chat with {guide_display_name}")
    st.caption("Ask questions by typing or speaking. You can ask where to go, request seasonal suggestions, inquire about traditional clothing, food, or attractions.")

    # Microphone Voice Input Controller
    render_speech_input_controller("guide_speech_mic")

    # Initialize guide chat history with friendly onboarding greeting if empty
    if "guide_chat_history" not in st.session_state or not isinstance(st.session_state.guide_chat_history, list):
        st.session_state.guide_chat_history = []

    if len(st.session_state.guide_chat_history) == 0:
        initial_greeting = get_conversational_onboarding_greeting(
            role_or_name="guide",
            destination=destination,
            assistant_name=guide_display_name,
            starting_location=st.session_state.get("starting_location", "")
        )
        st.session_state.guide_chat_history.append({"role": "assistant", "content": initial_greeting})

    # Quick Conversation Starters Chips
    st.markdown("<div style='font-size: 12.5px; color: #94a3b8; font-weight: 600; margin-bottom: 6px;'>💡 Quick Questions (Click to ask instantly):</div>", unsafe_allow_html=True)
    gq_cols1 = st.columns(4)
    guide_quick_trigger = None
    with gq_cols1[0]:
        if st.button("❄️ Where to travel in Dec?", key="gq_btn_dec", width="stretch"):
            guide_quick_trigger = "I don't know where to go in December. Can you recommend suitable destinations and explain why?"
    with gq_cols1[1]:
        if st.button("🌸 Best destinations for spring?", key="gq_btn_spring", width="stretch"):
            guide_quick_trigger = "What are the best destinations to visit during spring and why?"
    with gq_cols1[2]:
        if st.button("👘 Traditional clothing", key="gq_btn_attire", width="stretch"):
            guide_quick_trigger = f"Tell me about the traditional clothing and cultural dress of {destination}."
    with gq_cols1[3]:
        if st.button("🍜 Authentic food to try", key="gq_btn_food", width="stretch"):
            guide_quick_trigger = f"What authentic dishes and street foods should I try in {destination}?"

    gq_cols2 = st.columns(4)
    with gq_cols2[0]:
        if st.button("🗺️ Top 5 iconic places", key="gq_btn_places", width="stretch"):
            guide_quick_trigger = f"What are the top 5 must-visit attractions in {destination}?"
    with gq_cols2[1]:
        if st.button("🌤️ Weather & season", key="gq_btn_weather", width="stretch"):
            guide_quick_trigger = f"What is the typical weather and best season to visit {destination}?"
    with gq_cols2[2]:
        if st.button("💰 Budget & daily spend", key="gq_btn_budget", width="stretch"):
            guide_quick_trigger = f"What is the average daily budget and cost breakdown for {destination}?"
    with gq_cols2[3]:
        if st.button("🗑️ Clear Chat History", key="gq_btn_clear", width="stretch"):
            st.session_state.guide_chat_history = []
            st.rerun()

    # Process Quick Trigger
    if guide_quick_trigger:
        st.session_state.guide_chat_history.append({"role": "user", "content": guide_quick_trigger})
        with st.spinner(f"{guide_display_name} is typing..."):
            reply = answer_travel_question(
                destination,
                guide_quick_trigger,
                itinerary=plan,
                profile=profile,
                trip_context=trip_context,
                preferred_lang=st.session_state.get("asst_response_lang", "Auto Detect"),
                role="guide"
            )
        st.session_state.guide_chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    # Display Chat History with Voice Playback
    for g_idx, msg in enumerate(st.session_state.guide_chat_history):
        with st.chat_message(msg["role"]):
            clean_content = sanitize_chat_message_content(re.sub(r'<!-- SPEECH:[^>]+ -->', '', msg["content"]).strip())
            st.markdown(clean_content)
            if msg["role"] == "assistant":
                render_assistant_speech_controller(msg["content"], f"guide_speech_{g_idx}", default_lang="en-US")

    # Chat Input Box
    user_guide_msg = st.chat_input(f"Type your question or travel ideas for {guide_display_name}...", key="guide_text_chat_input")
    if user_guide_msg:
        st.session_state.guide_chat_history.append({"role": "user", "content": user_guide_msg})
        with st.chat_message("user"):
            st.markdown(user_guide_msg)
        with st.chat_message("assistant"):
            with st.spinner(f"{guide_display_name} is answering..."):
                reply = answer_travel_question(
                    destination,
                    user_guide_msg,
                    itinerary=plan,
                    profile=profile,
                    trip_context=trip_context,
                    preferred_lang=st.session_state.get("asst_response_lang", "Auto Detect"),
                    role="guide"
                )
                clean_reply = re.sub(r'<!-- SPEECH:[^>]+ -->', '', reply).strip()
                st.markdown(clean_reply)
                render_assistant_speech_controller(reply, f"guide_live_{len(st.session_state.guide_chat_history)}", default_lang="en-US")
        st.session_state.guide_chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    st.write("")
    st.markdown("---")
    st.markdown(f"### 📚 Curated Reference Guide for {destination}")
    st.caption("Deep-dive into verified destination attractions, culinary recommendations, cultural attire, budget breakdown, and transport:")

    # Interactive Guide Categories (8 requested in Section 5)
    categories = [
        ("Places", "🗺 Places"),
        ("Food", "🍜 Food"),
        ("Culture", "🏛 Culture"),
        ("Traditions", "👗 Traditions"),
        ("Budget", "💰 Budget"),
        ("Best Time", "🌤 Best Time"),
        ("Travel Tips", "🧳 Travel Tips"),
        ("Transport", "🚆 Transport")
    ]

    active_cat = st.session_state.get("guide_tab", "Places")
    cat_cols = st.columns(len(categories))
    for c_idx, (cat_key, cat_label) in enumerate(categories):
        with cat_cols[c_idx]:
            is_active_cat = (active_cat == cat_key)
            if st.button(
                cat_label,
                key=f"guide_cat_btn_{cat_key}",
                type="primary" if is_active_cat else "secondary",
                width="stretch"
            ):
                st.session_state.guide_tab = cat_key
                st.rerun()

    st.write("")

    # Dynamic Category Display
    if active_cat == "Places":
        st.markdown(f"### 🗺️ Top Tourist Attractions & Landmarks in {destination}")
        st.caption("Iconic must-see places with visitor tips, highlights, and prime visiting hours:")
        t_cards = get_tourist_cards(destination)
        if t_cards:
            p_cols = st.columns(3)
            for idx, card in enumerate(t_cards):
                with p_cols[idx % 3]:
                    show_image_card({**card, "country": destination}, "place")
        else:
            st.info(f"Top sightseeing destinations across {destination}.")

    elif active_cat == "Food":
        st.markdown(f"### 🍜 Authentic Food & Regional Specialties in {destination}")
        st.caption("Signature dishes, street food, and authentic spots to try them:")
        f_cards = get_food_cards(destination)
        if f_cards:
            f_cols = st.columns(3)
            for idx, card in enumerate(f_cards):
                with f_cols[idx % 3]:
                    show_image_card({**card, "country": destination}, "food")
        else:
            st.info(f"Delicious traditional culinary delicacies of {destination}.")

    elif active_cat == "Culture":
        st.markdown(f"### 🏛️ Cultural & Spiritual Heritage of {destination}")
        st.caption("Sacred sites, temples, architectural landmarks, and local etiquette:")
        religious_cards = get_religious_cards(destination)
        if religious_cards:
            c_cols = st.columns(3)
            for idx, card in enumerate(religious_cards):
                with c_cols[idx % 3]:
                    show_image_card({**card, "country": destination}, "religious")
        else:
            t_cards = get_tourist_cards(destination)
            if t_cards:
                c_cols = st.columns(3)
                for idx, card in enumerate(t_cards[:6]):
                    with c_cols[idx % 3]:
                        show_image_card({**card, "country": destination}, "religious")
            else:
                st.info(f"Explore the deep cultural and historical heritage of {destination}.")

    elif active_cat == "Traditions":
        st.markdown(f"### 👗 Traditional Attire & Costumes of {destination}")
        st.caption("Heritage garments, local names, fabrics, purchase costs, and daily rental options:")
        clothing_info = get_traditional_clothing(destination)
        raw_attires = clothing_info.get("attires") or [clothing_info.get("women"), clothing_info.get("men")]
        raw_attires = [a for a in raw_attires if a]
        women_list = [a for a in raw_attires if is_women_attire_dict(a)]
        men_list = [a for a in raw_attires if is_men_attire_dict(a)]
        reg_list = [a for a in raw_attires if a not in women_list and a not in men_list]
        primary_w = women_list[0] if women_list else None
        primary_m = men_list[0] if men_list else None
        remaining = (women_list[1:] if len(women_list) > 1 else []) + (men_list[1:] if len(men_list) > 1 else []) + reg_list
        attires = ([primary_w] if primary_w else []) + ([primary_m] if primary_m else []) + remaining

        used_reg = st.session_state.setdefault("used_destination_image_urls", set())
        for a in attires:
            att_gender = a.get("gender", "unisex")
            cur_img = a.get("image")
            if cur_img:
                if not is_valid_attire_image(a.get("name", ""), "", cur_img, a.get("name", ""), destination, gender=att_gender):
                    a["image"] = None
            if not a.get("image"):
                res_img = get_attire_image(a.get("name"), destination, gender=att_gender, exclude_images=tuple(used_reg))
                if res_img:
                    a["image"] = res_img
            if a.get("image"):
                used_reg.add(a["image"])
        for idx in range(0, len(attires), 2):
            pair = attires[idx:idx + 2]
            cols = st.columns(len(pair))
            for c_i, att in enumerate(pair):
                with cols[c_i]:
                    with st.container(border=True):
                        badge = att.get("category", "👘 Traditional Attire")
                        st.markdown(f"""<span style="background: rgba(236, 72, 153, 0.2); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.45); border-radius: 9999px; padding: 3px 12px; font-size: 11px; font-weight: 700;">{badge}</span>""", unsafe_allow_html=True)
                        if att.get("image"):
                            st.image(att["image"], caption=att.get("name"), width="stretch")
                        else:
                            is_w = is_women_attire_dict(att)
                            is_m = is_men_attire_dict(att)
                            if is_w:
                                fb_title = "Authentic adult female attire photo unavailable"
                                fb_sub = f"Only verified authentic photographs of adult women wearing authentic traditional garments from {destination} are displayed."
                            elif is_m:
                                fb_title = "Authentic adult male attire photo unavailable"
                                fb_sub = f"Only verified authentic photographs of adult men wearing authentic traditional garments from {destination} are displayed."
                            else:
                                fb_title = "Authentic adult attire photo unavailable"
                                fb_sub = f"Only verified authentic photographs of adult subjects wearing authentic traditional garments from {destination} are displayed."
                            st.markdown(
                                f"""
                                <div style="background: rgba(15, 23, 42, 0.75); border: 1px dashed rgba(236, 72, 153, 0.45); border-radius: 10px; padding: 22px 14px; text-align: center; margin-bottom: 12px;">
                                    <div style="font-size: 24px; margin-bottom: 4px;">📸</div>
                                    <div style="font-weight: 700; color: #f472b6; font-size: 13px;">{fb_title}</div>
                                    <div style="color: #94a3b8; font-size: 11px; margin-top: 4px;">{fb_sub}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        st.markdown(f"### {att.get('name')}")
                        if att.get("local_name"):
                            st.caption(f"Native Name: `{att['local_name']}`")
                        st.write(att.get("description", ""))
                        st.markdown(f"- **🧵 Authentic Fabrics:** {att.get('fabrics', 'Fine local fabrics')}")
                        st.markdown(f"- **💰 Estimated Purchase:** `{att.get('cost_inr', 'Varies')}`")
                        st.markdown(f"- **👘 Daily Rental Rate:** `{att.get('rental_price', 'Available near heritage sites')}`")
                        st.markdown(f"- **🛍️ Where to Find:** {att.get('where_to_buy', 'Central markets and tailors')}")

    elif active_cat == "Budget":
        st.markdown(f"### 💰 Budget Guide & Cost Breakdown for {destination}")
        st.caption("Smart financial planning guidelines based on real travel data:")
        c_meta_b = CURATED_30_DESTINATIONS.get(destination, {})
        est_day = c_meta_b.get("est_budget", "₹6,500 / day")
        curr_name = c_meta_b.get("currency", profile.get("currency", "Local Currency"))
        with st.container(border=True):
            b_c1, b_c2, b_c3 = st.columns(3)
            with b_c1:
                st.metric("💵 Average Daily Spend", est_day)
            with b_c2:
                st.metric("💱 Official Currency", curr_name)
            with b_c3:
                st.metric("💳 Suggested Trip Budget", f"₹{budget:,}")
        st.markdown("#### 📊 Budget Tiers & Spending Ranges:")
        tier_c1, tier_c2, tier_c3 = st.columns(3)
        with tier_c1:
            with st.container(border=True):
                st.markdown("##### 🎒 Budget / Backpacker")
                st.markdown("Hostels, street eats, public metro transit, and free attractions.")
                st.caption("Estimated: ~₹3,000 – ₹5,000 / day")
        with tier_c2:
            with st.container(border=True):
                st.markdown("##### 🧳 Mid-Range / Balanced")
                st.markdown("3-4★ Boutique hotels, casual dining, express trains, entry passes.")
                st.caption("Estimated: ~₹7,000 – ₹12,000 / day")
        with tier_c3:
            with st.container(border=True):
                st.markdown("##### 💎 Luxury / Premium")
                st.markdown("5★ Resorts, Michelin/fine dining, private drivers, guided VIP tours.")
                st.caption("Estimated: ~₹18,000+ / day")
        with st.expander("💡 Money-Saving Tips:"):
            st.markdown("- **Book Rail Passes Early:** Transport passes like regional bullet train passes save up to 40%.")
            st.markdown("- **Convenience Stores & Markets:** Authentic meals at local depachika or night markets offer gourmet tastes at great value.")
            st.markdown("- **Free Sightseeing:** Many temples, shrines, parks, and vantage points offer free entry.")

    elif active_cat == "Best Time":
        st.markdown(f"### 🌤️ Best Time to Visit {destination}")
        st.caption("Seasonal climate patterns, festivals, and optimal traveling periods:")
        c_meta_s = CURATED_30_DESTINATIONS.get(destination, {})
        b_season = c_meta_s.get("best_season") or profile.get("best_time") or "Spring & Autumn"
        with st.container(border=True):
            st.markdown(f"#### 🌸 Peak Recommendation: **{b_season}**")
            st.caption("Ideal temperatures, clear skies, and vibrant seasonal festivities.")
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                st.markdown("**🌱 Spring (March–May)**")
                st.caption("Mild weather, blooming flowers, pleasant strolls.")
            with s_col2:
                st.markdown("**☀️ Summer (June–August)**")
                st.caption("Festivals, beach getaways, lively nightlife, and outdoor hikes.")
            with s_col3:
                st.markdown("**🍁 Autumn (Sept–Nov)**")
                st.caption("Crisp air, colorful foliage, prime photography conditions.")

    elif active_cat == "Travel Tips":
        st.markdown(f"### 🧳 Practical Travel Tips for {destination}")
        st.caption("Essential recommendations, cultural norms, packing lists, and connectivity advice:")
        tips = get_travel_tips(destination)
        if tips:
            t_grid = st.columns(2)
            tips_items = []
            if isinstance(tips, dict):
                for k, v in tips.items():
                    tips_items.append(f"{k.capitalize()}: {v}")
            elif isinstance(tips, list):
                tips_items = tips
            for t_idx, tip_item in enumerate(tips_items[:6]):
                with t_grid[t_idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"**💡 {tip_item}**")
        with st.expander("🎒 Recommended Packing Essentials:"):
            st.markdown("- **Footwear:** Comfortable walking shoes for cobblestones, temples, and long sightseeing days.")
            st.markdown("- **Adapters & Power:** Universal travel plug adapter and high-capacity portable power bank.")
            st.markdown("- **Documents:** Digital copies of passport, travel insurance, hotel bookings, and offline maps.")

    elif active_cat == "Transport":
        st.markdown(f"### 🚆 Transportation Guide for {destination}")
        st.caption("Navigating the destination via rail, subway, intercity coaches, and taxis:")
        trans = get_transportation(destination)
        if isinstance(trans, dict):
            modes = trans.get("modes", [])
            tips_t = trans.get("tips", "")
            pass_t = trans.get("pass", "")
        else:
            modes = ["Metro / Subway", "High-Speed Rail", "City Buses", "Taxis & Rideshare"]
            tips_t = "Purchase a contactless transit card at the airport station."
            pass_t = "Look for multi-day tourist transit passes."
        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            with st.container(border=True):
                st.markdown("#### ✈️ Airport Arrivals")
                st.caption(f"Express train links and direct airport coaches connect to downtown {destination}.")
        with t_col2:
            with st.container(border=True):
                st.markdown("#### 🚇 City Transit & Subway")
                st.caption(f"Contactless transit cards: {pass_t or 'IC Smartcards'}")
        with t_col3:
            with st.container(border=True):
                st.markdown("#### 🚅 High-Speed & Regional")
                st.caption(f"Advice: {tips_t or 'Reserve express seats ahead during peak seasons.'}")
        if modes:
            st.markdown("##### Recommended Transit Modes:")
            m_cols = st.columns(min(len(modes), 4))
            for m_i, m_name in enumerate(modes):
                with m_cols[m_i % len(m_cols)]:
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:8px 12px; border-radius:8px; text-align:center; font-weight:600; color:#38bdf8;'>✓ {m_name}</div>", unsafe_allow_html=True)

    # Action Footer
    st.write("")
    g_nav1, g_nav2, g_nav3 = st.columns([1, 1.5, 1])
    with g_nav1:
        if st.button("← ✨ Back to Discover", key="guide_back_disc", width="stretch"):
            st.session_state.app_mode = "discover"
            st.rerun()
    with g_nav2:
        if st.button("CONTINUE TO MY TRIP →", key="guide_cont_itin", type="primary", width="stretch"):
            st.session_state.app_mode = "itinerary"
            st.rerun()
    with g_nav3:
        if st.button("🤖 Ask Travel Companion", key="guide_go_asst", width="stretch"):
            st.session_state.app_mode = "companion"
            st.rerun()


# ============================================================
# PAGE 5: MY TRIP (DASHBOARD, VISUAL BUDGET & DAY-BY-DAY)
# ============================================================

elif curr_mode == "itinerary":
    render_top_navigation("itinerary")

    multi_plan = st.session_state.get("multi_stop_plan")

    if multi_plan and multi_plan.get("stops"):
        # ========================================================
        # MULTI-STOP ORDERED JOURNEY DISPLAY
        # ========================================================
        st.markdown(
            f"""
            <div class="page-header-box">
                <span class="page-badge" style="background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.4);">
                    🗺️ MULTI-STOP ORDERED JOURNEY PLAN
                </span>
                <h1 class="page-title">{html.escape(multi_plan.get('route_title', 'Multi-City Journey'))}</h1>
                <p class="page-subtitle">{multi_plan.get('total_days', 7)} Total Days &bull; {multi_plan.get('travelers', 1)} Traveler(s) &bull; Origin & Return: {html.escape(multi_plan.get('origin', 'Hyderabad'))} &bull; {multi_plan.get('style', 'Balanced')} Rhythm</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Control Switcher: Edit or Clear Multi-Stop
        m_ctl1, m_ctl2 = st.columns([3, 1.2])
        with m_ctl1:
            st.info(f"✨ Currently viewing ordered multi-stop journey across {len(multi_plan['stops'])} destinations ({multi_plan.get('destination_stay_days', multi_plan.get('total_days'))} destination stay days).")
        with m_ctl2:
            if st.button("🔀 Edit Stops in Planner", key="itin_edit_multi_stops_btn", width="stretch"):
                st.session_state.app_mode = "plan"
                st.rerun()

        # Pre-Render 8-Point Route Validation Banner
        val_rep = multi_plan.get("validation_report", {})
        if val_rep:
            if val_rep.get("is_valid", True):
                st.success(f"✅ **Pre-Render Verification Passed ({val_rep.get('passed_checks', 8)}/{val_rep.get('total_checks', 8)} Checks):** Route sequence, requested stay durations, independent transport corridors, location-specific sights, and budget breakdown are 100% verified.")
            else:
                st.warning("⚠️ **Route Validation Advisory:** One or more journey parameters require review.")

        # Multi-Stop Budget Dashboard
        cost_bd = multi_plan.get("cost_breakdown", {})
        with st.container(border=True):
            st.markdown("### 💳 Multi-Stop Budget & Expense Breakdown")
            st.caption("Estimated budget distribution across all transportation legs, accommodation stays, dining, and sightseeing:")

            mb_c1, mb_c2, mb_c3, mb_c4, mb_c5, mb_c6 = st.columns(6)
            with mb_c1:
                st.metric("🏨 Accommodations", f"₹{cost_bd.get('Accommodation', int(multi_plan['budget'] * 0.35)):,}")
            with mb_c2:
                st.metric("🚆 All Transit Legs", f"₹{cost_bd.get('Intercity Transport', int(multi_plan['budget'] * 0.28)):,}")
            with mb_c3:
                st.metric("🍜 Dining & Food", f"₹{cost_bd.get('Dining', int(multi_plan['budget'] * 0.18)):,}")
            with mb_c4:
                st.metric("🎟️ Sightseeing", f"₹{cost_bd.get('Activities', int(multi_plan['budget'] * 0.14)):,}")
            with mb_c5:
                st.metric("💰 Total Estimated", f"₹{cost_bd.get('Total Estimated', int(multi_plan['budget'] * 0.95)):,}")
            with mb_c6:
                st.metric("💵 Buffer Remaining", f"₹{cost_bd.get('Buffer Remaining', int(multi_plan['budget'] * 0.05)):,}")

        st.write("")

        # Ordered Transportation Legs
        st.markdown("### 🚆 Transportation Legs & Route Connections")
        st.caption("Detailed recommendations for each leg: modes, estimated travel times, stations/terminals, buffer times, and booking links:")

        for l_idx, leg in enumerate(multi_plan.get("transport_legs", [])):
            leg_orig = leg.get("origin", "")
            leg_dest = leg.get("destination", "")
            leg_mode = leg.get("mode", "Transit")
            leg_time = leg.get("travel_time", "N/A")
            leg_cost = leg.get("cost_range", "N/A")
            leg_o_term = leg.get("origin_terminal", "Central Station / Airport")
            leg_d_term = leg.get("dest_terminal", "Central Station / Airport")
            leg_conn = leg.get("connection_info", "")
            leg_buf = leg.get("buffer_time", "1 hour")
            leg_link = leg.get("booking_link", "")

            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 8px;">
                        <div>
                            <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-weight: 700; padding: 3px 10px; border-radius: 999px; font-size: 11px;">
                                LEG {l_idx + 1}
                            </span>
                            <span style="font-size: 17px; font-weight: 800; color: #f8fafc; margin-left: 8px;">
                                {html.escape(leg_orig)} &rarr; {html.escape(leg_dest)}
                            </span>
                        </div>
                        <div>
                            <span style="background: rgba(16, 185, 129, 0.15); color: #34d399; font-weight: 700; padding: 4px 12px; border-radius: 8px; font-size: 12.5px;">
                                {html.escape(leg_cost)}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                t_leg_c1, t_leg_c2, t_leg_c3 = st.columns(3)
                with t_leg_c1:
                    st.markdown(f"**🚆 Recommended Mode:**  \n{leg_mode}")
                    st.markdown(f"⏱️ **Journey Time:** `{leg_time}`")
                with t_leg_c2:
                    st.markdown(f"📍 **Departure Terminal:**  \n{leg_o_term}")
                    st.markdown(f"🏁 **Arrival Terminal:**  \n{leg_d_term}")
                with t_leg_c3:
                    st.markdown(f"ℹ️ **Connection Notes:**  \n{leg_conn}")
                    st.markdown(f"⏳ **Buffer / Rest:** `{leg_buf}`")

                if leg_link:
                    st.markdown(f"🔗 **Official Schedule & Booking:** [{leg_link}]({leg_link})")

        st.write("")

        # Multi-Stop Day-by-Day Schedule Grouped by Stop
        st.markdown(f"### 📅 Destination Stops & Day-by-Day Schedule (Total {multi_plan.get('total_days')} Days)")

        for s_idx, stop in enumerate(multi_plan.get("stops", [])):
            s_city = stop.get("city", "")
            s_country = stop.get("country", "")
            s_days = stop.get("days", 1)
            s_drange = stop.get("day_range", f"Days")
            s_plan = stop.get("days_plan", [])

            with st.expander(f"📍 STOP {s_idx + 1}: {s_city.upper()}, {s_country.upper()} &bull; {s_days} Days ({s_drange})", expanded=(s_idx == 0)):
                st.caption(f"Curated morning, afternoon, and evening exploration for {s_city}:")

                for d_info in s_plan:
                    d_num = d_info.get("day_num", 1)
                    d_title = d_info.get("title", f"Exploring {s_city}")
                    st.markdown(f"#### 🗓️ Day {d_num}: {d_title}")
                    if d_info.get("etiquette_tip"):
                        st.info(f"💡 **Cultural Etiquette Tip:** {d_info['etiquette_tip']}")

                    for act in d_info.get("activities", []):
                        slot = act.get("time", "Time")
                        act_n = act.get("activity", "Sightseeing")
                        act_p = act.get("place", s_city)
                        act_c = act.get("cost", 0)
                        act_t = act.get("travel_time", "20 min")
                        act_m = act.get("transport", "Local transit")
                        period = "🌅 Morning" if "09:" in slot or "08:" in slot else ("☀️ Afternoon" if "13:" in slot or "14:" in slot else "🌙 Evening")

                        st.markdown(
                            f"""
                            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                    <span style="font-size: 12px; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.12); padding: 2px 8px; border-radius: 6px;">{period} &bull; {html.escape(slot)}</span>
                                    <span style="font-size: 12px; font-weight: 700; color: #34d399;">₹{act_c:,}</span>
                                </div>
                                <div style="font-size: 15px; font-weight: 800; color: #f8fafc; margin-bottom: 2px;">{html.escape(act_n)}</div>
                                <div style="font-size: 12.5px; color: #94a3b8;">
                                    📍 <strong>Spot:</strong> {html.escape(act_p)} &bull; ⏱️ <strong>Transit:</strong> {html.escape(str(act_t))} &bull; 🚆 <strong>Transit:</strong> {html.escape(str(act_m))}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        # Clear or reset multi-stop plan
        st.write("")
        if st.button("🗑️ Revert to Single-Destination Planner", key="revert_single_dest_btn"):
            st.session_state.multi_stop_plan = None
            st.rerun()

    else:
        # ========================================================
        # SINGLE-DESTINATION ITINERARY DISPLAY
        # ========================================================
        st.markdown(
            f"""
            <div class="page-header-box">
                <span class="page-badge" style="background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.4);">
                    📅 TRAVEL DASHBOARD &bull; STEP 4
                </span>
                <h1 class="page-title">MY {destination.upper()} JOURNEY {profile['flag']}</h1>
                <p class="page-subtitle">{days} Days &bull; {travelers} Traveler{'s' if travelers > 1 else ''} &bull; {style} Rhythm &bull; Starting from {starting_location}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # VISUAL BUDGET DASHBOARD
        with st.container(border=True):
            st.markdown("### 💳 Estimated Trip Budget")
            st.caption("Real-time allocation calculated by the intelligent budget engine:")

            budget_data = plan.get("budget", {}) if plan else {}
            b_acc = budget_data.get("Accommodation", int(budget * 0.35))
            b_trans = budget_data.get("Intercity / Transport", budget_data.get("Transport", int(budget * 0.18)))
            b_food = budget_data.get("Food & Dining", budget_data.get("Food", int(budget * 0.20)))
            b_act = budget_data.get("Activities & Sightseeing", budget_data.get("Activities", int(budget * 0.22)))

            b_c1, b_c2, b_c3, b_c4, b_c5, b_c6 = st.columns(6)
            with mb_c1 if 'mb_c1' in locals() else b_c1:
                st.metric("🏨 Accommodation", f"₹{b_acc:,}")
            with b_c2:
                st.metric("🍜 Food & Dining", f"₹{b_food:,}")
            with b_c3:
                st.metric("🚆 Transport", f"₹{b_trans:,}")
            with b_c4:
                st.metric("🎟️ Activities", f"₹{b_act:,}")
            with b_c5:
                st.metric("💰 Total Estimated", f"₹{total_cost:,}")
            with b_c6:
                st.metric("💵 Buffer Remaining", f"₹{remaining_budget:,}")

        st.write("")
        st.markdown(f"### 📅 Day-by-Day Journey Schedule (Day 1 to Day {days})")

        # Render day cards with Morning, Afternoon, Evening hierarchy
        for day in plan.get("days", []):
            d_num = day.get("day", 1)
            d_title = day.get("title", f"Exploring {destination}")
            d_acts = day.get("activities", [])

            with st.expander(f"📍 DAY {d_num:02d}: {d_title}", expanded=(d_num <= 3)):
                if day.get("etiquette_tip"):
                    st.info(f"💡 **Cultural Etiquette Tip:** {day['etiquette_tip']}")
                if not d_acts:
                    st.info("No specific activities scheduled for this day.")
                else:
                    for a_idx, act in enumerate(d_acts):
                        time_slot = act.get("time", "")
                        period = "🌅 Morning" if "09:" in time_slot or "08:" in time_slot or "10:" in time_slot else ("☀️ Afternoon" if "13:" in time_slot or "14:" in time_slot or "15:" in time_slot else "🌙 Evening")
                        act_name = act.get("activity", "Sightseeing")
                        act_place = act.get("place", destination)
                        act_cost = act.get("cost", 0)
                        act_travel = act.get("travel_time", "20 min")
                        act_transit = act.get("transport") or ("🚄 High-speed rail" if "Kyoto" in act_name or "intercity" in act_name.lower() else "🚇 Local metro / transit")

                        st.markdown(
                            f"""
                            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px 18px; margin-bottom: 12px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <span style="font-size: 13px; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.12); padding: 3px 10px; border-radius: 8px;">{period} &bull; {html.escape(time_slot)}</span>
                                    <span style="font-size: 13px; font-weight: 700; color: #34d399;">₹{act_cost:,}</span>
                                </div>
                                <div style="font-size: 16px; font-weight: 800; color: #f8fafc; margin-bottom: 4px;">{html.escape(act_name)}</div>
                                <div style="font-size: 13px; color: #94a3b8;">
                                    📍 <strong>Location:</strong> {html.escape(act_place)} &bull; ⏱️ <strong>Transit:</strong> {html.escape(str(act_travel))} &bull; 🚆 <strong>Mode:</strong> {html.escape(str(act_transit))}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        # Itinerary Fine-Tuning Container
        st.write("")
        with st.container(border=True):
            st.markdown("### 🛠️ Fine-Tune & Modify Your Itinerary")
            st.caption("Tell the AI planner how to customize this schedule (e.g. relax Day 4, reduce budget, add cultural activities, focus on food):")

            ft_cols = st.columns(4)
            quick_mod = None
            with ft_cols[0]:
                if st.button("🛋️ Make Day 4 more relaxing", key="mod_btn_relax", width="stretch"):
                    quick_mod = "Make Day 4 more relaxing with leisurely activities"
            with ft_cols[1]:
                if st.button("💵 Reduce activity costs", key="mod_btn_budget", width="stretch"):
                    quick_mod = "Reduce activity costs to optimize budget"
            with ft_cols[2]:
                if st.button("🎎 Add cultural activities", key="mod_btn_culture", width="stretch"):
                    quick_mod = "Replace shopping with more cultural activities and heritage landmarks"
            with ft_cols[3]:
                if st.button("🍜 More food experiences", key="mod_btn_food", width="stretch"):
                    quick_mod = "Add authentic regional food walks and local culinary tastings"

            req_col, req_btn_col = st.columns([4, 1])
            with req_col:
                mod_request = st.text_input(
                    "Custom modification request:",
                    value=quick_mod or "",
                    placeholder="Example: Change Day 3 afternoon to visit art museums, or decrease total budget by 10%",
                    key="itinerary_modification_input"
                )
            with req_btn_col:
                st.write("")
                st.write("")
                if st.button("🔄 Update Plan", width="stretch", key="itin_update_plan_btn", type="primary"):
                    active_req = (mod_request or quick_mod or "").strip()
                    if not active_req:
                        st.warning("Please enter or select a modification request.")
                    else:
                        with st.spinner("Updating your personalized itinerary..."):
                            st.session_state.itinerary = update_itinerary(
                                st.session_state.itinerary,
                                active_req,
                                budget,
                                destination,
                                interests
                            )
                        st.success("Your itinerary has been updated!")
                        st.rerun()

    st.write("")
    itin_nav1, itin_nav2 = st.columns([1, 2])
    with itin_nav1:
        if st.button("← 📖 Back to Travel Guide", key="itin_back_guide", width="stretch"):
            st.session_state.app_mode = "guide"
            st.rerun()
    with itin_nav2:
        if st.button("CONTINUE TO TRAVEL COMPANION →", key="itin_cont_companion", type="primary", width="stretch"):
            st.session_state.app_mode = "companion"
            st.rerun()


# ============================================================
# PAGE 7: TRAVEL COMPANION (TRIP-AWARE AI ASSISTANT)
# ============================================================

elif curr_mode in ("companion", "assistant"):
    render_top_navigation("companion")

    companion_display_name = get_assistant_name("companion")
    male_img = get_character_image("male")

    st.markdown(
        f"""
        <div class="page-header-box">
            <span class="page-badge" style="background: rgba(99,102,241,0.25); color: #818cf8; border: 1px solid rgba(99,102,241,0.5);">
                🤖 AI TRAVEL COMPANION
            </span>
            <h1 class="page-title">{html.escape(companion_display_name)} &bull; Travel Intelligence Companion</h1>
            <p class="page-subtitle">Multi-stop journey routing, transport advice, visas, connectivity, accommodations, and real-time support.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Character Banner Card
    with st.container(border=True):
        ac_c1, ac_c2 = st.columns([1.1, 3.5])
        with ac_c1:
            if male_img:
                st.image(male_img, width="stretch")
        with ac_c2:
            st.markdown(
                f"""
                <div style="padding: 4px 0;">
                    <span class="hero-character-badge" style="background: rgba(99,102,241,0.2); border-color: rgba(99,102,241,0.5); color: #818cf8; margin-bottom: 6px;">
                        🤖 {html.escape(companion_display_name)} &bull; AI Travel Companion
                    </span>
                    <h3 style="margin: 4px 0 6px 0; color: #f8fafc;">Your 24/7 Travel & Route Navigator</h3>
                    <p style="font-size: 13.5px; color: #cbd5e1; line-height: 1.5; margin: 0;">
                        I help you plan multi-city itineraries, compare transportation options (bullet trains, flights, local transit), understand visas, find dietary meals (halal, vegan, gluten-free), handle delays, and manage your budget.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Personalize Assistant Name Expander
    with st.expander(f"✨ Personalize Assistant Name (Currently: {companion_display_name})", expanded=False):
        c_rename_c1, c_rename_c2 = st.columns([3, 1])
        with c_rename_c1:
            new_c_name = st.text_input(
                "What would you like to call your travel assistant?",
                value=st.session_state.get("custom_assistant_name", ""),
                placeholder="e.g. Alex, Maya, Chinnu, Atlas...",
                key="companion_rename_input"
            )
        with c_rename_c2:
            st.write("")
            st.write("")
            if st.button("Save Name", key="companion_save_name_btn", width="stretch"):
                st.session_state["custom_assistant_name"] = new_c_name.strip()
                st.rerun()

    # Active Multi-Stop Journey Banner (if active)
    multi_plan_active = st.session_state.get("multi_stop_plan")
    if multi_plan_active and multi_plan_active.get("stops"):
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span style="background: rgba(16,185,129,0.2); color: #34d399; font-weight: 700; padding: 3px 10px; border-radius: 999px; font-size: 11px;">
                            Active Multi-Stop Plan
                        </span>
                        <div style="font-weight: 800; color: #f8fafc; font-size: 15px; margin-top: 4px;">
                            🗺️ {multi_plan_active.get('route_title', 'Multi-Stop Journey')} ({multi_plan_active.get('total_days', 7)} Days)
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("📅 View & Edit Multi-Stop Itinerary →", key="comp_jump_multi_btn", type="primary"):
                st.session_state.app_mode = "itinerary"
                st.rerun()

    # Trip Snapshot Card
    with st.container(border=True):
        tc_col1, tc_col2 = st.columns([1.5, 2.5])
        with tc_col1:
            st.markdown(
                f"""
                <div style="font-size: 15px; font-weight: 800; color: #f8fafc;">
                    🗺️ Active Journey Context
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 2px;">
                    AI Companion is synchronized with your trip parameters:
                </div>
                """,
                unsafe_allow_html=True
            )
        with tc_col2:
            st.markdown(
                f"""
                <div style="background: rgba(15,23,42,0.6); padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-size: 12.5px; color: #cbd5e1;">
                    📍 <strong>{destination} {profile['flag']}</strong> &bull; 📅 {days} Days &bull; 👥 {travelers} Travelers &bull; 🧳 {style} &bull; 💰 ₹{budget:,} &bull; ❤️ {interests_str}
                </div>
                """,
                unsafe_allow_html=True
            )

    # Control Bar: Language Selector & Clear Chat
    asst_ctrl_c1, asst_ctrl_c2 = st.columns([3, 1.2])
    with asst_ctrl_c1:
        SUPPORTED_LANGS = [
            "Auto Detect", "English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam",
            "Bengali", "Marathi", "Gujarati", "Punjabi", "Urdu", "French", "Spanish",
            "German", "Italian", "Japanese", "Korean", "Chinese", "Arabic", "Portuguese", "Russian", "Thai"
        ]
        cur_sel_lang = st.session_state.get("asst_response_lang", "Auto Detect")
        sel_lang_idx = SUPPORTED_LANGS.index(cur_sel_lang) if cur_sel_lang in SUPPORTED_LANGS else 0
        selected_lang = st.selectbox(
            "🌐 Response Language (Auto Detect or Choose):",
            SUPPORTED_LANGS,
            index=sel_lang_idx,
            key="asst_response_lang_selector"
        )
        st.session_state["asst_response_lang"] = selected_lang

    with asst_ctrl_c2:
        st.write("")
        st.write("")
        if st.button("🗑️ Clear Chat History", key="asst_clear_chat_btn", width="stretch"):
            st.session_state.chat_history = []
            st.rerun()

    # Microphone Voice Input Controller
    render_speech_input_controller("companion_speech_mic")

    # Suggested Questions Across 16+ Domains
    st.markdown("<div style='font-size: 13px; color: #94a3b8; font-weight: 600; margin-bottom: 6px;'>💡 Suggested Questions Across Travel Domains (Click to ask instantly):</div>", unsafe_allow_html=True)
    
    sq_row1 = st.columns(4)
    fp_quick_trigger = None
    with sq_row1[0]:
        if st.button("✈️ Multi-stop: Hyd to Japan", key="fp_btn_q1", width="stretch"):
            fp_quick_trigger = "I will start from Hyderabad on December 10. I want to travel to Japan, stay in Tokyo for 2 days, then go to Kyoto for 3 days, then visit Osaka for 2 days, and finally return to Hyderabad. Recommend the route, transportation, and a complete itinerary."
    with sq_row1[1]:
        if st.button("🛂 Visa & entry requirements", key="fp_btn_q2", width="stretch"):
            fp_quick_trigger = f"What are the visa and passport entry requirements for Indian travelers visiting {destination}?"
    with sq_row1[2]:
        if st.button("📱 SIM card, eSIM & apps", key="fp_btn_q3", width="stretch"):
            fp_quick_trigger = f"What is the best way to get mobile connectivity, SIM cards or eSIM, and useful navigation apps in {destination}?"
    with sq_row1[3]:
        if st.button("🏨 Accommodations & costs", key="fp_btn_q4", width="stretch"):
            fp_quick_trigger = f"Where should I stay in {destination} and what are the approximate hotel and hostel costs?"

    sq_row2 = st.columns(4)
    with sq_row2[0]:
        if st.button("🥗 Vegan & Halal food", key="fp_btn_q5", width="stretch"):
            fp_quick_trigger = f"Can I easily find vegetarian, vegan, and halal food options in {destination}? What are practical tips?"
    with sq_row2[1]:
        if st.button("⚠️ Flight/Train delay tips", key="fp_btn_q6", width="stretch"):
            fp_quick_trigger = f"What should I do if my flight or train is delayed or if I miss a connection while traveling in {destination}?"
    with sq_row2[2]:
        if st.button("♿ Accessibility & family", key="fp_btn_q7", width="stretch"):
            fp_quick_trigger = f"Is {destination} accessible for stroller, elderly, or wheelchair travelers? What are accessibility tips?"
    with sq_row2[3]:
        if st.button("💰 Budget-saving tips", key="fp_btn_q8", width="stretch"):
            fp_quick_trigger = f"How can I save money, optimize transit passes, and reduce daily costs in {destination}?"

    preferred_lang = st.session_state.get("asst_response_lang", "Auto Detect")

    if fp_quick_trigger:
        st.session_state.chat_history.append({"role": "user", "content": fp_quick_trigger})
        with st.spinner(f"{companion_display_name} is answering..."):
            ai_reply = answer_travel_question(
                destination,
                fp_quick_trigger,
                itinerary=plan,
                profile=profile,
                trip_context=trip_context,
                preferred_lang=preferred_lang,
                role="companion"
            )
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.rerun()

    # Render Chat History
    for msg_idx, msg in enumerate(st.session_state.chat_history):
        with st.chat_message(msg["role"]):
            clean_text = sanitize_chat_message_content(re.sub(r'<!-- SPEECH:[^>]+ -->', '', msg["content"]).strip())
            st.markdown(clean_text)
            if msg["role"] == "assistant":
                render_assistant_speech_controller(msg["content"], f"asst_page_{msg_idx}", default_lang="en-US")

    # User Chat Input
    user_chat_query_fp = st.chat_input(f"Ask {companion_display_name} about routes, visas, transit, packing, accommodations, or languages...", key="asst_chat_input_box")
    if user_chat_query_fp:
        st.session_state.chat_history.append({"role": "user", "content": user_chat_query_fp})
        with st.chat_message("user"):
            st.markdown(user_chat_query_fp)

        with st.chat_message("assistant"):
            with st.spinner("Answering from local travel intelligence..."):
                ai_reply = answer_travel_question(
                    destination,
                    user_chat_query_fp,
                    itinerary=plan,
                    profile=profile,
                    trip_context=trip_context,
                    preferred_lang=preferred_lang,
                    role="companion"
                )
                clean_ai_reply = re.sub(r'<!-- SPEECH:[^>]+ -->', '', ai_reply).strip()
                st.markdown(clean_ai_reply)
                render_assistant_speech_controller(ai_reply, f"asst_live_{len(st.session_state.chat_history)}", default_lang="en-US")

        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.rerun()

    st.write("")
    asst_nav1, asst_nav2 = st.columns([1, 2])
    with asst_nav1:
        if st.button("← 📅 Back to Itinerary", key="asst_back_itin", width="stretch"):
            st.session_state.app_mode = "itinerary"
            st.rerun()
    with asst_nav2:
        if st.button("CONTINUE TO SAFETY & EMERGENCY →", key="asst_cont_safety", type="primary", width="stretch"):
            st.session_state.app_mode = "safety"
            st.rerun()


# ============================================================
# PAGE 8: SAFETY & EMERGENCY (VERIFIED DIRECTORY & GUIDANCE)
# ============================================================

elif curr_mode == "safety":
    render_top_navigation("safety")

    st.markdown(
        f"""
        <div class="page-header-box">
            <span class="page-badge" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);">
                🛡️ VERIFIED OFFICIAL SAFETY DIRECTORY
            </span>
            <h1 class="page-title">Safety & Emergency Information</h1>
            <p class="page-subtitle">Reliably verified emergency contacts, official authorities, and local safety rules &bull; {destination.upper()} {profile['flag']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Destination Selector for Emergency Information
    s_col_sel, s_col_info = st.columns([1.5, 2.5])
    with s_col_sel:
        safety_dest_list = CURATED_COUNTRIES if destination in CURATED_COUNTRIES else countries
        s_idx = safety_dest_list.index(destination) if destination in safety_dest_list else 0
        s_new_dest = st.selectbox(
            "🌍 Select Country for Emergency Contacts:",
            safety_dest_list,
            index=s_idx,
            key=f"safety_country_select_{destination}"
        )
        if s_new_dest and s_new_dest != destination:
            switch_country_and_regenerate(s_new_dest)
            st.rerun()

    with s_col_info:
        em_info = get_verified_emergency_info(destination)
        st.markdown(
            f"""
            <div style="background: rgba(15,23,42,0.65); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 16px; margin-top: 6px;">
                <div style="font-size: 13px; font-weight: 700; color: #38bdf8;">Official Source Citation:</div>
                <div style="font-size: 12.5px; color: #cbd5e1; margin-top: 2px;">{em_info.get('source', 'Official Government Tourism and Emergency Services')}</div>
                <div style="font-size: 11.5px; color: #94a3b8; margin-top: 3px;"><a href="{em_info.get('source_url', '#')}" target="_blank" style="color:#38bdf8; text-decoration:underline;">Visit Official Source Portal ↗</a></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Emergency Numbers Grid (4 Cards)
    st.markdown("### 🚨 Primary Emergency Hotlines")
    st.caption("Call these numbers immediately in case of emergency. GSM digital mobile phones can also dial universal emergency standard 112.")

    em_c1, em_c2, em_c3, em_c4 = st.columns(4)
    with em_c1:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="text-align: center; padding: 8px 4px;">
                    <div style="font-size: 30px;">👮</div>
                    <div style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-top: 4px;">Police</div>
                    <div style="font-size: 24px; font-weight: 900; color: #38bdf8; font-family: monospace; margin: 6px 0;">{em_info.get('police', '112')}</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Law enforcement & immediate danger</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with em_c2:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="text-align: center; padding: 8px 4px;">
                    <div style="font-size: 30px;">🚑</div>
                    <div style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-top: 4px;">Medical / Ambulance</div>
                    <div style="font-size: 24px; font-weight: 900; color: #ef4444; font-family: monospace; margin: 6px 0;">{em_info.get('ambulance', '112')}</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Acute injury & hospital dispatch</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with em_c3:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="text-align: center; padding: 8px 4px;">
                    <div style="font-size: 30px;">🚒</div>
                    <div style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-top: 4px;">Fire & Rescue</div>
                    <div style="font-size: 24px; font-weight: 900; color: #f59e0b; font-family: monospace; margin: 6px 0;">{em_info.get('fire', '112')}</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Fire fighting & disaster rescue</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with em_c4:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="text-align: center; padding: 8px 4px;">
                    <div style="font-size: 30px;">🌐</div>
                    <div style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-top: 4px;">Tourist Helpline</div>
                    <div style="font-size: 16px; font-weight: 900; color: #10b981; font-family: monospace; margin: 10px 0;">{em_info.get('tourist_assistance', '112')}</div>
                    <div style="font-size: 11.5px; color: #cbd5e1;">Multilingual traveler support</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # Practical Local Safety Advice
    st.markdown("### 🦺 Practical Safety & Local Etiquette")
    saf_col1, saf_col2 = st.columns(2)

    with saf_col1:
        with st.container(border=True):
            st.markdown("#### 🚕 Transport & Taxi Safety")
            st.markdown("- **Licensed Vehicles:** Only hail registered metered cabs or book using verified mobile ride-hailing apps.")
            st.markdown("- **Airport Arrivals:** Avoid unmetered independent drivers in arrival halls; use designated official taxi stands or airport express trains.")
            st.markdown(f"- **Transit smartcards:** Use contactless cards ({get_transportation(destination).get('pass', 'regional IC smartcards')}) to eliminate carrying large cash amounts.")

        with st.container(border=True):
            st.markdown("#### 💧 Food, Water & Health Precaution")
            st.markdown("- **Drinking Water:** Verify if tap water is potable in this destination. When in doubt, choose sealed bottled or filtered water.")
            st.markdown("- **Travel Pharmacy:** Keep personal prescriptions with doctor notes in original packaging; carry oral rehydration salts and basic antacids.")
            st.markdown("- **Travel Insurance:** Save digital and printed copies of your international medical assistance policy.")

    with saf_col2:
        with st.container(border=True):
            st.markdown("#### 📜 Local Laws, Customs & Scams to Avoid")
            tips_d = get_travel_tips(destination)
            st.markdown(f"- **Social Etiquette:** {tips_d.get('etiquette', 'Respect religious sites, dress modestly covering knees and shoulders, and maintain quiet in residential areas.')}")
            st.markdown(f"- **Tipping & Currency:** {tips_d.get('tipping', 'Check local customs on service gratuities.')} {tips_d.get('currency_tips', '')}")
            st.markdown("- **Belongings Awareness:** Keep passports, wallets, and phones secure in crowded metro cars and tourist viewpoints.")

        with st.container(border=True):
            st.markdown("#### 🗣️ Essential Emergency Phrases (Local Language)")
            phrases = em_info.get("local_phrases", [("Help me please!", "Help me please!", "Universal emergency phrase")])
            dest_voice_code = get_destination_voice_code(destination)
            for p_idx, (roman, script, meaning) in enumerate(phrases):
                st.markdown(f"- **{script}** (*{roman}*) &bull; Meaning: **{meaning}**")
                render_assistant_speech_controller(script, f"saf_phrase_{p_idx}", default_lang=dest_voice_code)

    st.write("")
    s_nav1, s_nav2 = st.columns([1, 2])
    with s_nav1:
        if st.button("← 🤖 Back to AI Companion", key="safety_back_comp", width="stretch"):
            st.session_state.app_mode = "companion"
            st.rerun()
    with s_nav2:
        if st.button("CONTINUE TO SAVED PLACES →", key="safety_cont_saved", type="primary", width="stretch"):
            st.session_state.app_mode = "saved"
            st.rerun()


# ============================================================
# PAGE 9: SAVED PLACES (FUNCTIONAL FAVORITES & TRIP STASH)
# ============================================================

elif curr_mode == "saved":
    render_top_navigation("saved")

    saved_items = st.session_state.get("saved_places", [])

    st.markdown(
        f"""
        <div class="page-header-box">
            <span class="page-badge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4);">
                🔖 MY SAVED EXPERIENCES &bull; {len(saved_items)} PLACES
            </span>
            <h1 class="page-title">Saved Places & Favorites</h1>
            <p class="page-subtitle">Handpicked landmarks, authentic dining spots, and cultural treasures saved across your journey.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not saved_items:
        with st.container(border=True):
            st.markdown(
                """
                <div style="text-align: center; padding: 48px 20px;">
                    <div style="font-size: 48px; margin-bottom: 12px;">🔖</div>
                    <div style="font-size: 20px; font-weight: 800; color: #f8fafc; margin-bottom: 6px;">Your Saved Places is Empty</div>
                    <div style="font-size: 14px; color: #94a3b8; max-width: 520px; margin: 0 auto 20px auto;">
                        As you browse destinations on the 3D Globe, Discover feed, or Travel Guide, click <strong>"🔖 Save Place"</strong> to stash attractions and foods here for quick access.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            emp_c1, emp_c2 = st.columns(2)
            with emp_c1:
                if st.button("🌍 Explore the 3D Globe", key="saved_emp_globe", type="primary", width="stretch"):
                    st.session_state.app_mode = "explore"
                    st.rerun()
            with emp_c2:
                if st.button("✨ Discover Highlights", key="saved_emp_disc", width="stretch"):
                    st.session_state.app_mode = "discover"
                    st.rerun()

    else:
        top_ctrl1, top_ctrl2 = st.columns([4, 1.2])
        with top_ctrl1:
            st.markdown(f"**You have {len(saved_items)} saved place{'s' if len(saved_items) > 1 else ''}:**")
        with top_ctrl2:
            if st.button("🗑️ Clear All Saved", key="saved_clear_all_btn", width="stretch"):
                st.session_state.saved_places = []
                st.rerun()

        st.write("")
        saved_cols = st.columns(3)
        for s_idx, item in enumerate(saved_items):
            s_name = item.get("name", "Attraction")
            s_country = item.get("country", destination)
            s_type = item.get("type", "place")
            s_loc = item.get("location", s_country)
            s_desc = item.get("description", f"Explore {s_name} in {s_country}.")

            with saved_cols[s_idx % 3]:
                with st.container(border=True):
                    s_img_bytes, _ = get_card_image_bytes(s_country, s_name, s_type, location=s_loc)
                    if s_img_bytes:
                        st.image(s_img_bytes, width="stretch")
                    else:
                        st.markdown(
                            f"""
                            <div style="background: rgba(15, 23, 42, 0.75); border: 1px dashed rgba(56, 189, 248, 0.5); border-radius: 10px; padding: 28px 12px; text-align: center; margin-bottom: 8px;">
                                <div style="font-size: 28px; margin-bottom: 4px;">🏛️</div>
                                <div style="font-weight: 700; color: #38bdf8; font-size: 13px;">{s_name}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown(f"#### {s_name}")
                    st.caption(f"📍 {s_loc} &bull; {get_country_flag(s_country)} {s_country} &bull; *{s_type.title()}*")
                    st.write(s_desc[:160] + ("..." if len(s_desc) > 160 else ""))

                    act_c1, act_c2 = st.columns(2)
                    with act_c1:
                        if st.button("➕ Add to Trip", key=f"saved_add_itin_{s_idx}_{abs(hash(s_name)) % 100000}", width="stretch"):
                            if add_place_to_itinerary(s_name, s_country, target_day=1):
                                st.success(f"Added {s_name} to Day 1!")
                            else:
                                st.info("Generate your trip plan in Plan My Trip first.")
                    with act_c2:
                        if st.button("🗑️ Remove", key=f"saved_del_{s_idx}_{abs(hash(s_name)) % 100000}", width="stretch"):
                            st.session_state.saved_places.pop(s_idx)
                            st.rerun()

    st.write("")
    sv_nav1, sv_nav2 = st.columns([1, 2])
    with sv_nav1:
        if st.button("← 🛡️ Back to Safety", key="saved_back_safety", width="stretch"):
            st.session_state.app_mode = "safety"
            st.rerun()
    with sv_nav2:
        if st.button("CONTINUE TO TRIP SUMMARY →", key="saved_cont_summary", type="primary", width="stretch"):
            st.session_state.app_mode = "summary"
            st.rerun()


# ============================================================
# PAGE 10: TRIP SUMMARY (EXECUTIVE BLUEPRINT)
# ============================================================

elif curr_mode == "summary":
    render_top_navigation("summary")

    multi_plan_sum = st.session_state.get("multi_stop_plan")

    if multi_plan_sum and multi_plan_sum.get("stops"):
        st.markdown(
            f"""
            <div class="page-header-box" style="text-align: center; padding: 32px 20px;">
                <span class="page-badge" style="background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.4); font-size: 13px; font-weight: 700; letter-spacing: 1.5px;">
                    ✨ MULTI-STOP TRIP READY
                </span>
                <h1 class="page-title" style="font-size: 34px; margin-top: 14px; margin-bottom: 8px;">
                    {html.escape(multi_plan_sum.get('route_title', 'Multi-Stop Journey'))}
                </h1>
                <div style="font-size: 16px; color: #cbd5e1; font-weight: 600; margin-bottom: 12px;">
                    {multi_plan_sum.get('total_days', 7)} Days Across {len(multi_plan_sum.get('stops', []))} Destinations &bull; {multi_plan_sum.get('travelers', 1)} Traveler(s) &bull; {multi_plan_sum.get('style', 'Balanced')}
                </div>
                <div style="display: inline-block; background: rgba(30,41,59,0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 999px; padding: 6px 18px; color: #38bdf8; font-weight: 600; font-size: 14px;">
                    🛫 Origin & Final Return: {html.escape(multi_plan_sum.get('origin', 'Hyderabad'))}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        c_meta = CURATED_30_DESTINATIONS.get(destination, {})
        flag_emoji = c_meta.get("flag", profile.get("flag", "🌍"))
        cities_route = " → ".join(c_meta.get("cities", profile.get("cities", [destination]))[:4])
        interests_formatted = " · ".join([i.capitalize() for i in interests]) if isinstance(interests, list) else str(interests)

        st.markdown(
            f"""
            <div class="page-header-box" style="text-align: center; padding: 32px 20px;">
                <span class="page-badge" style="background: rgba(56,189,248,0.18); color: #38bdf8; border: 1px solid rgba(56,189,248,0.4); font-size: 13px; font-weight: 700; letter-spacing: 1.5px;">
                    ✨ YOUR TRIP IS READY
                </span>
                <h1 class="page-title" style="font-size: 38px; margin-top: 14px; margin-bottom: 8px;">
                    {flag_emoji} {destination.upper()}
                </h1>
                <div style="font-size: 16px; color: #cbd5e1; font-weight: 600; margin-bottom: 12px;">
                    {days} Days &bull; {travelers} Traveller{'s' if travelers > 1 else ''} &bull; {style}
                </div>
                <div style="display: inline-block; background: rgba(30,41,59,0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 999px; padding: 6px 18px; color: #38bdf8; font-weight: 600; font-size: 14px;">
                    📍 {cities_route}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Core Summary Card
    with st.container(border=True):
        sc1, sc2, sc3 = st.columns(3)
        if multi_plan_sum and multi_plan_sum.get("stops"):
            cost_bd_s = multi_plan_sum.get("cost_breakdown", {})
            with sc1:
                st.markdown(
                    f"""
                    <div style="padding: 12px 6px;">
                        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px;">Estimated Total Budget</div>
                        <div style="font-size: 26px; font-weight: 800; color: #34d399; margin-top: 4px;">₹{multi_plan_sum.get('budget', 150000):,}</div>
                        <div style="font-size: 12px; color: #cbd5e1; margin-top: 2px;">Estimated Total: ₹{cost_bd_s.get('Total Estimated', int(multi_plan_sum['budget'] * 0.95)):,} &bull; Buffer: ₹{cost_bd_s.get('Buffer Remaining', int(multi_plan_sum['budget'] * 0.05)):,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with sc2:
                st.markdown(
                    f"""
                    <div style="padding: 12px 6px;">
                        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px;">Route & Destinations</div>
                        <div style="font-size: 18px; font-weight: 700; color: #f8fafc; margin-top: 4px;">{len(multi_plan_sum['stops'])} Stops &bull; {multi_plan_sum['total_days']} Days</div>
                        <div style="font-size: 12px; color: #38bdf8; margin-top: 2px;">{html.escape(multi_plan_sum.get('route_title', 'Route'))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with sc3:
                st.markdown(
                    f"""
                    <div style="padding: 12px 6px;">
                        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px;">Transportation Summary</div>
                        <div style="font-size: 18px; font-weight: 700; color: #c084fc; margin-top: 4px;">{len(multi_plan_sum.get('transport_legs', []))} Intercity Legs</div>
                        <div style="font-size: 12px; color: #cbd5e1; margin-top: 2px;">Flights, High-Speed Trains & Express Transit</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            with sc1:
                st.markdown(
                    f"""
                    <div style="padding: 12px 6px;">
                        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px;">Estimated Budget</div>
                        <div style="font-size: 26px; font-weight: 800; color: #34d399; margin-top: 4px;">₹{budget:,}</div>
                        <div style="font-size: 12px; color: #cbd5e1; margin-top: 2px;">Allocated: ₹{total_cost:,} &bull; Buffer: ₹{remaining_budget:,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with sc2:
                st.markdown(
                    f"""
                    <div style="padding: 12px 6px;">
                        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px;">Route & Duration</div>
                        <div style="font-size: 20px; font-weight: 700; color: #f8fafc; margin-top: 4px;">{days} Days Across {destination}</div>
                        <div style="font-size: 12px; color: #38bdf8; margin-top: 2px;">{cities_route}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with sc3:
                st.markdown(
                    f"""
                    <div style="padding: 12px 6px;">
                        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px;">Selected Interests</div>
                        <div style="font-size: 16px; font-weight: 700; color: #c084fc; margin-top: 6px;">{interests_formatted}</div>
                        <div style="font-size: 12px; color: #cbd5e1; margin-top: 2px;">Departing: {starting_location}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.write("")

    # Primary Action Buttons as requested in Section 13
    btn_c1, btn_c2, btn_c3, btn_c4 = st.columns(4)
    with btn_c1:
        if st.button("View Full Itinerary", key="sum_go_itin", type="primary", width="stretch"):
            st.session_state.app_mode = "itinerary"
            st.rerun()
    with btn_c2:
        if st.button("Modify Trip", key="sum_go_plan", width="stretch"):
            st.session_state.app_mode = "plan"
            st.rerun()
    with btn_c3:
        if st.button("Ask AI Companion", key="sum_go_asst", width="stretch"):
            st.session_state.app_mode = "companion"
            st.rerun()
    with btn_c4:
        if st.button("🛡️ Safety & Helplines", key="sum_go_safety", width="stretch"):
            st.session_state.app_mode = "safety"
            st.rerun()

    st.write("")

    # 4 Structured Highlights
    sum_h1, sum_h2 = st.columns(2)

    with sum_h1:
        if multi_plan_sum and multi_plan_sum.get("stops"):
            with st.container(border=True):
                st.markdown("### 📍 Ordered Stops & Stay Durations")
                for s_i, stop in enumerate(multi_plan_sum.get("stops", [])):
                    st.markdown(f"- **Stop {s_i + 1}: {stop['city']}, {stop['country']}** ({stop['days']} Days &bull; {stop.get('day_range', '')})")
                    c_info = CURATED_30_DESTINATIONS.get(stop['country'], {})
                    st.caption(f"Highlights: {', '.join(c_info.get('highlights', ['Cultural landmarks'])[:3])}")
        else:
            with st.container(border=True):
                st.markdown("### 📍 Top Places to Visit")
                t_cards = get_tourist_cards(destination)
                if t_cards:
                    for tc in t_cards[:4]:
                        st.markdown(f"- **{tc.get('name', 'Attraction')}** ({tc.get('location', destination)})")
                        st.caption(tc.get("description", ""))
                else:
                    st.caption(f"Iconic highlights across {destination}.")

            with st.container(border=True):
                st.markdown("### 👘 Cultural & Attire Highlights")
                cl_info = get_traditional_clothing(destination)
                att_list = cl_info.get("attires") or [cl_info.get("women"), cl_info.get("men")]
                att_list = [a for a in att_list if a]
                for a in att_list[:2]:
                    st.markdown(f"- **{a.get('name', 'Attire')}** (`{a.get('local_name', '')}`)")
                    st.caption(f"Purchase: {a.get('cost_inr', 'Varies')} | Daily Rental: {a.get('rental_price', 'Available near sites')}")
                if cl_info.get("cultural_significance"):
                    st.caption(f"🌟 {cl_info['cultural_significance']}")

    with sum_h2:
        if multi_plan_sum and multi_plan_sum.get("stops"):
            with st.container(border=True):
                st.markdown("### 🚆 Transit Connections & Corridors")
                for l_i, leg in enumerate(multi_plan_sum.get("transport_legs", [])):
                    st.markdown(f"- **Leg {l_i + 1}: {leg['origin']} ➔ {leg['destination']}**")
                    st.caption(f"{leg['mode']} &bull; ~{leg['travel_time']} &bull; {leg['cost_range']}")
        else:
            with st.container(border=True):
                st.markdown("### 🍜 Must-Try Culinary Specialties")
                f_cards = get_food_cards(destination)
                if f_cards:
                    for fc in f_cards[:4]:
                        st.markdown(f"- **{fc.get('name', 'Dish')}**")
                        where = fc.get("where_to_try") or get_where_to_try(destination, fc.get("name", ""))
                        st.caption(f"Best spot: {where}")
                else:
                    st.caption(f"Authentic local food in {destination}.")

            with st.container(border=True):
                st.markdown("### 📅 Day-by-Day Route Overview")
                for day in plan.get("days", [])[:6]:
                    st.markdown(f"- **Day {day['day']}:** {day.get('title', 'Exploration')}")
                if len(plan.get("days", [])) > 6:
                    st.caption(f"&bull; ... and {len(plan.get('days', [])) - 6} additional days detailed in the full itinerary.")

    # Secondary Navigation
    st.write("")
    sum_sub1, sum_sub2 = st.columns(2)
    with sum_sub1:
        if st.button("🌍 Explore Another Destination", key="sum_go_explore", width="stretch"):
            st.session_state.app_mode = "explore"
            st.rerun()
    with sum_sub2:
        if st.button("🏠 Back to Home", key="sum_go_home", width="stretch"):
            st.session_state.app_mode = "landing"
            st.rerun()