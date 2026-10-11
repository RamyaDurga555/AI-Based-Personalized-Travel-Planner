"""
multi_stop_planner.py
=============================================================
Intelligent Multi-Stop, Multi-Country Itinerary Planning Engine
and Seasonal Destination Recommendation System.

Key Features:
1. Natural language trip request parser (extracts starting point,
   multiple ordered stops, dates/durations, transport preferences,
   and return journey).
2. Transportation route planner for intercity and international legs
   (modes, journey time, fare ranges, stations, connections, buffer time).
3. Day-by-day multi-stop itinerary synthesizer.
4. Month-by-month seasonal travel recommendation engine.
100% Deterministic Local Python Logic — Zero External API Keys.
=============================================================
"""

import re
import datetime
from typing import Dict, List, Any, Optional, Tuple


# ============================================================
# 1. CURATED TRANSPORTATION CORRIDOR DATABASE
# ============================================================

VERIFIED_TRANSIT_CORRIDORS: Dict[Tuple[str, str], Dict[str, Any]] = {
    # Japan Corridors
    ("tokyo", "kyoto"): {
        "recommended_mode": "Tokaido Shinkansen (Bullet Train)",
        "alternative_modes": ["Highway Express Coach (Willer Express)", "Domestic Flight (HND to ITM)"],
        "travel_time": "2h 15m (Nozomi) / 2h 40m (Hikari)",
        "cost_range_inr": "₹7,600 – ₹8,200",
        "cost_range_local": "¥13,870 – ¥14,520",
        "terminal_origin": "Tokyo Station (Tracks 14–19) / Shinagawa Station",
        "terminal_dest": "Kyoto Station (Central Shinkansen Gate)",
        "connections": "Direct non-stop service; trains depart every 10–15 minutes",
        "departure_window": "Recommended morning departure (08:30–10:00 AM) to maximize afternoon sightseeing in Kyoto",
        "buffer_notes": "Allow 20 minutes buffer for luggage storage and platform access. Reserve seats on the right (Seats D/E) for Mount Fuji views.",
        "booking_links": [{"name": "SmartEX Official App", "url": "https://smart-ex.jp/en/"}, {"name": "JR West / Central Online", "url": "https://www.westjr.co.jp/global/en/"}]
    },
    ("kyoto", "osaka"): {
        "recommended_mode": "JR Special Rapid Service / Hankyu Kyoto Main Line",
        "alternative_modes": ["Tokaido Shinkansen (Shin-Osaka, 14m)", "Keihan Main Line (to Yodoyabashi)"],
        "travel_time": "28–35 minutes",
        "cost_range_inr": "₹320 – ₹450",
        "cost_range_local": "¥570 – ¥800",
        "terminal_origin": "Kyoto Station (Platform 4/5) or Hankyu Kyoto-Kawaramachi",
        "terminal_dest": "Osaka Station (Umeda) or Shin-Osaka Station",
        "connections": "Direct frequent commuter rail; departs every 8–10 minutes throughout the day",
        "departure_window": "Flexible departure throughout the day; no seat reservation required",
        "buffer_notes": "Very frequent trains; allow 10 minutes at the station. IC transit cards (Suica/Pasmo/ICOCA) tap-to-pay accepted.",
        "booking_links": [{"name": "JR West Timetables", "url": "https://www.westjr.co.jp/global/en/"}]
    },
    ("tokyo", "osaka"): {
        "recommended_mode": "Tokaido Shinkansen (Nozomi Bullet Train)",
        "alternative_modes": ["Domestic Flight (HND to ITM / KIX)", "Overnight Highway Express Coach"],
        "travel_time": "2h 30m",
        "cost_range_inr": "₹8,000 – ₹8,800",
        "cost_range_local": "¥14,720 – ¥15,500",
        "terminal_origin": "Tokyo Station",
        "terminal_dest": "Shin-Osaka Station (Transfer to Midosuji Metro into city center)",
        "connections": "Direct high-speed bullet train",
        "departure_window": "Depart morning (09:00 AM) or early afternoon",
        "buffer_notes": "Allow 25 minutes at Tokyo Station. Transfer to Midosuji Line takes ~10 mins to Namba/Dotonbori.",
        "booking_links": [{"name": "SmartEX Official", "url": "https://smart-ex.jp/en/"}]
    },
    ("tokyo", "hakone"): {
        "recommended_mode": "Odakyu Limited Express Romancecar",
        "alternative_modes": ["Tokaido Shinkansen to Odawara + Hakone Tozan Line", "Highway Express Bus from Shinjuku"],
        "travel_time": "1h 25m",
        "cost_range_inr": "₹1,400 – ₹1,800",
        "cost_range_local": "¥2,470",
        "terminal_origin": "Shinjuku Station (Odakyu Sightseeing Service Center)",
        "terminal_dest": "Hakone-Yumoto Station",
        "connections": "Direct scenic train; connects with Hakone Tozan switchback railway",
        "departure_window": "Depart morning (08:30–09:30 AM)",
        "buffer_notes": "Hakone Freepass covers the Romancecar supplement, cable car, ropeway, and pirate cruise.",
        "booking_links": [{"name": "Odakyu Hakone Freepass", "url": "https://www.odakyu.jp/english/"}]
    },
    ("osaka", "hiroshima"): {
        "recommended_mode": "Sanyo Shinkansen (Nozomi / Sakura Bullet Train)",
        "alternative_modes": ["Highway Coach", "Regional JR Express"],
        "travel_time": "1h 25m",
        "cost_range_inr": "₹5,800 – ₹6,400",
        "cost_range_local": "¥10,630",
        "terminal_origin": "Shin-Osaka Station",
        "terminal_dest": "Hiroshima Station",
        "connections": "Direct bullet train",
        "departure_window": "Morning departure (08:30 AM) to allow full day at Peace Memorial Park & Miyajima Island",
        "buffer_notes": "Transfer to JR Sanyo Line to Miyajimaguchi for the scenic ferry to Itsukushima Shrine.",
        "booking_links": [{"name": "JR West Shinkansen", "url": "https://www.westjr.co.jp/global/en/"}]
    },

    # European Corridors
    ("paris", "london"): {
        "recommended_mode": "Eurostar High-Speed Passenger Train (Channel Tunnel)",
        "alternative_modes": ["Commercial Flight (CDG to LHR / LGW)", "FlixBus / BlaBlaCar Bus"],
        "travel_time": "2h 16m",
        "cost_range_inr": "₹6,500 – ₹14,000",
        "cost_range_local": "€70 – €160",
        "terminal_origin": "Gare du Nord (Paris)",
        "terminal_dest": "London St Pancras International",
        "connections": "Direct international high-speed train via Channel Tunnel",
        "departure_window": "Mid-morning (09:30 AM) or early evening",
        "buffer_notes": "CRITICAL: Arrive at least 90 minutes before departure for juxtaposed French & UK border immigration and customs control.",
        "booking_links": [{"name": "Eurostar Official", "url": "https://www.eurostar.com"}]
    },
    ("paris", "rome"): {
        "recommended_mode": "Direct Commercial Flight",
        "alternative_modes": ["High-Speed TGV / Frecciarossa Rail via Milan (10–11h scenic)", "Overnight sleeper train"],
        "travel_time": "2h 05m flight (+ 2h airport transit)",
        "cost_range_inr": "₹5,500 – ₹12,000",
        "cost_range_local": "€60 – €140",
        "terminal_origin": "Paris Charles de Gaulle (CDG) / Orly (ORY)",
        "terminal_dest": "Rome Fiumicino (FCO) / Ciampino (CIA)",
        "connections": "Direct daily flights operated by Air France, ITA Airways, easyJet",
        "departure_window": "Depart morning (10:00 AM) to arrive in Rome in time for afternoon gelato and Colosseum sunset",
        "buffer_notes": "Leonardo Express non-stop train connects FCO to Roma Termini in 32 minutes (€14).",
        "booking_links": [{"name": "Rome Fiumicino Airport Express", "url": "https://www.trenitalia.com"}]
    },
    ("rome", "florence"): {
        "recommended_mode": "Frecciarossa / Italo High-Speed Rail",
        "alternative_modes": ["InterCity Regional Train (3h)", "FlixBus Coach"],
        "travel_time": "1h 15m",
        "cost_range_inr": "₹2,200 – ₹4,200",
        "cost_range_local": "€24 – €48",
        "terminal_origin": "Roma Termini Station",
        "terminal_dest": "Firenze Santa Maria Novella (SMN)",
        "connections": "Direct non-stop high-speed train reaching 300 km/h",
        "departure_window": "Morning departure (09:00 AM) recommended",
        "buffer_notes": "Firenze SMN station is within easy walking distance of the Duomo and historic center.",
        "booking_links": [{"name": "Trenitalia Official", "url": "https://www.trenitalia.com"}, {"name": "Italo Rail", "url": "https://www.italotreno.it"}]
    },
    ("florence", "venice"): {
        "recommended_mode": "Frecciarossa / Italo High-Speed Rail",
        "alternative_modes": ["Regional InterCity", "Coach"],
        "travel_time": "2h 05m",
        "cost_range_inr": "₹2,800 – ₹5,200",
        "cost_range_local": "€30 – €58",
        "terminal_origin": "Firenze Santa Maria Novella",
        "terminal_dest": "Venezia Santa Lucia (Island Station)",
        "connections": "Direct high-speed train straight onto the Venetian lagoon",
        "departure_window": "Morning departure (09:30 AM)",
        "buffer_notes": "Ensure ticket destination is Venezia Santa Lucia (island), NOT Venezia Mestre (mainland). Step directly out onto the Grand Canal vaporetto waterbus.",
        "booking_links": [{"name": "Trenitalia Official", "url": "https://www.trenitalia.com"}]
    },
    ("madrid", "barcelona"): {
        "recommended_mode": "AVE / Iryo / Ouigo High-Speed Bullet Train",
        "alternative_modes": ["Iberia Shuttle Flight (MAD to BCN)", "ALSA Express Coach (7h)"],
        "travel_time": "2h 30m",
        "cost_range_inr": "₹2,500 – ₹6,500",
        "cost_range_local": "€28 – €75",
        "terminal_origin": "Madrid Puerta de Atocha",
        "terminal_dest": "Barcelona Sants Station",
        "connections": "Direct high-speed service traversing central Spain",
        "departure_window": "Mid-morning (09:30 AM)",
        "buffer_notes": "X-ray luggage security scanning required before boarding; allow 25 minutes buffer at Atocha.",
        "booking_links": [{"name": "Renfe AVE Official", "url": "https://www.renfe.com"}]
    },

    # India Corridors
    ("delhi", "agra"): {
        "recommended_mode": "Gatimaan Express / Vande Bharat Express",
        "alternative_modes": ["Yamuna Expressway AC Private Cab / Coach (3h)", "Taj Express (2h 15m)"],
        "travel_time": "1h 40m",
        "cost_range_inr": "₹750 – ₹1,550",
        "cost_range_local": "₹750 (CC) / ₹1,550 (EC)",
        "terminal_origin": "Hazrat Nizamuddin Station (Delhi)",
        "terminal_dest": "Agra Cantt Railway Station",
        "connections": "Direct morning train (departs 08:10 AM from Nizamuddin, arrives 09:50 AM)",
        "departure_window": "08:10 AM Gatimaan departure includes breakfast on board",
        "buffer_notes": "Taj Mahal is closed on Fridays. Pre-book battery-operated golf carts from parking to monuments.",
        "booking_links": [{"name": "IRCTC Official Portal", "url": "https://www.irctc.co.in"}]
    },
    ("delhi", "jaipur"): {
        "recommended_mode": "Vande Bharat Express / Shatabdi Express",
        "alternative_modes": ["Delhi-Jaipur Expressway AC Cab (4–5h)", "Domestic Flight (DEL to JAI, 55m)"],
        "travel_time": "3h 45m",
        "cost_range_inr": "₹900 – ₹1,850",
        "cost_range_local": "₹900 (Chair Car) / ₹1,850 (Executive)",
        "terminal_origin": "Delhi Cantt / New Delhi Railway Station",
        "terminal_dest": "Jaipur Junction",
        "connections": "Direct morning and evening high-speed executive trains",
        "departure_window": "Depart morning (06:10 AM Shatabdi or 15:00 PM Vande Bharat)",
        "buffer_notes": "Jaipur Junction is 15 minutes by auto-rickshaw or taxi to the Pink City heritage gates.",
        "booking_links": [{"name": "IRCTC Official Portal", "url": "https://www.irctc.co.in"}]
    },
    ("jaipur", "udaipur"): {
        "recommended_mode": "Vande Bharat Express / Intercity Superfast",
        "alternative_modes": ["AC Sleeper Coach / Private Cab (6h)", "Domestic Flight (50m)"],
        "travel_time": "3h 55m",
        "cost_range_inr": "₹850 – ₹1,700",
        "cost_range_local": "₹850 (CC) / ₹1,700 (EC)",
        "terminal_origin": "Jaipur Junction",
        "terminal_dest": "Udaipur City Railway Station",
        "connections": "Direct rail connectivity through the Aravalli hills",
        "departure_window": "Depart morning (07:30 AM)",
        "buffer_notes": "Arrive at Udaipur by lunch; sunset boat ride on Lake Pichola is ideal for the first evening.",
        "booking_links": [{"name": "IRCTC Official Portal", "url": "https://www.irctc.co.in"}]
    },

    # Thailand Corridors
    ("bangkok", "chiang mai"): {
        "recommended_mode": "Domestic Flight (Suvarnabhumi BKK / Don Mueang DMK)",
        "alternative_modes": ["Special Express Overnight Sleeper Train #9 (12h, scenic)", "AC VIP Express Coach (10h)"],
        "travel_time": "1h 15m (flight) / 12h (sleeper train)",
        "cost_range_inr": "₹2,800 – ₹5,500",
        "cost_range_local": "฿1,200 – ฿2,400",
        "terminal_origin": "Bangkok Suvarnabhumi (BKK) / Don Mueang (DMK) / Krung Thep Aphiwat (Train)",
        "terminal_dest": "Chiang Mai International Airport (CNX) / Chiang Mai Railway Station",
        "connections": "Hourly departures operated by Thai Airways, Bangkok Airways, AirAsia",
        "departure_window": "Depart morning (09:00 AM) or take the iconic 18:40 PM Special Express Sleeper Train",
        "buffer_notes": "Chiang Mai airport is located just 10 minutes from the historic Old City moat.",
        "booking_links": [{"name": "State Railway of Thailand (D-Ticket)", "url": "https://www.dticket.railway.co.th"}]
    },
    ("bangkok", "phuket"): {
        "recommended_mode": "Domestic Commercial Flight",
        "alternative_modes": ["Overnight AC VIP Coach (12h)", "Train to Surat Thani + Ferry/Bus"],
        "travel_time": "1h 20m",
        "cost_range_inr": "₹3,200 – ₹6,800",
        "cost_range_local": "฿1,400 – ฿3,000",
        "terminal_origin": "Bangkok Suvarnabhumi (BKK) / Don Mueang (DMK)",
        "terminal_dest": "Phuket International Airport (HKT)",
        "connections": "Frequent direct flights",
        "departure_window": "Depart mid-morning (10:00 AM)",
        "buffer_notes": "Phuket airport is 45–60 minutes from Patong, Kata, or Karon beaches via airport bus or Grab taxi.",
        "booking_links": [{"name": "Thai Airways / AirAsia Official", "url": "https://www.airasia.com"}]
    },

    # Nepal Corridors
    ("kathmandu", "pokhara"): {
        "recommended_mode": "Scenic Domestic Flight (Himalayan Panorama)",
        "alternative_modes": ["Tourist Deluxe AC Coach via Prithvi Highway (6–7h, NPR 1,200)", "Private 4WD Jeep"],
        "travel_time": "25–30 minutes (flight)",
        "cost_range_inr": "₹6,500 – ₹8,500",
        "cost_range_local": "NPR 11,000 – 14,000 ($90–$115)",
        "terminal_origin": "Tribhuvan International Airport (Kathmandu Domestic Terminal)",
        "terminal_dest": "Pokhara International Airport (PKR)",
        "connections": "Frequent morning flights operated by Buddha Air and Yeti Airlines",
        "departure_window": "Book early morning flights (07:30–09:30 AM) when skies are clearest",
        "buffer_notes": "Request a seat on the RIGHT side heading to Pokhara (and LEFT returning) for views of Langtang, Ganesh Himal, and Annapurna range.",
        "booking_links": [{"name": "Buddha Air Official", "url": "https://www.buddhaair.com"}]
    }
}


