from copy import deepcopy
import re


# ============================================================
# SAMPLE TRAVEL DATA
# ============================================================

COUNTRIES = {
    "Japan": {
        "flag": "🇯🇵",
        "duration": "7–10 days",
        "budget": "₹60k–₹1.8L",
        "season": "March–May / October–November",
        "places": [
            "Tokyo",
            "Kyoto",
            "Osaka",
            "Mount Fuji"
        ],
        "food": [
            "Sushi",
            "Ramen",
            "Tempura",
            "Okonomiyaki"
        ],
        "transport": [
            "Shinkansen",
            "Metro",
            "Local trains"
        ],
        "experiences": [
            "Mount Fuji",
            "Kyoto temples",
            "Tokyo city tour",
            "Traditional food experience"
        ],
        "activities": {
            "Tokyo": [
                ("09:00", "Tokyo city exploration", "Tokyo", 1500, 30),
                ("14:00", "Asakusa & Senso-ji", "Asakusa", 800, 25),
                ("19:00", "Ramen dinner", "Tokyo", 1200, 20)
            ],
            "Kyoto": [
                ("09:00", "Fushimi Inari Shrine", "Kyoto", 500, 30),
                ("14:00", "Kiyomizu-dera & Higashiyama", "Kyoto", 1000, 25),
                ("19:00", "Traditional Kyoto dinner", "Kyoto", 1800, 20)
            ],
            "Osaka": [
                ("10:00", "Osaka Castle", "Osaka", 900, 25),
                ("15:00", "Dotonbori food walk", "Osaka", 1600, 20),
                ("19:00", "Shopping at Shinsaibashi", "Osaka", 1000, 15)
            ],
            "Mount Fuji": [
                ("08:00", "Mount Fuji & Lake Kawaguchiko [Day Trip: 2h 15m travel time each way via Fuji Excursion Express]", "Kawaguchiko", 2500, 135),
                ("14:00", "Lake Kawaguchi Panoramic Photography & Oishi Park [Day Trip]", "Kawaguchiko", 1000, 30),
                ("18:00", "Return to Tokyo via Express Highway Bus / Train [Day Trip Return]", "Tokyo", 3000, 135)
            ]
        }
    },

    "India": {
        "flag": "🇮🇳",
        "duration": "4–10 days",
        "budget": "₹15k–₹1L",
        "season": "October–March",
        "places": [
            "Hyderabad",
            "Jaipur",
            "Goa",
            "Kerala"
        ],
        "food": [
            "Biryani",
            "Dosa",
            "Thali",
            "Seafood"
        ],
        "transport": [
            "Trains",
            "Buses",
            "Flights",
            "Metro"
        ],
        "experiences": [
            "Heritage walks",
            "Beaches",
            "Local food",
            "Nature"
        ],
        "activities": {
            "Hyderabad": [
                ("09:00", "Charminar & old city", "Hyderabad", 500, 25),
                ("14:00", "Golconda Fort", "Hyderabad", 700, 30),
                ("19:00", "Hyderabadi biryani", "Hyderabad", 500, 15)
            ],
            "Jaipur": [
                ("09:00", "Amber Fort", "Jaipur", 1000, 35),
                ("14:00", "City Palace", "Jaipur", 800, 25),
                ("19:00", "Local Rajasthani dinner", "Jaipur", 700, 20)
            ],
            "Goa": [
                ("09:00", "Beach morning", "Goa", 300, 20),
                ("14:00", "Portuguese heritage walk", "Goa", 700, 30),
                ("19:00", "Seafood dinner", "Goa", 900, 20)
            ],
            "Kerala": [
                ("09:00", "Backwater experience", "Alappuzha", 1500, 30),
                ("14:00", "Nature photography", "Alappuzha", 500, 20),
                ("19:00", "Kerala dinner", "Alappuzha", 700, 15)
            ]
        }
    },

    "France": {
        "flag": "🇫🇷",
        "duration": "5–10 days",
        "budget": "₹70k–₹2L",
        "season": "April–June / September–October",
        "places": [
            "Paris",
            "Eiffel Tower",
            "Louvre Museum",
            "Nice",
            "Lyon",
            "Versailles"
        ],
        "food": [
            "Croissant",
            "Crêpes",
            "Cheese",
            "French pastries"
        ],
        "transport": [
            "Metro",
            "TGV",
            "Tram",
            "Regional trains"
        ],
        "experiences": [
            "Eiffel Tower",
            "Louvre",
            "French food tour",
            "Seine cruise"
        ],
        "activities": {
            "Paris": [
                ("09:00", "Eiffel Tower area", "Paris", 2500, 25),
                ("14:00", "Louvre Museum", "Paris", 3000, 25),
                ("19:00", "French food experience", "Paris", 2500, 20)
            ],
            "Nice": [
                ("09:00", "Promenade des Anglais", "Nice", 800, 20),
                ("14:00", "Old Nice exploration", "Nice", 1000, 20),
                ("19:00", "Mediterranean dinner", "Nice", 2200, 15)
            ],
            "Lyon": [
                ("09:00", "Old Lyon walk", "Lyon", 700, 20),
                ("14:00", "Local food tour", "Lyon", 1800, 20),
                ("19:00", "Riverside evening", "Lyon", 500, 15)
            ],
            "Versailles": [
                ("09:00", "Palace of Versailles", "Versailles", 2500, 45),
                ("14:00", "Gardens", "Versailles", 500, 15),
                ("18:00", "Return to Paris", "Paris", 1000, 45)
            ]
        }
    },

    "Italy": {
        "flag": "🇮🇹",
        "duration": "6–12 days",
        "budget": "₹65k–₹1.8L",
        "season": "April–June / September–October",
        "places": [
            "Rome",
            "Florence",
            "Venice",
            "Milan"
        ],
        "food": [
            "Pizza",
            "Pasta",
            "Gelato",
            "Risotto"
        ],
        "transport": [
            "High-speed trains",
            "Metro",
            "Trams",
            "Water buses"
        ],
        "experiences": [
            "Colosseum",
            "Venice canals",
            "Tuscan food",
            "Renaissance art"
        ],
        "activities": {
            "Rome": [
                ("09:00", "Colosseum", "Rome", 2500, 25),
                ("14:00", "Roman Forum", "Rome", 1200, 15),
                ("19:00", "Italian dinner", "Rome", 1800, 20)
            ],
            "Florence": [
                ("09:00", "Duomo", "Florence", 1500, 20),
                ("14:00", "Uffizi area", "Florence", 2000, 20),
                ("19:00", "Tuscan dinner", "Florence", 1800, 15)
            ],
            "Venice": [
                ("09:00", "Grand Canal", "Venice", 1200, 25),
                ("14:00", "St Mark's Square", "Venice", 1000, 20),
                ("19:00", "Venetian dinner", "Venice", 2000, 20)
            ],
            "Milan": [
                ("09:00", "Duomo", "Milan", 1500, 20),
                ("14:00", "Galleria shopping", "Milan", 1000, 15),
                ("19:00", "Milanese dinner", "Milan", 1800, 20)
            ]
        }
    },

    "Thailand": {
        "flag": "🇹🇭",
        "duration": "5–10 days",
        "budget": "₹30k–₹1L",
        "season": "November–February",
        "places": [
            "Bangkok",
            "Phuket",
            "Chiang Mai",
            "Krabi"
        ],
        "food": [
            "Pad Thai",
            "Tom Yum",
            "Mango sticky rice",
            "Green curry"
        ],
        "transport": [
            "Metro",
            "Tuk-tuk",
            "Ferries",
            "Domestic flights"
        ],
        "experiences": [
            "Thai temples",
            "Beaches",
            "Street food",
            "Island trips"
        ],
        "activities": {
            "Bangkok": [
                ("09:00", "Grand Palace", "Bangkok", 1000, 25),
                ("14:00", "Wat Arun", "Bangkok", 500, 20),
                ("19:00", "Street food tour", "Bangkok", 1000, 15)
            ],
            "Phuket": [
                ("09:00", "Beach morning", "Phuket", 500, 20),
                ("14:00", "Island viewpoint", "Phuket", 800, 30),
                ("19:00", "Thai seafood dinner", "Phuket", 1200, 20)
            ],
            "Chiang Mai": [
                ("09:00", "Old city temples", "Chiang Mai", 500, 20),
                ("14:00", "Local market", "Chiang Mai", 700, 15),
                ("19:00", "Thai cooking experience", "Chiang Mai", 1800, 20)
            ],
            "Krabi": [
                ("09:00", "Railay Beach", "Krabi", 800, 30),
                ("14:00", "Island experience", "Krabi", 1500, 45),
                ("19:00", "Beach dinner", "Krabi", 1000, 20)
            ]
        }
    }
}