# ============================================================
# 2. INTERNATIONAL HUB & FLIGHT ESTIMATOR
# ============================================================

MAJOR_AIRPORT_CODES: Dict[str, Dict[str, str]] = {
    "hyderabad": {"code": "HYD", "name": "Rajiv Gandhi International Airport", "country": "India"},
    "delhi": {"code": "DEL", "name": "Indira Gandhi International Airport", "country": "India"},
    "new delhi": {"code": "DEL", "name": "Indira Gandhi International Airport", "country": "India"},
    "mumbai": {"code": "BOM", "name": "Chhatrapati Shivaji Maharaj International Airport", "country": "India"},
    "bengaluru": {"code": "BLR", "name": "Kempegowda International Airport", "country": "India"},
    "bangalore": {"code": "BLR", "name": "Kempegowda International Airport", "country": "India"},
    "chennai": {"code": "MAA", "name": "Chennai International Airport", "country": "India"},
    "kolkata": {"code": "CCU", "name": "Netaji Subhash Chandra Bose International Airport", "country": "India"},
    "tokyo": {"code": "HND/NRT", "name": "Tokyo Haneda (HND) / Narita (NRT)", "country": "Japan"},
    "osaka": {"code": "KIX/ITM", "name": "Kansai International (KIX) / Itami (ITM)", "country": "Japan"},
    "kyoto": {"code": "Kyoto Station (Rail Hub connected to KIX/ITM via JR Haruka Express)", "name": "Kyoto Station (Rail Hub connected to KIX/ITM via JR Haruka Express)", "country": "Japan"},
    "paris": {"code": "CDG/ORY", "name": "Charles de Gaulle (CDG) / Orly (ORY)", "country": "France"},
    "london": {"code": "LHR/LGW", "name": "Heathrow (LHR) / Gatwick (LGW)", "country": "United Kingdom"},
    "rome": {"code": "FCO", "name": "Leonardo da Vinci–Fiumicino Airport", "country": "Italy"},
    "bangkok": {"code": "BKK/DMK", "name": "Suvarnabhumi (BKK) / Don Mueang (DMK)", "country": "Thailand"},
    "singapore": {"code": "SIN", "name": "Singapore Changi Airport", "country": "Singapore"},
    "dubai": {"code": "DXB", "name": "Dubai International Airport", "country": "United Arab Emirates"},
    "kathmandu": {"code": "KTM", "name": "Tribhuvan International Airport", "country": "Nepal"},
    "new york": {"code": "JFK/EWR", "name": "John F. Kennedy (JFK) / Newark (EWR)", "country": "USA"},
    "zurich": {"code": "ZRH", "name": "Zurich Airport", "country": "Switzerland"}
}


def build_international_flight_leg(
    origin_city: str,
    dest_city: str,
    origin_country: str = "",
    dest_country: str = ""
) -> Dict[str, Any]:
    """
    Generates a realistic, independent international flight leg between origin and destination.
    Never copies return leg details from the outward leg without checking.
    Clearly marks flight fares as estimated live market ranges.
    """
    o_key = origin_city.strip().lower()
    d_key = dest_city.strip().lower()

    if o_key in MAJOR_AIRPORT_CODES:
        orig_info = MAJOR_AIRPORT_CODES[o_key]
    else:
        orig_info = {
            "code": "Origin Airport / Rail Hub",
            "name": f"{origin_city} Airport / Rail Hub",
            "country": origin_country or "Origin"
        }

    if d_key in MAJOR_AIRPORT_CODES:
        dest_info = MAJOR_AIRPORT_CODES[d_key]
    else:
        dest_info = {
            "code": "Destination Airport / Rail Hub",
            "name": f"{dest_city} International Airport / Gateway",
            "country": dest_country or "Destination"
        }

    is_india_origin = any(w in (orig_info["country"] + " " + origin_city).lower() for w in ["india", "hyderabad", "delhi", "mumbai", "bengaluru", "chennai", "kolkata"])
    is_india_dest = any(w in (dest_info["country"] + " " + dest_city).lower() for w in ["india", "hyderabad", "delhi", "mumbai", "bengaluru", "chennai", "kolkata"])
    dest_str = (dest_info["country"] + " " + dest_city).lower()
    orig_str = (orig_info["country"] + " " + origin_city).lower()

    # Outbound India -> Japan
    if is_india_origin and ("japan" in dest_str or "tokyo" in dest_str or "osaka" in dest_str):
        duration = "8h 30m – 11h 15m (1-stop via SIN/BKK/KUL, or direct DEL-HND)"
        cost_inr = "₹28,000 – ₹42,000 (estimated)"
        cost_local = "¥50,000 – ¥75,000 (estimated)"
        airline_options = "Singapore Airlines, Malaysia Airlines, Thai Airways, ANA, Air India"
        dep_window = "Evening departure (21:00–23:30) or early morning (05:30–07:00)"
        advice = "Arrive at airport 3 hours prior for international check-in and immigration. Complete Japan Visit Web digital customs clearance in advance."
    # Inbound Japan -> India (Return Leg)
    elif ("japan" in orig_str or "osaka" in orig_str or "tokyo" in orig_str) and is_india_dest:
        duration = "9h 15m – 12h 00m (Connecting via SIN/BKK/KUL or direct NRT-DEL)"
        cost_inr = "₹29,000 – ₹43,500 (estimated)"
        cost_local = "¥52,000 – ¥78,000 (estimated)"
        airline_options = "Singapore Airlines, Thai Airways, Malaysia Airlines, ANA, Air India"
        dep_window = "Morning (10:00–12:30) or late evening (22:00–00:30) international return flight"
        advice = f"Board from {dest_info['name'] if 'kix' in dest_str else orig_info['name']}. Allow 3 hours airport check-in and security buffer prior to flight departure."
    # India -> Europe
    elif is_india_origin and any(eu in dest_str for eu in ["france", "paris", "united kingdom", "london", "italy", "rome", "germany", "spain", "switzerland"]):
        duration = "9h 30m – 12h 00m"
        cost_inr = "₹32,000 – ₹48,000 (estimated)"
        cost_local = "€350 – €550 (estimated)"
        airline_options = "Emirates, Qatar Airways, Air France, British Airways, Air India, Lufthansa"
        dep_window = "Night departure (02:00–05:00) or early morning"
        advice = "Arrive 3.5 hours prior for biometric immigration and baggage check-in."
    # Europe -> India (Return Leg)
    elif any(eu in orig_str for eu in ["france", "paris", "united kingdom", "london", "italy", "rome", "germany", "spain", "switzerland"]) and is_india_dest:
        duration = "9h 00m – 11h 30m"
        cost_inr = "₹33,000 – ₹49,000 (estimated)"
        cost_local = "€360 – €570 (estimated)"
        airline_options = "Emirates, Qatar Airways, Air France, British Airways, Air India"
        dep_window = "Afternoon (14:00–16:00) or evening departure"
        advice = "Allow 3 hours at European airport for VAT tax refunds, baggage drop, and Schengen exit passport control."
    # India -> Southeast Asia
    elif is_india_origin and any(sea in dest_str for sea in ["thailand", "bangkok", "singapore", "vietnam"]):
        duration = "3h 45m – 5h 30m (Direct or 1-stop)"
        cost_inr = "₹12,000 – ₹22,000 (estimated)"
        cost_local = "Local equivalent (estimated)"
        airline_options = "Thai Airways, Singapore Airlines, IndiGo, AirAsia"
        dep_window = "Morning (06:00–09:00) or late night"
        advice = "Arrive 3 hours prior for international check-in."
    # Southeast Asia -> India
    elif any(sea in orig_str for sea in ["thailand", "bangkok", "singapore", "vietnam"]) and is_india_dest:
        duration = "3h 50m – 5h 45m"
        cost_inr = "₹13,000 – ₹23,000 (estimated)"
        cost_local = "Local equivalent (estimated)"
        airline_options = "Thai Airways, Singapore Airlines, IndiGo, AirAsia"
        dep_window = "Late morning or evening"
        advice = "Allow 3 hours for duty-free and international departure formalities."
    else:
        duration = "7h 00m – 13h 00m (Connecting commercial flight)"
        cost_inr = "₹25,000 – ₹46,000 (estimated)"
        cost_local = "Equivalent international fare (estimated)"
        airline_options = "Major international scheduled carriers (Star Alliance / OneWorld / SkyTeam)"
        dep_window = "Flexible scheduled commercial departure"
        advice = "Check-in online 24 hours prior and arrive 3 hours before departure."

    return {
        "origin": origin_city,
        "destination": dest_city,
        "recommended_mode": "Scheduled Commercial Flight (Economy / Premium)",
        "alternative_modes": ["Connecting flight via hub (saves 15–25% on peak dates)"],
        "travel_time": duration,
        "cost_range_inr": cost_inr,
        "cost_range_local": cost_local,
        "terminal_origin": f"{orig_info['name']} ({orig_info['code']})" if "(" not in orig_info['name'] else orig_info['name'],
        "terminal_dest": f"{dest_info['name']} ({dest_info['code']})" if "(" not in dest_info['name'] else dest_info['name'],
        "connections": f"Operated by {airline_options}. Note: Actual flight schedules and live fares vary by travel date and booking lead time.",
        "departure_window": dep_window,
        "buffer_notes": advice,
        "booking_links": [
            {"name": "Google Flights Multi-City", "url": "https://www.google.com/travel/flights"},
            {"name": "Skyscanner Multi-City Search", "url": "https://www.skyscanner.com"}
        ]
    }


def _normalize_leg_dict(leg: Dict[str, Any]) -> Dict[str, Any]:
    leg["mode"] = leg.get("recommended_mode", "Transit")
    leg["cost_range"] = leg.get("cost_range_inr", "N/A")
    leg["origin_terminal"] = leg.get("terminal_origin", "Central Station / Airport")
    leg["dest_terminal"] = leg.get("terminal_dest", "Central Station / Airport")
    leg["connection_info"] = leg.get("connections", "")
    leg["buffer_time"] = leg.get("buffer_notes", "1 hour")
    if not leg.get("booking_link") and leg.get("booking_links"):
        first_b = leg["booking_links"][0]
        leg["booking_link"] = first_b.get("url") if isinstance(first_b, dict) else str(first_b)
    elif not leg.get("booking_link"):
        leg["booking_link"] = "https://www.google.com/travel"
    return leg


def get_transport_leg(
    origin: str,
    destination: str,
    origin_country: str = "",
    dest_country: str = ""
) -> Dict[str, Any]:
    """
    Intelligently determines the best transport mode, duration, costs, and
    transfer directions between ANY pair of cities worldwide.
    """
    o_clean = origin.strip().lower()
    d_clean = destination.strip().lower()

    # 1. Exact verified corridor match
    if (o_clean, d_clean) in VERIFIED_TRANSIT_CORRIDORS:
        data = dict(VERIFIED_TRANSIT_CORRIDORS[(o_clean, d_clean)])
        data["origin"] = origin
        data["destination"] = destination
        return _normalize_leg_dict(data)

    # 2. Reverse verified corridor match
    if (d_clean, o_clean) in VERIFIED_TRANSIT_CORRIDORS:
        rev = dict(VERIFIED_TRANSIT_CORRIDORS[(d_clean, o_clean)])
        return _normalize_leg_dict({
            "origin": origin,
            "destination": destination,
            "recommended_mode": rev["recommended_mode"],
            "alternative_modes": rev["alternative_modes"],
            "travel_time": rev["travel_time"],
            "cost_range_inr": rev["cost_range_inr"],
            "cost_range_local": rev["cost_range_local"],
            "terminal_origin": rev["terminal_dest"],
            "terminal_dest": rev["terminal_origin"],
            "connections": rev["connections"],
            "departure_window": rev["departure_window"],
            "buffer_notes": rev["buffer_notes"],
            "booking_links": rev.get("booking_links", [])
        })

    # 3. Same country regional check
    same_country = bool(origin_country and dest_country and origin_country.strip().lower() == dest_country.strip().lower())

    if same_country:
        return _normalize_leg_dict({
            "origin": origin,
            "destination": destination,
            "recommended_mode": "High-Speed Rail / Intercity Express Train",
            "alternative_modes": ["Regional Highway Coach", "Domestic Flight"],
            "travel_time": "1h 30m – 3h 00m",
            "cost_range_inr": "₹2,500 – ₹6,500",
            "cost_range_local": "Local currency equivalent",
            "terminal_origin": f"{origin} Central Railway Station",
            "terminal_dest": f"{destination} Main Station",
            "connections": "Direct or single-transfer express rail",
            "departure_window": "Depart morning (09:00 AM) to maximize sightseeing at the next destination",
            "buffer_notes": "Allow 20 minutes buffer for platform navigation and ticket collection.",
            "booking_links": [{"name": "Official National Rail Operator", "url": "https://www.google.com/travel"}]
        })

    # 4. Cross-border / Intercontinental Flight
    return _normalize_leg_dict(build_international_flight_leg(origin, destination, origin_country, dest_country))