import json
import os

_COUNTRIES_DATA_CACHE = None

def _get_local_countries_db():
    global _COUNTRIES_DATA_CACHE
    if _COUNTRIES_DATA_CACHE is not None:
        return _COUNTRIES_DATA_CACHE

    paths = [
        os.path.join(os.path.dirname(__file__), "countries_data.json"),
        os.path.join(os.getcwd(), "countries_data.json"),
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    _COUNTRIES_DATA_CACHE = json.load(f)
                    return _COUNTRIES_DATA_CACHE
            except Exception:
                pass
    _COUNTRIES_DATA_CACHE = {}
    return _COUNTRIES_DATA_CACHE


# ============================================================
# COUNTRY INFORMATION
# ============================================================

def country_info(country):
    try:
        from country_data import get_country_knowledge
        knowledge = get_country_knowledge(country)
        canonical = knowledge.get("name", country)
        places = list(knowledge.get("cities", [canonical]))
        
        foods_raw = knowledge.get("food", [])
        food_list = [f[0] if isinstance(f, (tuple, list)) else str(f) for f in foods_raw]
        
        transport_modes = list(knowledge.get("transportation", {}).get("modes", ["Local transit", "Trains", "Buses", "Flights"]))
        
        experiences = [
            f"Iconic landmark discovery in {places[0] if places else canonical}",
            f"Historic & cultural heritage exploration in {places[1] if len(places) > 1 else places[0]}",
            f"Scenic nature & regional landscape discovery",
            f"Authentic local culinary tasting ({food_list[0] if food_list else 'regional dishes'})",
            f"Traditional artisan markets & neighborhood walking tour"
        ]
        
        # Build activities per city
        activities = {}
        attractions_list = knowledge.get("attractions", [])
        
        for c_idx, city in enumerate(places):
            city_attractions = [
                a[0] for a in attractions_list 
                if isinstance(a, (tuple, list)) and len(a) > 1 and (a[1].lower() in city.lower() or city.lower() in a[1].lower())
            ]
            if not city_attractions:
                city_attractions = [
                    f"{city} Historic Center & Landmark Plaza",
                    f"{city} Cultural Heritage Museum & Old Town"
                ]
                    
            p1 = city_attractions[0]
            p2 = city_attractions[1] if len(city_attractions) > 1 else f"{city} Cultural Museum & Historic Quarter"
            dish = food_list[c_idx % len(food_list)] if food_list else "authentic regional cuisine"
            
            activities[city] = [
                ("09:00", f"Explore {p1}", city, 800, 30),
                ("14:00", f"Visit {p2}", city, 600, 25),
                ("19:00", f"Enjoy authentic {dish} in {city}", city, 1100, 20)
            ]
            
        info_data = {
            "flag": knowledge.get("flag", "🌍"),
            "duration": knowledge.get("duration", "7–14 days"),
            "budget": knowledge.get("budget", "₹50k–₹1.5L"),
            "season": knowledge.get("season", "Spring and autumn are ideal"),
            "places": places,
            "food": food_list,
            "transport": transport_modes,
            "experiences": experiences,
            "activities": activities,
            "knowledge": knowledge
        }
        COUNTRIES[country] = info_data
        return info_data
    except Exception:
        if country in COUNTRIES:
            return COUNTRIES[country]
        return {
            "flag": "🌍",
            "duration": "7–10 days",
            "budget": "₹50k–₹1.5L",
            "season": "Spring / Autumn",
            "places": [country],
            "food": ["Local Cuisine"],
            "transport": ["Public transit", "Trains", "Buses"],
            "experiences": ["Landmark exploration"],
            "activities": {country: [("09:00", f"Explore {country}", country, 800, 30)]}
        }


# ============================================================
# ADD LIVE COUNTRY DATA
# ============================================================

def add_dynamic_country_data(
    country,
    places=None,
    food=None,
    experiences=None,
    flag="🌍",
    duration="5–10 days",
    budget="Varies",
    season="Depends on location"
):
    """
    Adds live country information to the existing sample
    travel data without removing the original sample data.
    """

    places = places or []
    food = food or []
    experiences = experiences or []

    if country in COUNTRIES:
        existing = COUNTRIES[country]

        if places:
            existing["places"] = places

        if food:
            existing["food"] = food

        if experiences:
            existing["experiences"] = experiences

        return

    activities = {}

    for index, place in enumerate(places[:8]):

        activities[place] = [
            (
                "09:00",
                f"Explore {place}",
                place,
                1500,
                30
            ),
            (
                "14:00",
                f"Visit {place}",
                place,
                1000,
                25
            ),
            (
                "19:00",
                f"Local experience in {place}",
                place,
                1200,
                20
            )
        ]

    COUNTRIES[country] = {
        "flag": flag,
        "duration": duration,
        "budget": budget,
        "season": season,
        "places": places,
        "food": food,
        "transport": [
            "Local transport",
            "Trains",
            "Buses",
            "Flights"
        ],
        "experiences": experiences or [
            "Local sightseeing",
            "Cultural experiences",
            "Local food",
            "Nature"
        ],
        "activities": activities
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

def recommend_destinations(country, interests):
    info = country_info(country)

    recommendations = []

    for place in info["places"]:

        if interests:

            reason = (
                f"{place} can be considered for your "
                f"{', '.join(interests).lower()} interests."
            )

        else:

            reason = (
                f"{place} is a popular place to explore."
            )

        recommendations.append({
            "name": place,
            "reason": reason
        })

    return recommendations[:6]


# ============================================================
# ACTIVITY POOL
# ============================================================

def _activity_pool(country, interests):

    info = country_info(country)

    pools = []

    for city, activities in info.get(
        "activities",
        {}
    ).items():

        for activity in activities:

            time = activity[0]
            name = activity[1]
            place = activity[2]
            cost = activity[3]
            travel_time = activity[4]

            score = 1

            text = name.lower()

            interest_text = [
                str(item).lower()
                for item in interests
            ]

            if "food" in interest_text:

                if any(
                    word in text
                    for word in [
                        "food",
                        "dinner",
                        "ramen",
                        "biryani",
                        "seafood",
                        "cooking",
                        "pizza",
                        "pasta"
                    ]
                ):

                    score += 3

            if "culture" in interest_text:

                if any(
                    word in text
                    for word in [
                        "temple",
                        "museum",
                        "palace",
                        "fort",
                        "heritage",
                        "old city",
                        "colosseum",
                        "shrine"
                    ]
                ):

                    score += 3

            if "nature" in interest_text:

                if any(
                    word in text
                    for word in [
                        "beach",
                        "lake",
                        "nature",
                        "garden",
                        "island",
                        "backwater"
                    ]
                ):

                    score += 3

            if "adventure" in interest_text:

                if any(
                    word in text
                    for word in [
                        "island",
                        "mount",
                        "beach",
                        "adventure"
                    ]
                ):

                    score += 2

            if "photography" in interest_text:

                if any(
                    word in text
                    for word in [
                        "photography",
                        "viewpoint",
                        "canal",
                        "tower",
                        "lake",
                        "beach"
                    ]
                ):

                    score += 2

            if "shopping" in interest_text:

                if "shopping" in text:
                    score += 3

            pools.append(
                (
                    score,
                    city,
                    activity
                )
            )

    # Ensure the pool is never empty
    if not pools:
        for p_idx, place in enumerate(info.get("places") or [destination]):
            default_acts = [
                ("09:00", f"Morning sightseeing and landmark discovery in {place}", place, 500, 25),
                ("14:00", f"Cultural immersion and local highlights in {place}", place, 800, 30),
                ("19:00", f"Authentic regional dining experience in {place}", place, 1200, 20)
            ]
            for act in default_acts:
                pools.append((2, place, act))

    pools.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return pools


# ============================================================
# ITINERARY GENERATOR
# ============================================================

def generate_itinerary(
    starting,
    destination,
    days,
    travelers,
    budget,
    interests,
    style,
    dietary_preferences=None,
    cultural_preferences=None
):
    # Support realistic durations up to 30 days
    days = max(1, min(30, int(days)))
    travelers = max(1, int(travelers))
    budget = max(5000, int(budget))
    starting_loc = str(starting or "").strip() or "Your Location"

    from destination_knowledge import get_city_food, get_destination_etiquette
    from country_data import get_country_knowledge, get_transportation

    info = country_info(destination)
    k_data = get_country_knowledge(destination)

    # Determine cities for this journey
    candidate_cities = list(info.get("activities", {}).keys())
    if not candidate_cities or len(candidate_cities) == 1 and candidate_cities[0] == destination:
        candidate_cities = k_data.get("cities", [destination])
    if not candidate_cities:
        candidate_cities = info.get("places", [destination])

    # Realistic city distribution: 2 to 4 days per city
    days_per_city = 3 if days >= 6 else (2 if days >= 4 else days)
    num_cities_to_visit = max(1, min(len(candidate_cities), (days + days_per_city - 1) // days_per_city))
    active_cities = candidate_cities[:num_cities_to_visit]

    # Destination Etiquette Guide
    etiquette_info = get_destination_etiquette(destination)

    # City-specific Attractions & Culture
    attractions_raw = k_data.get("attractions", [])
    culture_raw = k_data.get("culture", [])

    DAY_THEMES = [
        ("Landmark Highlights & Orientation", "Must-see architectural icons, orientation walk, and historic square"),
        ("Historic Heritage & Ancient Temples", "Centuries of world heritage monuments, national galleries, and shrines"),
        ("Scenic Nature, Gardens & Viewpoints", "Tranquil botanical parks, panoramic lookouts, and serene walkways"),
        ("Artisan Markets, Crafts & Old Town", "Handicrafts, local bazaars, and historic cobblestone lanes"),
        ("Gastronomic Journey & Culinary Delights", "Culinary traditions, food markets, and authentic regional tastings"),
        ("Day Excursion & Nature Adventure", "Outdoor excursions, scenic nature trails, and historic waterways"),
        ("Arts, Neighborhood Culture & Cafes", "Galleries, bohemian districts, indie bookstores, and relaxed cafes"),
        ("Spiritual Sanctums & Sacred Shrines", "Spiritual heritage sites, historic temples, and ancient sanctuaries"),
        ("Panoramic Lookouts & Sunset Promenade", "Scenic coastal or riverside promenades and sunset lookouts"),
        ("Botanical Escapes & Heritage Pavilions", "Tranquil flora collections, arboretums, and peaceful walkways"),
        ("Castles, Fortresses & Royal Citadels", "Historic ramparts, citadel architecture, and royal heritage"),
        ("Local Crafts & Artisan Workshops", "Traditional pottery, weaving, and regional craft studios"),
        ("Hidden Gems & Secluded Courtyards", "Charming secluded courtyards, quiet canals, and secret alleys"),
        ("Culinary Masterclass & Covered Markets", "Fresh produce discovery and authentic regional cooking traditions"),
        ("Harbor, Lake & Waterfront Heritage", "Historic ports, waterfront docks, and scenic boat experiences"),
        ("Music, Folklore & Traditional Arts", "Traditional folklore centers, musical heritage, and performance arts"),
        ("Scenic Mountain Valleys & Nature Trails", "Valley lookouts, panoramic nature viewpoints, and fresh mountain air"),
        ("Design, Architecture & Living Heritage", "Preserved heritage facades and iconic modern city architecture"),
        ("Historic Living & Artisan Quarters", "Strolling residential heritage quarters and greeting local artisans"),
        ("Excursion to Countryside Villages", "Day exploration of peaceful rural heritage hamlets and countryside"),
        ("Photography, Golden Hour & City Vistas", "Golden hour photo spots capturing dramatic regional topography"),
        ("Archaeology & Civilizational Relics", "Ruins, stone excavations, and ancient civilizational relics"),
        ("Evening Lantern Bazaars & Night Walks", "Evening lantern markets, sizzling street food stalls, and desserts"),
        ("Eco-Sanctuaries & Conservation Trails", "Protected wildlife habitats, bird-watching, and conservation trails"),
        ("Modern Culture & Avant-Garde Arts", "Avant-garde exhibitions, sculpture parks, and design museums"),
        ("Historic Teahouses & Roast Tastings", "Historic teahouses, regional roast tastings, and quiet reflection"),
        ("Waterfront Breezes & Seaside Dining", "Refreshing waterfront breeze, lakeside paths, and seaside dining"),
        ("Vintage Flea Markets & Curio Bazaars", "Vintage shops, flea markets, and collectible artisan souvenirs"),
        ("Panoramic Farewell Vantage Point", "Spectacular vantage point overlooking the entire cityscape"),
        ("Celebratory Grand Farewell Feast", "Celebratory farewell feast honoring regional culinary heritage")
    ]

    result_days = []
    used_attractions = set()

    for day_number in range(1, days + 1):
        # Determine city for this day
        city_idx = ((day_number - 1) // days_per_city) % len(active_cities)
        city = active_cities[city_idx]
        day_in_city = ((day_number - 1) % days_per_city) + 1

        is_first_day = (day_number == 1)
        is_last_day = (day_number == days)
        is_intercity_transfer = (day_in_city == 1 and day_number > 1)

        theme_title, theme_desc = DAY_THEMES[(day_number - 1) % len(DAY_THEMES)]

        # Retrieve authentic dishes specific to this city
        city_dishes = get_city_food(destination, city)
        if dietary_preferences:
            veg_req = any("veg" in str(p).lower() for p in dietary_preferences)
            vegan_req = any("vegan" in str(p).lower() for p in dietary_preferences)
            halal_req = any("halal" in str(p).lower() for p in dietary_preferences)
            filtered = []
            for d in city_dishes:
                if vegan_req and not d.get("is_vegan"):
                    continue
                if veg_req and not (d.get("is_vegetarian") or d.get("is_vegan")):
                    continue
                if halal_req and not d.get("is_halal", True):
                    continue
                filtered.append(d)
            if filtered:
                city_dishes = filtered

        breakfast_dish = next((d for d in city_dishes if d.get("breakfast_friendly")), city_dishes[0] if city_dishes else None)
        lunch_dish = city_dishes[(day_in_city - 1) % len(city_dishes)] if city_dishes else None
        dinner_dish = city_dishes[day_in_city % len(city_dishes)] if len(city_dishes) > 1 else (city_dishes[0] if city_dishes else None)

        # Contextual etiquette tip for this day
        if is_first_day:
            etiquette_tip = f"Arrival Etiquette: {etiquette_info.get('greetings', {}).get('summary', 'Greet locals politely and have documents ready.')}"
        elif is_last_day:
            etiquette_tip = f"Departure Courtesy: {etiquette_info.get('community_respect', {}).get('summary', 'Thank your hosts and settle all hotel bills politely.')}"
        elif any(w in theme_title.lower() for w in ["temple", "spiritual", "shrine", "heritage"]):
            etiquette_tip = f"Sacred Site Etiquette: {etiquette_info.get('temples_and_shrines', {}).get('summary', 'Remove shoes and dress modestly with covered shoulders.')}"
        elif any(w in theme_title.lower() for w in ["gastronomic", "culinary", "market", "feast"]):
            etiquette_tip = f"Dining Etiquette: {etiquette_info.get('dining', {}).get('summary', 'Respect local dining manners and table customs.')}"
        else:
            etiquette_tip = f"Transit & Community: {etiquette_info.get('public_transport', {}).get('summary', 'Keep voices low on public transit.')}"

        # Find city-specific attractions
        city_att_matches = [
            a[0] if isinstance(a, (tuple, list)) else str(a)
            for a in attractions_raw
            if isinstance(a, (tuple, list)) and len(a) > 1 and (a[1].lower() in city.lower() or city.lower() in a[1].lower())
        ]
        city_cult_matches = [
            c[0] if isinstance(c, (tuple, list)) else str(c)
            for c in culture_raw
            if isinstance(c, (tuple, list)) and len(c) > 1 and (c[1].lower() in city.lower() or city.lower() in c[1].lower())
        ]

        # Morning Attraction
        avail_att = [a for a in city_att_matches if a not in used_attractions]
        if avail_att:
            chosen_morn = avail_att[0]
            used_attractions.add(chosen_morn)
        elif city_att_matches:
            chosen_morn = city_att_matches[(day_in_city - 1) % len(city_att_matches)]
        else:
            chosen_morn = f"{city} Historic Center & Landmark Promenade"

        # Afternoon Attraction / Experience
        avail_cult = [c for c in city_cult_matches if c not in used_attractions]
        if avail_cult:
            chosen_aft = avail_cult[0]
            used_attractions.add(chosen_aft)
        elif city_cult_matches:
            chosen_aft = city_cult_matches[(day_in_city - 1) % len(city_cult_matches)]
        else:
            chosen_aft = f"{city} Cultural Heritage Museum & Artisan District"

        activities = []

        # DAY 1: ARRIVAL SCHEDULE
        if is_first_day:
            day_title = f"{city}: Arrival from {starting_loc} & Orientation"
            activities.append({
                "time": "10:30 AM",
                "activity": f"Arrival from {starting_loc} at {city} (Airport/Station transfer, hotel check-in & unpack)",
                "place": f"{city} Central Hotel",
                "cost": int(600 * travelers),
                "travel_time": "45 min",
                "transport": "Express Airport Transit / Licensed Taxi"
            })
            if lunch_dish:
                activities.append({
                    "time": "01:30 PM",
                    "activity": f"Welcome Lunch: Savor authentic {lunch_dish['name']} ({lunch_dish.get('taste_profile', 'Local specialty')})",
                    "place": lunch_dish.get("where_to_try", f"Traditional Cafe in {city}"),
                    "cost": int(750 * travelers),
                    "travel_time": "15 min",
                    "transport": "Short Walk / Local Tram"
                })
            activities.append({
                "time": "03:30 PM",
                "activity": f"Gentle Orientation Walk: Explore {chosen_morn}",
                "place": city,
                "cost": int(500 * travelers),
                "travel_time": "20 min",
                "transport": "Scenic Walking Tour"
            })
            if dinner_dish:
                activities.append({
                    "time": "07:30 PM",
                    "activity": f"Evening Welcome Dinner: Taste regional {dinner_dish['name']} — {dinner_dish.get('taste_profile', 'Authentic cuisine')}",
                    "place": dinner_dish.get("where_to_try", f"Authentic Dining Quarter in {city}"),
                    "cost": int(1100 * travelers),
                    "travel_time": "20 min",
                    "transport": "Evening Walk / City Metro"
                })

        # FINAL DAY: DEPARTURE & RETURN JOURNEY SCHEDULE
        elif is_last_day:
            day_title = f"{city}: Farewell & Return Journey to {starting_loc}"
            if breakfast_dish:
                activities.append({
                    "time": "08:30 AM",
                    "activity": f"Breakfast: {breakfast_dish['name']} ({breakfast_dish.get('taste_profile', 'Morning specialty')})",
                    "place": f"Local Morning Cafe in {city}",
                    "cost": int(400 * travelers),
                    "travel_time": "10 min",
                    "transport": "Morning Walk"
                })
            activities.append({
                "time": "10:00 AM",
                "activity": f"Final Highlights & Artisan Craft Shopping: Browse local souvenirs in {city}",
                "place": f"{city} Historic Artisan Market",
                "cost": int(600 * travelers),
                "travel_time": "20 min",
                "transport": "City Metro / Walking"
            })
            if lunch_dish:
                activities.append({
                    "time": "01:00 PM",
                    "activity": f"Celebratory Farewell Lunch: Authentic {lunch_dish['name']}",
                    "place": lunch_dish.get("where_to_try", f"Bistro in {city}"),
                    "cost": int(850 * travelers),
                    "travel_time": "15 min",
                    "transport": "Walking"
                })
            activities.append({
                "time": "04:00 PM",
                "activity": f"Hotel check-out, luggage collection & departure transit returning to {starting_loc}",
                "place": f"{city} International Airport / Central Station",
                "cost": int(900 * travelers),
                "travel_time": "50 min",
                "transport": "Express Departure Rail / Airport Shuttle"
            })

        # INTERMEDIATE EXPLORATION DAYS
        else:
            day_title = f"{city}: {theme_title}"
            # 1. Breakfast Suggestion
            if breakfast_dish:
                activities.append({
                    "time": "08:30 AM",
                    "activity": f"Local Breakfast Suggestion: {breakfast_dish['name']} ({breakfast_dish.get('taste_profile', 'Nutritious morning start')})",
                    "place": f"Traditional Morning Bakery / Cafe in {city}",
                    "cost": int(350 * travelers),
                    "travel_time": "10 min",
                    "transport": "Morning Walk"
                })

            # 2. Morning Sightseeing
            m_trans = "High-Speed Rail / Intercity Express" if is_intercity_transfer else f"{city} Metro / Scenic Walk"
            activities.append({
                "time": "10:00 AM",
                "activity": f"Morning Sightseeing: Discover {chosen_morn}",
                "place": city,
                "cost": int(800 * travelers),
                "travel_time": "25 min",
                "transport": m_trans
            })

            # 3. Lunch Featuring Local Dish
            if lunch_dish:
                activities.append({
                    "time": "01:00 PM",
                    "activity": f"Authentic Regional Lunch: Taste {lunch_dish['name']} ({lunch_dish.get('taste_profile', 'Regional specialty')})",
                    "place": lunch_dish.get("where_to_try", f"Local Food Market in {city}"),
                    "cost": int(750 * travelers),
                    "travel_time": "15 min",
                    "transport": "Walking / Tram"
                })

            # 4. Afternoon Cultural Activity
            activities.append({
                "time": "03:00 PM",
                "activity": f"Afternoon Cultural Experience: {chosen_aft} ({theme_desc})",
                "place": city,
                "cost": int(650 * travelers),
                "travel_time": "20 min",
                "transport": "City Transit / Walking"
            })

            # 5. Dinner Featuring Signature Local Cuisine
            if dinner_dish:
                activities.append({
                    "time": "07:30 PM",
                    "activity": f"Dinner & Evening Walk: Savor {dinner_dish['name']} ({dinner_dish.get('taste_profile', 'Evening delight')})",
                    "place": dinner_dish.get("where_to_try", f"Historic Dining Quarter in {city}"),
                    "cost": int(1150 * travelers),
                    "travel_time": "20 min",
                    "transport": "Evening Stroll / Metro"
                })

        result_days.append({
            "day": day_number,
            "city": city,
            "title": day_title,
            "etiquette_tip": etiquette_tip,
            "activities": activities
        })

    # Exact, Reliable Mathematical Budget Engine
    activity_actual = sum(
        activity.get("cost", 0)
        for day in result_days
        for activity in day.get("activities", [])
    )

    accommodation_actual = int((budget * 0.35) * min(1.0, days / 10.0)) * travelers
    intercity_actual = int((budget * 0.18) * min(1.0, days / 10.0))
    food_actual = int((budget * 0.22) * min(1.0, days / 10.0)) * travelers
    misc_actual = int(budget * 0.05)

    # Calculate total as EXACT sum of all categories
    total_calculated = accommodation_actual + intercity_actual + food_actual + activity_actual + misc_actual

    return {
        "starting": starting_loc,
        "destination": destination,
        "days": result_days,
        "budget": {
            "Accommodation": accommodation_actual,
            "Intercity/local transport": intercity_actual,
            "Food": food_actual,
            "Activities": activity_actual,
            "Miscellaneous": misc_actual
        },
        "total_cost": total_calculated
    }


# ============================================================
# AI ASSISTANT / ITINERARY MODIFICATION
# ============================================================

def update_itinerary(
    plan,
    request,
    budget,
    destination,
    interests
):

    updated_plan = deepcopy(plan)

    query = request.lower()

    # --------------------------------------------------------
    # Make a particular day less tiring
    # --------------------------------------------------------

    if (
        "less tiring" in query
        or "less busy" in query
        or "relax" in query
    ):

        match = re.search(
            r"day\s*(\d+)",
            query
        )

        if match:

            day_number = int(
                match.group(1)
            )

        else:

            day_number = 2

        for day in updated_plan["days"]:

            if day["day"] == day_number:

                day["activities"] = (
                    day["activities"][:1]
                )

                day["title"] += (
                    " — Relaxed"
                )

    # --------------------------------------------------------
    # Reduce budget
    # --------------------------------------------------------

    elif (
        "reduce" in query
        and "budget" in query
    ):

        for day in updated_plan["days"]:

            if len(
                day["activities"]
            ) > 1:

                day["activities"].sort(
                    key=lambda item:
                    item["cost"]
                )

                day["activities"] = (
                    day["activities"][:-1]
                )

        updated_plan["total_cost"] = min(
            updated_plan["total_cost"],
            budget
        )

    # --------------------------------------------------------
    # Add food experience
    # --------------------------------------------------------

    elif "food" in query:

        food_activities = [
            item
            for item in _activity_pool(
                destination,
                ["Food"]
            )
            if (
                "food" in item[2][1].lower()
                or "dinner" in item[2][1].lower()
                or "cooking" in item[2][1].lower()
            )
        ]

        if food_activities:

            _, city, activity = (
                food_activities[0]
            )

            updated_plan["days"][-1][
                "activities"
            ].append({
                "time": activity[0],
                "activity": activity[1],
                "place": activity[2],
                "cost": activity[3],
                "travel_time":
                    f"{activity[4]} min"
            })

    # --------------------------------------------------------
    # Replace an activity
    # --------------------------------------------------------

    elif "replace" in query:

        if updated_plan["days"]:

            day = updated_plan[
                "days"
            ][-1]

            alternatives = (
                _activity_pool(
                    destination,
                    interests
                )
            )

            if alternatives:

                _, city, activity = (
                    alternatives[0]
                )

                if day["activities"]:

                    day["activities"][0] = {
                        "time": activity[0],
                        "activity": activity[1],
                        "place": activity[2],
                        "cost": activity[3],
                        "travel_time":
                            f"{activity[4]} min"
                    }

    return updated_plan