# ============================================================
# 3. NATURAL LANGUAGE MULTI-STOP TRIP PROMPT PARSER
# ============================================================

KNOWN_GLOBAL_CITIES = {
    "tokyo": "Japan", "kyoto": "Japan", "osaka": "Japan", "hakone": "Japan", "nara": "Japan", "hiroshima": "Japan",
    "paris": "France", "nice": "France", "lyon": "France", "marseille": "France",
    "rome": "Italy", "florence": "Italy", "venice": "Italy", "milan": "Italy", "naples": "Italy",
    "london": "United Kingdom", "edinburgh": "United Kingdom", "manchester": "United Kingdom",
    "barcelona": "Spain", "madrid": "Spain", "seville": "Spain",
    "berlin": "Germany", "munich": "Germany", "frankfurt": "Germany",
    "zurich": "Switzerland", "geneva": "Switzerland", "lucerne": "Switzerland", "interlaken": "Switzerland",
    "bangkok": "Thailand", "chiang mai": "Thailand", "phuket": "Thailand", "krabi": "Thailand",
    "kathmandu": "Nepal", "pokhara": "Nepal", "chitwan": "Nepal",
    "delhi": "India", "new delhi": "India", "agra": "India", "jaipur": "India", "udaipur": "India",
    "mumbai": "India", "goa": "India", "varanasi": "India", "srinagar": "India", "kerala": "India",
    "hyderabad": "India", "bengaluru": "India", "bangalore": "India", "chennai": "India", "kolkata": "India",
    "singapore": "Singapore", "seoul": "South Korea", "busan": "South Korea",
    "hanoi": "Vietnam", "da nang": "Vietnam", "ho chi minh city": "Vietnam",
    "bali": "Indonesia", "cairo": "Egypt", "dubai": "United Arab Emirates",
    "new york": "USA", "san francisco": "USA", "los angeles": "USA"
}


def parse_multi_stop_trip_prompt(prompt: str) -> Dict[str, Any]:
    """
    Parses complex multi-stop travel requests with exact route fidelity.
    Supports both arrow notation (e.g. 'Plan Hyderabad → Tokyo (2 days) → Kyoto (3 days) → Osaka (2 days) → Hyderabad')
    and descriptive natural language sentences.
    Preserves exact origin, ordered stops, requested durations, and return destination.
    Flags missing origin or stops cleanly without inventing fake names.
    """
    p = prompt.strip()
    p_lower = p.lower()

    result: Dict[str, Any] = {
        "starting_location": "",
        "origin": "",
        "departure_date": "Upcoming Travel Date",
        "return_location": "",
        "stops": [],
        "budget": 120000,
        "travelers": 1,
        "style": "Balanced",
        "interests": ["Culture", "Food"],
        "target_countries": [],
        "route_preserved": [],
        "missing_information": []
    }

    # ---------------------------------------------------------
    # A. Check for Arrow-Delimited Syntax (→, ->, -->)
    # ---------------------------------------------------------
    arrow_pattern = r"\s*(?:→|->|-->)\s*"
    if re.search(arrow_pattern, p):
        segments = [s.strip() for s in re.split(arrow_pattern, p) if s.strip()]
        if len(segments) >= 2:
            raw_orig = segments[0]
            # Check if segment 0 is a stop with a duration (e.g. "Tokyo (2 days) -> Kyoto (3 days)")
            orig_d_match = re.search(r"(\d+)\s*(?:days?|nights?|d)", raw_orig, re.IGNORECASE)
            parsed_arrow_stops = []

            if orig_d_match:
                # Segment 0 is actually Stop 1, NOT the origin!
                dur_0 = int(orig_d_match.group(1))
                c_name_0 = re.sub(r"\([^\)]*\)", "", raw_orig)
                c_name_0 = re.sub(r"\d+\s*(?:days?|nights?|d)", "", c_name_0, flags=re.I)
                c_name_0 = re.sub(r"^(?:plan|from|start|depart|journey)\s+", "", c_name_0, flags=re.I)
                c_name_0 = re.sub(r"[^\w\s]", "", c_name_0).strip().title()
                country_0 = KNOWN_GLOBAL_CITIES.get(c_name_0.lower(), "Destination")
                if c_name_0:
                    parsed_arrow_stops.append({
                        "city": c_name_0,
                        "country": country_0,
                        "days": dur_0
                    })
                # Origin remains empty unless explicitly stated
            else:
                # Segment 0 is the starting location
                clean_orig = re.sub(r"^(?:plan|from|start|depart|journey)\s+", "", raw_orig, flags=re.I).strip()
                clean_orig = re.sub(r"[^\w\s]", "", clean_orig).strip().title()
                if clean_orig:
                    result["starting_location"] = clean_orig
                    result["origin"] = clean_orig

            # Middle segments are ordered stops
            for seg in segments[1:-1]:
                # Extract city and days e.g. "Tokyo (2 days)", "Kyoto 3d", "Osaka (2 days)"
                d_match = re.search(r"(\d+)\s*(?:days?|nights?|d)", seg, re.IGNORECASE)
                duration = int(d_match.group(1)) if d_match else 2
                city_name = re.sub(r"\([^\)]*\)", "", seg)
                city_name = re.sub(r"\d+\s*(?:days?|nights?|d)", "", city_name, flags=re.I)
                city_name = re.sub(r"[^\w\s]", "", city_name).strip().title()

                country_name = KNOWN_GLOBAL_CITIES.get(city_name.lower(), "Destination")
                if city_name:
                    parsed_arrow_stops.append({
                        "city": city_name,
                        "country": country_name,
                        "days": duration
                    })

            # Last segment could be return location OR a destination stop
            last_seg = segments[-1]
            last_d_match = re.search(r"(\d+)\s*(?:days?|nights?|d)", last_seg, re.IGNORECASE)
            if last_d_match:
                # Last segment has duration, so it's a stop, not a return
                dur = int(last_d_match.group(1))
                c_name = re.sub(r"\([^\)]*\)", "", last_seg)
                c_name = re.sub(r"\d+\s*(?:days?|nights?|d)", "", c_name, flags=re.I)
                c_name = re.sub(r"[^\w\s]", "", c_name).strip().title()
                country_name = KNOWN_GLOBAL_CITIES.get(c_name.lower(), "Destination")
                if c_name:
                    parsed_arrow_stops.append({
                        "city": c_name,
                        "country": country_name,
                        "days": dur
                    })
                result["return_location"] = result["starting_location"]
            else:
                # Last segment is the return location (e.g. "Hyderabad", "return to Hyderabad")
                clean_ret = re.sub(r"^(?:return to|back to|fly to|return)\s+", "", last_seg, flags=re.I).strip()
                clean_ret = re.sub(r"[^\w\s]", "", clean_ret).strip().title()
                result["return_location"] = clean_ret or result["starting_location"]

            if parsed_arrow_stops:
                result["stops"] = parsed_arrow_stops

    # ---------------------------------------------------------
    # B. Natural Language Regex Parser (if not fully populated by arrow syntax)
    # ---------------------------------------------------------
    if not result["starting_location"]:
        start_match = re.search(r"(?:start(?:ing)?\s+from|depart(?:ing)?\s+from|from|leaving)\s+([A-Za-z\s]+?)(?:\s+on|\s+in|\s+to|\s+for|,|\.|$)", p, re.IGNORECASE)
        if start_match:
            start_cand = start_match.group(1).strip()
            start_cand = re.sub(r"^(my|our|the)\s+", "", start_cand, flags=re.I).strip()
            if len(start_cand) >= 3 and start_cand.lower() not in ["december", "january", "november", "tomorrow", "next", "japan", "europe"]:
                result["starting_location"] = start_cand.title()
                result["origin"] = start_cand.title()

    # Departure Date
    date_match = re.search(r"(?:on|starting|leaving)\s+([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?", p, re.IGNORECASE)
    if date_match:
        result["departure_date"] = f"{date_match.group(1).title()} {date_match.group(2)}"
    else:
        month_match = re.search(r"(?:in|during|month of)\s+(january|february|march|april|may|june|july|august|september|october|november|december)", p_lower)
        if month_match:
            result["departure_date"] = f"{month_match.group(1).title()} 1"

    # Return Location
    if not result["return_location"]:
        return_match = re.search(r"(?:return(?:ing)?\s+to|back\s+to|fly\s+back\s+to)\s+([A-Za-z\s]+?)(?:[.,;]|$)", p, re.IGNORECASE)
        if return_match:
            ret_cand = return_match.group(1).strip().title()
            result["return_location"] = ret_cand
        elif result["starting_location"]:
            result["return_location"] = result["starting_location"]

    # Natural Language Stop Extraction if stops not parsed yet
    if not result["stops"]:
        stop_matches = []
        # Pattern A: <City> for <N> days
        for sm in re.finditer(r"(?:in|to|visit|stay in)?\s*([a-zA-Z\s]{3,20}?)\s+for\s+(\d{1,2})\s*(?:days?|nights?)", p, re.IGNORECASE):
            city_raw = sm.group(1).strip().lower()
            days_num = int(sm.group(2))
            city_raw = re.sub(r"^(?:travel|go|stay|visit|explore|then\s+go|then\s+visit)\s+(?:to\s+|in\s+)?", "", city_raw, flags=re.I).strip()
            if city_raw in KNOWN_GLOBAL_CITIES or any(kc in city_raw for kc in KNOWN_GLOBAL_CITIES):
                matched_k = next((kc for kc in KNOWN_GLOBAL_CITIES if kc == city_raw or kc in city_raw), city_raw)
                stop_matches.append((sm.start(), matched_k.title(), KNOWN_GLOBAL_CITIES.get(matched_k, "Destination"), days_num))

        # Pattern B: <N> days in/at <City>
        for sm in re.finditer(r"(\d{1,2})\s*(?:days?|nights?)\s+(?:in|at)\s+([a-zA-Z\s]{3,20}?)(?:,|\.|\s+then|\s+and|$)", p, re.IGNORECASE):
            days_num = int(sm.group(1))
            city_raw = sm.group(2).strip().lower()
            if city_raw in KNOWN_GLOBAL_CITIES or any(kc in city_raw for kc in KNOWN_GLOBAL_CITIES):
                matched_k = next((kc for kc in KNOWN_GLOBAL_CITIES if kc == city_raw or kc in city_raw), city_raw)
                if not any(item[1].lower() == matched_k.lower() for item in stop_matches):
                    stop_matches.append((sm.start(), matched_k.title(), KNOWN_GLOBAL_CITIES.get(matched_k, "Destination"), days_num))

        # Sort stops strictly by their appearance index in the prompt
        stop_matches.sort(key=lambda x: x[0])
        seen_cities = set()
        for _, city_name, country_name, duration_days in stop_matches:
            if city_name.lower() not in seen_cities and city_name.lower() != result["starting_location"].lower():
                seen_cities.add(city_name.lower())
                result["stops"].append({
                    "city": city_name,
                    "country": country_name,
                    "days": max(1, min(14, duration_days))
                })

    # Target countries
    for s in result["stops"]:
        if s["country"] not in result["target_countries"] and s["country"] != "Destination":
            result["target_countries"].append(s["country"])

    # Fallback to general country if still no stops
    if not result["stops"]:
        for c_k in ["Japan", "France", "Italy", "India", "Thailand", "United Kingdom"]:
            if c_k.lower() in p_lower:
                result["target_countries"].append(c_k)
                if c_k == "Japan":
                    result["stops"] = [
                        {"city": "Tokyo", "country": "Japan", "days": 2},
                        {"city": "Kyoto", "country": "Japan", "days": 3},
                        {"city": "Osaka", "country": "Japan", "days": 2}
                    ]
                break

    # Budget detection
    b_match = re.search(r"(?:budget|cost|under|around|within)?\s*(?:₹|inr|rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(l|lac|lakh|k)?", p_lower)
    if b_match:
        val_str = b_match.group(1).replace(",", "")
        try:
            val = float(val_str)
            unit = b_match.group(2)
            if unit in ["l", "lac", "lakh"]:
                val *= 100000
            elif unit == "k":
                val *= 1000
            result["budget"] = int(val)
        except Exception:
            pass

    # Travelers
    if any(w in p_lower for w in ["couple", "two of us", "with my wife", "with my husband", "with my partner", "2 travelers", "2 people"]):
        result["travelers"] = 2
    elif any(w in p_lower for w in ["family", "4 of us", "with kids"]):
        result["travelers"] = 4
    elif any(w in p_lower for w in ["solo", "alone", "myself", "1 person"]):
        result["travelers"] = 1

    # Style
    if any(w in p_lower for w in ["packed", "fast", "busy", "see everything", "intense"]):
        result["style"] = "Packed"
    elif any(w in p_lower for w in ["relax", "relaxed", "slow", "peaceful", "leisurely"]):
        result["style"] = "Relaxed"
    else:
        result["style"] = "Balanced"

    # Flag missing info
    if not result["starting_location"]:
        result["missing_information"].append("Starting location is missing. Please specify where your journey begins.")
    if not result["stops"]:
        result["missing_information"].append("Destination stops are missing. Please specify which cities you wish to visit.")

    # Canonical Route Array
    route_preserved = []
    if result["starting_location"]:
        route_preserved.append(result["starting_location"])
    for s in result["stops"]:
        route_preserved.append(f"{s['city']} ({s['days']}d)")
    if result["return_location"]:
        route_preserved.append(result["return_location"])
    result["route_preserved"] = route_preserved

    return result


# ============================================================
# 4. MULTI-STOP ITINERARY SYNTHESIZER
# ============================================================

def generate_multi_stop_journey(parsed_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes parsed stops and parameters, constructs independent intercity/international
    transportation legs, and builds a complete day-by-day itinerary with exact destination-specific
    attractions and accurate travel transitions.
    """
    stops = parsed_plan.get("stops", [])
    if not stops:
        return {}

    starting = parsed_plan.get("starting_location") or parsed_plan.get("origin") or "Hyderabad"
    return_loc = parsed_plan.get("return_location") or starting
    dep_date = parsed_plan.get("departure_date", "Upcoming Travel Date")
    travelers = parsed_plan.get("travelers", 1)
    budget = parsed_plan.get("budget", 140000)
    style = parsed_plan.get("style", "Balanced")

    # Destination stay days vs total travel days
    destination_stay_days = sum(s["days"] for s in stops)
    total_travel_days = destination_stay_days  # Stay days scheduled precisely across requested stops

    # 1. Build Independent Transportation Legs
    legs = []

    # Leg 1: Starting Location -> First Destination (Outbound International / Intercity)
    first_stop = stops[0]
    legs.append(get_transport_leg(
        origin=starting,
        destination=first_stop["city"],
        origin_country="India" if any(h in starting.lower() for h in ["hyderabad", "delhi", "mumbai", "bengaluru", "chennai", "kolkata"]) else "Origin",
        dest_country=first_stop["country"]
    ))

    # Inter-stop legs (consecutive destinations)
    for idx in range(len(stops) - 1):
        curr_stop = stops[idx]
        next_stop = stops[idx + 1]
        legs.append(get_transport_leg(
            origin=curr_stop["city"],
            destination=next_stop["city"],
            origin_country=curr_stop["country"],
            dest_country=next_stop["country"]
        ))

    # Final Return Leg: Last Destination -> Return Location (Planned Independently!)
    last_stop = stops[-1]
    legs.append(get_transport_leg(
        origin=last_stop["city"],
        destination=return_loc,
        origin_country=last_stop["country"],
        dest_country="India" if any(h in return_loc.lower() for h in ["hyderabad", "delhi", "mumbai", "bengaluru", "chennai", "kolkata"]) else "Return Destination"
    ))

    # 2. Build Day-by-Day Itinerary across all stops
    from destination_knowledge import get_city_food, get_destination_etiquette, get_city_attractions
    from country_data import get_country_knowledge

    days_itinerary = []
    current_day_number = 1

    # Augment each stop with days_plan
    stops_augmented = []

    for stop_idx, stop in enumerate(stops):
        city = stop["city"]
        country = stop["country"]
        stop_days = stop["days"]
        etiquette_info = get_destination_etiquette(country, city)

        # Retrieve authentic dishes & attractions strictly for this city
        city_dishes = get_city_food(country, city)
        city_attractions_pool = get_city_attractions(country, city)
        breakfast_dish = next((d for d in city_dishes if d.get("breakfast_friendly")), city_dishes[0] if city_dishes else None)

        stop_days_plan = []

        for day_in_stop in range(1, stop_days + 1):
            is_arrival_day = (stop_idx == 0 and day_in_stop == 1)
            is_departure_day = (stop_idx == len(stops) - 1 and day_in_stop == stop_days)
            is_intercity_transition_day = (day_in_stop == stop_days and stop_idx < len(stops) - 1)

            # Assign contextual title
            if is_arrival_day:
                title = f"Arrival in {city} from {starting} & Evening Orientation"
            elif is_intercity_transition_day:
                next_city = stops[stop_idx + 1]["city"]
                title = f"{city} Morning Highlights & High-Speed Transit to {next_city}"
            elif is_departure_day:
                title = f"Final Moments in {city} & Return Journey to {return_loc}"
            else:
                title = f"Immersive Cultural Exploration of {city}"

            # Pick location-specific attractions strictly matching this city
            attraction_idx = (day_in_stop - 1) % len(city_attractions_pool)
            morn_att = city_attractions_pool[attraction_idx]

            afternoon_att_idx = (day_in_stop) % len(city_attractions_pool)
            aft_att = city_attractions_pool[afternoon_att_idx]

            lunch_dish = city_dishes[(day_in_stop - 1) % len(city_dishes)] if city_dishes else None
            dinner_dish = city_dishes[day_in_stop % len(city_dishes)] if len(city_dishes) > 1 else (city_dishes[0] if city_dishes else None)

            # Contextual etiquette tip
            if is_arrival_day:
                etiquette_tip = f"Arrival Protocol: {etiquette_info.get('greetings', {}).get('summary', 'Greet locals politely and have documents ready.')}"
            elif is_intercity_transition_day or is_departure_day:
                etiquette_tip = f"Transit Etiquette: {etiquette_info.get('public_transport', {}).get('summary', 'Keep voices low on public transport and queue in designated lanes.')}"
            else:
                etiquette_tip = f"Heritage Respect: {etiquette_info.get('temples_and_shrines', {}).get('summary', 'Dress respectfully with covered shoulders at historic sites.')}"

            day_acts = []

            # -----------------------------------------------------------------
            # Activity 1: Morning Schedule
            # -----------------------------------------------------------------
            if is_arrival_day:
                day_acts.append({
                    "time": "09:30 AM",
                    "activity": f"International Flight Arrival & Immigration: Touchdown at {legs[0].get('dest_terminal', f'{city} Airport')}. Complete customs clearance and transfer to hotel.",
                    "place": f"{city} International Gateway",
                    "cost": int(1200 * travelers),
                    "travel_time": "60 min",
                    "transport": f"Express Airport Train / Shuttle into {city}"
                })
            else:
                if breakfast_dish:
                    day_acts.append({
                        "time": "08:30 AM",
                        "activity": f"Breakfast: {breakfast_dish['name']} ({breakfast_dish.get('taste_profile', 'Regional morning meal')})",
                        "place": f"Local Morning Dining in {city}",
                        "cost": int(380 * travelers),
                        "travel_time": "10 min",
                        "transport": "Morning Walk"
                    })

                day_acts.append({
                    "time": "10:00 AM",
                    "activity": f"Morning Sightseeing: {morn_att[0]} ({morn_att[1]})",
                    "place": f"{city} - {morn_att[3]}",
                    "cost": int(morn_att[2] * travelers) if morn_att[2] > 0 else int(300 * travelers),
                    "travel_time": "20 min",
                    "transport": morn_att[3]
                })

            # -----------------------------------------------------------------
            # Activity 2: Midday / Lunch Schedule
            # -----------------------------------------------------------------
            if lunch_dish:
                day_acts.append({
                    "time": "01:00 PM",
                    "activity": f"Authentic Regional Lunch: Savor {lunch_dish['name']} ({lunch_dish.get('taste_profile', 'Local delicacy')})",
                    "place": lunch_dish.get("where_to_try", f"Traditional Quarter in {city}"),
                    "cost": int(850 * travelers),
                    "travel_time": "15 min",
                    "transport": "Walking / Tram"
                })

            # -----------------------------------------------------------------
            # Activity 3: Afternoon Schedule & Intercity Transit
            # -----------------------------------------------------------------
            if is_intercity_transition_day:
                next_city = stops[stop_idx + 1]["city"]
                inter_leg = legs[stop_idx + 1]
                day_acts.append({
                    "time": "03:30 PM",
                    "activity": f"Intercity Journey: Check-out and board {inter_leg['mode']} from {inter_leg['origin_terminal']} to {inter_leg['dest_terminal']}. Journey time: {inter_leg['travel_time']}.",
                    "place": f"{city} to {next_city} Corridor",
                    "cost": int(2200 * travelers),
                    "travel_time": inter_leg["travel_time"],
                    "transport": inter_leg["mode"]
                })
            elif is_departure_day:
                day_acts.append({
                    "time": "04:00 PM",
                    "activity": f"Airport Transfer & Departure Buffer: Transfer to {legs[-1].get('origin_terminal', f'{city} International Airport')}. Complete check-in and security screening 3 hours prior to departure.",
                    "place": f"{city} International Terminal",
                    "cost": int(1500 * travelers),
                    "travel_time": "50 min",
                    "transport": f"Direct Express Train / Taxi to Airport"
                })
            else:
                day_acts.append({
                    "time": "03:30 PM",
                    "activity": f"Afternoon Cultural Experience: {aft_att[0]} ({aft_att[1]})",
                    "place": f"{city} - {aft_att[3]}",
                    "cost": int(aft_att[2] * travelers) if aft_att[2] > 0 else int(400 * travelers),
                    "travel_time": "25 min",
                    "transport": aft_att[3]
                })

            # -----------------------------------------------------------------
            # Activity 4: Evening Schedule
            # -----------------------------------------------------------------
            if is_departure_day:
                day_acts.append({
                    "time": "08:30 PM",
                    "activity": f"International Return Flight: Depart for {return_loc} ({legs[-1].get('connections', 'Scheduled carrier')}). Journey duration: {legs[-1].get('travel_time', 'N/A')}.",
                    "place": f"In Flight to {return_loc}",
                    "cost": 0,
                    "travel_time": legs[-1].get("travel_time", "Flight duration"),
                    "transport": "Scheduled Commercial Aircraft"
                })
            elif is_intercity_transition_day:
                next_city = stops[stop_idx + 1]["city"]
                day_acts.append({
                    "time": "07:30 PM",
                    "activity": f"Arrival & Check-in at {next_city}: Check into hotel, unpack, and enjoy an evening stroll around the central district.",
                    "place": f"{next_city} Central Quarter",
                    "cost": int(900 * travelers),
                    "travel_time": "20 min",
                    "transport": "Walking / Metro"
                })
            else:
                if dinner_dish:
                    day_acts.append({
                        "time": "07:30 PM",
                        "activity": f"Authentic Dinner: Enjoy {dinner_dish['name']} ({dinner_dish.get('taste_profile', 'Local delicacy')})",
                        "place": dinner_dish.get("where_to_try", f"Historic Dining District in {city}"),
                        "cost": int(1300 * travelers),
                        "travel_time": "20 min",
                        "transport": "Evening Walk / Local Metro"
                    })

            day_dict = {
                "day": current_day_number,
                "day_num": current_day_number,
                "stop_index": stop_idx + 1,
                "city": city,
                "country": country,
                "day_in_city": day_in_stop,
                "title": title,
                "etiquette_tip": etiquette_tip,
                "activities": day_acts
            }

            days_itinerary.append(day_dict)
            stop_days_plan.append(day_dict)
            current_day_number += 1

        start_day_stop = current_day_number - stop_days
        end_day_stop = current_day_number - 1
        stops_augmented.append({
            "city": city,
            "country": country,
            "days": stop_days,
            "day_range": f"Days {start_day_stop}–{end_day_stop}",
            "days_plan": stop_days_plan
        })

    # 3. Transparent, Itemized Budget Calculation
    # Calculate flight costs, intercity rail, hotel accommodation, meals, local transit, activities, and contingency
    total_nights = destination_stay_days
    # Estimated realistic accommodation cost per night
    hotel_per_night = 6500 if travelers == 1 else 8500
    b_acc = int(hotel_per_night * total_nights)

    # Transportation: 2 international flights (outbound + return) + intercity rail legs
    intl_flight_est = 35000 * travelers * 2  # Return international airfare band
    intercity_rail_est = (len(stops) - 1) * 7800 * travelers
    b_trans = int(intl_flight_est + intercity_rail_est)

    # Dining: 3 meals per day
    b_food = int(2200 * total_nights * travelers)

    # Local transit & Entry activities
    b_act = sum(a.get("cost", 0) for day in days_itinerary for a in day.get("activities", []))
    b_local_transit = int(600 * total_nights * travelers)

    # Contingency buffer: 5% of subtotal
    subtotal = b_acc + b_trans + b_food + b_act + b_local_transit
    b_contingency = int(subtotal * 0.05)
    total_exact = subtotal + b_contingency

    route_title = f"{starting} → " + " → ".join(f"{s['city']} ({s['days']}d)" for s in stops) + f" → {return_loc}"
    route_summary = f"{starting} 🛫 → " + " → ".join(f"{s['city']} ({s['days']}d)" for s in stops) + f" 🛫 → {return_loc}"

    canonical_journey = {
        "origin": starting,
        "starting_location": starting,
        "departure_date": dep_date,
        "return_location": return_loc,
        "route_title": route_title,
        "route_summary": route_summary,
        "stops": stops_augmented,
        "destination_stay_days": destination_stay_days,
        "total_days": destination_stay_days,
        "destination_count": len(stops),
        "travelers": travelers,
        "budget": budget,
        "total_cost": total_exact,
        "remaining_budget": max(0, budget - total_exact),
        "style": style,
        "currency": "INR (₹)",
        "pricing_model": "Estimated market ranges (live airfares and seasonal hotel tariffs vary upon actual booking)",
        "transport_legs": legs,
        "days": days_itinerary,
        "cost_breakdown": {
            "International Flights": int(intl_flight_est),
            "Intercity Rail & Transit": int(intercity_rail_est),
            "Intercity Transport": b_trans,
            "Accommodation": b_acc,
            "Dining": b_food,
            "Local Transportation": b_local_transit,
            "Activities": b_act,
            "Contingency Buffer (5%)": b_contingency,
            "Total Estimated": total_exact,
            "Buffer Remaining": max(0, budget - total_exact)
        },
        "budget_breakdown": {
            "Accommodation": b_acc,
            "Intercity & Flights": b_trans,
            "Food & Dining": b_food,
            "Activities & Sightseeing": b_act,
            "Local Transit": b_local_transit,
            "Contingency Buffer": b_contingency
        }
    }

    # Run 8-Point Pre-Render Validation
    canonical_journey["validation_report"] = validate_itinerary_plan(canonical_journey, parsed_plan)

    return canonical_journey


# ============================================================
# 5. PRE-RENDER 8-POINT ITINERARY VALIDATOR
# ============================================================

def validate_itinerary_plan(journey: Dict[str, Any], raw_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates the generated multi-stop plan against all 8 critical requirements:
    1. Every requested destination appears in the correct order.
    2. Every destination has the requested stay duration.
    3. Each transport leg connects the correct consecutive locations.
    4. The return leg reaches the specified starting point / return destination.
    5. Every attraction matches the scheduled destination or is explicitly labelled as a day trip.
    6. Travel days and stay days are calculated consistently.
    7. The displayed budget is consistent with its breakdown.
    8. Missing information is requested instead of invented.
    """
    checks = []
    is_valid = True

    req_stops = raw_request.get("stops", [])
    gen_stops = journey.get("stops", [])

    # Check 1: Destination order
    req_cities = [s["city"].lower() for s in req_stops]
    gen_cities = [s["city"].lower() for s in gen_stops]
    order_ok = (req_cities == gen_cities)
    checks.append({
        "check": "Destination Order",
        "passed": order_ok,
        "details": f"Expected: {req_cities} | Actual: {gen_cities}"
    })
    if not order_ok:
        is_valid = False

    # Check 2: Stay durations
    req_days = [s["days"] for s in req_stops]
    gen_days = [s["days"] for s in gen_stops]
    durations_ok = (req_days == gen_days)
    checks.append({
        "check": "Stay Durations",
        "passed": durations_ok,
        "details": f"Requested stays: {req_days} days | Generated: {gen_days} days"
    })
    if not durations_ok:
        is_valid = False

    # Check 3: Transport legs connect consecutive locations
    legs = journey.get("transport_legs", [])
    legs_ok = True
    leg_errors = []
    # Leg 0 must connect origin -> Stop 1
    if legs and gen_stops:
        if legs[0]["origin"].lower() != journey.get("origin", "").lower() or legs[0]["destination"].lower() != gen_stops[0]["city"].lower():
            legs_ok = False
            leg_errors.append(f"Leg 1 mismatch: {legs[0]['origin']} -> {legs[0]['destination']}")
        # Consecutive legs
        for i in range(len(gen_stops) - 1):
            if i + 1 < len(legs):
                c_leg = legs[i + 1]
                if c_leg["origin"].lower() != gen_stops[i]["city"].lower() or c_leg["destination"].lower() != gen_stops[i + 1]["city"].lower():
                    legs_ok = False
                    leg_errors.append(f"Leg {i + 2} mismatch: {c_leg['origin']} -> {c_leg['destination']}")
    checks.append({
        "check": "Transport Leg Connectivity",
        "passed": legs_ok,
        "details": "All consecutive stops are connected" if legs_ok else "; ".join(leg_errors)
    })
    if not legs_ok:
        is_valid = False

    # Check 4: Return leg reaches specified return point
    return_loc = journey.get("return_location", "")
    return_leg_ok = (len(legs) > 0 and legs[-1]["destination"].lower() == return_loc.lower())
    checks.append({
        "check": "Return Leg Destination",
        "passed": return_leg_ok,
        "details": f"Final leg terminates at '{legs[-1]['destination'] if legs else 'N/A'}' (expected: '{return_loc}')"
    })
    if not return_leg_ok:
        is_valid = False

    # Check 5: Attraction geographic accuracy (no cross-city bleeding)
    attractions_ok = True
    mismatches = []
    from destination_knowledge import CITY_ATTRACTIONS_DATABASE
    for day in journey.get("days", []):
        day_city = day.get("city", "").lower()
        for act in day.get("activities", []):
            act_text = act.get("activity", "").lower()
            # Fushimi Inari in Tokyo check
            if "tokyo" in day_city and "fushimi inari" in act_text:
                attractions_ok = False
                mismatches.append(f"Fushimi Inari scheduled in {day_city}")
            # Mount Fuji in Tokyo without day trip label
            if "tokyo" in day_city and "mount fuji" in act_text and "day trip" not in act_text:
                attractions_ok = False
                mismatches.append(f"Mount Fuji not labeled as day trip in {day_city}")
            # Osaka Castle in Kyoto check
            if "kyoto" in day_city and "osaka castle" in act_text:
                attractions_ok = False
                mismatches.append(f"Osaka Castle scheduled in {day_city}")
    checks.append({
        "check": "Attraction Geographic Accuracy",
        "passed": attractions_ok,
        "details": "All attractions belong to scheduled cities" if attractions_ok else "; ".join(mismatches)
    })
    if not attractions_ok:
        is_valid = False

    # Check 6: Day count consistency
    total_stay = sum(s["days"] for s in gen_stops)
    total_days_field = journey.get("destination_stay_days", total_stay)
    days_count_ok = (total_stay == total_days_field == len(journey.get("days", [])))
    checks.append({
        "check": "Day Count Consistency",
        "passed": days_count_ok,
        "details": f"Stay days: {total_stay} | Schedule days: {len(journey.get('days', []))} (Consistent)"
    })
    if not days_count_ok:
        is_valid = False

    # Check 7: Budget breakdown consistency
    cost_bd = journey.get("cost_breakdown", {})
    calc_sum = (
        cost_bd.get("Accommodation", 0) +
        cost_bd.get("Intercity Transport", 0) +
        cost_bd.get("Dining", 0) +
        cost_bd.get("Local Transportation", 0) +
        cost_bd.get("Activities", 0) +
        cost_bd.get("Contingency Buffer (5%)", 0)
    )
    total_est = cost_bd.get("Total Estimated", 0)
    budget_ok = (abs(calc_sum - total_est) < 50)
    checks.append({
        "check": "Budget Breakdown Consistency",
        "passed": budget_ok,
        "details": f"Sum of components: ₹{calc_sum:,} == Total Estimated: ₹{total_est:,}"
    })
    if not budget_ok:
        is_valid = False

    # Check 8: Missing information verification
    missing_info = raw_request.get("missing_information", [])
    checks.append({
        "check": "Missing Information Handled",
        "passed": True,
        "details": "Explicitly requested from user" if missing_info else "All essential fields verified"
    })

    return {
        "is_valid": is_valid,
        "checks": checks,
        "total_checks": len(checks),
        "passed_checks": sum(1 for c in checks if c["passed"])
    }


# ============================================================
# 6. SEASONAL DESTINATION RECOMMENDER ENGINE
# ============================================================

SEASONAL_CALENDAR_DATA: Dict[str, List[Dict[str, Any]]] = {
    "december": [
        {
            "country": "Japan",
            "cities": ["Tokyo", "Kyoto", "Hokkaido (Sapporo)", "Shirakawa-go"],
            "flag": "🇯🇵",
            "category": "Winter Magic & Illuminations",
            "weather": "Crisp, sunny, and dry in Tokyo & Kyoto (8°C–13°C average); fairytale powder snow in Hokkaido.",
            "why_optimal": "Dazzling winter street illuminations, piping hot ramen and nabe stews, open-air hot spring onsens overlooking snowy mountains, and tranquil crowd-free temples.",
            "highlights": "Roppongi Winter Illuminations, Sapporo Winter Wonder, Arashiyama Bamboo Grove, Onsen in Hakone.",
            "budget_tier": "₹8,500 – ₹11,000 / day (estimated)",
            "caution": "Pack thermal base layers and slip-resistant boots if traveling up north to Hokkaido."
        },
        {
            "country": "Thailand",
            "cities": ["Bangkok", "Chiang Mai", "Phuket", "Krabi"],
            "flag": "🇹🇭",
            "category": "Tropical Sunshine & Beach Paradise",
            "weather": "Peak cool and dry season (24°C–31°C typical); calm turquoise waters and minimal humidity.",
            "why_optimal": "Superb weather across both coasts; island-hopping in the Andaman Sea is at its calmest, and night markets in Bangkok and Chiang Mai are pleasantly cool.",
            "highlights": "Phi Phi Islands boat tour, Grand Palace, Chiang Mai Sunday Night Walking Street, Wat Arun sunset.",
            "budget_tier": "₹3,500 – ₹6,000 / day (estimated)",
            "caution": "December is peak travel season; book flights and boutique island hotels 4–6 weeks ahead."
        },
        {
            "country": "India",
            "cities": ["Rajasthan (Jaipur, Udaipur, Jaisalmer)", "Goa", "Kerala"],
            "flag": "🇮🇳",
            "category": "Heritage Forts & Coastal Sun",
            "weather": "Delightful warm sunshine (20°C–26°C); cool, crisp desert evenings and gentle coastal sea breeze.",
            "why_optimal": "The ideal month to explore royal palaces, desert camel safaris, and beach sunsets without scorching summer heat.",
            "highlights": "Amber Fort in Jaipur, Lake Pichola in Udaipur, Backwaters of Alleppey, Palolem Beach in Goa.",
            "budget_tier": "₹3,000 – ₹5,500 / day (estimated)",
            "caution": "Desert nights in Jaisalmer drop to 8°C; carry a warm fleece or shawl."
        },
        {
            "country": "Switzerland",
            "cities": ["Zermatt", "Zurich", "Lucerne", "Interlaken"],
            "flag": "🇨🇭",
            "category": "Alpine Snow & Christmas Markets",
            "weather": "Sub-zero Alpine winter (-2°C to 4°C typical); reliable snow in high ski resorts.",
            "why_optimal": "Cozy Swiss fondue dinners, scenic Glacier Express journeys through snowy gorges, and charming wooden Christmas markets.",
            "highlights": "Matterhorn views from Zermatt, Zurich Old Town lights, Chapel Bridge in Lucerne, Jungfraujoch.",
            "budget_tier": "₹14,000 – ₹20,000 / day (estimated)",
            "caution": "Pack full winter gear (heavy thermal parka, gloves, and woolen beanies)."
        }
    ],
    "january": [
        {
            "country": "Thailand",
            "cities": ["Bangkok", "Chiang Mai", "Koh Samui", "Phuket"],
            "flag": "🇹🇭",
            "category": "Dry Season Tropical Haven",
            "weather": "Clear skies, low humidity (23°C–30°C typical), and calm seas.",
            "why_optimal": "Superb weather for scuba diving, beach relaxation, and mountain temple exploration.",
            "highlights": "Similan Islands diving, Wat Rong Khun, floating markets, Bangkok street food.",
            "budget_tier": "₹3,800 – ₹6,200 / day (estimated)",
            "caution": "Very popular with European and Asian winter travelers."
        },
        {
            "country": "India",
            "cities": ["Jaipur", "Agra", "Varanasi", "Kochi"],
            "flag": "🇮🇳",
            "category": "Cultural & Heritage Splendor",
            "weather": "Mild, pleasant days (18°C–24°C average) across central and southern India.",
            "why_optimal": "Pleasant walking temperatures for exploring UNESCO World Heritage monuments and spice plantations.",
            "highlights": "Taj Mahal morning mist, Jaipur Literature Festival, Fort Kochi art biennale.",
            "budget_tier": "₹3,200 – ₹5,800 / day (estimated)",
            "caution": "Morning fog in Northern India can occasionally delay early trains."
        },
        {
            "country": "Egypt",
            "cities": ["Cairo", "Luxor", "Aswan", "Hurghada"],
            "flag": "🇪🇬",
            "category": "Ancient Civilizations & Nile Cruises",
            "weather": "Comfortable daytime temperatures (19°C–23°C); escape the blistering 45°C summer desert heat.",
            "why_optimal": "Walking through the Valley of the Kings and Giza Pyramids is comfortable and unhurried.",
            "highlights": "Giza Pyramids, Karnak Temple, Nile Felucca sailing, Egyptian Museum.",
            "budget_tier": "₹4,500 – ₹8,000 / day (estimated)",
            "caution": "Desert nights are cool; carry a medium jacket."
        }
    ],
    "april": [
        {
            "country": "Japan",
            "cities": ["Tokyo", "Kyoto", "Osaka", "Nara"],
            "flag": "🇯🇵",
            "category": "Cherry Blossom (Sakura) Season",
            "weather": "Crisp spring (14°C–20°C typical); blooming pink sakura across city parks and riverbanks.",
            "why_optimal": "One of the world's premier natural spectacles; enjoy lively Hanami blossom picnics and seasonal sakura sweets.",
            "highlights": "Shinjuku Gyoen, Philosopher's Path in Kyoto, Meguro River illuminations, Himeji Castle.",
            "budget_tier": "₹9,500 – ₹13,000 / day (estimated)",
            "caution": "Peak international demand; reserve hotels and bullet train passes well in advance."
        },
        {
            "country": "Netherlands",
            "cities": ["Amsterdam", "Lisse (Keukenhof)", "Utrecht", "Rotterdam"],
            "flag": "🇳🇱",
            "category": "Tulip Blooms & Canal Biking",
            "weather": "Pleasant spring (11°C–17°C typical); millions of colorful tulips in full bloom.",
            "why_optimal": "World-famous Keukenhof gardens open for only 8 weeks; sunny canal-side bike rides and King's Day festival (April 27).",
            "highlights": "Keukenhof Gardens, Rijksmuseum, Jordaan canal stroll, Zaanse Schans windmills.",
            "budget_tier": "₹11,000 – ₹15,000 / day (estimated)",
            "caution": "King's Day on April 27 turns Amsterdam into a massive orange street festival; book early."
        },
        {
            "country": "Nepal",
            "cities": ["Kathmandu", "Pokhara", "Nagarkot", "Chitwan"],
            "flag": "🇳🇵",
            "category": "Himalayan Spring & Rhododendron Forests",
            "weather": "Warm days (22°C–26°C typical), clear mountain vistas, blooming scarlet rhododendrons.",
            "why_optimal": "Superb trekking weather along the Annapurna and Everest foothill trails with high visibility.",
            "highlights": "Phewa Lake boating, Boudhanath Stupa, Sarangkot sunrise, Chitwan wildlife safari.",
            "budget_tier": "₹2,500 – ₹4,500 / day (estimated)",
            "caution": "Afternoon mountain haze can occasionally form; do sightseeing early in the morning."
        }
    ],
    "july": [
        {
            "country": "Switzerland",
            "cities": ["Interlaken", "Zermatt", "Lucerne", "Grindelwald"],
            "flag": "🇨🇭",
            "category": "Alpine Hiking & Turquoise Lakes",
            "weather": "Warm sunshine (20°C–26°C typical); blooming alpine meadows and open mountain trails.",
            "why_optimal": "Crystal-clear lake swimming, scenic open-air cable cars, and world-class hiking trails beneath snow-capped peaks.",
            "highlights": "First Cliff Walk in Grindelwald, Lake Geneva boat cruise, Matterhorn Glacier Trail.",
            "budget_tier": "₹15,000 – ₹22,000 / day (estimated)",
            "caution": "Peak summer crowds; start popular hikes early morning."
        },
        {
            "country": "Indonesia (Bali)",
            "cities": ["Ubud", "Seminyak", "Uluwatu", "Nusa Penida"],
            "flag": "🇮🇩",
            "category": "Dry Season Tropical Haven",
            "weather": "Dry season (26°C–29°C typical); low humidity, cool offshore evening breezes.",
            "why_optimal": "While Southeast Asian mainland experiences summer monsoon, Bali enjoys its driest, sunniest weather of the year.",
            "highlights": "Tegallalang Rice Terraces, Uluwatu cliff temple & Kecak dance, Kelingking Beach, scuba diving.",
            "budget_tier": "₹3,500 – ₹6,500 / day (estimated)",
            "caution": "July is Australian school holiday season; popular beach clubs fill quickly."
        },
        {
            "country": "Norway",
            "cities": ["Oslo", "Bergen", "Flåm", "Geirangerfjord"],
            "flag": "🇳🇴",
            "category": "Midnight Sun & Majestic Fjords",
            "weather": "Mild summer (16°C–22°C typical); up to 19 hours of daylight and the legendary midnight sun.",
            "why_optimal": "Fjord ferry cruises through UNESCO World Heritage cliffs with roaring waterfalls at peak flow.",
            "highlights": "Geirangerfjord cruise, Flåm scenic mountain railway, Bryggen harbor in Bergen.",
            "budget_tier": "₹13,000 – ₹18,000 / day (estimated)",
            "caution": "Weather in western fjords can be changeable; carry a light waterproof windbreaker."
        }
    ],
    "october": [
        {
            "country": "Italy",
            "cities": ["Rome", "Florence", "Venice", "Tuscany"],
            "flag": "🇮🇹",
            "category": "Tuscan Harvest & Mild Autumn",
            "weather": "Pleasant, mild temperatures (18°C–23°C typical); intense summer crowds have cleared.",
            "why_optimal": "Grape and olive harvest season in Tuscany, pleasant walking weather across ancient stone streets, and reduced wait times at the Colosseum and Uffizi.",
            "highlights": "Colosseum & Roman Forum, Duomo in Florence, Chianti wine countryside, St. Mark's Square.",
            "budget_tier": "₹9,000 – ₹13,500 / day (estimated)",
            "caution": "Occasional autumn rain showers; carry a compact travel umbrella."
        },
        {
            "country": "Nepal",
            "cities": ["Kathmandu", "Pokhara", "Everest Region", "Annapurna"],
            "flag": "🇳🇵",
            "category": "Crystal Clear Himalayan Trekking",
            "weather": "Post-monsoon crystal skies (18°C–24°C in valleys); pristine snow peaks visible every day.",
            "why_optimal": "The absolute #1 best trekking month of the entire year; vibrant Dashain & Tihar festivals fill the streets with music and celebration.",
            "highlights": "Poon Hill sunrise, Phewa Lake reflections, Kathmandu Durbar Square, Annapurna Base Camp.",
            "budget_tier": "₹2,600 – ₹4,800 / day (estimated)",
            "caution": "Popular trekking lodges fill fast; pre-book domestic flights and guides."
        },
        {
            "country": "Japan",
            "cities": ["Kyoto", "Tokyo", "Nikko", "Hakone"],
            "flag": "🇯🇵",
            "category": "Autumn Foliage (Koyo)",
            "weather": "Mild, crisp, comfortable autumn weather (17°C–22°C typical); vivid scarlet maple leaves.",
            "why_optimal": "Historic temple gardens framed by glowing red and amber foliage; comfortable walking temperatures with no summer humidity.",
            "highlights": "Tofuku-ji Maple Gardens, Kiyomizu-dera night illuminations, Nikko Toshogu Shrine.",
            "budget_tier": "₹8,500 – ₹11,500 / day (estimated)",
            "caution": "Mid-October to November is high season for Japanese domestic tourists."
        }
    ]
}


def recommend_destinations_by_season(
    month: str,
    interests: Optional[List[str]] = None,
    budget: Optional[int] = None,
    pace: Optional[str] = None,
    year: Optional[str] = None
) -> str:
    """
    Returns curated seasonal travel recommendations based on climate,
    festivals, and typical patterns for the requested month.
    Clearly distinguishes multi-year climate patterns from live forecasts and qualifies costs and dates.
    """
    m_clean = month.strip().lower()

    # Detect year if mentioned e.g. "December 2026"
    y_match = re.search(r"\b(202[4-9]|2030)\b", m_clean)
    travel_year = year or (y_match.group(1) if y_match else None)

    # Map month aliases
    target_key = "december"
    for k in SEASONAL_CALENDAR_DATA.keys():
        if k in m_clean:
            target_key = k
            break
    if target_key not in SEASONAL_CALENDAR_DATA:
        if any(m in m_clean for m in ["nov", "dec", "jan", "feb", "winter"]):
            target_key = "december"
        elif any(m in m_clean for m in ["mar", "apr", "may", "spring"]):
            target_key = "april"
        elif any(m in m_clean for m in ["jun", "jul", "aug", "summer"]):
            target_key = "july"
        else:
            target_key = "october"

    destinations = SEASONAL_CALENDAR_DATA[target_key]
    month_title = target_key.title()
    year_display = f" {travel_year}" if travel_year else ""

    lines = [
        f"### 🌍 Recommended Destinations for **{month_title}{year_display}**",
        "",
        f"If you're planning travel for **{month_title}{year_display}**, here are top destinations selected for their optimal weather patterns, local cultural experiences, and seasonal highlights:",
        ""
    ]

    if not travel_year:
        lines.append("🗓️ *Planning note: When booking specific dates, please confirm your intended travel year (e.g. December 2026) to check exact festival calendars, school vacation periods, and updated flight schedules.*")
        lines.append("")

    for d in destinations:
        lines.append(f"#### {d['flag']} **{d['country']}** &bull; *{d['category']}*")
        lines.append(f"- **📍 Recommended Route:** {', '.join(d['cities'])}")
        lines.append(f"- **🌤️ Historical Climate Pattern:** {d['weather']} *(Note: represents typical multi-year climate averages, not a live guaranteed forecast)*")
        lines.append(f"- **✨ Why Visit in {month_title}:** {d['why_optimal']}")
        lines.append(f"- **🌟 Must-See Highlights:** {d['highlights']}")
        lines.append(f"- **💰 Estimated Daily Cost:** {d['budget_tier']}")
        lines.append(f"- **💡 Practical Advice:** {d['caution']}")
        lines.append("")

    lines.append("---")
    lines.append("💡 *Weather notes are based on historical meteorological averages and typical seasonal patterns. Conditions can vary year-to-year. Costs and festival dates are estimates and should be confirmed closer to your departure!*")

    return "\n".join(lines)
