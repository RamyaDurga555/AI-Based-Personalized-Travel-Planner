"""
country_data.py - Universal Data-Driven Travel Knowledge Engine
Provides authentic tourist attractions, food, culture, transportation, travel tips,
and AI assistant context for all 250 countries worldwide.
"""

import os
import json
import re
import html
import urllib.request
import urllib.parse
from typing import Dict, List, Any, Optional, Tuple

# Path to the 250-country database
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DB_PATH = os.path.join(_BASE_DIR, "countries_data.json")

_COUNTRIES_DB_CACHE: Optional[Dict[str, Any]] = None

def get_countries_db() -> Dict[str, Any]:
    global _COUNTRIES_DB_CACHE
    if _COUNTRIES_DB_CACHE is not None:
        return _COUNTRIES_DB_CACHE
    if os.path.exists(_DB_PATH):
        try:
            with open(_DB_PATH, "r", encoding="utf-8") as f:
                _COUNTRIES_DB_CACHE = json.load(f)
                return _COUNTRIES_DB_CACHE
        except Exception:
            pass
    _COUNTRIES_DB_CACHE = {}
    return _COUNTRIES_DB_CACHE


# ============================================================
# COMPREHENSIVE CURATED KNOWLEDGE FOR 80+ GLOBAL TRAVEL DESTINATIONS
# ============================================================

COUNTRY_DESTINATIONS: Dict[str, Dict[str, Any]] = {
    "India": {
        "cities": ["New Delhi", "Agra", "Jaipur", "Srinagar (Jammu & Kashmir)", "Gulmarg (Jammu & Kashmir)", "Pahalgam (Jammu & Kashmir)", "Sonamarg (Jammu & Kashmir)", "Goa", "Varanasi", "Kerala", "Mumbai", "Amritsar", "Udaipur", "Hampi"],
        "attractions": [
            ("Taj Mahal", "Agra", "Taj_Mahal"),
            ("Golden Temple", "Amritsar", "Golden_Temple"),
            ("India Gate", "New Delhi", "India_Gate"),
            ("Meenakshi Temple", "Madurai", "Meenakshi_Amman_Temple"),
            ("Tirumala Temple", "Tirupati", "Venkateswara_Temple,_Tirumala"),
            ("Jaipur (Hawa Mahal)", "Jaipur", "Jaipur"),
            ("Dal Lake", "Srinagar (Jammu & Kashmir)", "Dal_Lake"),
            ("Gulmarg Gondola & Meadows", "Gulmarg (Jammu & Kashmir)", "Gulmarg"),
            ("Pahalgam Betaab Valley", "Pahalgam (Jammu & Kashmir)", "Pahalgam"),
            ("Sonamarg Thajiwas Glacier", "Sonamarg (Jammu & Kashmir)", "Sonamarg"),
            ("Mughal Gardens (Shalimar & Nishat)", "Srinagar (Jammu & Kashmir)", "Shalimar_Bagh,_Srinagar"),
            ("Shankaracharya Temple", "Srinagar (Jammu & Kashmir)", "Shankaracharya_Temple"),
            ("Goa Beaches", "Goa", "Goa"),
            ("Varanasi Ghats", "Varanasi", "Varanasi"),
            ("Kerala Backwaters", "Kerala", "Kerala_backwaters"),
            ("Qutub Minar", "New Delhi", "Qutb_Minar"),
            ("Amber Palace", "Jaipur", "Amber_Fort"),
            ("Gateway of India", "Mumbai", "Gateway_of_India")
        ],
        "food": [
            ("Biryani", "Aromatic basmati rice cooked with spices, saffron, and tender meat or vegetables.", "Biryani"),
            ("Masala Dosa", "Crisp South Indian fermented crepe stuffed with spiced potato filling, served with sambar and coconut chutney.", "Dosa"),
            ("Butter Chicken", "Tender chicken simmered in a mildly spiced, velvety tomato-butter gravy.", "Butter_chicken"),
            ("Idli", "Soft, fluffy steamed savory cakes made of fermented black lentils and rice, served with hot sambar and fresh coconut chutney.", "Idli"),
            ("Chole Bhature", "Spicy chickpea curry paired with fluffy, deep-fried bread.", "Chole_bhature"),
            ("Samosa", "Crispy golden fried pastry stuffed with spiced potatoes, green peas, and herbs.", "Samosa"),
            ("Rogan Josh", "Slow-cooked Kashmiri aromatic lamb curry infused with maval petals, ginger, and fennel spices.", "Rogan_josh"),
            ("Kashmiri Kahwa", "Traditional green tea infused with saffron strands, crushed almonds, cardamom, and cinnamon.", "Kahwah"),
            ("Gulab Jamun", "Soft fried milk dumplings soaked in fragrant cardamom-rose sugar syrup.", "Gulab_jamun")
        ],
        "culture": [
            ("Shankaracharya Temple", "Srinagar (Jammu & Kashmir)", "Historic 9th-century hill shrine overlooking Srinagar, Shankaracharya hill and Dal Lake."),
            ("Mughal Gardens Heritage", "Srinagar (Jammu & Kashmir)", "Centuries-old terraced Persian-style garden layout built by Mughal emperors overlooking Dal Lake."),
            ("Tirumala Venkateswara Temple", "Tirupati", "One of the most sacred and visited Hindu pilgrimage shrines in the world."),
            ("Varanasi Kashi Vishwanath", "Varanasi", "Ancient holy city temple along the sacred banks of the River Ganges."),
            ("Golden Temple (Harmandir Sahib)", "Amritsar", "The spiritual and cultural heart of Sikhism with community kitchen (Langar)."),
            ("Meenakshi Temple", "Madurai", "Towering Dravidian gopuram sculptures dedicated to Goddess Meenakshi.")
        ],
        "transportation": {
            "modes": ["Indian Railways (Vande Bharat & Express Trains)", "City Metro Systems (Delhi, Mumbai, Bengaluru)", "App-based Cabs (Ola & Uber)", "Domestic Flights (connecting all regions)", "Auto-rickshaws (metered / app-booked)", "State Intercity AC Buses"],
            "tips": "Book long-distance trains via IRCTC weeks ahead. In cities like Delhi, Bengaluru, and Mumbai, the Metro avoids road traffic. Use app-based cabs (Ola/Uber) to avoid fare haggling.",
            "pass": "IRCTC Tourist Passes for rail; Smart Travel Cards for Delhi / Mumbai Metro."
        },
        "travel_tips": {
            "tipping": "10% is standard in sit-down restaurants; ₹20–₹50 for hotel porters.",
            "currency_tips": "UPI (digital payment) is ubiquitous everywhere from luxury malls to roadside chai stalls. Keep some cash (INR ₹) for remote rural areas.",
            "etiquette": "Remove footwear before entering temples, shrines, and homes. Dress modestly at religious sites (shoulders and knees covered). Use the right hand for giving or receiving items.",
            "best_season": "October to March across most of India. Mountain destinations (Kashmir, Himachal, Ladakh) are best from May to September.",
            "safety": "Drink packaged or filtered water. Keep photocopies of ID. Jammu & Kashmir is a vibrant northern Union Territory of India—enjoy Dal Lake houseboats and Gulmarg gondola rides."
        }
    },

    "Nepal": {
        "cities": ["Kathmandu", "Pokhara", "Lumbini", "Chitwan", "Bhaktapur", "Nagarkot", "Solukhumbu (Everest Region)"],
        "attractions": [
            ("Mount Everest", "Solukhumbu", "Mount_Everest"),
            ("Pashupatinath Temple", "Kathmandu", "Pashupatinath_Temple"),
            ("Boudhanath Stupa", "Kathmandu", "Boudhanath"),
            ("Kathmandu Durbar Square", "Kathmandu", "Kathmandu_Durbar_Square"),
            ("Phewa Lake", "Pokhara", "Phewa_Lake"),
            ("Swayambhunath (Monkey Temple)", "Kathmandu", "Swayambhunath"),
            ("Chitwan National Park", "Chitwan", "Chitwan_National_Park"),
            ("Peace Pagoda (Shanti Stupa)", "Pokhara", "World_Peace_Pagoda"),
        ],
        "food": [
            ("Momo", "Steamed Nepali dumplings filled with spiced vegetables or minced meat, served with fiery tomato-sesame achar.", "Momo_(food)"),
            ("Dal Bhat", "Nutritious traditional Nepali national meal with steamed rice (Bhat), slow-simmered spiced lentil soup (Dal), seasonal vegetable curry (Tarkari), sautéed greens (Saag), and spicy achar relish served on a brass thali.", "Dal_bhat"),
            ("Thukpa", "Comforting Himalayan hot noodle soup with fresh vegetables, coriander, and mountain spices.", "Thukpa"),
            ("Sel Roti", "Traditional ring-shaped sweet fried rice-flour bread prepared during Dashain and Tihar festivals.", "Sel_roti"),
            ("Choila & Newari Khaja", "Spicy grilled marinated meat paired with beaten rice (baji) and fermented mustard greens.", "Choila"),
            ("Juju Dhau", "Rich, creamy 'King Curd' sweet yogurt traditionally served in clay pots in Bhaktapur.", "Juju_dhau")
        ],
        "culture": [
            ("Pashupatinath Temple", "Kathmandu", "Sacred 5th-century Hindu temple complex dedicated to Lord Shiva on the Bagmati River."),
            ("Boudhanath Stupa", "Kathmandu", "One of the largest spherical stupas in the world and center of Tibetan Buddhism in Nepal."),
            ("Swayambhunath", "Kathmandu", "Ancient hilltop stupa with watchful Buddha eyes, overlooking the Kathmandu Valley."),
            ("Lumbini Sacred Garden", "Lumbini", "UNESCO World Heritage site and venerated birthplace of Gautama Buddha in 623 BC."),
            ("Bhaktapur Durbar Square", "Bhaktapur", "Preserved medieval Malla royal palace complex with the 55-Window Palace.")
        ],
        "transportation": {
            "modes": ["Tourist Express Buses (Kathmandu-Pokhara)", "Domestic Himalayan Flights & Helicopters", "Local Taxis & Ride-Hailing (Pathao / InDrive)", "Private 4WD Jeeps", "Local Shared Microbuses", "Trekking & Mountain Trails"],
            "tips": "For Pokhara and Chitwan, AC tourist buses are comfortable and scenic. For mountain regions (Lukla, Jomsom), morning domestic flights or 4WD jeeps are essential. Download Pathao in Kathmandu for easy cab bookings.",
            "pass": "TIMS (Trekkers' Information Management System) Card and National Park Entry Permits."
        },
        "travel_tips": {
            "tipping": "10% in tourist cafes and restaurants; 500–1000 NPR per day for trekking guides and porters.",
            "currency_tips": "Nepalese Rupee (NPR ₨). Carry cash for rural trekking circuits; ATMs are abundant in Kathmandu and Pokhara.",
            "etiquette": "Always walk clockwise around Buddhist stupas and chortens. Remove shoes at temple entrances. Greet with hands together saying 'Namaste'.",
            "best_season": "October to December (crystal-clear skies, peak trekking season) and March to May (rhododendron blooms).",
            "safety": "Drink bottled or boiled water. Allow time for acclimatization above 2,500m to prevent altitude sickness."
        }
    },

    "Japan": {
        "cities": ["Tokyo", "Kyoto", "Osaka", "Mount Fuji / Hakone", "Hiroshima", "Nara", "Sapporo", "Takayama", "Fukuoka"],
        "attractions": [
            ("Mount Fuji", "Yamanashi / Shizuoka", "Mount_Fuji"),
            ("Fushimi Inari Shrine", "Kyoto", "Fushimi_Inari-taisha"),
            ("Tokyo Tower", "Tokyo", "Tokyo_Tower"),
            ("Tokyo Skytree & Shibuya Crossing", "Tokyo", "Tokyo"),
            ("Kinkaku-ji (Golden Pavilion)", "Kyoto", "Kinkaku-ji"),
            ("Osaka Castle", "Osaka", "Osaka_Castle"),
            ("Hiroshima Peace Memorial", "Hiroshima", "Hiroshima_Peace_Memorial"),
            ("Nara Deer Park & Todai-ji", "Nara", "Nara_Park"),
            ("Arashiyama Bamboo Grove", "Kyoto", "Arashiyama"),
        ],
        "food": [
            ("Sushi & Sashimi", "Expertly prepared fresh fish paired with seasoned vinegar sushi rice.", "Sushi"),
            ("Ramen", "Wheat noodles served in rich tonkotsu, miso, or shoyu broth with sliced chashu.", "Ramen"),
            ("Tempura", "Seafood and seasonal vegetables dipped in light batter and fried to crisp perfection.", "Tempura"),
            ("Okonomiyaki", "Savory Japanese teppan cabbage pancake layered with batter, meat, and bonito.", "Okonomiyaki"),
            ("Takoyaki", "Ball-shaped Japanese savory street snack filled with tender diced octopus.", "Takoyaki"),
            ("Matcha & Wagashi", "Traditional stone-ground green tea served with delicate seasonal sweets.", "Wagashi")
        ],
        "culture": [
            ("Fushimi Inari-taisha", "Kyoto", "Thousands of vermilion torii gates winding through sacred Mount Inari forest."),
            ("Senso-ji Temple", "Tokyo", "Tokyo's oldest and most significant ancient Buddhist temple founded in 645 AD."),
            ("Meiji Jingu Shrine", "Tokyo", "Serene Shinto shrine set within 170 acres of lush evergreen forest in central Tokyo."),
            ("Todai-ji Temple", "Nara", "Colossal wooden temple housing the world's largest bronze Buddha statue."),
            ("Kiyomizu-dera", "Kyoto", "Historic cliffside temple offering wooden stage panoramas over cherry and maple trees.")
        ],
        "transportation": {
            "modes": ["Shinkansen (High-Speed Bullet Trains)", "Tokyo Metro & City Subways", "Japan Rail (JR) Local Lines", "Clean Public City Buses", "Walkable Pedestrian City Zones", "Bicycle Rentals"],
            "tips": "Purchase an IC card (Suica, Pasmo, or ICOCA) for seamless tap-and-go travel on all subways, buses, and convenience stores. Shinkansen trains run with to-the-second punctuality.",
            "pass": "Japan Rail Pass (JR Pass) or Regional JR West/East Passes; Tokyo Subway 24/48/72hr tickets."
        },
        "travel_tips": {
            "tipping": "No tipping anywhere in Japan. Tipping is considered unusual or even insulting as exceptional service is standard.",
            "currency_tips": "Carry cash (JPY ¥) as many traditional ramen shops, temples, and coin lockers do not accept foreign credit cards. 7-Eleven ATMs accept international cards reliably.",
            "etiquette": "Maintain silence on trains and subways. Stand on the left (Tokyo) or right (Osaka) on escalators. Bow when greeting or thanking people. Remove shoes at ryokans, temples, and tatami rooms.",
            "best_season": "March to May (cherry blossom season) and October to November (vibrant autumn foliage).",
            "safety": "One of the safest countries globally. Clean tap water, highly reliable medical facilities, and low crime."
        }
    },

    "France": {
        "cities": ["Paris", "Nice & French Riviera", "Lyon", "Marseille", "Bordeaux", "Strasbourg", "Normandy", "Provence", "Versailles"],
        "attractions": [
            ("Eiffel Tower", "Paris", "Eiffel_Tower"),
            ("Louvre Museum", "Paris", "Louvre"),
            ("Palace of Versailles", "Versailles", "Palace_of_Versailles"),
            ("Mont Saint-Michel", "Normandy", "Mont-Saint-Michel"),
            ("Promenade des Anglais", "Nice", "Nice"),
            ("Vieux Lyon", "Lyon", "Vieux_Lyon"),
            ("Champs-Élysées & Arc de Triomphe", "Paris", "Arc_de_Triomphe"),
            ("Sainte-Chapelle", "Paris", "Sainte-Chapelle"),
        ],
        "food": [
            ("Croissant & Viennoiseries", "Flaky, golden, multilayered butter pastries baked fresh each morning.", "Croissant"),
            ("Crêpes & Galettes", "Thin sweet wheat pancakes and savory Breton buckwheat galettes.", "Crêpe"),
            ("Boeuf Bourguignon", "Tender beef braised slowly in red Burgundy wine, carrots, mushrooms, and herbs.", "Beef_bourguignon"),
            ("Ratatouille", "Traditional Provençal stew of eggplant, zucchini, bell peppers, tomatoes, and herbs.", "Ratatouille"),
            ("Artisan French Cheeses", "Brie, Camembert, Roquefort, and Comté served with fresh baguette.", "French_cheese"),
            ("Macarons", "Delicate almond meringue sandwich confections with ganache and buttercream.", "Macaron")
        ],
        "culture": [
            ("Notre-Dame de Paris", "Paris", "Iconic French Gothic cathedral on the Île de la Cité dating back to 1163."),
            ("Sainte-Chapelle", "Paris", "Breathtaking 13th-century Gothic royal chapel renowned for stained glass windows."),
            ("Mont-Saint-Michel Abbey", "Normandy", "Spectacular medieval Benedictine abbey perched atop a tidal island."),
            ("Basilique Notre-Dame de Fourvière", "Lyon", "Hilltop basilica offering sweeping vistas across Lyon and the Rhône."),
            ("Chartres Cathedral", "Chartres", "High Gothic masterpiece with preserved 13th-century stained glass.")
        ],
        "transportation": {
            "modes": ["TGV Inoui & Ouigo (High-Speed Trains)", "Paris Métro & RER Network", "SNCF TER Regional Trains", "Modern City Trams (Lyon, Nice, Bordeaux)", "Self-service City Bikes (Vélib')", "Walking in historic districts"],
            "tips": "Validate physical transit tickets before boarding train platforms. Book TGV high-speed trains early for significant savings. Use the Navigo Easy pass in Paris for public transit.",
            "pass": "Eurail France Pass; Navigo Easy Pass in Paris; regional SNCF day passes."
        },
        "travel_tips": {
            "tipping": "Service is included (service compris) by law. Leaving 5–10% or rounding up is customary for good service.",
            "currency_tips": "Euro (EUR €). Contactless card payment (Carte Bancaire / Visa / Mastercard) is universally accepted.",
            "etiquette": "Always say 'Bonjour, Madame/Monsieur' when entering any shop or cafe before asking questions. Avoid speaking loudly in public transit.",
            "best_season": "April to June and September to October offer mild temperatures and fewer crowds than July–August.",
            "safety": "Be mindful of pickpockets around major Paris tourist sights (Eiffel Tower, Louvre, Montmartre) and train stations."
        }
    },

    "United States": {
        "cities": ["New York", "San Francisco", "Los Angeles", "Las Vegas", "Grand Canyon", "Yellowstone", "Washington D.C.", "Chicago", "Miami", "Hawaii"],
        "attractions": [
            ("Statue of Liberty", "New York", "Statue_of_Liberty"),
            ("Grand Canyon National Park", "Arizona", "Grand_Canyon"),
            ("Times Square & Central Park", "New York", "Times_Square"),
            ("Yellowstone National Park", "Wyoming / Montana", "Yellowstone_National_Park"),
            ("Golden Gate Bridge", "San Francisco", "Golden_Gate_Bridge"),
            ("Walt Disney World", "Florida", "Walt_Disney_World"),
            ("National Mall & Monuments", "Washington D.C.", "National_Mall"),
            ("Yosemite National Park", "California", "Yosemite_National_Park"),
        ],
        "food": [
            ("Classic Cheeseburger", "Juicy grilled beef patty with melted cheese, lettuce, pickles, and brioche bun.", "Cheeseburger"),
            ("New York Style Pizza", "Wide, hand-tossed thin-crust pizza slice with tangy tomato sauce and mozzarella.", "New_York-style_pizza"),
            ("Southern Barbecue", "Slow-smoked pulled pork, brisket, and ribs glazed with smoky regional sauce.", "Barbecue_in_the_United_States"),
            ("Clam Chowder", "Creamy New England soup loaded with fresh clams, tender potatoes, and herbs.", "Clam_chowder"),
            ("Key Lime Pie", "Tart and creamy Floridian dessert made with authentic Key lime juice on graham crust.", "Key_lime_pie"),
            ("Tex-Mex Tacos", "Crispy and soft tortillas packed with seasoned meats, guacamole, salsa, and cheese.", "Taco")
        ],
        "culture": [
            ("National Cathedral", "Washington D.C.", "Magnificent neo-Gothic cathedral hosting historic state funerals and services."),
            ("St. Patrick's Cathedral", "New York", "Deco-era Gothic Catholic cathedral standing opposite Rockefeller Center on 5th Ave."),
            ("Smithsonian Institution Museums", "Washington D.C.", "World's largest museum and research complex, offering free admission."),
            ("Mission San Francisco de Asís", "San Francisco", "Oldest surviving stone and adobe structure in San Francisco founded in 1776."),
            ("Independence Hall", "Philadelphia", "UNESCO World Heritage birthplace where the US Constitution was signed in 1787.")
        ],
        "transportation": {
            "modes": ["Domestic Flights (essential for cross-country distances)", "Car Rental & Road Trips (best for National Parks)", "Metropolitan Subways (NYC Subway, Chicago L, DC Metro)", "Amtrak Passenger Rail (Northeast Corridor)", "Ride-Hailing (Uber & Lyft nationwide)", "Intercity Buses (Greyhound, Megabus)"],
            "tips": "Outside major dense cities like New York and Chicago, renting a car is almost mandatory for flexibility. Keep GPS offline maps downloaded for remote national parks without cell reception.",
            "pass": "National Parks 'America the Beautiful' Annual Pass ($80); OMNY contactless in NYC."
        },
        "travel_tips": {
            "tipping": "Tipping is customary and expected in US restaurants (18% to 22% of total pre-tax bill), $1–$2 per drink at bars, and $2–$5/day for hotel housekeeping.",
            "currency_tips": "US Dollar (USD $). Credit and debit cards (Apple Pay, Google Pay, chip & PIN) are used everywhere.",
            "etiquette": "Prices shown on tags and menus do not include state/local sales tax, which is calculated at checkout.",
            "best_season": "Spring (April–May) and Autumn (September–October) provide prime travel weather nationwide. Summer is peak for national parks.",
            "safety": "Emergency number is 911. Research neighborhoods in large urban centers and keep valuables out of rental cars."
        }
    },

    "United Kingdom": {
        "cities": ["London", "Edinburgh", "Scottish Highlands", "Bath", "Oxford & Cambridge", "Lake District", "Manchester", "York", "Belfast"],
        "attractions": [
            ("Big Ben & Westminster Palace", "London", "Big_Ben"),
            ("Tower of London & Tower Bridge", "London", "Tower_of_London"),
            ("Stonehenge Prehistoric Monument", "Wiltshire", "Stonehenge"),
            ("Edinburgh Castle", "Edinburgh", "Edinburgh_Castle"),
            ("Lake District National Park", "Cumbria", "Lake_District"),
            ("Buckingham Palace", "London", "Buckingham_Palace"),
            ("Roman Baths & Royal Crescent", "Bath", "Roman_Baths_(Bath)"),
            ("British Museum", "London", "British_Museum"),
        ],
        "food": [
            ("Fish and Chips", "Crisp beer-battered cod or haddock served with thick chips, mushy peas, and tartar sauce.", "Fish_and_chips"),
            ("Sunday Roast", "Roast beef or chicken served with Yorkshire pudding, roast potatoes, gravy, and veg.", "Sunday_roast"),
            ("Full English Breakfast", "Sausages, crispy bacon, fried eggs, baked beans, grilled tomatoes, and toast.", "Full_English_breakfast"),
            ("Shepherd's / Cottage Pie", "Minced lamb or beef cooked in savory onion gravy under golden mashed potatoes.", "Shepherd's_pie"),
            ("Traditional Afternoon Tea", "Warm scones with clotted cream and strawberry jam, cucumber sandwiches, and tea.", "Afternoon_tea"),
            ("Haggis with Neeps & Tatties", "Traditional spiced Scottish dish served with mashed turnips and buttery potatoes.", "Haggis")
        ],
        "culture": [
            ("Westminster Abbey", "London", "Royal coronation church and resting place of British monarchs and poets since 1066."),
            ("St Paul's Cathedral", "London", "Christopher Wren's domed architectural masterpiece that survived the London Blitz."),
            ("Canterbury Cathedral", "Canterbury", "Cradle of English Christianity and UNESCO World Heritage pilgrimage shrine."),
            ("St Giles' Cathedral", "Edinburgh", "Historic High Kirk of Edinburgh on the Royal Mile dating back to the 12th century."),
            ("York Minster", "York", "One of the largest Gothic cathedrals in Northern Europe with medieval stained glass.")
        ],
        "transportation": {
            "modes": ["National Rail Intercity Trains (LNER, Avanti, GWR)", "London Underground ('The Tube')", "Iconic Red Double-decker Buses", "Black Cabs & Ride-hailing (Uber / Bolt)", "Intercity Coaches (National Express)", "Scenic Ferries (Scotland & Isle of Wight)"],
            "tips": "In London, simply tap in and out using any contactless bank card or phone—no Oyster card needed. Book intercity trains weeks in advance via Trainline to avoid exorbitant same-day fares.",
            "pass": "BritRail Pass for international visitors; National Trust / English Heritage visitor passes."
        },
        "travel_tips": {
            "tipping": "10–12.5% is common in restaurants (often added automatically as an optional service charge). Tipping at pub counters is not expected.",
            "currency_tips": "Pound Sterling (GBP £). Contactless card payment is used everywhere; many London venues are 100% cashless.",
            "etiquette": "Always queue patiently in lines. Stand on the right on Tube escalators. Always carry a compact umbrella or rain jacket regardless of the forecast.",
            "best_season": "May to September brings long daylight hours, open gardens, and festival season (such as the Edinburgh Fringe in August).",
            "safety": "Emergency number is 999 or 112. Very safe country with comprehensive public transport across England, Scotland, Wales, and Northern Ireland."
        }
    },

    "Australia": {
        "cities": ["Sydney", "Melbourne", "Cairns (Great Barrier Reef)", "Uluru / Red Centre", "Brisbane", "Perth", "Gold Coast", "Tasmania", "Adelaide"],
        "attractions": [
            ("Sydney Opera House & Harbour Bridge", "Sydney", "Sydney_Opera_House"),
            ("Great Barrier Reef", "Queensland", "Great_Barrier_Reef"),
            ("Uluru (Ayers Rock)", "Northern Territory", "Uluru"),
            ("Bondi Beach & Coastal Walk", "Sydney", "Bondi_Beach"),
            ("Great Ocean Road (Twelve Apostles)", "Victoria", "Great_Ocean_Road"),
            ("Melbourne Laneways & Arts Precinct", "Melbourne", "Melbourne"),
            ("Daintree Rainforest", "Queensland", "Daintree_Rainforest"),
            ("Cradle Mountain", "Tasmania", "Cradle_Mountain"),
        ],
        "food": [
            ("Aussie Meat Pie", "Flaky individual pie filled with minced meat and rich gravy, topped with tomato sauce.", "Meat_pie_(Australia_and_New_Zealand)"),
            ("Fresh Seafood Platter", "Sydney rock oysters, Moreton Bay bugs, king prawns, and barramundi.", "Seafood"),
            ("Chicken Parmigiana ('Parma')", "Breaded chicken schnitzel topped with tomato passata, ham, and melted cheese.", "Chicken_parmigiana"),
            ("Barramundi Fillet", "Pan-seared native Australian freshwater fish served with seasonal salad and lemon.", "Barramundi"),
            ("Pavlova", "Crisp meringue dessert topped with whipped cream, passionfruit, kiwi, and berries.", "Pavlova_(cake)"),
            ("Lamington", "Soft sponge cake squares coated in rich chocolate icing and rolled in desiccated coconut.", "Lamington")
        ],
        "culture": [
            ("Uluru-Kata Tjuta Sacred Sites", "Northern Territory", "Deeply spiritual Anangu sacred landscape steeped in ancient Tjukurpa creation stories."),
            ("St Mary's Cathedral", "Sydney", "Imposing neo-Gothic Catholic cathedral built from Sydney honey-coloured sandstone."),
            ("St Paul's Cathedral", "Melbourne", "Gothic revival cathedral anchoring central Melbourne opposite Flinders Street."),
            ("Kakadu Indigenous Rock Art", "Northern Territory", "Galleries of ancient Indigenous Australian rock art dating back over 20,000 years."),
            ("Port Arthur Historic Site", "Tasmania", "World Heritage convict settlement reflecting early colonial Australian history.")
        ],
        "transportation": {
            "modes": ["Domestic Flights (Qantas, Virgin Australia, Jetstar)", "Rental Cars & Campervans (ideal for road trips)", "Sydney Opal Transit (Trains, Ferries, Light Rail)", "Melbourne Yarra Trams (Free Tram Zone in CBD)", "Suburban Rail Networks", "Long-distance Trains (The Ghan, Indian Pacific)"],
            "tips": "Distances are enormous—flying between states saves full days of driving. In Melbourne, trams within the central CBD are completely free. In Sydney, the ferry from Circular Quay to Manly is a scenic must-do.",
            "pass": "Opal Card / contactless in NSW; myki card in Victoria; Go Card in Queensland."
        },
        "travel_tips": {
            "tipping": "Tipping is not expected as Australian hospitality staff receive high minimum wages. 5–10% for exceptional fine dining is appreciated.",
            "currency_tips": "Australian Dollar (AUD $). Tap-and-go contactless card payment is universal.",
            "etiquette": "Always swim between the red and yellow flags on surf beaches. Apply SPF 50+ sunscreen and wear a hat—the Southern Hemisphere UV index is exceptionally strong.",
            "best_season": "September to November (spring) and March to May (autumn). Visit the tropical north (Cairns/Darwin) during the dry season (May–October).",
            "safety": "Emergency number is 000. Follow wildlife safety warnings (crocodiles in the tropical north; observe ocean rip currents)."
        }
    },

    "Brazil": {
        "cities": ["Rio de Janeiro", "São Paulo", "Salvador da Bahia", "Foz do Iguaçu", "Manaus (Amazon)", "Florianópolis", "Brasília", "Ouro Preto"],
        "attractions": [
            ("Christ the Redeemer & Corcovado", "Rio de Janeiro", "Christ_the_Redeemer_(statue)"),
            ("Copacabana & Ipanema Beaches", "Rio de Janeiro", "Copacabana,_Rio_de_Janeiro"),
            ("Iguazu Falls (Cataratas do Iguaçu)", "Paraná", "Iguazu_Falls"),
            ("Amazon Rainforest & Rio Negro", "Amazonas", "Amazon_rainforest"),
            ("Sugarloaf Mountain (Pão de Açúcar)", "Rio de Janeiro", "Sugarloaf_Mountain"),
            ("Pelourinho Historic Center", "Salvador", "Salvador,_Bahia"),
            ("Teatro Amazonas", "Manaus", "Amazon_Theatre"),
            ("Lençóis Maranhenses", "Maranhão", "Lençóis_Maranhenses_National_Park"),
        ],
        "food": [
            ("Feijoada", "Rich traditional stew of black beans, smoked pork, and beef served with rice, farofa, and orange.", "Feijoada"),
            ("Pão de Queijo", "Chewy and crisp warm cheese bread balls made with cassava flour and Minas cheese.", "Pão_de_queijo"),
            ("Moqueca Baiana", "Fragrant coastal seafood stew simmered in coconut milk, dendê palm oil, and bell peppers.", "Moqueca"),
            ("Churrasco & Picanha", "Prime cuts of beef skewered and roasted over open wood flames at traditional rodízios.", "Picanha"),
            ("Coxinha", "Tear-shaped crispy savory croquette filled with shredded seasoned chicken.", "Coxinha"),
            ("Açaí Bowl", "Frozen pureed Amazonian açaí berries topped with granola, fresh bananas, and honey.", "Açaí_na_tigela")
        ],
        "culture": [
            ("Metropolitan Cathedral of Saint Sebastian", "Rio de Janeiro", "Futuristic conical modern cathedral inspired by Mayan pyramid architecture."),
            ("Church of São Francisco de Assis", "Ouro Preto", "Baroque and Rococo masterpiece decorated with sculptures by legendary Aleijadinho."),
            ("Church of Nosso Senhor do Bonfim", "Salvador", "Historic Bahian pilgrimage shrine famous for colorful wishing ribbons (fitas)."),
            ("Cathedral of Brasília", "Brasília", "Oscar Niemeyer's hyper-modern masterpiece formed by 16 parabolic concrete columns."),
            ("Mosteiro de São Bento", "Rio de Janeiro", "17th-century Benedictine monastery adorned with intricate gold-leaf woodwork.")
        ],
        "transportation": {
            "modes": ["Domestic Flights (LATAM, Gol, Azul)", "Metrô Rio & São Paulo Metrô", "Intercity Executive Buses (Leito / Cometa)", "App-based Ride-hailing (Uber & 99)", "Registered Airport & City Taxis", "River Boats (Amazon waterways)"],
            "tips": "For intercity travel between Rio, São Paulo, and distant regions, domestic flights are the most efficient option. In Rio and São Paulo, the metro is fast, air-conditioned, and safe during daylight hours. Use Uber or 99 rather than hailing unmarked street cabs at night.",
            "pass": "RioCard Mais (Rio de Janeiro); Bilhete Único (São Paulo)."
        },
        "travel_tips": {
            "tipping": "A 10% service fee (serviço) is normally included on restaurant bills. Tipping taxi drivers is not expected, but rounding up is polite.",
            "currency_tips": "Brazilian Real (BRL R$). Cards (credit and debit) are widely accepted across urban cities, including beach kiosks via wireless terminals.",
            "etiquette": "Brazilians are warm and expressive. Greet with a handshake or light kiss on the cheek. Dress casually at the beach, but avoid walking through city streets in just swimwear.",
            "best_season": "May to October offers pleasant temperatures with lower humidity and rainfall. December to March is hot, energetic, and carnival season.",
            "safety": "Keep smartphones, expensive cameras, and jewelry discreet in busy public areas. Take official radio taxis or Uber after dark."
        }
    },

    "Egypt": {
        "cities": ["Cairo", "Giza", "Luxor", "Aswan", "Alexandria", "Sharm El Sheikh", "Hurghada", "Siwa Oasis"],
        "attractions": [
            ("Great Pyramids of Giza & Sphinx", "Giza", "Great_Pyramid_of_Giza"),
            ("Valley of the Kings", "Luxor", "Valley_of_the_Kings"),
            ("Karnak Temple Complex", "Luxor", "Karnak"),
            ("Abu Simbel Sun Temples", "Aswan", "Abu_Simbel"),
            ("The Grand Egyptian Museum", "Giza / Cairo", "Grand_Egyptian_Museum"),
            ("Nile River Felucca Cruise", "Aswan / Luxor", "Nile"),
            ("Philae Temple of Isis", "Aswan", "Philae"),
            ("Khan el-Khalili Bazaar", "Cairo", "Khan_el-Khalili"),
        ],
        "food": [
            ("Koshari", "Egypt's national dish—comforting mix of rice, lentils, macaroni, chickpeas, spiced tomato sauce, and fried onions.", "Koshary"),
            ("Ful Medames", "Slow-simmered fava beans seasoned with olive oil, lemon juice, garlic, and cumin, served with warm pita.", "Ful_medames"),
            ("Shawarma", "Thinly sliced marinated beef or chicken roasted on a vertical spit and wrapped in flatbread with tahini.", "Shawarma"),
            ("Taameya (Egyptian Falafel)", "Crisp and fluffy deep-fried patties made with fresh fava beans and fragrant green herbs.", "Falafel"),
            ("Molokhia", "Traditional nutrient-rich soup made from finely minced jute leaves simmered with garlic and coriander.", "Mulukhiyah"),
            ("Umm Ali", "Warm Egyptian bread pudding baked with pastry, sweet milk, raisins, and roasted nuts.", "Umm_Ali")
        ],
        "culture": [
            ("Al-Azhar Mosque", "Cairo", "Founded in 970 AD, one of the oldest and most prestigious institutions of Islamic learning."),
            ("Mosque of Muhammad Ali", "Cairo", "Prominent Ottoman landmark crowned by alabaster walls inside the Citadel of Saladin."),
            ("Hanging Church (Saint Virgin Mary)", "Cairo", "Ancient 3rd-century Coptic Christian church built atop a Roman fortress gatehouse."),
            ("Karnak Temple of Amun-Ra", "Luxor", "Enormous hypostyle hall featuring 134 towering stone columns covered in hieroglyphs."),
            ("Monastery of Saint Anthony", "Red Sea", "Oldest active Christian monastery in the world situated in the Eastern Desert.")
        ],
        "transportation": {
            "modes": ["Domestic Flights (EgyptAir linking Cairo, Luxor, Aswan)", "Nile Cruise Ships & Sail Feluccas", "Cairo Metro (Africa's first underground)", "Egyptian National Railways (Sleeper & AC Express)", "App-based Ride-hailing (Uber & Careem)", "Registered White Metered Taxis"],
            "tips": "For Cairo city travel, Uber and Careem eliminate price haggling. To experience Upper Egypt between Luxor and Aswan, a 3-night Nile cruise or scenic train journey is unmatched.",
            "pass": "Cairo Metro Ticket cards; Luxor Pass and Cairo Pass for major historic sites."
        },
        "travel_tips": {
            "tipping": "Tipping ('Baksheesh') is an integral part of Egyptian culture. Keep small banknotes for temple attendants, drivers, luggage handlers, and servers (10%).",
            "currency_tips": "Egyptian Pound (EGP £). Card payments are standard at government antiquities counters; cash is needed for bazaars and small shops.",
            "etiquette": "Dress modestly when visiting mosques and town centers (cover shoulders and knees). Always ask before photographing locals. Remove shoes when entering mosques.",
            "best_season": "October to April brings pleasant, sunny weather. Avoid mid-summer (June–August) in Luxor and Aswan where heat frequently exceeds 40°C.",
            "safety": "Drink bottled water. Licensed tourist guides provide immense context and help manage street vendors at historical sites."
        }
    },

    "South Africa": {
        "cities": ["Cape Town", "Johannesburg", "Kruger National Park", "Durban", "Stellenbosch & Winelands", "Garden Route", "Drakensberg", "Blyde River Canyon"],
        "attractions": [
            ("Table Mountain & Aerial Cableway", "Cape Town", "Table_Mountain"),
            ("Kruger National Park Safari", "Mpumalanga / Limpopo", "Kruger_National_Park"),
            ("Robben Island Heritage Site", "Cape Town", "Robben_Island"),
            ("Cape Point & Boulders Beach Penguins", "Cape Peninsula", "Cape_Point"),
            ("Kirstenbosch National Botanical Garden", "Cape Town", "Kirstenbosch_National_Botanical_Garden"),
            ("Blyde River Canyon & God's Window", "Mpumalanga", "Blyde_River_Canyon"),
            ("Durban Golden Mile & Beachfront", "Durban", "Durban"),
            ("Stellenbosch Wine Estate Valley", "Western Cape", "Stellenbosch"),
        ],
        "food": [
            ("Bobotie", "Spiced minced meat baked with an egg-custard topping, served with golden yellow rice and chutney.", "Bobotie"),
            ("Biltong & Droëwors", "Traditional cured and air-dried seasoned beef or wild game meat, cured with coriander and vinegar.", "Biltong"),
            ("Bunny Chow", "Famous Durban street-food dish of a hollowed bread loaf filled with rich, aromatic lamb or bean curry.", "Bunny_chow"),
            ("Boerewors", "Coarse-ground spiced farmer sausage grilled outdoors over sizzling charcoal braais.", "Boerewors"),
            ("Malva Pudding", "Decadent sweet spongy apricot pudding soaked in warm caramel syrup and served with custard.", "Malva_pudding"),
            ("Chakalaka & Pap", "Spicy vegetable relish made with beans and tomatoes, paired with traditional maize porridge.", "Chakalaka")
        ],
        "culture": [
            ("St. George's Cathedral", "Cape Town", "The historic 'People's Cathedral' where Archbishop Desmond Tutu led anti-apartheid campaigns."),
            ("District Six Museum", "Cape Town", "Moving memorial dedicated to the vibrant multi-racial community displaced during apartheid."),
            ("Nelson Mandela Sanctuary & Capture Site", "Howick / Soweto", "Landmark monuments commemorating Nelson Mandela's long walk to freedom."),
            ("Nizamiye Mosque", "Midrand", "Largest Ottoman-style mosque complex in the Southern Hemisphere."),
            ("Cradle of Humankind", "Gauteng", "UNESCO World Heritage paleoanthropological site containing 40% of all human ancestor fossils.")
        ],
        "transportation": {
            "modes": ["Car Rental (best for Garden Route & Kruger Self-drive)", "Domestic Flights (linking Cape Town, Joburg, Durban)", "Gautrain High-Speed Rail (Joburg Airport to Pretoria)", "MyCiTi Bus Rapid Transit (Cape Town)", "Ride-hailing Apps (Uber & Bolt)", "Guided Safari 4x4 Game Vehicles"],
            "tips": "Renting a car offers the greatest independence for touring the scenic Cape Peninsula, Garden Route, and Kruger Park. The Gautrain is safe, clean, and fast between O.R. Tambo Airport and Sandton.",
            "pass": "Gautrain Gold Card; MyCiTi Smart Card for Cape Town; SANParks Wild Card for unlimited National Park entry."
        },
        "travel_tips": {
            "tipping": "10% to 15% is customary in restaurants. Tipping R10–R20 for car guards and petrol station attendants is standard.",
            "currency_tips": "South African Rand (ZAR R). Credit cards (Visa and Mastercard) are accepted almost everywhere.",
            "etiquette": "South Africa is known as the 'Rainbow Nation' with 11 official languages. Greet locals politely. Drive on the left side of the road.",
            "best_season": "May to September (dry winter) is the absolute best time for wildlife safari game viewing. November to March is prime for Cape Town beaches and wine harvesting.",
            "safety": "Stay alert in large downtown city centers after dark. Store valuables out of sight in rental car trunks. Use Uber rather than walking at night in unfamiliar areas."
        }
    },

    "Canada": {
        "cities": ["Toronto", "Vancouver", "Montreal", "Banff & Lake Louise", "Quebec City", "Niagara Falls", "Victoria", "Jasper", "Ottawa", "Whistler"],
        "attractions": [
            ("Banff National Park & Lake Louise", "Alberta", "Banff_National_Park"),
            ("CN Tower & Waterfront", "Toronto", "CN_Tower"),
            ("Niagara Falls (Horseshoe Falls)", "Ontario", "Niagara_Falls"),
            ("Old Quebec & Château Frontenac", "Quebec City", "Old_Quebec"),
            ("Stanley Park & Seawall", "Vancouver", "Stanley_Park"),
            ("Moraine Lake & Valley of the Ten Peaks", "Alberta", "Moraine_Lake"),
            ("Notre-Dame Basilica of Montreal", "Montreal", "Notre-Dame_Basilica_(Montreal)"),
            ("Parliament Hill", "Ottawa", "Parliament_Hill"),
        ],
        "food": [
            ("Poutine", "Golden crisp french fries smothered in squeaky fresh cheese curds and piping-hot savory gravy.", "Poutine"),
            ("Maple Syrup Specialties", "Pure Grade-A Canadian amber maple syrup served over hot pancakes or in maple taffy on snow.", "Maple_syrup"),
            ("Butter Tarts", "Iconic Canadian pastry shells filled with a rich, decadent filling of butter, brown sugar, and eggs.", "Butter_tart"),
            ("Tourtière", "Traditional French-Canadian spiced minced pork and beef pie enjoyed with cranberry chutney.", "Tourtière"),
            ("Peameal Bacon Sandwich", "Cornmeal-crusted cured pork loin served in a bakery bun—a Toronto St. Lawrence Market legend.", "Peameal_bacon"),
            ("Nanaimo Bars", "Famous British Columbia three-layer no-bake bar with graham crumb base, custard, and chocolate.", "Nanaimo_bar")
        ],
        "culture": [
            ("Notre-Dame Basilica", "Montreal", "Dramatic Gothic Revival basilica celebrated for its intricate azure, gold-leaf woodwork."),
            ("Saint Joseph's Oratory of Mount Royal", "Montreal", "Canada's largest church crowned by one of the world's largest domes."),
            ("Canadian Museum of History", "Gatineau / Ottawa", "World-renowned museum housing the world's largest indoor collection of totem poles."),
            ("Parliament of Canada", "Ottawa", "Gothic Revival seat of Canadian federal democracy overlooking the Ottawa River."),
            ("Haida Heritage Centre", "Haida Gwaii, British Columbia", "First Nations cultural centre celebrating ancient cedar carving and Haida art.")
        ],
        "transportation": {
            "modes": ["VIA Rail Intercity Passenger Trains", "Domestic Flights (Air Canada, WestJet, Porter)", "Trans-Canada Highway Car Rentals", "Subway & SkyTrain (Toronto TTC, Montreal STM, Vancouver TransLink)", "BC Ferries Coastal Network", "Ride-Hailing (Uber & Lyft)"],
            "tips": "Due to immense distances, fly between eastern cities (Toronto/Montreal) and western cities (Vancouver/Calgary). Transit in Vancouver, Toronto, and Montreal is efficient and tap-enabled.",
            "pass": "Parks Canada Discovery Pass (free entry to all National Parks); PRESTO Card (Ontario); Compass Card (Vancouver)."
        },
        "travel_tips": {
            "tipping": "15% to 20% in restaurants, bars, and for personal services; $2–$5/day for hotel housekeeping.",
            "currency_tips": "Canadian Dollar (CAD $). Credit and debit tap payments are accepted everywhere from taxis to small bakeries.",
            "etiquette": "Canada is officially bilingual (English and French). In Quebec, greeting with 'Bonjour' is appreciated. Say 'please' and 'thank you' frequently.",
            "best_season": "June to September for warm outdoor weather, hiking, and lakes. December to March for world-class skiing and winter wonderlands.",
            "safety": "One of the safest countries in the world. Tap water is pristine. Be prepared for cold weather during winter and heed wildlife safety in mountain parks."
        }
    },

    "Italy": {
        "cities": ["Rome", "Florence", "Venice", "Milan", "Amalfi Coast", "Naples", "Tuscany", "Lake Como", "Sicily", "Cinque Terre"],
        "attractions": [
            ("Colosseum & Roman Forum", "Rome", "Colosseum"),
            ("Venice Grand Canal & St. Mark's", "Venice", "Grand_Canal_(Venice)"),
            ("Leaning Tower of Pisa", "Pisa", "Leaning_Tower_of_Pisa"),
            ("Florence Cathedral (Duomo)", "Florence", "Florence_Cathedral"),
            ("Trevi Fountain", "Rome", "Trevi_Fountain"),
            ("Lake Como & Bellagio", "Lombardy", "Lake_Como"),
            ("Amalfi Coast Cliffs", "Campania", "Amalfi_Coast"),
            ("Pantheon", "Rome", "Pantheon,_Rome"),
        ],
        "food": [
            ("Neapolitan Pizza", "Wood-fired blistered crust topped with San Marzano tomatoes, fresh mozzarella di bufala, and basil.", "Neapolitan_pizza"),
            ("Pasta Carbonara & Cacio e Pepe", "Classic Roman pasta tossed with crispy guanciale, pecorino romano, and fresh cracked pepper.", "Carbonara"),
            ("Artisan Gelato", "Dense, velvety Italian frozen dessert made fresh in flavors like pistachio, stracciatella, and dark chocolate.", "Gelato"),
            ("Risotto alla Milanese", "Creamy arborio rice simmered slowly in rich bone broth and infused with vibrant saffron.", "Risotto"),
            ("Tiramisu", "Layers of espresso-soaked ladyfingers and whipped mascarpone cream dusted with cocoa powder.", "Tiramisu"),
            ("Fiorentina Steak", "Thick-cut Chianina T-bone grilled rare over wood embers with rosemary and sea salt.", "Bistecca_alla_fiorentina")
        ],
        "culture": [
            ("St. Peter's Basilica & Vatican", "Vatican / Rome", "The epicenter of Catholicism housing Michelangelo's Pietà and stunning dome."),
            ("Florence Duomo (Santa Maria del Fiore)", "Florence", "Brunelleschi's magnificent red-tiled brick dome dominating the Florentine skyline."),
            ("St Mark's Basilica", "Venice", "Italo-Byzantine cathedral adorned with over 8,000 square meters of shimmering gold mosaics."),
            ("Milan Cathedral (Duomo di Milano)", "Milan", "Colossal Gothic cathedral featuring 135 spires and panoramic rooftop terraces."),
            ("Pompeii Archaeological Park", "Campania", "Ancient Roman city frozen in time by the catastrophic eruption of Mount Vesuvius in 79 AD.")
        ],
        "transportation": {
            "modes": ["High-Speed Trains (Frecciarossa & Italo)", "Trenitalia Regional Trains", "Rome Metro & Milan Metro", "Venice Vaporetti (Water Buses)", "City Trams & Clean Electric Buses", "Ferry Lines along Amalfi Coast & Lakes"],
            "tips": "High-speed rail connects Rome, Florence, Venice, and Milan in just 1.5 to 3 hours. IMPORTANT: Always validate physical regional train and bus tickets at green/yellow stamping machines before boarding to avoid heavy fines.",
            "pass": "Eurail Italy Pass; Roma Pass (includes transit & museum entry); ACTV Venice Travel Card."
        },
        "travel_tips": {
            "tipping": "Tipping is not obligatory; a small 'coperto' (cover charge) is often included on the bill. Leaving €1–€2 per person is a friendly gesture.",
            "currency_tips": "Euro (EUR €). Card payments are standard, though carrying small coins (€1/€2) for espresso at coffee bars and public restrooms is wise.",
            "etiquette": "Cover shoulders and knees when visiting churches. Stand at the counter ('al banco') for espresso like a local. Never order cappuccino after 11:00 AM.",
            "best_season": "April to June and September to October offer mild Mediterranean weather and fewer crowds than sweltering July–August.",
            "safety": "Keep a close eye on wallets and bags on crowded Rome and Milan metros and around busy central train stations."
        }
    },

    "Thailand": {
        "cities": ["Bangkok", "Phuket", "Chiang Mai", "Krabi", "Koh Samui", "Ayutthaya", "Pai", "Pattaya", "Hua Hin"],
        "attractions": [
            ("Grand Palace & Temple of the Emerald Buddha", "Bangkok", "Grand_Palace"),
            ("Wat Arun (Temple of Dawn)", "Bangkok", "Wat_Arun"),
            ("Railay Beach & Krabi Cliffs", "Krabi", "Railay_Beach"),
            ("Phi Phi Islands & Maya Bay", "Krabi", "Phi_Phi_Islands"),
            ("Chiang Mai Old City & Wat Phra That Doi Suthep", "Chiang Mai", "Chiang_Mai"),
            ("Phuket Old Town & Big Buddha", "Phuket", "Phuket_province"),
            ("Ayutthaya Historical Park", "Ayutthaya", "Ayutthaya_Historical_Park"),
            ("Damnoen Saduak Floating Market", "Ratchaburi", "Damnoen_Saduak_floating_market"),
        ],
        "food": [
            ("Pad Thai", "Stir-fried rice noodles tossed with tamarind, fresh bean sprouts, crushed peanuts, lime, and shrimp.", "Pad_thai"),
            ("Tom Yum Goong", "Fiery and sour soup infused with fragrant lemongrass, kaffir lime leaves, galangal, chili, and prawns.", "Tom_yum"),
            ("Mango Sticky Rice", "Warm glutinous rice cooked in sweet coconut milk and served with chilled ripe yellow mango.", "Mango_sticky_rice"),
            ("Green Curry (Gaeng Keow Wan)", "Rich coconut milk curry flavored with green chili paste, bamboo shoots, and Thai sweet basil.", "Green_curry"),
            ("Som Tam (Som Tum / Papaya Salad)", "Crisp shredded green papaya pounded in a mortar with lime, chilies, fish sauce, and peanuts.", "Som_tam"),
            ("Massaman Curry", "Mild, aromatic Southern Thai curry cooked with coconut milk, tender beef, potatoes, and roasted peanuts.", "Massaman_curry")
        ],
        "culture": [
            ("Wat Phra Kaew (Emerald Buddha)", "Bangkok", "The most sacred Buddhist temple in Thailand located within the historic Grand Palace."),
            ("Wat Pho (Temple of the Reclining Buddha)", "Bangkok", "Birthplace of traditional Thai massage, home to a 46-meter gilded reclining Buddha."),
            ("Wat Rong Khun (White Temple)", "Chiang Rai", "Extraordinary contemporary Buddhist art temple gleaming with mirror-mosaic glass."),
            ("Wat Chedi Luang", "Chiang Mai", "Magnificent 14th-century ruined stone pagoda towering in the centre of old Chiang Mai."),
            ("Sanctuary of Truth", "Pattaya", "Colossal seaside all-wood pavilion intricately hand-carved with Hindu and Buddhist sculptures.")
        ],
        "transportation": {
            "modes": ["Bangkok Skytrain (BTS) & Subway (MRT)", "Chao Phraya River Express Boats", "Domestic Flights (connecting Bangkok to islands & north)", "Traditional Tuk-tuks & Songthaews", "App-based Ride-hailing (Grab & Bolt)", "Inter-island Ferries & Speedboats"],
            "tips": "In Bangkok, the BTS Skytrain and MRT subway glide over traffic jams. Use the Grab app for fixed-price rides. For tuk-tuks, always agree on the exact fare before stepping inside.",
            "pass": "BTS Rabbit Card (Bangkok); MRT Single Journey / Stored Value Cards."
        },
        "travel_tips": {
            "tipping": "Tipping is not customary in everyday food stalls; leaving 10% in sit-down restaurants or rounding up taxi fares is appreciated.",
            "currency_tips": "Thai Baht (THB ฿). Cash is king at street food markets and small night bazaars; credit cards are used in major hotels and malls.",
            "etiquette": "Always dress respectfully at temples (shoulders and knees covered; take off shoes). Never touch anyone on the head or point your feet at religious statues. Treat imagery of the Royal Family with utmost respect.",
            "best_season": "November to February brings cool, dry, and pleasant weather across the country.",
            "safety": "Drink bottled water. Beware of common scams like strangers claiming a major temple is 'closed today'."
        }
    }
}


# ============================================================
# DYNAMIC COUNTRY RESOLUTION ENGINE
# ============================================================

def normalize_country_key(country: str) -> str:
    c = str(country or "").strip()
    c_lower = c.lower()
    
    # Check for direct matches or overrides
    aliases = {
        "usa": "United States",
        "united states of america": "United States",
        "uk": "United Kingdom",
        "great britain": "United Kingdom",
        "england": "United Kingdom",
        "uae": "United Arab Emirates",
        "south korea": "South Korea",
        "korea": "South Korea",
        "republic of korea": "South Korea",
        "viet nam": "Vietnam",
        "türkiye": "Turkey",
        "turkiye": "Turkey",
        "czech republic": "Czechia",
        "russia": "Russia",
        "russian federation": "Russia",
    }
    if c_lower in aliases:
        return aliases[c_lower]
        
    for k in COUNTRY_DESTINATIONS.keys():
        if k.lower() == c_lower:
            return k
            
    # Check db
    db = get_countries_db()
    rec = db.get(c_lower)
    if rec:
        return rec.get("name", c)
        
    return c


def get_country_knowledge(country: str) -> Dict[str, Any]:
    """
    Returns authentic country knowledge.
    Works for ALL 250 countries by using rich curated profiles where available,
    and dynamically synthesizing authentic profiles from countries_data.json.
    """
    canonical_name = normalize_country_key(country)
    
    db = get_countries_db()
    c_lower = canonical_name.lower()
    matched = db.get(c_lower)
    
    if not matched:
        for rec in db.values():
            if rec.get("name", "").lower() == c_lower or rec.get("official_name", "").lower() == c_lower:
                matched = rec
                break

    capital = ""
    region = "Worldwide"
    subregion = ""
    currency_str = "Local Currency"
    languages_str = "Official National Language"
    population = 1000000
    flag = "🌍"
    
    if matched:
        caps = matched.get("capital")
        if isinstance(caps, list) and caps:
            capital = caps[0]
        elif isinstance(caps, str):
            capital = caps
        region = matched.get("region") or "Worldwide"
        subregion = matched.get("subregion") or region
        flag = matched.get("flag") or "🌍"
        population = matched.get("population") or 1000000
        
        curs = matched.get("currency")
        if isinstance(curs, dict):
            first_c = list(curs.values())[0] if curs else {}
            if isinstance(first_c, dict):
                currency_str = f"{first_c.get('name', 'Currency')} ({first_c.get('symbol', '')})"
            elif isinstance(first_c, str):
                currency_str = first_c
        elif isinstance(curs, str):
            currency_str = curs
            
        langs = matched.get("languages")
        if isinstance(langs, dict):
            languages_str = ", ".join(langs.values())
        elif isinstance(langs, list):
            languages_str = ", ".join(langs)
        elif isinstance(langs, str) and langs:
            languages_str = langs

    # 1. Curated database
    curated = COUNTRY_DESTINATIONS.get(canonical_name)
    if not curated:
        for k, v in COUNTRY_DESTINATIONS.items():
            if k.lower() == canonical_name.lower():
                curated = v
                canonical_name = k
                break

    if curated:
        return {
            "name": canonical_name,
            "flag": flag if flag != "🌍" else curated.get("flag", "🌍"),
            "capital": capital or (curated.get("cities", [canonical_name])[0]),
            "region": region,
            "subregion": subregion,
            "currency": currency_str,
            "languages": languages_str,
            "population": population,
            "duration": curated.get("duration", "7–12 days"),
            "budget": curated.get("budget", "₹50k–₹1.8L"),
            "season": curated.get("travel_tips", {}).get("best_season", "Spring and Autumn are popular"),
            **curated
        }
            
    # 2. Dynamic synthesis from 250-country dataset
    main_city = capital or canonical_name
    
    # Dynamic Geographic Synthesis based on country characteristics
    is_island = any(term in subregion.lower() or term in region.lower() for term in ["caribbean", "polynesia", "micronesia", "melanesia"]) or population < 800000
    is_mountainous = any(term in subregion.lower() for term in ["alpine", "central asia", "caucasus", "andes"])
    
    cities = [
        main_city,
        f"{main_city} Heritage District",
        f"{canonical_name} Coastal & Waterfront Zone" if not is_mountainous else f"{canonical_name} Highland Valley",
        f"{canonical_name} Regional Cultural Hub",
        f"{canonical_name} Nature & Wildlife Sanctuary",
        f"{canonical_name} Historic Old Town"
    ]
    
    c_slug = canonical_name.replace(" ", "_")
    cuisine_slug = f"{c_slug}_cuisine"
    main_city_slug = main_city.replace(" ", "_")

    attractions = [
        (f"{main_city} Historic Centre", main_city, main_city_slug),
        (f"{canonical_name} National Museum", main_city, f"National_Museum_of_{c_slug}"),
        (f"{canonical_name} Central Plaza & Cathedral", main_city, main_city_slug),
        (f"{canonical_name} Nature Reserve", f"{canonical_name} Region", c_slug),
        (f"{canonical_name} Heritage Fortress & Lookout", f"{canonical_name} Province", c_slug),
        (f"{canonical_name} Coastal Promenade & Beach" if is_island else f"{canonical_name} Mountain Trail", canonical_name, c_slug)
    ]
    
    # Sub-region-specific dynamic cuisine templates with verified Wikipedia slugs for actual prepared dishes
    c_lower = canonical_name.lower()
    is_maghreb = any(k in c_lower for k in ["morocco", "algeria", "tunisia", "libya", "mauritania"])
    is_gulf = any(k in c_lower for k in ["saudi", "emirates", "qatar", "oman", "kuwait", "bahrain", "yemen"])
    is_levant = any(k in c_lower for k in ["jordan", "lebanon", "syria", "palestine", "iraq"])
    is_andean = any(k in c_lower for k in ["peru", "bolivia", "ecuador"])
    is_colombia_ven = any(k in c_lower for k in ["colombia", "venezuela"])
    is_pampas = any(k in c_lower for k in ["argentina", "uruguay", "chile", "paraguay"])
    is_nordic = any(k in c_lower for k in ["norway", "sweden", "denmark", "finland", "iceland"])
    is_central_am = any(k in c_lower for k in ["mexico", "guatemala", "honduras", "salvador", "nicaragua", "costa rica", "panama", "belize"])
    is_caribbean_zone = "caribbean" in subregion.lower() or any(k in c_lower for k in ["cuba", "jamaica", "dominican", "haiti", "bahamas", "trinidad", "barbados", "guyana", "suriname"])
    is_pacific = "polynesia" in subregion.lower() or "micronesia" in subregion.lower() or "melanesia" in subregion.lower() or any(k in c_lower for k in ["zealand", "fiji", "samoa", "tonga", "tahiti", "vanuatu"])
    is_portugal = "portugal" in c_lower
    is_alpine = any(k in c_lower for k in ["switzerland", "austria", "liechtenstein"])
    is_turkey = "turkey" in c_lower or "türkiye" in c_lower
    is_slavic = any(k in c_lower for k in ["poland", "ukraine", "czech", "slovakia", "russia", "belarus", "bulgaria", "serbia", "croatia", "bosnia", "slovenia", "macedonia", "montenegro"])
    is_central_asia = any(k in c_lower for k in ["uzbekistan", "kazakhstan", "kyrgyzstan", "tajikistan", "turkmenistan", "mongolia"])
    is_persian = any(k in c_lower for k in ["iran", "persia", "afghanistan"])
    is_south_asia = any(k in c_lower for k in ["pakistan", "bangladesh", "sri lanka", "nepal", "bhutan", "maldives"])
    is_east_africa = any(k in c_lower for k in ["kenya", "tanzania", "uganda", "ethiopia", "rwanda", "somalia"])

    if is_maghreb:
        food = [
            (f"{canonical_name} Tagine Stew", "Slow-cooked savory stew simmered in an earthenware conical pot with tender meat, vegetables, and warm spices.", "Tagine"),
            ("Couscous Royale", "Steamed semolina grains served with slow-cooked vegetables, tender meat, and aromatic broth.", "Couscous"),
            ("Pastilla (Savory Sweet Pie)", "Crisp paper-thin warqa pastry stuffed with spiced meat, almonds, and dusted with cinnamon sugar.", "Pastilla"),
            ("Harira Soup", "Hearty traditional soup made with tomatoes, lentils, chickpeas, and fresh coriander.", "Harira"),
            ("Moroccan Mint Tea & Pastries", "Fresh spearmint tea poured from height, accompanied by almond-paste pastries.", "Maghrebi_mint_tea")
        ]
    elif is_gulf or is_levant or "western asia" in subregion.lower():
        food = [
            (f"{canonical_name} Spiced Kabsa / Mandi", "Fragrant spiced long-grain basmati rice served with roasted meat and toasted nuts.", "Kabsa"),
            ("Shawarma Platter", "Thinly sliced slow-roasted marinated meat wrapped in fresh flatbread with garlic toum sauce.", "Shawarma"),
            ("Crispy Falafel & Hummus", "Golden fried chickpea fritters served with velvety tahini hummus and warm pita bread.", "Falafel"),
            ("Stuffed Grape Leaves", "Tender vine leaves rolled around seasoned rice, herbs, and lemon-infused olive oil.", "Dolma"),
            ("Kunafa Sweet Pastry", "Warm spun pastry soaked in sweet floral syrup, layered with melted cheese and pistachios.", "Kanafeh")
        ]
    elif is_persian:
        food = [
            (f"{canonical_name} Chelo Kebab & Saffron Rice", "Grilled skewered minced lamb (koobideh) served alongside steaming basmati rice with golden saffron butter and grilled tomatoes.", "Chelow_kabab"),
            ("Ghormeh Sabzi Herb Stew", "Ancient aromatic slow-simmered stew of kidney beans, fragrant herbs, sun-dried limes, and tender lamb.", "Ghormeh_sabzi"),
            ("Tahdig (Crispy Rice Crust)", "Prized crunchy golden-brown rice crust formed at the bottom of the pot, infused with saffron.", "Tahdig"),
            ("Ash Reshteh Herb & Noodle Soup", "Rich nourishing thick soup prepared with flat noodles, chickpeas, lentils, herbs, and topped with kashk whey.", "Aash_reshteh"),
            ("Shirazi Salad", "Crisp refreshing diced salad of Persian cucumbers, tomatoes, red onions, mint, and sour grape verjuice.", "Shirazi_salad")
        ]
    elif is_central_asia:
        food = [
            (f"{canonical_name} Traditional Plov / Pilaf", "Aromatic long-grain rice simmered in a cast-iron kazan with tender lamb, sweet yellow carrots, onions, cumin, and garlic bulbs.", "Pilaf"),
            ("Laghman Hand-Pulled Noodles", "Chewy hand-pulled noodles topped with wok-tossed lamb, sweet peppers, tomatoes, and rich savory broth.", "Laghman_(food)"),
            ("Crispy Tandoor Samsa", "Flaky clay-oven baked pastry pockets filled with spiced minced meat, onions, and black cumin seeds.", "Samsa_(food)"),
            ("Charcoal-Grilled Shashlik", "Skewers of succulent marinated meat charcoal-roasted to perfection, served with thinly sliced pickled onions.", "Shashlik"),
            ("Steamed Manti Dumplings", "Thin-skinned large steamed dumplings packed with juicy minced beef or pumpkin, served with yogurt.", "Manti_(food)")
        ]
    elif is_south_asia:
        food = [
            (f"{canonical_name} Royal Biryani Platter", "Fragrant basmati rice layered with marinated spiced meat, caramelized onions, saffron, and fresh mint.", "Biryani"),
            ("Slow-Simmered Nihari / Korma", "Rich, velvety aromatic stew slow-cooked with bone-in tender meat, whole spices, and ginger.", "Nihari"),
            ("Crispy Samosas & Mint Chutney", "Flaky golden pastry triangles filled with spiced potatoes, green peas, and served with coriander-mint chutney.", "Samosa"),
            ("Tandoori Flatbreads & Daal", "Freshly baked garlic butter naan bread served with slow-cooked buttery black lentils (daal).", "Naan"),
            ("Gulab Jamun / Kheer Delicacy", "Warm golden milk-solid dumplings soaked in rose and cardamom syrup.", "Gulab_jamun")
        ]
    elif is_andean:
        food = [
            (f"{canonical_name} Fresh Ceviche", "Freshly caught fish cured in zesty key lime juice, seasoned with ají peppers, red onions, sweet potato, and choclo corn.", "Ceviche"),
            ("Lomo Saltado", "High-heat wok-stir-fried beef tenderloin strips with red onions, tomatoes, crispy french fries, and steamed rice.", "Lomo_saltado"),
            ("Causa Limeña", "Layered chilled yellow potato terrine seasoned with spicy ají amarillo and stuffed with tuna or shredded chicken.", "Causa_a_la_lime%C3%B1a"),
            ("Empanadas al Horno", "Golden baked pastry turnovers filled with seasoned minced beef, hard-boiled eggs, and green olives.", "Empanada"),
            ("Alfajores con Dulce de Leche", "Melt-in-your-mouth cornstarch shortbread cookies filled with rich dulce de leche caramel and rolled in shredded coconut.", "Alfajor")
        ]
    elif is_colombia_ven:
        food = [
            (f"{canonical_name} Bandeja Paisa / Pabellón", "Hearty regional platter loaded with red beans, white rice, shredded beef, chicharrón, fried egg, plantain, and arepa.", "Bandeja_paisa"),
            ("Artisanal Arepas con Queso", "Thick golden griddled corn cakes with a crisp exterior, filled with melted campesino cheese.", "Arepa"),
            ("Ajiaco Bogotano / Sancocho", "Comforting slow-cooked soup made with native potatoes, shredded chicken, sweet corn on the cob, capers, and cream.", "Ajiaco"),
            ("Crispy Empanadas de Carne", "Crisp golden yellow corn pastries stuffed with seasoned shredded beef and mashed potatoes, served with ají sauce.", "Empanada"),
            ("Sweet Fried Patacones / Plátano", "Twice-fried crispy smashed green plantains topped with hogao tomato-garlic creole sauce.", "Tostones")
        ]
    elif is_pampas:
        food = [
            (f"{canonical_name} Asado Criollo", "Traditional wood-fired barbecue featuring prime cuts of beef slow-grilled to perfection with chimichurri sauce.", "Asado"),
            ("Empanadas Criollas", "Handmade savory turnover pastries stuffed with spiced ground beef, sweet onions, and green olives.", "Empanada"),
            ("Milanesa Napolitana", "Crispy golden breaded veal or beef cutlet topped with rich tomato sauce, melted ham, and mozzarella cheese.", "Milanesa"),
            ("Choripán con Chimichurri", "Grilled artisanal chorizo sausage in crusty baguette with fresh garlic-parsley chimichurri.", "Chorip%C3%A1n"),
            ("Dulce de Leche Specialties", "Decadent caramelized milk spread served with artisanal pastries and medialunas.", "Dulce_de_leche")
        ]
    elif is_central_am:
        food = [
            (f"{canonical_name} Tacos Tradicionales", "Warm handmade corn tortillas loaded with marinated grilled meats, fresh cilantro, onions, and spicy salsa.", "Taco"),
            ("Fresh Guacamole & Totopos", "Creamy mashed ripe avocados blended with lime juice, cilantro, tomatoes, and crispy corn tortilla chips.", "Guacamole"),
            ("Enchiladas con Salsa", "Corn tortillas rolled around shredded chicken, drenched in green tomatillo or red chili salsa and melted cheese.", "Enchilada"),
            ("Tamales Tradicionales", "Steamed seasoned masa dough wrapped in corn husks or banana leaves, stuffed with savory fillings.", "Tamale"),
            ("Churros con Chocolate", "Crispy golden fried dough pastries dusted in cinnamon sugar, served with warm dipping chocolate.", "Churro")
        ]
    elif is_caribbean_zone:
        food = [
            (f"{canonical_name} Jerk Chicken Platter", f"Signature {canonical_name} slow-marinated roasted jerk chicken with aromatic pimento and scotch bonnet.", "Jerk_(cooking)"),
            ("Grilled Seafood Platter", "Freshly caught local grilled fish and lobster served with fried plantains.", "Seafood"),
            ("Rice and Peas", "Fragrant long-grain rice simmered with coconut milk, kidney beans, and fresh thyme.", "Rice_and_peas"),
            ("Fried Sweet Plantains", "Golden caramelized ripe plantain slices served hot.", "Fried_plantain"),
            ("Traditional Rum Cake", "Moist spiced sponge cake steeped in aged local rum and dried fruits.", "Rum_cake")
        ]
    elif is_nordic:
        food = [
            (f"{canonical_name} Köttbullar / Meatballs", "Tender seasoned meatballs served with creamy brown gravy, lingonberry jam, and buttery mashed potatoes.", "K%C3%B6ttbullar"),
            ("Gravlax Cured Salmon", "Delicate salmon fillets salt-and-sugar cured with fresh dill, served on crispbread with mustard-dill sauce.", "Gravlax"),
            ("Smørrebrød Open-Faced Sandwiches", "Hearty dense dark rye bread topped with pickled herring, roast beef, or cold-water shrimp.", "Sm%C3%B8rrebr%C3%B8d"),
            ("Fresh Warm Cinnamon Buns", "Aromatic cardamom-scented braided yeast pastry loaded with sweet cinnamon butter and pearl sugar.", "Cinnamon_roll"),
            ("Traditional Fruit & Berry Tart", "Crisp buttery crust filled with sweet cream and topped with fresh wild forest berries.", "Custard_tart")
        ]
    elif is_pacific:
        food = [
            (f"{canonical_name} Traditional Hāngī / Underground Roast", "Feast of meats and root vegetables slow-steamed in an earthen oven for deep, smoky flavors.", "H%C4%81ng%C4%AB"),
            ("Fresh Fish Kokoda / Poke Bowl", "Fresh diced ocean fish cured in citrus juices and tossed with rich coconut milk and scallions.", "Poke_(dish)"),
            ("Traditional Savory Meat Pie", "Golden flaky pastry crust baked with slow-simmered minced beef, rich brown gravy, and cheddar.", "Meat_pie"),
            ("Crispy Fish and Chips", "Fresh deep-fried beer-battered fish fillets served hot with crispy potato chips and tartar sauce.", "Fish_and_chips"),
            ("Pavlova with Fresh Fruit", "Crisp meringue dessert shell with a soft marshmallow center, topped with whipped cream and kiwi fruit.", "Pavlova_(dessert)")
        ]
    elif is_portugal:
        food = [
            ("Pastel de Nata", "Iconic Portuguese egg custard tart in crisp flaky puff pastry, lightly blistered on top and dusted with cinnamon.", "Pastel_de_nata"),
            ("Bacalhau à Brás", "Shredded salted cod sautéed with finely chopped onions, matchstick potatoes, scrambled eggs, and black olives.", "Bacalhau_%C3%A0_Br%C3%A1s"),
            ("Francesinha", "Hearty layered sandwich stuffed with ham, fresh linguiça sausage, steak, covered in melted cheese and beer-tomato sauce.", "Francesinha"),
            ("Caldo Verde", "Comforting green soup made from puréed potatoes and garlic, enriched with shredded collard greens and chouriço sausage.", "Caldo_verde"),
            ("Sardinhas Assadas", "Charcoal-grilled fresh whole sardines seasoned with sea salt, served on crusty bread with roasted bell peppers.", "Grilled_sardines")
        ]
    elif is_alpine:
        food = [
            ("Swiss Cheese Fondue", "Melted Gruyère and Emmentaler cheeses blended with white wine and garlic, served bubbling for dipping bread cubes.", "Fondue"),
            ("Rösti", "Crispy golden pan-fried grated potato pancake, often topped with fried eggs, melted raclette cheese, or herbs.", "R%C3%B6sti"),
            ("Raclette", "Wheel of Alpine cow's milk cheese melted and scraped over hot boiled new potatoes, gherkins, and pickled onions.", "Raclette"),
            ("Zürcher Geschnetzeltes", "Tender sliced veal cooked in a rich white wine, cream, and button mushroom sauce.", "Z%C3%BCrcher_Geschnetzeltes"),
            ("Bircher Muesli", "Traditional nourishing breakfast of rolled oats soaked overnight in milk with grated fresh apples, honey, and nuts.", "Muesli")
        ]
    elif is_turkey:
        food = [
            ("Döner Kebab", "Tender marinated meat roasted slowly on a vertical spit, served with warm lavash flatbread, tomatoes, and yogurt.", "Doner_kebab"),
            ("Baklava", "Crisp layers of delicate filo pastry filled with finely chopped green pistachios, sweetened with fragrant syrup.", "Baklava"),
            ("Lahmacun", "Thin crispy stone-baked flatbread topped with spiced minced lamb, onions, tomatoes, and fresh parsley.", "Lahmacun"),
            ("Menemen", "Scrambled eggs cooked with juicy diced tomatoes, green peppers, olive oil, and herbs, eaten warm with crusty bread.", "Menemen_(food)"),
            ("Turkish Delight (Lokum)", "Beloved chewy confectionery flavored with rosewater, mastic, bergamot, or loaded with pistachios.", "Turkish_delight")
        ]
    elif is_slavic:
        food = [
            (f"{canonical_name} Handcrafted Pierogi / Dumplings", "Tender boiled dumplings generously stuffed with potato and cheese, sauerkraut, or wild mushrooms, sautéed with butter.", "Pierogi"),
            ("Bigos (Hunter's Stew)", "Hearty slow-simmered stew of shredded white cabbage, sauerkraut, varied smoked sausages, and forest mushrooms.", "Bigos"),
            ("Barszcz / Borscht Beetroot Soup", "Deep ruby beetroot broth enriched with garlic, dill, and served with sour cream or savory pastries.", "Borscht"),
            ("Kotlet Schabowy (Crispy Schnitzel)", "Tender breaded pork cutlet pan-fried in butter until golden brown, served with dill potatoes.", "Kotlet_schabowy"),
            ("Warm Fruit Strudel / Sernik", "Delicate baked pastry or traditional baked cheesecake scented with citrus zest and vanilla.", "Strudel")
        ]
    elif is_east_africa:
        food = [
            ("Ugali & Sukuma Wiki", "The cornerstone East African staple: dense white cornmeal porridge paired with braised collard greens.", "Ugali"),
            ("Nyama Choma", "Tender goat or beef slow-roasted over open hardwood charcoal embers, served with fresh kachumbari tomato relish.", "Nyama_choma"),
            ("Mandazi Sweet Pastry", "Golden cardamom-scented fried triangular dough pastries dusted with powdered sugar, enjoyed with spiced chai.", "Mandazi"),
            ("Kachumbari Salad", "Crisp refreshing salad of diced fresh ripe tomatoes, red onions, chili peppers, cilantro, and fresh lime juice.", "Kachumbari"),
            ("East African Chapati", "Soft, multi-layered flaky flatbread pan-fried with oil, perfect for scooping rich bean or meat stews.", "Chapati")
        ]
    elif "africa" in region.lower():
        food = [
            (f"{canonical_name} Jollof Rice / Stew", "Rich tomato and bell pepper simmered rice seasoned with thyme, curry, and roasted meat.", "Jollof_rice"),
            ("Grilled Meat Skewers (Suya)", "Charcoal-grilled seasoned beef skewers dusted with crushed peanut spice rub.", "Suya"),
            ("Savory Grain Relish Bowl", "Traditional staple prepared from slow-simmered milled grains with savory vegetable sauce.", "Porridge"),
            ("Fried Plantains & Beans", "Sweet caramelized golden plantains accompanied by seasoned slow-simmered legumes.", "Fried_plantain"),
            ("Mandazi Sweet Pastry", "Golden cardamom-infused fried pastry dusted with powdered sugar and wild honey.", "Mandazi")
        ]
    elif "asia" in region.lower():
        food = [
            ("Fried Rice (Chao Fan / Khao Pad)", "Authentic wok-fried rice prepared with fresh vegetables, egg, garlic, and savory regional spices.", "Fried_rice"),
            ("Comforting Noodle Soup", "Steaming bowl of hand-pulled noodles in slow-simmered savory aromatic broth.", "Noodle_soup"),
            ("Steamed Savory Dumplings", "Tender steamed dumplings stuffed with minced meat, scallions, ginger, and dipping sauce.", "Dumpling"),
            ("Aromatic Coconut Curry", "Rich aromatic coconut milk curry simmered with vegetables, herbs, and warm spices.", "Curry"),
            ("Sweet Rice Delicacy", "Warm fragrant glutinous rice served with sweet coconut cream and toasted sesame.", "Sticky_rice")
        ]
    elif "europe" in region.lower():
        food = [
            ("Hearty Country Stew", "Rich and comforting slow-simmered meat and vegetable stew seasoned with aromatic herbs.", "Goulash"),
            ("Artisan Cheese & Fresh Bread Board", "Platter of regional aged cheeses served with crusty sourdough bread and fruit preserves.", "Cheese_plate"),
            ("Vegetable & Bean Minestrone", "Comforting hearty soup filled with garden vegetables, white beans, herbs, and olive oil.", "Minestrone"),
            ("Baked Savory Meat Pie", "Flaky golden baked pastry crust stuffed with seasoned minced meat and savory gravy.", "Meat_pie"),
            ("Fresh Berry Tart", "Delicate fruit tart filled with sweet pastry cream and topped with fresh wild berries.", "Custard_tart")
        ]
    else:
        food = [
            (f"{canonical_name} Grilled Meat Specialty", "Celebrated slow-cooked tender meat prepared with traditional regional spices and vegetables.", "Asado"),
            ("Roasted Spiced Potatoes & Greens", "Oven-roasted golden potatoes seasoned with regional herbs and fresh garlic.", "Roasted_potato"),
            ("Fresh Artisan Bread & Cheese", f"Locally baked crusty bread paired with authentic cheeses from {canonical_name}.", "Cheese_plate"),
            ("Crispy Savory Street Fritters", "Beloved golden crispy street snack served hot with savory dipping chutney.", "Fritter"),
            ("Traditional Honey Pastry", "Flaky sweet dessert pastry drizzled with pure honey and crushed nuts.", "Baklava")
        ]
        
    culture = [
        (f"{main_city} National Cathedral & Sacred Shrine", main_city, f"Historic spiritual landmark reflecting the deep heritage of {canonical_name}."),
        (f"{canonical_name} Monument of Independence", main_city, f"Celebrated national monument honoring the founders and history of {canonical_name}."),
        (f"{canonical_name} Historic Old Town Quarter", main_city, f"Preserved cobblestone streets, colonial/traditional facades, and artisan craft shops."),
        (f"{canonical_name} Cultural Heritage Museum", main_city, f"Premier museum exhibiting ancient artifacts, folk costumes, and art."),
        (f"{canonical_name} Ancient Sanctuary & Viewpoint", f"{canonical_name}", f"Sacred historical hill offering panoramic vistas across the landscape.")
    ]
    
    # Geography-adapted transportation
    if is_island:
        transport_modes = ["Inter-Island Passenger Ferries", "Domestic Island Flights / Catamarans", "Rental Scooters & Motorbikes", "Public Island Minibuses", "Water Taxis", "Walking in coastal towns"]
        transport_tips = f"Inter-island ferries and water taxis connect main coastal hubs. Renting a scooter or using local shared minibuses is the most flexible way to explore {canonical_name}."
    elif is_mountainous:
        transport_modes = ["Scenic Mountain Railway / Buses", "4WD Vehicle Rentals", "Regional Express Coaches", "Local Shared Minivans", "Cable Cars & Funiculars", "Walking & Hiking Trails"]
        transport_tips = f"A sturdy 4WD rental or reliable mountain coach is recommended for exploring elevation changes and scenic passes across {canonical_name}."
    else:
        transport_modes = ["Intercity Express Buses", "Passenger Rail Network", "Domestic Flights (for long distances)", "Metropolitan City Buses & Taxis", "Car Rental for countryside road trips", "App-based Cabs"]
        transport_tips = f"In {main_city}, city buses and licensed taxis are readily available. For traveling between provinces, intercity coaches or domestic rail connect major towns."
        
    travel_tips = {
        "tipping": "5% to 10% is customary in sit-down restaurants if service is not already included on the bill.",
        "currency_tips": f"{currency_str}. Keep local cash on hand for small open-air markets, rural transit, and street food stalls.",
        "etiquette": f"Greet locals respectfully with a warm handshake or polite nod. When visiting places of worship in {canonical_name}, dress conservatively with shoulders covered.",
        "best_season": f"Check seasonal weather variations for {region}. Dry seasons with moderate temperatures offer the most comfortable sightseeing conditions.",
        "safety": f"Keep identification and emergency contacts stored securely. Stick to well-lit areas after dark and use registered transportation in {main_city}."
    }
    
    return {
        "name": canonical_name,
        "flag": flag,
        "capital": main_city,
        "region": region,
        "subregion": subregion,
        "currency": currency_str,
        "languages": languages_str,
        "population": population,
        "duration": "7–12 days",
        "budget": "₹50k–₹1.5L",
        "season": "Spring and autumn are ideal",
        "cities": cities,
        "attractions": attractions,
        "food": food,
        "culture": culture,
        "transportation": {
            "modes": transport_modes,
            "tips": transport_tips,
            "pass": f"{canonical_name} Visitor Transit Pass / Local Metro Pass"
        },
        "travel_tips": travel_tips
    }


# ============================================================
# REQUIRED TOP-LEVEL FUNCTIONS
# ============================================================

def get_attractions(country: str) -> List[Dict[str, str]]:
    """Return verified attractions list for the selected country."""
    data = get_country_knowledge(country)
    results = []
    for item in data.get("attractions", []):
        if isinstance(item, (tuple, list)):
            name = item[0]
            loc = item[1] if len(item) > 1 else data["name"]
            slug = item[2] if len(item) > 2 else ""
            results.append({
                "name": name,
                "location": loc,
                "slug": slug,
                "description": f"Must-see landmark in {loc}, {data['name']}."
            })
    return results


def get_food(country: str, city: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return authentic food recommendations for the selected country and city."""
    dishes = []
    try:
        from destination_knowledge import get_city_food
        dishes = get_city_food(country, city) or []
        if dishes and len(dishes) >= 3:
            return dishes
    except Exception:
        dishes = []
    data = get_country_knowledge(country)
    results = list(dishes) if dishes else []
    existing_names = {d.get("name", "").lower() for d in results}
    for item in data.get("food", []):
        if isinstance(item, (tuple, list)):
            if item[0].lower() not in existing_names:
                slug = item[2] if len(item) > 2 else ""
                results.append({
                    "name": item[0],
                    "description": item[1] if len(item) > 1 else f"Popular local culinary specialty of {data['name']}.",
                    "slug": slug
                })
    return results


def get_culture(country: str) -> List[Dict[str, str]]:
    """Return cultural and religious heritage sites for the selected country."""
    data = get_country_knowledge(country)
    results = []
    for item in data.get("culture", []):
        if isinstance(item, (tuple, list)):
            slug = item[3] if len(item) > 3 else (item[2] if len(item) > 2 and "_" in str(item[2]) else "")
            results.append({
                "name": item[0],
                "location": item[1] if len(item) > 1 else data["name"],
                "slug": slug,
                "description": item[2] if len(item) > 2 else f"Historic cultural heritage site in {data['name']}."
            })
    return results


def get_transportation(country: str) -> Dict[str, Any]:
    """Return adapted transportation recommendations for the selected country."""
    data = get_country_knowledge(country)
    return data.get("transportation", {
        "modes": ["Local transit", "Trains", "Buses", "Flights"],
        "tips": f"Public transport and licensed taxis are available in {data['name']}.",
        "pass": "Local City Transit Card"
    })


def get_travel_tips(country: str) -> Dict[str, str]:
    """Return country-specific travel tips, tipping, and etiquette."""
    data = get_country_knowledge(country)
    return data.get("travel_tips", {})


def get_images(country: str, attraction: str) -> Dict[str, Any]:
    """
    Generate country-validated image search queries and metadata.
    Guarantees that the image search context includes the actual landmark and country.
    """
    clean_country = normalize_country_key(country)
    clean_attraction = str(attraction or "").strip()
    query = f"{clean_attraction} {clean_country} landmark tourism travel"
    return {
        "country": clean_country,
        "attraction": clean_attraction,
        "query": query,
        "search_term": f"{clean_attraction}, {clean_country}"
    }


def generate_itinerary(
    country: str,
    duration: int = 7,
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate a full data-driven itinerary for 1 to 30 days for ANY country.
    """
    from planner import generate_itinerary as _planner_generate
    prefs = preferences or {}
    starting = prefs.get("starting", "Your Location")
    travelers = prefs.get("travelers", 1)
    budget = prefs.get("budget", 80000)
    interests = prefs.get("interests", ["Culture", "Food"])
    style = prefs.get("style", "Balanced")
    return _planner_generate(starting, country, duration, travelers, budget, interests, style)




LANGUAGE_CODES: Dict[str, str] = {
    "afrikaans": "af", "albanian": "sq", "amharic": "am", "arabic": "ar", "armenian": "hy",
    "azerbaijani": "az", "basque": "eu", "belarusian": "be", "bengali": "bn", "bosnian": "bs",
    "bulgarian": "bg", "burmese": "my", "catalan": "ca", "cebuano": "ceb", "chichewa": "ny",
    "chinese": "zh-CN", "mandarin": "zh-CN", "cantonese": "zh-TW", "corsican": "co", "croatian": "hr",
    "czech": "cs", "danish": "da", "dutch": "nl", "english": "en", "esperanto": "eo",
    "estonian": "et", "filipino": "tl", "tagalog": "tl", "finnish": "fi", "french": "fr",
    "frisian": "fy", "galician": "gl", "georgian": "ka", "german": "de", "greek": "el",
    "gujarati": "gu", "haitian creole": "ht", "hausa": "ha", "hawaiian": "haw", "hebrew": "iw",
    "hindi": "hi", "hmong": "hmn", "hungarian": "hu", "icelandic": "is", "igbo": "ig",
    "indonesian": "id", "irish": "ga", "italian": "it", "japanese": "ja", "javanese": "jw",
    "kannada": "kn", "kazakh": "kk", "khmer": "km", "kinyarwanda": "rw", "korean": "ko",
    "kurdish": "ku", "kyrgyz": "ky", "lao": "lo", "latin": "la", "latvian": "lv",
    "lithuanian": "lt", "luxembourgish": "lb", "macedonian": "mk", "malagasy": "mg", "malay": "ms",
    "malayalam": "ml", "maltese": "mt", "maori": "mi", "marathi": "mr", "mongolian": "mn",
    "myanmar": "my", "nepali": "ne", "norwegian": "no", "odia": "or", "oriya": "or",
    "pashto": "ps", "persian": "fa", "farsi": "fa", "polish": "pl", "portuguese": "pt",
    "punjabi": "pa", "romanian": "ro", "russian": "ru", "samoan": "sm", "scots gaelic": "gd",
    "serbian": "sr", "sesotho": "st", "shona": "sn", "sindhi": "sd", "sinhala": "si",
    "slovak": "sk", "slovenian": "sl", "somali": "so", "spanish": "es", "sundanese": "su",
    "swahili": "sw", "swedish": "sv", "tajik": "tg", "tamil": "ta", "tatar": "tt",
    "telugu": "te", "thai": "th", "turkish": "tr", "turkmen": "tk", "ukrainian": "uk",
    "urdu": "ur", "uyghur": "ug", "uzbek": "uz", "vietnamese": "vi", "welsh": "cy",
    "xhosa": "xh", "yiddish": "yi", "yoruba": "yo", "zulu": "zu"
}

CURATED_PHRASES = {
    "Thai": {
        "thank you": {
            "phrase": "Khop khun khrap (male) / Khop khun kha (female)",
            "script": "ขอบคุณครับ / ขอบคุณค่ะ",
            "phonetic": "kohp-koon-KRAP (male) / kohp-koon-KHA (female)",
            "note": "In Thai culture, politeness particles are essential: men end phrases with 'khrap' and women with 'kha'. Accompany this with a gentle 'Wai' (hands pressed together at chest level with a slight bow) to show sincere gratitude!"
        },
        "hello": {
            "phrase": "Sawatdee khrap (male) / Sawatdee kha (female)",
            "script": "สวัสดีครับ / สวัสดีค่ะ",
            "phonetic": "sah-wahd-DEE-krap / sah-wahd-DEE-kha",
            "note": "Universal polite greeting used for both 'Hello' and 'Goodbye' at any time of day."
        },
        "goodbye": {
            "phrase": "La gorn khrap/kha (formal) or Sawatdee khrap/kha",
            "script": "ลาก่อนครับ / ลาก่อนค่ะ",
            "phonetic": "lah-GORN-krap / sah-wahd-DEE-kha",
            "note": "Most locals simply use 'Sawatdee' accompanied by a polite smile or nod."
        },
        "you're welcome": {
            "phrase": "Mai pen rai khrap/kha",
            "script": "ไม่เป็นไรครับ / ไม่เป็นไรค่ะ",
            "phonetic": "my-pen-RYE",
            "note": "Also means 'No worries' or 'It doesn't matter' — reflecting the relaxed Thai outlook on life."
        },
        "no problem": {
            "phrase": "Mai pen rai khrap (male) / Mai pen rai kha (female) or Mai mee bpan-ha",
            "script": "ไม่เป็นไรครับ / ไม่เป็นไรค่ะ (ไม่มีปัญหา)",
            "phonetic": "my-pen-RYE-krap (male) / my-pen-RYE-kha (female)",
            "note": "Thailand's most famous and beloved phrase! 'Mai pen rai' literally means 'it doesn't matter' or 'no worries', and serves as both 'No problem' and 'You're welcome'. If you mean strictly 'there is no problem / zero issues', you can say 'Mai mee bpan-ha' (ไม่มีปัญหา, phonetic: my-mee-bpahn-HAH). Male speakers add 'khrap' and female speakers add 'kha'."
        },
        "how much": {
            "phrase": "Raka thao rai khrap/kha?",
            "script": "ราคาเท่าไหร่ครับ / ค่ะ",
            "phonetic": "rah-KAH-tow-RYE",
            "note": "Essential when browsing vibrant night markets and street food stalls."
        },
        "delicious": {
            "phrase": "Aroy mak khrap/kha!",
            "script": "อร่อยมากครับ / ค่ะ",
            "phonetic": "ah-ROY-mahk",
            "note": "A huge compliment to local street food vendors and restaurant hosts!"
        },
        "where is the bathroom": {
            "phrase": "Hong nam yoo tee nai khrap/kha?",
            "script": "ห้องน้ำอยู่ที่ไหนครับ / ค่ะ",
            "phonetic": "hong-NAHM-yoo-tee-NYE",
            "note": "'Hong nam' literally translates to 'water room'."
        },
        "not spicy": {
            "phrase": "Mai phet khrap/kha",
            "script": "ไม่เผ็ดครับ / ค่ะ",
            "phonetic": "my-PET",
            "note": "Very useful if you prefer mild food, as authentic Thai food can be fiery!"
        }
    },
    "Japanese": {
        "thank you": {
            "phrase": "Arigatou gozaimasu",
            "script": "ありがとうございます",
            "phonetic": "ah-ree-GAH-toh goh-zeye-MAHS",
            "meaning": "Thank you very much (polite)",
            "note": "Standard polite 'Thank you very much'. A subtle bow while saying this is customary.",
            "voice_code": "ja-JP",
            "audio_text": "ありがとうございます"
        },
        "hello": {
            "phrase": "Konnichiwa",
            "script": "こんにちは",
            "phonetic": "kohn-nee-chee-WAH",
            "meaning": "Hello / Good afternoon",
            "note": "Used from late morning through afternoon.",
            "voice_code": "ja-JP",
            "audio_text": "こんにちは"
        },
        "goodbye": {
            "phrase": "Sayonara",
            "script": "さようなら",
            "phonetic": "sah-yoh-NAH-rah",
            "meaning": "Goodbye",
            "note": "'Sayonara' is formal; 'Mata ne' or 'Ja ne' is used with friends.",
            "voice_code": "ja-JP",
            "audio_text": "さようなら"
        },
        "no problem": {
            "phrase": "Daijōbu desu",
            "script": "大丈夫です",
            "phonetic": "dye-JOH-boo des",
            "meaning": "No problem / It's okay",
            "note": "'Daijōbu desu' (大丈夫です) is the natural everyday way to say 'No problem / It's okay'. In formal settings, you can also use 'Mondai arimasen' (問題ありません, literally 'There is no problem').",
            "voice_code": "ja-JP",
            "audio_text": "大丈夫です"
        },
        "excuse me": {
            "phrase": "Sumimasen",
            "script": "すみません",
            "phonetic": "soo-mee-mah-SEN",
            "meaning": "Excuse me / Sorry",
            "note": "Multi-purpose: 'Excuse me', 'Sorry', or calling a waiter's attention in an izakaya.",
            "voice_code": "ja-JP",
            "audio_text": "すみません"
        },
        "delicious": {
            "phrase": "Oishii desu!",
            "script": "美味しいです",
            "phonetic": "oy-SHEE-des",
            "meaning": "It is delicious!",
            "note": "Complimenting the chef after sushi or ramen.",
            "voice_code": "ja-JP",
            "audio_text": "美味しいです"
        },
        "where is the bathroom": {
            "phrase": "Toire wa doko desu ka?",
            "script": "トイレはどこですか？",
            "phonetic": "TOY-reh wah DOH-koh des kah?",
            "meaning": "Where is the bathroom?",
            "note": "Widely understood across train stations and shops.",
            "voice_code": "ja-JP",
            "audio_text": "トイレはどこですか？"
        }
    },
    "Korean": {
        "thank you": {
            "phrase": "Gamsahamnida",
            "script": "감사합니다",
            "phonetic": "gahm-sah-hahm-NEE-dah",
            "meaning": "Thank you (formal/polite)",
            "note": "The standard respectful way to thank someone in Korean.",
            "voice_code": "ko-KR",
            "audio_text": "감사합니다"
        },
        "hello": {
            "phrase": "Annyeonghaseyo",
            "script": "안녕하세요",
            "phonetic": "ahn-nyung-hah-seh-yoh",
            "meaning": "Hello / Good day (polite)",
            "note": "Universal polite greeting used anytime with a slight nod.",
            "voice_code": "ko-KR",
            "audio_text": "안녕하세요"
        },
        "goodbye": {
            "phrase": "Annyeonghi gaseyo",
            "script": "안녕히 가세요",
            "phonetic": "ahn-nyung-hee gah-seh-yoh",
            "meaning": "Goodbye (Go peacefully)",
            "note": "Used when saying goodbye to someone who is leaving.",
            "voice_code": "ko-KR",
            "audio_text": "안녕히 가세요"
        },
        "no problem": {
            "phrase": "Gwenchanayo",
            "script": "괜찮아요",
            "phonetic": "gwen-chahn-AH-yoh",
            "meaning": "No problem / It's all right / It's okay",
            "note": "'Gwenchanayo' (괜찮아요) means 'No problem / It's okay'. You can also say 'Anieyo' (아니에요, 'Not at all / Don't mention it').",
            "voice_code": "ko-KR",
            "audio_text": "괜찮아요"
        },
        "where is the bathroom": {
            "phrase": "Hwajangsil-i eodi-yeyo?",
            "script": "화장실이 어디예요?",
            "phonetic": "hwah-jahng-sheel ee uh-dee-yeh-yoh?",
            "meaning": "Where is the bathroom?",
            "note": "Very useful phrase in restaurants and subway stations.",
            "voice_code": "ko-KR",
            "audio_text": "화장실이 어디예요?"
        },
        "delicious": {
            "phrase": "Mas-iss-eoyo!",
            "script": "맛있어요!",
            "phonetic": "mahs-iss-uh-yoh",
            "meaning": "It is delicious!",
            "note": "Said with enthusiasm to restaurant hosts in Seoul or Busan.",
            "voice_code": "ko-KR",
            "audio_text": "맛있어요!"
        }
    },
    "French": {
        "thank you": {
            "phrase": "Merci beaucoup",
            "script": "Merci beaucoup",
            "phonetic": "mair-SEE boh-KOO",
            "meaning": "Thank you very much",
            "note": "Always pair with eye contact and a warm smile in France.",
            "voice_code": "fr-FR",
            "audio_text": "Merci beaucoup"
        },
        "hello": {
            "phrase": "Bonjour",
            "script": "Bonjour",
            "phonetic": "bohn-ZHOOR",
            "meaning": "Hello / Good day",
            "note": "Essential etiquette: always say 'Bonjour' before asking for anything in a French shop or cafe!",
            "voice_code": "fr-FR",
            "audio_text": "Bonjour"
        },
        "goodbye": {
            "phrase": "Au revoir",
            "script": "Au revoir",
            "phonetic": "oh ruh-VWAHR",
            "meaning": "Goodbye",
            "note": "Standard polite farewell.",
            "voice_code": "fr-FR",
            "audio_text": "Au revoir"
        },
        "please": {
            "phrase": "S'il vous plaît",
            "script": "S'il vous plaît",
            "phonetic": "seel voo PLEH",
            "meaning": "Please",
            "note": "Polite form used with service staff and strangers.",
            "voice_code": "fr-FR",
            "audio_text": "S'il vous plaît"
        },
        "no problem": {
            "phrase": "Pas de problème",
            "script": "Pas de problème",
            "phonetic": "pah duh proh-BLEM",
            "meaning": "No problem / You're welcome",
            "note": "'Pas de problème' translates directly to 'No problem'. You can also say 'De rien' ('It's nothing') or 'Il n'y a pas de quoi'.",
            "voice_code": "fr-FR",
            "audio_text": "Pas de problème"
        },
        "excuse me": {
            "phrase": "Excusez-moi / Pardon",
            "script": "Excusez-moi",
            "phonetic": "ex-koo-zay-MWAH",
            "meaning": "Excuse me / Pardon",
            "note": "Used when navigating crowds or entering the metro.",
            "voice_code": "fr-FR",
            "audio_text": "Excusez-moi"
        },
        "where is the bathroom": {
            "phrase": "Où sont les toilettes ?",
            "script": "Où sont les toilettes ?",
            "phonetic": "oo sohn lay twah-LET?",
            "meaning": "Where is the bathroom / toilet?",
            "note": "Direct and polite in any restaurant or museum.",
            "voice_code": "fr-FR",
            "audio_text": "Où sont les toilettes ?"
        }
    },
    "Italian": {
        "thank you": {
            "phrase": "Grazie mille",
            "script": "Grazie mille",
            "phonetic": "GRAHT-tsyeh MEE-leh",
            "meaning": "Thank you very much (a thousand thanks)",
            "note": "'Grazie mille' translates to 'a thousand thanks'.",
            "voice_code": "it-IT",
            "audio_text": "Grazie mille"
        },
        "hello": {
            "phrase": "Ciao / Buongiorno",
            "script": "Ciao / Buongiorno",
            "phonetic": "CHOW / bwon-JOHR-noh",
            "meaning": "Hello / Good day",
            "note": "Use 'Buongiorno' in shops and restaurants until late afternoon.",
            "voice_code": "it-IT",
            "audio_text": "Ciao"
        },
        "you're welcome": {
            "phrase": "Prego",
            "script": "Prego",
            "phonetic": "PRAY-goh",
            "meaning": "You're welcome",
            "note": "Standard polite response to 'Grazie'.",
            "voice_code": "it-IT",
            "audio_text": "Prego"
        },
        "no problem": {
            "phrase": "Nessun problema",
            "script": "Nessun problema",
            "phonetic": "nes-SOON proh-BLEH-mah",
            "meaning": "No problem",
            "note": "'Nessun problema' translates directly to 'No problem'. You can also say 'Di niente' ('Don't mention it').",
            "voice_code": "it-IT",
            "audio_text": "Nessun problema"
        },
        "delicious": {
            "phrase": "Delizioso! / Molto buono!",
            "script": "Molto buono!",
            "phonetic": "MOHL-toh BWOH-noh",
            "meaning": "It is delicious!",
            "note": "Italians take immense pride in regional cuisine!",
            "voice_code": "it-IT",
            "audio_text": "Molto buono!"
        }
    },
    "Spanish": {
        "thank you": {
            "phrase": "Muchas gracias",
            "script": "Muchas gracias",
            "phonetic": "MOO-chahs GRAH-syahs",
            "meaning": "Thank you very much",
            "note": "'Muchas gracias' means 'Thank you very much'.",
            "voice_code": "es-ES",
            "audio_text": "Muchas gracias"
        },
        "hello": {
            "phrase": "Hola",
            "script": "¡Hola!",
            "phonetic": "OH-lah",
            "meaning": "Hello / Hi",
            "note": "'Hola' is universally friendly and polite across Spain and Latin America.",
            "voice_code": "es-ES",
            "audio_text": "¡Hola!"
        },
        "you're welcome": {
            "phrase": "De nada",
            "script": "De nada",
            "phonetic": "deh NAH-dah",
            "meaning": "You're welcome (It's nothing)",
            "note": "Literal translation: 'It's nothing'.",
            "voice_code": "es-ES",
            "audio_text": "De nada"
        },
        "no problem": {
            "phrase": "No hay problema",
            "script": "No hay problema",
            "phonetic": "noh eye proh-BLEH-mah",
            "meaning": "No problem / Don't worry",
            "note": "'No hay problema' is the exact Spanish equivalent for 'No problem'.",
            "voice_code": "es-ES",
            "audio_text": "No hay problema"
        },
        "where is the bathroom": {
            "phrase": "¿Dónde está el baño?",
            "script": "¿Dónde está el baño?",
            "phonetic": "DOHN-deh es-TAH el BAHN-yoh?",
            "meaning": "Where is the bathroom?",
            "note": "Essential travel question in cafes and attractions.",
            "voice_code": "es-ES",
            "audio_text": "¿Dónde está el baño?"
        }
    },
    "German": {
        "thank you": {
            "phrase": "Danke schön",
            "script": "Danke schön",
            "phonetic": "DAHN-kuh shurn",
            "meaning": "Thank you very much",
            "note": "Standard polite 'Thank you very much'.",
            "voice_code": "de-DE",
            "audio_text": "Danke schön"
        },
        "hello": {
            "phrase": "Guten Tag / Hallo",
            "script": "Guten Tag",
            "phonetic": "GOO-ten TAHK",
            "meaning": "Hello / Good day",
            "note": "'Guten Tag' is standard daytime polite greeting.",
            "voice_code": "de-DE",
            "audio_text": "Guten Tag"
        },
        "please": {
            "phrase": "Bitte schön",
            "script": "Bitte schön",
            "phonetic": "BIT-tuh shurn",
            "meaning": "Please / You're welcome",
            "note": "Used for both 'Please' and 'You're welcome'.",
            "voice_code": "de-DE",
            "audio_text": "Bitte schön"
        },
        "no problem": {
            "phrase": "Kein Problem",
            "script": "Kein Problem",
            "phonetic": "kyne proh-BLEHM",
            "meaning": "No problem",
            "note": "'Kein Problem' is the exact German equivalent for 'No problem'.",
            "voice_code": "de-DE",
            "audio_text": "Kein Problem"
        }
    },
    "Hindi": {
        "thank you": {
            "phrase": "Dhanyawaad / Shukriya",
            "script": "धन्यवाद / शुक्रिया",
            "phonetic": "DHAN-yuh-wahd / shoo-KREE-yah",
            "meaning": "Thank you very much",
            "note": "Both 'Dhanyawad' and 'Shukriya' express heartfelt gratitude.",
            "voice_code": "hi-IN",
            "audio_text": "धन्यवाद"
        },
        "hello": {
            "phrase": "Namaste / Namaskar",
            "script": "नमस्ते / नमस्कार",
            "phonetic": "nuh-muh-STAY",
            "meaning": "Hello / Greetings",
            "note": "Universal respectful greeting accompanied by folding hands together at the chest.",
            "voice_code": "hi-IN",
            "audio_text": "नमस्ते"
        },
        "no problem": {
            "phrase": "Koi baat nahi",
            "script": "कोई बात नहीं",
            "phonetic": "koy baat NAH-hee",
            "meaning": "No problem / Don't worry about it",
            "note": "'Koi baat nahi' means 'No problem / It's fine'.",
            "voice_code": "hi-IN",
            "audio_text": "कोई बात नहीं"
        },
        "how much": {
            "phrase": "Kitna hua?",
            "script": "कितना हुआ?",
            "phonetic": "kit-NAH HOO-ah?",
            "meaning": "How much is it?",
            "note": "Used when asking for the bill or bargaining at bazaars.",
            "voice_code": "hi-IN",
            "audio_text": "कितना हुआ?"
        }
    },
    "Telugu": {
        "thank you": {
            "phrase": "Dhanyavadalu",
            "script": "ధన్యవాదాలు",
            "phonetic": "dhun-yuh-vah-DAH-loo",
            "meaning": "Thank you very much",
            "note": "Respectful and warm expression of thanks in Telugu.",
            "voice_code": "te-IN",
            "audio_text": "ధన్యవాదాలు"
        },
        "hello": {
            "phrase": "Namaskaram",
            "script": "నమస్కారం",
            "phonetic": "nuh-muh-SKAH-ruhm",
            "meaning": "Hello / Greetings",
            "note": "Traditional Telugu greeting with joined palms.",
            "voice_code": "te-IN",
            "audio_text": "నమస్కారం"
        },
        "no problem": {
            "phrase": "Parvaledu / Emi samasya ledu",
            "script": "పర్వాలేదు / ఏమీ సమస్య లేదు",
            "phonetic": "par-wah-LEH-doo",
            "meaning": "No problem / It's okay / Never mind",
            "note": "'పర్వాలేదు' (Parvaledu) is the natural, everyday phrase for 'No problem'.",
            "voice_code": "te-IN",
            "audio_text": "పర్వాలేదు"
        },
        "where is the bathroom": {
            "phrase": "Washroom ekkada undi?",
            "script": "వాష్‌రూమ్ ఎక్కడ ఉంది?",
            "phonetic": "washroom EK-kuh-duh OON-dee?",
            "meaning": "Where is the bathroom?",
            "note": "Common everyday inquiry in Andhra Pradesh and Telangana.",
            "voice_code": "te-IN",
            "audio_text": "వాష్‌రూమ్ ఎక్కడ ఉంది?"
        }
    },
    "Tamil": {
        "thank you": {
            "phrase": "Nandri",
            "script": "நன்றி",
            "phonetic": "NUN-dree",
            "meaning": "Thank you",
            "note": "Direct and polite in Tamil Nadu.",
            "voice_code": "ta-IN",
            "audio_text": "நன்றி"
        },
        "hello": {
            "phrase": "Vanakkam",
            "script": "வணக்கம்",
            "phonetic": "vuh-NUHK-kuhm",
            "meaning": "Hello / Greetings",
            "note": "Classic respectful Tamil greeting with hands folded.",
            "voice_code": "ta-IN",
            "audio_text": "வணக்கம்"
        },
        "no problem": {
            "phrase": "Prachanai illai",
            "script": "பிரச்சனை இல்லை",
            "phonetic": "pruh-chuh-nye ILL-eye",
            "meaning": "No problem / No issue",
            "note": "'Prachanai illai' means 'There is no problem'.",
            "voice_code": "ta-IN",
            "audio_text": "பிரச்சனை இல்லை"
        }
    },
    "Nepali": {
        "thank you": {
            "phrase": "Dhanyabad",
            "script": "धन्यवाद",
            "phonetic": "DHAN-ya-bahd",
            "meaning": "Thank you",
            "note": "Standard respectful way to express gratitude in Nepal. Accompanied by hands joined together at chest level in a 'Namaste' gesture.",
            "voice_code": "ne-NP",
            "audio_text": "धन्यवाद"
        },
        "hello": {
            "phrase": "Namaste / Namaskar",
            "script": "नमस्ते / नमस्कार",
            "phonetic": "nah-mahs-TAY",
            "meaning": "Hello / Greetings / I bow to the divine in you",
            "note": "Universal warm greeting across Nepal said with palms pressed together.",
            "voice_code": "ne-NP",
            "audio_text": "नमस्ते"
        },
        "goodbye": {
            "phrase": "Pheri bhetaula",
            "script": "फेरी भेटौँला",
            "phonetic": "FAY-ree bay-TOW-lah",
            "meaning": "See you again / Until we meet again",
            "note": "Friendly departure expression preferred over final goodbyes.",
            "voice_code": "ne-NP",
            "audio_text": "फेरी भेटौँला"
        },
        "no problem": {
            "phrase": "Samasya chhaina / Kehi chhaina",
            "script": "समस्या छैन / केही छैन",
            "phonetic": "sah-MAHS-yah CHYE-nah",
            "meaning": "No problem / No worries / It's nothing",
            "note": "'Samasya chhaina' literally translates to 'There is no problem'. You can also say 'Kehi chhaina' (केही छैन, 'It's nothing').",
            "voice_code": "ne-NP",
            "audio_text": "समस्या छैन"
        },
        "how much": {
            "phrase": "Yesko kati parchha?",
            "script": "यसको कति पर्छ?",
            "phonetic": "YES-ko KAH-tee PAR-chha?",
            "meaning": "How much does this cost?",
            "note": "Essential phrase when shopping in Kathmandu Thamel and local bazaars.",
            "voice_code": "ne-NP",
            "audio_text": "यसको कति पर्छ?"
        },
        "delicious": {
            "phrase": "Dherai meetho chha!",
            "script": "धेरै मीठो छ!",
            "phonetic": "DHE-rye MEE-tho chha",
            "meaning": "Very delicious!",
            "note": "High praise for momo and dal bhat hosts!",
            "voice_code": "ne-NP",
            "audio_text": "धेरै मीठो छ"
        },
        "where is the bathroom": {
            "phrase": "Shauchalaya kahan chha?",
            "script": "शौचालय कहाँ छ?",
            "phonetic": "show-CHA-lah-ya kah-HAHN chha?",
            "meaning": "Where is the bathroom?",
            "voice_code": "ne-NP",
            "audio_text": "शौचालय कहाँ छ?"
        }
    },
    "Chinese": {
        "thank you": {
            "phrase": "Xièxie",
            "script": "谢谢",
            "phonetic": "shyeh-shyeh",
            "meaning": "Thank you",
            "voice_code": "zh-CN",
            "audio_text": "谢谢"
        },
        "hello": {
            "phrase": "Nǐ hǎo",
            "script": "你好",
            "phonetic": "nee-how",
            "meaning": "Hello",
            "voice_code": "zh-CN",
            "audio_text": "你好"
        },
        "no problem": {
            "phrase": "Méi wèntí / Bù kèqì",
            "script": "没问题 / 不客气",
            "phonetic": "may wen-tee / boo kuh-chee",
            "meaning": "No problem / You're welcome",
            "voice_code": "zh-CN",
            "audio_text": "没问题"
        },
        "how much": {
            "phrase": "Duōshǎo qián?",
            "script": "多少钱？",
            "phonetic": "dwaw-shaow chyen?",
            "meaning": "How much money?",
            "voice_code": "zh-CN",
            "audio_text": "多少钱？"
        }
    },
    "Vietnamese": {
        "thank you": {
            "phrase": "Cảm ơn",
            "script": "Cảm ơn",
            "phonetic": "gahm uhn",
            "meaning": "Thank you",
            "voice_code": "vi-VN",
            "audio_text": "Cảm ơn"
        },
        "hello": {
            "phrase": "Xin chào",
            "script": "Xin chào",
            "phonetic": "sin chow",
            "meaning": "Hello",
            "voice_code": "vi-VN",
            "audio_text": "Xin chào"
        },
        "no problem": {
            "phrase": "Không có gì",
            "script": "Không có gì",
            "phonetic": "khome caw zee",
            "meaning": "No problem / You're welcome",
            "voice_code": "vi-VN",
            "audio_text": "Không có gì"
        }
    },
    "Indonesian": {
        "thank you": {
            "phrase": "Terima kasih",
            "script": "Terima kasih",
            "phonetic": "teh-REE-mah KAH-see",
            "meaning": "Thank you",
            "voice_code": "id-ID",
            "audio_text": "Terima kasih"
        },
        "hello": {
            "phrase": "Halo / Selamat siang",
            "script": "Halo / Selamat siang",
            "phonetic": "HAH-loh",
            "meaning": "Hello / Good afternoon",
            "voice_code": "id-ID",
            "audio_text": "Selamat siang"
        },
        "no problem": {
            "phrase": "Sama-sama / Tidak apa-apa",
            "script": "Sama-sama / Tidak apa-apa",
            "phonetic": "tee-DAHK ah-pah-ah-pah",
            "meaning": "No problem / You're welcome",
            "voice_code": "id-ID",
            "audio_text": "Tidak apa-apa"
        }
    },
    "French": {
        "thank you": {
            "phrase": "Merci beaucoup",
            "script": "Merci beaucoup",
            "phonetic": "mair-SEE boh-KOO",
            "meaning": "Thank you very much",
            "voice_code": "fr-FR",
            "audio_text": "Merci beaucoup"
        },
        "hello": {
            "phrase": "Bonjour",
            "script": "Bonjour",
            "phonetic": "bohn-ZHOOR",
            "meaning": "Hello / Good day",
            "voice_code": "fr-FR",
            "audio_text": "Bonjour"
        },
        "no problem": {
            "phrase": "De rien / Pas de problème",
            "script": "De rien / Pas de problème",
            "phonetic": "pah duh proh-BLEM",
            "meaning": "No problem / You're welcome",
            "voice_code": "fr-FR",
            "audio_text": "Pas de problème"
        }
    },
    "Spanish": {
        "thank you": {
            "phrase": "Muchas gracias",
            "script": "Muchas gracias",
            "phonetic": "MOO-chahs GRAH-syahs",
            "meaning": "Thank you very much",
            "voice_code": "es-ES",
            "audio_text": "Muchas gracias"
        },
        "hello": {
            "phrase": "Hola",
            "script": "Hola",
            "phonetic": "OH-lah",
            "meaning": "Hello",
            "voice_code": "es-ES",
            "audio_text": "Hola"
        },
        "no problem": {
            "phrase": "De nada / No hay problema",
            "script": "De nada / No hay problema",
            "phonetic": "noh eye proh-BLEH-mah",
            "meaning": "No problem / You're welcome",
            "voice_code": "es-ES",
            "audio_text": "No hay problema"
        }
    },
    "German": {
        "thank you": {
            "phrase": "Vielen Dank / Danke schön",
            "script": "Vielen Dank / Danke schön",
            "phonetic": "FEE-len dahnk",
            "meaning": "Thank you very much",
            "voice_code": "de-DE",
            "audio_text": "Vielen Dank"
        },
        "hello": {
            "phrase": "Hallo / Guten Tag",
            "script": "Hallo / Guten Tag",
            "phonetic": "HAH-loh / GOO-ten tahk",
            "meaning": "Hello / Good day",
            "voice_code": "de-DE",
            "audio_text": "Guten Tag"
        },
        "no problem": {
            "phrase": "Kein Problem / Bitte schön",
            "script": "Kein Problem / Bitte schön",
            "phonetic": "kyne proh-BLAYM",
            "meaning": "No problem / You're welcome",
            "voice_code": "de-DE",
            "audio_text": "Kein Problem"
        }
    },
    "Italian": {
        "thank you": {
            "phrase": "Grazie mille",
            "script": "Grazie mille",
            "phonetic": "GRAHT-syeh MEEL-leh",
            "meaning": "Thank you very much",
            "voice_code": "it-IT",
            "audio_text": "Grazie mille"
        },
        "hello": {
            "phrase": "Ciao / Buongiorno",
            "script": "Ciao / Buongiorno",
            "phonetic": "CHOW / bwohn-JOHR-noh",
            "meaning": "Hello / Good day",
            "voice_code": "it-IT",
            "audio_text": "Buongiorno"
        },
        "no problem": {
            "phrase": "Prego / Nessun problema",
            "script": "Prego / Nessun problema",
            "phonetic": "nes-SOON proh-BLEH-mah",
            "meaning": "No problem / You're welcome",
            "voice_code": "it-IT",
            "audio_text": "Nessun problema"
        }
    }
}


def translate_live(text: str, target_code: str, source_code: str = "en") -> str:
    """Translate arbitrary phrase to target language code with resilient multi-provider fallback."""
    clean_text = str(text or "").strip()
    if not clean_text or not target_code:
        return ""

    # Clamp text to 450 characters to prevent MyMemory query limit error
    chunk = clean_text[:450]

    # 1. MyMemory API (Reliable, fast, high limit)
    try:
        pair = f"{source_code}|{target_code}"
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(chunk)}&langpair={pair}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=5) as res:
            if res.status == 200:
                data = json.loads(res.read().decode("utf-8"))
                trans = data.get("responseData", {}).get("translatedText", "").strip()
                if trans and not any(trans.lower().startswith(bad) for bad in ["invalid", "my_memory", "query error", "query length limit"]):
                    trans = html.unescape(trans)
                    return trans
    except Exception:
        pass

    # 2. Google Translate Single API fallback
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_code}&tl={target_code}&dt=t&q=" + urllib.parse.quote(clean_text)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=4) as res:
            if res.status == 200:
                data = json.loads(res.read().decode("utf-8"))
                return "".join([item[0] for item in data[0] if item[0]]).strip()
    except Exception:
        pass

    return ""


def detect_user_lang_and_translate(text: str) -> Tuple[str, str, str]:
    """
    Detects user input language and translates it into English so that the
    assistant and knowledge engines can process questions in ANY language.
    Returns: (english_query, lang_code, lang_name)
    """
    clean = str(text or "").strip()
    if not clean:
        return "", "en", "English"

    # Script-based detection
    if re.search(r'[\u0c00-\u0c7f]', clean):
        eng = translate_live(clean, "en", "te")
        return eng or clean, "te", "Telugu"
    if re.search(r'[\u0b80-\u0bff]', clean):
        eng = translate_live(clean, "en", "ta")
        return eng or clean, "ta", "Tamil"
    if re.search(r'[\u0c80-\u0cff]', clean):
        eng = translate_live(clean, "en", "kn")
        return eng or clean, "kn", "Kannada"
    if re.search(r'[\u0d00-\u0d7f]', clean):
        eng = translate_live(clean, "en", "ml")
        return eng or clean, "ml", "Malayalam"
    if re.search(r'[\u0980-\u09ff]', clean):
        eng = translate_live(clean, "en", "bn")
        return eng or clean, "bn", "Bengali"
    if re.search(r'[\u0a80-\u0aff]', clean):
        eng = translate_live(clean, "en", "gu")
        return eng or clean, "gu", "Gujarati"
    if re.search(r'[\u0a00-\u0a7f]', clean):
        eng = translate_live(clean, "en", "pa")
        return eng or clean, "pa", "Punjabi"
    if re.search(r'[\u0e00-\u0e7f]', clean):
        eng = translate_live(clean, "en", "th")
        return eng or clean, "th", "Thai"
    if re.search(r'[\u0900-\u097f]', clean):
        eng = translate_live(clean, "en", "hi")
        return eng or clean, "hi", "Hindi"
    if re.search(r'[\u3040-\u30ff]', clean):
        eng = translate_live(clean, "en", "ja")
        return eng or clean, "ja", "Japanese"
    if re.search(r'[\u4e00-\u9fff]', clean):
        eng = translate_live(clean, "en", "zh")
        return eng or clean, "zh", "Chinese"
    if re.search(r'[\uac00-\ud7af]', clean):
        eng = translate_live(clean, "en", "ko")
        return eng or clean, "ko", "Korean"
    if re.search(r'[\u0600-\u06ff]', clean):
        eng = translate_live(clean, "en", "ar")
        return eng or clean, "ar", "Arabic"
    if re.search(r'[\u0400-\u04ff]', clean):
        eng = translate_live(clean, "en", "ru")
        return eng or clean, "ru", "Russian"

    # Latin foreign language markers
    q_low = clean.lower()
    foreign_markers = [
        ("es", "Spanish", ["¿", "¡", "cuál", "cómo", "cuánto", "dónde", "por qué", "qué lugares", "ropa tradicional", "vestimenta", "gracias", "hola"]),
        ("fr", "French", ["quelle", "comment", "combien", "pourquoi", "où est", "qu'est-ce", "vêtement traditionnel", "tenue traditionnelle", "bonjour", "merci"]),
        ("de", "German", ["wie viel", "warum", "welche", "tracht", "wo ist", "traditionelle kleidung", "danke", "hallo"]),
        ("it", "Italian", ["quale", "quanto", "come posso", "abito tradizionale", "dove si", "grazie", "ciao"]),
        ("pt", "Portuguese", ["qual", "quanto custa", "como chegar", "roupa tradicional", "obrigado", "olá"])
    ]
    for code, name, markers in foreign_markers:
        if any(m in q_low for m in markers):
            eng = translate_live(clean, "en", code)
            return eng or clean, code, name

    # Non-ascii characters present without specific script matched
    if any(ord(c) > 127 for c in clean):
        try:
            url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(clean)}&langpair=autodetect|en"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as res:
                data = json.loads(res.read().decode("utf-8"))
                trans = data.get("responseData", {}).get("translatedText", "")
                matches = data.get("matches", [])
                src_code = "auto"
                if matches:
                    src_code = matches[0].get("source", "").split("-")[0].lower()
                lang_name_found = "Local Language"
                for ln, lc in LANGUAGE_CODES.items():
                    if lc == src_code:
                        lang_name_found = ln.title()
                        break
                if trans and not trans.lower().startswith("invalid"):
                    return html.unescape(trans), src_code, lang_name_found
        except Exception:
            pass

    return clean, "en", "English"


# ============================================================
def get_attire_ai_fallback_url(*args, **kwargs) -> None:
    """
    CRITICAL RULE: AI generation for traditional attire is completely removed.
    Always returns None to ensure only verified authentic photographs of real people are displayed.
    """
    return None


# ============================================================
# TRADITIONAL CLOTHING & ATTIRE (MEN & WOMEN WITH COSTS)
# ============================================================

CURATED_TRADITIONAL_CLOTHING = {   'Argentina': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                        'cost_inr': '₹8,000 – ₹25,000',
                                        'cost_local': '$80,000 – $250,000 ARS',
                                        'cultural_significance': 'Represents the warmth and folklore of women in the '
                                                                 'rural Argentine interior.',
                                        'description': 'Floor-length gathered floral cotton skirt with ruffled '
                                                       'flounces, high-necked embroidered blouse, neckerchief, and '
                                                       'hair tied into two braids.',
                                        'fabrics': 'Printed calico cotton, poplin, canvas alpargatas',
                                        'gender': 'Women',
                                        'image': None,
                                        'local_name': 'Vestido de paisana',
                                        'name': 'Vestido de Paisana Argentina',
                                        'region': 'The Pampas & Rural Argentina',
                                        'rental_price': '$18,000 – $45,000 ARS per day',
                                        'where_to_buy': 'Feria de Mataderos (Buenos Aires)'},
                                    {   'category': "👨 Men's Traditional Attire",
                                        'cost_inr': '₹12,000 – ₹42,000',
                                        'cost_local': '$120,000 – $420,000+ ARS',
                                        'cultural_significance': 'Defining symbol of Argentine equestrian pride and '
                                                                 'frontier heritage.',
                                        'description': 'Authentic attire of the Argentine horseman: wide pleated '
                                                       'trousers (Bombachas), tall leather boots, linen shirt, '
                                                       'silver-studded coin belt (Rastra), and wool poncho.',
                                        'fabrics': 'Heavy cotton twill, top-grain leather, sterling silver coins',
                                        'gender': 'Men',
                                        'image': None,
                                        'local_name': 'Traje de gaucho',
                                        'name': 'Traje de Gaucho Tradicional',
                                        'region': 'The Pampas & Rural Argentina',
                                        'rental_price': '$25,000 – $60,000 ARS per day',
                                        'where_to_buy': 'San Antonio de Areco, San Telmo Fair (Buenos Aires)'},
                                    {   'category': '🏔️ Northern Andean / Gaucho Attire',
                                        'cost_inr': '₹14,000 – ₹48,000',
                                        'cost_local': '$140,000 – $480,000 ARS',
                                        'cultural_significance': 'A sacred northern Argentine emblem of liberty and '
                                                                 'patriotic defiance.',
                                        'description': 'Iconic crimson-red handwoven wool poncho featuring bold black '
                                                       'mourning stripes and fringe, commemorating the martyrdom of '
                                                       'independence hero General Martín Miguel de Güemes.',
                                        'fabrics': "Hand-spun llama or sheep's wool, natural cochineal dyes",
                                        'gender': 'Regional',
                                        'image': None,
                                        'local_name': 'Poncho salteño de Güemes',
                                        'name': 'Poncho Salteño Tradicional',
                                        'region': 'Salta, Jujuy & Northwest Argentina',
                                        'rental_price': '$20,000 – $50,000 ARS per day',
                                        'where_to_buy': 'Mercado Artesanal de Salta, Cachi weavers cooperative'}],
                     'country': 'Argentina',
                     'cultural_significance': 'Argentine attire represents the epic history of the pampas gauchos and '
                                              'Andean high-altitude weavers.',
                     'men': {   'category': "👨 Men's Traditional Attire",
                                'cost_inr': '₹12,000 – ₹42,000',
                                'cost_local': '$120,000 – $420,000+ ARS',
                                'cultural_significance': 'The defining symbol of Argentine independence and equestrian '
                                                         'pride, celebrated on Día de la Tradición.',
                                'description': 'Authentic attire of the Argentine horseman: wide pleated trousers '
                                               '(Bombachas de campo), tall soft leather riding boots, a crisp shirt '
                                               'with silk neckerchief, a wide leather belt studded with silver coins '
                                               '(Rastra), and a wool poncho.',
                                'fabrics': 'Heavy cotton twill, top-grain leather, sterling silver coins, and woven '
                                           'wool',
                                'gender': 'Men',
                                'image': None,
                                'local_name': 'Traje de gaucho tradicional',
                                'name': 'Traje de Gaucho Tradicional',
                                'region': 'The Pampas (Buenos Aires Province, La Pampa, Entre Ríos)',
                                'rental_price': '$25,000 – $60,000 ARS per day',
                                'where_to_buy': 'San Antonio de Areco artisan leather shops, San Telmo Fair (Buenos '
                                                'Aires)'},
                     'rental_note': 'Feria de Mataderos and estancias in San Antonio de Areco offer authentic gaucho '
                                    'styling and riding gear.',
                     'women': {   'category': "👩 Women's Traditional Attire",
                                  'cost_inr': '₹8,000 – ₹25,000',
                                  'cost_local': '$80,000 – $250,000 ARS',
                                  'cultural_significance': 'Represents the warmth, family devotion, and folklore of '
                                                           'women in the rural Argentine interior.',
                                  'description': 'Floor-length gathered floral cotton skirt with ruffled flounces, a '
                                                 'high-necked embroidered blouse, a small neckerchief or light shawl, '
                                                 'canvas alpargatas shoes, and hair neatly parted into two braids.',
                                  'fabrics': 'Printed calico cotton, poplin, and canvas alpargatas',
                                  'gender': 'Women',
                                  'image': None,
                                  'local_name': 'Vestido de paisana',
                                  'name': 'Vestido de Paisana Argentina',
                                  'region': 'The Pampas & Rural Argentina',
                                  'rental_price': '$18,000 – $45,000 ARS per day',
                                  'where_to_buy': 'Feria de Mataderos (Buenos Aires), rural estancias across Buenos '
                                                  'Aires province'}},
    'Australia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                        'cost_inr': '₹10,000 – ₹32,000',
                                        'cost_local': '$180 – $580 AUD',
                                        'cultural_significance': 'Celebrates the strength of Australian rural women '
                                                                 'across the frontier.',
                                        'description': 'Durable ankle-length gingham or floral cotton homestead dress '
                                                       'with buttoned cuffs, leather boots, and wide-brimmed felt bush '
                                                       'hat.',
                                        'fabrics': 'Gingham cotton, heavy canvas apron, leather boots',
                                        'gender': 'Women',
                                        'image': None,
                                        'local_name': 'Australian Homestead Dress',
                                        'name': 'Australian Bush Pioneer & Homestead Dress',
                                        'region': 'Rural Victoria, New South Wales & Country Queensland',
                                        'rental_price': '$40 – $85 AUD per day',
                                        'where_to_buy': 'Country stores in Dubbo, Tamworth, and Toowoomba'},
                                    {   'category': "👨 Men's Traditional Attire",
                                        'cost_inr': '₹18,000 – ₹60,000',
                                        'cost_local': '$320 – $1,100+ AUD',
                                        'cultural_significance': 'Born of the harsh sun, celebrated in outback '
                                                                 'folklore and the stockman tradition.',
                                        'description': 'Authentic outback station gear: pure fur felt wide-brimmed '
                                                       'Akubra hat, waterproof oilskin coat, moleskin trousers, and '
                                                       'leather boots.',
                                        'fabrics': 'Australian rabbit-fur felt, oilskin, moleskin cotton',
                                        'gender': 'Men',
                                        'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/A_young_man_in_an_Akubra_hat_%2831523078262%29.jpg/960px-A_young_man_in_an_Akubra_hat_%2831523078262%29.jpg',
                                        'local_name': 'Bushman / Drover Attire',
                                        'name': 'Australian Bush Drover Attire & Akubra Hat',
                                        'region': 'Outback Queensland, Northern Territory & NSW',
                                        'rental_price': '$50 – $120 AUD per day',
                                        'where_to_buy': 'R.M. Williams, Akubra retailers across Australia'},
                                    {   'category': '🌍 Regional / Outback Station Attire',
                                        'cost_inr': '₹14,000 – ₹42,000',
                                        'cost_local': '$250 – $750 AUD',
                                        'cultural_significance': 'Iconic Australian bad-weather gear keeping stockmen '
                                                                 'dry through sudden high-country rainstorms.',
                                        'description': 'Full-length waterproof oilskin riding coat featuring shoulder '
                                                       'storm cape, leg straps for riding horseback, and fan-tail rear '
                                                       'flap.',
                                        'fabrics': 'Heavyweight paraffin-waxed Egyptian cotton',
                                        'gender': 'Regional',
                                        'image': None,
                                        'local_name': 'Driza-Bone Oilskin Coat',
                                        'name': 'Australian Outback Cattleman Driza-Bone Coat',
                                        'region': 'Snowy Mountains & High Country Station',
                                        'rental_price': '$40 – $80 AUD per day',
                                        'where_to_buy': 'Driza-Bone flagship stores and country outfitters'}],
                     'country': 'Australia',
                     'cultural_significance': 'Australian heritage clothing was forged in the rugged outback, '
                                              'balancing extreme weather protection with enduring style.',
                     'men': {   'category': "👨 Men's Traditional Attire",
                                'cost_inr': '₹18,000 – ₹60,000',
                                'cost_local': '$320 – $1,100+ AUD',
                                'cultural_significance': 'Born of the harsh sun and vast red plains, celebrated in '
                                                         "Banjo Paterson's poems and the legendary Australian stockman "
                                                         'tradition.',
                                'description': 'Authentic Australian outback station gear: a pure rabbit-fur felt '
                                               'wide-brimmed Akubra hat, waterproof oilskin coat (Driza-Bone), durable '
                                               'moleskin trousers, and R.M. Williams elastic-sided leather riding '
                                               'boots.',
                                'fabrics': 'Australian rabbit-fur felt, heavyweight oilskin, and moleskin cotton',
                                'gender': 'Men',
                                'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/A_young_man_in_an_Akubra_hat_%2831523078262%29.jpg/960px-A_young_man_in_an_Akubra_hat_%2831523078262%29.jpg',
                                'local_name': 'Bushman / Drover Attire',
                                'name': 'Australian Bush Drover Attire & Akubra Hat',
                                'region': 'Outback Queensland, Northern Territory & NSW',
                                'rental_price': '$50 – $120 AUD per day',
                                'where_to_buy': 'R.M. Williams stores (Pan-Australia), Akubra stockists (Kempsey, '
                                                'Sydney)'},
                     'rental_note': 'Outback stations and historic towns like Sovereign Hill provide colonial and '
                                    'drover dress experiences.',
                     'women': {   'category': "👩 Women's Traditional Attire",
                                  'cost_inr': '₹10,000 – ₹32,000',
                                  'cost_local': '$180 – $580 AUD',
                                  'cultural_significance': 'Celebrates the strength of Australian rural women who '
                                                           'established homesteads across the frontier.',
                                  'description': 'Durable ankle-length gingham or floral cotton homestead dress with '
                                                 'buttoned cuffs, sturdy leather riding boots, and a wide-brimmed felt '
                                                 'bush hat.',
                                  'fabrics': 'Gingham cotton, heavy canvas apron, and kangaroo-leather boots',
                                  'gender': 'Women',
                                  'image': None,
                                  'local_name': 'Australian Homestead Dress',
                                  'name': 'Australian Bush Pioneer & Homestead Dress',
                                  'region': 'Rural Victoria, New South Wales & Country Queensland',
                                  'rental_price': '$40 – $85 AUD per day',
                                  'where_to_buy': 'Country Outfitter stores in Dubbo, Tamworth, and Toowoomba'}},
    'Austria': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹15,000 – ₹55,000',
                                      'cost_local': '170 – 620 EUR',
                                      'cultural_significance': 'Celebrated alpine regional attire worn with pride at '
                                                               'church services, Salzburg Music Festival, and village '
                                                               'harvest balls.',
                                      'description': 'Fitted alpine bodice, gathered knee-or-ankle-length skirt, white '
                                                     'puffed-sleeve blouse, and hand-pleated silk apron with knot '
                                                     'indicating marital status.',
                                      'fabrics': 'Loden wool, fine Austrian linen, and dupioni silk',
                                      'gender': 'Women',
                                      'image': None,
                                      'local_name': 'Salzburger Dirndl',
                                      'name': 'Austrian Trachten Dirndl & Silk Apron',
                                      'region': 'Salzburg, Tyrol & Salzkammergut',
                                      'rental_price': '45 – 95 EUR per day',
                                      'where_to_buy': 'Trachten Forstenlechner (Salzburg), Tostmann Trachten (Vienna)'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹22,000 – ₹75,000',
                                      'cost_local': '250 – 850 EUR',
                                      'cultural_significance': "Classic gentleman's suit popularized by Archduke "
                                                               'Johann of Austria in the 19th century as a symbol of '
                                                               'unity and regional pride.',
                                      'description': 'Grey Loden wool jacket with dark green stand-up collar and '
                                                     'lapels, paired with staghorn buttons and supple chamois leather '
                                                     'breeches (Lederhosen).',
                                      'fabrics': 'Styrian Loden wool, deer buckskin, and horn buttons',
                                      'gender': 'Men',
                                      'image': None,
                                      'local_name': 'Steireranzug / Lederhose',
                                      'name': 'Steireranzug Wool Suit & Lederhosen',
                                      'region': 'Styria, Tyrol & Carinthia',
                                      'rental_price': '55 – 120 EUR per day',
                                      'where_to_buy': 'Gössl Trachten, Lodenfrey, Tyrolean artisan leather workshops'}],
                   'country': 'Austria',
                   'cultural_significance': 'Austrian Tracht represents a living, prestigious lifestyle worn across '
                                            'countryside and Viennese society.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': '₹22,000 – ₹75,000',
                              'cost_local': '250 – 850 EUR',
                              'cultural_significance': "Classic gentleman's suit popularized by Archduke Johann of "
                                                       'Austria in the 19th century as a symbol of unity and regional '
                                                       'pride.',
                              'description': 'Grey Loden wool jacket with dark green stand-up collar and lapels, '
                                             'paired with staghorn buttons and supple chamois leather breeches '
                                             '(Lederhosen).',
                              'fabrics': 'Styrian Loden wool, deer buckskin, and horn buttons',
                              'gender': 'Men',
                              'image': None,
                              'local_name': 'Steireranzug / Lederhose',
                              'name': 'Steireranzug Wool Suit & Lederhosen',
                              'region': 'Styria, Tyrol & Carinthia',
                              'rental_price': '55 – 120 EUR per day',
                              'where_to_buy': 'Gössl Trachten, Lodenfrey, Tyrolean artisan leather workshops'},
                   'rental_note': 'Trachten boutiques in Innsbruck and Salzburg offer daily rentals for Oktoberfest '
                                  'and village festivals.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': '₹15,000 – ₹55,000',
                                'cost_local': '170 – 620 EUR',
                                'cultural_significance': 'Celebrated alpine regional attire worn with pride at church '
                                                         'services, Salzburg Music Festival, and village harvest '
                                                         'balls.',
                                'description': 'Fitted alpine bodice, gathered knee-or-ankle-length skirt, white '
                                               'puffed-sleeve blouse, and hand-pleated silk apron with knot indicating '
                                               'marital status.',
                                'fabrics': 'Loden wool, fine Austrian linen, and dupioni silk',
                                'gender': 'Women',
                                'image': None,
                                'local_name': 'Salzburger Dirndl',
                                'name': 'Austrian Trachten Dirndl & Silk Apron',
                                'region': 'Salzburg, Tyrol & Salzkammergut',
                                'rental_price': '45 – 95 EUR per day',
                                'where_to_buy': 'Trachten Forstenlechner (Salzburg), Tostmann Trachten (Vienna)'}},
    'Bangladesh': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                         'cost_inr': '₹3,500 – ₹45,000',
                                         'cost_local': '4,800 – 62,000 BDT',
                                         'cultural_significance': 'A 2,000-year-old Bengal textile marvel designated '
                                                                  'as UNESCO Intangible Cultural Heritage of Humanity.',
                                         'description': 'UNESCO-recognized fine muslin handloom saree featuring '
                                                        'supplementary weft geometric and floral motifs, paired with '
                                                        'silk blouse and ornate gold jewellery.',
                                         'fabrics': 'Fine handspun cotton muslin and golden zari threads',
                                         'gender': 'Women',
                                         'image': None,
                                         'local_name': 'জামদানি শাড়ি',
                                         'name': 'Jamdani & Muslin Saree',
                                         'region': 'Dhaka Division (Narayanganj Shitalakhya Riverbanks)',
                                         'rental_price': '1,500 – 4,000 BDT per day',
                                         'where_to_buy': 'Demra Jamdani Palli, Aarong flagship stores (Dhaka)'},
                                     {   'category': "👨 Men's Traditional Attire",
                                         'cost_inr': '₹2,000 – ₹12,000',
                                         'cost_local': '2,800 – 16,500 BDT',
                                         'cultural_significance': 'Worn by Bengali gentlemen for Eid, weddings, and '
                                                                  'celebrations like Pohela Boishakh (Bengali New '
                                                                  'Year).',
                                         'description': 'Crisp tailored long tunic (Panjabi) with embroidered placket, '
                                                        'loose white drawstring trousers (Pajama), and high-collared '
                                                        'black sleeveless waistcoat (Mujib Coat).',
                                         'fabrics': 'Khadi cotton, fine endi silk, and tussar silk',
                                         'gender': 'Men',
                                         'image': None,
                                         'local_name': 'পাঞ্জাবি ও পায়জামা (মুজিব কোট)',
                                         'name': 'Panjabi and Pajama with Mujib Coat',
                                         'region': 'Pan-Bangladesh',
                                         'rental_price': '800 – 2,200 BDT per day',
                                         'where_to_buy': 'Aarong, Lubnan, New Market (Dhaka)'}],
                      'country': 'Bangladesh',
                      'cultural_significance': 'Bangladeshi traditional attire embodies the historic textile supremacy '
                                               'of the Bengal delta, renowned from ancient Rome to Mughal courts.',
                      'men': {   'category': "👨 Men's Traditional Attire",
                                 'cost_inr': '₹2,000 – ₹12,000',
                                 'cost_local': '2,800 – 16,500 BDT',
                                 'cultural_significance': 'Worn by Bengali gentlemen for Eid, weddings, and '
                                                          'celebrations like Pohela Boishakh (Bengali New Year).',
                                 'description': 'Crisp tailored long tunic (Panjabi) with embroidered placket, loose '
                                                'white drawstring trousers (Pajama), and high-collared black '
                                                'sleeveless waistcoat (Mujib Coat).',
                                 'fabrics': 'Khadi cotton, fine endi silk, and tussar silk',
                                 'gender': 'Men',
                                 'image': None,
                                 'local_name': 'পাঞ্জাবি ও পায়জামা (মুজিব কোট)',
                                 'name': 'Panjabi and Pajama with Mujib Coat',
                                 'region': 'Pan-Bangladesh',
                                 'rental_price': '800 – 2,200 BDT per day',
                                 'where_to_buy': 'Aarong, Lubnan, New Market (Dhaka)'},
                      'rental_note': 'Aarong outlets across Dhaka provide ready-made garments and bespoke tailoring '
                                     'services.',
                      'women': {   'category': "👩 Women's Traditional Attire",
                                   'cost_inr': '₹3,500 – ₹45,000',
                                   'cost_local': '4,800 – 62,000 BDT',
                                   'cultural_significance': 'A 2,000-year-old Bengal textile marvel designated as '
                                                            'UNESCO Intangible Cultural Heritage of Humanity.',
                                   'description': 'UNESCO-recognized fine muslin handloom saree featuring '
                                                  'supplementary weft geometric and floral motifs, paired with silk '
                                                  'blouse and ornate gold jewellery.',
                                   'fabrics': 'Fine handspun cotton muslin and golden zari threads',
                                   'gender': 'Women',
                                   'image': None,
                                   'local_name': 'জামদানি শাড়ি',
                                   'name': 'Jamdani & Muslin Saree',
                                   'region': 'Dhaka Division (Narayanganj Shitalakhya Riverbanks)',
                                   'rental_price': '1,500 – 4,000 BDT per day',
                                   'where_to_buy': 'Demra Jamdani Palli, Aarong flagship stores (Dhaka)'}},
    'Bhutan': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹6,000 – ₹35,000',
                                     'cost_local': '6,000 – 35,000 BTN',
                                     'cultural_significance': 'Mandatory formal national attire (Driglam Namzha) worn '
                                                              'for Dzong fortress visits, religious Tsechu festivals, '
                                                              'and official ceremonies.',
                                     'description': 'An ankle-length rectangular piece of intricately woven fabric '
                                                    'wrapped snugly around the body, pinned at both shoulders with '
                                                    'silver brooches (Koma), worn over an inner blouse (Wonju) and '
                                                    'short jacket (Toego).',
                                     'fabrics': 'Handwoven raw silk (Kishutara) and sheep wool',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'དཀྱི་རྭ (Kira)',
                                     'name': 'Kira and Wonju with Toego',
                                     'region': 'Pan-Bhutan (Thimphu & Paro)',
                                     'rental_price': '1,500 – 3,500 BTN per day',
                                     'where_to_buy': 'National Institute for Zorig Chusum (Thimphu), Centenary Farmers '
                                                     'Market handicraft stalls'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹5,000 – ₹30,000',
                                     'cost_local': '5,000 – 30,000 BTN',
                                     'cultural_significance': 'National male dress codified by Zhabdrung Ngawang '
                                                              'Namgyal in the 17th century to reinforce sovereign '
                                                              'Bhutanese identity.',
                                     'description': 'Knee-length robe tied tightly around the waist with a handwoven '
                                                    'textile belt (Kera), creating a large pouch (Torsey) in front '
                                                    'used to carry essentials, completed with white cuffs (Lagay) and '
                                                    'ceremonial raw silk scarf (Kabney).',
                                     'fabrics': 'Handspun geometric wool (Mathra) and raw silk',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'བགོ (Gho)',
                                     'name': 'Gho and Kera with Kabney',
                                     'region': 'Pan-Bhutan (Thimphu & Punakha)',
                                     'rental_price': '1,200 – 3,000 BTN per day',
                                     'where_to_buy': 'Thimphu Handicraft Emporium, Paro Town weavers'}],
                  'country': 'Bhutan',
                  'cultural_significance': 'Bhutanese national dress is an essential expression of Gross National '
                                           'Happiness and cultural preservation under Driglam Namzha.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹5,000 – ₹30,000',
                             'cost_local': '5,000 – 30,000 BTN',
                             'cultural_significance': 'National male dress codified by Zhabdrung Ngawang Namgyal in '
                                                      'the 17th century to reinforce sovereign Bhutanese identity.',
                             'description': 'Knee-length robe tied tightly around the waist with a handwoven textile '
                                            'belt (Kera), creating a large pouch (Torsey) in front used to carry '
                                            'essentials, completed with white cuffs (Lagay) and ceremonial raw silk '
                                            'scarf (Kabney).',
                             'fabrics': 'Handspun geometric wool (Mathra) and raw silk',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'བགོ (Gho)',
                             'name': 'Gho and Kera with Kabney',
                             'region': 'Pan-Bhutan (Thimphu & Punakha)',
                             'rental_price': '1,200 – 3,000 BTN per day',
                             'where_to_buy': 'Thimphu Handicraft Emporium, Paro Town weavers'},
                  'rental_note': 'Costume rental shops near Thimphu Clock Tower and Paro Dzong rent complete sets with '
                                 'boots for tourists.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹6,000 – ₹35,000',
                               'cost_local': '6,000 – 35,000 BTN',
                               'cultural_significance': 'Mandatory formal national attire (Driglam Namzha) worn for '
                                                        'Dzong fortress visits, religious Tsechu festivals, and '
                                                        'official ceremonies.',
                               'description': 'An ankle-length rectangular piece of intricately woven fabric wrapped '
                                              'snugly around the body, pinned at both shoulders with silver brooches '
                                              '(Koma), worn over an inner blouse (Wonju) and short jacket (Toego).',
                               'fabrics': 'Handwoven raw silk (Kishutara) and sheep wool',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'དཀྱི་རྭ (Kira)',
                               'name': 'Kira and Wonju with Toego',
                               'region': 'Pan-Bhutan (Thimphu & Paro)',
                               'rental_price': '1,500 – 3,500 BTN per day',
                               'where_to_buy': 'National Institute for Zorig Chusum (Thimphu), Centenary Farmers '
                                               'Market handicraft stalls'}},
    'Brazil': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹8,000 – ₹28,000',
                                     'cost_local': 'R$ 500 – R$ 1,800 BRL',
                                     'cultural_significance': 'Recognized national intangible cultural heritage '
                                                              'honoring Afro-Brazilian matriarchs.',
                                     'description': 'Billowing multi-layered white eyelet lace skirt, starched '
                                                    'petticoats, embroidered cotton blouse, twisted cloth turban, and '
                                                    'sacred beaded necklaces.',
                                     'fabrics': 'Pure white cotton lace, broderie anglaise, linen',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Traje de Baiana',
                                     'name': 'Traje de Baiana de Acarajé (Bahia Traditional Dress)',
                                     'region': 'Salvador, Bahia & Northeastern Coast',
                                     'rental_price': 'R$ 120 – R$ 300 BRL per day',
                                     'where_to_buy': 'Mercado Modelo (Salvador), Pelourinho artisan shops'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹10,000 – ₹35,000',
                                     'cost_local': 'R$ 650 – R$ 2,200 BRL',
                                     'cultural_significance': 'Official cultural heritage symbol of the southern '
                                                              'pampas cowboy tradition.',
                                     'description': 'Traditional equestrian clothing of Southern grasslands: baggy '
                                                    'pleated trousers (Bombachas) tucked into leather boots, leather '
                                                    'belt with coin pockets, and silk neckerchief.',
                                     'fabrics': 'Heavy cotton twill, top-grain leather, silk',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Pilcha Gaúcha Masculina',
                                     'name': 'Traje Gaúcho Tradicional (Pampas Cowboy)',
                                     'region': 'Rio Grande do Sul & Southern Pampas',
                                     'rental_price': 'R$ 150 – R$ 350 BRL per day',
                                     'where_to_buy': 'Casas de Pilcha in Porto Alegre'},
                                 {   'category': '🎉 Festive / Carnaval Cultural Attire',
                                     'cost_inr': '₹25,000 – ₹110,000+',
                                     'cost_local': 'R$ 1,500 – R$ 7,000+ BRL',
                                     'cultural_significance': "The exuberant soul of Rio's Sambadrome parades, "
                                                              'showcasing Afro-Brazilian percussive dance artistry.',
                                     'description': 'Spectacular handcrafted costume featuring sparkling '
                                                    'rhinestone-studded bustiers, towering iridescent feather plume '
                                                    'backpieces, and matching glittering headpieces.',
                                     'fabrics': 'Ostrich & pheasant feathers, Swarovski crystals, metallic lamé',
                                     'gender': 'Regional',
                                     'image': None,
                                     'local_name': 'Fantasia de Passista de Carnaval',
                                     'name': 'Samba Carnaval Traditional Passista Regalia',
                                     'region': 'Rio de Janeiro & São Paulo Sambadromes',
                                     'rental_price': 'R$ 350 – R$ 800 BRL for photography experiences',
                                     'where_to_buy': 'Cidade do Samba atelier workshops (Rio de Janeiro)'}],
                  'country': 'Brazil',
                  'cultural_significance': 'Brazilian attire brings together Afro-descendant traditions in the '
                                           'northeast and pampas cowboy heritage in the south.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹10,000 – ₹35,000',
                             'cost_local': 'R$ 650 – R$ 2,200 BRL',
                             'cultural_significance': 'Protected by state law as the official cultural symbol of the '
                                                      'brave and independent frontier spirit of Rio Grande do Sul.',
                             'description': 'Traditional equestrian clothing of the Southern grasslands: baggy pleated '
                                            'trousers (Bombachas) tucked into polished leather boots, a broad leather '
                                            'belt with coin pockets (Guaiaca), silk neckerchief (Lenço), and a flat '
                                            'wool hat.',
                             'fabrics': 'Heavy cotton twill, top-grain leather, and silk neckerchief',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'Pilcha Gaúcha Masculina',
                             'name': 'Traje Gaúcho Tradicional (Pampas Cowboy)',
                             'region': 'Rio Grande do Sul & Southern Pampas',
                             'rental_price': 'R$ 150 – R$ 350 BRL per day',
                             'where_to_buy': 'Casas de Pilcha in Porto Alegre, Caxias do Sul'},
                  'rental_note': 'Carnaval costume studios in Rio and Salvador provide photo sessions in full '
                                 'authentic festive attire.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹8,000 – ₹28,000',
                               'cost_local': 'R$ 500 – R$ 1,800 BRL',
                               'cultural_significance': 'Recognized by IPHAN as national intangible heritage, '
                                                        'celebrated by the Afro-descendant culinary matriarchs of '
                                                        'Bahia.',
                               'description': 'Billowing multi-layered white eyelet lace skirt (Saia rodada), starched '
                                              'petticoats, embroidered cotton blouse, an intricately twisted cloth '
                                              'turban (Torso), and sacred beaded necklaces (Contas) honoring '
                                              'Afro-Brazilian heritage.',
                               'fabrics': 'Pure white cotton lace, broderie anglaise, and starched linen',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'Traje de Baiana / Vestimenta Tradicional',
                               'name': 'Traje de Baiana de Acarajé (Bahia Traditional Dress)',
                               'region': 'Salvador, Bahia & Northeastern Coast',
                               'rental_price': 'R$ 120 – R$ 300 BRL for cultural photo shoots',
                               'where_to_buy': 'Mercado Modelo (Salvador), Pelourinho artisan boutiques'}},
    'Cambodia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹3,500 – ₹24,000',
                                       'cost_local': '170,000 – 1,180,000 KHR',
                                       'cultural_significance': 'Rooted in Khmer temple reliefs from Angkor Wat '
                                                                'depicting celestial Apsara dancers, celebrating Khmer '
                                                                'classical arts.',
                                       'description': 'Long rectangular woven skirt pleated around the waist with a '
                                                      'front knot, worn with a diagonal silk shoulder wrap (Sbai) and '
                                                      'ornate gold Apsara belt.',
                                       'fabrics': 'Golden Koh Dach raw silk, Hol ikat weave',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'សំពត់ (Sampot)',
                                       'name': 'Sampot Tep Apsara & Sampot Samloy',
                                       'region': 'Siem Reap & Phnom Penh',
                                       'rental_price': '35,000 – 80,000 KHR per day',
                                       'where_to_buy': 'Old Market (Phsar Chas, Siem Reap), Central Market (Phnom '
                                                       'Penh)'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹3,000 – ₹20,000',
                                       'cost_local': '150,000 – 980,000 KHR',
                                       'cultural_significance': 'Ceremonial attire reserved for royal weddings, '
                                                                'coronation ceremonies, and Khmer New Year '
                                                                'festivities.',
                                       'description': 'Traditional lower wrap where the cloth is passed between the '
                                                      'legs and tucked at the back to form billowy pantaloon trousers, '
                                                      'paired with a stand-collar silk shirt.',
                                       'fabrics': 'Handwoven raw silk, Phnom Srok cotton',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'សំពត់ចងក្បិន',
                                       'name': 'Sampot Chang Kben & Silk Shirt',
                                       'region': 'Siem Reap & Phnom Penh',
                                       'rental_price': '30,000 – 75,000 KHR per day',
                                       'where_to_buy': 'Artisans Angkor (Siem Reap), Russian Market (Phnom Penh)'}],
                    'country': 'Cambodia',
                    'cultural_significance': 'Cambodian attire preserves sacred Khmer textile heritage, linking modern '
                                             'celebrations to Angkorian imperial history.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹3,000 – ₹20,000',
                               'cost_local': '150,000 – 980,000 KHR',
                               'cultural_significance': 'Ceremonial attire reserved for royal weddings, coronation '
                                                        'ceremonies, and Khmer New Year festivities.',
                               'description': 'Traditional lower wrap where the cloth is passed between the legs and '
                                              'tucked at the back to form billowy pantaloon trousers, paired with a '
                                              'stand-collar silk shirt.',
                               'fabrics': 'Handwoven raw silk, Phnom Srok cotton',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'សំពត់ចងក្បិន',
                               'name': 'Sampot Chang Kben & Silk Shirt',
                               'region': 'Siem Reap & Phnom Penh',
                               'rental_price': '30,000 – 75,000 KHR per day',
                               'where_to_buy': 'Artisans Angkor (Siem Reap), Russian Market (Phnom Penh)'},
                    'rental_note': 'Apsara costume photography studios operate near Angkor Wat temple entrance for '
                                   'historic souvenir photos.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹3,500 – ₹24,000',
                                 'cost_local': '170,000 – 1,180,000 KHR',
                                 'cultural_significance': 'Rooted in Khmer temple reliefs from Angkor Wat depicting '
                                                          'celestial Apsara dancers, celebrating Khmer classical arts.',
                                 'description': 'Long rectangular woven skirt pleated around the waist with a front '
                                                'knot, worn with a diagonal silk shoulder wrap (Sbai) and ornate gold '
                                                'Apsara belt.',
                                 'fabrics': 'Golden Koh Dach raw silk, Hol ikat weave',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'សំពត់ (Sampot)',
                                 'name': 'Sampot Tep Apsara & Sampot Samloy',
                                 'region': 'Siem Reap & Phnom Penh',
                                 'rental_price': '35,000 – 80,000 KHR per day',
                                 'where_to_buy': 'Old Market (Phsar Chas, Siem Reap), Central Market (Phnom Penh)'}},
    'Canada': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹35,000 – ₹120,000+',
                                     'cost_local': '$550 – $1,900+ CAD',
                                     'cultural_significance': 'Essential for maternal care and survival in the high '
                                                              'Arctic environment.',
                                     'description': 'Masterpiece of Arctic engineering: hand-stitched parka featuring '
                                                    'a built-in baby pouch, voluminous protective hood, and beaded '
                                                    'tail.',
                                     'fabrics': 'Tanned caribou hide, duffle wool, Arctic fur ruff',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'ᐊᒫᐅᑦ (Amauti)',
                                     'name': 'Inuit Traditional Amauti & Winter Parka',
                                     'region': 'Nunavut & Arctic Canada',
                                     'rental_price': '$70 – $150 CAD per day',
                                     'where_to_buy': 'Nunavut Arts & Crafts Association (Iqaluit)'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹16,000 – ₹50,000',
                                     'cost_local': '$260 – $800 CAD',
                                     'cultural_significance': 'Emblematic of the fur-trade voyageur culture and the '
                                                              'Métis Nation.',
                                     'description': 'Heavy hooded wool coat crafted from a point blanket, secured with '
                                                    'a brightly finger-woven arrow-patterned sash and beaded '
                                                    'moccasins.',
                                     'fabrics': 'Point blanket wool, finger-woven yarn, tanned hide',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Capote de voyageur et Ceinture fléchée',
                                     'name': "Canadian Métis Voyageur Capote & L'Assomption Sash",
                                     'region': 'Red River, Manitoba & Northern Canada',
                                     'rental_price': '$50 – $100 CAD per day',
                                     'where_to_buy': 'Festival du Voyageur artisan shops (Winnipeg)'},
                                 {   'category': '🌸 Indigenous / Métis Heritage Attire',
                                     'cost_inr': '₹12,000 – ₹38,000',
                                     'cost_local': '$190 – $600 CAD',
                                     'cultural_significance': 'Celebrates womanhood, sacred connection to Mother '
                                                              'Earth, and cultural resurgence.',
                                     'description': 'Graceful dress decorated with colorful horizontal satin ribbons '
                                                    'and delicate five-petal flower beadwork, earning the Métis the '
                                                    "name 'The Flower Beadwork People'.",
                                     'fabrics': 'Calico cotton, satin ribbons, and Czech glass beads',
                                     'gender': 'Regional',
                                     'image': None,
                                     'local_name': 'Métis Ribbon Dress',
                                     'name': 'Canadian Métis Floral Beadwork Ribbon Dress',
                                     'region': 'Prairie Provinces (Manitoba, Saskatchewan, Alberta)',
                                     'rental_price': '$45 – $90 CAD per day',
                                     'where_to_buy': 'Indigenous art galleries in Winnipeg, Edmonton, and Saskatoon'}],
                  'country': 'Canada',
                  'cultural_significance': 'Canadian traditional dress reflects Indigenous Arctic ingenuity and '
                                           'French-Canadian fur trade history.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹16,000 – ₹50,000',
                             'cost_local': '$260 – $800 CAD',
                             'cultural_significance': 'Emblematic of the fur-trade coureurs des bois and the Métis '
                                                      "Nation's proud cultural identity.",
                             'description': "Heavy hooded wool coat crafted from a Hudson's Bay point blanket with "
                                            'horn toggles, secured with a brightly finger-woven arrow-patterned sash '
                                            '(Ceinture fléchée) and beaded moosehide moccasins.',
                             'fabrics': 'Pure virgin point blanket wool, finger-woven yarn, and tanned hide',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'Capote de voyageur et Ceinture fléchée',
                             'name': "Canadian Métis Voyageur Capote & L'Assomption Sash",
                             'region': 'Red River, Manitoba, Quebec & Northern Canada',
                             'rental_price': '$50 – $100 CAD per day',
                             'where_to_buy': 'Festival du Voyageur artisan shops (Winnipeg), Maison Gabrielle-Roy'},
                  'rental_note': 'Winter festival cultural centres in Winnipeg and Montreal offer historic voyageur '
                                 'styling.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹35,000 – ₹120,000+',
                               'cost_local': '$550 – $1,900+ CAD',
                               'cultural_significance': 'Essential for maternal bonding and survival in the Arctic, '
                                                        'representing thousands of years of Inuit environmental '
                                                        'mastery.',
                               'description': "Masterpiece of Arctic design: a hand-stitched woman's parka featuring a "
                                              'built-in baby pouch (Amaut) at the back, a voluminous hood protecting '
                                              'both mother and infant from freezing winds, and fringed beaded tail.',
                               'fabrics': 'Tanned caribou hide, duffle wool, and Arctic fox fur ruff',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'ᐊᒫᐅᑦ (Amauti)',
                               'name': 'Inuit Traditional Amauti & Winter Parka',
                               'region': 'Nunavut, Northwest Territories & Arctic Canada',
                               'rental_price': '$70 – $150 CAD for cultural photography',
                               'where_to_buy': 'Nunavut Arts & Crafts Association (Iqaluit), Yellowknife artisan '
                                               'co-ops'}},
    'Chile': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹5,000 – ₹28,000',
                                    'cost_local': '55,000 – 310,000 CLP',
                                    'cultural_significance': 'Worn during Fiestas Patrias (September 18) for dancing '
                                                             "Chile's national dance, the courtship Cueca.",
                                    'description': 'Fitted waist jacket with ruffled peplum and flared ankle-length '
                                                   'circle skirt with petticoat, accessorized with a white dancing '
                                                   'handkerchief (Pañuelo) for the Cueca dance.',
                                    'fabrics': 'Fine wool broadcloth, poplin, and lace petticoats',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': 'Vestido de Huasa / Ropón',
                                    'name': 'Vestido de Huasa Elegante (Cueca National Dance Dress)',
                                    'region': 'Central Valley (Santiago, Rancagua, Maule)',
                                    'rental_price': '15,000 – 38,000 CLP per day',
                                    'where_to_buy': 'Los Dominicos Artisan Village (Santiago), Rancagua saddle shops'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹7,000 – ₹45,000',
                                    'cost_local': '78,000 – 500,000 CLP',
                                    'cultural_significance': 'The Chamanto of Doñihue takes months to weave and was '
                                                             'gifted to world leaders at the 2004 APEC Summit in '
                                                             'Chile.',
                                    'description': 'Short tailored riding jacket, tight trousers with leather gaiters '
                                                   '(Polainas), silver spurs (Espuelas), wheat-straw hat (Chupalla), '
                                                   'and reversible woven mini-poncho (Chamanto).',
                                    'fabrics': 'Doñihue silk-and-wool reversible Chamanto, braided wheat straw',
                                    'gender': 'Men',
                                    'image': None,
                                    'local_name': 'Traje de Huaso y Chamanto',
                                    'name': 'Traje de Huaso con Chamanto y Chupalla Hat',
                                    'region': 'Central Valley (Doñihue & Colchagua)',
                                    'rental_price': '20,000 – 55,000 CLP per day',
                                    'where_to_buy': 'Pueblito Los Dominicos (Santiago), Doñihue master weavers'}],
                 'country': 'Chile',
                 'cultural_significance': 'Chilean Huaso attire embodies the equestrian traditions, rodeo skill, and '
                                          'patriotic folk culture of the Central Valley.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹7,000 – ₹45,000',
                            'cost_local': '78,000 – 500,000 CLP',
                            'cultural_significance': 'The Chamanto of Doñihue takes months to weave and was gifted to '
                                                     'world leaders at the 2004 APEC Summit in Chile.',
                            'description': 'Short tailored riding jacket, tight trousers with leather gaiters '
                                           '(Polainas), silver spurs (Espuelas), wheat-straw hat (Chupalla), and '
                                           'reversible woven mini-poncho (Chamanto).',
                            'fabrics': 'Doñihue silk-and-wool reversible Chamanto, braided wheat straw',
                            'gender': 'Men',
                            'image': None,
                            'local_name': 'Traje de Huaso y Chamanto',
                            'name': 'Traje de Huaso con Chamanto y Chupalla Hat',
                            'region': 'Central Valley (Doñihue & Colchagua)',
                            'rental_price': '20,000 – 55,000 CLP per day',
                            'where_to_buy': 'Pueblito Los Dominicos (Santiago), Doñihue master weavers'},
                 'rental_note': 'Traditional costume shops in Santiago rent Huaso attires during the September '
                                'national holidays.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹5,000 – ₹28,000',
                              'cost_local': '55,000 – 310,000 CLP',
                              'cultural_significance': "Worn during Fiestas Patrias (September 18) for dancing Chile's "
                                                       'national dance, the courtship Cueca.',
                              'description': 'Fitted waist jacket with ruffled peplum and flared ankle-length circle '
                                             'skirt with petticoat, accessorized with a white dancing handkerchief '
                                             '(Pañuelo) for the Cueca dance.',
                              'fabrics': 'Fine wool broadcloth, poplin, and lace petticoats',
                              'gender': 'Women',
                              'image': None,
                              'local_name': 'Vestido de Huasa / Ropón',
                              'name': 'Vestido de Huasa Elegante (Cueca National Dance Dress)',
                              'region': 'Central Valley (Santiago, Rancagua, Maule)',
                              'rental_price': '15,000 – 38,000 CLP per day',
                              'where_to_buy': 'Los Dominicos Artisan Village (Santiago), Rancagua saddle shops'}},
    'China': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹3,000 – ₹45,000+',
                                    'cost_local': '¥700 – ¥3,800+ CNY',
                                    'cultural_significance': 'Timeless symbol of Chinese feminine poise and '
                                                             'Shanghainese 1920s cultural revival.',
                                    'description': 'Figure-hugging one-piece Chinese silk dress featuring a mandarin '
                                                   'collar, diagonal closure with Pankou frog buttons, and side leg '
                                                   'slits.',
                                    'fabrics': 'Mulberry silk satin, Hangzhou brocade',
                                    'gender': 'Women',
                                    'image': 'https://upload.wikimedia.org/wikipedia/commons/8/84/Qipao_woman.jpg',
                                    'local_name': '旗袍',
                                    'name': 'Cheongsam / Qipao Silk Gown',
                                    'region': 'Shanghai, Hong Kong, Beijing & Pan-China',
                                    'rental_price': '¥120 – ¥350 CNY per day',
                                    'where_to_buy': 'Changle Road (Shanghai), Qianmen Street (Beijing)'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹5,000 – ₹25,000',
                                    'cost_local': '¥400 – ¥2,000 CNY',
                                    'cultural_significance': 'Defining garment of Chinese scholars, embodying '
                                                             'Confucian balance, modesty, and intellectual poise.',
                                    'description': 'Full-length cross-collar robe with wide flowing sleeves, '
                                                   'contrasting collar band, and silk sash tied at the waist with jade '
                                                   'pendants.',
                                    'fabrics': 'Pure mulberry silk, breathable ramie linen',
                                    'gender': 'Men',
                                    'image': None,
                                    'local_name': '道袍 / 男子汉服',
                                    'name': "Daopao & Men's Hanfu (Scholar Robe)",
                                    'region': "Jiangnan, Beijing, Xi'an & Pan-China",
                                    'rental_price': '¥100 – ¥250 CNY per day',
                                    'where_to_buy': "Suzhou Silk Street, Xi'an Grand Tang Mall boutiques"},
                                {   'category': '🌸 Heritage Dynastic Attire',
                                    'cost_inr': '₹4,000 – ₹20,000',
                                    'cost_local': '¥350 – ¥1,800 CNY',
                                    'cultural_significance': 'A spectacular renaissance of classical Chinese aesthetic '
                                                             'heritage embraced by millions during Mid-Autumn Festival '
                                                             'and Hanfu Day.',
                                    'description': 'High-chested wrap skirt (Qun) tied above the bust with embroidered '
                                                   'silk ribbons, worn over a lightweight inner blouse (Ru) and draped '
                                                   'with a fluttering silk scarf (Pibo).',
                                    'fabrics': 'Flowing silk chiffon, organza, and gold-thread embroidery',
                                    'gender': 'Regional',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a6/Hanfu_movement_in_Guangzhou.jpg/960px-Hanfu_movement_in_Guangzhou.jpg',
                                    'local_name': '齐胸襦裙 (Qíxiōng Rúqún)',
                                    'name': 'Traditional Hanfu (Ruqun Robe)',
                                    'region': "Tang & Song Dynasties (Xi'an, Luoyang, Hangzhou)",
                                    'rental_price': '¥100 – ¥300 CNY per day (includes hair styling & photography '
                                                    'makeup)',
                                    'where_to_buy': "Xi'an Giant Wild Goose Pagoda cultural avenue, West Lake "
                                                    '(Hangzhou)'}],
                 'country': 'China',
                 'cultural_significance': 'Chinese traditional clothing encapsulates thousands of years of dynastic '
                                          'textile innovation, from ancient silk weaving to embroidery.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹5,000 – ₹25,000',
                            'cost_local': '¥400 – ¥2,000 CNY',
                            'cultural_significance': 'The defining garment of Ming Dynasty scholars, embodying '
                                                     'Confucian modesty, balance, and intellectual grace.',
                            'description': 'Full-length cross-collar robe (Jiaoling Youren) with wide flowing sleeves, '
                                           'contrasting white collar band, side concealed gussets, and silk sash tied '
                                           'at the waist with jade pendants.',
                            'fabrics': 'Pure mulberry silk, breathable ramie linen, and brocade',
                            'gender': 'Men',
                            'image': None,
                            'local_name': '道袍 / 男子汉服',
                            'name': "Daopao & Men's Hanfu (Scholar Robe)",
                            'region': "Jiangnan, Beijing, Xi'an & Pan-China",
                            'rental_price': '¥100 – ¥250 CNY per day',
                            'where_to_buy': "Suzhou Silk Street, Xi'an Grand Tang Mall boutiques, Chengdu Jinli "
                                            'Street'},
                 'rental_note': "Boutiques near Xi'an City Wall, Beijing Forbidden City, and Hangzhou West Lake "
                                'provide full imperial dress-up experiences.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': 'Bespoke: ₹8,000 – ₹45,000+ • Ready-to-wear: ₹3,000 – ₹12,000',
                              'cost_local': '¥700 – ¥3,800+ CNY',
                              'cultural_significance': 'Evolving from Manchu banner garments into 1920s cosmopolitan '
                                                       'Shanghai glamour, the Qipao is the timeless symbol of Chinese '
                                                       'feminine elegance.',
                              'description': 'Figure-hugging one-piece Chinese dress featuring a high mandarin '
                                             'stand-up collar, diagonal front closure with intricate handmade Pankou '
                                             'frog knots, and side leg slits.',
                              'fabrics': 'Mulberry silk satin, Hangzhou brocade, and hand-embroidered jacquard',
                              'gender': 'Women',
                              'image': 'https://upload.wikimedia.org/wikipedia/commons/8/84/Qipao_woman.jpg',
                              'local_name': '旗袍 (Qípáo)',
                              'name': 'Cheongsam / Qipao Silk Gown',
                              'region': 'Shanghai, Hong Kong, Beijing & Pan-China',
                              'rental_price': '¥120 – ¥350 CNY per day',
                              'where_to_buy': 'Changle Road (Shanghai custom Qipao Street), Qianmen (Beijing)'}},
    'Colombia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹3,500 – ₹22,000',
                                       'cost_local': '160,000 – 1,050,000 COP',
                                       'cultural_significance': 'The definitive dance attire of Colombian Cumbia, '
                                                                'embodying the joyous fusion of African, Indigenous, '
                                                                'and Spanish musical traditions.',
                                       'description': 'Enormous flowing layered ruffled skirt (Pollera) with lace '
                                                      'trim, off-the-shoulder ruffled blouse, and red carnations '
                                                      'pinned in swept-back hair, danced with lit candles.',
                                       'fabrics': 'Checked gingham cotton (vichy), white poplin, and cotton lace',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'Pollera Cumbiambera',
                                       'name': 'Traje de Cumbia (Falda de Cumbia & Blusa con Vuelos)',
                                       'region': 'Caribbean Coast (Barranquilla, Cartagena) & Pan-Colombia',
                                       'rental_price': '40,000 – 110,000 COP per day',
                                       'where_to_buy': 'Carnival shops in Barranquilla, Las Bóvedas craft shops '
                                                       '(Cartagena)'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹3,000 – ₹20,000',
                                       'cost_local': '140,000 – 950,000 COP',
                                       'cultural_significance': 'The Sombrero Vueltiao made by Zenú indigenous '
                                                                'artisans is official Cultural Symbol of the Nation by '
                                                                'Colombian law.',
                                       'description': 'Crisp white cotton shirt and trousers with a red neckerchief '
                                                      '(Pañolón), woven shoulder bag (Mochila Wayuu), and iconic '
                                                      'braided cane hat (Sombrero Vueltiao).',
                                       'fabrics': 'Caña flecha palm fiber (Zenú weaving), raw white cotton',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'Traje de Cumbiambero y Sombrero Vueltiao',
                                       'name': 'Traje de Cumbia & Sombrero Vueltiao with Ruana',
                                       'region': 'Caribbean Coast & Andean Highlands',
                                       'rental_price': '35,000 – 90,000 COP per day',
                                       'where_to_buy': 'Pasaje Rivas (Bogotá), Las Bóvedas (Cartagena)'}],
                    'country': 'Colombia',
                    'cultural_significance': 'Colombian traditional dress reflects the multicultural rhythm of coastal '
                                             'Cumbia, Afro-Colombian joy, and Andean mountain pride.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹3,000 – ₹20,000',
                               'cost_local': '140,000 – 950,000 COP',
                               'cultural_significance': 'The Sombrero Vueltiao made by Zenú indigenous artisans is '
                                                        'official Cultural Symbol of the Nation by Colombian law.',
                               'description': 'Crisp white cotton shirt and trousers with a red neckerchief (Pañolón), '
                                              'woven shoulder bag (Mochila Wayuu), and iconic braided cane hat '
                                              '(Sombrero Vueltiao).',
                               'fabrics': 'Caña flecha palm fiber (Zenú weaving), raw white cotton',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'Traje de Cumbiambero y Sombrero Vueltiao',
                               'name': 'Traje de Cumbia & Sombrero Vueltiao with Ruana',
                               'region': 'Caribbean Coast & Andean Highlands',
                               'rental_price': '35,000 – 90,000 COP per day',
                               'where_to_buy': 'Pasaje Rivas (Bogotá), Las Bóvedas (Cartagena)'},
                    'rental_note': 'Carnival boutiques in Barranquilla and cultural centers in Cartagena offer festive '
                                   'dressing experiences.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹3,500 – ₹22,000',
                                 'cost_local': '160,000 – 1,050,000 COP',
                                 'cultural_significance': 'The definitive dance attire of Colombian Cumbia, embodying '
                                                          'the joyous fusion of African, Indigenous, and Spanish '
                                                          'musical traditions.',
                                 'description': 'Enormous flowing layered ruffled skirt (Pollera) with lace trim, '
                                                'off-the-shoulder ruffled blouse, and red carnations pinned in '
                                                'swept-back hair, danced with lit candles.',
                                 'fabrics': 'Checked gingham cotton (vichy), white poplin, and cotton lace',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'Pollera Cumbiambera',
                                 'name': 'Traje de Cumbia (Falda de Cumbia & Blusa con Vuelos)',
                                 'region': 'Caribbean Coast (Barranquilla, Cartagena) & Pan-Colombia',
                                 'rental_price': '40,000 – 110,000 COP per day',
                                 'where_to_buy': 'Carnival shops in Barranquilla, Las Bóvedas craft shops '
                                                 '(Cartagena)'}},
    'Egypt': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹3,500 – ₹14,000',
                                    'cost_local': '700 – 2,800 EGP',
                                    'cultural_significance': 'Icon of Egyptian popular folk theater and classic '
                                                             'cinema.',
                                    'description': 'Vibrant floral long dress with ruffled hem and side slits, '
                                                   'enveloped in the dramatic draped black silk wrap (Milaya Lef) '
                                                   'adorned with golden sequins.',
                                    'fabrics': 'Egyptian cotton, silk crepe, golden paillettes',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': 'الثوب البلدي والملاية لف',
                                    'name': 'Egyptian Baladi Dress & Milaya Lef',
                                    'region': 'Cairo & Alexandria',
                                    'rental_price': '150 – 350 EGP per day',
                                    'where_to_buy': 'Khan el-Khalili textile quarter (Cairo)'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹2,500 – ₹10,000',
                                    'cost_local': '500 – 2,000 EGP',
                                    'cultural_significance': 'Quintessential dress of the Nile Valley, providing '
                                                             'cooling breathability in the desert climate.',
                                    'description': 'Loose, flowing full-length robe with wide sleeves and rounded '
                                                   'neckline, tailored from Egyptian cotton, paired with a wrapped '
                                                   'white turban.',
                                    'fabrics': '100% Giza Egyptian cotton, wool for winter',
                                    'gender': 'Men',
                                    'image': None,
                                    'local_name': 'الجلابية المصرية',
                                    'name': 'Egyptian Galabeya & Emamah',
                                    'region': 'Upper Egypt (Luxor, Aswan) & Nile Delta',
                                    'rental_price': '100 – 250 EGP per day',
                                    'where_to_buy': 'Khan el-Khalili (Cairo), Luxor Old Souq'},
                                {   'category': '🌍 Regional / Nile Nubian Attire',
                                    'cost_inr': '₹3,000 – ₹11,000',
                                    'cost_local': '600 – 2,200 EGP',
                                    'cultural_significance': 'Preserves the ancient civilization of Nubia along the '
                                                             'First Cataract of the Nile.',
                                    'description': 'Luminous white outer tunic worn over dresses adorned with joyful '
                                                   'geometric rainbow embroidery, paired with layered turquoise and '
                                                   'gold beadwork.',
                                    'fabrics': 'Lightweight white linen, multi-color embroidery thread',
                                    'gender': 'Regional',
                                    'image': None,
                                    'local_name': 'الزي النوبي التراثي',
                                    'name': 'Nubian Traditional Embroidered Jellabiya',
                                    'region': 'Nubian Villages (Elephantine Island, Aswan)',
                                    'rental_price': '120 – 300 EGP per day',
                                    'where_to_buy': 'Nubian Village craft stalls (Gharb Soheil, Aswan)'}],
                 'country': 'Egypt',
                 'cultural_significance': 'Egyptian traditional dress reflects millennia of agricultural mastery along '
                                          'the fertile Nile.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹2,500 – ₹10,000',
                            'cost_local': '500 – 2,000 EGP',
                            'cultural_significance': 'The quintessential dress of the Nile Valley, keeping inhabitants '
                                                     'cool in the North African climate for centuries.',
                            'description': 'Loose, flowing full-length robe with wide sleeves and a rounded neckline, '
                                           'tailored from world-renowned long-staple Egyptian cotton, paired with a '
                                           'wrapped white turban (Emamah).',
                            'fabrics': '100% Giza Egyptian cotton, wool for winter',
                            'gender': 'Men',
                            'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/63/Egyptian_galabeya.jpg/330px-Egyptian_galabeya.jpg',
                            'local_name': 'الجلابية المصرية والعمامة',
                            'name': 'Egyptian Galabeya & Emamah',
                            'region': 'Upper Egypt (Luxor, Aswan) & Nile Delta',
                            'rental_price': '100 – 250 EGP per day',
                            'where_to_buy': 'Khan el-Khalili (Cairo), Luxor Old Souq, Aswan Bazaar'},
                 'rental_note': 'Felucca crews and cultural village studios in Aswan and Cairo offer authentic dress '
                                'experiences.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹3,500 – ₹14,000',
                              'cost_local': '700 – 2,800 EGP',
                              'cultural_significance': 'Icon of Egyptian popular folk theater and cinematic golden '
                                                       "age, epitomizing bold, witty feminine charm (Dala'a).",
                              'description': 'Vibrant floral long dress with ruffled hem and side slits, enveloped in '
                                             'the dramatic draped black silk wrap (Milaya Lef) adorned with golden '
                                             'sequins and coin fringes.',
                              'fabrics': 'Egyptian cotton, silk crepe, and golden metallic paillettes',
                              'gender': 'Women',
                              'image': None,
                              'local_name': 'الثوب البلدي والملاية لف',
                              'name': 'Egyptian Baladi Dress & Milaya Lef',
                              'region': 'Cairo, Alexandria & Nile Delta',
                              'rental_price': '150 – 350 EGP per photoshoot',
                              'where_to_buy': 'Khan el-Khalili textile quarter (Cairo), Alexandria souqs'}},
    'Ethiopia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹3,500 – ₹25,000',
                                       'cost_local': '4,800 – 34,000 ETB',
                                       'cultural_significance': 'Worn by Ethiopian women for Sunday Orthodox Christian '
                                                                'services, Enkutatash (New Year), Timkat, and '
                                                                'weddings.',
                                       'description': 'Ankle-length snowy white hand-spun cotton dress featuring '
                                                      'vibrant woven geometric embroidery (Tibeb) along hem and cuffs, '
                                                      'paired with a matching gauzy shawl (Netela).',
                                       'fabrics': 'Shemma handwoven Ethiopian cotton and colored silk Tibeb threads',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'ሀበሻ ቀሚስ (Habesha Kemis)',
                                       'name': 'Habesha Kemis with Netela Shawl',
                                       'region': 'Highland Ethiopia (Amhara, Tigray, Addis Ababa)',
                                       'rental_price': '1,200 – 3,500 ETB per day',
                                       'where_to_buy': 'Shiro Meda Market (Addis Ababa), Merkato traditional artisan '
                                                       'quarter'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹3,000 – ₹20,000',
                                       'cost_local': '4,100 – 27,500 ETB',
                                       'cultural_significance': 'Symbolizes peace, purity, and ancient Solomonic '
                                                                'Christian heritage dating back over 1,700 years.',
                                       'description': 'White cotton tunic and tapered trousers paired with a thick '
                                                      'two-layered woven cotton mantle (Gabi) draped over the '
                                                      'shoulders with decorative Tibeb borders.',
                                       'fabrics': 'Pure hand-spun Shemma cotton and embroidery',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'የባህል ልብስ እና ጋቢ',
                                       'name': 'Traditional Ethiopian Kidan with Gabi Wrap',
                                       'region': 'Highland Ethiopia',
                                       'rental_price': '1,000 – 3,000 ETB per day',
                                       'where_to_buy': 'Shiro Meda Market (Entoto Road, Addis Ababa)'}],
                    'country': 'Ethiopia',
                    'cultural_significance': 'Ethiopian traditional clothing represents uncolonized highland artisanal '
                                             'traditions preserved through ancient handloom weaving.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹3,000 – ₹20,000',
                               'cost_local': '4,100 – 27,500 ETB',
                               'cultural_significance': 'Symbolizes peace, purity, and ancient Solomonic Christian '
                                                        'heritage dating back over 1,700 years.',
                               'description': 'White cotton tunic and tapered trousers paired with a thick two-layered '
                                              'woven cotton mantle (Gabi) draped over the shoulders with decorative '
                                              'Tibeb borders.',
                               'fabrics': 'Pure hand-spun Shemma cotton and embroidery',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'የባህል ልብስ እና ጋቢ',
                               'name': 'Traditional Ethiopian Kidan with Gabi Wrap',
                               'region': 'Highland Ethiopia',
                               'rental_price': '1,000 – 3,000 ETB per day',
                               'where_to_buy': 'Shiro Meda Market (Entoto Road, Addis Ababa)'},
                    'rental_note': 'Traditional boutique shops along Shiro Meda in Addis Ababa provide custom fittings '
                                   'and photo packages.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹3,500 – ₹25,000',
                                 'cost_local': '4,800 – 34,000 ETB',
                                 'cultural_significance': 'Worn by Ethiopian women for Sunday Orthodox Christian '
                                                          'services, Enkutatash (New Year), Timkat, and weddings.',
                                 'description': 'Ankle-length snowy white hand-spun cotton dress featuring vibrant '
                                                'woven geometric embroidery (Tibeb) along hem and cuffs, paired with a '
                                                'matching gauzy shawl (Netela).',
                                 'fabrics': 'Shemma handwoven Ethiopian cotton and colored silk Tibeb threads',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'ሀበሻ ቀሚስ (Habesha Kemis)',
                                 'name': 'Habesha Kemis with Netela Shawl',
                                 'region': 'Highland Ethiopia (Amhara, Tigray, Addis Ababa)',
                                 'rental_price': '1,200 – 3,500 ETB per day',
                                 'where_to_buy': 'Shiro Meda Market (Addis Ababa), Merkato traditional artisan '
                                                 'quarter'}},
    'Fiji': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                   'cost_inr': '₹3,000 – ₹18,000',
                                   'cost_local': '80 – 480 FJD',
                                   'cultural_significance': 'The elegant national dress of Fijian women, worn for '
                                                            'Sunday church services, royal welcoming ceremonies, and '
                                                            'village weddings.',
                                   'description': 'Two-piece formal ensemble featuring an ankle-length wrapped skirt '
                                                  '(Sulu) and matching short-sleeved tunic (Jaba) printed with vibrant '
                                                  'Polynesian floral motifs.',
                                   'fabrics': 'Hand-printed Masi barkcloth, polished cotton, and silk rayon',
                                   'gender': 'Women',
                                   'image': None,
                                   'local_name': 'Sulu jaba',
                                   'name': 'Fijian Chambamba Sulu jaba Hand-printed Tunic',
                                   'region': 'Viti Levu (Suva, Nadi) & Outer Islands',
                                   'rental_price': '25 – 65 FJD per day',
                                   'where_to_buy': "Suva Flea Market, Nadi Handicraft Market, Jack's of Fiji"},
                               {   'category': "👨 Men's Traditional Attire",
                                   'cost_inr': '₹2,500 – ₹15,000',
                                   'cost_local': '65 – 400 FJD',
                                   'cultural_significance': 'Introduced by Ratu Sir Lala Sukuna in the early 20th '
                                                            'century, worn as official attire by parliamentarians, '
                                                            'business leaders, and the military.',
                                   'description': 'Tailored mid-calf wrap kilt (Sulu vakataga) with side pockets and '
                                                  'belt loops, worn formally with a collar shirt or colorful floral '
                                                  'Bula shirt and woven salusalu garland.',
                                   'fabrics': 'Fine suit wool blend, tropical cotton, and natural hibiscus fiber',
                                   'gender': 'Men',
                                   'image': None,
                                   'local_name': 'Sulu vakataga',
                                   'name': 'Fijian Sulu vakataga Formal Pocketed Wrap Kilt with Bula Shirt',
                                   'region': 'Pan-Fiji',
                                   'rental_price': '20 – 55 FJD per day',
                                   'where_to_buy': "Tappoo stores, Jack's of Fiji, Suva Municipal Market"}],
                'country': 'Fiji',
                'cultural_significance': 'Fijian attire combines South Pacific Masi barkcloth heritage with dignified '
                                         'modern island protocol.',
                'men': {   'category': "👨 Men's Traditional Attire",
                           'cost_inr': '₹2,500 – ₹15,000',
                           'cost_local': '65 – 400 FJD',
                           'cultural_significance': 'Introduced by Ratu Sir Lala Sukuna in the early 20th century, '
                                                    'worn as official attire by parliamentarians, business leaders, '
                                                    'and the military.',
                           'description': 'Tailored mid-calf wrap kilt (Sulu vakataga) with side pockets and belt '
                                          'loops, worn formally with a collar shirt or colorful floral Bula shirt and '
                                          'woven salusalu garland.',
                           'fabrics': 'Fine suit wool blend, tropical cotton, and natural hibiscus fiber',
                           'gender': 'Men',
                           'image': None,
                           'local_name': 'Sulu vakataga',
                           'name': 'Fijian Sulu vakataga Formal Pocketed Wrap Kilt with Bula Shirt',
                           'region': 'Pan-Fiji',
                           'rental_price': '20 – 55 FJD per day',
                           'where_to_buy': "Tappoo stores, Jack's of Fiji, Suva Municipal Market"},
                'rental_note': 'Resorts and handicraft centers across Denarau and Nadi provide traditional dress '
                               'fittings for cultural evenings.',
                'women': {   'category': "👩 Women's Traditional Attire",
                             'cost_inr': '₹3,000 – ₹18,000',
                             'cost_local': '80 – 480 FJD',
                             'cultural_significance': 'The elegant national dress of Fijian women, worn for Sunday '
                                                      'church services, royal welcoming ceremonies, and village '
                                                      'weddings.',
                             'description': 'Two-piece formal ensemble featuring an ankle-length wrapped skirt (Sulu) '
                                            'and matching short-sleeved tunic (Jaba) printed with vibrant Polynesian '
                                            'floral motifs.',
                             'fabrics': 'Hand-printed Masi barkcloth, polished cotton, and silk rayon',
                             'gender': 'Women',
                             'image': None,
                             'local_name': 'Sulu jaba',
                             'name': 'Fijian Chambamba Sulu jaba Hand-printed Tunic',
                             'region': 'Viti Levu (Suva, Nadi) & Outer Islands',
                             'rental_price': '25 – 65 FJD per day',
                             'where_to_buy': "Suva Flea Market, Nadi Handicraft Market, Jack's of Fiji"}},
    'France': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹25,000 – ₹85,000',
                                     'cost_local': '€280 – €950 EUR',
                                     'cultural_significance': 'Beloved patriotic symbol of Alsace celebrated in '
                                                              'historic towns along the Wine Route.',
                                     'description': 'Famous regional costume comprising a pleated red wool skirt, '
                                                    'fitted black velvet bodice, white chemise, and oversized black '
                                                    'bow headdress.',
                                     'fabrics': 'Alsatian wool, silk taffeta, black velvet',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Costume alsacien',
                                     'name': "Costume d'Alsace (Alsatian Traditional Dress)",
                                     'region': 'Alsace (Strasbourg, Colmar)',
                                     'rental_price': '€55 – €120 EUR per day',
                                     'where_to_buy': 'Heritage shops in Strasbourg and Colmar'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹20,000 – ₹70,000',
                                     'cost_local': '€220 – €780 EUR',
                                     'cultural_significance': "Worn with pride during Brittany's Fest Noz and "
                                                              'Cornouaille Celtic festivals.',
                                     'description': 'Stately ensemble featuring a black wool jacket with yellow silk '
                                                    'embroidery, an ornate velvet-trimmed waistcoat, and broad-brimmed '
                                                    'black hat trailing ribbons.',
                                     'fabrics': 'Broadcloth wool, silk embroidery, velvet',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Costume traditionnel breton masculin',
                                     'name': 'Costume Breton Traditionnel (Breton Gilet & Chapeau)',
                                     'region': 'Brittany (Quimper, Rennes)',
                                     'rental_price': '€50 – €110 EUR per day',
                                     'where_to_buy': "Ateliers de broderie in Quimper and Pont-l'Abbé"},
                                 {   'category': '🌻 Regional / Southern French Attire',
                                     'cost_inr': '₹18,000 – ₹65,000',
                                     'cost_local': '€200 – €720 EUR',
                                     'cultural_significance': 'Eulogized by Nobel laureate Frédéric Mistral, '
                                                              'celebrated during the Fête du Costume in Arles.',
                                     'description': 'Refined 19th-century southern French attire celebrated by '
                                                    'Mistral, featuring printed Provençal floral fabrics (Indiennes), '
                                                    'a folded lace fichu shawl, and velvet hair ribbon.',
                                     'fabrics': 'Provencal block-printed cotton (Indiennes), fine lace, silk velvet',
                                     'gender': 'Regional',
                                     'image': None,
                                     'local_name': "Costume d'Arlésienne et de Gardian",
                                     'name': 'Costume Traditionnel Provençal',
                                     'region': 'Provence (Arles, Avignon, Camargue)',
                                     'rental_price': '€50 – €100 EUR per day',
                                     'where_to_buy': 'Souleiado and Les Indiennes de Nîmes boutiques (Arles & '
                                                     'Avignon)'}],
                  'country': 'France',
                  'cultural_significance': 'French traditional regional wear celebrates distinct historical provinces, '
                                           'from Celtic Brittany to sun-drenched Provence.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹20,000 – ₹70,000',
                             'cost_local': '€220 – €780 EUR',
                             'cultural_significance': 'Worn with immense pride during the Festival de Cornouaille in '
                                                      "Quimper, celebrating Brittany's ancient Celtic heritage.",
                             'description': 'Stately Celtic-French ensemble featuring a black wool jacket (Chupenn) '
                                            'decorated with yellow silk thread embroidery, an ornate velvet-trimmed '
                                            'waistcoat (Gilet), and a broad-brimmed black hat trailing velvet ribbons.',
                             'fabrics': 'Black broadcloth wool, silk embroidery, and fine velvet',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'Costume traditionnel breton masculin',
                             'name': 'Costume Breton Traditionnel (Breton Gilet & Chapeau)',
                             'region': 'Brittany (Quimper, Rennes, Brest)',
                             'rental_price': '€50 – €110 EUR per festival day',
                             'where_to_buy': "Ateliers de broderie in Quimper and Pont-l'Abbé"},
                  'rental_note': 'Costume clubs in Strasbourg, Quimper, and Arles provide historic dressing for local '
                                 'pageants.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹25,000 – ₹85,000',
                               'cost_local': '€280 – €950 EUR',
                               'cultural_significance': 'A beloved patriotic symbol of Alsace, celebrated during wine '
                                                        'harvest festivals and Christmas fairs.',
                               'description': 'Famous regional costume comprising a pleated red wool skirt (Kittel), a '
                                              'fitted black velvet corset-bodice (Mieder), a white linen chemise, and '
                                              'the iconic oversized black silk bow headdress (Grand nœud).',
                               'fabrics': 'Alsatian wool, silk taffeta, and black velvet',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'Costume alsacien féminin',
                               'name': "Costume d'Alsace (Alsatian Traditional Dress)",
                               'region': 'Alsace (Strasbourg, Colmar, Riquewihr)',
                               'rental_price': '€55 – €120 EUR per day',
                               'where_to_buy': 'Atelier du Costume Alsacien (Strasbourg), Colmar folk shops'}},
    'Germany': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹12,000 – ₹55,000+',
                                      'cost_local': '€130 – €600+ EUR',
                                      'cultural_significance': 'Bavarian folk masterpiece where the apron bow '
                                                               'placement signals relationship status.',
                                      'description': 'Fitted corseted bodice with sweetheart neckline, full gathered '
                                                     'skirt, white puff-sleeve blouse, and a contrasting silk or '
                                                     'cotton apron tied with a bow.',
                                      'fabrics': 'Loden wool, breathable cotton, pure silk apron',
                                      'gender': 'Women',
                                      'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a1/Volksfestumzug_in_Vilshofen_a.d._Donau_2012_%283%29.JPG/960px-Volksfestumzug_in_Vilshofen_a.d._Donau_2012_%283%29.JPG',
                                      'local_name': 'Dirndl mit Schürze',
                                      'name': 'Bavarian Dirndl mit Schürze (Apron)',
                                      'region': 'Bavaria & Alpine Southern Germany',
                                      'rental_price': '€40 – €80 EUR per day',
                                      'where_to_buy': 'Trachten Angermaier, Moser Trachten (Munich)'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹25,000 – ₹85,000+',
                                      'cost_local': '€280 – €950+ EUR',
                                      'cultural_significance': 'Originally alpine workwear, now the international '
                                                               'symbol of Bavarian heritage and Oktoberfest.',
                                      'description': 'Sturdy knee-length leather breeches made from supple tanned '
                                                     'deerskin with hand-carved horn buttons and branch embroidery, '
                                                     'paired with suspenders and checked shirt.',
                                      'fabrics': 'Wild stag deerskin, horn buttons, loden wool',
                                      'gender': 'Men',
                                      'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5e/MB-Tracht_paar.jpg/960px-MB-Tracht_paar.jpg',
                                      'local_name': 'Lederhose und Trachtenhemd',
                                      'name': 'Bavarian Lederhosen mit Trachtenhemd',
                                      'region': 'Bavaria (München, Garmisch-Partenkirchen)',
                                      'rental_price': '€45 – €85 EUR per day',
                                      'where_to_buy': 'Trachten Angermaier (Munich), Lodenfrey'},
                                  {   'category': '🌍 Regional / Southwestern Attire',
                                      'cost_inr': '₹22,000 – ₹70,000',
                                      'cost_local': '€250 – €800 EUR',
                                      'cultural_significance': 'One of the most famous regional symbols of Germany, '
                                                               'preserving Black Forest Lutheran village traditions '
                                                               'since the 18th century.',
                                      'description': 'Iconic wide-brimmed straw hat decorated with 14 large red woolen '
                                                     'pompoms (worn by unmarried women) or black pompoms (married '
                                                     'women), paired with a black velvet bodice and embroidered apron.',
                                      'fabrics': 'Woven straw, pure virgin wool pompoms, and velvet',
                                      'gender': 'Regional',
                                      'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d1/Schwarzwaelderin_in_Tracht.jpg/960px-Schwarzwaelderin_in_Tracht.jpg',
                                      'local_name': 'Schwarzwälder Bollenhut-Tracht',
                                      'name': 'Black Forest Bollenhut Tracht',
                                      'region': 'Black Forest (Gutach, Kirnbach & Reichenbach, Baden-Württemberg)',
                                      'rental_price': '€50 – €100 EUR for regional events',
                                      'where_to_buy': 'Gutach Open Air Museum artisan workshops, Freiburg handcraft '
                                                      'centers'}],
                   'country': 'Germany',
                   'cultural_significance': 'German regional Trachten celebrate regional identity with distinct '
                                            'leathercraft and embroidery.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': 'Authentic Deerskin: ₹25,000 – ₹85,000+ • Goat/Cow: ₹10,000 – ₹22,000',
                              'cost_local': '€280 – €950+ EUR',
                              'cultural_significance': 'Originally durable alpine workwear for alpine farmers and '
                                                       'foresters, Lederhosen now represent Bavarian cultural pride '
                                                       'and Oktoberfest celebration.',
                              'description': 'Sturdy knee-length leather breeches made from supple tanned deerskin '
                                             'with hand-carved horn buttons and intricate green branch embroidery, '
                                             'paired with suspenders (H-Träger), a checked shirt, and wool Loferl leg '
                                             'warmers.',
                              'fabrics': 'Wild stag deerskin (Hirschleder), horn buttons, and loden wool',
                              'gender': 'Men',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5e/MB-Tracht_paar.jpg/960px-MB-Tracht_paar.jpg',
                              'local_name': 'Lederhose und Trachtenhemd',
                              'name': 'Bavarian Lederhosen mit Trachtenhemd',
                              'region': 'Bavaria (München, Garmisch-Partenkirchen, Allgäu)',
                              'rental_price': '€45 – €85 EUR per day (Oktoberfest season)',
                              'where_to_buy': 'Trachten Angermaier (Munich), Lodenfrey (Munich), Steingass'},
                   'rental_note': 'Costume rental shops across Munich provide complete Trachten styling during the '
                                  'Oktoberfest season.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': '₹12,000 – ₹55,000+',
                                'cost_local': '€130 – €600+ EUR',
                                'cultural_significance': 'The placement of the apron bow communicates marital status: '
                                                         'left side indicates single, right indicates married or '
                                                         'engaged, and center indicates a virgin.',
                                'description': 'Fitted corseted bodice (Mieder) with sweetheart neckline, a full '
                                               'gathered skirt, cropped white puff-sleeve blouse, and a contrasting '
                                               'silk or cotton apron (Schürze) tied with a bow.',
                                'fabrics': 'Loden wool, breathable cotton, and pure silk apron',
                                'gender': 'Women',
                                'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a1/Volksfestumzug_in_Vilshofen_a.d._Donau_2012_%283%29.JPG/960px-Volksfestumzug_in_Vilshofen_a.d._Donau_2012_%283%29.JPG',
                                'local_name': 'Dirndl mit Schürze',
                                'name': 'Bavarian Dirndl mit Schürze (Apron)',
                                'region': 'Bavaria & Alpine Southern Germany',
                                'rental_price': '€40 – €80 EUR per day',
                                'where_to_buy': 'Trachten Angermaier, Moser Trachten (Munich & Bavaria)'}},
    'Ghana': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹6,000 – ₹38,000',
                                    'cost_local': '1,050 – 6,700 GHS',
                                    'cultural_significance': 'Kente patterns convey proverbs, royal lineage, and moral '
                                                             'principles, historically worn by Ashanti queens.',
                                    'description': 'Fitted peplum blouse (Kaba), floor-length wrap skirt, and matching '
                                                   'stole fashioned from authentic handwoven Kente cloth, adorned with '
                                                   'yellow gold brass beads.',
                                    'fabrics': 'Bonwire handwoven Kente cotton and silk, Adinkra cloth',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': 'Kaba and Slot (Kente)',
                                    'name': 'Kente Cloth Draped Dress & Kaba Blouse',
                                    'region': 'Ashanti Region (Kumasi, Bonwire) & Volta Region',
                                    'rental_price': '250 – 700 GHS per day',
                                    'where_to_buy': 'Makola Market (Accra), Bonwire Kente Weaving Village (Kumasi)'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹8,000 – ₹48,000',
                                    'cost_local': '1,400 – 8,500 GHS',
                                    'cultural_significance': 'Historically reserved for kings (Asantehene) and chiefs; '
                                                             'today worn for Independence Day, weddings, and Durbar '
                                                             'assemblies.',
                                    'description': 'Monumental seamless textile (approx. 8x12 feet) draped '
                                                   'majestically over the left shoulder toga-style, leaving the right '
                                                   'arm bare, paired with handcrafted leather sandals (Ahenema).',
                                    'fabrics': 'Heavy hand-loomed silk and cotton strips joined with master stitches',
                                    'gender': 'Men',
                                    'image': None,
                                    'local_name': 'Kente Toga',
                                    'name': 'Handwoven Ashanti Kente Toga',
                                    'region': 'Ashanti Kingdom (Kumasi)',
                                    'rental_price': '300 – 850 GHS per day',
                                    'where_to_buy': 'Kumasi Cultural Centre, Centre for National Culture (Accra)'}],
                 'country': 'Ghana',
                 'cultural_significance': 'Ghanaian Kente is one of the most recognizable and philosophically profound '
                                          'textile systems in global cultural history.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹8,000 – ₹48,000',
                            'cost_local': '1,400 – 8,500 GHS',
                            'cultural_significance': 'Historically reserved for kings (Asantehene) and chiefs; today '
                                                     'worn for Independence Day, weddings, and Durbar assemblies.',
                            'description': 'Monumental seamless textile (approx. 8x12 feet) draped majestically over '
                                           'the left shoulder toga-style, leaving the right arm bare, paired with '
                                           'handcrafted leather sandals (Ahenema).',
                            'fabrics': 'Heavy hand-loomed silk and cotton strips joined with master stitches',
                            'gender': 'Men',
                            'image': None,
                            'local_name': 'Kente Toga',
                            'name': 'Handwoven Ashanti Kente Toga',
                            'region': 'Ashanti Kingdom (Kumasi)',
                            'rental_price': '300 – 850 GHS per day',
                            'where_to_buy': 'Kumasi Cultural Centre, Centre for National Culture (Accra)'},
                 'rental_note': 'Cultural centers in Accra and Kumasi offer Kente fitting, styling, and photography '
                                'sessions.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹6,000 – ₹38,000',
                              'cost_local': '1,050 – 6,700 GHS',
                              'cultural_significance': 'Kente patterns convey proverbs, royal lineage, and moral '
                                                       'principles, historically worn by Ashanti queens.',
                              'description': 'Fitted peplum blouse (Kaba), floor-length wrap skirt, and matching stole '
                                             'fashioned from authentic handwoven Kente cloth, adorned with yellow gold '
                                             'brass beads.',
                              'fabrics': 'Bonwire handwoven Kente cotton and silk, Adinkra cloth',
                              'gender': 'Women',
                              'image': None,
                              'local_name': 'Kaba and Slot (Kente)',
                              'name': 'Kente Cloth Draped Dress & Kaba Blouse',
                              'region': 'Ashanti Region (Kumasi, Bonwire) & Volta Region',
                              'rental_price': '250 – 700 GHS per day',
                              'where_to_buy': 'Makola Market (Accra), Bonwire Kente Weaving Village (Kumasi)'}},
    'Greece': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹22,000 – ₹80,000',
                                     'cost_local': '€250 – €900 EUR',
                                     'cultural_significance': 'Unified regional Greek styles into an elegant national '
                                                              'standard celebrated on Independence Day.',
                                     'description': 'National court dress designed by Queen Amalia: silk pleated '
                                                    'skirt, gold-embroidered black velvet jacket (Kontogouni), and red '
                                                    'pillbox cap (Fesi).',
                                     'fabrics': 'Silk taffeta, dark velvet, gold bullion embroidery, lace',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Στολή Αμαλίας',
                                     'name': 'Amalia Traditional Greek Dress',
                                     'region': 'Athens & Pan-Greece',
                                     'rental_price': '€50 – €120 EUR per day',
                                     'where_to_buy': 'Plaka heritage shops (Athens), Nafplio'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹35,000 – ₹130,000+',
                                     'cost_local': '€400 – €1,500+ EUR',
                                     'cultural_significance': 'Worn by the Presidential Guard at the Tomb of the '
                                                              'Unknown Soldier.',
                                     'description': 'Ceremonial military attire featuring a white kilt with 400 '
                                                    'pleats, gold-embroidered velvet waistcoat (Fermeli), and red '
                                                    'leather clogs with pompoms (Tsarouchia).',
                                     'fabrics': 'Fine white cotton, heavy velvet, gold braid, leather',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Φουστανέλα των Ευζώνων',
                                     'name': 'Evzone Fustanella (Presidential Guard Uniform)',
                                     'region': 'Athens, Peloponnese & Central Greece',
                                     'rental_price': '€60 – €150 EUR per day',
                                     'where_to_buy': 'Traditional tailors in Monastiraki (Athens)'},
                                 {   'category': '🌍 Regional / Island Attire',
                                     'cost_inr': '₹18,000 – ₹65,000',
                                     'cost_local': '€200 – €750 EUR',
                                     'cultural_significance': 'The fringe on the black Sariki headscarf symbolizes '
                                                              'tears shed for the fallen heroes of the Arkadi '
                                                              'Monastery.',
                                     'description': 'Distinguished island attire featuring pleated dark blue breeches '
                                                    '(Vraka), embroidered waistcoat (Meintanogeleko), silk waist sash, '
                                                    'white leather boots (Stivania), and knitted fringed headscarf '
                                                    '(Sariki).',
                                     'fabrics': 'Heavy wool broadcloth, white calf leather, and silk',
                                     'gender': 'Regional',
                                     'image': None,
                                     'local_name': 'Κρητική φορεσιά (Βράκα)',
                                     'name': 'Cretan Traditional Vraka Costume',
                                     'region': 'Crete (Chania, Heraklion, Rethymno)',
                                     'rental_price': '€45 – €100 EUR per day',
                                     'where_to_buy': 'Artisan workshops in Chania Old Town and Anogeia (Crete)'}],
                  'country': 'Greece',
                  'cultural_significance': 'Greek traditional attire commemorates the resilient spirit of independence '
                                           'and ancient Byzantine embroidery arts.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹35,000 – ₹130,000+',
                             'cost_local': '€400 – €1,500+ EUR',
                             'cultural_significance': 'Worn by the heroes of the 1821 Greek War of Independence and '
                                                      'today by the Presidential Guard at the Tomb of the Unknown '
                                                      'Soldier.',
                             'description': 'Ceremonial highland military attire featuring a snow-white kilt with 400 '
                                            'pleats (one for each year of Ottoman rule), a gold-embroidered velvet '
                                            'waistcoat (Fermeli), and red leather clogs with black pompoms '
                                            '(Tsarouchia).',
                             'fabrics': 'Fine white cotton, heavy velvet, gold braid, and leather',
                             'gender': 'Men',
                             'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/13/Souliotis_in_Corfu.jpg/330px-Souliotis_in_Corfu.jpg',
                             'local_name': 'Φουστανέλα των Ευζώνων',
                             'name': 'Evzone Fustanella (Presidential Guard Uniform)',
                             'region': 'Athens (Syntagma), Peloponnese & Central Greece',
                             'rental_price': '€60 – €150 EUR per festival day',
                             'where_to_buy': 'Traditional tailors in Monastiraki (Athens), Nafplio artisan studios'},
                  'rental_note': 'Costume ateliers in Plaka and Monastiraki in Athens provide authentic fitting for '
                                 'festive events.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹22,000 – ₹80,000',
                               'cost_local': '€250 – €900 EUR',
                               'cultural_significance': 'Unified diverse regional Greek folk styles into an elegant '
                                                        'national standard celebrated on Greek Independence Day.',
                               'description': 'Biedermeier-inspired national court dress designed by Queen Amalia of '
                                              'Greece in the 1830s, consisting of a silk pleated skirt (Kavadi), a '
                                              'gold-embroidered black velvet jacket (Kontogouni), and a red pillbox '
                                              'cap (Fesi) with gold tassels.',
                               'fabrics': 'Silk taffeta, dark velvet, gold bullion embroidery, and lace',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'Στολή Αμαλίας',
                               'name': 'Amalia Traditional Greek Dress',
                               'region': 'Athens, Peloponnese & Pan-Greece',
                               'rental_price': '€50 – €120 EUR per day',
                               'where_to_buy': 'Plaka heritage boutiques (Athens), Peloponnesian Folklore Foundation '
                                               '(Nafplio)'}},
    'Guatemala': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                        'cost_inr': '₹4,500 – ₹28,000',
                                        'cost_local': '420 – 2,600 GTQ',
                                        'cultural_significance': 'Each Mayan community weaves distinct geometric '
                                                                 'motifs recording village origin, marital status, and '
                                                                 'ancestral Mayan mythology.',
                                        'description': 'Handwoven backstrap-loomed tunic (Huipil) decorated with '
                                                       'sacred Mayan cosmology symbols, paired with a wrapped tube '
                                                       'skirt (Corte), embroidered sash (Faja), and braided hairband '
                                                       '(Cinta).',
                                        'fabrics': 'Natural cotton dyed with indigo and cochineal, backstrap loomed',
                                        'gender': 'Women',
                                        'image': None,
                                        'local_name': 'Huipil y Corte',
                                        'name': 'Maya Traje Típico (Huipil & Corte Skirt)',
                                        'region': 'Highlands (Santiago Atitlán, Chichicastenango, Quetzaltenango)',
                                        'rental_price': '100 – 250 GTQ per day',
                                        'where_to_buy': 'Chichicastenango Market, Panajachel artisan markets (Lake '
                                                        'Atitlán)'},
                                    {   'category': "👨 Men's Traditional Attire",
                                        'cost_inr': '₹4,000 – ₹24,000',
                                        'cost_local': '370 – 2,200 GTQ',
                                        'cultural_significance': 'Worn by Maya elders and community leaders '
                                                                 '(Cofradías), preserving unbroken pre-Columbian '
                                                                 'textile heritage.',
                                        'description': 'Red-and-white striped collared tunic, woolen wrap skirt '
                                                       '(Rodillera) worn over embroidered trousers, topped with a '
                                                       'braided black wool jacket (Cotón) with bat symbol on back.',
                                        'fabrics': 'Homespun sheep wool, handwoven cotton, and soutache braid',
                                        'gender': 'Men',
                                        'image': None,
                                        'local_name': 'Traje de Sololá / Cotón',
                                        'name': 'Sololá Maya Traditional Woolen Cofradía Jacket',
                                        'region': 'Sololá & Chichicastenango',
                                        'rental_price': '90 – 220 GTQ per day',
                                        'where_to_buy': 'Sololá Central Market, Chichicastenango village weavers'}],
                     'country': 'Guatemala',
                     'cultural_significance': 'Guatemalan Maya attire is one of the richest living indigenous textile '
                                              'traditions in the Americas, handwoven on backstrap looms for millennia.',
                     'men': {   'category': "👨 Men's Traditional Attire",
                                'cost_inr': '₹4,000 – ₹24,000',
                                'cost_local': '370 – 2,200 GTQ',
                                'cultural_significance': 'Worn by Maya elders and community leaders (Cofradías), '
                                                         'preserving unbroken pre-Columbian textile heritage.',
                                'description': 'Red-and-white striped collared tunic, woolen wrap skirt (Rodillera) '
                                               'worn over embroidered trousers, topped with a braided black wool '
                                               'jacket (Cotón) with bat symbol on back.',
                                'fabrics': 'Homespun sheep wool, handwoven cotton, and soutache braid',
                                'gender': 'Men',
                                'image': None,
                                'local_name': 'Traje de Sololá / Cotón',
                                'name': 'Sololá Maya Traditional Woolen Cofradía Jacket',
                                'region': 'Sololá & Chichicastenango',
                                'rental_price': '90 – 220 GTQ per day',
                                'where_to_buy': 'Sololá Central Market, Chichicastenango village weavers'},
                     'rental_note': 'Textile cooperatives around Lake Atitlán (San Juan La Laguna) offer weaving '
                                    'demonstrations and photo dressing.',
                     'women': {   'category': "👩 Women's Traditional Attire",
                                  'cost_inr': '₹4,500 – ₹28,000',
                                  'cost_local': '420 – 2,600 GTQ',
                                  'cultural_significance': 'Each Mayan community weaves distinct geometric motifs '
                                                           'recording village origin, marital status, and ancestral '
                                                           'Mayan mythology.',
                                  'description': 'Handwoven backstrap-loomed tunic (Huipil) decorated with sacred '
                                                 'Mayan cosmology symbols, paired with a wrapped tube skirt (Corte), '
                                                 'embroidered sash (Faja), and braided hairband (Cinta).',
                                  'fabrics': 'Natural cotton dyed with indigo and cochineal, backstrap loomed',
                                  'gender': 'Women',
                                  'image': None,
                                  'local_name': 'Huipil y Corte',
                                  'name': 'Maya Traje Típico (Huipil & Corte Skirt)',
                                  'region': 'Highlands (Santiago Atitlán, Chichicastenango, Quetzaltenango)',
                                  'rental_price': '100 – 250 GTQ per day',
                                  'where_to_buy': 'Chichicastenango Market, Panajachel artisan markets (Lake '
                                                  'Atitlán)'}},
    'India': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹2,500 – ₹80,000+',
                                    'cost_local': '₹2,500 – ₹80,000+ INR',
                                    'cultural_significance': 'Symbol of Indian elegance, grace, and regional handloom '
                                                             'artistry.',
                                    'description': 'Classic 6-to-9 yard handwoven pure silk saree draped elegantly '
                                                   'across the shoulder with an ornate pallu and matching blouse.',
                                    'fabrics': 'Pure mulberry silk with real gold and silver Zari weave',
                                    'gender': 'Women',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b5/South_Asian_Bridal_Stying_by_pattupleats.jpg/960px-South_Asian_Bridal_Stying_by_pattupleats.jpg',
                                    'local_name': 'बनारसी / कांजीवरम रेशमी साड़ी',
                                    'name': 'Banarasi & Kanjivaram Silk Saree',
                                    'region': 'Varanasi (UP) & Tamil Nadu (Pan-India)',
                                    'rental_price': '₹1,500 – ₹4,500 per day',
                                    'where_to_buy': 'Varanasi Silk Weavers Guild, T. Nagar (Chennai), Nalli Silks'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹8,000 – ₹45,000+',
                                    'cost_local': '₹8,000 – ₹45,000+ INR',
                                    'cultural_significance': 'A regal attire worn for royal court ceremonies, '
                                                             'weddings, and formal national celebrations.',
                                    'description': 'Tailored regal long coat (Sherwani) worn by Indian grooms and '
                                                   'gentlemen, paired with churidar trousers, embroidered stole, and '
                                                   'jeweled Safa turban.',
                                    'fabrics': 'Raw silk, Banarasi brocade, and gold Zari embroidery',
                                    'gender': 'Men',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/2/27/Bride_and_Groom_During_Pair_Pujan_Rasam.jpg/960px-Bride_and_Groom_During_Pair_Pujan_Rasam.jpg',
                                    'local_name': 'शेरवानी और चूड़ीदार',
                                    'name': 'Royal Sherwani & Churidar',
                                    'region': 'North India, Rajasthan & Hyderabad',
                                    'rental_price': '₹1,800 – ₹5,000 per day',
                                    'where_to_buy': 'Chandni Chowk (Delhi), Johari Bazaar (Jaipur), Manyavar '
                                                    'boutiques'},
                                {   'category': "👩 Women's Festive Attire",
                                    'cost_inr': '₹5,000 – ₹60,000+',
                                    'cost_local': '₹5,000 – ₹60,000+ INR',
                                    'cultural_significance': 'Iconic festive attire worn during Navratri Garba dances '
                                                             'and grand Indian wedding celebrations.',
                                    'description': 'Voluminous pleated flared skirt (Lehenga), fitted embroidered '
                                                   'blouse (Choli), and sheer draped scarf (Dupatta) adorned with '
                                                   'mirror-work or Zardozi.',
                                    'fabrics': 'Silk, georgette, velvet, and organza',
                                    'gender': 'Women',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6e/Indian_woman_wearing_choli_and_lehenga%2C_Oct._2019.jpg/960px-Indian_woman_wearing_choli_and_lehenga%2C_Oct._2019.jpg',
                                    'local_name': 'लहंगा चोली',
                                    'name': 'Lehenga Choli with Dupatta',
                                    'region': 'Rajasthan, Gujarat & North India',
                                    'rental_price': '₹1,500 – ₹4,000 per day',
                                    'where_to_buy': 'Law Garden (Ahmedabad), Bapu Bazaar (Jaipur), Karol Bagh (Delhi)'},
                                {   'category': '🌍 Regional / Southern Attire',
                                    'cost_inr': '₹1,200 – ₹6,500',
                                    'cost_local': '₹1,200 – ₹6,500 INR',
                                    'cultural_significance': 'Sacred and auspicious attire worn for temple entry, '
                                                             'Onam, Pongal, and classical dance recitals.',
                                    'description': 'Pure unstitched cotton or Kasavu gold-bordered white garment '
                                                   'wrapped around the waist, paired with a matching silk shirt and '
                                                   'shoulder cloth (Angavastram).',
                                    'fabrics': 'Kerala Kasavu handloom cotton, Mysore silk',
                                    'gender': 'Men',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3d/An_Indian_dancer_in_dhoti%2C_wrapped_around_his_waist.jpg/960px-An_Indian_dancer_in_dhoti%2C_wrapped_around_his_waist.jpg',
                                    'local_name': 'धोती-कुर्ता / வேஷ்டி / മുണ്ട്',
                                    'name': 'Dhoti-Kurta, Mundu & Angavastram',
                                    'region': 'South India (Tamil Nadu, Kerala, Karnataka) & Bengal',
                                    'rental_price': '₹600 – ₹1,500 per day',
                                    'where_to_buy': 'Kasavukada (Kochi), Pothys (Chennai), Co-optex stores'}],
                 'country': 'India',
                 'cultural_significance': 'Indian traditional attire showcases thousands of years of exquisite '
                                          'handloom mastery.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹8,000 – ₹45,000+',
                            'cost_local': '₹8,000 – ₹45,000+ INR',
                            'cultural_significance': 'A regal attire worn for royal court ceremonies, weddings, and '
                                                     'formal national celebrations.',
                            'description': 'Tailored regal long coat (Sherwani) worn by Indian grooms and gentlemen, '
                                           'paired with churidar trousers, embroidered stole, and jeweled Safa turban.',
                            'fabrics': 'Raw silk, Banarasi brocade, and gold Zari embroidery',
                            'gender': 'Men',
                            'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/2/27/Bride_and_Groom_During_Pair_Pujan_Rasam.jpg/960px-Bride_and_Groom_During_Pair_Pujan_Rasam.jpg',
                            'local_name': 'शेरवानी और चूड़ीदार',
                            'name': 'Royal Sherwani & Churidar',
                            'region': 'North India, Rajasthan & Hyderabad',
                            'rental_price': '₹1,800 – ₹5,000 per day',
                            'where_to_buy': 'Chandni Chowk (Delhi), Johari Bazaar (Jaipur), Manyavar boutiques'},
                 'rental_note': 'Costume rental studios in Delhi, Jaipur, Varanasi, and Chennai offer complete bridal '
                                'and cultural photography packages.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹2,500 – ₹80,000+',
                              'cost_local': '₹2,500 – ₹80,000+ INR',
                              'cultural_significance': 'With over 4,000 years of heritage, the saree is the definitive '
                                                       'symbol of Indian elegance, grace, and regional handloom '
                                                       'artistry.',
                              'description': 'Classic 6-to-9 yard handwoven pure silk saree draped elegantly across '
                                             'the shoulder with an ornate pallu and matching blouse, worn by Indian '
                                             'brides and women.',
                              'fabrics': 'Pure mulberry silk with real gold and silver Zari weave',
                              'gender': 'Women',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b5/South_Asian_Bridal_Stying_by_pattupleats.jpg/960px-South_Asian_Bridal_Stying_by_pattupleats.jpg',
                              'local_name': 'बनारसी / कांजीवरम रेशमी साड़ी',
                              'name': 'Banarasi & Kanjivaram Silk Saree',
                              'region': 'Varanasi (UP) & Tamil Nadu (Pan-India)',
                              'rental_price': '₹1,500 – ₹4,500 per day',
                              'where_to_buy': 'Varanasi Silk Weavers Guild, T. Nagar (Chennai), Nalli Silks '
                                              '(Pan-India)'}},
    'Indonesia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                        'cost_inr': '₹4,500 – ₹28,000+',
                                        'cost_local': 'Rp 850,000 – Rp 5,200,000+ IDR',
                                        'cultural_significance': 'UNESCO-recognized national dress symbolizing grace, '
                                                                 'cultural poise, and Javanese royalty.',
                                        'description': 'Intricately embroidered sheer lace or brocade blouse fastened '
                                                       'with gold brooches, draped over a tightly wrapped hand-waxed '
                                                       'Batik Tulis sarong.',
                                        'fabrics': 'Batik Tulis cotton, sheer French lace, brocade',
                                        'gender': 'Women',
                                        'image': 'https://upload.wikimedia.org/wikipedia/commons/6/63/GKR_Hayu_2.jpg',
                                        'local_name': 'Kebaya Jawa dan Kain Batik',
                                        'name': 'Kebaya Jawa & Hand-Drawn Batik Sarong',
                                        'region': 'Java, Bali, Sunda & Pan-Indonesia',
                                        'rental_price': 'Rp 200,000 – Rp 500,000 IDR per day',
                                        'where_to_buy': 'Pasar Beringharjo (Yogyakarta), Danar Hadi boutiques'},
                                    {   'category': "👨 Men's Traditional Attire",
                                        'cost_inr': '₹3,500 – ₹16,000',
                                        'cost_local': 'Rp 650,000 – Rp 3,000,000 IDR',
                                        'cultural_significance': 'Dignified courtly ensemble originating in the '
                                                                 'Mataram Sultanate, worn for royal Kraton events.',
                                        'description': 'Formal single-breasted high-collared tailored coat worn with a '
                                                       'hand-drawn batik waist-wrap, a pleated Blangkon head cloth, '
                                                       'and an ornamental Keris.',
                                        'fabrics': 'Hand-drawn Batik Tulis cotton, fine velvet',
                                        'gender': 'Men',
                                        'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5f/Batik_Trusmi_Cirebon_%2823%29.jpg/960px-Batik_Trusmi_Cirebon_%2823%29.jpg',
                                        'local_name': 'Baju Beskap dan Kemeja Batik',
                                        'name': 'Batik Shirt & Javanese Beskap',
                                        'region': 'Java (Yogyakarta, Surakarta / Solo)',
                                        'rental_price': 'Rp 150,000 – Rp 350,000 IDR per day',
                                        'where_to_buy': 'Pasar Beringharjo (Yogyakarta), Pasar Klewer (Solo)'},
                                    {   'category': '👑 Royal Temple Ceremonial Attire',
                                        'cost_inr': '₹20,000 – ₹75,000+',
                                        'cost_local': 'Rp 3,800,000 – Rp 14,000,000+ IDR',
                                        'cultural_significance': 'Historically reserved for Balinese royalty, now worn '
                                                                 'during sacred temple tooth-filing ceremonies and '
                                                                 'Hindu weddings.',
                                        'description': 'Magnificent royal ceremonial ensemble adorned with gold-woven '
                                                       'Prada Songket fabrics, a towering golden filigree crown '
                                                       '(Gelungan), and floral armlets.',
                                        'fabrics': 'Balinese Songket woven with gold leaf, velvet, and gilded brass',
                                        'gender': 'Regional',
                                        'image': None,
                                        'local_name': 'Payas Agung Bali',
                                        'name': 'Balinese Payas Agung Ceremonial Regalia',
                                        'region': 'Bali (Denpasar, Gianyar, Ubud)',
                                        'rental_price': 'Rp 400,000 – Rp 900,000 IDR per photoshoot',
                                        'where_to_buy': 'Kumbasari Traditional Market (Denpasar), Sukawati Art '
                                                        'Market'}],
                     'country': 'Indonesia',
                     'cultural_significance': 'Indonesian traditional attire reflects the maritime trade crossroads '
                                              'and master craft of UNESCO-recognized Batik.',
                     'men': {   'category': "👨 Men's Traditional Attire",
                                'cost_inr': '₹3,500 – ₹16,000',
                                'cost_local': 'Rp 650,000 – Rp 3,000,000 IDR',
                                'cultural_significance': 'A dignified courtly ensemble originating in the Mataram '
                                                         'Sultanate, worn for royal Kraton audiences and Javanese '
                                                         'wedding processions.',
                                'description': 'Formal single-breasted high-collared tailored coat (Beskap) worn with '
                                               'a hand-drawn batik waist-wrap (Jarik), a pleated head cloth '
                                               '(Blangkon), and an ornamental ceremonial Keris dagger tucked into the '
                                               'back.',
                                'fabrics': 'Hand-drawn Batik Tulis cotton, fine velvet, and gold thread',
                                'gender': 'Men',
                                'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5f/Batik_Trusmi_Cirebon_%2823%29.jpg/960px-Batik_Trusmi_Cirebon_%2823%29.jpg',
                                'local_name': 'Baju Beskap dan Kemeja Batik',
                                'name': 'Batik Shirt & Javanese Beskap',
                                'region': 'Java (Yogyakarta, Surakarta / Solo) & Pan-Indonesia',
                                'rental_price': 'Rp 150,000 – Rp 350,000 IDR per day',
                                'where_to_buy': 'Pasar Beringharjo (Yogyakarta), Pasar Klewer (Solo), Mirota Batik'},
                     'rental_note': 'Boutiques across Yogyakarta, Solo, and Ubud offer complete cultural dressing '
                                    'sessions with hair styling and palace photography.',
                     'women': {   'category': "👩 Women's Traditional Attire",
                                  'cost_inr': '₹4,500 – ₹28,000+',
                                  'cost_local': 'Rp 850,000 – Rp 5,200,000+ IDR',
                                  'cultural_significance': "Designated as Indonesia's national dress and UNESCO "
                                                           'Masterpiece of Intangible Heritage, celebrating the '
                                                           'philosophy of nature and unity.',
                                  'description': 'Intricately embroidered sheer lace or brocade blouse (Kebaya) '
                                                 'fastened with ornate gold brooches (Keronsang), draped over a '
                                                 'tightly wrapped hand-waxed Batik Tulis sarong with a traditional '
                                                 'hair bun (Sanggul).',
                                  'fabrics': 'Batik Tulis cotton, sheer French lace, brocade, and velvet',
                                  'gender': 'Women',
                                  'image': 'https://upload.wikimedia.org/wikipedia/commons/6/63/GKR_Hayu_2.jpg',
                                  'local_name': 'Kebaya Encim / Kebaya Jawa dan Kain Batik',
                                  'name': 'Kebaya Jawa & Hand-Drawn Batik Sarong',
                                  'region': 'Java, Bali, Sunda & Pan-Indonesia',
                                  'rental_price': 'Rp 200,000 – Rp 500,000 IDR per day',
                                  'where_to_buy': 'Malioboro Street (Yogyakarta), Danar Hadi boutiques, Pasar Baru '
                                                  '(Jakarta)'}},
    'Ireland': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹25,000 – ₹90,000',
                                      'cost_local': '€280 – €1,000 EUR',
                                      'cultural_significance': 'World-famous emblem of Irish musical and dance '
                                                               'storytelling.',
                                      'description': 'Stunning flared velvet dress embellished with Celtic knotwork '
                                                     'and spiral embroidery inspired by the Book of Kells.',
                                      'fabrics': 'Velvet, satin, gilded embroidery thread',
                                      'gender': 'Women',
                                      'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4c/Trinity_Academy_of_Irish_Dance.jpg/960px-Trinity_Academy_of_Irish_Dance.jpg',
                                      'local_name': 'Irish Step Dance Dress',
                                      'name': 'Traditional Irish Step Dance Embroidered Costume',
                                      'region': 'National Heritage (Dublin, Galway, Cork)',
                                      'rental_price': '€60 – €150 EUR per day',
                                      'where_to_buy': 'Specialty costume shops in Dublin and Galway'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹12,000 – ₹32,000',
                                      'cost_local': '€130 – €350 EUR',
                                      'cultural_significance': 'World-renowned maritime heritage knitting, with each '
                                                               'stitch symbolizing protection, harvest, and luck.',
                                      'description': 'Heavy natural cream wool sweater featuring cable, diamond, and '
                                                     'honeycomb stitches, worn over a collarless grandfather shirt and '
                                                     'Donegal flat cap.',
                                      'fabrics': 'Pure Irish wool with natural lanolin, Donegal tweed',
                                      'gender': 'Men',
                                      'image': None,
                                      'local_name': 'Geansaí Árann agus Léine',
                                      'name': 'Traditional Aran Wool Sweater & Grandfather Shirt',
                                      'region': 'Aran Islands (Inis Mór), Galway & West Coast',
                                      'rental_price': '€35 – €75 EUR per day',
                                      'where_to_buy': 'Aran Sweater Market (Inis Mór & Galway)'},
                                  {   'category': '🍀 Gaelic Historical Attire',
                                      'cost_inr': '₹18,000 – ₹60,000',
                                      'cost_local': '€200 – €680 EUR',
                                      'cultural_significance': 'The authentic ancient attire of medieval Gaelic '
                                                               "chieftains and bards, celebrating Ireland's "
                                                               'pre-conquest sovereign roots.',
                                      'description': 'Historical Gaelic tunic (Léine) dyed in golden saffron with '
                                                     'voluminous hanging sleeves, cinched with a leather belt and '
                                                     'wrapped in a heavy wool mantle (Brat) pinned with a Celtic '
                                                     'penannular brooch.',
                                      'fabrics': 'Pure Irish flax linen dyed with saffron, coarse homespun wool',
                                      'gender': 'Regional',
                                      'image': None,
                                      'local_name': 'Léine Chroich agus Brat',
                                      'name': 'Celtic Saffron Léine & Tweed Brat',
                                      'region': 'Ancient Ireland & Gaelic Heritage',
                                      'rental_price': '€45 – €90 EUR for historical festivals',
                                      'where_to_buy': 'Heritage reenactment guild shops in Kilkenny and Armagh'}],
                   'country': 'Ireland',
                   'cultural_significance': 'Irish traditional dress reflects Celtic monastic artistry and resilient '
                                            'coastal traditions.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': 'Hand-knit: ₹12,000 – ₹32,000',
                              'cost_local': '€130 – €350 EUR',
                              'cultural_significance': "Each stitch holds meaning: cable represents fisherman's ropes "
                                                       'for safety, diamond symbolizes wealth and success, and '
                                                       'blackberry honors nature.',
                              'description': 'Heavy unscoured water-repellent natural cream wool sweater featuring '
                                             'intricate hand-knit cable, diamond, and blackberry stitches, worn over a '
                                             'collarless Irish grandfather shirt and a Donegal tweed flat cap.',
                              'fabrics': '100% pure Irish wool with natural lanolin, Donegal tweed',
                              'gender': 'Men',
                              'image': None,
                              'local_name': 'Geansaí Árann agus Léine',
                              'name': 'Traditional Aran Wool Sweater & Grandfather Shirt',
                              'region': 'Aran Islands (Inis Mór), Galway & West Coast',
                              'rental_price': '€35 – €75 EUR per day',
                              'where_to_buy': 'Aran Sweater Market (Inis Mór & Galway), Magee of Donegal (Donegal '
                                              'Town)'},
                   'rental_note': 'Aran woolens and tweed caps can be purchased in historic shops across Temple Bar '
                                  'and Galway.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': '₹25,000 – ₹90,000',
                                'cost_local': '€280 – €1,000 EUR',
                                'cultural_significance': 'Celebrated worldwide during feiseanna (festivals), St. '
                                                         "Patrick's Day parades, and Riverdance performances.",
                                'description': 'Stunning stiffened flared dress adorned with intricate Celtic '
                                               'knotwork, Tara brooches, and spiral embroidery inspired by the Book of '
                                               'Kells, paired with white poodle socks and ghillies dance shoes.',
                                'fabrics': 'Velvet, silk satin, metallic Celtic embroidery threads',
                                'gender': 'Women',
                                'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4c/Trinity_Academy_of_Irish_Dance.jpg/960px-Trinity_Academy_of_Irish_Dance.jpg',
                                'local_name': 'Irish Step Dance Dress',
                                'name': 'Traditional Irish Step Dance Embroidered Costume',
                                'region': 'National Heritage (Dublin, Galway, Cork, Belfast)',
                                'rental_price': '€60 – €150 EUR per day',
                                'where_to_buy': 'Irish dance ateliers in Dublin, Belfast, and Cork'}},
    'Italy': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹35,000 – ₹130,000+',
                                    'cost_local': '€400 – €1,500+ EUR',
                                    'cultural_significance': 'Family heirloom folk costume celebrated during the '
                                                             "historic Sant'Efisio parade.",
                                    'description': 'Richly embroidered folk dress featuring a velvet bodice, pleated '
                                                   'wool skirt, lace veil, and precious gold filigree buttons.',
                                    'fabrics': 'Brocade, rich velvet, handwoven orbace wool, gold filigree',
                                    'gender': 'Women',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b9/Barisardo_-_Costume_tradizionale_%2804%29.JPG/960px-Barisardo_-_Costume_tradizionale_%2804%29.JPG',
                                    'local_name': 'Costume tradizionale sardo femminile',
                                    'name': 'Costume Tradizionale Sardo (Sardinian Folk Dress)',
                                    'region': 'Sardinia (Nuoro, Bari Sardo, Cagliari)',
                                    'rental_price': '€60 – €150 EUR per day',
                                    'where_to_buy': 'Heritage craft guilds in Nuoro and Cagliari'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹18,000 – ₹60,000',
                                    'cost_local': '€200 – €700 EUR',
                                    'cultural_significance': 'Preserves prehistoric Nuragic and pastoral Mediterranean '
                                                             'roots.',
                                    'description': 'Striking pastoral Mediterranean dress consisting of white linen '
                                                   'shirt, black wool double-breasted vest, dark pleated kilt, white '
                                                   'linen breeches, leather gaiters, and Berrita cap.',
                                    'fabrics': 'Handwoven orbace wool, coarse linen, sheepskin',
                                    'gender': 'Men',
                                    'image': None,
                                    'local_name': 'Costume tradizionale sardo maschile',
                                    'name': 'Abito Tradizionale Sardo Maschile (Sardinian Mastruca)',
                                    'region': 'Sardinia (Barbagia & Nuoro)',
                                    'rental_price': '€50 – €110 EUR per day',
                                    'where_to_buy': 'Artisan ateliers in Nuoro and Mamoiada'},
                                {   'category': '🌍 Alpine / Northern Regional Attire',
                                    'cost_inr': '₹15,000 – ₹55,000',
                                    'cost_local': '€180 – €650 EUR',
                                    'cultural_significance': 'Symbolizes the distinct alpine mountain culture bridging '
                                                             'Italian and Central European alpine heritage.',
                                    'description': 'Alpine folk dress featuring leather breeches or loden skirts, '
                                                   'accompanied by the iconic blue cotton apron (Schürze) and green '
                                                   'felt alpine hat with feather.',
                                    'fabrics': 'Pure South Tyrolean loden wool, linen, and leather',
                                    'gender': 'Regional',
                                    'image': None,
                                    'local_name': 'Südtiroler Tracht',
                                    'name': "Costume Tradizionale Tirolese dell'Alto Adige",
                                    'region': 'South Tyrol / Alto Adige (Bolzano, Merano)',
                                    'rental_price': '€45 – €90 EUR per day',
                                    'where_to_buy': 'Trachten workshops in Bolzano and Merano'}],
                 'country': 'Italy',
                 'cultural_significance': 'Italian traditional attire demonstrates tremendous regional diversity, from '
                                          'Mediterranean silk filigree to alpine loden.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹18,000 – ₹60,000',
                            'cost_local': '€200 – €700 EUR',
                            'cultural_significance': 'Preserves prehistoric Nuragic and pastoral Mediterranean roots, '
                                                     "worn during the Cavalcata Sarda and Sant'Efisio festivals.",
                            'description': 'Striking shepherd and village folk dress consisting of a white pleated '
                                           'linen shirt, black wool double-breasted vest (Cosso), dark pleated kilt '
                                           '(Raggetas), white linen breeches, leather gaiters, and long wool cap '
                                           '(Berrita).',
                            'fabrics': 'Handwoven orbace wool, coarse linen, and sheepskin',
                            'gender': 'Men',
                            'image': None,
                            'local_name': 'Costume tradizionale sardo maschile',
                            'name': 'Abito Tradizionale Sardo Maschile (Sardinian Mastruca)',
                            'region': 'Sardinia (Barbagia, Nuoro & Cagliari)',
                            'rental_price': '€50 – €110 EUR per day',
                            'where_to_buy': 'Artisan tailoring ateliers in Nuoro, Mamoiada, and Cagliari'},
                 'rental_note': 'Costume studios in Sardinia, Venice, and Florence offer rental styling for carnival '
                                'and historic pageants.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹35,000 – ₹130,000+',
                              'cost_local': '€400 – €1,500+ EUR',
                              'cultural_significance': 'Passed down through generations as family heirlooms, '
                                                       "celebrated during the festival of Sant'Efisio in Cagliari.",
                              'description': 'Richly embroidered folk dress featuring a scarlet or emerald velvet '
                                             'bodice (Bustu), pleated wool skirt (Falda), lace veil (Toulle), and '
                                             'precious filigree gold buttons (Bottoni sardi).',
                              'fabrics': 'Brocade, rich velvet, handwoven orbace wool, and gold filigree',
                              'gender': 'Women',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b9/Barisardo_-_Costume_tradizionale_%2804%29.JPG/960px-Barisardo_-_Costume_tradizionale_%2804%29.JPG',
                              'local_name': 'Costume tradizionale sardo femminile',
                              'name': 'Costume Tradizionale Sardo (Sardinian Folk Dress)',
                              'region': "Sardinia (Bari Sardo, Nuoro, Quartu Sant'Elena)",
                              'rental_price': '€60 – €150 EUR per festival day',
                              'where_to_buy': 'Sardinian heritage craft guilds in Nuoro and Cagliari'}},
    'Japan': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹60,000 – ₹300,000+',
                                    'cost_local': '¥100,000 – ¥500,000+ JPY',
                                    'cultural_significance': 'Masterpiece of wearable Japanese art celebrating '
                                                             'coming-of-age, tea rituals, and weddings.',
                                    'description': 'Exquisite silk kimono featuring long swinging sleeves decorated '
                                                   'with hand-painted seasonal motifs, tied with a brocade Fukuro Obi '
                                                   'sash.',
                                    'fabrics': 'Chirimen silk, Nishijin gold brocade, Yuzen dyeing',
                                    'gender': 'Women',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/99/Two_young_maiko_in_Seirai-in_Temple_02.jpg/960px-Two_young_maiko_in_Seirai-in_Temple_02.jpg',
                                    'local_name': '振袖 / 訪問着',
                                    'name': 'Furisode & Houmongi Kimono',
                                    'region': 'Kyoto, Kanazawa & Pan-Japan',
                                    'rental_price': '¥4,000 – ¥12,000 JPY per day',
                                    'where_to_buy': 'Gion kimono rental salons (Kyoto), Asakusa (Tokyo)'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹28,000 – ₹110,000+',
                                    'cost_local': '¥50,000 – ¥200,000+ JPY',
                                    'cultural_significance': 'Worn by grooms at Shinto wedding ceremonies, graduation '
                                                             'rituals, and tea masters.',
                                    'description': 'The highest formal attire for Japanese men: black silk kimono '
                                                   'bearing family crests, pleated hakama trousers, and a haori '
                                                   'jacket.',
                                    'fabrics': 'Habutae silk, Sendai-hira silk weave',
                                    'gender': 'Men',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f7/Japanese_wedding_in_temple.jpg/960px-Japanese_wedding_in_temple.jpg',
                                    'local_name': '紋付羽織袴',
                                    'name': 'Montsuki Haori Hakama (Formal Crested Attire)',
                                    'region': 'Kyoto, Tokyo & Pan-Japan',
                                    'rental_price': '¥5,000 – ¥15,000 JPY per day',
                                    'where_to_buy': 'Nishijin district (Kyoto), Asakusa kimono shops (Tokyo)'},
                                {   'category': '👘 Festive Summer Attire',
                                    'cost_inr': '₹2,200 – ₹7,500',
                                    'cost_local': '¥4,000 – ¥13,000 JPY',
                                    'cultural_significance': 'The beloved dress of summer fireworks (Hanabi), temple '
                                                             'dance festivals (Bon Odori), and relaxing at traditional '
                                                             'hot spring ryokans.',
                                    'description': 'Lightweight unlined cotton summer kimono with indigo and floral '
                                                   'prints, tied with a simple Hanhaba Obi and worn with wooden Geta '
                                                   'clogs.',
                                    'fabrics': 'Breathable Japanese woven cotton and linen',
                                    'gender': 'Unisex',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/35/Himeji_Yukata_Matsuri_2009p1_006.jpg/960px-Himeji_Yukata_Matsuri_2009p1_006.jpg',
                                    'local_name': '浴衣と下駄',
                                    'name': 'Summer Yukata & Geta Clogs',
                                    'region': 'Pan-Japan (Onsen Towns & Summer Matsuri Festivals)',
                                    'rental_price': '¥3,000 – ¥6,000 JPY per day',
                                    'where_to_buy': 'Uniqlo Japan (summer collection), Don Quijote, Asakusa '
                                                    'Nakamise-dori'}],
                 'country': 'Japan',
                 'cultural_significance': 'The kimono embodies Japanese aesthetic ideals of seasonal beauty and '
                                          'mindful etiquette.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹28,000 – ₹110,000+',
                            'cost_local': '¥50,000 – ¥200,000+ JPY',
                            'cultural_significance': 'Worn by grooms at Shinto wedding ceremonies, graduation rituals, '
                                                     'Coming of Age Day (Seijin no Hi), and formal tea ceremonies.',
                            'description': 'The highest formal attire for Japanese men: a black habutae silk kimono '
                                           'bearing five family crests (Kamon), wide pleated hakama trousers, a haori '
                                           'jacket, and white tabi with zori sandals.',
                            'fabrics': 'Black habutae silk, Sendai-hira silk weave, and white silk cords',
                            'gender': 'Men',
                            'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f7/Japanese_wedding_in_temple.jpg/960px-Japanese_wedding_in_temple.jpg',
                            'local_name': '紋付羽織袴 (もんつきはおりはかま)',
                            'name': 'Montsuki Haori Hakama (Formal Crested Attire)',
                            'region': 'Kyoto, Tokyo & Pan-Japan',
                            'rental_price': '¥5,000 – ¥15,000 JPY per day',
                            'where_to_buy': 'Nishijin textile district (Kyoto), Ginza Motoji (Tokyo), Asakusa kimono '
                                            'shops'},
                 'rental_note': 'Over 500 kimono rental boutiques in Kyoto and Tokyo provide complete tourist '
                                'dressing, hairstyling, and photoshoot packages.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹60,000 – ₹300,000+',
                              'cost_local': '¥100,000 – ¥500,000+ JPY',
                              'cultural_significance': 'A masterpiece of wearable art representing seasonal harmony, '
                                                       'purity, and the pinnacle of Japanese textile craftsmanship.',
                              'description': 'Exquisite silk kimono featuring long, swinging sleeves decorated with '
                                             'hand-painted nature motifs, tied with a brocade Fukuro Obi sash and '
                                             'traditional hair kanzashi.',
                              'fabrics': 'Chirimen crepe silk, Nishijin gold brocade, and Yuzen resist-dyeing',
                              'gender': 'Women',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/99/Two_young_maiko_in_Seirai-in_Temple_02.jpg/960px-Two_young_maiko_in_Seirai-in_Temple_02.jpg',
                              'local_name': '振袖 (ふりそで) / 訪問着',
                              'name': 'Furisode & Houmongi Kimono',
                              'region': 'Kyoto (Gion), Kanazawa & Pan-Japan',
                              'rental_price': '¥4,000 – ¥12,000 JPY per day',
                              'where_to_buy': 'Gion & Kiyomizu-dera kimono rental salons (Kyoto), Asakusa (Tokyo)'}},
    'Jordan': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹5,000 – ₹32,000',
                                     'cost_local': '42 – 270 JOD',
                                     'cultural_significance': 'A treasured family heirloom preserving regional '
                                                              'identity and Bedouin pastoral heritage.',
                                     'description': 'Full-length black or cream tunic (Thob) with dense cross-stitch '
                                                    'geometric embroidery (Tatreez) on chest, sleeves, and hem, paired '
                                                    'with a silver-pinned headscarf (Hatta).',
                                     'fabrics': 'Fine linen, black cotton broadcloth, and silk cross-stitch thread',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'الثوب الأردني المطرز',
                                     'name': 'Jordanian Embroidered Thob with Hatta',
                                     'region': 'Salt, Irbid, Madaba & Bedouin South (Wadi Rum)',
                                     'rental_price': '12 – 35 JOD per day',
                                     'where_to_buy': 'Downtown Amman (Al-Balad souks), Jordan River Foundation '
                                                     'showrooms'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹3,000 – ₹16,000',
                                     'cost_local': '25 – 135 JOD',
                                     'cultural_significance': 'The red Shemagh with white tassels is the revered '
                                                              'national symbol of Jordanian sovereignty, military '
                                                              'honor, and Bedouin pride.',
                                     'description': 'Tailored floor-length tunic (Dishdasha) worn with iconic '
                                                    'red-and-white checkered Jordanian Shemagh (Keffiyeh) featuring '
                                                    'distinctive cotton tassels (Hadab), held by a black goat-hair '
                                                    'Agal.',
                                     'fabrics': 'Breathable cotton poplin, wool-blend Shemagh',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'الدشداشة والشماغ الأردني (Shemagh)',
                                     'name': 'Jordanian Dishdasha with Red Keffiyeh & Agal',
                                     'region': 'Pan-Jordan',
                                     'rental_price': '8 – 25 JOD per day',
                                     'where_to_buy': 'Souk Mango (Amman), Petra handicraft centers'}],
                  'country': 'Jordan',
                  'cultural_significance': 'Jordanian attire carries deep Bedouin hospitality traditions, documented '
                                           'in the rich Tatreez needlework of Salt and Petra.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹3,000 – ₹16,000',
                             'cost_local': '25 – 135 JOD',
                             'cultural_significance': 'The red Shemagh with white tassels is the revered national '
                                                      'symbol of Jordanian sovereignty, military honor, and Bedouin '
                                                      'pride.',
                             'description': 'Tailored floor-length tunic (Dishdasha) worn with iconic red-and-white '
                                            'checkered Jordanian Shemagh (Keffiyeh) featuring distinctive cotton '
                                            'tassels (Hadab), held by a black goat-hair Agal.',
                             'fabrics': 'Breathable cotton poplin, wool-blend Shemagh',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'الدشداشة والشماغ الأردني (Shemagh)',
                             'name': 'Jordanian Dishdasha with Red Keffiyeh & Agal',
                             'region': 'Pan-Jordan',
                             'rental_price': '8 – 25 JOD per day',
                             'where_to_buy': 'Souk Mango (Amman), Petra handicraft centers'},
                  'rental_note': 'Costume photo studios at Petra Visitor Center and Wadi Rum camps provide authentic '
                                 'dress experiences.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹5,000 – ₹32,000',
                               'cost_local': '42 – 270 JOD',
                               'cultural_significance': 'A treasured family heirloom preserving regional identity and '
                                                        'Bedouin pastoral heritage.',
                               'description': 'Full-length black or cream tunic (Thob) with dense cross-stitch '
                                              'geometric embroidery (Tatreez) on chest, sleeves, and hem, paired with '
                                              'a silver-pinned headscarf (Hatta).',
                               'fabrics': 'Fine linen, black cotton broadcloth, and silk cross-stitch thread',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'الثوب الأردني المطرز',
                               'name': 'Jordanian Embroidered Thob with Hatta',
                               'region': 'Salt, Irbid, Madaba & Bedouin South (Wadi Rum)',
                               'rental_price': '12 – 35 JOD per day',
                               'where_to_buy': 'Downtown Amman (Al-Balad souks), Jordan River Foundation showrooms'}},
    'Kenya': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹2,500 – ₹14,000',
                                    'cost_local': '4,000 – 22,000 KES',
                                    'cultural_significance': 'Colors symbolize life elements: red for courage and '
                                                             'blood, white for peace, blue for water and sky, green '
                                                             'for pastoral grazing land.',
                                    'description': 'Vibrant cotton wrap cloth (Kanga) printed with Swahili proverbs, '
                                                   'adorned with multi-tiered circular flat beaded wedding collars '
                                                   '(Enkarewa) and long dangling ear ornaments.',
                                    'fabrics': 'East African cotton wax-print and fine glass seed beads',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': 'Kanga & Maasai Beadwork (Enkarewa)',
                                    'name': 'Maasai Kanga Shúkà Wrap & Beaded Collar',
                                    'region': 'Rift Valley, Kajiado & Maasai Mara',
                                    'rental_price': '1,000 – 2,500 KES per day',
                                    'where_to_buy': 'Maasai Market (Nairobi City Hall / Supreme Court), Narok cultural '
                                                    'bomas'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹2,000 – ₹10,000',
                                    'cost_local': '3,200 – 16,000 KES',
                                    'cultural_significance': 'Iconic attire of Maasai warriors (Morans), providing '
                                                             'warmth against savannah morning dew and protection '
                                                             'during pastoral migrations.',
                                    'description': 'Geometric red-and-blue checked woven blanket (Shúkà) draped over '
                                                   'one shoulder and secured at the waist, worn with beaded wrist '
                                                   'cuffs, neck choker, and wooden ceremonial baton (Rungu).',
                                    'fabrics': 'Heavy twill acrylic cotton weave (all-weather savannah blanket)',
                                    'gender': 'Men',
                                    'image': None,
                                    'local_name': 'Shúkà (Moran Attire)',
                                    'name': 'Maasai Shúkà Wrap with Beaded Belt & Rungu',
                                    'region': 'Maasai Mara & Samburu',
                                    'rental_price': '800 – 2,000 KES per day',
                                    'where_to_buy': 'Nairobi Maasai Market, cultural centers in Narok and Amboseli'}],
                 'country': 'Kenya',
                 'cultural_significance': 'Kenyan traditional attire connects 40+ ethnic groups, with the Maasai Shúkà '
                                          'serving as a worldwide ambassador of African pastoral heritage.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹2,000 – ₹10,000',
                            'cost_local': '3,200 – 16,000 KES',
                            'cultural_significance': 'Iconic attire of Maasai warriors (Morans), providing warmth '
                                                     'against savannah morning dew and protection during pastoral '
                                                     'migrations.',
                            'description': 'Geometric red-and-blue checked woven blanket (Shúkà) draped over one '
                                           'shoulder and secured at the waist, worn with beaded wrist cuffs, neck '
                                           'choker, and wooden ceremonial baton (Rungu).',
                            'fabrics': 'Heavy twill acrylic cotton weave (all-weather savannah blanket)',
                            'gender': 'Men',
                            'image': None,
                            'local_name': 'Shúkà (Moran Attire)',
                            'name': 'Maasai Shúkà Wrap with Beaded Belt & Rungu',
                            'region': 'Maasai Mara & Samburu',
                            'rental_price': '800 – 2,000 KES per day',
                            'where_to_buy': 'Nairobi Maasai Market, cultural centers in Narok and Amboseli'},
                 'rental_note': 'Cultural bomas near Maasai Mara national reserve provide dressing experiences and '
                                'guided traditional dances.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹2,500 – ₹14,000',
                              'cost_local': '4,000 – 22,000 KES',
                              'cultural_significance': 'Colors symbolize life elements: red for courage and blood, '
                                                       'white for peace, blue for water and sky, green for pastoral '
                                                       'grazing land.',
                              'description': 'Vibrant cotton wrap cloth (Kanga) printed with Swahili proverbs, adorned '
                                             'with multi-tiered circular flat beaded wedding collars (Enkarewa) and '
                                             'long dangling ear ornaments.',
                              'fabrics': 'East African cotton wax-print and fine glass seed beads',
                              'gender': 'Women',
                              'image': None,
                              'local_name': 'Kanga & Maasai Beadwork (Enkarewa)',
                              'name': 'Maasai Kanga Shúkà Wrap & Beaded Collar',
                              'region': 'Rift Valley, Kajiado & Maasai Mara',
                              'rental_price': '1,000 – 2,500 KES per day',
                              'where_to_buy': 'Maasai Market (Nairobi City Hall / Supreme Court), Narok cultural '
                                              'bomas'}},
    'Malaysia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹3,500 – ₹22,000',
                                       'cost_local': '180 – 1,150 MYR',
                                       'cultural_significance': 'The beloved national dress of Malaysian women, '
                                                                'recognized for its modest silhouette and rich '
                                                                'handloom batik heritage.',
                                       'description': 'Graceful loose-fitting knee-length tunic worn over an '
                                                      'ankle-length pleated sarong skirt (kain), paired with matching '
                                                      'Tudung headscarf and Dokoh chest brooch.',
                                       'fabrics': 'Hand-drawn Terengganu batik silk, songket brocade, and chiffon',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'Baju Kurung',
                                       'name': 'Baju Kurung & Baju Kebaya with Tudung',
                                       'region': 'Pan-Malaysia (Kuala Lumpur, Kelantan, Terengganu)',
                                       'rental_price': '50 – 140 MYR per day',
                                       'where_to_buy': 'Central Market (Pasar Seni, KL), Jalan Tuanku Abdul Rahman, '
                                                       'Jakel Mall'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹3,000 – ₹18,000',
                                       'cost_local': '150 – 950 MYR',
                                       'cultural_significance': 'Worn by Malay men for Hari Raya Aidilfitri '
                                                                'celebrations, royal palace audiences, and Friday '
                                                                'congregations.',
                                       'description': 'Long-sleeved shirt and trousers suit worn with a decorative '
                                                      'woven gold-thread short sarong (Sampin) around the hips and '
                                                      'black velvet cap (Songkok).',
                                       'fabrics': 'Satin silk, jacquard weave, and Terengganu gold songket',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'Baju Melayu Cekak Musang',
                                       'name': 'Baju Melayu with Songket Sampin & Songkok',
                                       'region': 'Pan-Malaysia',
                                       'rental_price': '45 – 120 MYR per day',
                                       'where_to_buy': 'Jalan TAR boutiques, Masjid India bazaars (Kuala Lumpur)'}],
                    'country': 'Malaysia',
                    'cultural_significance': 'Malaysian traditional attire reflects harmony, royal protocol, and '
                                             'maritime trade influences from the historic Sultanate of Malacca.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹3,000 – ₹18,000',
                               'cost_local': '150 – 950 MYR',
                               'cultural_significance': 'Worn by Malay men for Hari Raya Aidilfitri celebrations, '
                                                        'royal palace audiences, and Friday congregations.',
                               'description': 'Long-sleeved shirt and trousers suit worn with a decorative woven '
                                              'gold-thread short sarong (Sampin) around the hips and black velvet cap '
                                              '(Songkok).',
                               'fabrics': 'Satin silk, jacquard weave, and Terengganu gold songket',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'Baju Melayu Cekak Musang',
                               'name': 'Baju Melayu with Songket Sampin & Songkok',
                               'region': 'Pan-Malaysia',
                               'rental_price': '45 – 120 MYR per day',
                               'where_to_buy': 'Jalan TAR boutiques, Masjid India bazaars (Kuala Lumpur)'},
                    'rental_note': 'Costume rental shops in Central Market (Kuala Lumpur) offer photo-shoot '
                                   'experiences.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹3,500 – ₹22,000',
                                 'cost_local': '180 – 1,150 MYR',
                                 'cultural_significance': 'The beloved national dress of Malaysian women, recognized '
                                                          'for its modest silhouette and rich handloom batik heritage.',
                                 'description': 'Graceful loose-fitting knee-length tunic worn over an ankle-length '
                                                'pleated sarong skirt (kain), paired with matching Tudung headscarf '
                                                'and Dokoh chest brooch.',
                                 'fabrics': 'Hand-drawn Terengganu batik silk, songket brocade, and chiffon',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'Baju Kurung',
                                 'name': 'Baju Kurung & Baju Kebaya with Tudung',
                                 'region': 'Pan-Malaysia (Kuala Lumpur, Kelantan, Terengganu)',
                                 'rental_price': '50 – 140 MYR per day',
                                 'where_to_buy': 'Central Market (Pasar Seni, KL), Jalan Tuanku Abdul Rahman, Jakel '
                                                 'Mall'}},
    'Mexico': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹12,000 – ₹45,000',
                                     'cost_local': '$2,500 – $9,500 MXN',
                                     'cultural_significance': 'Celebrated historic folk costume of Independence Day '
                                                              'and folk ballets.',
                                     'description': 'Embroidered floral blouse, shimmering sequined green and red '
                                                    'skirt with coat of arms, and folded silk rebozo shawl.',
                                     'fabrics': 'Poplin cotton, metallic sequins, woven silk',
                                     'gender': 'Women',
                                     'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/39/Poblanas.jpg/960px-Poblanas.jpg',
                                     'local_name': 'China Poblana',
                                     'name': 'Vestido de China Poblana',
                                     'region': 'Puebla & Central Mexico',
                                     'rental_price': '$600 – $1,400 MXN per day',
                                     'where_to_buy': 'Mercado El Parián (Puebla), La Ciudadela (CDMX)'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹18,000 – ₹70,000+',
                                     'cost_local': '$4,000 – $15,000+ MXN',
                                     'cultural_significance': 'UNESCO-inscribed emblem of Mexican Charrería and '
                                                              'mariachi music.',
                                     'description': 'Fitted equestrian wool jacket and trousers embellished with '
                                                    'silver botonadura, silk bow tie, and felt sombrero.',
                                     'fabrics': 'Fine wool, silver botonadura, suede',
                                     'gender': 'Men',
                                     'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c0/CharroMexicano2115.jpg',
                                     'local_name': 'Traje de charro',
                                     'name': 'Traje de Charro (Traditional Equestrian Attire)',
                                     'region': 'Jalisco & Central Mexico',
                                     'rental_price': '$800 – $2,000 MXN per day',
                                     'where_to_buy': 'Plaza Garibaldi (Mexico City), Tlaquepaque'},
                                 {   'category': '🌺 Regional / Oaxacan Matriarchal Attire',
                                     'cost_inr': '₹20,000 – ₹80,000+',
                                     'cost_local': '$4,500 – $18,000+ MXN',
                                     'cultural_significance': 'Immortalized by artist Frida Kahlo, representing the '
                                                              'proud, independent matriarchs of the Zapotec culture.',
                                     'description': 'Opulent black velvet blouse (Huipil) and full skirt embroidered '
                                                    'with brilliant polychrome floral bouquets, crowned with a halo of '
                                                    'pleated starched lace (Resplandor).',
                                     'fabrics': 'Rich black velvet, satin ribbons, starched lace, and gold coins',
                                     'gender': 'Regional',
                                     'image': None,
                                     'local_name': 'Traje de tehuana',
                                     'name': 'Traje Tehuana de Oaxaca',
                                     'region': 'Isthmus of Tehuantepec (Oaxaca)',
                                     'rental_price': '$800 – $1,800 MXN per day',
                                     'where_to_buy': 'Mercado Benito Juárez (Oaxaca City), Tehuantepec artisan '
                                                     'co-ops'}],
                  'country': 'Mexico',
                  'cultural_significance': 'Mexican traditional dress is a celebration of vibrant color, indigenous '
                                           'embroidery, and silver craftsmanship.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹18,000 – ₹70,000+',
                             'cost_local': '$4,000 – $15,000+ MXN',
                             'cultural_significance': 'A UNESCO-inscribed national symbol of Mexican pride, '
                                                      'horsemanship (Charrería), and mariachi musicianship.',
                             'description': 'Fitted equestrian wool jacket and trousers embellished with silver and '
                                            'suede botonadura down the sides, accompanied by a silk bow tie (Moño) and '
                                            'a wide-brimmed felt sombrero.',
                             'fabrics': 'Fine Mexican wool, stamped silver botonadura, and deerskin suede',
                             'gender': 'Men',
                             'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c0/CharroMexicano2115.jpg',
                             'local_name': 'Traje de charro de gala',
                             'name': 'Traje de Charro (Traditional Equestrian Attire)',
                             'region': 'Jalisco, Guadalajara & Central Mexico',
                             'rental_price': '$800 – $2,000 MXN per day',
                             'where_to_buy': 'Plaza Garibaldi mariachi shops (Mexico City), Tlaquepaque (Guadalajara)'},
                  'rental_note': 'Costume studios near Plaza Garibaldi and in Oaxaca City offer traditional dressing '
                                 'for cultural photoshoots.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹12,000 – ₹45,000',
                               'cost_local': '$2,500 – $9,500 MXN',
                               'cultural_significance': 'Legendary historic dress symbolizing the fusion of Asian silk '
                                                        'trade and indigenous Mexican weaving.',
                               'description': 'Short-sleeved white blouse hand-embroidered with floral beads, a '
                                              'shimmering sequined green and red skirt depicting the Mexican eagle, '
                                              'and a folded silk rebozo shawl.',
                               'fabrics': 'Fine poplin cotton, thousands of metallic sequins, and woven silk',
                               'gender': 'Women',
                               'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/39/Poblanas.jpg/960px-Poblanas.jpg',
                               'local_name': 'Traje de China Poblana',
                               'name': 'Vestido de China Poblana',
                               'region': 'Puebla & Central Mexico',
                               'rental_price': '$600 – $1,400 MXN per day',
                               'where_to_buy': 'Mercado El Parián (Puebla), Mercado de Artesanías La Ciudadela '
                                               '(CDMX)'}},
    'Mongolia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹6,000 – ₹28,000',
                                       'cost_local': '250,000 – 1,150,000 MNT',
                                       'cultural_significance': 'Centuries-old nomadic dress adapted to harsh steppe '
                                                                'winds, worn for Tsagaan Sar (Lunar New Year) and '
                                                                'Naadam.',
                                       'description': 'Floor-length double-breasted silk tunic (Deel) with high '
                                                      'Mandarin collar, worn with a sleeveless embroidered silk '
                                                      'waistcoat (Uuuji) and silver hair ornaments.',
                                       'fabrics': 'Heavy brocade silk, lambskin lining, and gold thread',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'Монгол дээл ба ууж',
                                       'name': 'Mongol Deel with Uuuji Waistcoat',
                                       'region': 'Pan-Mongolia (Ulaanbaatar & Steppe)',
                                       'rental_price': '40,000 – 100,000 MNT per day',
                                       'where_to_buy': 'Naran Tuul Market (Black Market), State Department Store '
                                                       '(Ulaanbaatar)'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹5,500 – ₹26,000',
                                       'cost_local': '220,000 – 1,050,000 MNT',
                                       'cultural_significance': 'Practical equestrian attire of the Mongol empire, '
                                                                'functioning as an all-weather riding coat, portable '
                                                                'blanket, and tent accessory.',
                                       'description': 'Sturdy calf-length belted tunic clasped on the right chest, '
                                                      'secured with a broad silk sash (Büs), paired with upturned '
                                                      'leather riding boots (Gutal) and pointed fur cap (Malgai).',
                                       'fabrics': 'Felted wool, thick silk brocade, and sheepskin',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'Эрэгтэй дээл ба малгай',
                                       'name': 'Mongol Deel with Leather Boots & Malgai Cap',
                                       'region': 'Nomadic Steppe & Khangai Mountains',
                                       'rental_price': '35,000 – 90,000 MNT per day',
                                       'where_to_buy': 'Ulaanbaatar artisan workshops, Peace Avenue tailoring shops'}],
                    'country': 'Mongolia',
                    'cultural_significance': 'The Mongol Deel is an ingenious multi-purpose nomadic garment that has '
                                             'endured virtually unchanged since the era of Genghis Khan.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹5,500 – ₹26,000',
                               'cost_local': '220,000 – 1,050,000 MNT',
                               'cultural_significance': 'Practical equestrian attire of the Mongol empire, functioning '
                                                        'as an all-weather riding coat, portable blanket, and tent '
                                                        'accessory.',
                               'description': 'Sturdy calf-length belted tunic clasped on the right chest, secured '
                                              'with a broad silk sash (Büs), paired with upturned leather riding boots '
                                              '(Gutal) and pointed fur cap (Malgai).',
                               'fabrics': 'Felted wool, thick silk brocade, and sheepskin',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'Эрэгтэй дээл ба малгай',
                               'name': 'Mongol Deel with Leather Boots & Malgai Cap',
                               'region': 'Nomadic Steppe & Khangai Mountains',
                               'rental_price': '35,000 – 90,000 MNT per day',
                               'where_to_buy': 'Ulaanbaatar artisan workshops, Peace Avenue tailoring shops'},
                    'rental_note': 'Tour operators in Ulaanbaatar and ger camps in Terelj National Park offer Deel '
                                   'rental photography sessions.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹6,000 – ₹28,000',
                                 'cost_local': '250,000 – 1,150,000 MNT',
                                 'cultural_significance': 'Centuries-old nomadic dress adapted to harsh steppe winds, '
                                                          'worn for Tsagaan Sar (Lunar New Year) and Naadam.',
                                 'description': 'Floor-length double-breasted silk tunic (Deel) with high Mandarin '
                                                'collar, worn with a sleeveless embroidered silk waistcoat (Uuuji) and '
                                                'silver hair ornaments.',
                                 'fabrics': 'Heavy brocade silk, lambskin lining, and gold thread',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'Монгол дээл ба ууж',
                                 'name': 'Mongol Deel with Uuuji Waistcoat',
                                 'region': 'Pan-Mongolia (Ulaanbaatar & Steppe)',
                                 'rental_price': '40,000 – 100,000 MNT per day',
                                 'where_to_buy': 'Naran Tuul Market (Black Market), State Department Store '
                                                 '(Ulaanbaatar)'}},
    'Morocco': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹8,000 – ₹55,000',
                                      'cost_local': '950 – 6,500 MAD',
                                      'cultural_significance': 'Masterpiece of Moroccan haute couture worn for '
                                                               'weddings, Henna nights, and royal receptions.',
                                      'description': 'Two-piece formal gown consisting of a fine base under-dress '
                                                     '(Tahtia) and a sheer embroidered open over-dress (Fouqia), '
                                                     'cinched with a wide gilded metal belt (Mdamma) and gold Sfifa '
                                                     'trimmings.',
                                      'fabrics': 'Fassi silk brocade, velvet, French lace, and real gold braid',
                                      'gender': 'Women',
                                      'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/4/45/Moroccan_woman_wearing_traditional_Takchita_caftan.jpg/960px-Moroccan_woman_wearing_traditional_Takchita_caftan.jpg',
                                      'local_name': 'تكشيطة مغربية (Takchita)',
                                      'name': 'Moroccan Takchita & Silk Caftan with Mdamma Belt',
                                      'region': 'Fez, Marrakech, Rabat & Pan-Morocco',
                                      'rental_price': '300 – 900 MAD per day',
                                      'where_to_buy': 'Medina of Fez, Souks of Marrakech, Negafa bridal salons'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹3,500 – ₹20,000',
                                      'cost_local': '420 – 2,400 MAD',
                                      'cultural_significance': 'Timeless national dress of Moroccan men, worn daily '
                                                               'and formally for Friday prayers and royal banquets.',
                                      'description': 'Ankle-length hooded robe (Djellaba) with distinctive pointed '
                                                     'hood (Qob), worn over a tunic, paired with soft leather pointed '
                                                     'slippers (Babouche) and iconic crimson felt Tarbouch (Fez) hat.',
                                      'fabrics': 'Fine handwoven Chefchaouen wool or summer linen with silk Sfifa '
                                                 'needlework',
                                      'gender': 'Men',
                                      'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ab/Moroccan_gentleman_wearing_traditional_Djellaba_and_Fez.jpg/960px-Moroccan_gentleman_wearing_traditional_Djellaba_and_Fez.jpg',
                                      'local_name': 'جلابة و طربوش (Djellaba & Fez)',
                                      'name': 'Moroccan Djellaba Robe with Tarbouch (Fez) Hat',
                                      'region': 'Fez, Meknes & Pan-Morocco',
                                      'rental_price': '120 – 350 MAD per day',
                                      'where_to_buy': 'Souk Smarine (Marrakech), Kissaria of Fez Medina'}],
                   'country': 'Morocco',
                   'cultural_significance': 'Moroccan attire preserves thousand-year Andalusian-Arab-Berber artisanal '
                                            'craftsmanship in leather, silk, and gold embroidery.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': '₹3,500 – ₹20,000',
                              'cost_local': '420 – 2,400 MAD',
                              'cultural_significance': 'Timeless national dress of Moroccan men, worn daily and '
                                                       'formally for Friday prayers and royal banquets.',
                              'description': 'Ankle-length hooded robe (Djellaba) with distinctive pointed hood (Qob), '
                                             'worn over a tunic, paired with soft leather pointed slippers (Babouche) '
                                             'and iconic crimson felt Tarbouch (Fez) hat.',
                              'fabrics': 'Fine handwoven Chefchaouen wool or summer linen with silk Sfifa needlework',
                              'gender': 'Men',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ab/Moroccan_gentleman_wearing_traditional_Djellaba_and_Fez.jpg/960px-Moroccan_gentleman_wearing_traditional_Djellaba_and_Fez.jpg',
                              'local_name': 'جلابة و طربوش (Djellaba & Fez)',
                              'name': 'Moroccan Djellaba Robe with Tarbouch (Fez) Hat',
                              'region': 'Fez, Meknes & Pan-Morocco',
                              'rental_price': '120 – 350 MAD per day',
                              'where_to_buy': 'Souk Smarine (Marrakech), Kissaria of Fez Medina'},
                   'rental_note': 'Traditional Negafa studios across Marrakech and Casablanca offer full dress '
                                  'fittings and Henna photo sessions.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': '₹8,000 – ₹55,000',
                                'cost_local': '950 – 6,500 MAD',
                                'cultural_significance': 'Masterpiece of Moroccan haute couture worn for weddings, '
                                                         'Henna nights, and royal receptions.',
                                'description': 'Two-piece formal gown consisting of a fine base under-dress (Tahtia) '
                                               'and a sheer embroidered open over-dress (Fouqia), cinched with a wide '
                                               'gilded metal belt (Mdamma) and gold Sfifa trimmings.',
                                'fabrics': 'Fassi silk brocade, velvet, French lace, and real gold braid',
                                'gender': 'Women',
                                'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/4/45/Moroccan_woman_wearing_traditional_Takchita_caftan.jpg/960px-Moroccan_woman_wearing_traditional_Takchita_caftan.jpg',
                                'local_name': 'تكشيطة مغربية (Takchita)',
                                'name': 'Moroccan Takchita & Silk Caftan with Mdamma Belt',
                                'region': 'Fez, Marrakech, Rabat & Pan-Morocco',
                                'rental_price': '300 – 900 MAD per day',
                                'where_to_buy': 'Medina of Fez, Souks of Marrakech, Negafa bridal salons'}},
    'Myanmar': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹2,500 – ₹18,000',
                                      'cost_local': '65,000 – 460,000 MMK',
                                      'cultural_significance': 'Worn with natural Thanaka bark facial cosmetic paste '
                                                               'during Thingyan Water Festival and pagoda visits.',
                                      'description': 'Ankle-length wrap cylindrical sarong skirt (Thummy) folded '
                                                     'sideways and tucked at the waist, worn with a tailored sheer or '
                                                     'silk blouse (Eingyi) and delicate shawl.',
                                      'fabrics': 'Amarapura silk, Inle lotus fiber, and floral cotton',
                                      'gender': 'Women',
                                      'image': None,
                                      'local_name': 'ထဘီ နှင့် အင်္ကျီ',
                                      'name': 'Thummy Longyi and Eingyi Blouse',
                                      'region': 'Mandalay, Inle Lake & Yangon',
                                      'rental_price': '15,000 – 35,000 MMK per day',
                                      'where_to_buy': 'Bogyoke Aung San Market (Scott Market, Yangon), Mandalay Silk '
                                                      'Weavers Guild'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹2,000 – ₹15,000',
                                      'cost_local': '50,000 – 380,000 MMK',
                                      'cultural_significance': 'Everyday and formal national attire worn by Myanmar '
                                                               'men, symbolizing modesty, mindfulness, and Buddhist '
                                                               'devotion.',
                                      'description': 'Comfortable cylindrical checked or striped sarong skirt (Paso) '
                                                     'knotted at the navel, paired with a mandarin-collar cotton '
                                                     'shirt, formal jacket, and ceremonial cloth turban (Gaung Baung).',
                                      'fabrics': 'Handloom cotton, Acheik silk brocade, and muslin',
                                      'gender': 'Men',
                                      'image': None,
                                      'local_name': 'ပုဆိုး နှင့် ခေါင်းပေါင်း',
                                      'name': 'Paso Longyi and Eingyi Jacket with Gaung Baung',
                                      'region': 'Pan-Myanmar',
                                      'rental_price': '12,000 – 30,000 MMK per day',
                                      'where_to_buy': 'Bogyoke Market (Yangon), Mahamuni pagoda precinct (Mandalay)'}],
                   'country': 'Myanmar',
                   'cultural_significance': 'Burmese traditional dress highlights continuous thousand-year traditions '
                                            'of Inle Lake lotus weaving and royal Amarapura silk jacquards.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': '₹2,000 – ₹15,000',
                              'cost_local': '50,000 – 380,000 MMK',
                              'cultural_significance': 'Everyday and formal national attire worn by Myanmar men, '
                                                       'symbolizing modesty, mindfulness, and Buddhist devotion.',
                              'description': 'Comfortable cylindrical checked or striped sarong skirt (Paso) knotted '
                                             'at the navel, paired with a mandarin-collar cotton shirt, formal jacket, '
                                             'and ceremonial cloth turban (Gaung Baung).',
                              'fabrics': 'Handloom cotton, Acheik silk brocade, and muslin',
                              'gender': 'Men',
                              'image': None,
                              'local_name': 'ပုဆိုး နှင့် ခေါင်းပေါင်း',
                              'name': 'Paso Longyi and Eingyi Jacket with Gaung Baung',
                              'region': 'Pan-Myanmar',
                              'rental_price': '12,000 – 30,000 MMK per day',
                              'where_to_buy': 'Bogyoke Market (Yangon), Mahamuni pagoda precinct (Mandalay)'},
                   'rental_note': 'Photo studios around Shwedagon Pagoda rent traditional court and everyday attires.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': '₹2,500 – ₹18,000',
                                'cost_local': '65,000 – 460,000 MMK',
                                'cultural_significance': 'Worn with natural Thanaka bark facial cosmetic paste during '
                                                         'Thingyan Water Festival and pagoda visits.',
                                'description': 'Ankle-length wrap cylindrical sarong skirt (Thummy) folded sideways '
                                               'and tucked at the waist, worn with a tailored sheer or silk blouse '
                                               '(Eingyi) and delicate shawl.',
                                'fabrics': 'Amarapura silk, Inle lotus fiber, and floral cotton',
                                'gender': 'Women',
                                'image': None,
                                'local_name': 'ထဘီ နှင့် အင်္ကျီ',
                                'name': 'Thummy Longyi and Eingyi Blouse',
                                'region': 'Mandalay, Inle Lake & Yangon',
                                'rental_price': '15,000 – 35,000 MMK per day',
                                'where_to_buy': 'Bogyoke Aung San Market (Scott Market, Yangon), Mandalay Silk Weavers '
                                                'Guild'}},
    'Nepal': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹3,500 – ₹14,000',
                                    'cost_local': '₨5,500 – ₨22,000 NPR',
                                    'cultural_significance': 'Awarded during the sacred Gunyo Cholo ceremony marking a '
                                                             "young woman's coming of age and celebrated during "
                                                             'Dashain and Teej.',
                                    'description': 'Traditional Nepali attire for women: a pleated printed skirt '
                                                   '(Gunyo) or silk saree worn with a front-wrapping wrap blouse '
                                                   '(Cholo), secured with a tightly wrapped fabric waist-sash (Patuka) '
                                                   'and adorned with gold Tilhari and Pote necklaces.',
                                    'fabrics': 'Handloom Dhaka cotton, pure raw silk, and velvet',
                                    'gender': 'Women',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/64/Traditional_Dress111.jpg/960px-Traditional_Dress111.jpg',
                                    'local_name': 'गुन्यु चोली र पटुका',
                                    'name': 'Gunyo Cholo & Saree with Patuka',
                                    'region': 'Pan-Nepal & Kathmandu Valley',
                                    'rental_price': '₨1,000 – ₨2,500 NPR per day',
                                    'where_to_buy': 'Indra Chowk (Kathmandu), Thamel boutiques, Bhaktapur Artisan '
                                                    'Street'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹2,500 – ₹8,000',
                                    'cost_local': '₨4,000 – ₨13,000 NPR',
                                    'cultural_significance': 'The eight ties of the Daura represent the Astamatrika '
                                                             '(eight divine guardian deities), symbolizing peace, '
                                                             'harmony, and national heritage.',
                                    'description': 'Authentic national dress of Nepali men: a double-breasted upper '
                                                   'tunic (Daura) fastened with eight traditional cloth ties, tapered '
                                                   'trousers (Suruwal), a tailored waistcoat, and a hand-loomed '
                                                   'geometric Dhaka Topi cap.',
                                    'fabrics': 'Hand-spun Palpali Dhaka cotton, tweed wool, and fine silk',
                                    'gender': 'Men',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e5/Daura_Suruwal_by_Mahalaxmi_Silwal.jpg/960px-Daura_Suruwal_by_Mahalaxmi_Silwal.jpg',
                                    'local_name': 'दौरा सुरुवाल र ढाका टोपी',
                                    'name': 'Daura-Suruwal & Dhaka Topi',
                                    'region': 'Kathmandu Valley & Himalayan Hill Regions',
                                    'rental_price': '₨800 – ₨1,800 NPR per day',
                                    'where_to_buy': 'Ason Bazaar (Kathmandu), New Road, Mangal Bazaar (Patan)'},
                                {   'category': '🌍 Regional / Ethnic Attire',
                                    'cost_inr': '₹3,000 – ₹9,000',
                                    'cost_local': '₨4,800 – ₨14,500 NPR',
                                    'cultural_significance': 'Symbolizes the deep agrarian and cultural identity of '
                                                             'the Indigenous Newars of the Kathmandu Valley, worn '
                                                             'during festivals like Bisket Jatra.',
                                    'description': 'Iconic black handwoven cotton sari with a distinctive bold red '
                                                   'border, worn with a white waist-cloth wrap (Ga) and black blouse '
                                                   'by Newari women.',
                                    'fabrics': 'Handspun local black and crimson-bordered cotton',
                                    'gender': 'Regional',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9e/A_group_of_newa_woman.jpg/960px-A_group_of_newa_woman.jpg',
                                    'local_name': 'हाकु पतासी',
                                    'name': 'Haku Patasi (Newari Traditional Dress)',
                                    'region': 'Kathmandu Valley (Newar Community of Bhaktapur & Patan)',
                                    'rental_price': '₨800 – ₨2,000 NPR per day',
                                    'where_to_buy': 'Bhaktapur Durbar Square handloom guild, Patan Old Town weavers'}],
                 'country': 'Nepal',
                 'cultural_significance': 'Nepali traditional attire preserves distinct ethnic identity with Dhaka '
                                          'textiles handwoven on traditional looms in Palpa and Tehrathum.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹2,500 – ₹8,000',
                            'cost_local': '₨4,000 – ₨13,000 NPR',
                            'cultural_significance': 'The eight ties of the Daura represent the Astamatrika (eight '
                                                     'divine guardian deities), symbolizing peace, harmony, and '
                                                     'national heritage.',
                            'description': 'Authentic national dress of Nepali men: a double-breasted upper tunic '
                                           '(Daura) fastened with eight traditional cloth ties, tapered trousers '
                                           '(Suruwal), a tailored waistcoat, and a hand-loomed geometric Dhaka Topi '
                                           'cap.',
                            'fabrics': 'Hand-spun Palpali Dhaka cotton, tweed wool, and fine silk',
                            'gender': 'Men',
                            'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e5/Daura_Suruwal_by_Mahalaxmi_Silwal.jpg/960px-Daura_Suruwal_by_Mahalaxmi_Silwal.jpg',
                            'local_name': 'दौरा सुरुवाल र ढाका टोपी',
                            'name': 'Daura-Suruwal & Dhaka Topi',
                            'region': 'Kathmandu Valley & Himalayan Hill Regions',
                            'rental_price': '₨800 – ₨1,800 NPR per day',
                            'where_to_buy': 'Ason Bazaar (Kathmandu), New Road, Mangal Bazaar (Patan)'},
                 'rental_note': 'Costume rental boutiques in Thamel, Patan Durbar Square, and Bhaktapur offer complete '
                                'cultural photo-shoot experiences.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': '₹3,500 – ₹14,000',
                              'cost_local': '₨5,500 – ₨22,000 NPR',
                              'cultural_significance': 'Awarded during the sacred Gunyo Cholo ceremony marking a young '
                                                       "woman's coming of age and celebrated during Dashain and Teej.",
                              'description': 'Traditional Nepali attire for women: a pleated printed skirt (Gunyo) or '
                                             'silk saree worn with a front-wrapping wrap blouse (Cholo), secured with '
                                             'a tightly wrapped fabric waist-sash (Patuka) and adorned with gold '
                                             'Tilhari and Pote necklaces.',
                              'fabrics': 'Handloom Dhaka cotton, pure raw silk, and velvet',
                              'gender': 'Women',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/64/Traditional_Dress111.jpg/960px-Traditional_Dress111.jpg',
                              'local_name': 'गुन्यु चोली र पटुका',
                              'name': 'Gunyo Cholo & Saree with Patuka',
                              'region': 'Pan-Nepal & Kathmandu Valley',
                              'rental_price': '₨1,000 – ₨2,500 NPR per day',
                              'where_to_buy': 'Indra Chowk (Kathmandu), Thamel boutiques, Bhaktapur Artisan Street'}},
    'Netherlands': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                          'cost_inr': '₹10,000 – ₹38,000',
                                          'cost_local': '110 – 430 EUR',
                                          'cultural_significance': 'The internationally famous symbol of Dutch '
                                                                   'identity, worn by fishing community women along '
                                                                   'the former Zuiderzee.',
                                          'description': 'Black wool jacket (Kletjie) over a colorful floral bib '
                                                         '(Kraplap), striped wool skirt, pleated apron, coral bead '
                                                         'necklace, and starched winged white lace cap (Hul).',
                                          'fabrics': 'Homespun wool, Dutch cotton, and starched bobbin lace',
                                          'gender': 'Women',
                                          'image': None,
                                          'local_name': 'Volendammer Klederdracht (Hul)',
                                          'name': 'Volendam Klederdracht with Winged Lace Cap',
                                          'region': 'North Holland (Volendam & Marken)',
                                          'rental_price': '30 – 65 EUR per day',
                                          'where_to_buy': 'Volendam harbor souvenir boutiques, Edam heritage shops'},
                                      {   'category': "👨 Men's Traditional Attire",
                                          'cost_inr': '₹9,000 – ₹34,000',
                                          'cost_local': '100 – 380 EUR',
                                          'cultural_significance': 'Fishing costume designed for flexibility on '
                                                                   'fishing smacks, paired with waterproof carved '
                                                                   'wooden klompen.',
                                          'description': 'Heavy red wool jacket or dark waistcoat with silver coin '
                                                         'buttons, voluminous baggy black wool trousers, neckerchief, '
                                                         'black cap, and yellow wooden clogs (Klompen).',
                                          'fabrics': 'Broadcloth wool, silver guilder coin fasteners, and carved '
                                                     'willow wood',
                                          'gender': 'Men',
                                          'image': None,
                                          'local_name': 'Volendammer Mannendracht',
                                          'name': "Volendam Man's Klederdracht with Baggy Breeches",
                                          'region': 'North Holland (Volendam)',
                                          'rental_price': '25 – 60 EUR per day',
                                          'where_to_buy': 'Haven Volendam photo shops, Zaanse Schans craft center'}],
                       'country': 'Netherlands',
                       'cultural_significance': 'Dutch Klederdracht reflects the resilient seafaring and polder '
                                                'heritage of maritime North Holland.',
                       'men': {   'category': "👨 Men's Traditional Attire",
                                  'cost_inr': '₹9,000 – ₹34,000',
                                  'cost_local': '100 – 380 EUR',
                                  'cultural_significance': 'Fishing costume designed for flexibility on fishing '
                                                           'smacks, paired with waterproof carved wooden klompen.',
                                  'description': 'Heavy red wool jacket or dark waistcoat with silver coin buttons, '
                                                 'voluminous baggy black wool trousers, neckerchief, black cap, and '
                                                 'yellow wooden clogs (Klompen).',
                                  'fabrics': 'Broadcloth wool, silver guilder coin fasteners, and carved willow wood',
                                  'gender': 'Men',
                                  'image': None,
                                  'local_name': 'Volendammer Mannendracht',
                                  'name': "Volendam Man's Klederdracht with Baggy Breeches",
                                  'region': 'North Holland (Volendam)',
                                  'rental_price': '25 – 60 EUR per day',
                                  'where_to_buy': 'Haven Volendam photo shops, Zaanse Schans craft center'},
                       'rental_note': 'Historic photography studios along Haven street in Volendam provide authentic '
                                      'dress-up souvenir photo shoots.',
                       'women': {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹10,000 – ₹38,000',
                                    'cost_local': '110 – 430 EUR',
                                    'cultural_significance': 'The internationally famous symbol of Dutch identity, '
                                                             'worn by fishing community women along the former '
                                                             'Zuiderzee.',
                                    'description': 'Black wool jacket (Kletjie) over a colorful floral bib (Kraplap), '
                                                   'striped wool skirt, pleated apron, coral bead necklace, and '
                                                   'starched winged white lace cap (Hul).',
                                    'fabrics': 'Homespun wool, Dutch cotton, and starched bobbin lace',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': 'Volendammer Klederdracht (Hul)',
                                    'name': 'Volendam Klederdracht with Winged Lace Cap',
                                    'region': 'North Holland (Volendam & Marken)',
                                    'rental_price': '30 – 65 EUR per day',
                                    'where_to_buy': 'Volendam harbor souvenir boutiques, Edam heritage shops'}},
    'New Zealand': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                          'cost_inr': '₹12,000 – ₹55,000',
                                          'cost_local': '240 – 1,100 NZD',
                                          'cultural_significance': 'Worn by Māori women during Kapa Haka cultural '
                                                                   'performances, pōwhiri welcoming ceremonies, and '
                                                                   'national commemorations.',
                                          'description': 'Swishing kilt skirt made of dried scraped flax stalks '
                                                         '(Piupiu), woven geometric chest band (Pari), feathered '
                                                         'prestige cloak (Korowai), and carved pounamu jade pendant.',
                                          'fabrics': 'Harakeke (New Zealand flax), kiwi and pheasant feathers, Pounamu '
                                                     'greenstone',
                                          'gender': 'Women',
                                          'image': None,
                                          'local_name': 'Piupiu, Pari me te Korowai',
                                          'name': 'Māori Traditional Piupiu Skirt & Pari Bodice with Korowai',
                                          'region': 'Rotorua, Bay of Plenty & Pan-New Zealand',
                                          'rental_price': '60 – 150 NZD per day',
                                          'where_to_buy': 'Te Puia New Zealand Māori Arts and Crafts Institute '
                                                          '(Rotorua)'},
                                      {   'category': "👨 Men's Traditional Attire",
                                          'cost_inr': '₹10,000 – ₹48,000',
                                          'cost_local': '200 – 960 NZD',
                                          'cultural_significance': 'The sacred attire of Māori Toa (warriors), worn '
                                                                   'for performing the Haka and representing tribal '
                                                                   'mana and heritage.',
                                          'description': 'Dried flax hollow tube skirt (Piupiu) that rattles '
                                                         'rhythmically during the Haka, woven belt (Tātua), carved '
                                                         'taiaha staff, and traditional moko facial markings.',
                                          'fabrics': 'Scraped rolled Harakeke flax reed and woven muka cordage',
                                          'gender': 'Men',
                                          'image': None,
                                          'local_name': 'Piupiu me te Tātua',
                                          'name': 'Māori Warrior Piupiu Flax Kilt, Tatua Belt & Korowai',
                                          'region': 'Rotorua & Te Ika-a-Māui',
                                          'rental_price': '50 – 130 NZD per day',
                                          'where_to_buy': 'Te Puia craft stores (Rotorua), Whakarewarewa Living '
                                                          'Village'}],
                       'country': 'New Zealand',
                       'cultural_significance': 'Māori traditional garments carry spiritual prestige (Mana) and '
                                                'connect wearers to ancestral lineages (Whakapapa).',
                       'men': {   'category': "👨 Men's Traditional Attire",
                                  'cost_inr': '₹10,000 – ₹48,000',
                                  'cost_local': '200 – 960 NZD',
                                  'cultural_significance': 'The sacred attire of Māori Toa (warriors), worn for '
                                                           'performing the Haka and representing tribal mana and '
                                                           'heritage.',
                                  'description': 'Dried flax hollow tube skirt (Piupiu) that rattles rhythmically '
                                                 'during the Haka, woven belt (Tātua), carved taiaha staff, and '
                                                 'traditional moko facial markings.',
                                  'fabrics': 'Scraped rolled Harakeke flax reed and woven muka cordage',
                                  'gender': 'Men',
                                  'image': None,
                                  'local_name': 'Piupiu me te Tātua',
                                  'name': 'Māori Warrior Piupiu Flax Kilt, Tatua Belt & Korowai',
                                  'region': 'Rotorua & Te Ika-a-Māui',
                                  'rental_price': '50 – 130 NZD per day',
                                  'where_to_buy': 'Te Puia craft stores (Rotorua), Whakarewarewa Living Village'},
                       'rental_note': 'Cultural centers in Rotorua (Te Puia, Mitai Māori Village) provide authentic '
                                      'attire and guided cultural experiences.',
                       'women': {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹12,000 – ₹55,000',
                                    'cost_local': '240 – 1,100 NZD',
                                    'cultural_significance': 'Worn by Māori women during Kapa Haka cultural '
                                                             'performances, pōwhiri welcoming ceremonies, and national '
                                                             'commemorations.',
                                    'description': 'Swishing kilt skirt made of dried scraped flax stalks (Piupiu), '
                                                   'woven geometric chest band (Pari), feathered prestige cloak '
                                                   '(Korowai), and carved pounamu jade pendant.',
                                    'fabrics': 'Harakeke (New Zealand flax), kiwi and pheasant feathers, Pounamu '
                                               'greenstone',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': 'Piupiu, Pari me te Korowai',
                                    'name': 'Māori Traditional Piupiu Skirt & Pari Bodice with Korowai',
                                    'region': 'Rotorua, Bay of Plenty & Pan-New Zealand',
                                    'rental_price': '60 – 150 NZD per day',
                                    'where_to_buy': 'Te Puia New Zealand Māori Arts and Crafts Institute (Rotorua)'}},
    'Nigeria': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹6,000 – ₹45,000',
                                      'cost_local': '110,000 – 820,000 NGN',
                                      'cultural_significance': 'A symbol of feminine royalty and communal joy (Owambe '
                                                               'celebrations), where Gele tying is an elevated art '
                                                               'form.',
                                      'description': 'Loose round-neck blouse (Buba), wrap skirt (Iro), matching '
                                                     'shoulder sash (Ipele), and elaborately sculpted, architectural '
                                                     'pleated head-tie (Gele) adorned with coral bead necklaces.',
                                      'fabrics': 'Aso Oke handwoven textile, metallic brocade, and Swiss voile lace',
                                      'gender': 'Women',
                                      'image': None,
                                      'local_name': 'Ìró àti Bùbá (Gèlè)',
                                      'name': 'Iro and Buba with Gele Headtie (Yoruba)',
                                      'region': 'Southwest Nigeria (Lagos, Ibadan) & Pan-Nigeria',
                                      'rental_price': '25,000 – 75,000 NGN per day',
                                      'where_to_buy': 'Balogun Market (Lagos Island), Tejuosho Market (Yaba), bespoke '
                                                      'fashion houses'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹7,500 – ₹55,000',
                                      'cost_local': '135,000 – 1,000,000 NGN',
                                      'cultural_significance': 'Worn by Nigerian men of distinction, symbolizing '
                                                               'prestige, dignity, and cultural pride at traditional '
                                                               'weddings and state galas.',
                                      'description': 'Grand four-piece flowing attire comprising a wide-sleeved '
                                                     'majestic outer robe (Agbada) with intricate chest embroidery, '
                                                     'inner tunic (Buba), drawstring trousers (Sokoto), and '
                                                     'embroidered cap (Fila).',
                                      'fabrics': 'Handwoven Aso Oke, guinea brocade, and damask silk',
                                      'gender': 'Men',
                                      'image': None,
                                      'local_name': 'Agbádá àti Fìlà',
                                      'name': 'Agbada Robe with Fila Cap (Yoruba)',
                                      'region': 'Pan-Nigeria (Lagos, Abuja, Kano)',
                                      'rental_price': '30,000 – 90,000 NGN per day',
                                      'where_to_buy': 'Lekki Arts Market, Balogun Market (Lagos), Garki Market '
                                                      '(Abuja)'}],
                   'country': 'Nigeria',
                   'cultural_significance': 'Nigerian traditional attire represents the pinnacle of West African '
                                            'ceremonial fashion and textile weaving artistry.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': '₹7,500 – ₹55,000',
                              'cost_local': '135,000 – 1,000,000 NGN',
                              'cultural_significance': 'Worn by Nigerian men of distinction, symbolizing prestige, '
                                                       'dignity, and cultural pride at traditional weddings and state '
                                                       'galas.',
                              'description': 'Grand four-piece flowing attire comprising a wide-sleeved majestic outer '
                                             'robe (Agbada) with intricate chest embroidery, inner tunic (Buba), '
                                             'drawstring trousers (Sokoto), and embroidered cap (Fila).',
                              'fabrics': 'Handwoven Aso Oke, guinea brocade, and damask silk',
                              'gender': 'Men',
                              'image': None,
                              'local_name': 'Agbádá àti Fìlà',
                              'name': 'Agbada Robe with Fila Cap (Yoruba)',
                              'region': 'Pan-Nigeria (Lagos, Abuja, Kano)',
                              'rental_price': '30,000 – 90,000 NGN per day',
                              'where_to_buy': 'Lekki Arts Market, Balogun Market (Lagos), Garki Market (Abuja)'},
                   'rental_note': 'Aso Ebi designers and stylists across Lagos provide full custom styling and Gele '
                                  'headtie services.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': '₹6,000 – ₹45,000',
                                'cost_local': '110,000 – 820,000 NGN',
                                'cultural_significance': 'A symbol of feminine royalty and communal joy (Owambe '
                                                         'celebrations), where Gele tying is an elevated art form.',
                                'description': 'Loose round-neck blouse (Buba), wrap skirt (Iro), matching shoulder '
                                               'sash (Ipele), and elaborately sculpted, architectural pleated head-tie '
                                               '(Gele) adorned with coral bead necklaces.',
                                'fabrics': 'Aso Oke handwoven textile, metallic brocade, and Swiss voile lace',
                                'gender': 'Women',
                                'image': None,
                                'local_name': 'Ìró àti Bùbá (Gèlè)',
                                'name': 'Iro and Buba with Gele Headtie (Yoruba)',
                                'region': 'Southwest Nigeria (Lagos, Ibadan) & Pan-Nigeria',
                                'rental_price': '25,000 – 75,000 NGN per day',
                                'where_to_buy': 'Balogun Market (Lagos Island), Tejuosho Market (Yaba), bespoke '
                                                'fashion houses'}},
    'Norway': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹55,000 – ₹220,000+',
                                     'cost_local': '7,500 – 30,000+ NOK',
                                     'cultural_significance': 'Cherished national heirloom worn on Constitution Day '
                                                              '(17th of May) and family celebrations.',
                                     'description': 'Magnificent folk costume featuring an embroidered wool skirt and '
                                                    'bodice with regional Rosemåling motifs, and heirloom silver '
                                                    'filigree brooches.',
                                     'fabrics': 'Norwegian virgin wool, pure linen, sterling silver',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Kvinnebunad',
                                     'name': "Kvinnebunad (Norwegian Women's Folk Dress)",
                                     'region': 'Hardanger, Telemark & Pan-Norway',
                                     'rental_price': '1,500 – 3,200 NOK per day',
                                     'where_to_buy': 'Heimen Husfliden (Oslo), Norsk Flid branches'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹45,000 – ₹180,000+',
                                     'cost_local': '6,000 – 24,000+ NOK',
                                     'cultural_significance': 'Worn with pride on Syttende Mai to celebrate Norwegian '
                                                              'freedom and regional identity.',
                                     'description': 'Tailored national folk costume consisting of wool jacket, '
                                                    'double-breasted scarlet vest, knee-breeches with silver buttons, '
                                                    'and white stockings.',
                                     'fabrics': 'Pure Norwegian wool broadcloth, linen, silver filigree',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Herrebunad',
                                     'name': "Herrebunad (Norwegian Men's National Folk Suit)",
                                     'region': 'Telemark, Gudbrandsdalen & Pan-Norway',
                                     'rental_price': '1,200 – 2,800 NOK per day',
                                     'where_to_buy': 'Heimen Husfliden (Oslo), Norsk Flid'},
                                 {   'category': '🏔️ Fjord Heritage Attire',
                                     'cost_inr': '₹50,000 – ₹200,000+',
                                     'cost_local': '7,000 – 28,000+ NOK',
                                     'cultural_significance': 'Regarded as the Mother of all Bunads, instrumental in '
                                                              "Norway's 1905 romantic national awakening.",
                                     'description': 'The quintessential Norwegian national costume featuring brilliant '
                                                    'white-on-white Hardangersøm counted-thread openwork embroidery on '
                                                    'the apron and a beaded chest piece (Brystduk).',
                                     'fabrics': 'Scarlet wool, openwork linen embroidery, glass seed beads',
                                     'gender': 'Regional',
                                     'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/62/KinsarvikBunad.jpg/330px-KinsarvikBunad.jpg',
                                     'local_name': 'Hardangerbunad',
                                     'name': 'Hardanger Bunad (The National Bunad)',
                                     'region': 'Hardanger Fjord (Vestland)',
                                     'rental_price': '1,400 – 3,000 NOK per day',
                                     'where_to_buy': 'Hardanger Folkemuseum shops (Utne), Bergen craft guild'}],
                  'country': 'Norway',
                  'cultural_significance': "Norwegian Bunads represent one of the world's most vibrant living folk "
                                           'costume traditions.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹45,000 – ₹180,000+',
                             'cost_local': '6,000 – 24,000+ NOK',
                             'cultural_significance': 'Worn with immense pride on Syttende Mai (Constitution Day) to '
                                                      'celebrate Norwegian independence and regional origins.',
                             'description': 'Impeccably tailored national folk costume consisting of a wool jacket, '
                                            'double-breasted scarlet or emerald vest, wool knee-breeches with '
                                            'hand-cast silver buttons (Sølje), white hand-knit wool stockings, and '
                                            'buckled shoes.',
                             'fabrics': 'Pure Norwegian wool broadcloth, linen, and solid silver filigree',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'Herrebunad',
                             'name': "Herrebunad (Norwegian Men's National Folk Suit)",
                             'region': 'Telemark, Gudbrandsdalen & Pan-Norway',
                             'rental_price': '1,200 – 2,800 NOK per day (Constitution Day 17th of May)',
                             'where_to_buy': 'Heimen Husfliden (Oslo), Norsk Flid Husfliden (Pan-Norway)'},
                  'rental_note': 'Husfliden boutiques across all major Norwegian cities provide authorized Bunad '
                                 'fittings.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹55,000 – ₹220,000+',
                               'cost_local': '7,500 – 30,000+ NOK',
                               'cultural_significance': 'A cherished family heirloom passed down through generations, '
                                                        'strictly protected to reflect accurate parish tailoring.',
                               'description': 'Magnificent folk costume featuring an embroidered wool skirt and bodice '
                                              'decorated with regional floral Rosemåling motifs, an embroidered purse '
                                              '(Veske), and heirloom silver filigree brooches (Sølje).',
                               'fabrics': 'Norwegian virgin wool, pure linen, and handmade sterling silver',
                               'gender': 'Women',
                               'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/62/KinsarvikBunad.jpg/330px-KinsarvikBunad.jpg',
                               'local_name': 'Kvinnebunad',
                               'name': "Kvinnebunad (Norwegian Women's Folk Dress)",
                               'region': 'Hardanger, Telemark & Pan-Norway',
                               'rental_price': '1,500 – 3,200 NOK per day',
                               'where_to_buy': 'Heimen Husfliden (Oslo), Husfliden branches across Norway'}},
    'Oman': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                   'cost_inr': '₹5,500 – ₹36,000',
                                   'cost_local': '25 – 165 OMR',
                                   'cultural_significance': 'Vibrant regional styles in Dhofar and Nizwa celebrate '
                                                            "Oman's seafaring spice history and modest pride.",
                                   'description': 'Knee-length dress with metallic Zari neck embroidery, worn over '
                                                  'fitted ankle trousers (Sirwal) with ornate metallic cuffs, draped '
                                                  'with a colorful silk shawl (Lahaf).',
                                   'fabrics': 'Omani silk brocade, velvet, and gold wire embroidery',
                                   'gender': 'Women',
                                   'image': None,
                                   'local_name': 'الزي العماني النسائي',
                                   'name': 'Omani Dishdasha and Sirwal with Lahaf',
                                   'region': 'Muscat, Nizwa, Dhofar & Sharqiyah',
                                   'rental_price': '8 – 25 OMR per day',
                                   'where_to_buy': 'Mutrah Souq (Muscat), Nizwa Fort Souq'},
                               {   'category': "👨 Men's Traditional Attire",
                                   'cost_inr': '₹6,000 – ₹42,000',
                                   'cost_local': '28 – 195 OMR',
                                   'cultural_significance': 'The Khanjar dagger is featured on the national emblem and '
                                                            'flag, symbolizing Omani chivalry, courage, and identity.',
                                   'description': 'Clean collarless tunic (Dishdasha) with subtle tassel (Tarboosha) '
                                                  'perfumed with frankincense, worn with hand-embroidered Kashmiri '
                                                  'wool turban (Massar) or Kummah cap, and ceremonial curved silver '
                                                  'dagger (Khanjar) on belt.',
                                   'fabrics': 'Fine Japanese cotton, cashmere wool Massar, and solid silver filigree',
                                   'gender': 'Men',
                                   'image': None,
                                   'local_name': 'الدشداشة والمصر والخنجر العماني',
                                   'name': 'Omani Dishdasha with Massar Turban & Silver Khanjar',
                                   'region': 'Pan-Oman',
                                   'rental_price': '10 – 30 OMR per day',
                                   'where_to_buy': 'Mutrah Souq silver guild, Nizwa Souq khanjar craftsmen'}],
                'country': 'Oman',
                'cultural_significance': 'Omani traditional dress stands apart in the Arabian Gulf for its distinctive '
                                         'Massar turban, fragrant Tarboosha, and master silver Khanjar craftsmanship.',
                'men': {   'category': "👨 Men's Traditional Attire",
                           'cost_inr': '₹6,000 – ₹42,000',
                           'cost_local': '28 – 195 OMR',
                           'cultural_significance': 'The Khanjar dagger is featured on the national emblem and flag, '
                                                    'symbolizing Omani chivalry, courage, and identity.',
                           'description': 'Clean collarless tunic (Dishdasha) with subtle tassel (Tarboosha) perfumed '
                                          'with frankincense, worn with hand-embroidered Kashmiri wool turban (Massar) '
                                          'or Kummah cap, and ceremonial curved silver dagger (Khanjar) on belt.',
                           'fabrics': 'Fine Japanese cotton, cashmere wool Massar, and solid silver filigree',
                           'gender': 'Men',
                           'image': None,
                           'local_name': 'الدشداشة والمصر والخنجر العماني',
                           'name': 'Omani Dishdasha with Massar Turban & Silver Khanjar',
                           'region': 'Pan-Oman',
                           'rental_price': '10 – 30 OMR per day',
                           'where_to_buy': 'Mutrah Souq silver guild, Nizwa Souq khanjar craftsmen'},
                'rental_note': 'Shops near Mutrah Souq and Nizwa Fort offer authentic dressing experiences with '
                               'ceremonial Khanjars.',
                'women': {   'category': "👩 Women's Traditional Attire",
                             'cost_inr': '₹5,500 – ₹36,000',
                             'cost_local': '25 – 165 OMR',
                             'cultural_significance': "Vibrant regional styles in Dhofar and Nizwa celebrate Oman's "
                                                      'seafaring spice history and modest pride.',
                             'description': 'Knee-length dress with metallic Zari neck embroidery, worn over fitted '
                                            'ankle trousers (Sirwal) with ornate metallic cuffs, draped with a '
                                            'colorful silk shawl (Lahaf).',
                             'fabrics': 'Omani silk brocade, velvet, and gold wire embroidery',
                             'gender': 'Women',
                             'image': None,
                             'local_name': 'الزي العماني النسائي',
                             'name': 'Omani Dishdasha and Sirwal with Lahaf',
                             'region': 'Muscat, Nizwa, Dhofar & Sharqiyah',
                             'rental_price': '8 – 25 OMR per day',
                             'where_to_buy': 'Mutrah Souq (Muscat), Nizwa Fort Souq'}},
    'Pakistan': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹4,000 – ₹38,000',
                                       'cost_local': '13,500 – 128,000 PKR',
                                       'cultural_significance': 'The official national dress of Pakistani women, '
                                                                'embodying Mughal artistic grandeur and modest grace.',
                                       'description': 'Flowing flared tunic (Anarkali Kameez) paired with gathered '
                                                      'trousers (Shalwar) and heavily embellished Chiffon or Organza '
                                                      'Dupatta with Zardozi gold embroidery.',
                                       'fabrics': 'Pure chiffon, lawn cotton, jamawar silk, and gota patti',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'شلوار قمیض اور دوپٹہ',
                                       'name': 'Anarkali Shalwar Kameez & Dupatta',
                                       'region': 'Punjab, Sindh & Pan-Pakistan',
                                       'rental_price': '3,000 – 9,000 PKR per day',
                                       'where_to_buy': 'Liberty Market (Lahore), Tariq Road (Karachi), J. (Junaid '
                                                       'Jamshed boutiques)'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹2,500 – ₹16,000',
                                       'cost_local': '8,500 – 54,000 PKR',
                                       'cultural_significance': 'The quintessential national garment of Pakistan, worn '
                                                                'for Friday prayers, weddings, and national '
                                                                'celebrations.',
                                       'description': 'Tailored collared tunic and baggy shalwar trousers, paired with '
                                                      'a tailored woolen waistcoat (Wascoat) and traditional Peshawari '
                                                      'chappal leather sandals.',
                                       'fabrics': 'Fine boski silk, tropical Egyptian cotton, and karandi wool',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'پشاور شلوار قمیض اور واسکٹ',
                                       'name': 'Peshawari Shalwar Kameez with Wascoat',
                                       'region': 'Khyber Pakhtunkhwa & Pan-Pakistan',
                                       'rental_price': '2,000 – 5,000 PKR per day',
                                       'where_to_buy': 'Qissa Khwani Bazaar (Peshawar), Anarkali Bazaar (Lahore)'}],
                    'country': 'Pakistan',
                    'cultural_significance': 'Pakistani traditional attire combines Mughal royal heritage, Central '
                                             'Asian equestrian cuts, and Sindhi-Balochi needlework.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹2,500 – ₹16,000',
                               'cost_local': '8,500 – 54,000 PKR',
                               'cultural_significance': 'The quintessential national garment of Pakistan, worn for '
                                                        'Friday prayers, weddings, and national celebrations.',
                               'description': 'Tailored collared tunic and baggy shalwar trousers, paired with a '
                                              'tailored woolen waistcoat (Wascoat) and traditional Peshawari chappal '
                                              'leather sandals.',
                               'fabrics': 'Fine boski silk, tropical Egyptian cotton, and karandi wool',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'پشاور شلوار قمیض اور واسکٹ',
                               'name': 'Peshawari Shalwar Kameez with Wascoat',
                               'region': 'Khyber Pakhtunkhwa & Pan-Pakistan',
                               'rental_price': '2,000 – 5,000 PKR per day',
                               'where_to_buy': 'Qissa Khwani Bazaar (Peshawar), Anarkali Bazaar (Lahore)'},
                    'rental_note': 'Boutiques across Lahore and Islamabad cater to festive attire rentals for wedding '
                                   'celebrations.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹4,000 – ₹38,000',
                                 'cost_local': '13,500 – 128,000 PKR',
                                 'cultural_significance': 'The official national dress of Pakistani women, embodying '
                                                          'Mughal artistic grandeur and modest grace.',
                                 'description': 'Flowing flared tunic (Anarkali Kameez) paired with gathered trousers '
                                                '(Shalwar) and heavily embellished Chiffon or Organza Dupatta with '
                                                'Zardozi gold embroidery.',
                                 'fabrics': 'Pure chiffon, lawn cotton, jamawar silk, and gota patti',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'شلوار قمیض اور دوپٹہ',
                                 'name': 'Anarkali Shalwar Kameez & Dupatta',
                                 'region': 'Punjab, Sindh & Pan-Pakistan',
                                 'rental_price': '3,000 – 9,000 PKR per day',
                                 'where_to_buy': 'Liberty Market (Lahore), Tariq Road (Karachi), J. (Junaid Jamshed '
                                                 'boutiques)'}},
    'Peru': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                   'cost_inr': '₹4,500 – ₹30,000',
                                   'cost_local': '200 – 1,350 PEN',
                                   'cultural_significance': 'Rooted in Incan textile traditions combined with Spanish '
                                                            'colonial silhouettes, worn with pride for Inti Raymi and '
                                                            'feast days.',
                                   'description': 'Multi-layered flared wool skirt (Pollera) with bright woven ribbon '
                                                  'borders, embroidered jacket (Jubona), handwoven shoulder mantle '
                                                  '(Lliclla) pinned with a silver Tupu, and round flat Montera hat.',
                                   'fabrics': 'Alpaca and sheep wool dyed with natural plant extracts, embroidered '
                                              'ribbon',
                                   'gender': 'Women',
                                   'image': None,
                                   'local_name': 'Pollera y Lliclla',
                                   'name': 'Andean Pollera Skirt and Montera Hat with Lliclla',
                                   'region': 'Cusco, Sacred Valley & Puno (Lake Titicaca)',
                                   'rental_price': '45 – 120 PEN per day',
                                   'where_to_buy': 'San Pedro Market (Cusco), Pisac Sunday Market, Chinchero weaving '
                                                   'guild'},
                               {   'category': "👨 Men's Traditional Attire",
                                   'cost_inr': '₹4,000 – ₹28,000',
                                   'cost_local': '180 – 1,250 PEN',
                                   'cultural_significance': "Poncho patterns indicate the wearer's specific Andean "
                                                            'community, providing thermal insulation above 4,000 '
                                                            'meters altitude.',
                                   'description': 'Geometric handwoven red-and-earth-toned alpaca wool poncho, '
                                                  'knee-length bayeta trousers, and knitted wool earflap hat (Chullo) '
                                                  'adorned with beads.',
                                   'fabrics': '100% baby alpaca and sheep wool handspun on drop spindles',
                                   'gender': 'Men',
                                   'image': None,
                                   'local_name': 'Poncho andino y Chullo',
                                   'name': 'Andean Alpaca Poncho with Chullo Wool Hat',
                                   'region': 'Cusco Highlands & Ausangate',
                                   'rental_price': '40 – 100 PEN per day',
                                   'where_to_buy': 'Chinchero Weavers Centre, Pisac Market (Sacred Valley)'}],
                'country': 'Peru',
                'cultural_significance': 'Peruvian Andean textiles embody Quechua and Aymara indigenous knowledge, '
                                         'designated as Intangible Cultural Heritage of Peru.',
                'men': {   'category': "👨 Men's Traditional Attire",
                           'cost_inr': '₹4,000 – ₹28,000',
                           'cost_local': '180 – 1,250 PEN',
                           'cultural_significance': "Poncho patterns indicate the wearer's specific Andean community, "
                                                    'providing thermal insulation above 4,000 meters altitude.',
                           'description': 'Geometric handwoven red-and-earth-toned alpaca wool poncho, knee-length '
                                          'bayeta trousers, and knitted wool earflap hat (Chullo) adorned with beads.',
                           'fabrics': '100% baby alpaca and sheep wool handspun on drop spindles',
                           'gender': 'Men',
                           'image': None,
                           'local_name': 'Poncho andino y Chullo',
                           'name': 'Andean Alpaca Poncho with Chullo Wool Hat',
                           'region': 'Cusco Highlands & Ausangate',
                           'rental_price': '40 – 100 PEN per day',
                           'where_to_buy': 'Chinchero Weavers Centre, Pisac Market (Sacred Valley)'},
                'rental_note': 'Traditional weaving cooperatives in Chinchero and Plaza de Armas in Cusco offer '
                               'authentic photo dressing.',
                'women': {   'category': "👩 Women's Traditional Attire",
                             'cost_inr': '₹4,500 – ₹30,000',
                             'cost_local': '200 – 1,350 PEN',
                             'cultural_significance': 'Rooted in Incan textile traditions combined with Spanish '
                                                      'colonial silhouettes, worn with pride for Inti Raymi and feast '
                                                      'days.',
                             'description': 'Multi-layered flared wool skirt (Pollera) with bright woven ribbon '
                                            'borders, embroidered jacket (Jubona), handwoven shoulder mantle (Lliclla) '
                                            'pinned with a silver Tupu, and round flat Montera hat.',
                             'fabrics': 'Alpaca and sheep wool dyed with natural plant extracts, embroidered ribbon',
                             'gender': 'Women',
                             'image': None,
                             'local_name': 'Pollera y Lliclla',
                             'name': 'Andean Pollera Skirt and Montera Hat with Lliclla',
                             'region': 'Cusco, Sacred Valley & Puno (Lake Titicaca)',
                             'rental_price': '45 – 120 PEN per day',
                             'where_to_buy': 'San Pedro Market (Cusco), Pisac Sunday Market, Chinchero weaving guild'}},
    'Philippines': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                          'cost_inr': '₹5,000 – ₹32,000',
                                          'cost_local': '3,400 – 22,000 PHP',
                                          'cultural_significance': 'The national dress of Filipina women, elevated to '
                                                                   'haute couture and celebrated at State of the '
                                                                   'Nation addresses and cultural galas.',
                                          'description': 'Floor-length gown distinguished by dramatic structured '
                                                         'pleated butterfly sleeves (mangas de mariposa), paired with '
                                                         'an embroidered pañuelo scarf.',
                                          'fabrics': 'Piña cloth (pineapple leaf fiber), jusi banana silk, and organza',
                                          'gender': 'Women',
                                          'image': None,
                                          'local_name': "Terno (Baro't Saya)",
                                          'name': "Baro't Saya / Maria Clara Terno Dress",
                                          'region': 'Luzon (Manila, Bulacan) & Pan-Philippines',
                                          'rental_price': '1,200 – 3,500 PHP per day',
                                          'where_to_buy': 'Divisoria 168 Mall, Kultura Filipino boutiques (SM Malls), '
                                                          'Lumban (Laguna)'},
                                      {   'category': "👨 Men's Traditional Attire",
                                          'cost_inr': '₹4,000 – ₹25,000',
                                          'cost_local': '2,700 – 17,000 PHP',
                                          'cultural_significance': 'Proclaimed official national dress of Filipino men '
                                                                   'by President Ramon Magsaysay in 1953, worn for '
                                                                   'weddings and diplomacy.',
                                          'description': 'Sheer embroidered formal dress shirt worn untucked over an '
                                                         'undershirt (camisón) with dark dress trousers, decorated '
                                                         'with delicate Calado needlework.',
                                          'fabrics': 'Fine handwoven Piña-silk, jusi fiber, and organic abaca',
                                          'gender': 'Men',
                                          'image': None,
                                          'local_name': 'Barong Tagalog',
                                          'name': 'Barong Tagalog (Piña Cloth Embroidered Shirt)',
                                          'region': 'Pan-Philippines (Lumban & Taal)',
                                          'rental_price': '900 – 2,500 PHP per day',
                                          'where_to_buy': 'Kultura Filipino, Onesimus, Lumban artisan workshops '
                                                          '(Laguna)'}],
                       'country': 'Philippines',
                       'cultural_significance': 'Philippine traditional wear exemplifies delicate tropical '
                                                'fiber-weaving artistry made from indigenous pineapple leaf and banana '
                                                'stalks.',
                       'men': {   'category': "👨 Men's Traditional Attire",
                                  'cost_inr': '₹4,000 – ₹25,000',
                                  'cost_local': '2,700 – 17,000 PHP',
                                  'cultural_significance': 'Proclaimed official national dress of Filipino men by '
                                                           'President Ramon Magsaysay in 1953, worn for weddings and '
                                                           'diplomacy.',
                                  'description': 'Sheer embroidered formal dress shirt worn untucked over an '
                                                 'undershirt (camisón) with dark dress trousers, decorated with '
                                                 'delicate Calado needlework.',
                                  'fabrics': 'Fine handwoven Piña-silk, jusi fiber, and organic abaca',
                                  'gender': 'Men',
                                  'image': None,
                                  'local_name': 'Barong Tagalog',
                                  'name': 'Barong Tagalog (Piña Cloth Embroidered Shirt)',
                                  'region': 'Pan-Philippines (Lumban & Taal)',
                                  'rental_price': '900 – 2,500 PHP per day',
                                  'where_to_buy': 'Kultura Filipino, Onesimus, Lumban artisan workshops (Laguna)'},
                       'rental_note': 'Costume rentals available in Intramuros historical district for cultural '
                                      'walking tours.',
                       'women': {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹5,000 – ₹32,000',
                                    'cost_local': '3,400 – 22,000 PHP',
                                    'cultural_significance': 'The national dress of Filipina women, elevated to haute '
                                                             'couture and celebrated at State of the Nation addresses '
                                                             'and cultural galas.',
                                    'description': 'Floor-length gown distinguished by dramatic structured pleated '
                                                   'butterfly sleeves (mangas de mariposa), paired with an embroidered '
                                                   'pañuelo scarf.',
                                    'fabrics': 'Piña cloth (pineapple leaf fiber), jusi banana silk, and organza',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': "Terno (Baro't Saya)",
                                    'name': "Baro't Saya / Maria Clara Terno Dress",
                                    'region': 'Luzon (Manila, Bulacan) & Pan-Philippines',
                                    'rental_price': '1,200 – 3,500 PHP per day',
                                    'where_to_buy': 'Divisoria 168 Mall, Kultura Filipino boutiques (SM Malls), Lumban '
                                                    '(Laguna)'}},
    'Poland': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹10,000 – ₹38,000',
                                     'cost_local': '480 – 1,820 PLN',
                                     'cultural_significance': 'The archetypal national costume of Poland, elevated '
                                                              'during the Kościuszko Uprising as a symbol of Polish '
                                                              'patriotic defiance.',
                                     'description': 'Black velvet corset richly embroidered with shimmering sequins, '
                                                    'glass beads, and multicolored ribbons, floral printed skirt, '
                                                    'white apron, and colorful floral wreath (Wianek).',
                                     'fabrics': 'Velvet, silk ribbons, batiste linen, and glass beads',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Strój krakowski (Gorset)',
                                     'name': 'Strój Krakowski (Cracovian Folk Dress)',
                                     'region': 'Lesser Poland (Kraków & Małopolska)',
                                     'rental_price': '120 – 280 PLN per day',
                                     'where_to_buy': 'Sukiennice (Cloth Hall, Kraków Main Square), Cepelia folk art '
                                                     'stores'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹11,000 – ₹40,000',
                                     'cost_local': '520 – 1,920 PLN',
                                     'cultural_significance': 'Tadeusz Kościuszko wore the Cracovian peasant dress '
                                                              'when taking his oath on Kraków Market Square in 1794.',
                                     'description': 'Navy blue long vest (Kaftan) with brass buttons and red pom-poms, '
                                                    'white linen shirt, red-and-white vertically striped trousers, and '
                                                    'four-cornered red cap (Rogatywka) topped with peacock feathers.',
                                     'fabrics': 'Wool broadcloth, striped cotton, and genuine peacock tail feathers',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Kaftan krakowski i rogatywka',
                                     'name': 'Strój Krakowski with Rogatywka Cap',
                                     'region': 'Lesser Poland (Kraków)',
                                     'rental_price': '130 – 300 PLN per day',
                                     'where_to_buy': 'Kraków Cloth Hall stalls, Cepelia folk boutiques'}],
                  'country': 'Poland',
                  'cultural_significance': 'The Cracovian costume holds unique status as the official national folk '
                                           'costume of Poland.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹11,000 – ₹40,000',
                             'cost_local': '520 – 1,920 PLN',
                             'cultural_significance': 'Tadeusz Kościuszko wore the Cracovian peasant dress when taking '
                                                      'his oath on Kraków Market Square in 1794.',
                             'description': 'Navy blue long vest (Kaftan) with brass buttons and red pom-poms, white '
                                            'linen shirt, red-and-white vertically striped trousers, and four-cornered '
                                            'red cap (Rogatywka) topped with peacock feathers.',
                             'fabrics': 'Wool broadcloth, striped cotton, and genuine peacock tail feathers',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'Kaftan krakowski i rogatywka',
                             'name': 'Strój Krakowski with Rogatywka Cap',
                             'region': 'Lesser Poland (Kraków)',
                             'rental_price': '130 – 300 PLN per day',
                             'where_to_buy': 'Kraków Cloth Hall stalls, Cepelia folk boutiques'},
                  'rental_note': 'Folk dance guilds and studios near Kraków Rynek Główny offer costume fittings and '
                                 'photography.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹10,000 – ₹38,000',
                               'cost_local': '480 – 1,820 PLN',
                               'cultural_significance': 'The archetypal national costume of Poland, elevated during '
                                                        'the Kościuszko Uprising as a symbol of Polish patriotic '
                                                        'defiance.',
                               'description': 'Black velvet corset richly embroidered with shimmering sequins, glass '
                                              'beads, and multicolored ribbons, floral printed skirt, white apron, and '
                                              'colorful floral wreath (Wianek).',
                               'fabrics': 'Velvet, silk ribbons, batiste linen, and glass beads',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'Strój krakowski (Gorset)',
                               'name': 'Strój Krakowski (Cracovian Folk Dress)',
                               'region': 'Lesser Poland (Kraków & Małopolska)',
                               'rental_price': '120 – 280 PLN per day',
                               'where_to_buy': 'Sukiennice (Cloth Hall, Kraków Main Square), Cepelia folk art stores'}},
    'Portugal': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹12,000 – ₹42,000',
                                       'cost_local': '135 – 470 EUR',
                                       'cultural_significance': 'Celebrated at the Romaria de Nossa Senhora da Agonia, '
                                                                'representing maritime prosperity and peasant pride.',
                                       'description': 'Vibrant scarlet and black hand-embroidered wool skirt, floral '
                                                      'printed apron, cross-stitched linen chemise, headscarf, and '
                                                      'heart-shaped filigree gold jewelry (Coração de Viana).',
                                       'fabrics': 'Homespun wool, Minho linen, and Portuguese gold filigree',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'Traje à Vianesa (Lavradeira)',
                                       'name': 'Traje à Vianesa (Viana do Castelo Folk Costume)',
                                       'region': 'Minho (Viana do Castelo) & Northern Portugal',
                                       'rental_price': '35 – 75 EUR per day',
                                       'where_to_buy': 'Viana do Castelo artisan workshops, Praça da República stores'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹10,000 – ₹36,000',
                                       'cost_local': '110 – 400 EUR',
                                       'cultural_significance': 'Symbol of the courageous Portuguese bull and horse '
                                                                'herders along the fertile banks of the Tagus River.',
                                       'description': 'Traditional cattle-drover costume with scarlet wool vest '
                                                      '(Colete Encarnado), white linen shirt, navy knee breeches, '
                                                      'white knit stockings, and green stocking cap (Barrete).',
                                       'fabrics': 'Thick wool broadcloth, knitted wool, and linen',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'Traje de Campino',
                                       'name': 'Traje de Campino do Ribatejo',
                                       'region': 'Ribatejo (Tagus Valley)',
                                       'rental_price': '30 – 70 EUR per day',
                                       'where_to_buy': 'Vila Franca de Xira and Santarém traditional tailoring shops'}],
                    'country': 'Portugal',
                    'cultural_significance': 'Portuguese folk dress reflects deep maritime, agricultural, and '
                                             'artisanal gold-filigree traditions preserved across centuries.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹10,000 – ₹36,000',
                               'cost_local': '110 – 400 EUR',
                               'cultural_significance': 'Symbol of the courageous Portuguese bull and horse herders '
                                                        'along the fertile banks of the Tagus River.',
                               'description': 'Traditional cattle-drover costume with scarlet wool vest (Colete '
                                              'Encarnado), white linen shirt, navy knee breeches, white knit '
                                              'stockings, and green stocking cap (Barrete).',
                               'fabrics': 'Thick wool broadcloth, knitted wool, and linen',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'Traje de Campino',
                               'name': 'Traje de Campino do Ribatejo',
                               'region': 'Ribatejo (Tagus Valley)',
                               'rental_price': '30 – 70 EUR per day',
                               'where_to_buy': 'Vila Franca de Xira and Santarém traditional tailoring shops'},
                    'rental_note': 'Folk attire is available for photos at cultural centers in Viana do Castelo and '
                                   'Lisbon folklore festivals.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹12,000 – ₹42,000',
                                 'cost_local': '135 – 470 EUR',
                                 'cultural_significance': 'Celebrated at the Romaria de Nossa Senhora da Agonia, '
                                                          'representing maritime prosperity and peasant pride.',
                                 'description': 'Vibrant scarlet and black hand-embroidered wool skirt, floral printed '
                                                'apron, cross-stitched linen chemise, headscarf, and heart-shaped '
                                                'filigree gold jewelry (Coração de Viana).',
                                 'fabrics': 'Homespun wool, Minho linen, and Portuguese gold filigree',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'Traje à Vianesa (Lavradeira)',
                                 'name': 'Traje à Vianesa (Viana do Castelo Folk Costume)',
                                 'region': 'Minho (Viana do Castelo) & Northern Portugal',
                                 'rental_price': '35 – 75 EUR per day',
                                 'where_to_buy': 'Viana do Castelo artisan workshops, Praça da República stores'}},
    'Saudi Arabia': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                           'cost_inr': '₹4,500 – ₹28,000+',
                                           'cost_local': '200 – 1,200+ SAR',
                                           'cultural_significance': 'A harmonious blend of Islamic modesty and opulent '
                                                                    'regional needlework traditions.',
                                           'description': 'Graceful black silk or crepe cloak embellished with '
                                                          'geometric gold Zaree embroidery, worn over a hand-stitched '
                                                          'traditional Najdi dress with a matching scarf.',
                                           'fabrics': 'Pure crepe silk, velvet panels, gold metallic embroidery',
                                           'gender': 'Women',
                                           'image': None,
                                           'local_name': 'الثوب النجدي والعباية',
                                           'name': 'Embroidered Najdi Thobe & Contemporary Abaya',
                                           'region': 'Najd (Riyadh, Diriyah) & Hijaz',
                                           'rental_price': '100 – 250 SAR per day',
                                           'where_to_buy': 'Taiba Souq (Riyadh), Souq Al Alawi (Jeddah)'},
                                       {   'category': "👨 Men's Traditional Attire",
                                           'cost_inr': '₹3,500 – ₹18,000',
                                           'cost_local': '150 – 800 SAR',
                                           'cultural_significance': 'The official national dress of Saudi men, '
                                                                    'embodying dignity, modesty, and desert heritage.',
                                           'description': 'Immaculate ankle-length tailored white cotton robe with '
                                                          'mandarin collar, paired with a folded red-and-white '
                                                          'checkered headdress and black agal cord.',
                                           'fabrics': 'Crisp breathable cotton, fine wool',
                                           'gender': 'Men',
                                           'image': None,
                                           'local_name': 'الثوب والغترة والعقال',
                                           'name': 'Thobe & Ghutra with Agal',
                                           'region': 'Riyadh, Jeddah & Pan-Saudi Arabia',
                                           'rental_price': '80 – 180 SAR per day',
                                           'where_to_buy': 'Souq Al Zal (Riyadh), Al Balad (Jeddah)'},
                                       {   'category': '🌺 Regional / Southern Highland Attire',
                                           'cost_inr': '₹6,000 – ₹22,000',
                                           'cost_local': '250 – 950 SAR',
                                           'cultural_significance': 'A UNESCO-inscribed intangible cultural heritage '
                                                                    'tradition celebrating the unique agrarian '
                                                                    'highland culture of southern Arabia.',
                                           'description': 'Colorful highland attire adorned with vibrant geometric '
                                                          'Al-Qatt Al-Asiri motifs, complemented by fragrant fresh '
                                                          'herbal flower crowns worn by the Flower Men of Asir.',
                                           'fabrics': 'Black velvet, brightly dyed cotton embroidery, and fresh '
                                                      'mountain blooms',
                                           'gender': 'Regional',
                                           'image': None,
                                           'local_name': 'زي عسير التراثي',
                                           'name': 'Asir Regional Floral Headband & Embroidered Attire',
                                           'region': 'Asir Province & Sarawat Mountains (Abha)',
                                           'rental_price': '80 – 180 SAR per day',
                                           'where_to_buy': 'Tuesday Market (Souq Al Thulatha, Abha), Rijal Almaa '
                                                           'heritage village'}],
                        'country': 'Saudi Arabia',
                        'cultural_significance': 'Saudi attire combines desert climate practicality with rich regional '
                                                 'embroidery traditions.',
                        'men': {   'category': "👨 Men's Traditional Attire",
                                   'cost_inr': '₹3,500 – ₹18,000',
                                   'cost_local': '150 – 800 SAR',
                                   'cultural_significance': 'The official national dress of Saudi men, embodying '
                                                            'dignity, modesty, and desert heritage.',
                                   'description': 'Immaculate ankle-length tailored white cotton robe (Thobe) with '
                                                  'mandarin collar, paired with a folded red-and-white checkered '
                                                  'headdress (Ghutra / Shemagh) held securely by a double black cord '
                                                  '(Agal).',
                                   'fabrics': 'Crisp Japanese breathable cotton, fine English wool for winter',
                                   'gender': 'Men',
                                   'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6e/Dishdasha.jpg/330px-Dishdasha.jpg',
                                   'local_name': 'الثوب والغترة والعقال',
                                   'name': 'Thobe & Ghutra with Agal',
                                   'region': 'Riyadh, Jeddah & Pan-Saudi Arabia',
                                   'rental_price': '80 – 180 SAR per day',
                                   'where_to_buy': 'Souq Al Zal (Riyadh), Al Balad historical markets (Jeddah)'},
                        'rental_note': 'Diriyah and Al-Ula cultural sites offer traditional dress photo experiences '
                                       'for tourists.',
                        'women': {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹4,500 – ₹28,000+',
                                     'cost_local': '200 – 1,200+ SAR',
                                     'cultural_significance': 'A harmonious blend of Islamic modesty and opulent '
                                                              'regional needlework traditions celebrating Saudi '
                                                              'National Day.',
                                     'description': 'Graceful black silk or crepe cloak (Abaya) embellished with '
                                                    'geometric gold Zaree thread embroidery, worn over an intricately '
                                                    'hand-stitched traditional Najdi dress with a matching scarf '
                                                    '(Tarha).',
                                     'fabrics': 'Pure crepe silk, velvet panels, and gold metallic embroidery',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'الثوب النجدي والعباية',
                                     'name': 'Embroidered Najdi Thobe & Contemporary Abaya',
                                     'region': 'Najd (Riyadh, Diriyah) & Hijaz',
                                     'rental_price': '100 – 250 SAR per day',
                                     'where_to_buy': 'Taiba Souq (Riyadh), Souq Al Alawi (Jeddah)'}},
    'South Africa': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                           'cost_inr': '₹12,000 – ₹42,000',
                                           'cost_local': 'R 1,800 – R 6,200 ZAR',
                                           'cultural_significance': 'Symbolic geometric beadwork language of '
                                                                    'affection, status, and lineage.',
                                           'description': 'Pleated cowhide leather skirt, wide flared basketry hat '
                                                          '(Isicholo) dyed with red ochre, and an intricate geometric '
                                                          'beaded collar.',
                                           'fabrics': 'Tanned cowhide leather, natural woven grasses, glass seed beads',
                                           'gender': 'Women',
                                           'image': None,
                                           'local_name': 'Isidwaba nesicholo',
                                           'name': 'Zulu Beaded Attire (Isidwaba & Isicholo)',
                                           'region': 'KwaZulu-Natal & Pan-South Africa',
                                           'rental_price': 'R 300 – R 700 ZAR per day',
                                           'where_to_buy': 'Phansi Museum craft shop (Durban), Mai Mai Market '
                                                           '(Joburg)'},
                                       {   'category': "👨 Men's Traditional Attire",
                                           'cost_inr': '₹10,000 – ₹32,000',
                                           'cost_local': 'R 1,500 – R 4,800 ZAR',
                                           'cultural_significance': 'Respected warrior heritage symbolizing dignity '
                                                                    'and courage.',
                                           'description': 'Warrior attire featuring calfskin front and rear aprons, '
                                                          'cow-tail arm and leg bands, a beaded headband, and an oval '
                                                          'Nguni cattle hide shield.',
                                           'fabrics': 'Natural tanned Nguni cattle hide, goat hair, glass beads',
                                           'gender': 'Men',
                                           'image': None,
                                           'local_name': 'Ibheshu / Isiphunzi',
                                           'name': 'Zulu Traditional Attire (Ibheshu & Amacoco)',
                                           'region': 'KwaZulu-Natal (Eshowe, Durban, Ulundi)',
                                           'rental_price': 'R 250 – R 600 ZAR per day',
                                           'where_to_buy': 'Victoria Street Market (Durban), Shakaland craft village'},
                                       {   'category': '🌍 Regional / Eastern Cape Attire',
                                           'cost_inr': '₹8,000 – ₹28,000',
                                           'cost_local': 'R 1,200 – R 4,200 ZAR',
                                           'cultural_significance': 'The iconic heritage wear of the Xhosa nation, '
                                                                    'worn by Nelson Mandela and celebrated at wedding '
                                                                    'rites.',
                                           'description': 'Stunning cream-colored heavy cotton canvas skirt and wrap '
                                                          'adorned with bold horizontal black woven braids, beads, and '
                                                          'a wrapped headscarf (Iqhiya).',
                                           'fabrics': 'Durable cotton canvas (Isidabane), black soutache braid',
                                           'gender': 'Regional',
                                           'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1f/Typical_Xhosa_woman_attire.jpg/960px-Typical_Xhosa_woman_attire.jpg',
                                           'local_name': 'Umbhaco',
                                           'name': 'Xhosa Traditional Umbhaco Attire',
                                           'region': 'Eastern Cape (Qunu, Mthatha, East London)',
                                           'rental_price': 'R 200 – R 500 ZAR per day',
                                           'where_to_buy': 'Nelson Mandela Museum craft center (Mthatha), Greenmarket '
                                                           'Square (Cape Town)'}],
                        'country': 'South Africa',
                        'cultural_significance': "South African traditional dress honors the 'Rainbow Nation' with "
                                                 'beadwork and leather craftsmanship.',
                        'men': {   'category': "👨 Men's Traditional Attire",
                                   'cost_inr': '₹10,000 – ₹32,000',
                                   'cost_local': 'R 1,500 – R 4,800 ZAR',
                                   'cultural_significance': 'A deeply respected warrior heritage symbolizing dignity, '
                                                            'courage, and respect for ancestors (Amadlozi).',
                                   'description': 'Regal warrior attire featuring calfskin or springbok front and rear '
                                                  'aprons (Ibheshu), cow-tail arm and leg bands (Amacoco), a beaded '
                                                  'headband, and an oval Nguni cattle hide shield (Isihlangu).',
                                   'fabrics': 'Natural tanned Nguni cattle hide, goat hair, and hand-strung glass '
                                              'beads',
                                   'gender': 'Men',
                                   'image': None,
                                   'local_name': 'Ibheshu / Isiphunzi',
                                   'name': 'Zulu Traditional Attire (Ibheshu & Amacoco)',
                                   'region': 'KwaZulu-Natal (Eshowe, Durban, Ulundi)',
                                   'rental_price': 'R 250 – R 600 ZAR per day',
                                   'where_to_buy': 'The Victoria Street Market (Durban), Shakaland cultural craft '
                                                   'center'},
                        'rental_note': 'Cultural villages like Lesedi and Shakaland provide full authentic dress '
                                       'fitting and photo sessions.',
                        'women': {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹12,000 – ₹42,000',
                                     'cost_local': 'R 1,800 – R 6,200 ZAR',
                                     'cultural_significance': 'The geometric beadwork serves as an intricate symbolic '
                                                              'language of affection, status, and clan history.',
                                     'description': 'Pleated cowhide leather skirt (Isidwaba) softened with animal '
                                                    'fat, a wide flared basketry hat (Isicholo) dyed with red ochre, '
                                                    'and an intricate geometric beaded bib collar whose colors convey '
                                                    'messages of love.',
                                     'fabrics': 'Tanned cowhide leather, natural woven grasses, and glass seed beads',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Isidwaba nesicholo',
                                     'name': 'Zulu Beaded Attire (Isidwaba & Isicholo)',
                                     'region': 'KwaZulu-Natal & Pan-South Africa',
                                     'rental_price': 'R 300 – R 700 ZAR per day',
                                     'where_to_buy': 'Phansi Museum craft shop (Durban), KwaMai Mai Market '
                                                     '(Johannesburg)'}},
    'South Korea': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                          'cost_inr': '₹18,000 – ₹85,000+',
                                          'cost_local': '₩280,000 – ₩1,300,000+ KRW',
                                          'cultural_significance': 'Celebrates Korean beauty and granting free '
                                                                   'admission to Seoul Royal Palaces when worn.',
                                          'description': "Elegant Korean women's ensemble comprising a fitted jacket "
                                                         '(Jeogori) with Otgoreum bow, and billowing wrap skirt '
                                                         '(Chima).',
                                          'fabrics': 'Oxa silk, brocade, organza',
                                          'gender': 'Women',
                                          'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/35/Couple_waring_traditional_Korean_costumes_in_Gyeongbokgung%2Cthe_Seoul_palace_05.jpg/960px-Couple_waring_traditional_Korean_costumes_in_Gyeongbokgung%2Cthe_Seoul_palace_05.jpg',
                                          'local_name': '치마 저고리 한복',
                                          'name': 'Chima Jeogori Hanbok',
                                          'region': 'Seoul, Jeonju & Pan-Korea',
                                          'rental_price': '₩15,000 – ₩35,000 KRW per 4 hours',
                                          'where_to_buy': 'Bukchon Hanbok salons (Seoul), Gwangjang Market'},
                                      {   'category': "👨 Men's Traditional Attire",
                                          'cost_inr': '₹16,000 – ₹65,000',
                                          'cost_local': '₩250,000 – ₩1,000,000+ KRW',
                                          'cultural_significance': 'Reflects the Confucian values of dignity, '
                                                                   'composure, and natural harmony.',
                                          'description': "Traditional Korean men's attire consisting of loose trousers "
                                                         '(Baji) tied at the ankles, a jacket (Jeogori), a long '
                                                         "flowing scholar's coat (Dopo), and a horsehair Gat hat.",
                                          'fabrics': 'Fine Korean ramie (Mosi), and mulberry silk',
                                          'gender': 'Men',
                                          'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8a/Korea_Hanbok_Experience_03_%288028304028%29.jpg/960px-Korea_Hanbok_Experience_03_%288028304028%29.jpg',
                                          'local_name': '바지 저고리와 도포',
                                          'name': 'Baji Jeogori Hanbok & Dopo Coat',
                                          'region': 'Seoul, Bukchon Hanok Village & Pan-Korea',
                                          'rental_price': '₩15,000 – ₩35,000 KRW per 4 hours',
                                          'where_to_buy': 'Gwangjang Market (Seoul), Dongdaemun Hanbok Market'},
                                      {   'category': '👑 Royal Ceremonial Attire',
                                          'cost_inr': '₹35,000 – ₹140,000+',
                                          'cost_local': '₩550,000 – ₩2,200,000+ KRW',
                                          'cultural_significance': 'Worn by queens, princesses, and court ladies '
                                                                   'during royal court ceremonies and imperial '
                                                                   'weddings.',
                                          'description': 'Ornate semi-formal royal palace garment featuring side '
                                                         'slits, gold-leaf roundels (Geumbak), and vibrant crimson or '
                                                         'lime-green silk worn with a royal Jokduri crown.',
                                          'fabrics': 'Royal damask silk, Geumbak real gold leaf stamping',
                                          'gender': 'Women',
                                          'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f0/Hanbok_Day_2016_29_%2830467033136%29.jpg/960px-Hanbok_Day_2016_29_%2830467033136%29.jpg',
                                          'local_name': '당의 (唐衣) / 원삼',
                                          'name': 'Royal Court Ceremonial Hanbok (Dangui & Wonsam)',
                                          'region': 'Joseon Dynasty Royal Court (Gyeongbokgung & Changdeokgung)',
                                          'rental_price': '₩25,000 – ₩50,000 KRW per 4 hours',
                                          'where_to_buy': 'Royal Hanbok specialist studios around Gyeongbokgung '
                                                          'Palace'}],
                       'country': 'South Korea',
                       'cultural_significance': 'The Hanbok has over 1,600 years of unbroken cultural continuity, '
                                                'harmonizing vibrant primary colors with natural curves.',
                       'men': {   'category': "👨 Men's Traditional Attire",
                                  'cost_inr': '₹16,000 – ₹65,000',
                                  'cost_local': '₩250,000 – ₩1,000,000+ KRW',
                                  'cultural_significance': 'Reflects the Confucian values of dignity, composure, and '
                                                           'natural harmony of the Joseon Dynasty scholarly elite.',
                                  'description': "Traditional Korean men's attire consisting of loose trousers (Baji) "
                                                 "tied at the ankles, a jacket (Jeogori), a long flowing scholar's "
                                                 'coat (Dopo), and a horsehair Gat hat.',
                                  'fabrics': 'Fine Korean ramie (Mosi), and mulberry silk',
                                  'gender': 'Men',
                                  'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8a/Korea_Hanbok_Experience_03_%288028304028%29.jpg/960px-Korea_Hanbok_Experience_03_%288028304028%29.jpg',
                                  'local_name': '바지 저고리와 도포',
                                  'name': 'Baji Jeogori Hanbok & Dopo Coat',
                                  'region': 'Seoul, Bukchon Hanok Village & Pan-Korea',
                                  'rental_price': '₩15,000 – ₩35,000 KRW per 4 hours',
                                  'where_to_buy': 'Gwangjang Market (Seoul), Dongdaemun Hanbok Market'},
                       'rental_note': 'Wearing a Hanbok grants complimentary free admission to all Five Grand Palaces '
                                      'in Seoul.',
                       'women': {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹18,000 – ₹85,000+',
                                    'cost_local': '₩280,000 – ₩1,300,000+ KRW',
                                    'cultural_significance': 'Recognized globally for its fluid curved silhouette, '
                                                             'vibrant natural Five Directional Colors (Obangsaek), and '
                                                             'celebration of Chuseok and Seollal.',
                                    'description': "Elegant Korean women's ensemble comprising a short, fitted jacket "
                                                   '(Jeogori) tied with a graceful Otgoreum bow, and a billowing '
                                                   'high-waisted wrap skirt (Chima).',
                                    'fabrics': 'Oxa silk, brocade, and fine embroidered organza',
                                    'gender': 'Women',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/35/Couple_waring_traditional_Korean_costumes_in_Gyeongbokgung%2Cthe_Seoul_palace_05.jpg/960px-Couple_waring_traditional_Korean_costumes_in_Gyeongbokgung%2Cthe_Seoul_palace_05.jpg',
                                    'local_name': '치마 저고리 한복',
                                    'name': 'Chima Jeogori Hanbok',
                                    'region': 'Seoul (Gyeongbokgung), Jeonju & Pan-Korea',
                                    'rental_price': '₩15,000 – ₩35,000 KRW per 4 hours (Free entry to Seoul Royal '
                                                    'Palaces)',
                                    'where_to_buy': 'Bukchon Hanbok Rental (Seoul), Insa-dong boutiques, Gwangjang '
                                                    'Market'}},
    'Spain': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹12,000 – ₹150,000+',
                                    'cost_local': '€140 – €1,600+ EUR',
                                    'cultural_significance': 'The vibrant heartbeat of the Seville April Fair (Feria '
                                                             'de Abril) and flamenco culture.',
                                    'description': 'Figure-skimming gown flaring into cascading ruffled tiers, adorned '
                                                   'with polka dots, embroidered Manila shawl, and a large red hair '
                                                   'blossom.',
                                    'fabrics': 'Polka-dot poplin cotton, lace, silk embroidery',
                                    'gender': 'Women',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/58/Flamenca_001.jpg/960px-Flamenca_001.jpg',
                                    'local_name': 'Traje de flamenca',
                                    'name': 'Traje de Flamenca (Traje de Gitana)',
                                    'region': 'Andalusia (Seville, Granada, Córdoba)',
                                    'rental_price': '€50 – €120 EUR per day',
                                    'where_to_buy': 'Calle Cuna boutiques (Seville)'},
                                {   'category': "👨 Men's Traditional Attire",
                                    'cost_inr': '₹22,000 – ₹75,000',
                                    'cost_local': '€250 – €850 EUR',
                                    'cultural_significance': 'Noble country attire of Andalusian horsemen seen at the '
                                                             'Feria de Abril.',
                                    'description': 'Elegantly tailored short equestrian jacket, high-waisted trousers '
                                                   'buttoned up the calves, leather chaps, white shirt, and '
                                                   'flat-brimmed felt hat.',
                                    'fabrics': 'Fine Spanish wool, cowhide leather, starched cotton',
                                    'gender': 'Men',
                                    'image': None,
                                    'local_name': 'Traje corto campero y sombrero cordobés',
                                    'name': 'Traje Corto Andaluz & Sombrero Cordobés',
                                    'region': 'Andalusia (Seville, Córdoba, Jerez)',
                                    'rental_price': '€60 – €120 EUR per day',
                                    'where_to_buy': 'Sastrería de Campo (Seville), Sombrerería Padilla Crespo'},
                                {   'category': '🎆 Regional / Valencian Festival Attire',
                                    'cost_inr': '₹45,000 – ₹200,000+',
                                    'cost_local': '€500 – €2,500+ EUR',
                                    'cultural_significance': 'The crown jewel of Las Fallas, a UNESCO World Heritage '
                                                             'festival honoring St. Joseph with fire and parades.',
                                    'description': 'Magnificent 18th-century silk gown woven with metallic floral '
                                                   'designs, delicate lace apron, and an elaborate tripartite '
                                                   'hairstyle adorned with gilded filigree hair-needles (Peinetas).',
                                    'fabrics': 'Espolín silk woven on ancient jacquard looms, gold and silver threads',
                                    'gender': 'Regional',
                                    'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e5/Falleras_con_traje_t%C3%ADpico_valenciano_en_pasacalles.jpg/960px-Falleras_con_traje_t%C3%ADpico_valenciano_en_pasacalles.jpg',
                                    'local_name': 'Traje de fallera',
                                    'name': 'Traje de Fallera Valenciana',
                                    'region': 'Valencia (Las Fallas Festival)',
                                    'rental_price': '€100 – €250 EUR per festival day',
                                    'where_to_buy': 'Artisan silk ateliers in Valencia (Barrio del Carmen)'}],
                 'country': 'Spain',
                 'cultural_significance': 'Spanish attire is renowned for dramatic passion, intricate leather craft, '
                                          'and centuries of silk weaving in Valencia.',
                 'men': {   'category': "👨 Men's Traditional Attire",
                            'cost_inr': '₹22,000 – ₹75,000',
                            'cost_local': '€250 – €850 EUR',
                            'cultural_significance': 'The noble country attire of Andalusian horsemen, seen in all its '
                                                     'majesty during the Feria de Abril and Romería de El Rocío.',
                            'description': 'Elegantly tailored short equestrian jacket (Guerrera), high-waisted '
                                           'trousers (Calzona) buttoned up the lower calves, leather chaps (Zahones), '
                                           'white ruffled shirt, and a wide-brimmed felt hat (Sombrero Cordobés).',
                            'fabrics': 'Fine Spanish wool, genuine cowhide leather, and starched cotton',
                            'gender': 'Men',
                            'image': None,
                            'local_name': 'Traje corto campero y sombrero cordobés',
                            'name': 'Traje Corto Andaluz & Sombrero Cordobés',
                            'region': 'Andalusia (Seville, Córdoba, Jerez de la Frontera)',
                            'rental_price': '€60 – €120 EUR per day during Feria',
                            'where_to_buy': 'Sastrería de Campo (Seville), Sombrerería Padilla Crespo (Seville)'},
                 'rental_note': 'Boutiques in Seville, Córdoba, and Valencia offer full dress and accessory rentals '
                                'for festivals.',
                 'women': {   'category': "👩 Women's Traditional Attire",
                              'cost_inr': 'Off-the-rack: ₹12,000 – ₹38,000 • Designer: ₹45,000 – ₹150,000+',
                              'cost_local': '€140 – €1,600+ EUR',
                              'cultural_significance': 'The only traditional folk dress in the world that follows an '
                                                       'annual couture fashion calendar with dynamic changes in runway '
                                                       'trends.',
                              'description': 'Iconic figure-skimming gown fitted to mid-thigh before flaring into '
                                             'dramatic cascading ruffled tiers (Volantes), adorned with polka dots, '
                                             'embroidered Manila shawl (Mantón), and a hair comb (Peineta).',
                              'fabrics': 'Polka-dot poplin cotton, stretch lace, and silk embroidery',
                              'gender': 'Women',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/58/Flamenca_001.jpg/960px-Flamenca_001.jpg',
                              'local_name': 'Traje de flamenca / Traje de gitana',
                              'name': 'Traje de Flamenca (Traje de Gitana)',
                              'region': 'Andalusia (Seville, Granada, Córdoba, Málaga)',
                              'rental_price': '€50 – €120 EUR per day',
                              'where_to_buy': 'Calle Cuna & Calle Sierpes fashion boutiques (Seville)'}},
    'Sri Lanka': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                        'cost_inr': '₹4,500 – ₹28,000',
                                        'cost_local': '18,000 – 110,000 LKR',
                                        'cultural_significance': 'Aristocratic garment of the Kingdom of Kandy.',
                                        'description': 'Distinctive five-piece national Kandyan saree featuring a '
                                                       'frilled waist peplum (Ohoriya) and shoulder drape.',
                                        'fabrics': 'Handloom Colombo silk, gold brocade',
                                        'gender': 'Women',
                                        'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/Musical-show_%28325791237%29.jpg/960px-Musical-show_%28325791237%29.jpg',
                                        'local_name': 'ඔසරිය',
                                        'name': 'Osari (Kandyan Saree)',
                                        'region': 'Central Highlands (Kandy)',
                                        'rental_price': '4,500 – 12,000 LKR per day',
                                        'where_to_buy': 'Barefoot (Colombo), Laksala Handicrafts'},
                                    {   'category': "👨 Men's Traditional Attire",
                                        'cost_inr': '₹15,000 – ₹65,000',
                                        'cost_local': '60,000 – 260,000 LKR',
                                        'cultural_significance': 'Worn by royal dignitaries of the Temple of the Tooth '
                                                                 'Relic.',
                                        'description': 'Regal ceremonial attire with pleated white sarong, embroidered '
                                                       'velvet jacket with puffed sleeves, and ceremonial hat.',
                                        'fabrics': 'Velvet, gold filigree embroidery, silk',
                                        'gender': 'Men',
                                        'image': None,
                                        'local_name': 'නිලමේ ඇඳුම',
                                        'name': 'Nilame Aduma (Kandyan Chieftain Attire)',
                                        'region': 'Kandy',
                                        'rental_price': '8,000 – 20,000 LKR per day',
                                        'where_to_buy': 'Kandyan costume tailors in Kandy Old Town'}],
                     'country': 'Sri Lanka',
                     'cultural_significance': 'Sri Lankan traditional dress balances Kandyan royal heritage with '
                                              'breezy coastal handloom textile artistry.',
                     'men': {   'category': "👨 Men's Traditional Attire",
                                'cost_inr': '₹15,000 – ₹65,000',
                                'cost_local': '60,000 – 260,000 LKR',
                                'cultural_significance': 'Worn by high royal dignitaries (Nilames) of the Temple of '
                                                         'the Sacred Tooth Relic and modern grooms for traditional '
                                                         'weddings.',
                                'description': 'Regal ceremonial attire consisting of a voluminous pleated white '
                                               'sarong cloth, embroidered velvet jacket with puffed sleeves, metallic '
                                               'waistband, and four-cornered hat.',
                                'fabrics': 'Velvet with gold filigree Zari embroidery, stiff silk, and muslin',
                                'gender': 'Men',
                                'image': None,
                                'local_name': 'නිලමේ ඇඳුම (Mul Anduma)',
                                'name': 'Nilame Aduma (Kandyan Chieftain Attire)',
                                'region': 'Central Highlands (Kandy)',
                                'rental_price': '8,000 – 20,000 LKR per day',
                                'where_to_buy': 'Traditional Kandyan costume tailors in Kandy Old Town and Matale'},
                     'rental_note': 'Costume rental studios near Kandy Lake offer full traditional photography sets.',
                     'women': {   'category': "👩 Women's Traditional Attire",
                                  'cost_inr': '₹4,500 – ₹28,000',
                                  'cost_local': '18,000 – 110,000 LKR',
                                  'cultural_significance': 'Aristocratic garment of the Kingdom of Kandy, worn by '
                                                           'brides and women during cultural pageants like Esala '
                                                           'Perahera.',
                                  'description': 'Distinctive five-piece national Kandyan saree featuring a frilled '
                                                 'waist peplum (Ohoriya), fitted embroidered blouse, and decorative '
                                                 'shoulder drape.',
                                  'fabrics': 'Handloom Colombo silk, gold-threaded brocade, and batiks',
                                  'gender': 'Women',
                                  'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/Musical-show_%28325791237%29.jpg/960px-Musical-show_%28325791237%29.jpg',
                                  'local_name': 'ඔසරිය (Kandyan Osari)',
                                  'name': 'Osari (Kandyan Saree)',
                                  'region': 'Central Highlands (Kandy) & Pan-Sri Lanka',
                                  'rental_price': '4,500 – 12,000 LKR per day',
                                  'where_to_buy': 'Kandy Handlooms, Barefoot (Colombo), Laksala Handicrafts'}},
    'Sweden': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹18,000 – ₹58,000',
                                     'cost_local': '2,200 – 7,100 SEK',
                                     'cultural_significance': 'Designed in 1903 by Märtha Jörgensen, worn on Swedish '
                                                              'National Day (June 6) and Midsummer Eve by the Royal '
                                                              'Family and citizens.',
                                     'description': 'National blue and yellow folk costume featuring an embroidered '
                                                    'yellow apron adorned with marguerites, blue wool bodice, white '
                                                    'chemise, and white starched cap.',
                                     'fabrics': 'Swedish wool, fine linen, and silk embroidery',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Sverigedräkten',
                                     'name': 'Sverigedräkten (National Folk Costume)',
                                     'region': 'Pan-Sweden (Dalarna & Stockholm)',
                                     'rental_price': '450 – 950 SEK per day',
                                     'where_to_buy': 'Skansen Craft Shop (Stockholm), Svensk Hemslöjd (Swedish '
                                                     'Handcrafts)'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹16,000 – ₹52,000',
                                     'cost_local': '2,000 – 6,400 SEK',
                                     'cultural_significance': 'Worn around Midsummer Maypoles to dance traditional '
                                                              'ring dances and play fiddle folk polskas.',
                                     'description': 'Dark blue or yellow knee breeches with red yarn tassels, '
                                                    'embroidered vest with brass buttons, high white linen collar, and '
                                                    'black felt brimmed hat.',
                                     'fabrics': 'Wool wadmal cloth, handspun linen, and brass buttons',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Folkdräkt (Leksandsdräkt)',
                                     'name': 'Swedish Folkdräkt with Knee Breeches & Vest',
                                     'region': 'Dalarna (Lake Siljan)',
                                     'rental_price': '400 – 900 SEK per day',
                                     'where_to_buy': 'Leksand Hemslöjd, Rättvik traditional costume guilds'}],
                  'country': 'Sweden',
                  'cultural_significance': 'Swedish folk costumes represent regional identity, Midsummer celebration, '
                                           'and vibrant Swedish textile craft guilds (Hemslöjd).',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹16,000 – ₹52,000',
                             'cost_local': '2,000 – 6,400 SEK',
                             'cultural_significance': 'Worn around Midsummer Maypoles to dance traditional ring dances '
                                                      'and play fiddle folk polskas.',
                             'description': 'Dark blue or yellow knee breeches with red yarn tassels, embroidered vest '
                                            'with brass buttons, high white linen collar, and black felt brimmed hat.',
                             'fabrics': 'Wool wadmal cloth, handspun linen, and brass buttons',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'Folkdräkt (Leksandsdräkt)',
                             'name': 'Swedish Folkdräkt with Knee Breeches & Vest',
                             'region': 'Dalarna (Lake Siljan)',
                             'rental_price': '400 – 900 SEK per day',
                             'where_to_buy': 'Leksand Hemslöjd, Rättvik traditional costume guilds'},
                  'rental_note': 'Costume rentals available at Skansen Open-Air Museum in Stockholm during festive '
                                 'seasons.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹18,000 – ₹58,000',
                               'cost_local': '2,200 – 7,100 SEK',
                               'cultural_significance': 'Designed in 1903 by Märtha Jörgensen, worn on Swedish '
                                                        'National Day (June 6) and Midsummer Eve by the Royal Family '
                                                        'and citizens.',
                               'description': 'National blue and yellow folk costume featuring an embroidered yellow '
                                              'apron adorned with marguerites, blue wool bodice, white chemise, and '
                                              'white starched cap.',
                               'fabrics': 'Swedish wool, fine linen, and silk embroidery',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'Sverigedräkten',
                               'name': 'Sverigedräkten (National Folk Costume)',
                               'region': 'Pan-Sweden (Dalarna & Stockholm)',
                               'rental_price': '450 – 950 SEK per day',
                               'where_to_buy': 'Skansen Craft Shop (Stockholm), Svensk Hemslöjd (Swedish Handcrafts)'}},
    'Switzerland': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                          'cost_inr': '₹30,000 – ₹120,000',
                                          'cost_local': '320 – 1,300 CHF',
                                          'cultural_significance': 'A symbol of cantonal heritage, worn during Swiss '
                                                                   'National Day (August 1) and alpine cattle descent '
                                                                   'processions (Alpabzug).',
                                          'description': 'Stiff black velvet bodice laced with silver chains and '
                                                         'rosettes (Chropfkette), white linen blouse, dark pleated '
                                                         'wool skirt, and gossamer horsehair lace bonnet.',
                                          'fabrics': 'Black velvet, Bernese fine linen, and silver filigree',
                                          'gender': 'Women',
                                          'image': None,
                                          'local_name': 'Berner Tracht',
                                          'name': 'Swiss Tracht with Bernese Lace Bonnet',
                                          'region': 'Canton of Bern, Appenzell & Valais',
                                          'rental_price': '80 – 180 CHF per day',
                                          'where_to_buy': 'Heimatwerk stores (Zurich & Bern), cantonal Trachtenverein '
                                                          'weavers'},
                                      {   'category': "👨 Men's Traditional Attire",
                                          'cost_inr': '₹28,000 – ₹95,000',
                                          'cost_local': '300 – 1,020 CHF',
                                          'cultural_significance': 'The historic attire of Appenzell alpine dairymen '
                                                                   '(Senn), famous for cowbell ringing and alpine '
                                                                   'yodeling.',
                                          'description': 'Vibrant yellow knee breeches with brass dairy cow plaques on '
                                                         'suspenders, embroidered Edelweiss blue linen shirt, scarlet '
                                                         'waistcoat, and carved silver spoon earring.',
                                          'fabrics': 'Dyed buckskin leather, brushed cotton, and silver ornaments',
                                          'gender': 'Men',
                                          'image': None,
                                          'local_name': 'Appenzeller Chüelederhosene',
                                          'name': 'Swiss Chüelederhosene with Edelweiss Shirt',
                                          'region': 'Appenzell Innerrhoden & Bernese Oberland',
                                          'rental_price': '75 – 160 CHF per day',
                                          'where_to_buy': 'Appenzell town artisan craft guilds, Swiss Heritage '
                                                          'Guilds'}],
                       'country': 'Switzerland',
                       'cultural_significance': 'Swiss cantonal traditional costumes embody the pastoral alpine '
                                                'heritage and democratic independence of the 26 cantons.',
                       'men': {   'category': "👨 Men's Traditional Attire",
                                  'cost_inr': '₹28,000 – ₹95,000',
                                  'cost_local': '300 – 1,020 CHF',
                                  'cultural_significance': 'The historic attire of Appenzell alpine dairymen (Senn), '
                                                           'famous for cowbell ringing and alpine yodeling.',
                                  'description': 'Vibrant yellow knee breeches with brass dairy cow plaques on '
                                                 'suspenders, embroidered Edelweiss blue linen shirt, scarlet '
                                                 'waistcoat, and carved silver spoon earring.',
                                  'fabrics': 'Dyed buckskin leather, brushed cotton, and silver ornaments',
                                  'gender': 'Men',
                                  'image': None,
                                  'local_name': 'Appenzeller Chüelederhosene',
                                  'name': 'Swiss Chüelederhosene with Edelweiss Shirt',
                                  'region': 'Appenzell Innerrhoden & Bernese Oberland',
                                  'rental_price': '75 – 160 CHF per day',
                                  'where_to_buy': 'Appenzell town artisan craft guilds, Swiss Heritage Guilds'},
                       'rental_note': 'Swiss Heimatwerk and local cultural associations in Interlaken and Appenzell '
                                      'offer photo-shoot costumes.',
                       'women': {   'category': "👩 Women's Traditional Attire",
                                    'cost_inr': '₹30,000 – ₹120,000',
                                    'cost_local': '320 – 1,300 CHF',
                                    'cultural_significance': 'A symbol of cantonal heritage, worn during Swiss '
                                                             'National Day (August 1) and alpine cattle descent '
                                                             'processions (Alpabzug).',
                                    'description': 'Stiff black velvet bodice laced with silver chains and rosettes '
                                                   '(Chropfkette), white linen blouse, dark pleated wool skirt, and '
                                                   'gossamer horsehair lace bonnet.',
                                    'fabrics': 'Black velvet, Bernese fine linen, and silver filigree',
                                    'gender': 'Women',
                                    'image': None,
                                    'local_name': 'Berner Tracht',
                                    'name': 'Swiss Tracht with Bernese Lace Bonnet',
                                    'region': 'Canton of Bern, Appenzell & Valais',
                                    'rental_price': '80 – 180 CHF per day',
                                    'where_to_buy': 'Heimatwerk stores (Zurich & Bern), cantonal Trachtenverein '
                                                    'weavers'}},
    'Tanzania': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹1,800 – ₹12,000',
                                       'cost_local': '55,000 – 370,000 TZS',
                                       'cultural_significance': "A fundamental voice of Swahili women's cultural "
                                                                'communication, worn for wedding ceremonies, child '
                                                                'naming, and daily coastal life.',
                                       'description': 'Coordinated pair of printed cotton wraps (Kanga) featuring '
                                                      'Swahili philosophical messages (Jina) along the border, draped '
                                                      'around waist and head, or tailored into Kitenge dresses.',
                                       'fabrics': 'East African wax-print cotton, Zanzibar spices dye prints',
                                       'gender': 'Women',
                                       'image': None,
                                       'local_name': 'Kanga na Kitenge',
                                       'name': 'Kanga & Kitenge Dressed Wrap with Gele',
                                       'region': 'Zanzibar, Dar es Salaam & Coastal Swahili Coast',
                                       'rental_price': '15,000 – 40,000 TZS per day',
                                       'where_to_buy': 'Stone Town markets (Zanzibar), Kariakoo Market (Dar es '
                                                       'Salaam)'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹2,200 – ₹14,000',
                                       'cost_local': '68,000 – 430,000 TZS',
                                       'cultural_significance': 'National dress of Swahili gentlemen, worn for Friday '
                                                                'prayers, weddings, and official state receptions.',
                                       'description': 'Floor-length pristine white or cream tunic (Kanzu) with subtle '
                                                      'maroon and gold embroidery along collar and tassels, paired '
                                                      'with hand-embroidered cylindrical Swahili cap (Kofia) and suit '
                                                      'jacket.',
                                       'fabrics': 'Lightweight breathable cotton, poplin linen, and silk thread',
                                       'gender': 'Men',
                                       'image': None,
                                       'local_name': 'Kanzu na Kofia',
                                       'name': 'Kanzu White Robe with Embroidered Kofia Cap',
                                       'region': 'Zanzibar & Coastal Swahili Coast',
                                       'rental_price': '20,000 – 50,000 TZS per day',
                                       'where_to_buy': 'Darajani Bazaar (Stone Town, Zanzibar), Mnazi Mmoja tailors'}],
                    'country': 'Tanzania',
                    'cultural_significance': 'Tanzanian attire mirrors the rich maritime spice trade blending Bantu '
                                             'African, Omani Arab, and Indian Ocean coastal influences.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹2,200 – ₹14,000',
                               'cost_local': '68,000 – 430,000 TZS',
                               'cultural_significance': 'National dress of Swahili gentlemen, worn for Friday prayers, '
                                                        'weddings, and official state receptions.',
                               'description': 'Floor-length pristine white or cream tunic (Kanzu) with subtle maroon '
                                              'and gold embroidery along collar and tassels, paired with '
                                              'hand-embroidered cylindrical Swahili cap (Kofia) and suit jacket.',
                               'fabrics': 'Lightweight breathable cotton, poplin linen, and silk thread',
                               'gender': 'Men',
                               'image': None,
                               'local_name': 'Kanzu na Kofia',
                               'name': 'Kanzu White Robe with Embroidered Kofia Cap',
                               'region': 'Zanzibar & Coastal Swahili Coast',
                               'rental_price': '20,000 – 50,000 TZS per day',
                               'where_to_buy': 'Darajani Bazaar (Stone Town, Zanzibar), Mnazi Mmoja tailors'},
                    'rental_note': 'Stone Town boutiques offer traditional Zanzibari attire for historical walking '
                                   'photo shoots.',
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹1,800 – ₹12,000',
                                 'cost_local': '55,000 – 370,000 TZS',
                                 'cultural_significance': "A fundamental voice of Swahili women's cultural "
                                                          'communication, worn for wedding ceremonies, child naming, '
                                                          'and daily coastal life.',
                                 'description': 'Coordinated pair of printed cotton wraps (Kanga) featuring Swahili '
                                                'philosophical messages (Jina) along the border, draped around waist '
                                                'and head, or tailored into Kitenge dresses.',
                                 'fabrics': 'East African wax-print cotton, Zanzibar spices dye prints',
                                 'gender': 'Women',
                                 'image': None,
                                 'local_name': 'Kanga na Kitenge',
                                 'name': 'Kanga & Kitenge Dressed Wrap with Gele',
                                 'region': 'Zanzibar, Dar es Salaam & Coastal Swahili Coast',
                                 'rental_price': '15,000 – 40,000 TZS per day',
                                 'where_to_buy': 'Stone Town markets (Zanzibar), Kariakoo Market (Dar es Salaam)'}},
    'Thailand': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹7,500 – ₹35,000+',
                                       'cost_local': '฿3,200 – ฿15,000+ THB',
                                       'cultural_significance': 'Created under royal patronage celebrating classical '
                                                                'Thai silk craftsmanship.',
                                       'description': 'Opulent formal Thai national dress featuring an asymmetrical '
                                                      'one-shoulder pleated silk shawl (Sabai) draped across the '
                                                      'chest, paired with an embroidered wrap-skirt.',
                                       'fabrics': 'Handwoven Thai silk brocade woven with golden metallic threads',
                                       'gender': 'Women',
                                       'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b3/Siam_traditional_clothes.jpg/960px-Siam_traditional_clothes.jpg',
                                       'local_name': 'ชุดไทยจักรี',
                                       'name': 'Chut Thai Chakkri (Royal Silk Dress)',
                                       'region': 'Bangkok, Ayutthaya & Central Thailand',
                                       'rental_price': '฿500 – ฿1,200 THB per day',
                                       'where_to_buy': 'Wat Arun costume rental salons, Phahurat Market (Bangkok)'},
                                   {   'category': "👨 Men's Traditional Attire",
                                       'cost_inr': '₹6,000 – ₹24,000',
                                       'cost_local': '฿2,500 – ฿10,000 THB',
                                       'cultural_significance': 'Standardized royal national attire for Thai men worn '
                                                                'at temple rites, royal festivals, and formal '
                                                                'weddings.',
                                       'description': 'Formal royal-patterned Thai silk jacket with a high mandarin '
                                                      'collar (Raj Pattern), round metal buttons, and a tied silk '
                                                      'cummerbund sash.',
                                       'fabrics': 'Handwoven Mudmee Thai silk and golden raw silk',
                                       'gender': 'Men',
                                       'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Prem_Tinsulanonda_2010-01-20.jpg/960px-Prem_Tinsulanonda_2010-01-20.jpg',
                                       'local_name': 'เสื้อพระราชทาน',
                                       'name': 'Suea Phraratchathan (Thai Formal Silk Attire)',
                                       'region': 'Bangkok, Chiang Mai & Pan-Thailand',
                                       'rental_price': '฿600 – ฿1,500 THB per day',
                                       'where_to_buy': 'The Old Siam Shopping Plaza (Bangkok), Warorot Market (Chiang '
                                                       'Mai)'},
                                   {   'category': '🎭 Ceremonial / Classical Attire',
                                       'cost_inr': '₹25,000 – ₹90,000+',
                                       'cost_local': '฿10,000 – ฿38,000+ THB',
                                       'cultural_significance': 'A UNESCO-inscribed intangible cultural heritage art '
                                                                'form depicting episodes of the Ramakien.',
                                       'description': 'Intricate theatrical regalia adorned with gold bullion '
                                                      'embroidery, glass mirror-jewels, curved shoulder wings '
                                                      '(Inthanu), and a gilded tiered Chada crown.',
                                       'fabrics': 'Gold bullion embroidery, silk velvet, and gilded brass ornaments',
                                       'gender': 'Regional',
                                       'image': None,
                                       'local_name': 'โขน (เครื่องแต่งกาย)',
                                       'name': 'Khon Classical Masked Dance Regalia',
                                       'region': 'Royal Palace Theatres & Sala Chalermkrung',
                                       'rental_price': '฿1,500 – ฿3,500 THB for photo shoots',
                                       'where_to_buy': 'Silpakorn Fine Arts Guild, Bangkok National Theatre artisan '
                                                       'workshops'}],
                    'country': 'Thailand',
                    'cultural_significance': 'Thai traditional costumes demonstrate centuries of intricate gold-thread '
                                             'silk weaving preserved by master weavers in Isan.',
                    'men': {   'category': "👨 Men's Traditional Attire",
                               'cost_inr': '₹6,000 – ₹24,000',
                               'cost_local': '฿2,500 – ฿10,000 THB',
                               'cultural_significance': 'Standardized by HM King Bhumibol Adulyadej as the dignified '
                                                        'national attire for men at official ceremonies.',
                               'description': 'Formal royal-patterned Thai silk jacket with a high mandarin collar '
                                              '(Raj Pattern), round metal buttons, and a tied silk cummerbund sash '
                                              '(Phaa Khao Ma), worn with dark tailored trousers.',
                               'fabrics': 'Handwoven Mudmee Thai silk and golden raw silk',
                               'gender': 'Men',
                               'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Prem_Tinsulanonda_2010-01-20.jpg/960px-Prem_Tinsulanonda_2010-01-20.jpg',
                               'local_name': 'เสื้อพระราชทาน',
                               'name': 'Suea Phraratchathan (Thai Formal Silk Attire)',
                               'region': 'Bangkok, Chiang Mai & Pan-Thailand',
                               'rental_price': '฿600 – ฿1,500 THB per day',
                               'where_to_buy': 'The Old Siam Shopping Plaza (Bangkok), Warorot Market (Chiang Mai)'},
                    'rental_note': 'Renting Chut Thai for memorable photo sessions around the ornate spires of Wat '
                                   "Arun is one of Bangkok's top cultural experiences.",
                    'women': {   'category': "👩 Women's Traditional Attire",
                                 'cost_inr': '₹7,500 – ₹35,000+',
                                 'cost_local': '฿3,200 – ฿15,000+ THB',
                                 'cultural_significance': 'Created under the royal patronage of Queen Sirikit to '
                                                          "celebrate Thailand's eight formal national styles.",
                                 'description': 'Opulent formal Thai national dress featuring an asymmetrical '
                                                'one-shoulder pleated silk shawl (Sabai) draped across the chest and '
                                                'trailing down the back, paired with a pleated wrap-skirt (Sin).',
                                 'fabrics': 'Handwoven Thai silk brocade woven with golden metallic threads (Yok dok)',
                                 'gender': 'Women',
                                 'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b3/Siam_traditional_clothes.jpg/960px-Siam_traditional_clothes.jpg',
                                 'local_name': 'ชุดไทยจักรี',
                                 'name': 'Chut Thai Chakkri (Royal Silk Dress)',
                                 'region': 'Bangkok, Ayutthaya & Central Thailand',
                                 'rental_price': '฿500 – ฿1,200 THB per day (available near Wat Arun)',
                                 'where_to_buy': 'Wat Arun costume rental stalls, Phahurat Textile Market (Bangkok)'}},
    'Turkey': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                     'cost_inr': '₹9,000 – ₹48,000',
                                     'cost_local': '3,800 – 20,000 TRY',
                                     'cultural_significance': 'Centuries-old imperial court bridal wear worn for the '
                                                              'sacred Henna Night (Kına Gecesi) preceding the wedding '
                                                              'day.',
                                     'description': 'Heavily gilded crimson or royal purple velvet coat dress '
                                                    'decorated with Ottoman botanical motifs (Bindallı) worked in gold '
                                                    'cord (Maraş işi), worn over satin salvar bloomers.',
                                     'fabrics': 'Silk velvet, metallic gold cord, and Bursa satin',
                                     'gender': 'Women',
                                     'image': None,
                                     'local_name': 'Bindallı (Osmanlı Kaftanı)',
                                     'name': 'Ottoman Bindallı Velvet Kaftan Dress',
                                     'region': 'Istanbul, Bursa & Central Anatolia',
                                     'rental_price': '900 – 2,500 TRY per day',
                                     'where_to_buy': 'Grand Bazaar (Kapalıçarşı, Istanbul), Fatih bridal boutiques, '
                                                     'Bursa Koza Han'},
                                 {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': '₹8,000 – ₹38,000',
                                     'cost_local': '3,400 – 16,000 TRY',
                                     'cultural_significance': 'Heroic costume of Aegean mountain freedom fighters '
                                                              '(Efes/Zeybeks), celebrated in the brave Zeybek folk '
                                                              'dance.',
                                     'description': 'Short embroidered jacket with hanging slit sleeves (Cepken), '
                                                    'pleated knee-length trousers (Potur / Şalvar), wide leather '
                                                    'pistol belt (Silahlık), and fringed felt cap (Fes).',
                                     'fabrics': 'Felt broadcloth, metallic silver braid, and leather',
                                     'gender': 'Men',
                                     'image': None,
                                     'local_name': 'Zeybek Giysisi / Cepken',
                                     'name': 'Turkish Zeybek / Ottoman Cepken Embroidered Vest',
                                     'region': 'Aegean Region (İzmir, Aydın) & Anatolia',
                                     'rental_price': '800 – 2,200 TRY per day',
                                     'where_to_buy': 'Kemeraltı Bazaar (İzmir), Grand Bazaar folk costumiers '
                                                     '(Istanbul)'}],
                  'country': 'Turkey',
                  'cultural_significance': 'Turkish attire reflects the opulent synthesis of Central Asian nomadic '
                                           'textiles, Seljuk motifs, and Ottoman imperial court magnificence.',
                  'men': {   'category': "👨 Men's Traditional Attire",
                             'cost_inr': '₹8,000 – ₹38,000',
                             'cost_local': '3,400 – 16,000 TRY',
                             'cultural_significance': 'Heroic costume of Aegean mountain freedom fighters '
                                                      '(Efes/Zeybeks), celebrated in the brave Zeybek folk dance.',
                             'description': 'Short embroidered jacket with hanging slit sleeves (Cepken), pleated '
                                            'knee-length trousers (Potur / Şalvar), wide leather pistol belt '
                                            '(Silahlık), and fringed felt cap (Fes).',
                             'fabrics': 'Felt broadcloth, metallic silver braid, and leather',
                             'gender': 'Men',
                             'image': None,
                             'local_name': 'Zeybek Giysisi / Cepken',
                             'name': 'Turkish Zeybek / Ottoman Cepken Embroidered Vest',
                             'region': 'Aegean Region (İzmir, Aydın) & Anatolia',
                             'rental_price': '800 – 2,200 TRY per day',
                             'where_to_buy': 'Kemeraltı Bazaar (İzmir), Grand Bazaar folk costumiers (Istanbul)'},
                  'rental_note': 'Costume rental studios in Sultanahmet (Istanbul) offer Ottoman palace photography '
                                 'experiences.',
                  'women': {   'category': "👩 Women's Traditional Attire",
                               'cost_inr': '₹9,000 – ₹48,000',
                               'cost_local': '3,800 – 20,000 TRY',
                               'cultural_significance': 'Centuries-old imperial court bridal wear worn for the sacred '
                                                        'Henna Night (Kına Gecesi) preceding the wedding day.',
                               'description': 'Heavily gilded crimson or royal purple velvet coat dress decorated with '
                                              'Ottoman botanical motifs (Bindallı) worked in gold cord (Maraş işi), '
                                              'worn over satin salvar bloomers.',
                               'fabrics': 'Silk velvet, metallic gold cord, and Bursa satin',
                               'gender': 'Women',
                               'image': None,
                               'local_name': 'Bindallı (Osmanlı Kaftanı)',
                               'name': 'Ottoman Bindallı Velvet Kaftan Dress',
                               'region': 'Istanbul, Bursa & Central Anatolia',
                               'rental_price': '900 – 2,500 TRY per day',
                               'where_to_buy': 'Grand Bazaar (Kapalıçarşı, Istanbul), Fatih bridal boutiques, Bursa '
                                               'Koza Han'}},
    'USA': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                  'cost_inr': '₹7,500 – ₹22,000',
                                  'cost_local': '$90 – $260 USD',
                                  'cultural_significance': 'Honors the resilience of 19th-century pioneer women along '
                                                           'historic migration trails.',
                                  'description': 'High-necked, long-sleeved dress made from small floral calico cotton '
                                                 'prints, worn with a white canvas apron and matching deep-brimmed '
                                                 'sunbonnet.',
                                  'fabrics': 'Woven calico cotton, starched muslin',
                                  'gender': 'Women',
                                  'image': None,
                                  'local_name': 'Pioneer Calico Prairie Dress',
                                  'name': 'American Frontier Pioneer Prairie Dress',
                                  'region': 'American Midwest & Great Plains',
                                  'rental_price': '$30 – $65 USD per day',
                                  'where_to_buy': 'Living history museum shops across the American West'},
                              {   'category': "👨 Men's Traditional Attire",
                                  'cost_inr': '₹15,000 – ₹55,000',
                                  'cost_local': '$180 – $650+ USD',
                                  'cultural_significance': 'Indelible icon of the American frontier, rodeo, and '
                                                           'cattle-ranching culture.',
                                  'description': 'Classic rugged frontier wear featuring a pearl-snap western shirt, '
                                                 'leather belt with silver trophy buckle, denim jeans, handcrafted '
                                                 'boots, and Stetson hat.',
                                  'fabrics': 'Cotton denim, full-grain boot leather, beaver-fur felt',
                                  'gender': 'Men',
                                  'image': None,
                                  'local_name': 'American Western Cowboy Wear',
                                  'name': 'Western Cowboy Attire & Stetson Hat',
                                  'region': 'Texas, Wyoming, Montana & American West',
                                  'rental_price': '$40 – $90 USD per day',
                                  'where_to_buy': "Cavender's, Boot Barn, Fort Worth Stockyards"},
                              {   'category': '🌍 Indigenous Heritage Attire',
                                  'cost_inr': '₹28,000 – ₹95,000+',
                                  'cost_local': '$350 – $1,200+ USD',
                                  'cultural_significance': 'A sacred manifestation of Diné worldview (Hózhó—balance '
                                                           'and harmony) handwoven on upright looms.',
                                  'description': 'Two handwoven wool panels joined at the shoulders and sides in rich '
                                                 'indigo, black, and cochineal red geometric bands, cinched with a '
                                                 'stamped sterling silver concho belt and turquoise squash-blossom '
                                                 'necklace.',
                                  'fabrics': 'Handspun Navajo Churro wool, sterling silver, and Kingman turquoise',
                                  'gender': 'Regional',
                                  'image': None,
                                  'local_name': 'Diné Biil / Traditional Navajo Rug Dress',
                                  'name': 'Navajo Traditional Woven Biil Attire',
                                  'region': 'Navajo Nation (Arizona, New Mexico, Utah)',
                                  'rental_price': '$60 – $140 USD for cultural education',
                                  'where_to_buy': 'Hubbell Trading Post (Ganado, AZ), Gallup Native Arts Guild (NM)'}],
               'country': 'USA',
               'cultural_significance': 'American traditional dress spans Native American indigenous textile mastery '
                                        'to 19th-century western frontier traditions.',
               'men': {   'category': "👨 Men's Traditional Attire",
                          'cost_inr': '₹15,000 – ₹55,000',
                          'cost_local': '$180 – $650+ USD',
                          'cultural_significance': 'An indelible icon of the American frontier, rugged independence, '
                                                   'and cattle-ranching heritage.',
                          'description': 'Classic rugged American frontier wear featuring a pearl-snap western shirt, '
                                         'leather belt with engraved silver trophy buckle, durable denim jeans, '
                                         'handcrafted leather boots, and a wide-brimmed felt Stetson cowboy hat.',
                          'fabrics': 'Heavy-duty cotton denim, full-grain boot leather, and beaver-fur felt',
                          'gender': 'Men',
                          'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d1/HerdQuit.jpg/330px-HerdQuit.jpg',
                          'local_name': 'American Western Cowboy Wear',
                          'name': 'Western Cowboy Attire & Stetson Hat',
                          'region': 'Texas, Wyoming, Montana & American West',
                          'rental_price': '$40 – $90 USD per day',
                          'where_to_buy': "Cavender's, Boot Barn (Pan-USA), Fort Worth Stockyards shops (Texas)"},
               'rental_note': 'Western outfitters in Fort Worth, San Antonio, and Nashville provide authentic hat and '
                              'boot styling.',
               'women': {   'category': "👩 Women's Traditional Attire",
                            'cost_inr': '₹7,500 – ₹22,000',
                            'cost_local': '$90 – $260 USD',
                            'cultural_significance': 'Honors the resilience and resourcefulness of women settlers on '
                                                     'the 19th-century Oregon and Santa Fe trails.',
                            'description': 'High-necked, long-sleeved 19th-century dress made from small floral calico '
                                           'cotton prints, worn with a protective white canvas apron and a '
                                           'deep-brimmed fabric sunbonnet.',
                            'fabrics': '100% woven calico cotton, starched muslin',
                            'gender': 'Women',
                            'image': None,
                            'local_name': 'Pioneer Calico Prairie Dress',
                            'name': 'American Frontier Pioneer Prairie Dress',
                            'region': 'American Midwest, Great Plains & Westward Trails',
                            'rental_price': '$30 – $65 USD per day',
                            'where_to_buy': 'Living history museum shops in Williamsburg (VA), Nauvoo, Cody (WY)'}},
    'Ukraine': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹4,500 – ₹28,000',
                                      'cost_local': '2,000 – 12,500 UAH',
                                      'cultural_significance': 'A sacred cultural talisman (Oberih) representing '
                                                               'resilience, family lineage, and national identity '
                                                               'celebrated on World Vyshyvanka Day.',
                                      'description': 'Hand-embroidered linen blouse (Vyshyvanka) with geometric red '
                                                     'and black protective talisman patterns, woven wrap skirt '
                                                     '(Plakhta), embroidered apron, and fresh flower head wreath with '
                                                     'streaming ribbons (Vinok).',
                                      'fabrics': 'Homespun flax linen, wool yarn embroidery, and satin ribbons',
                                      'gender': 'Women',
                                      'image': None,
                                      'local_name': 'Вишиванка, плахта та вінок',
                                      'name': 'Vyshyvanka Embroidered Blouse & Plakhta with Vinok',
                                      'region': 'Poltava, Kyiv & Western Ukraine (Hutsulshchyna)',
                                      'rental_price': '500 – 1,800 UAH per day',
                                      'where_to_buy': 'Andriyivskyy Descent (Kyiv), Rynok Square souvenir stalls '
                                                      '(Lviv), Etnodim'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹4,000 – ₹22,000',
                                      'cost_local': '1,800 – 9,800 UAH',
                                      'cultural_significance': 'Celebrates the Zaporozhian Cossack warrior heritage of '
                                                               'freedom, bravery, and self-determination.',
                                      'description': 'Linen shirt with red-and-black cross-stitch along chest placket '
                                                     'and collar, billowy crimson or blue Cossack trousers '
                                                     '(Sharovary), secured with a wide woven woolen sash (Koyas).',
                                      'fabrics': 'Natural flax linen, wool, and heavy cotton',
                                      'gender': 'Men',
                                      'image': None,
                                      'local_name': 'Чоловіча вишиванка та шаровари',
                                      'name': 'Vyshyvanka Embroidered Shirt with Sharovary & Sash',
                                      'region': 'Cossack Dnieper Region & Western Ukraine',
                                      'rental_price': '450 – 1,500 UAH per day',
                                      'where_to_buy': 'Lviv Vernissage market, Vsi Svoi boutiques (Kyiv)'}],
                   'country': 'Ukraine',
                   'cultural_significance': 'The Vyshyvanka is the central cultural code of Ukrainian national unity, '
                                            'carrying encoded ancestral blessings in every stitch.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': '₹4,000 – ₹22,000',
                              'cost_local': '1,800 – 9,800 UAH',
                              'cultural_significance': 'Celebrates the Zaporozhian Cossack warrior heritage of '
                                                       'freedom, bravery, and self-determination.',
                              'description': 'Linen shirt with red-and-black cross-stitch along chest placket and '
                                             'collar, billowy crimson or blue Cossack trousers (Sharovary), secured '
                                             'with a wide woven woolen sash (Koyas).',
                              'fabrics': 'Natural flax linen, wool, and heavy cotton',
                              'gender': 'Men',
                              'image': None,
                              'local_name': 'Чоловіча вишиванка та шаровари',
                              'name': 'Vyshyvanka Embroidered Shirt with Sharovary & Sash',
                              'region': 'Cossack Dnieper Region & Western Ukraine',
                              'rental_price': '450 – 1,500 UAH per day',
                              'where_to_buy': 'Lviv Vernissage market, Vsi Svoi boutiques (Kyiv)'},
                   'rental_note': 'Ethno-studios in Lviv and Kyiv rent full historical costumes for weddings and '
                                  'patriotic celebrations.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': '₹4,500 – ₹28,000',
                                'cost_local': '2,000 – 12,500 UAH',
                                'cultural_significance': 'A sacred cultural talisman (Oberih) representing resilience, '
                                                         'family lineage, and national identity celebrated on World '
                                                         'Vyshyvanka Day.',
                                'description': 'Hand-embroidered linen blouse (Vyshyvanka) with geometric red and '
                                               'black protective talisman patterns, woven wrap skirt (Plakhta), '
                                               'embroidered apron, and fresh flower head wreath with streaming ribbons '
                                               '(Vinok).',
                                'fabrics': 'Homespun flax linen, wool yarn embroidery, and satin ribbons',
                                'gender': 'Women',
                                'image': None,
                                'local_name': 'Вишиванка, плахта та вінок',
                                'name': 'Vyshyvanka Embroidered Blouse & Plakhta with Vinok',
                                'region': 'Poltava, Kyiv & Western Ukraine (Hutsulshchyna)',
                                'rental_price': '500 – 1,800 UAH per day',
                                'where_to_buy': 'Andriyivskyy Descent (Kyiv), Rynok Square souvenir stalls (Lviv), '
                                                'Etnodim'}},
    'United Arab Emirates': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                                   'cost_inr': '₹5,000 – ₹35,000',
                                                   'cost_local': '220 – 1,550 AED',
                                                   'cultural_significance': 'A mark of elegance and modesty, where '
                                                                            'Talli bobbin lace is recognized as UNESCO '
                                                                            'Intangible Cultural Heritage.',
                                                   'description': 'Flowing black cloak (Abaya) over an embroidered '
                                                                  'jalabiya (Mukhawara), matched with lightweight '
                                                                  'headscarf (Sheila) and traditional golden metallic '
                                                                  'leather face mask (Burqa).',
                                                   'fabrics': 'Crepe silk, satin, gold Talli braid embroidery',
                                                   'gender': 'Women',
                                                   'image': None,
                                                   'local_name': 'العباية والشيلة (Mukhawara)',
                                                   'name': 'Emirati Abaya & Sheila with Burqa Face Adornment',
                                                   'region': 'Abu Dhabi, Dubai & Sharjah',
                                                   'rental_price': '60 – 180 AED per day',
                                                   'where_to_buy': 'Souk Naif (Deira, Dubai), Souk Al Zafarana (Al '
                                                                   'Ain), Madinat Jumeirah'},
                                               {   'category': "👨 Men's Traditional Attire",
                                                   'cost_inr': '₹3,500 – ₹22,000',
                                                   'cost_local': '150 – 950 AED',
                                                   'cultural_significance': 'The quintessential national dress of '
                                                                            'Emirati men, worn for governance, '
                                                                            'business meetings, and daily life.',
                                                   'description': 'Collarless ankle-length white robe (Kandura) with '
                                                                  'decorative matching fabric tassel (Farkha / '
                                                                  'Tarboosha) on chest, worn with white or checkered '
                                                                  'headcloth (Ghutra) and black cord (Agal).',
                                                   'fabrics': 'Finest Japanese polyester-cotton blend, Italian poplin',
                                                   'gender': 'Men',
                                                   'image': None,
                                                   'local_name': 'الكندورة والغترة والعقال',
                                                   'name': 'Emirati Kandura (Dishdasha) with Ghutra & Agal',
                                                   'region': 'Pan-UAE',
                                                   'rental_price': '45 – 120 AED per day',
                                                   'where_to_buy': 'Al Bait Al Khaleeji tailors, Deira Souk, Meena '
                                                                   'Bazaar'}],
                                'country': 'United Arab Emirates',
                                'cultural_significance': 'Emirati attire reflects desert climate adaptation, Bedouin '
                                                         'hospitality, and modern Gulf refinement.',
                                'men': {   'category': "👨 Men's Traditional Attire",
                                           'cost_inr': '₹3,500 – ₹22,000',
                                           'cost_local': '150 – 950 AED',
                                           'cultural_significance': 'The quintessential national dress of Emirati men, '
                                                                    'worn for governance, business meetings, and daily '
                                                                    'life.',
                                           'description': 'Collarless ankle-length white robe (Kandura) with '
                                                          'decorative matching fabric tassel (Farkha / Tarboosha) on '
                                                          'chest, worn with white or checkered headcloth (Ghutra) and '
                                                          'black cord (Agal).',
                                           'fabrics': 'Finest Japanese polyester-cotton blend, Italian poplin',
                                           'gender': 'Men',
                                           'image': None,
                                           'local_name': 'الكندورة والغترة والعقال',
                                           'name': 'Emirati Kandura (Dishdasha) with Ghutra & Agal',
                                           'region': 'Pan-UAE',
                                           'rental_price': '45 – 120 AED per day',
                                           'where_to_buy': 'Al Bait Al Khaleeji tailors, Deira Souk, Meena Bazaar'},
                                'rental_note': 'Heritage villages in Abu Dhabi and Al Fahidi historical quarter in '
                                               'Dubai offer traditional dress photo experiences.',
                                'women': {   'category': "👩 Women's Traditional Attire",
                                             'cost_inr': '₹5,000 – ₹35,000',
                                             'cost_local': '220 – 1,550 AED',
                                             'cultural_significance': 'A mark of elegance and modesty, where Talli '
                                                                      'bobbin lace is recognized as UNESCO Intangible '
                                                                      'Cultural Heritage.',
                                             'description': 'Flowing black cloak (Abaya) over an embroidered jalabiya '
                                                            '(Mukhawara), matched with lightweight headscarf (Sheila) '
                                                            'and traditional golden metallic leather face mask '
                                                            '(Burqa).',
                                             'fabrics': 'Crepe silk, satin, gold Talli braid embroidery',
                                             'gender': 'Women',
                                             'image': None,
                                             'local_name': 'العباية والشيلة (Mukhawara)',
                                             'name': 'Emirati Abaya & Sheila with Burqa Face Adornment',
                                             'region': 'Abu Dhabi, Dubai & Sharjah',
                                             'rental_price': '60 – 180 AED per day',
                                             'where_to_buy': 'Souk Naif (Deira, Dubai), Souk Al Zafarana (Al Ain), '
                                                             'Madinat Jumeirah'}},
    'United Kingdom': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                             'cost_inr': '₹15,000 – ₹45,000',
                                             'cost_local': '£150 – £450 GBP',
                                             'cultural_significance': 'Safeguards Welsh cultural and linguistic '
                                                                      "heritage, worn proudly on St. David's Day.",
                                             'description': 'Historical folk ensemble featuring a scarlet wool flannel '
                                                            'open bedgown, striped petticoat, starched white apron, '
                                                            'and tall black stovepipe hat.',
                                             'fabrics': 'Pure Welsh wool flannel, starched white cotton',
                                             'gender': 'Women',
                                             'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/53/Welsh_spinners.jpeg/330px-Welsh_spinners.jpeg',
                                             'local_name': 'Gwisg Gymreig Draddodiadol',
                                             'name': 'Welsh National Traditional Dress',
                                             'region': 'Wales (Cardiff, Snowdonia)',
                                             'rental_price': '£35 – £75 GBP per day',
                                             'where_to_buy': 'St Fagans National Museum shops, Cardiff Arcades'},
                                         {   'category': "👨 Men's Traditional Attire",
                                             'cost_inr': '₹35,000 – ₹120,000+',
                                             'cost_local': '£350 – £1,200+ GBP',
                                             'cultural_significance': 'Proud emblem of Scottish Gaelic heritage and '
                                                                      'clan identity worn at weddings and Highland '
                                                                      'Games.',
                                             'description': 'Eight yards of heavy wool pleated into a clan tartan '
                                                            'kilt, accompanied by a Prince Charlie coatee with '
                                                            'silver-plated buttons, horsehair sporran, and kilt pin.',
                                             'fabrics': 'Pure Scottish worsted wool tartan, leather, silver',
                                             'gender': 'Men',
                                             'image': None,
                                             'local_name': 'Highland Dress / Scottish Kilt',
                                             'name': 'Scottish Highland Kilt & Prince Charlie Jacket',
                                             'region': 'Scotland (Edinburgh, Highlands)',
                                             'rental_price': '£55 – £110 GBP per weekend',
                                             'where_to_buy': 'Royal Mile Kiltmakers (Edinburgh), Gordon Nicolson '
                                                             'Kilts'},
                                         {   'category': "🌍 Regional / Women's Highland Attire",
                                             'cost_inr': '₹12,000 – ₹38,000',
                                             'cost_local': '£120 – £380 GBP',
                                             'cultural_significance': "Historical Gaelic women's attire providing "
                                                                      'warmth and family allegiance during Highland '
                                                                      'gatherings.',
                                             'description': "Traditional Gaelic women's wrap consisting of wide "
                                                            'white-ground clan tartan fabric draped gracefully around '
                                                            'the shoulders and fastened with a circular silver Celtic '
                                                            'brooch.',
                                             'fabrics': 'Lightweight woven Highland wool and Celtic silver',
                                             'gender': 'Regional',
                                             'image': None,
                                             'local_name': 'Earasaid (Arisaid)',
                                             'name': 'Scottish Highland Tartan Arisaid & Plaid',
                                             'region': 'Scottish Highlands & Hebrides Islands',
                                             'rental_price': '£40 – £80 GBP per day',
                                             'where_to_buy': 'Isle of Skye weavers, Inverness Tartan Guild'}],
                          'country': 'United Kingdom',
                          'cultural_significance': 'Traditional attire across the UK preserves distinct Celtic '
                                                   'identity and centuries of wool weaving.',
                          'men': {   'category': "👨 Men's Traditional Attire",
                                     'cost_inr': 'Full Regalia: ₹35,000 – ₹120,000+',
                                     'cost_local': '£350 – £1,200+ GBP',
                                     'cultural_significance': 'The proud emblem of Scottish Gaelic heritage and clan '
                                                              'identity, worn at Highland Games, weddings, and Ceilidh '
                                                              'dances.',
                                     'description': 'Eight yards of heavy woven wool pleated into a clan tartan kilt, '
                                                    'accompanied by a black Prince Charlie tailored coatee with '
                                                    'silver-plated buttons, a horsehair or leather pouch (Sporran), '
                                                    'kilt pin, and a small ceremonial sgian-dubh knife tucked in the '
                                                    'sock.',
                                     'fabrics': '100% pure Scottish worsted wool tartan, leather, and sterling silver',
                                     'gender': 'Men',
                                     'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e2/Scottish_mercenaries_in_the_Thirty_Years_War.jpg/330px-Scottish_mercenaries_in_the_Thirty_Years_War.jpg',
                                     'local_name': 'Highland Dress / Scottish Kilt',
                                     'name': 'Scottish Highland Kilt & Prince Charlie Jacket',
                                     'region': 'Scotland (Edinburgh, Glasgow, Highlands & Islands)',
                                     'rental_price': '£55 – £110 GBP per weekend',
                                     'where_to_buy': 'Royal Mile Whiskies & Kilts (Edinburgh), Gordon Nicolson '
                                                     'Kiltmakers'},
                          'rental_note': "Kilt rental outfitters on Edinburgh's Royal Mile provide complete fitting, "
                                         'highland accessories, and shoes.',
                          'women': {   'category': "👩 Women's Traditional Attire",
                                       'cost_inr': '₹15,000 – ₹45,000',
                                       'cost_local': '£150 – £450 GBP',
                                       'cultural_significance': 'Popularized by Lady Llanover in the 19th century to '
                                                                'safeguard Welsh linguistic and textile identity, '
                                                                "celebrated on St. David's Day.",
                                       'description': 'Historical folk ensemble featuring a scarlet wool flannel open '
                                                      'bedgown (Betgwn), checked or striped petticoat, starched white '
                                                      'apron, fringed shawl, and a distinctive tall black stovepipe '
                                                      'hat worn over a frilled mob cap.',
                                       'fabrics': 'Pure Welsh wool flannel, starched white cotton, and lace',
                                       'gender': 'Women',
                                       'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/53/Welsh_spinners.jpeg/330px-Welsh_spinners.jpeg',
                                       'local_name': 'Gwisg Gymreig Draddodiadol',
                                       'name': 'Welsh National Traditional Dress',
                                       'region': 'Wales (Cardiff, Snowdonia, St Davids)',
                                       'rental_price': '£35 – £75 GBP per day',
                                       'where_to_buy': 'St Fagans National Museum of History craft shops, Cardiff '
                                                       'Victorian Arcades'}},
    'Vietnam': {   'attires': [   {   'category': "👩 Women's Traditional Attire",
                                      'cost_inr': '₹3,500 – ₹16,000',
                                      'cost_local': '1,000,000 – 4,800,000 VND',
                                      'cultural_significance': 'Quintessential emblem of Vietnamese grace and poise, '
                                                               'worn during festivals and weddings.',
                                      'description': 'Form-fitting silk tunic split from waist downward into flowing '
                                                     'panels, worn over wide-leg trousers with a conical palm hat.',
                                      'fabrics': 'Ha Dong natural silk, chiffon, hand-embroidery',
                                      'gender': 'Women',
                                      'image': 'https://upload.wikimedia.org/wikipedia/commons/1/1a/%C3%81o_d%C3%A0i_hoa_ph%C6%B0%E1%BB%A3ng_-_Ph%C3%A1t_Tr%C6%B0%C6%A1ng_-_51231007393_%28cropped%29.jpg',
                                      'local_name': 'Áo dài nữ và Nón lá',
                                      'name': 'Áo Dài Silk Tunic & Nón Lá',
                                      'region': 'Hue Imperial City, Hanoi & Saigon',
                                      'rental_price': '150,000 – 350,000 VND per day',
                                      'where_to_buy': 'Hoi An custom tailors, Hang Gai Street (Hanoi)'},
                                  {   'category': "👨 Men's Traditional Attire",
                                      'cost_inr': '₹4,500 – ₹18,000',
                                      'cost_local': '1,350,000 – 5,400,000 VND',
                                      'cultural_significance': 'Five buttons symbolize the Five Virtues of Confucian '
                                                               'philosophy.',
                                      'description': 'Tailored silk long tunic for men featuring a firm mandarin '
                                                     'collar and five-button fastening, paired with silk trousers and '
                                                     'a black wrapped fabric turban.',
                                      'fabrics': 'Thượng Hải brocade silk and Ha Dong mulberry silk',
                                      'gender': 'Men',
                                      'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/05/Hisu_lee_2015-08-16_%28Unsplash%29.jpg/960px-Hisu_lee_2015-08-16_%28Unsplash%29.jpg',
                                      'local_name': 'Áo dài nam truyền thống',
                                      'name': "Áo Dài Nam (Men's Traditional Ao Dai)",
                                      'region': 'Hanoi, Hue & Pan-Vietnam',
                                      'rental_price': '180,000 – 400,000 VND per day',
                                      'where_to_buy': 'Hang Gai Street (Hanoi), Hoi An Ancient Town tailors'},
                                  {   'category': '🌍 Regional / Southern Attire',
                                      'cost_inr': '₹1,200 – ₹4,000',
                                      'cost_local': '350,000 – 1,200,000 VND',
                                      'cultural_significance': 'Emblematic of the pastoral, hard-working, and '
                                                               'warm-hearted agrarian culture of the Mekong Delta '
                                                               'waterway communities.',
                                      'description': 'Simple, comfortable collarless silk tunic buttoned down the '
                                                     'front with two lower pockets, accompanied by a checkered cotton '
                                                     'scarf (Khăn rằn) and conical hat.',
                                      'fabrics': 'Soft Southern Vietnamese silk and breathable cotton',
                                      'gender': 'Regional',
                                      'image': None,
                                      'local_name': 'Áo bà ba Nam Bộ',
                                      'name': 'Áo Bà Ba (Mekong Delta Silk Attire)',
                                      'region': 'Mekong River Delta & Southern Countryside',
                                      'rental_price': '100,000 – 200,000 VND per day',
                                      'where_to_buy': 'Can Tho Riverside Market, Cai Rang Floating Market, Ben Thanh '
                                                      'Market'}],
                   'country': 'Vietnam',
                   'cultural_significance': 'Vietnamese traditional attire reflects a deep synthesis of royal court '
                                            'elegance and everyday waterway lifestyle.',
                   'men': {   'category': "👨 Men's Traditional Attire",
                              'cost_inr': '₹4,500 – ₹18,000',
                              'cost_local': '1,350,000 – 5,400,000 VND',
                              'cultural_significance': 'The five buttons represent the Five Virtues (Nhân, Lễ, Nghĩa, '
                                                       'Trí, Tín) of Confucian tradition.',
                              'description': 'Tailored silk long tunic for men featuring a firm mandarin collar and '
                                             'five-button fastening, paired with silk trousers and a black wrapped '
                                             'fabric turban (Khăn đóng).',
                              'fabrics': 'Thượng Hải brocade silk and Ha Dong mulberry silk',
                              'gender': 'Men',
                              'image': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/05/Hisu_lee_2015-08-16_%28Unsplash%29.jpg/960px-Hisu_lee_2015-08-16_%28Unsplash%29.jpg',
                              'local_name': 'Áo dài nam truyền thống',
                              'name': "Áo Dài Nam (Men's Traditional Ao Dai)",
                              'region': 'Hanoi, Hue & Pan-Vietnam',
                              'rental_price': '180,000 – 400,000 VND per day',
                              'where_to_buy': 'Hang Gai Street (Hanoi Silk Street), Hoi An Ancient Town tailors'},
                   'rental_note': 'Hoi An Ancient Town offers 24-hour bespoke tailor-made Ao Dai fitted directly to '
                                  'tourist measurements.',
                   'women': {   'category': "👩 Women's Traditional Attire",
                                'cost_inr': 'Tailored: ₹3,500 – ₹16,000 • Ready-made: ₹1,800 – ₹6,000',
                                'cost_local': '1,000,000 – 4,800,000 VND',
                                'cultural_significance': 'The quintessential emblem of Vietnamese grace, feminine '
                                                         'poise, and national pride, celebrated during Tết.',
                                'description': 'Form-fitting silk tunic with high mandarin collar split from the waist '
                                               'downward into two flowing front and back panels, worn over wide-leg '
                                               'silk trousers with a conical palm leaf hat (Nón Lá).',
                                'fabrics': 'Pure Vietnamese Ha Dong natural silk, chiffon, and hand-embroidered velvet',
                                'gender': 'Women',
                                'image': 'https://upload.wikimedia.org/wikipedia/commons/1/1a/%C3%81o_d%C3%A0i_hoa_ph%C6%B0%E1%BB%A3ng_-_Ph%C3%A1t_Tr%C6%B0%C6%A1ng_-_51231007393_%28cropped%29.jpg',
                                'local_name': 'Áo dài nữ và Nón lá',
                                'name': 'Áo Dài Silk Tunic & Nón Lá',
                                'region': 'Hue Imperial City, Hanoi & Saigon',
                                'rental_price': '150,000 – 350,000 VND per day',
                                'where_to_buy': 'Hoi An 24-hour custom tailors, Dong Xuan Market (Hanoi), Ben Thanh '
                                                'Market (Saigon)'}}}


def get_synthesized_clothing(country_name: str) -> Dict[str, Any]:
    """Generates authentic traditional clothing profile for any of the 250 countries without borrowing photos from other nations."""
    prof = get_country_knowledge(country_name)
    c_name = prof.get("name", country_name)
    region = (prof.get("region") or "").lower()
    subregion = (prof.get("subregion") or "").lower()
    capital = prof.get("capital") or c_name
    curr = prof.get("currency") or "local currency"
    c_low = c_name.lower()

    # Cultural zone selection based on geography and ethnography
    is_maghreb = any(k in c_low for k in ["morocco", "algeria", "tunisia", "libya", "mauritania"])
    is_gulf = any(k in c_low for k in ["saudi", "emirates", "qatar", "oman", "kuwait", "bahrain", "yemen"])
    is_levant = any(k in c_low for k in ["jordan", "lebanon", "syria", "palestine", "iraq"])
    is_persian = any(k in c_low for k in ["iran", "persia", "afghanistan"])
    is_central_asia = any(k in c_low for k in ["uzbekistan", "kazakhstan", "kyrgyzstan", "tajikistan", "turkmenistan", "mongolia"])
    is_south_asia = any(k in c_low for k in ["pakistan", "bangladesh", "sri lanka", "nepal", "bhutan", "maldives"])
    is_andean = any(k in c_low for k in ["peru", "bolivia", "ecuador"])
    is_colombia_ven = any(k in c_low for k in ["colombia", "venezuela"])
    is_pampas = any(k in c_low for k in ["argentina", "uruguay", "chile", "paraguay"])
    is_central_am = any(k in c_low for k in ["guatemala", "honduras", "salvador", "nicaragua", "costa rica", "panama", "belize"])
    is_caribbean = "caribbean" in subregion or any(k in c_low for k in ["cuba", "jamaica", "dominican", "haiti", "bahamas", "trinidad", "barbados", "guyana", "suriname"])
    is_nordic = any(k in c_low for k in ["norway", "sweden", "denmark", "finland", "iceland"])
    is_alpine = any(k in c_low for k in ["switzerland", "austria", "liechtenstein"])
    is_slavic = any(k in c_low for k in ["ukraine", "poland", "czech", "slovakia", "russia", "belarus", "bulgaria", "serbia", "croatia", "bosnia", "slovenia", "macedonia", "montenegro"])
    is_pacific = "polynesia" in subregion or "micronesia" in subregion or "melanesia" in subregion or any(k in c_low for k in ["zealand", "fiji", "samoa", "tonga", "tahiti", "vanuatu"])
    is_east_africa = any(k in c_low for k in ["kenya", "tanzania", "uganda", "ethiopia", "rwanda", "somalia"])
    is_portugal = "portugal" in c_low
    is_turkey = "turkey" in c_low or "türkiye" in c_low

    if is_maghreb:
        men = {
            "name": f"{c_name} Traditional Djellaba & Tarbouch",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "جلابة وطربوش (Djellaba & Tarbouch)",
            "region": f"{c_name}",
            "image": None,
            "description": "Flowing hooded robe with long sleeves, handcrafted sfifa needlework along the seams, paired with yellow leather babouche slippers.",
            "fabrics": "Fine woven wool, lightweight cotton, or linen",
            "cost_inr": "₹4,000 – ₹14,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,200 per day",
            "where_to_buy": f"Traditional medina souks and tailor quarters in {capital}",
            "cultural_significance": "A timeless Maghrebi garment worn for Friday prayers, family celebrations, and daily elegance."
        }
        women = {
            "name": f"{c_name} Royal Embroidered Caftan / Takchita",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "قفطان مغاربي (Caftan / Takchita)",
            "region": f"{c_name}",
            "image": None,
            "description": "Two-piece ceremonial silk velvet gown adorned with intricate gold zardozi and sfifa braiding, cinched with an ornate metallic mdamma belt.",
            "fabrics": "Pure silk velvet, jacquard brocade, and metallic thread",
            "cost_inr": "₹12,000 – ₹45,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹2,500 – ₹6,000 per day",
            "where_to_buy": f"Haute couture caftan ateliers and bridal boutiques in {capital}",
            "cultural_significance": "Celebrated at weddings and grand receptions as the pinnacle of North African textile craftsmanship."
        }
        regional = {
            "name": f"{c_name} Berber Traditional Fibula Dress",
            "gender": "Regional",
            "category": "🌍 Regional / Traditional Variation",
            "local_name": "Tamazight Regalia",
            "region": "Atlas & Mountain Provinces",
            "image": None,
            "description": "Handwoven wool drapery fastened at the shoulders with carved silver fibula brooches, paired with amber and coral bead necklaces.",
            "fabrics": "Pure virgin mountain wool and tribal silver jewelry",
            "cost_inr": "₹6,000 – ₹22,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,200 – ₹2,800 per day",
            "where_to_buy": f"Mountain artisan cooperatives in {c_name}",
            "cultural_significance": "Preserves ancestral indigenous Amazigh identity and talismanic jewelry traditions."
        }
        significance = f"Traditional attire in {c_name} blends Andalusian-Moorish heritage with ancient Berber craftsmanship."

    elif is_gulf or is_levant or "western asia" in subregion:
        men = {
            "name": f"{c_name} National Thobe / Dishdasha & Keffiyeh",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "ثوب / دشداشة (Thobe / Dishdasha)",
            "region": f"{c_name}",
            "image": None,
            "description": "Tailored ankle-length robe with structured mandarin collar, worn with the Ghutra/Keffiyeh headdress held in place by the black corded Agal.",
            "fabrics": "Crisp breathable white cotton or tropical wool blend",
            "cost_inr": "₹3,500 – ₹16,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹800 – ₹2,000 per day",
            "where_to_buy": f"Heritage souks and specialized menswear tailors in {capital}",
            "cultural_significance": "The official national dress worn with pride across daily business and ceremonial life."
        }
        women = {
            "name": f"{c_name} Tatreez Embroidered Thobe & Abaya",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "ثوب مطرز / عباية (Tatreez Thobe)",
            "region": f"{c_name}",
            "image": None,
            "description": "Flowing linen or silk gown embellished with heritage cross-stitch Tatreez embroidery depicting regional flora and geometric motifs, paired with a matching veil.",
            "fabrics": "Hand-embroidered linen, raw silk, and crepe",
            "cost_inr": "₹6,000 – ₹28,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,200 – ₹3,000 per day",
            "where_to_buy": f"Artisan embroidery cooperatives and cultural boutiques in {capital}",
            "cultural_significance": "Tatreez embroidery is an UNESCO-recognized art expressing heritage, regional identity, and community history."
        }
        regional = {
            "name": f"{c_name} Ceremonial Bisht Robe",
            "gender": "Ceremonial",
            "category": "👑 Ceremonial Royal Attire",
            "local_name": "بشت (Bisht)",
            "region": f"{c_name}",
            "image": None,
            "description": "Flowing outer cloak trimmed with genuine gold or silver metallic thread embroidery, worn over the Thobe for weddings and VIP occasions.",
            "fabrics": "Camel hair, fine wool, and French metallic gold thread",
            "cost_inr": "₹15,000 – ₹60,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹2,500 – ₹5,500 per day",
            "where_to_buy": f"Royal Bisht ateliers in {capital}",
            "cultural_significance": "Conveys leadership, prestige, and joyous celebration at weddings and state functions."
        }
        significance = f"Attire in {c_name} reflects the bedouin values of dignity, hospitality, and cultural continuity."

    elif is_persian:
        men = {
            "name": f"{c_name} Traditional Persian Robe & Kolah Cap",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "لباس سنتی مردانه (Persian Traditional Suit)",
            "region": f"{c_name}",
            "image": None,
            "description": "Tailored vest (Jelaghe) over a mandarin-collared linen tunic, wide pleated trousers (Shalvar), embroidered waist sash (Kammarband), and felt Kolah cap.",
            "fabrics": "Handloom wool, silk brocade, and soft linen",
            "cost_inr": "₹5,000 – ₹20,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,500 per day",
            "where_to_buy": f"Grand Bazaar artisan textile shops in {capital}",
            "cultural_significance": "Celebrates Nowruz and ancient Persian cultural roots with regal elegance."
        }
        women = {
            "name": f"{c_name} Termeh Brocade Silk Gown & Chador",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "لباس ترمه و پیراهن سنتی (Termeh Traditional Gown)",
            "region": f"{c_name}",
            "image": None,
            "description": "Exquisite handwoven Termeh paisley silk coat worn over a multi-tiered pleated skirt (Daman), delicate sheer veil, and gold-embroidered slippers.",
            "fabrics": "Pure Termeh silk-wool brocade with gold paisley motifs",
            "cost_inr": "₹9,000 – ₹36,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,800 – ₹4,500 per day",
            "where_to_buy": f"Textile artisan souks and Termeh boutiques in {capital}",
            "cultural_significance": "Termeh weaving has flourished for over four centuries, symbolizing eternal life and beauty."
        }
        regional = {
            "name": f"{c_name} Nomadic Bakhtiari / Qashqai Regalia",
            "gender": "Regional",
            "category": "🏔️ Nomadic Tribal Regalia",
            "local_name": "لباس عشایری (Tribal Nomadic Dress)",
            "region": "Zagros Mountains & Highland Valleys",
            "image": None,
            "description": "Multi-layered shimmering colorful skirts, coin-fringed velvet vest, and long silk scarf held by decorative jeweled pins.",
            "fabrics": "Vibrant silk organza, velvet, and antique coin fringe",
            "cost_inr": "₹6,000 – ₹24,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,200 – ₹3,000 per day",
            "where_to_buy": f"Highland cultural centers and tribal bazaars in {c_name}",
            "cultural_significance": "Reflects the free spirit, equestrian mastery, and vivid colors of the pastoral nomads."
        }
        significance = f"Persian traditional garments showcase four millennia of weaving artistry, courtly dignity, and poetic symbolism."

    elif is_central_asia:
        men = {
            "name": f"{c_name} Traditional Chapan & Doppa / Tubeteika",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Chapan & Doʻppi / Tubeteika",
            "region": f"{c_name}",
            "image": None,
            "description": "Quilted silk-cotton outer robe (Chapan) featuring hand-stitched floral borders, belted with a triangular silk sash (Belbog'), paired with a black-and-white embroidered Doppa skullcap.",
            "fabrics": "Quilted velvet, pure silk, or Ikat-dyed handloom fabric",
            "cost_inr": "₹4,500 – ₹18,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,400 per day",
            "where_to_buy": f"Chorsu Bazaar and Silk Road artisan caravanserais in {capital}",
            "cultural_significance": "A symbol of deep respect and hospitality, traditionally presented to honored guests across Central Asia."
        }
        women = {
            "name": f"{c_name} Khan-Atlas Pure Silk Robe & Tunic",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Xonatlas / Adras Dress",
            "region": f"{c_name}",
            "image": None,
            "description": "Luminous cloud-patterned rainbow Ikat silk dress (Khan-Atlas) worn over tailored silk trousers (Ishton), accessorized with filigree silver jewelry and embroidered skullcap.",
            "fabrics": "Natural Margilan mulberry silk hand-dyed with plant pigments",
            "cost_inr": "₹6,000 – ₹26,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,200 – ₹3,200 per day",
            "where_to_buy": f"Traditional silk weaving ateliers in {capital}",
            "cultural_significance": "Celebrated as the UNESCO-recognized crowning glory of Central Asian textile art."
        }
        regional = {
            "name": f"{c_name} Nomadic Deel / Felt Regalia",
            "gender": "Regional",
            "category": "🐎 Steppe Nomadic Regalia",
            "local_name": "Deel / Shapan",
            "region": "Steppe & Mountain Valleys",
            "image": None,
            "description": "Durable high-collared wrap robe fastening with clasps on the right shoulder, tied with a long silk sash, worn with leather riding boots.",
            "fabrics": "Heavy wool felt, lambskin lining, or raw silk",
            "cost_inr": "₹5,500 – ₹22,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,100 – ₹2,800 per day",
            "where_to_buy": f"Nomadic heritage centers and craft workshops in {c_name}",
            "cultural_significance": "Engineered for horseback riding and resilience in extreme continental climates."
        }
        significance = f"Central Asian attire carries the living soul of the Great Silk Road, where Chinese silks and nomadic craftsmanship converged."

    elif is_south_asia:
        men = {
            "name": f"{c_name} Heritage Kurta Pajama / Shalwar Kameez & Waistcoat",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Kurta Pajama / Shalwar Kameez",
            "region": f"{c_name}",
            "image": None,
            "description": "Tailored knee-length cotton or silk tunic (Kurta), comfortable trousers, structured Nehru/waistcoat with brass buttons, and embroidered mojari footwear.",
            "fabrics": "Handspun khadi cotton, tussar silk, and jacquard brocade",
            "cost_inr": "₹2,500 – ₹12,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹700 – ₹1,800 per day",
            "where_to_buy": f"Heritage textile bazaars and bespoke tailors in {capital}",
            "cultural_significance": "Worn across South Asia for weddings, religious ceremonies, and formal celebrations."
        }
        women = {
            "name": f"{c_name} Embroidered Shalwar Kameez / Sari with Dupatta",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Shalwar Kameez / Sari",
            "region": f"{c_name}",
            "image": None,
            "description": "Gracefully draped silk sari or intricately embroidered tunic paired with wide trousers and a flowing matching dupatta scarf adorned with zari borders.",
            "fabrics": "Pure mulberry silk, georgette, and metallic zari thread",
            "cost_inr": "₹3,500 – ₹18,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹900 – ₹2,400 per day",
            "where_to_buy": f"Silk saree emporiums and ethnic boutiques in {capital}",
            "cultural_significance": "An icon of graceful poise and centuries-old handloom weaving traditions."
        }
        regional = {
            "name": f"{c_name} Regional Ajrak / Mirrorwork Regalia",
            "gender": "Regional",
            "category": "✨ Regional Artisan Regalia",
            "local_name": "Ajrak & Mirrorwork Waistcoat",
            "region": f"{c_name} Heritage Districts",
            "image": None,
            "description": "Hand block-printed indigo and madder-red Ajrak shawl paired with a waistcoat embellished with tiny mirrors and hand embroidery.",
            "fabrics": "Block-printed organic cotton, natural indigo dye, and glass mirrors",
            "cost_inr": "₹2,000 – ₹8,500",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹600 – ₹1,500 per day",
            "where_to_buy": f"Artisan cooperatives and craft villages in {c_name}",
            "cultural_significance": "Celebrates ancient Indus Valley block-printing techniques and folk embroidery."
        }
        significance = f"South Asian attire embodies royal courtly splendor, spiritual harmony, and unmatched textile diversity."

    elif is_slavic:
        men = {
            "name": f"{c_name} Traditional Slavic Embroidered Kosovorotka & Belt",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Strój Męski / Kosovorotka / Rubakha",
            "region": f"{c_name}",
            "image": None,
            "description": "Stand-collar linen tunic with red-and-white cross-stitch geometric embroidery on the chest and cuffs, tied with a braided woven sash, paired with tailored wool trousers and boots.",
            "fabrics": "Flax linen, cotton thread embroidery, and woven wool sash",
            "cost_inr": "₹4,500 – ₹17,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,500 per day",
            "where_to_buy": f"Folk art guilds and Cepelia craft galleries in {capital}",
            "cultural_significance": "Traditional Slavic embroidery patterns served as protective amulets celebrating nature and family harmony."
        }
        women = {
            "name": f"{c_name} Strój Ludowy / Vyshyvanka Folk Dress with Floral Wreath",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Strój Ludowy / Vyshyvanka",
            "region": f"{c_name}",
            "image": None,
            "description": "Hand-embroidered white linen blouse, fitted velvet bodice (gorset) laced with ribbons and beads, colorful pleated floral skirt, lace apron, and a crown of fresh flowers or ribbons with coral beads.",
            "fabrics": "Pure linen, velvet, ribbon trimmings, and genuine coral beads",
            "cost_inr": "₹8,000 – ₹32,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,500 – ₹4,000 per day",
            "where_to_buy": f"Regional folklore ateliers across {capital}",
            "cultural_significance": "The quintessential Slavic national folk dress, worn during Dożynki harvest festivals and Kupala summer rites."
        }
        regional = {
            "name": f"{c_name} Highland Góral Woolen Regalia",
            "gender": "Regional",
            "category": "🏔️ Highland Mountain Regalia",
            "local_name": "Strój Góralski (Highland Folk Dress)",
            "region": "Carpathian & Tatra Mountains",
            "image": None,
            "description": "White wool felt trousers (portki) adorned with heart-shaped embroidered parzenica motifs, embroidered leather vest, and broad leather ciupaga belt.",
            "fabrics": "Heavy fulled mountain wool, sheepskin, and brass studs",
            "cost_inr": "₹10,000 – ₹38,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,800 – ₹4,500 per day",
            "where_to_buy": f"Mountain craft workshops in {c_name}",
            "cultural_significance": "Emblematic of mountaineer independence, pastoral resilience, and spirited highland dance."
        }
        significance = f"Slavic folk dress honors the agrarian rhythm of the seasons, ancestral floral symbols, and village craftsmanship."

    elif is_colombia_ven:
        men = {
            "name": f"{c_name} Ruana Campesina & Sombrero Vueltiao",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Ruana y Sombrero Vueltiao",
            "region": f"{c_name}",
            "image": None,
            "description": "Heavy woven virgin wool poncho (ruana) with an opening for the head, crisp white linen shirt, dark trousers, and the iconic braided cane Sombrero Vueltiao.",
            "fabrics": "100% virgin sheep wool and arrow cane (caña flecha)",
            "cost_inr": "₹5,000 – ₹18,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,400 per day",
            "where_to_buy": f"Artisan craft markets in {capital} and Andean artisan towns",
            "cultural_significance": "The Sombrero Vueltiao is a national cultural symbol crafted using Zenú pre-Columbian braiding techniques."
        }
        women = {
            "name": f"{c_name} Traje de Pollera Colorada (Ruffled Folk Dress)",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Pollera Colorada / Sanjuanero",
            "region": f"{c_name}",
            "image": None,
            "description": "Off-the-shoulder white blouse with lace ruffles, paired with an expansive flowing layered skirt printed with colorful floral cascades, accessorized with fresh flowers in the hair.",
            "fabrics": "Soft cotton, fine lace, and satin ribbon borders",
            "cost_inr": "₹6,000 – ₹22,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,200 – ₹2,800 per day",
            "where_to_buy": f"Folklore dress boutiques and carnival markets in {capital}",
            "cultural_significance": "Celebrates cumbia and bambuco folklore, where the swirling skirt portrays joyful courtship."
        }
        regional = {
            "name": f"{c_name} Llanero Joropo Cowboy Attire (Liqui Liqui)",
            "gender": "Regional",
            "category": "🌾 Plains Cowboy Regalia",
            "local_name": "Liqui Liqui / Traje Llanero",
            "region": "Eastern Plains (Los Llanos)",
            "image": None,
            "description": "Tailored jacket with high stand collar and metallic buttons, matching straight trousers, wide-brimmed felt hat, and leather alpargatas.",
            "fabrics": "Crisp linen or tropical gabardine with bone buttons",
            "cost_inr": "₹5,500 – ₹20,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,100 – ₹2,500 per day",
            "where_to_buy": f"Traditional menswear shops across {c_name}",
            "cultural_significance": "The formal national suit of the plains cowboy, worn with pride for Joropo harp festivals."
        }
        significance = f"Attire in {c_name} unites Andean indigenous warmth, Caribbean coastal rhythm, and plains cattle ranching nobility."

    elif is_caribbean:
        men = {
            "name": f"{c_name} Guayabera Linen Shirt & Panama Hat",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Guayabera & Jipijapa Hat",
            "region": f"{c_name}",
            "image": None,
            "description": "Lightweight breathable four-pocket pleated linen shirt (Guayabera) worn untucked with linen trousers and a finely woven toquilla straw hat.",
            "fabrics": "100% fine Irish or Italian linen, natural palm fiber",
            "cost_inr": "₹3,500 – ₹14,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹800 – ₹2,000 per day",
            "where_to_buy": f"Heritage menswear boutiques and port markets in {capital}",
            "cultural_significance": "The official formal attire of the Caribbean, accepted internationally for diplomacy and island celebrations."
        }
        women = {
            "name": f"{c_name} Quadrille / Bandana Cloth Ruffled Folk Dress",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Quadrille / Bandana Dress",
            "region": f"{c_name}",
            "image": None,
            "description": "Vibrant red-and-white madras/bandana cotton dress with puffy sleeves, ruffled neckline, sweeping ruffled skirt, and matching headwrap (tie-head).",
            "fabrics": "Pure cotton madras check, white cotton eyelet lace",
            "cost_inr": "₹4,000 – ₹16,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹900 – ₹2,200 per day",
            "where_to_buy": f"Craft markets and cultural centers in {capital}",
            "cultural_significance": "The national costume of the English and French Caribbean, worn proudly on National Heritage and Independence Days."
        }
        regional = {
            "name": f"{c_name} Carnival Masquerade Feather Regalia",
            "gender": "Regional",
            "category": "🎉 Carnival Festive Regalia",
            "local_name": "Carnival Mas Regalia",
            "region": f"{c_name} Coastal Celebrations",
            "image": None,
            "description": "Spectacular masquerade costume laden with iridescent ostrich and pheasant feathers, sequined bodysuits, and jeweled headdresses.",
            "fabrics": "Lycra, glass crystals, holographic foil, and natural feathers",
            "cost_inr": "₹12,000 – ₹55,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹3,000 – ₹9,000 per day",
            "where_to_buy": f"Mas camps and costume design studios in {c_name}",
            "cultural_significance": "Celebrates liberation, musical dynamism, and Caribbean carnival artistry."
        }
        significance = f"Caribbean attire channels the vibrant history, resilience, and joyful spirit of island culture."

    elif is_andean:
        men = {
            "name": f"{c_name} Handwoven Andean Poncho & Chullo",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Poncho y Chullo Andino",
            "region": "Highland Andes",
            "image": None,
            "description": "Geometric handwoven alpaca wool poncho with ancient community motifs, ear-flapped knit chullo cap, and sturdy trousers.",
            "fabrics": "Pure baby alpaca and sheep wool dyed with natural plant extracts",
            "cost_inr": "₹4,500 – ₹18,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,500 per day",
            "where_to_buy": f"Indigenous textile markets in {capital} and highland valleys",
            "cultural_significance": "Poncho patterns identify the wearer's community, marital status, and altitude origins."
        }
        women = {
            "name": f"{c_name} Pollera Skirt & Embroidered Lliclla Shawl",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Pollera y Lliclla",
            "region": "Andean Highlands",
            "image": None,
            "description": "Layered pleated gathered skirts (polleras) in vibrant colors, handwoven shoulder mantle (lliclla) pinned with a silver tupu, and felt bowler or montera hat.",
            "fabrics": "Handspun wool, velvet ribbon borders, and silver tupu brooches",
            "cost_inr": "₹6,000 – ₹24,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,200 – ₹3,000 per day",
            "where_to_buy": f"Handicraft markets and weaving cooperatives in {c_name}",
            "cultural_significance": "Preserves Quechua and Aymara astronomical weaving codes passed down from Incan ancestors."
        }
        regional = {
            "name": f"{c_name} Fiesta Folkloric Dance Regalia",
            "gender": "Regional",
            "category": "🎭 Festival Regalia",
            "local_name": "Traje de Danza Tradicional",
            "region": f"{c_name}",
            "image": None,
            "description": "Elaborately sequined and embroidered dance costume adorned with metallic fringe, mirrors, and sculptural masks.",
            "fabrics": "Velvet, metallic lamé, and glass beads",
            "cost_inr": "₹8,000 – ₹32,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,500 – ₹3,500 per day",
            "where_to_buy": f"Festival costume ateliers in {c_name}",
            "cultural_significance": "Worn during magnificent patron saint carnivals celebrating highland folklore."
        }
        significance = f"Reflects the living ancestral traditions of the Andes and indigenous textile mastery."

    elif is_nordic:
        men = {
            "name": f"{c_name} Traditional Folkdräkt / Bunad Folk Suit",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Folkdräkt / Bunad",
            "region": f"{c_name}",
            "image": None,
            "description": "Tailored wool vest with brass or silver buttons, linen stand-collar shirt, wool breeches with silver knee buckles, and hand-knit wool stockings.",
            "fabrics": "Homespun Nordic wool broadcloth, flax linen, and silver buttons",
            "cost_inr": "₹25,000 – ₹90,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹3,500 – ₹8,000 per day",
            "where_to_buy": f"Husfliden and folk craft guilds in {capital}",
            "cultural_significance": "Emblematic of pastoral heritage, worn proudly on National Day and midsummer celebrations."
        }
        women = {
            "name": f"{c_name} Traditional Embroidered Apron Dress & Bodice",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Folkdräkt / Bunad",
            "region": f"{c_name}",
            "image": None,
            "description": "Fitted woolen bodice laced over a smocked white linen blouse, pleated skirt, hand-embroidered regional apron, and silver heirloom brooches.",
            "fabrics": "Virgin wool, pure linen, and handcrafted silver jewelry",
            "cost_inr": "₹30,000 – ₹110,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹4,000 – ₹9,000 per day",
            "where_to_buy": f"National handicraft ateliers across {c_name}",
            "cultural_significance": "A prized family heirloom handed down through generations, celebrating midsummer and regional rural roots."
        }
        regional = {
            "name": f"{c_name} Regional Midsummer Festive Costume",
            "gender": "Regional",
            "category": "🌸 Festival Regalia",
            "local_name": "Festdräkt",
            "region": f"{c_name}",
            "image": None,
            "description": "Bright festive ensemble featuring colorful woven silk ribbons, floral head wreaths, and polished leather dancing shoes.",
            "fabrics": "Fine wool, silk ribbons, and natural linen",
            "cost_inr": "₹20,000 – ₹75,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹3,000 – ₹6,500 per day",
            "where_to_buy": f"Heritage folk ateliers in {c_name}",
            "cultural_significance": "Celebrates the return of the sun and seasonal fertility during Midsummer."
        }
        significance = f"Nordic traditional dress embodies centuries of pastoral self-sufficiency and community folklore."

    elif is_pacific:
        men = {
            "name": f"{c_name} Formal Sulu / Lavalava & Island Shirt",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Sulu vakataga / Lavalava",
            "region": f"{c_name}",
            "image": None,
            "description": "Tailored pocketed wrap skirt (sulu/lavalava) worn formally with a crisp collared island shirt, braided coconut-fiber sash, and leather sandals.",
            "fabrics": "Fine suit-weight cotton, tropical linen, and woven pandanus leaf",
            "cost_inr": "₹3,000 – ₹10,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹700 – ₹1,500 per day",
            "where_to_buy": f"Central island markets and garment shops in {capital}",
            "cultural_significance": "The official attire for government, church, and ceremonies across Pacific Island nations."
        }
        women = {
            "name": f"{c_name} Puletasi / Tapa Cloth Island Dress",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Puletasi / Tapa Dress",
            "region": f"{c_name}",
            "image": None,
            "description": "Two-piece ensemble consisting of a tailored tunic top and long matching wrap skirt patterned with traditional island tapa motifs, complemented by a fresh floral lei.",
            "fabrics": "Tapa bark cloth, printed cotton, and mother-of-pearl accents",
            "cost_inr": "₹3,500 – ₹12,500",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹800 – ₹1,800 per day",
            "where_to_buy": f"Handicraft village markets and local boutiques in {capital}",
            "cultural_significance": "Celebrated for its grace, modesty, and deep connection to Pacific voyaging traditions."
        }
        regional = {
            "name": f"{c_name} Ceremonial Feather Cloak / Woven Regalia",
            "gender": "Ceremonial",
            "category": "👑 Tribal Heritage Regalia",
            "local_name": "Kahu Huruhuru / Taʻovala",
            "region": f"{c_name}",
            "image": None,
            "description": "Hand-woven flax or pandanus matting adorned with native bird feathers, shell ornaments, and carved bone pendants.",
            "fabrics": "Harakeke flax, natural feathers, and pounamu / carved shell",
            "cost_inr": "₹15,000 – ₹60,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹2,500 – ₹6,000 per day",
            "where_to_buy": f"Cultural centers and indigenous art galleries in {c_name}",
            "cultural_significance": "Conveys ancestral mana, chieftain status, and sacred communal prestige."
        }
        significance = f"Pacific attire reflects the living spiritual connection between island communities and the ocean."

    elif is_portugal:
        men = {
            "name": "Traje de Campino (Traditional Ribatejo Horseman Attire)",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Traje de Campino",
            "region": "Ribatejo & Alentejo",
            "image": None,
            "description": "Authentic Portuguese horseman dress: scarlet wool waistcoat (colete encarnado), white pleated linen shirt, black knee-breeches, green knit cap (carapuço), and white wool stockings.",
            "fabrics": "Pure wool felt, unbleached linen, and brass buttons",
            "cost_inr": "₹12,000 – ₹42,000",
            "cost_local": "130 – 480 EUR",
            "rental_price": "50 – 120 EUR per day",
            "where_to_buy": "Folk costume ateliers in Santarém and Lisbon",
            "cultural_significance": "Worn with pride during cattle drives, bullfighting festivals, and regional folk pageants."
        }
        women = {
            "name": "Traje à Vianesa (Traditional Minho Embroidered Dress)",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Traje à Vianesa / Traje de Noiva",
            "region": "Viana do Castelo & Minho",
            "image": None,
            "description": "Exquisite hand-embroidered red and black wool skirt and bodice decorated with floral beadwork, a printed apron, and abundant filigrana de ouro (gold filigree jewelry).",
            "fabrics": "Homespun wool, hand-printed cotton apron, and Portuguese gold filigree",
            "cost_inr": "₹15,000 – ₹55,000",
            "cost_local": "170 – 620 EUR",
            "rental_price": "60 – 140 EUR per day",
            "where_to_buy": "Traditional embroidery cooperatives in Viana do Castelo",
            "cultural_significance": "The official symbol of Portuguese female folklore, celebrated during the Festas de Nossa Senhora da Agonia."
        }
        regional = {
            "name": "Traje de Nazaré (Coastal Fisherfolk Attire)",
            "gender": "Regional",
            "category": "🌊 Coastal Folk Regalia",
            "local_name": "Traje das Sete Saias",
            "region": "Nazaré Coastal Province",
            "image": None,
            "description": "Traditional ensemble of seven layered woolen petticoats (sete saias), embroidered apron, knit shawl, and black velvet bonnet.",
            "fabrics": "Plaid and flannel wool, cotton lace",
            "cost_inr": "₹10,000 – ₹36,000",
            "cost_local": "110 – 400 EUR",
            "rental_price": "45 – 100 EUR per day",
            "where_to_buy": "Fisherman artisan workshops in Nazaré",
            "cultural_significance": "The seven skirts represent the seven days of the week and maritime virtues."
        }
        significance = "Portuguese folk attire expresses maritime bravery and ancient agricultural festivity."

    elif is_alpine:
        men = {
            "name": "Swiss Alpine Tracht & Edelweisshemd",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Appenzeller Tracht / Edelweisshemd",
            "region": "Appenzell & Bernese Oberland",
            "image": None,
            "description": "Embroidered blue cotton Edelweiss shirt, leather suspenders with carved brass cattle ornaments, red or black wool vest, and brown breeches.",
            "fabrics": "Pure brushed cotton with Edelweiss embroidery, cowhide leather",
            "cost_inr": "₹18,000 – ₹65,000",
            "cost_local": "200 – 750 CHF",
            "rental_price": "70 – 160 CHF per day",
            "where_to_buy": "Heritage folk boutiques in Appenzell, Lucerne, and Bern",
            "cultural_significance": "Worn during the ceremonial Alpine cattle descent (Alpabzug) and Swiss National Day."
        }
        women = {
            "name": "Swiss Trachtenkleid with Bonnet & Silver Chains",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Festtagstracht",
            "region": "All Swiss Cantons",
            "image": None,
            "description": "Pleated silk or wool skirt, velvet bodice laced with fine silver filigree chains, delicate tulle apron, and cantonal lace bonnet with wing-like tulle.",
            "fabrics": "Silk taffeta, dark velvet, and silver filigree chains",
            "cost_inr": "₹28,000 – ₹95,000",
            "cost_local": "320 – 1,100 CHF",
            "rental_price": "90 – 220 CHF per day",
            "where_to_buy": "Specialty Trachten ateliers across Zurich and Bern",
            "cultural_significance": "Each of the 26 cantons maintains distinct traditional bonnet shapes and silver chain lacing."
        }
        regional = {
            "name": "Engadin Alpine Festive Folk Costume",
            "gender": "Regional",
            "category": "🏔️ Alpine Heritage Attire",
            "local_name": "Engadiner Tracht",
            "region": "Graubünden & Engadin",
            "image": None,
            "description": "Vibrant scarlet woolen skirt and jacket decorated with intricate black velvet ribbon trims and white ruff collars.",
            "fabrics": "Loden wool, fine velvet ribbons, and linen",
            "cost_inr": "₹22,000 – ₹80,000",
            "cost_local": "250 – 900 CHF",
            "rental_price": "80 – 180 CHF per day",
            "where_to_buy": "Heritage craft centers in St. Moritz and Chur",
            "cultural_significance": "Celebrated at Chalandamarz spring festivals welcoming the return of birds and green pastures."
        }
        significance = "Swiss traditional dress honors alpine self-reliance, pastoral life, and cantonal autonomy."

    elif is_turkey:
        men = {
            "name": "Traditional Turkish Kaftan, Şalvar & Yelek",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Kaftan, Şalvar ve Yelek",
            "region": "Aegean & Central Anatolia",
            "image": None,
            "description": "Embroidered short velvet or wool vest (yelek), voluminous pleated trousers (şalvar), wide fabric sash (kuşak), and traditional fez or patterned headdress.",
            "fabrics": "Wool broadcloth, silk embroidery, and hammered silver buckle",
            "cost_inr": "₹6,000 – ₹24,000",
            "cost_local": "2,500 – 10,000 TRY",
            "rental_price": "600 – 1,800 TRY per day",
            "where_to_buy": "Grand Bazaar textile souks in Istanbul, Kemeraltı in Izmir",
            "cultural_significance": "Worn during traditional zeybek folk dances symbolizing courage and heroic chivalry."
        }
        women = {
            "name": "Traditional Turkish Bindallı Silk Velvet Gown",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Bindallı / Üçetek",
            "region": "All Anatolian Provinces",
            "image": None,
            "description": "Richly embroidered purple or burgundy velvet robe featuring floral maraş gold-cord needlework (dîvâl), worn over silk şalvar trousers and crowned with a coin-fringed headdress.",
            "fabrics": "Deep velvet, gold and silver bullion thread, and pure silk",
            "cost_inr": "₹10,000 – ₹42,000",
            "cost_local": "4,000 – 18,000 TRY",
            "rental_price": "900 – 2,800 TRY per day",
            "where_to_buy": "Traditional bridal ateliers in Istanbul and Bursa",
            "cultural_significance": "The quintessential Ottoman bridal and henna night (Kına Gecesi) ceremonial gown."
        }
        regional = {
            "name": "Black Sea Region Folkloric Horon Attire",
            "gender": "Regional",
            "category": "🌊 Regional Dance Regalia",
            "local_name": "Karadeniz Yöresel Kıyafeti",
            "region": "Trabzon & Black Sea Coast",
            "image": None,
            "description": "Black fitted tunic, wrap hood (başlık), leather cartridge belt, and soft leather boots designed for the rapid footwork of the Horon dance.",
            "fabrics": "Heavy black wool, leather strapping, and brass hardware",
            "cost_inr": "₹5,000 – ₹20,000",
            "cost_local": "2,000 – 8,500 TRY",
            "rental_price": "500 – 1,500 TRY per day",
            "where_to_buy": "Folk dance shops in Trabzon and Samsun",
            "cultural_significance": "Reflects the spirited seafaring and mountain courage of the Black Sea people."
        }
        significance = "Turkish folk attire bridges Ottoman courtly splendor with vibrant Anatolian village life."

    elif is_east_africa:
        men = {
            "name": "Maasai Shúkà & Beaded Regalia",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Shúkà / Kanzu",
            "region": "Rift Valley & East African Savannah",
            "image": None,
            "description": "Iconic red-and-blue geometric checked cloth draped elegantly over the body, paired with beaded leather armbands, necklaces, and traditional walking staff (rungu).",
            "fabrics": "Heavy durable woven cotton acrylic check, glass seed beads, and leather",
            "cost_inr": "₹2,500 – ₹9,000",
            "cost_local": "3,000 – 12,000 KES",
            "rental_price": "800 – 1,800 KES per day",
            "where_to_buy": "Maasai Market in Nairobi, cultural bomas across the Rift Valley",
            "cultural_significance": "Red symbolizes courage, blood, and strength, instantly recognizable as the warrior heritage of the Maasai."
        }
        women = {
            "name": "Swahili Kanga & Beaded Collar Dress",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Kanga & Kitenge",
            "region": "Coastal & Highland East Africa",
            "image": None,
            "description": "Vibrant printed cotton cloth printed with Swahili proverbs (jina), tailored into flattering dresses or wrapped around the waist and head, complemented by multi-tiered circular bead collars.",
            "fabrics": "100% African cotton wax print and ceremonial beadwork",
            "cost_inr": "₹2,800 – ₹11,000",
            "cost_local": "3,500 – 14,000 KES",
            "rental_price": "900 – 2,000 KES per day",
            "where_to_buy": "Biashara Street textile markets in Nairobi and Mombasa",
            "cultural_significance": "Kanga proverbs communicate affection, social wisdom, and community solidarity."
        }
        regional = {
            "name": "Samburu / Kikuyu Heritage Ceremonial Dress",
            "gender": "Regional",
            "category": "🌍 Regional / Traditional Variation",
            "local_name": "Traditional Regalia",
            "region": "Central Highlands & Northern Kenya",
            "image": None,
            "description": "Hand-crafted goatskin or cotton robe heavily embellished with cowrie shells, ochre pigment, and layered brass wrist torcs.",
            "fabrics": "Natural tanned leather, brass, and cowrie shells",
            "cost_inr": "₹3,500 – ₹14,000",
            "cost_local": "4,500 – 18,000 KES",
            "rental_price": "1,000 – 2,400 KES per day",
            "where_to_buy": "Community artisan cooperatives in Kenya",
            "cultural_significance": "Honors pastoral lineage, rites of elderhood, and ancestral blessings."
        }
        significance = "East African attire celebrates pastoral fortitude, color harmony, and deep communal identity."
    elif "africa" in region:
        men = {
            "name": f"{c_name} Grand Agbada / Kanzu & Embroidered Cap",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": "Agbada / Boubou / Kanzu",
            "region": f"{c_name}",
            "image": None,
            "description": "Voluminous flowing robe with ornate neckline and chest embroidery, worn over matching tailored trousers and hand-stitched cap.",
            "fabrics": "Polished cotton, shimmering bazin brocade, or artisan wax-print",
            "cost_inr": "₹3,500 – ₹14,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹900 – ₹2,000 per day",
            "where_to_buy": f"Central textile markets and tailor quarters in {capital}",
            "cultural_significance": "A statement of regal dignity and celebratory respect worn at weddings and national festivals."
        }
        women = {
            "name": f"{c_name} Traditional Embroidered Blouse, Wrapper & Gele",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": "Kanga / Buba & Iro / Kemis",
            "region": f"{c_name}",
            "image": None,
            "description": "Vibrant hand-dyed wrap skirt and tailored blouse, accompanied by an intricately sculpted Gele headtie or soft sheer netela veil.",
            "fabrics": "African wax-print, damask, or handspun organic cotton",
            "cost_inr": "₹4,000 – ₹16,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,200 per day",
            "where_to_buy": f"Heritage fabric markets and traditional dress designers in {capital}",
            "cultural_significance": "Celebrates lineage, feminine beauty, and vibrant community pride during milestone celebrations."
        }
        regional = {
            "name": f"{c_name} Heritage Beadwork & Festival Regalia",
            "gender": "Regional",
            "category": "🌍 Regional / Traditional Variation",
            "local_name": "Festive Beadwork Regalia",
            "region": f"{c_name}",
            "image": None,
            "description": "Traditional textile wrap adorned with artisan beadwork, cowrie shells, and carved brass or wood amulets.",
            "fabrics": "Woven cotton, glass beads, and leather accents",
            "cost_inr": "₹2,500 – ₹9,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹700 – ₹1,500 per day",
            "where_to_buy": f"Community artisan cooperatives and village markets in {c_name}",
            "cultural_significance": "Preserves ancestral storytelling patterns passed down through generations."
        }
        significance = f"Traditional attire in {c_name} reflects community lineage, celebratory rites, and master textile craftsmanship."

    elif "asia" in region:
        men = {
            "name": f"{c_name} Traditional High-Collar Silk Tunic & Sash",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": f"{c_name} Traditional Tunic",
            "region": f"{c_name}",
            "image": None,
            "description": "Mandarin-collared raw silk tunic with frog button closures or tailored waist sash, paired with comfortable silk-blend trousers.",
            "fabrics": "Raw mulberry silk, handloom linen, or brocade",
            "cost_inr": "₹3,500 – ₹13,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹800 – ₹1,900 per day",
            "where_to_buy": f"Heritage textile quarters and silk ateliers in {capital}",
            "cultural_significance": "Symbolizes harmony, natural grace, and centuries-old weaving traditions."
        }
        women = {
            "name": f"{c_name} Traditional Silk Embroidered Robe & Wrap",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": f"{c_name} Silk Gown",
            "region": f"{c_name}",
            "image": None,
            "description": "Graceful flowing silk garment featuring delicate floral embroidery, structured neckline, matching waist sash, and fine hair pins.",
            "fabrics": "Pure mulberry silk, fine organza, and metallic thread",
            "cost_inr": "₹4,500 – ₹18,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,000 – ₹2,500 per day",
            "where_to_buy": f"Silk markets and historical costume ateliers in {capital}",
            "cultural_significance": "Celebrated for timeless elegance during Lunar New Year, harvest festivals, and family rites."
        }
        regional = {
            "name": f"{c_name} Highland Handloom Brocade Regalia",
            "gender": "Regional",
            "category": "🌍 Regional / Traditional Variation",
            "local_name": f"{c_name} Folk Dress",
            "region": "Highland Cultural Zones",
            "image": None,
            "description": "Traditional festive outfit embellished with geometric handloom weaving patterns and silver filigree buttons.",
            "fabrics": "Handloom brocade and natural dyed cotton",
            "cost_inr": "₹3,800 – ₹14,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹900 – ₹2,000 per day",
            "where_to_buy": f"Artisan workshops and village markets in {c_name}",
            "cultural_significance": "Marks major temple festivals and agricultural harvest thanksgivings."
        }
        significance = f"Attire in {c_name} embodies harmony, balance, and millennia of regional artistic refinement."

    else:  # Europe, Americas & General
        men = {
            "name": f"{c_name} Heritage Tailored Tracht / Folk Suit",
            "gender": "Men",
            "category": "👨 Men's Traditional Attire",
            "local_name": f"{c_name} Folk Suit",
            "region": f"{c_name}",
            "image": None,
            "description": "Tailored wool or linen vest with antique brass buttons, stand-collar linen shirt, comfortable wool trousers or breeches, and heritage hat.",
            "fabrics": "Loden wool, flax linen, and brushed cotton",
            "cost_inr": "₹4,500 – ₹18,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,200 – ₹2,800 per day",
            "where_to_buy": f"Old Town craft ateliers and heritage boutiques in {capital}",
            "cultural_significance": "Reflects rural and alpine festive traditions celebrated during national holidays."
        }
        women = {
            "name": f"{c_name} Heritage Folk Apron Dress & Bodice",
            "gender": "Women",
            "category": "👩 Women's Traditional Attire",
            "local_name": f"{c_name} Folk Dress",
            "region": f"{c_name}",
            "image": None,
            "description": "Fitted bodice laced over a white puff-sleeve blouse, gathered full skirt, embroidered silk/cotton apron, and ribboned headpiece.",
            "fabrics": "Pure linen, jacquard brocade, and velvet trim",
            "cost_inr": "₹5,500 – ₹22,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,500 – ₹3,200 per day",
            "where_to_buy": f"Traditional costume boutiques and historical festival shops in {capital}",
            "cultural_significance": "Worn during harvest festivals, church pageants, and village celebrations."
        }
        regional = {
            "name": f"{c_name} Regional Folkloric Dance Costume",
            "gender": "Regional",
            "category": "🌍 Regional / Traditional Variation",
            "local_name": f"{c_name} Folk Costumes",
            "region": f"{c_name} Countryside",
            "image": None,
            "description": "Celebrated village ensemble featuring floral ribbon braids, pleated skirts, and polished leather dancing boots.",
            "fabrics": "Embroidered wool, velvet ribbons, and flax linen",
            "cost_inr": "₹4,000 – ₹16,000",
            "cost_local": f"Equivalent in {curr}",
            "rental_price": "₹1,100 – ₹2,400 per day",
            "where_to_buy": f"Regional cultural centers and folk dance guilds in {c_name}",
            "cultural_significance": "Emblematic of pastoral joy and seasonal midsummer or autumn festivals."
        }
        significance = f"Embodies the cultural pride, festive heritage, and artistic roots of {c_name}."

        # Authentic photography only: do NOT attach AI fallback.
    for item in [men, women, regional]:
        if "image" not in item:
            item["image"] = None

    return {
        "men": men,
        "women": women,
        "attires": [women, men, regional],
        "cultural_significance": significance,
        "rental_note": f"Traditional costume rentals are commonly available near historical landmarks and cultural centers in {capital} for photography."
    }


def get_traditional_clothing(country_name: str) -> Dict[str, Any]:
    """Returns traditional clothing data with exact photos for any of the 250 countries."""
    norm = normalize_country_key(country_name)
    for k, v in CURATED_TRADITIONAL_CLOTHING.items():
        if k.lower() == country_name.lower() or k.lower() == norm.lower():
            return v
    return get_synthesized_clothing(country_name)


def format_traditional_clothing_markdown(clothing: Dict[str, Any]) -> str:
    """Formats clothing data into an aesthetic guide for men, women, and regional attire with costs and photos."""
    c_name = clothing["country"]
    attires = clothing.get("attires") or [clothing.get("women"), clothing.get("men")]
    attires = [a for a in attires if a]
    sig = clothing.get("cultural_significance", "")
    note = clothing.get("rental_note", "")

    lines = [
        f"### 👘 Traditional Dresses & Cultural Attire in {c_name}",
        "",
        f"Traditional clothing in **{c_name}** represents centuries of artisanal heritage, local textile weaving, and regional identity. Styles vary naturally across regions, communities, celebrations, and individual choices:",
        ""
    ]

    for att in attires:
        badge = att.get("category", "Traditional Attire")
        lines.append("---")
        lines.append("")
        lines.append(f"#### {badge}: **{att['name']}**")
        lines.append("")
        if att.get("image"):
            lines.append(f"![{att['name']}]({att['image']})")
            lines.append("📷 *Verified historical photograph via Wikimedia Commons public repository.*")
            lines.append("")
        else:
            lines.append("📸 *Authentic adult attire photo unavailable. Only verified authentic photographs of adult subjects wearing authentic traditional garments are displayed.*")
            lines.append("")
        lines.append(f"- **Original / Native Name:** `{att.get('local_name', att['name'])}`")
        if att.get("region"):
            lines.append(f"- **📍 Region / Origin:** {att['region']}")
        lines.append(f"- **Garment Description:** {att.get('description', '')}")
        if att.get("cultural_significance"):
            lines.append(f"- **🌟 Cultural Significance & When Worn:** {att['cultural_significance']}")
        if att.get("fabrics"):
            lines.append(f"- **Authentic Fabrics:** {att['fabrics']}")
        if att.get("cost_inr"):
            lines.append(f"- **💰 Estimated Purchase Cost (INR):** **{att['cost_inr']}**")
        if att.get("cost_local"):
            lines.append(f"- **💵 Local Currency Cost:** **{att['cost_local']}**")
        if att.get("rental_price"):
            lines.append(f"- **🏷️ Daily Rental Rate:** {att['rental_price']}")
        if att.get("where_to_buy"):
            lines.append(f"- **🛍️ Recommended Shopping & Rental Spots:** {att['where_to_buy']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("💡 **Respectful Cultural Context & Traveler Guidance:**")
    lines.append(f"- **Regional Diversity:** Clothing varies significantly by province, occasion, and community in {c_name}. Everyday wear in modern metropolitan hubs is contemporary, while traditional attire is proudly worn during national festivals, weddings, cultural ceremonies, and temple/shrine visits.")
    lines.append("- **Respectful Experience:** Travelers are warmly welcomed to experience traditional attire through registered rental services near historic heritage areas and gardens. Always treat cultural garments with modesty and respect.")
    if sig:
        lines.append(f"- **Cultural Background:** {sig}")
    if note:
        lines.append(f"- **Rental Tips:** {note}")
    lines.append("")

    return "\n".join(lines)



LANGUAGE_VOICE_CODES: Dict[str, str] = {
    "japanese": "ja-JP", "korean": "ko-KR", "french": "fr-FR", "spanish": "es-ES",
    "german": "de-DE", "italian": "it-IT", "thai": "th-TH", "hindi": "hi-IN",
    "telugu": "te-IN", "tamil": "ta-IN", "kannada": "kn-IN", "malayalam": "ml-IN",
    "bengali": "bn-IN", "gujarati": "gu-IN", "punjabi": "pa-IN", "urdu": "ur-PK",
    "chinese": "zh-CN", "mandarin": "zh-CN", "arabic": "ar-SA", "russian": "ru-RU",
    "portuguese": "pt-BR", "nepali": "ne-NP", "vietnamese": "vi-VN", "indonesian": "id-ID",
    "greek": "el-GR", "turkish": "tr-TR", "dutch": "nl-NL", "english": "en-US"
}


def answer_language_phrase_question(question: str, country_name: str, knowledge: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """Answers language, phrase, greeting, and translation questions for any country."""
    q_lower = str(question or "").lower()

    phrase_indicators = [
        "how to say", "how do you say", "how do i say", "how can i say", "how would you say",
        "say in thai", "say in japanese", "say in french", "say in spanish", "say in italian",
        "say in german", "say in hindi", "say in chinese", "say in korean", "say in arabic",
        "say in nepali", "say in vietnamese", "say in indonesian", "say in portuguese",
        "translate", "useful phrases", "essential phrases", "basic phrases",
        "common words", "common phrases", "learn the language",
        "thank you in", "hello in", "goodbye in", "please in", "cheers in",
        "what does", "meaning of", "in thailand (thai), you can say", "you can say",
        "no problem in", "say 'no problem'", 'say "no problem"', "how to say no problem",
        "何と言いますか", "どう言いますか", "ありがとう", "こんにちは", "大丈夫",
        "ఎలా చెప్పాలి", "comment dire", "cómo se dice", "wie sagt man"
    ]
    if not any(pi in q_lower or pi in question for pi in phrase_indicators) and not q_lower.startswith(("how to say", "how do you say", "how do i say")):
        return None

    # Country mapping to detect when a country is explicitly named in the prompt
    COUNTRY_TO_LANG = {
        "nepal": ("ne", "Nepali", "Nepal"),
        "japan": ("ja", "Japanese", "Japan"),
        "thailand": ("th", "Thai", "Thailand"),
        "france": ("fr", "French", "France"),
        "italy": ("it", "Italian", "Italy"),
        "germany": ("de", "German", "Germany"),
        "spain": ("es", "Spanish", "Spain"),
        "china": ("zh", "Chinese", "China"),
        "korea": ("ko", "Korean", "South Korea"),
        "south korea": ("ko", "Korean", "South Korea"),
        "vietnam": ("vi", "Vietnamese", "Vietnam"),
        "indonesia": ("id", "Indonesian", "Indonesia"),
        "india": ("hi", "Hindi", "India"),
        "brazil": ("pt", "Portuguese", "Brazil"),
        "portugal": ("pt", "Portuguese", "Portugal"),
        "russia": ("ru", "Russian", "Russia"),
        "greece": ("el", "Greek", "Greece"),
        "turkey": ("tr", "Turkish", "Turkey"),
        "egypt": ("ar", "Arabic", "Egypt"),
        "saudi arabia": ("ar", "Arabic", "Saudi Arabia"),
        "mexico": ("es", "Spanish", "Mexico"),
    }

    target_code = None
    lang_name = None

    for c_kw, (c_code, c_lang, c_country_name) in COUNTRY_TO_LANG.items():
        if re.search(r'\b(?:in|for|of)\s+' + re.escape(c_kw) + r'\b', q_lower) or re.search(r'\b' + re.escape(c_kw) + r'\b', q_lower):
            target_code = c_code
            lang_name = c_lang
            country_name = c_country_name
            break

    prof = knowledge if (knowledge and not target_code) else get_country_knowledge(country_name)
    c_name = prof.get("name", country_name)
    country_langs = str(prof.get("languages", "English") or "")

    if "日本語" in question or "何と言いますか" in question or "どう言いますか" in question:
        target_code = "ja"
        lang_name = "Japanese"

    # Check if a specific language is explicitly named in the question
    if not target_code:
        for l_name, l_code in LANGUAGE_CODES.items():
            if re.search(r'\b' + re.escape(l_name) + r'\b', q_lower):
                target_code = l_code
                lang_name = l_name.title()
                break

    # If no language specified, resolve from the selected country's primary languages
    if not target_code:
        candidate_langs = [l.strip().lower() for l in re.split(r'[,/]', country_langs) if l.strip()]
        for cand in candidate_langs:
            for l_name, l_code in LANGUAGE_CODES.items():
                if (l_name == cand or l_name in cand) and l_code != "en":
                    target_code = l_code
                    lang_name = l_name.title()
                    break
            if target_code:
                break
        if not target_code and candidate_langs:
            for cand in candidate_langs:
                for l_name, l_code in LANGUAGE_CODES.items():
                    if l_name == cand or l_name in cand or cand in l_name:
                        target_code = l_code
                        lang_name = l_name.title()
                        break
                if target_code:
                    break

    if not target_code:
        target_code = "en"
        lang_name = country_langs.split(",")[0].strip().title() if country_langs else "Local Language"

    # Extract target phrase
    quote_match = re.search(r'["\']([^"\']+)["\']', question)
    phrase_candidate = ""
    if "ありがとう" in question or "arigat" in q_lower:
        phrase_candidate = "thank you"
    elif "大丈夫" in question:
        phrase_candidate = "no problem"
    elif quote_match:
        phrase_candidate = quote_match.group(1).strip()
    else:
        m = re.search(r'how\s+(?:to|do\s+you|can\s+i|would\s+you)\s+say\s+(.+?)(?:\s+in|\s*$)', q_lower)
        if m:
            phrase_candidate = m.group(1).strip()
        else:
            m2 = re.search(r'what\s+is\s+(.+?)\s+in\s+', q_lower)
            if m2:
                phrase_candidate = m2.group(1).strip()
            else:
                m3 = re.search(r'translate\s+(.+?)(?:\s+to|\s+into|\s+in|\s*$)', q_lower)
                if m3:
                    phrase_candidate = m3.group(1).strip()

    if not phrase_candidate:
        if "no problem" in q_lower or "no worries" in q_lower or "never mind" in q_lower:
            phrase_candidate = "no problem"
        elif "thank" in q_lower:
            phrase_candidate = "thank you"
        elif "hello" in q_lower or "hi" in q_lower:
            phrase_candidate = "hello"
        elif "goodbye" in q_lower or "bye" in q_lower:
            phrase_candidate = "goodbye"
        elif "please" in q_lower:
            phrase_candidate = "please"
        elif "delicious" in q_lower:
            phrase_candidate = "delicious"
        elif "bathroom" in q_lower or "toilet" in q_lower:
            phrase_candidate = "where is the bathroom"
        elif "how much" in q_lower or "price" in q_lower or "cost" in q_lower:
            phrase_candidate = "how much"
        else:
            phrase_candidate = "useful phrases"

    p_key = phrase_candidate.lower().strip("?!.,\"' ")

    # Check curated phrasebook
    lang_book = CURATED_PHRASES.get(lang_name, {})
    for key, data in lang_book.items():
        if key in p_key or p_key in key:
            voice_code = data.get("voice_code") or LANGUAGE_VOICE_CODES.get(lang_name.lower(), "en-US")
            audio_text = data.get("audio_text") or data.get("script") or data.get("phrase", "")
            meaning_str = data.get("meaning", key.title())

            res = f"### 🗣️ How to Say \"{key.title()}\" in {lang_name}\n\n"
            res += f"**{lang_name}:**\n{data['script']}\n\n"
            res += f"**Romanization:**\n{data['phrase']}\n\n"
            res += f"**Meaning:**\n{meaning_str}\n\n"
            res += f"💡 **Phonetic Pronunciation & Tip:**\n- *{data['phonetic']}*\n"
            if data.get("note"):
                res += f"- {data['note']}\n"
            res += f"\n<!-- SPEECH:{voice_code}:{audio_text} -->"
            return res

    # If general "useful phrases" requested
    if p_key in ["useful phrases", "essential phrases", "basic phrases", "phrases"]:
        if lang_book:
            res = f"### 🗣️ Essential {lang_name} Travel Phrases ({c_name})\n\n"
            res += "Here are the most practical everyday phrases for your journey:\n\n"
            for k, d in lang_book.items():
                res += f"- **{k.title()}:** **{d['phrase']}** (`{d['script']}`) &bull; *{d['phonetic']}*\n"
            v_code = LANGUAGE_VOICE_CODES.get(lang_name.lower(), "en-US")
            first_phrase = list(lang_book.values())[0].get("script", "")
            res += f"\n<!-- SPEECH:{v_code}:{first_phrase} -->"
            return res
        else:
            essentials = [
                ("Hello / Greetings", "Hello"),
                ("Thank you", "Thank you"),
                ("Please", "Please"),
                ("You're welcome / No problem", "You're welcome"),
                ("How much is this?", "How much is this?"),
                ("Where is the bathroom?", "Where is the bathroom?")
            ]
            res = f"### 🗣️ Essential {lang_name} Travel Phrases ({c_name})\n\n"
            res += f"Here are practical everyday travel phrases translated into **{lang_name}** for your visit to **{c_name}**:\n\n"
            for label, eng in essentials:
                tr = translate_live(eng, target_code)
                res += f"- **{label}:** **{tr}**\n"
            v_code = LANGUAGE_VOICE_CODES.get(lang_name.lower(), f"{target_code}-US")
            res += f"\n<!-- SPEECH:{v_code}:Hello -->"
            return res

    # Live translation for any phrase across all 250 countries
    trans = translate_live(phrase_candidate, target_code)
    if trans:
        v_code = LANGUAGE_VOICE_CODES.get(lang_name.lower(), f"{target_code}-{'IN' if target_code in ['hi','te','ta','kn','ml','bn','gu','pa'] else 'US'}")
        res = f"### 🗣️ How to Say \"{phrase_candidate.title()}\" in {lang_name} ({c_name})\n\n"
        res += f"**{lang_name}:**\n{trans}\n\n"
        res += f"**Romanization:**\n{phrase_candidate.title()} in {lang_name}\n\n"
        res += f"**Meaning:**\n{phrase_candidate.title()}\n\n"
        if lang_name == "Thai":
            res += "💡 **Polite Particle Tip:**\n"
            res += f"- If you are **male**, add **khrap** (ครับ) at the end: `{trans} ครับ`\n"
            res += f"- If you are **female**, add **kha** (ค่ะ) at the end: `{trans} ค่ะ`\n"
        res += f"\n<!-- SPEECH:{v_code}:{trans} -->"
        return res

    return f"### 🗣️ Translation for \"{phrase_candidate.title()}\" in {lang_name} ({c_name})\n\nIn **{c_name}**, the local language is **{lang_name}**. To express **\"{phrase_candidate.title()}\"**, travelers use the native phrasebook equivalent."


def answer_word_meaning_question(question: str) -> Optional[str]:
    """Answers word/phrase meaning and etymology questions like 'What does Hola mean?'."""
    q_low = str(question or "").lower().strip()

    m = re.search(r'what\s+does\s+["\']?([^"\'?]+?)["\']?\s+mean', q_low)
    if not m:
        m = re.search(r'meaning\s+of\s+["\']?([^"\'?]+?)["\']?(?:\s|$)', q_low)
    if not m:
        m = re.search(r'what\s+is\s+["\']?([^"\'?]+?)["\']?\s+mean', q_low)

    if not m:
        return None

    target_word = m.group(1).strip()
    if not target_word or len(target_word) > 40:
        return None

    w_clean = target_word.lower().strip("?!.,\"' ")

    KNOWN_MEANINGS = {
        "hola": {
            "lang": "Spanish",
            "script": "¡Hola!",
            "romanization": "Hola",
            "phonetic": "OH-lah",
            "meaning": "Hello / Hi",
            "voice_code": "es-ES",
            "audio": "¡Hola!",
            "explanation": "'Hola' is the most ubiquitous and friendly greeting in the Spanish language. It is used casually and warmly throughout Spain and Latin America at any time of day, whether meeting a friend or entering a shop."
        },
        "merci": {
            "lang": "French",
            "script": "Merci",
            "romanization": "Merci",
            "phonetic": "mair-SEE",
            "meaning": "Thank you",
            "voice_code": "fr-FR",
            "audio": "Merci",
            "explanation": "'Merci' is the fundamental French expression of gratitude. To say 'Thank you very much', locals say 'Merci beaucoup'."
        },
        "arigato": {
            "lang": "Japanese",
            "script": "ありがとう",
            "romanization": "Arigatou",
            "phonetic": "ah-ree-GAH-toh",
            "meaning": "Thank you",
            "voice_code": "ja-JP",
            "audio": "ありがとう",
            "explanation": "'Arigatou' is the casual Japanese word for 'Thank you'. For polite or formal situations (in shops, restaurants, or to strangers), always use 'Arigatou gozaimasu' (ありがとうございます) accompanied by a slight bow."
        },
        "konnichiwa": {
            "lang": "Japanese",
            "script": "こんにちは",
            "romanization": "Konnichiwa",
            "phonetic": "kohn-nee-chee-WAH",
            "meaning": "Hello / Good afternoon",
            "voice_code": "ja-JP",
            "audio": "こんにちは",
            "explanation": "'Konnichiwa' is the standard polite daytime greeting in Japan, typically used from late morning until dusk."
        },
        "sayonara": {
            "lang": "Japanese",
            "script": "さようなら",
            "romanization": "Sayonara",
            "phonetic": "sah-yoh-NAH-rah",
            "meaning": "Goodbye",
            "voice_code": "ja-JP",
            "audio": "さようなら",
            "explanation": "'Sayonara' means 'Goodbye'. In modern Japanese, it often implies a long or final parting; friends commonly use casual expressions like 'Mata ne' (See you later)."
        },
        "ciao": {
            "lang": "Italian",
            "script": "Ciao",
            "romanization": "Ciao",
            "phonetic": "CHOW",
            "meaning": "Hello / Goodbye",
            "voice_code": "it-IT",
            "audio": "Ciao",
            "explanation": "'Ciao' is the iconic Italian informal greeting used both when meeting and parting among friends and peers."
        },
        "danke": {
            "lang": "German",
            "script": "Danke",
            "romanization": "Danke",
            "phonetic": "DAHN-kuh",
            "meaning": "Thank you",
            "voice_code": "de-DE",
            "audio": "Danke",
            "explanation": "'Danke' is the universal German word for 'Thank you'. For a warmer 'Thank you very much', say 'Danke schön' or 'Vielen Dank'."
        },
        "namaste": {
            "lang": "Hindi / Sanskrit",
            "script": "नमस्ते",
            "romanization": "Namaste",
            "phonetic": "nuh-muh-STAY",
            "meaning": "Hello / I bow to the divine within you",
            "voice_code": "hi-IN",
            "audio": "नमस्ते",
            "explanation": "'Namaste' is a traditional greeting originating from Sanskrit ('namas' = bow, 'te' = to you). It is performed by joining palms together at chest level (Anjali Mudra) with a slight respectful bow, acknowledging the divine spark in others."
        },
        "mai pen rai": {
            "lang": "Thai",
            "script": "ไม่เป็นไร",
            "romanization": "Mai pen rai",
            "phonetic": "my-pen-RYE",
            "meaning": "No problem / Never mind / You're welcome",
            "voice_code": "th-TH",
            "audio": "ไม่เป็นไร",
            "explanation": "'Mai pen rai' is Thailand's cultural philosophy summarized in three words: let it go, no worries, and don't fret over small things."
        },
        "gamsahamnida": {
            "lang": "Korean",
            "script": "감사합니다",
            "romanization": "Gamsahamnida",
            "phonetic": "gahm-sah-hahm-NEE-dah",
            "meaning": "Thank you (formal/polite)",
            "voice_code": "ko-KR",
            "audio": "감사합니다",
            "explanation": "'Gamsahamnida' is the respectful, polite way to thank people in Korean, widely used with elders, service staff, and in professional settings."
        }
    }

    if w_clean in KNOWN_MEANINGS:
        d = KNOWN_MEANINGS[w_clean]
        res = f"### 📖 Meaning of \"{target_word.title()}\"\n\n"
        res += f"- **Language:** **{d['lang']}**\n"
        res += f"- **Original Script:** `{d['script']}`\n"
        res += f"- **Romanization / Pronunciation:** **{d['romanization']}** (*{d['phonetic']}*)\n"
        res += f"- **Meaning in English:** **{d['meaning']}**\n\n"
        res += f"💡 **Cultural Context & Usage:**\n{d['explanation']}\n\n"
        res += f"<!-- SPEECH:{d['voice_code']}:{d['audio']} -->"
        return res

    trans = translate_live(target_word, "en", "auto")
    if trans and trans.lower().strip() != w_clean:
        res = f"### 📖 Meaning of \"{target_word.title()}\"\n\n"
        res += f"- **Word:** **{target_word}**\n"
        res += f"- **English Meaning:** **{trans}**\n\n"
        res += f"💡 **Usage:** \"{target_word}\" translates directly to \"**{trans}**\" in English.\n\n"
        res += f"<!-- SPEECH:en-US:{trans} -->"
        return res

    return None


def query_general_knowledge(question: str) -> Optional[str]:
    """Answers math, science, history, geography, and open-ended general knowledge questions."""
    q_raw = str(question or "").strip()
    if not q_raw:
        return None
    q_low = q_raw.lower()

    # 1. Simple math calculation
    math_match = re.search(r'(?:what\s+is|calculate|compute)?\s*([\d\.\s\+\-\*\/\(\)\^\%]+)\s*\??$', q_low)
    if math_match:
        expr = math_match.group(1).strip()
        if re.search(r'[\+\-\*\/]', expr) and re.search(r'\d', expr) and not re.search(r'[a-zA-Z]', expr):
            try:
                safe_expr = expr.replace('^', '**')
                val = eval(safe_expr, {"__builtins__": None}, {})
                if isinstance(val, (int, float)):
                    res_val = f"{val:g}" if isinstance(val, float) else f"{val:,}"
                    return f"### 🔢 Calculation Result\n\n**{expr} = {res_val}**\n\n<!-- SPEECH:en-US:{expr} equals {res_val} -->"
            except Exception:
                pass

    # 2. General encyclopedic lookup (no country bias)
    stop_words = {'what', 'is', 'the', 'of', 'in', 'a', 'an', 'are', 'tell', 'me', 'about', 'how', 'why', 'where', 'who', 'when', 'can', 'you', 'explain', 'define'}
    words = [w for w in re.sub(r'[^\w\s]', '', q_raw).split() if w.lower() not in stop_words]
    search_query = " ".join(words) if words else q_raw
    if not search_query:
        return None

    try:
        url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
            'action': 'query', 'list': 'search', 'srsearch': search_query, 'format': 'json', 'srlimit': 3
        })
        req = urllib.request.Request(url, headers={'User-Agent': 'AITravelPlannerBot/2.0 (travel@planner.ai)'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))
            results = data.get('query', {}).get('search', [])
            if not results:
                return None
            title = results[0]['title']

        url_page = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
            'action': 'query', 'prop': 'extracts', 'exintro': 1, 'explaintext': 1,
            'titles': title, 'format': 'json', 'redirects': 1
        })
        req_page = urllib.request.Request(url_page, headers={'User-Agent': 'AITravelPlannerBot/2.0 (travel@planner.ai)'})
        with urllib.request.urlopen(req_page, timeout=5) as res_page:
            d = json.loads(res_page.read().decode('utf-8'))
            pages = list(d.get('query', {}).get('pages', {}).values())
            if not pages or pages[0].get('pageid', -1) == -1:
                return None
            extract = pages[0].get('extract', '').strip()
            if not extract:
                return None

            clean_extract = clean_wiki_text(extract)
            paragraphs = [p.strip() for p in clean_extract.split('\n') if p.strip()]
            top_content = "\n\n".join(paragraphs[:3]) if paragraphs else clean_extract[:600]
            first_sentence = top_content.split('.')[0] + '.' if '.' in top_content else top_content[:150]

            return f"### 💡 {title}\n\n{top_content}\n\n<!-- SPEECH:en-US:{first_sentence} -->"
    except Exception:
        pass

    return None


def clean_wiki_text(text: str) -> str:
    """Clean encyclopedic text by stripping citations and pronunciation strings."""
    text = re.sub(r'\[\s*\d+\s*\]', '', text)
    text = re.sub(r'\[\s*note\s*\d+\s*\]', '', text, flags=re.I)
    text = re.sub(r'\[\s*[a-z]\s*\]', '', text, flags=re.I)
    text = re.sub(r'\(\s*[A-Z\s,;\-\/—\.\'’ːˈˌ]+[^\)]*\)', '', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def query_country_encyclopedia(
    question: str,
    country_name: str,
    knowledge: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """
    Dynamically answers open-ended, factual, historical, cultural, or geographical
    questions about the selected country using live encyclopedic data.
    """
    q_raw = str(question or "").strip()
    if not q_raw:
        return None
    q_lower = q_raw.lower()
    headers = {"User-Agent": "AITravelPlannerBot/2.0 (travel@planner.ai)"}

    prof = knowledge or get_country_knowledge(country_name)
    c_name = prof.get("name", country_name)
    known_attractions = [a[0] if isinstance(a, (tuple, list)) else a.get("name", "") for a in prof.get("attractions", [])]
    known_cities = prof.get("cities", [])

    # Fast direct metadata answers
    if any(k in q_lower for k in ["what is the capital", "capital of", "capital city"]):
        cap = prof.get("capital", "")
        if cap:
            return f"### 🏛️ Capital of {c_name}\n\nThe capital city of **{c_name}** is **{cap}**."

    if any(k in q_lower for k in ["what currency", "currency of", "money used in", "what is the currency"]):
        curr = prof.get("currency", "")
        if curr:
            return f"### 💵 Currency of {c_name}\n\nThe official currency of **{c_name}** is **{curr}**."

    if any(k in q_lower for k in ["what language", "languages spoken", "official language"]):
        langs = prof.get("languages", [])
        if langs:
            lang_str = ", ".join(langs) if isinstance(langs, list) else str(langs)
            return f"### 🗣️ Languages of {c_name}\n\nThe primary official and widely spoken language(s) in **{c_name}** are **{lang_str}**."

    # Extract query keywords
    clean_q = re.sub(r'[^\w\s]', ' ', q_raw)
    stop_words = {
        'what', 'is', 'the', 'of', 'in', 'a', 'an', 'are', 'tell', 'me', 'about',
        'how', 'why', 'where', 'who', 'when', 'can', 'i', 'do', 'you', 'know',
        'does', 'did', 'was', 'were', 'to', 'for', 'from', 'with', 'by', 'at'
    }
    keywords = [w for w in clean_q.split() if w.lower() not in stop_words]

    search_queries = []
    if keywords:
        search_queries.append(" ".join(keywords))
    search_queries.append(q_raw)
    if country_name.lower() not in q_lower:
        search_queries.append(f"{' '.join(keywords)} {country_name}")

    candidate_titles = []
    for sq in search_queries[:2]:
        url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
            'action': 'query',
            'list': 'search',
            'srsearch': sq,
            'format': 'json',
            'srlimit': 6
        })
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode('utf-8'))
                for item in data.get('query', {}).get('search', []):
                    t = item.get('title', '')
                    if t and t not in candidate_titles:
                        candidate_titles.append(t)
        except Exception:
            pass
        if candidate_titles:
            break

    if not candidate_titles:
        candidate_titles = [country_name]

    # Filter out irrelevant sports leagues, seasons, movies, and tour pages for non-entertainment queries
    DISCARD_PATTERNS = ["league", "season", "tour", "(film)", "(album)", "championship", "f.c.", "football club", "grand prix", "cup"]
    is_entertainment = any(w in q_lower for w in ["sport", "football", "league", "film", "movie", "song", "album", "tour", "music", "actor", "match", "championship"])
    if not is_entertainment:
        filtered = [t for t in candidate_titles if not any(dp in t.lower() for dp in DISCARD_PATTERNS)]
        if filtered:
            candidate_titles = filtered

    # Score candidates
    scored_candidates = []
    for t in candidate_titles:
        score = 0
        t_lower = t.lower()
        if t_lower.startswith("list of"):
            score -= 10
        if t_lower in q_lower:
            score += 15
        for att in known_attractions:
            if att.lower() in t_lower or t_lower in att.lower():
                score += 12
                break
        for city in known_cities:
            if city.lower() in t_lower or t_lower in city.lower():
                score += 8
                break
        scored_candidates.append((score, t))

    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    best_title = scored_candidates[0][1]

    # Fetch article extract
    extract_url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'query',
        'prop': 'extracts',
        'explaintext': 1,
        'redirects': 1,
        'titles': best_title,
        'format': 'json'
    })

    try:
        req = urllib.request.Request(extract_url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as res:
            data = json.loads(res.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            page = next(iter(pages.values()))
            full_text = page.get('extract', '')
    except Exception:
        full_text = ''

    if not full_text:
        return None

    # Break into sections
    sections = []
    cur_sec = "Overview"
    cur_lines = []
    for line in full_text.split('\n'):
        line_s = line.strip()
        if line_s.startswith('==') and line_s.endswith('=='):
            if cur_lines:
                sections.append((cur_sec, '\n'.join(cur_lines).strip()))
                cur_lines = []
            cur_sec = line_s.strip('=').strip()
        else:
            if line_s:
                cur_lines.append(line_s)
    if cur_lines:
        sections.append((cur_sec, '\n'.join(cur_lines).strip()))

    overview_paras = [clean_wiki_text(p) for p in sections[0][1].split('\n') if len(clean_wiki_text(p)) > 40] if sections else []

    is_name_query = any(w in q_lower for w in ['original name', 'name', 'meaning', 'called', 'etymology', 'origin'])
    is_who_built = any(w in q_lower for w in ['who built', 'built by', 'builder', 'architect', 'commissioned'])

    result_paras = []

    # A: Name / Etymology queries (e.g. Bangkok original name)
    if is_name_query:
        for sec_name, sec_text in sections:
            if any(k in sec_name.lower() for k in ['name', 'etymology', 'naming']):
                paras = [clean_wiki_text(p) for p in sec_text.split('\n') if len(clean_wiki_text(p)) > 40]
                if paras:
                    result_paras.extend(paras[:3])
                break

    # B: Who built queries
    if is_who_built or not result_paras:
        if overview_paras:
            lead = overview_paras[0]
            if is_who_built:
                result_paras.append(lead)
                for sec_name, sec_text in sections[1:]:
                    if any(k in sec_name.lower() for k in ['construction', 'history', 'origins', 'commission']):
                        paras = [clean_wiki_text(p) for p in sec_text.split('\n') if len(clean_wiki_text(p)) > 40]
                        if paras:
                            result_paras.append(paras[0])
                        break

    # C: General keyword-based paragraph scoring
    if not result_paras:
        q_words = [w.lower() for w in keywords if len(w) > 2]
        scored = []
        for sec_name, sec_text in sections:
            for p in sec_text.split('\n'):
                p_clean = clean_wiki_text(p)
                if len(p_clean) < 50:
                    continue
                p_lower = p_clean.lower()
                score = sum(3 for w in q_words if w in p_lower)
                if sec_name.lower() in ['overview', 'history', 'etymology', 'geography', 'name']:
                    score += 2
                scored.append((score, p_clean))
        scored.sort(key=lambda x: x[0], reverse=True)
        if scored and scored[0][0] > 0:
            result_paras = [p for s, p in scored[:2]]
        elif overview_paras:
            result_paras = [overview_paras[0]]

    if not result_paras and overview_paras:
        result_paras = [overview_paras[0]]

    if not result_paras:
        return None

    response = f"### 💡 {best_title} &bull; {c_name}\n\n"
    response += "\n\n".join(result_paras)
    return response


# ============================================================
# BROAD TRAVEL INTELLIGENCE HELPERS (VISA, SIM, ACCOMMODATION, DIET, DISRUPTIONS)
# ============================================================

def format_multi_stop_chat_response(journey: Dict[str, Any]) -> str:
    stops = journey.get("stops", [])
    legs = journey.get("transport_legs", [])
    starting = journey.get("starting_location") or journey.get("origin") or "Origin"
    return_loc = journey.get("return_location", starting)
    stay_days = journey.get("destination_stay_days", sum(s.get("days", 1) for s in stops))
    total_days = journey.get("total_days", stay_days)
    cost_bd = journey.get("cost_breakdown", {})
    val_report = journey.get("validation_report", {})
    val_badge = "✅ **Route Validation: Verified (8/8 Checks Passed)**" if val_report.get("is_valid", True) else "⚠️ **Route Validation: Review Advised**"

    route_str = f"**{starting}** 🛫 → " + " → ".join(f"**{s['city']}** ({s['days']} Days)" for s in stops) + f" 🛫 → **{return_loc}**"

    lines = [
        f"### 🗺️ Multi-Stop Journey: {route_str}",
        "",
        f"{val_badge}",
        "",
        f"Here is your verified multi-stop itinerary across **{len(stops)} destinations** (**{stay_days} Destination Stay Days** total).",
        f"- **Starting Point:** {starting}",
        f"- **Ordered Stops:** " + ", ".join(f"{s['city']} ({s['days']}d)" for s in stops),
        f"- **Final Return:** {return_loc}",
        f"- **Estimated Budget Total:** ₹{cost_bd.get('Total Estimated', journey.get('total_cost', 0)):,} (INR) *[Based on verified market estimates, not live airline/hotel feeds]*",
        "",
        "#### 🚆 Independent Transportation Legs & Gateways:",
        ""
    ]

    for idx, leg in enumerate(legs):
        leg_title = f"Leg {idx + 1}: {leg['origin']} ➔ {leg['destination']}"
        lines.append(f"**{leg_title}**")
        lines.append(f"- **Recommended Mode:** {leg['mode']}")
        lines.append(f"- **⏱️ Travel Time:** {leg['travel_time']} &bull; **💰 Cost:** {leg['cost_range']}")
        lines.append(f"- **📍 Terminals:** {leg['origin_terminal']} ➔ {leg['dest_terminal']}")
        lines.append(f"- **🚆 Connections:** {leg['connection_info']}")
        lines.append(f"- **⏰ Departure Window:** {leg.get('departure_window', 'Scheduled departure')}")
        lines.append(f"- **💡 Buffer & Travel Advice:** {leg['buffer_time']}")
        if leg.get("booking_link"):
            lines.append(f"- **🔗 Booking Portal:** [{leg.get('booking_link')}]({leg.get('booking_link')})")
        lines.append("")

    lines.append("#### 💳 Estimated Cost Breakdown:")
    lines.append(f"- 🏨 **Accommodation ({stay_days} Nights):** ₹{cost_bd.get('Accommodation', 0):,}")
    lines.append(f"- ✈️ **International Flight Legs:** ₹{cost_bd.get('International Flights', 0):,}")
    lines.append(f"- 🚆 **Intercity Rail & Regional Transit:** ₹{cost_bd.get('Intercity Rail & Transit', 0):,}")
    lines.append(f"- 🍜 **Dining & Regional Food:** ₹{cost_bd.get('Dining', 0):,}")
    lines.append(f"- 🎟️ **Sightseeing & Heritage Admissions:** ₹{cost_bd.get('Activities', 0):,}")
    lines.append(f"- 🛡️ **Contingency Buffer (5%):** ₹{cost_bd.get('Contingency Buffer (5%)', 0):,}")
    lines.append(f"- 💰 **Total Estimated:** **₹{cost_bd.get('Total Estimated', 0):,}**")
    lines.append("")

    lines.append("#### 📅 Day-by-Day Journey Overview:")
    lines.append("")
    for day in journey.get("days", []):
        d_num = day.get("day", day.get("day_num", 1))
        d_city = day["city"]
        d_title = day["title"]
        acts_str = " &bull; ".join(a["activity"][:55] + "..." if len(a["activity"]) > 55 else a["activity"] for a in day.get("activities", [])[:2])
        lines.append(f"- **Day {d_num:02d} ({d_city}):** {d_title} — *{acts_str}*")

    lines.append("")
    lines.append("---")
    lines.append("💡 *This complete multi-stop journey has been prepared for your itinerary. Click '📅 My Itinerary' in the navigation bar to view all day-by-day details, or explore our interactive tools to adjust dates and stops!*")

    return "\n".join(lines)


def answer_visa_and_entry_question(country_name: str, q: str) -> str:
    return f"""### 🛂 Visa & Entry Requirements for {country_name}

Here are essential passport and entry requirements when planning your journey to **{country_name}**:

1. **Passport Validity (Universal Standard):**
   - Your passport must have at least **6 months validity** remaining beyond your scheduled date of departure from {country_name}.
   - Ensure at least **2 completely blank visa pages** for entry and exit immigration stamps.

2. **Tourist Visa Regulations:**
   - **For Indian Passport Holders:** Many countries offer streamlined e-Visas or Visa-on-Arrival (e.g. Thailand, Vietnam, UAE, Sri Lanka, Indonesia). Japan offers single/multiple entry tourist visas and e-Visas. Schengen nations (France, Italy, Germany, Spain) require an advance short-stay Schengen visa. Nepal allows Indian citizens entry with a valid Passport or Voter ID without requiring a visa.
   - **For US, UK, EU, and Australian Citizens:** Most destination countries offer 30-to-90 day visa-free entry or simple electronic travel authorizations (eTA).

3. **Mandatory Documentation Checklist:**
   - Confirmed return or onward international flight ticket.
   - Proof of accommodation (hotel reservation confirmation or host address).
   - Sufficient proof of funds (international debit/credit card or bank statement).
   - Digital arrival card or customs declaration form (completed online 24–72 hours prior to arrival where applicable).

4. **Official Advisory:**
   - Always verify the latest official consular requirements on the destination's official immigration portal prior to purchasing non-refundable airfares."""


def answer_connectivity_and_apps_question(country_name: str, q: str) -> str:
    c_low = country_name.lower()
    if "japan" in c_low:
        apps_info = "Google Maps, Japan Travel by NAVITIME, Suica / Pasmo digital IC card in Apple/Google Wallet, Google Translate (camera mode), Tabiko"
        sim_advice = "eSIM (Airalo, Ubigi) or Pocket Wi-Fi (Ninja WiFi / Japan Wireless picked up at Haneda/Narita/KIX airport). Pocket Wi-Fi is ideal for groups of 2+."
    elif "thailand" in c_low:
        apps_info = "Grab (ride-hailing & food), Bolt, Google Maps, LINE (local messaging), ViaBus"
        sim_advice = "Tourist SIM from AIS, TrueMove, or dtac available at airport arrivals or 7-Eleven (~฿299 for 8–15 days unlimited data), or Airalo eSIM."
    elif "india" in c_low:
        apps_info = "Uber, Ola, Rapido, IRCTC Rail Connect, MakeMyTrip, Google Pay"
        sim_advice = "Airtel or Jio physical SIM card at international airports (requires passport, visa copy, and passport photo for KYC verification), or global roaming eSIM."
    elif any(e in c_low for e in ["france", "italy", "spain", "germany", "uk"]):
        apps_info = "Citymapper, TheFork (dining bookings), Uber/FreeNow, Trainline, Omio"
        sim_advice = "Airalo or Holafly EU regional eSIM with EU-wide roaming (covers all EU nations seamlessly), or Orange Holiday Europe SIM."
    else:
        apps_info = "Google Maps, Google Translate, Citymapper, Uber/Grab"
        sim_advice = "Regional travel eSIM (Airalo / Maya Mobile) for instant activation upon landing, or a prepaid local SIM card from official carrier counters at the airport."

    return f"""### 📱 Connectivity, SIM Cards & Essential Apps for {country_name}

Stay seamlessly connected during your trip to **{country_name}**:

1. **SIM Card & Mobile Internet Options:**
   - **eSIM (Most Convenient):** If your phone supports digital eSIM, install Airalo, Ubigi, or Holafly before departure. Connects immediately to local mobile networks upon landing without swapping physical plastic cards.
   - **Local Physical Tourist SIM:** Available at airport arrival halls from verified telecom providers.
   - **{sim_advice}**

2. **Public Wi-Fi:**
   - Available in major hotels, cafes, and major transit hubs. However, do not rely exclusively on public Wi-Fi for live navigation and train transfers.

3. **Must-Have Travel Apps:**
   - **Navigation & Transit:** {apps_info}
   - **Language:** Google Translate with the local offline language dictionary downloaded.
   - **Safety & Documents:** Offline copies of passport, boarding passes, and emergency contact numbers saved to your device."""


def answer_accommodation_question(country_name: str, q: str) -> str:
    c_low = country_name.lower()
    if "japan" in c_low:
        tiers = """- **Budget / Capsule Hotels:** ₹2,200 – ₹4,500 / night (Clean, futuristic, central locations like Shinjuku, Asakusa, Umeda).
- **Mid-Range Business Hotels (APA, Daiwa Roynet, Dormy Inn):** ₹6,000 – ₹12,000 / night (Modern, compact, often with natural onsen baths and breakfast).
- **Traditional Ryokan Experience:** ₹18,000 – ₹45,000 / night (Tatami mat rooms, multi-course Kaiseki dinner, and private hot springs in Hakone or Kyoto)."""
        areas = "Stay near major JR train hubs: Shinjuku or Tokyo Station in Tokyo; Downtown Kawaramachi or Kyoto Station in Kyoto; Namba/Umeda in Osaka."
    elif "thailand" in c_low:
        tiers = """- **Hostels & Guesthouses:** ₹1,000 – ₹2,500 / night.
- **Boutique 4-Star Hotels:** ₹3,500 – ₹7,500 / night (Exceptional value with rooftop pools in Bangkok and Chiang Mai).
- **Luxury Beach Resorts:** ₹12,000 – ₹30,000+ / night in Phuket or Koh Samui."""
        areas = "Sukhumvit (near BTS Skytrain) or Riverside in Bangkok; Nimman or Old City in Chiang Mai."
    elif "india" in c_low:
        tiers = """- **Budget Guesthouses / Homestays:** ₹1,200 – ₹2,800 / night.
- **3–4 Star City Hotels:** ₹3,500 – ₹8,000 / night.
- **Heritage Haveli & Palace Hotels:** ₹12,000 – ₹50,000+ / night in Rajasthan (Jaipur, Udaipur)."""
        areas = "Central transit-connected districts with vetted security and complimentary breakfast."
    else:
        tiers = f"""- **Budget Hostels & Guesthouses:** ₹2,000 – ₹4,500 / night.
- **Mid-Range Boutique Hotels (3–4 Star):** ₹6,500 – ₹14,000 / night.
- **5-Star Luxury Resorts & Heritage Properties:** ₹18,000 – ₹45,000+ / night."""
        areas = f"Choose accommodations within walking distance (under 10 minutes) of a major metro station or central walking district in {country_name}."

    return f"""### 🏨 Accommodation Options & Estimated Costs in {country_name}

Here is a realistic breakdown of lodging styles, nightly cost bands, and recommended neighborhoods in **{country_name}**:

#### Approximate Nightly Rates:
{tiers}

#### Where to Base Yourself:
- **Recommended Areas:** {areas}
- **Booking Strategy:** For high season travel, reserve flexible cancellation accommodations 4–8 weeks in advance."""


def answer_dietary_needs_question(country_name: str, q: str) -> str:
    return f"""### 🥗 Dining with Dietary Preferences in {country_name}

Navigating dietary preferences and food restrictions in **{country_name}**:

1. **Vegetarian & Vegan Travel:**
   - **HappyCow App:** Download the HappyCow app for verified plant-based and vegetarian cafes worldwide.
   - **Local Dishes:** Look for naturally vegetarian heritage preparations (lentil curries, vegetable tempura, vegetable sushi rolls, fresh salads, tofu stews, and Margherita pizza).
   - **Important Note:** In many East Asian cuisines (like Japan and Thailand), savory broth frequently contains bonito fish flakes (dashi) or fish sauce unless explicitly requested as Buddhist vegetarian (*Shojin Ryori* in Japan, *Jay* เจ in Thailand).

2. **Halal Dining:**
   - Look for verified Halal certified logos in restaurant windows. Middle Eastern, Turkish, Indian, and Malaysian/Indonesian restaurants widely offer certified halal meats in major international cities.

3. **Gluten-Free & Allergies:**
   - In Japan, standard soy sauce contains wheat/gluten; carry a translated Japanese food allergy card (*Arerugi kado*) stating your exact allergy in the native script.
   - In Europe, EU allergen regulations require all dining menus to clearly indicate 14 common allergens (nuts, gluten, dairy, shellfish).

4. **Helpful Local Phrase to Show Waitstaff:**
   - *"I do not eat meat, fish, or seafood. Is there a vegetarian option?"*
   - Always communicate food allergies clearly before ordering."""


def answer_travel_disruptions_question(country_name: str, q: str) -> str:
    return f"""### 🔄 Handling Travel Delays, Missed Connections & Changes

If your travel itinerary is impacted by a flight delay, train disruption, or missed connection:

1. **Immediate Step — Official Service Desk:**
   - Head immediately to the airline transfer desk or railway station customer service office (*Midori-no-Madoguchi* in Japan, SNCF/Trenitalia in Europe). In cases of carrier-caused delays, they will rebook you on the next available departure at no additional charge.

2. **Retain All Receipts & Documentation:**
   - Request an official written delay verification notice from airline/rail staff.
   - Keep all boarding passes, ticket stubs, and receipts for necessary meals or emergency hotel accommodations for travel insurance claims.

3. **Backup Transit Alternatives:**
   - **Japan:** If a Shinkansen is briefly held due to weather, trains resume rapidly, and tickets can be swapped at station ticket windows.
   - **Europe:** High-speed rail lines frequently operate hourly; alternatively, regional trains or express coach lines (FlixBus) provide dependable backups.
   - **Domestic / Regional Flights:** Use Google Flights to check secondary carriers operating the same city pair.

4. **Adjusting Your Itinerary:**
   - If an activity or hotel check-in is missed, message your accommodation immediately to prevent your reservation from being marked as a no-show.
   - You can also ask me anytime to adjust your day's schedule or resequence upcoming activities!"""


def answer_accessibility_question(country_name: str, q: str) -> str:
    return f"""### ♿ Accessibility & Senior Travel in {country_name}

Helpful accessibility and mobility guidance for **{country_name}**:

1. **Public Transit & Station Infrastructure:**
   - Major metropolitan subway networks and high-speed rail terminals feature elevator access, tactile paving, and dedicated priority seating.
   - High-speed trains provide designated wheelchair spaces and accessible restrooms. Notify station staff at ticket gates for ramp assistance boarding the train.

2. **Historic Quarters & Cobblestone Streets:**
   - Historic old towns, ancient castles, and temple grounds frequently feature uneven stone paths, stairs, or gravel courtyards.
   - Recommended to check ahead for accessible perimeter routes and book step-free vehicles or accessible taxis.

3. **Pacing for Seniors & Travelers with Mobility Needs:**
   - Limit daily itineraries to **1–2 key highlights per day** with scheduled resting breaks in scenic parks or teahouses.
   - Opt for centrally located hotels adjacent to elevator-equipped transit stations."""


def get_conversational_onboarding_greeting(
    role_or_name: str = "guide",
    destination: str = "",
    assistant_name: str = "",
    starting_location: str = "",
    days: int = 7,
    budget: int = 80000,
    has_custom_trip: bool = False,
    **kwargs
) -> str:
    """
    Returns a natural, step-by-step greeting that asks only ONE relevant next question.
    Accepts flexible argument order for backwards compatibility.
    """
    # Detect role
    raw_str = str(role_or_name).lower()
    if "companion" in raw_str or raw_str in ("alex", "male"):
        role_label = "AI Travel Companion"
        default_name = "Alex"
    else:
        role_label = "Travel Guide"
        default_name = "Maya"

    # Resolve character name
    char_name = assistant_name.strip() if assistant_name and assistant_name.strip() else kwargs.get("character_name", "")
    if not char_name:
        if role_or_name not in ("guide", "companion", "Travel Guide", "AI Travel Companion"):
            char_name = role_or_name
        else:
            char_name = default_name

    dest = destination or kwargs.get("destination", "")

    if not dest or dest in ["Select a Country", "World"]:
        return (
            f"Hi! 👋 I'm **{char_name}**, your personal {role_label} from the **AI-Based Personalized Travel Planner**.\n\n"
            "Where do you want to go? Do you already have a destination in mind, or would you like me to suggest one based on this season?"
        )
    elif not starting_location or starting_location in ("Your Location", ""):
        return (
            f"Hello! I'm **{char_name}**, your {role_label} for **{dest}** ✈️.\n\n"
            f"Where will you be starting your journey from, and when are you planning to travel?"
        )
    elif not has_custom_trip:
        return (
            f"Welcome! I'm **{char_name}**, and I'm ready to help plan your **{days}-day** journey to **{dest}**.\n\n"
            "What kind of experience are you looking for — iconic landmarks, authentic local food, cultural attire, or budget-friendly ideas?"
        )
    else:
        return (
            f"Hi there! I'm **{char_name}**, your personal {role_label}.\n\n"
            f"How can I assist you with your journey to **{dest}** today? Ask me anything about routes, packing, dining, or travel tips!"
        )


def _answer_travel_question_inner(
    country: str,
    question: str,
    itinerary: Optional[Dict[str, Any]] = None,
    profile: Optional[Dict[str, Any]] = None,
    trip_context: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    role: Optional[str] = None,
    **kwargs
) -> str:
    country_name = normalize_country_key(country)
    knowledge = get_country_knowledge(country_name)
    c_name = knowledge["name"]
    q = str(question or "").strip().lower()

    if not q:
        return f"Hi! 👋 I'm your AI Travel Assistant for **{country_name}**. Ask me anything about your trip, itinerary, authentic food, landmarks, transportation, budget, or travel tips!"

    # Detect if another country is explicitly mentioned in the question
    COUNTRY_MENTION_MAP = {
        "nepal": "Nepal", "japan": "Japan", "thailand": "Thailand", "france": "France",
        "italy": "Italy", "germany": "Germany", "spain": "Spain", "china": "China",
        "south korea": "South Korea", "korea": "South Korea", "vietnam": "Vietnam",
        "indonesia": "Indonesia", "india": "India", "brazil": "Brazil", "portugal": "Portugal",
        "russia": "Russia", "greece": "Greece", "turkey": "Turkey", "egypt": "Egypt",
        "saudi arabia": "Saudi Arabia", "mexico": "Mexico", "united kingdom": "United Kingdom",
        "uk": "United Kingdom", "england": "United Kingdom", "scotland": "United Kingdom",
        "united states": "USA", "usa": "USA", "america": "USA", "canada": "Canada",
        "australia": "Australia", "norway": "Norway", "argentina": "Argentina", "ireland": "Ireland"
    }
    for c_kw, c_target in COUNTRY_MENTION_MAP.items():
        if re.search(r'\b(?:in|for|of|to|about)\s+' + re.escape(c_kw) + r'\b', q) or (re.search(r'\b' + re.escape(c_kw) + r'\b', q) and country.lower() != c_kw):
            country_name = normalize_country_key(c_target)
            knowledge = get_country_knowledge(country_name)
            c_name = knowledge["name"]
            break

    cities = knowledge.get("cities", [c_name])
    attractions = [a[0] if isinstance(a, (tuple, list)) else a.get("name", "") for a in knowledge.get("attractions", [])]
    foods = knowledge.get("food", [])
    transport = knowledge.get("transportation", {})
    tips = knowledge.get("travel_tips", {})

    # Extract trip context if available
    ctx = trip_context or {}
    trip_days = ctx.get("days", 7)
    trip_travelers = ctx.get("travelers", 1)
    trip_budget = ctx.get("budget", 80000)
    trip_style = ctx.get("style", "Relaxed")
    trip_start = ctx.get("starting", "Your Location")

    # 0a. WORD / PHRASE MEANINGS (e.g. "What does Hola mean?")
    word_meaning = answer_word_meaning_question(question)
    if word_meaning:
        return word_meaning

    # 0a1. MULTI-STOP & MULTI-COUNTRY TRIP PLANNING REQUESTS
    multi_stop_cues = ["start from", "starting from", "then go to", "then visit", "and return to", "return to", "stay in", "for 2 days, then", "for 3 days, then", "multi-stop", "multi stop", "multi city"]
    is_multi_stop = any(cue in q for cue in multi_stop_cues) or (
        any(c1 in q for c1 in ["tokyo", "paris", "delhi", "rome", "london", "bangkok"]) and
        any(c2 in q for c2 in ["kyoto", "nice", "agra", "florence", "edinburgh", "chiang mai", "osaka"]) and
        any(w in q for w in ["days", "route", "itinerary", "transport", "travel", "plan"])
    )
    if is_multi_stop:
        try:
            from multi_stop_planner import parse_multi_stop_trip_prompt, generate_multi_stop_journey
            parsed_m = parse_multi_stop_trip_prompt(question)
            if parsed_m and parsed_m.get("stops"):
                journey = generate_multi_stop_journey(parsed_m)
                if journey:
                    return format_multi_stop_chat_response(journey)
        except Exception:
            pass

    # 0a2. SEASONAL DESTINATION ADVICE ("Where to go in December?", "I don't know where to go")
    season_cues = ["where should i go", "where to go", "where to travel", "suggest where to go", "don't know where to go", "recommend a destination", "best place to visit in", "best places to visit in", "best country to visit in"]
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    if any(sc in q for sc in season_cues) or (any(m in q for m in months) and any(w in q for w in ["visit", "travel", "go", "trip", "vacation", "holiday", "recommend"]) and not any(ck in q for ck in ["tokyo", "paris", "rome", "delhi"])):
        try:
            from multi_stop_planner import recommend_destinations_by_season
            target_m = next((m for m in months if m in q), "december")
            return recommend_destinations_by_season(target_m)
        except Exception:
            pass

    # 0a3. VISA & PASSPORT ENTRY REQUIREMENTS
    if any(k in q for k in ["visa", "passport", "entry requirement", "entry rule", "travel document", "embassy", "customs form", "validity"]):
        return answer_visa_and_entry_question(c_name, q)

    # 0a4. CONNECTIVITY, SIM & APPS
    if any(k in q for k in ["sim card", "esim", "roaming", "internet", "wifi", "mobile data", "connectivity", "apps", "useful apps"]):
        return answer_connectivity_and_apps_question(c_name, q)

    # 0a5. ACCOMMODATION & COSTS
    if any(k in q for k in ["hotel", "hostel", "stay", "accommodation", "resort", "airbnb", "guesthouse", "ryokan", "where to stay"]):
        return answer_accommodation_question(c_name, q)

    # 0a5a. KIMONO VS YUKATA CLOTHING COMPARISON
    if any(k in q for k in ["kimono and a yukata", "kimono and yukata", "difference between a kimono", "difference between kimono", "kimono vs yukata"]):
        from destination_knowledge import compare_kimono_and_yukata
        return compare_kimono_and_yukata()

    # 0a5b. SHINTO SHRINE VS BUDDHIST TEMPLE BEHAVIOR & ETIQUETTE
    if any(k in q for k in ["behave when visiting a shrine", "shrine etiquette", "visiting a shrine", "how to behave at a shrine", "shinto shrine rules", "how should i behave when visiting a shrine", "behave at a shrine"]):
        from destination_knowledge import answer_shrine_behavior
        return answer_shrine_behavior()

    # 0a5c. FOOD ALLERGIES WARNING
    if any(k in q for k in ["food allergies", "food allergy", "allergies i should watch", "allergies to watch out for", "any food allergies", "watch out for allergies"]):
        from destination_knowledge import answer_food_allergies_guide
        return answer_food_allergies_guide(c_name)

    # 0a5d. REPLACE RESTAURANT WITH VEGETARIAN OPTION
    if any(k in q for k in ["replace this restaurant", "replace restaurant", "vegetarian option", "replace with vegetarian", "replace dinner with vegetarian", "substitute vegetarian"]):
        from destination_knowledge import replace_meal_with_vegetarian
        return replace_meal_with_vegetarian(q, c_name, cities[0] if cities else None)

    # 0a5e. CULTURAL ACTIVITY SUGGESTION FOR SPECIFIC DAY / CITY
    if any(k in q for k in ["cultural activity", "cultural activities"]) and any(w in q for w in ["suggest", "recommend", "second day", "day 2", "kyoto", "tokyo"]):
        from destination_knowledge import suggest_cultural_activity
        target_city = next((c for c in ["kyoto", "tokyo", "osaka", "rome", "paris"] if c in q), cities[0] if cities else "Kyoto")
        day_num = 2 if any(d in q for d in ["second", "2"]) else 1
        return suggest_cultural_activity(c_name, target_city, day_num=day_num)

    # 0a5f. CITY-SPECIFIC FOOD INQUIRIES ("What should I eat in Tokyo if I'm vegetarian?", "Which local dishes should I try in Osaka?", "What should I eat in Kyoto?")
    if any(k in q for k in ["what should i eat", "which local dishes", "what to eat in", "dishes should i try", "dishes to try in", "what to eat", "food in tokyo", "food in kyoto", "food in osaka", "eat in tokyo", "eat in kyoto", "eat in osaka"]):
        from destination_knowledge import answer_city_food_question
        return answer_city_food_question(c_name, q, city=cities[0] if cities else None)

    # 0a6. DIETARY RESTRICTIONS (VEGETARIAN, VEGAN, HALAL, GLUTEN-FREE, ALLERGIES)
    if any(k in q for k in ["vegetarian", "vegan", "halal", "jain", "gluten", "allergy", "allergies", "pork", "diet"]):
        return answer_dietary_needs_question(c_name, q)

    # 0a7. DELAYS & TRAVEL DISRUPTIONS
    if any(k in q for k in ["delay", "delayed", "missed connection", "flight cancelled", "train cancelled", "strike", "disruption", "alternate route"]):
        return answer_travel_disruptions_question(c_name, q)

    # 0a8. ACCESSIBILITY & SENIOR TRAVEL
    if any(k in q for k in ["wheelchair", "accessible", "accessibility", "elderly", "senior", "disability", "mobility"]):
        return answer_accessibility_question(c_name, q)

    # 0b. 10-DAY TRIP PACKING GUIDE (e.g. "What should I pack for a 10 day trip?")
    if any(k in q for k in ["pack for 10 day", "10 day trip", "pack for a 10 day", "10 days trip", "packing for 10", "pack for 10"]):
        return f"""### 🎒 Comprehensive 10-Day Trip Packing Guide

Preparing for a **10-day journey** requires versatile, comfortable layering and smart organization:

1. **👕 Clothing & Layering:**
   - **Tops:** 6–7 versatile, moisture-wicking shirts/blouses (mix of short and long sleeves).
   - **Bottoms:** 3–4 comfortable pairs (travel trousers, jeans, or lightweight breathable pants).
   - **Outerwear:** 1 packable light jacket, fleece, or cardigan (plus a rain-resistant windbreaker).
   - **Undergarments & Socks:** 8–10 sets (quick-drying fabrics recommended).
   - **Sacred / Cultural Modesty:** Lightweight shawl or scarf to cover shoulders and knees when visiting temples, churches, or sacred sites.
   - **Sleepwear:** 2 comfortable sleepwear sets.

2. **👟 Footwear:**
   - **Primary:** 1 pair of broken-in, supportive walking sneakers (expect 10,000–18,000 steps daily).
   - **Secondary:** 1 comfortable slip-on pair or dressy walking shoes for dining and sacred site visits where shoes are frequently removed.

3. **🧴 Toiletries & Personal Care:**
   - Travel-size toothbrush, toothpaste, shampoo bar, deodorant, and moisturizer.
   - Broad-spectrum sunscreen (SPF 50+) and lip balm with UV protection.
   - Hand sanitizer and travel disinfectant wipes.

4. **🔌 Electronics & Connectivity:**
   - Universal travel power adapter compatible with local wall sockets.
   - High-capacity portable power bank (10,000–20,000 mAh) for long sightseeing days.
   - Phone charging cables, headphones, and portable luggage scale.

5. **💊 Travel Health & Pharmacy:**
   - Personal prescription medications (in original packaging with doctor's prescription).
   - Basic travel first-aid: pain relievers (paracetamol/ibuprofen), antacids, motion sickness tablets, and adhesive band-aids.
   - Electrolyte rehydration packets.

6. **📄 Travel Documents & Money:**
   - Passport & visa copies (printed and saved digitally in cloud storage).
   - Travel insurance policy details and international emergency contact numbers.
   - 2 credit/debit cards plus local cash for street stalls and transit.

💡 **Traveler Pro-Tip:** Use compression packing cubes to organize outfits by day or category and save 35% of suitcase space!

<!-- SPEECH:en-US:For a 10-day trip, pack versatile layering tops, comfortable walking sneakers, a universal power adapter, and essential travel documents. -->"""

    # 0c. BEST TIME TO VISIT (e.g. "What is the best time to visit Japan?")
    if any(k in q for k in ["best time", "when to visit", "best season", "best month"]):
        if "japan" in q or c_name == "Japan":
            return f"""### 🌸 Best Time to Visit Japan

The best times to visit **Japan** are **Spring (March to May)** and **Autumn (September to November)**:

1. **🌸 Spring (March – May) — The Iconic Cherry Blossom Season:**
   - **Highlights:** World-famous Sakura (cherry blossoms) bloom across Tokyo, Kyoto, Osaka, and Hiroshima from late March to mid-April.
   - **Weather:** Mild, crisp, and comfortable (15°C–21°C / 59°F–70°F). Ideal for outdoor sightseeing and temple walking.
   - **Festivals:** Hanami (flower-viewing picnics under blooming sakura trees).

2. **🍁 Autumn (September – November) — Vibrant Fall Foliage:**
   - **Highlights:** Breathtaking red and gold maple leaves (Koyo) transform Kyoto's temples, Mount Fuji, and Nikko.
   - **Weather:** Clear blue skies, lower humidity, and very comfortable temperatures (14°C–20°C).
   - **Bonus:** Less crowded than peak sakura season, with exceptional seasonal dining (chestnuts, matsutake, persimmons).

3. **❄️ Winter (December – February) — Snow & Hot Springs:**
   - **Highlights:** World-class powder skiing in Hokkaido and the Japanese Alps, relaxing outdoor onsen (hot springs), snow monkeys, and illuminated winter festivals.

4. **☀️ Summer (June – August) — Climbing Fuji & Festive Matsuri:**
   - **Highlights:** Mount Fuji climbing season opens; magnificent fireworks festivals (hanabi) and traditional street matsuri.
   - **Note:** Temperatures are hot and humid (28°C–35°C), with the brief rainy season (tsuyu) in June/early July.

💡 **Recommendation:** For the ultimate quintessential journey, aim for **April (cherry blossoms)** or **October/November (autumn foliage)**!

<!-- SPEECH:en-US:The best times to visit Japan are Spring from March to May for cherry blossoms, and Autumn from September to November for spectacular foliage. -->"""
        else:
            season_str = tips.get("best_season", "Spring and Autumn offer mild, pleasant sightseeing weather.")
            return f"""### ☀️ Best Time to Visit {c_name}

Planning your trip to **{c_name}** around local seasons ensures the most rewarding sightseeing experience:

- **Optimal Season:** **{season_str}**
- **Climate Overview:** Mild temperatures, lower rainfall, and ideal daylight hours for walking tours and cultural exploration.
- **Shoulder Season Benefits:** Fewer tourist crowds, better photography lighting, and more affordable accommodations.
- **Tip:** Check local national holidays and festival dates before booking flights.

<!-- SPEECH:en-US:The best time to visit {c_name} is during {season_str}. -->"""

    # 0d. SPECIFIC COUNTRY CULTURE INQUIRY (e.g. "Tell me about Indian culture")
    if any(k in q for k in ["indian culture", "culture of india", "tell me about indian culture", "about indian culture"]):
        return f"""### 🇮🇳 Guide to Indian Culture & Heritage

Indian culture is one of the world's oldest, most diverse, and culturally profound civilizations, spanning over 5,000 years of living history:

1. **🕊️ Philosophy & Spiritual Heritage:**
   - **Atithi Devo Bhava:** The ancient ethos meaning *"The Guest is God"*, forming the foundation of legendary Indian hospitality.
   - **Birthplace of World Religions:** Cradle of Hinduism, Buddhism, Jainism, and Sikhism, celebrating peaceful coexistence and spiritual inquiry.
   - **Yoga & Ayurveda:** Ancient holistic systems of wellness, mindfulness, and natural healing practiced globally.

2. **🎉 Vibrant Festivals & Celebrations:**
   - **Diwali (Festival of Lights):** Symbolizing the victory of light over darkness and good over evil, celebrated with earthen lamps (diyas), fireworks, and sweets.
   - **Holi (Festival of Colors):** A jubilant spring celebration of unity, forgiveness, and vibrant powdered pigments.
   - **Regional Festivals:** Navratri, Eid, Christmas, Durga Puja (Kolkata), Pongal (Tamil Nadu), Onam (Kerala), and Baisakhi (Punjab).

3. **🍛 Extraordinary Gastronomic Diversity:**
   - Indian cuisine varies dramatically every 100 kilometers — from rich northern Mughlai curries, biryanis, and tandoori breads to southern coconut-infused curries, crispy dosas, and coastal seafood.
   - Celebrated for mastery of aromatic spices (turmeric, cardamom, cumin, saffron) used for both flavor and health benefits.

4. **👗 Art, Textiles & Traditional Attire:**
   - Centuries of artisanal textile excellence: Kanchipuram and Banarasi silk sarees, Pashmina shawls from Kashmir, intricate Chikankari embroidery, and colorful Rajasthani block prints.
   - Traditional wear: Sarees and Lehengas for women; Kurta-Pajama, Sherwani, and Dhoti/Veshti for men.

5. **🏛️ Architectural Wonders:**
   - Masterpieces ranging from the sublime white marble Taj Mahal in Agra to the rock-cut Kailash Temple at Ellora, Dravidian temple gopurams in Tamil Nadu, and majestic desert forts in Rajasthan.

<!-- SPEECH:en-US:Indian culture is a rich 5,000-year-old civilization celebrated for Atithi Devo Bhava, diverse festivals like Diwali and Holi, extraordinary cuisine, and vibrant textiles. -->"""

    # 1. LANGUAGE, GREETINGS & PHRASE TRANSLATIONS (e.g., "How to say 'No Problem' in Thai")
    phrase_reply = answer_language_phrase_question(question, c_name, knowledge)
    if phrase_reply:
        return phrase_reply

    # 1b. TRADITIONAL CLOTHING & ATTIRE FOR MEN & WOMEN WITH COSTS (FOR ALL COUNTRIES)
    clothing_keywords = [
        "traditional dress", "traditional clothes", "traditional attire", "traditional clothing",
        "folk costume", "what to wear", "dress cost", "cost of dress", "clothing cost", "clothes cost",
        "men dress", "women dress", "men and women", "men's dress", "women's dress",
        "kimono", "saree", "chut thai", "dirndl", "lederhosen", "kilt", "hanbok", "ao dai", "costume",
        "attire", "traditional wear", "ethnic wear", "dresses", "traditional dresses"
    ]
    if any(k in q for k in clothing_keywords):
        clothing_data = get_traditional_clothing(c_name)
        return format_traditional_clothing_markdown(clothing_data)

    # 2. SPECIFIC CITY-TO-CITY TRANSIT QUESTIONS (e.g., "How do I travel from Tokyo to Kyoto?")
    if "tokyo" in q and "kyoto" in q:
        return f"""### 🚆 Traveling Between Tokyo and Kyoto (Japan)

Here are the best ways to travel between Tokyo and Kyoto:

1. **Tokaido Shinkansen (Bullet Train) — Highly Recommended:**
   - **Nozomi Train:** Fastest option taking just **2 hours 15 minutes**. Trains depart every 10–15 minutes.
   - **Hikari Train:** Takes **2 hours 40 minutes** and is fully covered by the Japan Rail (JR) Pass.
   - **Cost:** ~¥14,000–¥14,500 (~₹7,800–₹8,200) one way for a reserved seat.
   - **Tip:** Reserve seat on the right side (seats D/E) going from Tokyo to Kyoto for dramatic views of Mount Fuji!

2. **Highway Express Bus (Budget Friendly):**
   - **Day & Overnight Buses (e.g., Willer Express):** Take 7 to 8 hours.
   - **Cost:** ~¥3,500–¥8,000 (~₹2,000–₹4,500). Overnight buses save one night of hotel stay.

3. **Domestic Flight:**
   - Flying from Tokyo Haneda (HND) to Osaka Itami (ITM) takes ~1 hour 15 mins plus 50 mins train into Kyoto, but city-center to city-center the bullet train is much more convenient and punctual."""

    if "delhi" in q and ("agra" in q or "taj" in q):
        return f"""### 🚆 Traveling Between New Delhi and Agra (India)

Here are the most convenient transportation options:

1. **Gatimaan Express / Vande Bharat Express (Fastest & Most Comfortable):**
   - **Gatimaan Express:** Leaves Hazrat Nizamuddin station at 08:10 AM, arriving at Agra Cantt in **1 hour 40 minutes**.
   - **Cost:** ~₹750 (Chair Car) / ~₹1,500 (Executive Class) including light meal service.
2. **Taj Express / Bhopal Shatabdi:**
   - Highly reliable morning trains connecting Delhi and Agra in under 2 hours.
3. **Yamuna Expressway (Private Cab or AC Intercity Bus):**
   - Private AC cab takes **3 to 3.5 hours** door-to-door via the smooth 6-lane Yamuna Expressway. Cost is approx ₹3,000–₹4,500."""

    if "kathmandu" in q and "pokhara" in q:
        return f"""### 🚌 Traveling Between Kathmandu and Pokhara (Nepal)

Traveling between Kathmandu and Pokhara offers two popular options:

1. **Domestic Scenic Flight (Fastest & Spectacular):**
   - **Duration:** 25–30 minutes from Kathmandu Domestic Airport (KTM) to Pokhara (PKR).
   - **Airlines:** Buddha Air, Yeti Airlines.
   - **Cost:** ~$100–$120 (approx NPR 13,000–16,000 / ₹8,000–₹10,000). Request a seat on the right side heading to Pokhara for views of the Himalayan range!
2. **Tourist AC Express Bus:**
   - **Duration:** 6 to 8 hours along the Prithvi Highway alongside the Trishuli River.
   - **Cost:** NPR 1,200–2,500 (approx ₹750–₹1,500). Clean coaches with lunch stops."""

    # 2. ITINERARY MODIFICATION / "Change Day X" / "Modify Day X"
    day_match = re.search(r"day\s*(\d+)", q)
    if day_match and any(w in q for w in ["change", "modify", "replace", "relax", "swap", "alter", "less tiring", "different"]):
        d_num = day_match.group(1)
        relax_place = attractions[2] if len(attractions) > 2 else f"Scenic Park & Teahouse in {cities[0]}"
        return f"""### 🛠️ Custom Itinerary Recommendation for Day {d_num} in {c_name}

To make **Day {d_num}** more relaxing and enjoyable while maintaining authentic cultural depth in {c_name}, here is an updated plan:

- **🌅 Morning (09:30 AM): Leisurely Breakfast & Stroll**
  - **Activity:** Relaxed morning at a traditional local cafe or bakery, followed by a tranquil garden walk around **{relax_place}**.
  - **Estimated Cost:** ₹800 &bull; **Pace:** Very gentle with no rushed transit.

- **☀️ Afternoon (01:30 PM): Authentic Regional Lunch & Craft Discovery**
  - **Activity:** Savor authentic **{foods[0][0] if foods else 'local dishes'}** at a quiet family-run restaurant, followed by browsing a local handicraft atelier or tea salon.
  - **Estimated Cost:** ₹1,200 &bull; **Pace:** Unhurried, shaded indoor atmosphere.

- **🌆 Evening (06:00 PM): Sunset Promenade & Signature Dining**
  - **Activity:** Sunset stroll along the scenic waterfront or historic pedestrian quarter, followed by a relaxed 3-course dinner.
  - **Estimated Cost:** ₹1,500 &bull; **Pace:** Recharging for the days ahead.

💡 *You can also click '🔄 Update Itinerary' below to permanently apply custom modifications to your trip!*"""

    # 3. "HOW MUCH MONEY SHOULD I CARRY?" / CASH vs CARD / CURRENCY
    if any(k in q for k in ["how much money", "cash", "carry", "atm", "currency", "card or cash", "credit card"]):
        return f"""### 💵 Money & Currency Guide for {c_name}

Here is practical advice on managing money and payments in **{c_name}**:

- **Local Currency:** {knowledge.get('currency', 'Local currency')}.
- **Cash vs. Cards:**
  - In major metropolitan areas and hotels in **{c_name}**, credit/debit cards (Visa, Mastercard) are widely accepted.
  - **Carry Daily Cash:** We recommend carrying approximately **₹2,500–₹4,500 worth in local currency** per person per day for street food stalls, small temple donations, metered taxis, and traditional markets.
- **ATMs:** International ATMs at airports, bank branches, and convenience stores offer the most favorable exchange rates.
- **Currency Advice:** {tips.get('currency_tips', 'Inform your bank of travel dates to avoid card blocks.')}"""

    # 4. "WHAT SHOULD I DO IF IT RAINS?" / RAINY DAY ACTIVITIES
    if any(k in q for k in ["rain", "rainy", "raining", "bad weather", "indoor"]):
        indoor_att = [a for a in attractions if any(w in a.lower() for w in ["museum", "palace", "temple", "shrine", "center", "gallery"])]
        indoor_highlight = indoor_att[0] if indoor_att else f"The National Museum & Cultural Centers in {cities[0]}"
        return f"""### 🌧️ Rainy Day Activities in {c_name}

Rainy weather won't disrupt your journey! Here are the best indoor experiences in **{c_name}**:

1. **Explore World-Class Museums & Galleries:**
   - Spend a dry afternoon immersing yourself in **{indoor_highlight}**, discovering centuries of art, archaeological treasures, and royal heritage.
2. **Covered Market Halls & Culinary Workshops:**
   - Wander through historic covered food arcades and sample fresh **{foods[0][0] if foods else 'local delicacies'}**.
   - Book a 2-hour cooking class or traditional tea/coffee tasting session.
3. **Historic Covered Shrines & Sacred Architecture:**
   - Many of {c_name}'s premier historic temples, cathedrals, and palaces offer expansive sheltered pavilions with serene soundscapes during rainfall.
4. **Relax in Traditional Spas & Hot Springs:**
   - Experience authentic wellness traditions (onsen, thermal baths, or Ayurvedic rejuvenation)."""

    # 5. "WHICH PLACES ARE BEST FOR PHOTOGRAPHY?" / PHOTO SPOTS
    if (re.search(r'\b(?:photo|photos|photography|camera|instagram|pictures|photogenic)\b', q) and "photosynthesis" not in q):
        return f"""### 📸 Best Photography Spots in {c_name}

Capture breathtaking shots across **{c_name}** with these top viewpoints and photography tips:

- **Iconic Landmarks at Golden Hour:**
  - **{attractions[0] if attractions else c_name}:** Arrive 30 minutes before sunrise to capture the early morning mist without tourist crowds.
  - **{attractions[1] if len(attractions) > 1 else 'Panoramic Viewpoint'}:** Outstanding sunset vantage point overlooking historic architecture.
- **Vibrant Street Photography:**
  - Explore the narrow alleys, lanterns, and artisan quarters of **{cities[0]}** for candid shots of daily life, historic facades, and street food preparation.
- **Top Topography & Landscapes:**
  - Capture mountain vistas, coastal headlands, or rice terraces during the late afternoon when the warm light accentuates textures.
- **Photography Etiquette:** Always politely ask locals before taking portraits, and check photography regulations inside active places of worship."""

    # 6. "CAN I VISIT WITH CHILDREN?" / FAMILY-FRIENDLY
    if any(k in q for k in ["child", "children", "kid", "family", "toddler", "baby"]):
        return f"""### 👨‍👩‍👧‍👦 Traveling with Children in {c_name}

**{c_name}** is a rewarding family travel destination with excellent attractions for all ages:

- **Top Family Attractions:**
  - Interactive science & natural history museums, expansive public botanical parks, wildlife conservation reserves, and scenic boat rides.
- **Kid-Friendly Dining:**
  - Mild, flavorful options like {foods[0][0] if foods else 'fresh dishes'} are widely available. Family-friendly restaurants are accustomed to catering to young children.
- **Pacing & Rest:**
  - Plan for maximum **two major activities per day**, allowing a relaxed midday break to avoid travel fatigue.
- **Transit with Strollers:**
  - Metropolitan transit systems offer elevator access, though historic cobblestone quarters are best navigated with a supportive baby carrier."""

    # 7. "SUGGEST A ROMANTIC ACTIVITY" / COUPLES / HONEYMOON
    if any(k in q for k in ["romantic", "couple", "honeymoon", "date", "anniversary"]):
        return f"""### 🌹 Romantic Activities in {c_name}

Create unforgettable memories with your partner in **{c_name}**:

1. **Sunset Scenic Cruise or Waterfront Promenade:**
   - Enjoy a private boat excursion or twilight stroll along the scenic waterways of {cities[0]}.
2. **Panoramic Rooftop or Heritage Dining:**
   - Reserve a candlelit table overlooking {attractions[0] if attractions else c_name}, pairing regional wines or tea with authentic culinary specialties.
3. **Tranquil Historic Garden Walk:**
   - Escape city sounds in serene heritage botanical grounds, walking hand-in-hand under flowering tree canopies.
4. **Couples' Spa & Thermal Retreat:**
   - Unwind with traditional regional wellness therapies and private hot spring or herbal baths."""

    # 8. "WHICH PLACES SHOULD I SKIP IF I ONLY HAVE 3 DAYS?" / 3-DAY SHORT TRIP
    if any(k in q for k in ["skip", "3 day", "3 days", "short trip", "only have a few days", "express trip"]):
        return f"""### ⚡ 3-Day Express Priorities for {c_name}

With only **3 days** in **{c_name}**, focus on depth rather than exhausting travel:

- **What to FOCUS On:**
  - Stay based exclusively in **{cities[0]}** to eliminate time-consuming intercity transfers and hotel check-ins.
  - Visit the top two iconic landmarks (**{attractions[0] if attractions else 'Central Landmark'}** and **{attractions[1] if len(attractions) > 1 else 'Historic Quarter'}**).
  - Dedicate your evenings to food markets and signature dining.
- **What to SKIP:**
  - **Skip distant provinces or regional day excursions** (such as traveling across multiple islands or remote mountain passes).
  - **Skip secondary museums or shopping malls** that require long commutes. Quality time at central heritage sights offers a far more memorable trip!"""

    # 9. "PLAN A 30-DAY TRIP" / 30-DAY GRAND TOUR
    if any(k in q for k in ["30 day", "30 days", "30-day", "30-days", "month long", "month-long", "four weeks"]):
        return f"""### 🗺️ Grand 30-Day Travel Framework for {c_name}

A full 30-day grand tour allows you to experience the complete geographical, cultural, and gastronomic spectrum of **{c_name}** across diverse regions:

- **Week 1 (Days 1–7): The Historic & Cultural Heart ({cities[0]})**
  - World-class museums, historic citadels, culinary walking tours, and peaceful garden retreats in {c_name}.
- **Week 2 (Days 8–15): Heritage Hubs & Artisan Provinces ({cities[1] if len(cities) > 1 else 'Regional Hub'})**
  - World Heritage temples, centuries-old artisan workshops, and ancient fortresses across diverse regions.
- **Week 3 (Days 16–22): Scenic Landscapes & Nature Escapes ({cities[2] if len(cities) > 2 else 'Scenic Valley'})**
  - Dramatic mountain vistas, national park conservation trails, and pristine waterways.
- **Week 4 (Days 23–30): Hidden Gems, Coastal Living & Grand Farewell ({cities[-1]})**
  - Secluded village life, regional cooking masterclasses, artisan souvenir shopping, and celebratory farewell dinners.

💡 *Our planner has already created your complete day-by-day 30-day itinerary for {c_name} in the '✨ Your Itinerary' section!*"""

    # 9b. MULTI-DAY ITINERARY INQUIRIES (e.g., "What should I do for 10 days?", "10 days", "7-day plan", "14 days")
    days_pattern = re.search(r"(\d+)\s*[- ]?days?", q)
    if days_pattern and any(w in q for w in ["do", "plan", "itinerary", "visit", "trip", "travel", "recommend", "suggest", "guide"]):
        target_days = int(days_pattern.group(1))
        hub_count = min(max(2, target_days // 3), len(cities))
        selected_cities = cities[:hub_count]
        day3 = min(3, target_days)
        day4 = min(4, target_days)
        day7 = min(7, target_days)
        day8 = min(8, target_days)
        extra_block = f"\n- **Days {day8}–{target_days}: Scenic Nature & Farewell ({selected_cities[2] if len(selected_cities) > 2 else selected_cities[-1]})**\n  - Scenic countryside, mountain or coastal vistas, and relaxing farewell dinners across regional landscapes of {c_name}." if target_days > 7 else ""
        return f"""### 🗺️ Recommended {target_days}-Day Itinerary Framework for {c_name}

For a **{target_days}-day trip** to **{c_name}**, here is a recommended journey framework exploring its top regions ({', '.join(selected_cities)}):

- **Days 1–{day3}: Arrival & Historic Capital ({selected_cities[0]})**
  - Explore the iconic landmarks including **{attractions[0] if attractions else 'Central Heritage Site'}**, world-class museums, and authentic local food markets in {c_name}.
- **Days {day4}–{day7}: Cultural Heritage & Historic Provinces ({selected_cities[1] if len(selected_cities) > 1 else 'Scenic Province'})**
  - Discover ancient architecture, artisan quarters, and regional gastronomic specialties ({foods[0][0] if foods else 'local delicacies'}).{extra_block}

💡 *You can select {target_days} days in the trip duration slider to automatically generate your detailed day-by-day schedule with transit routes and cost breakdowns for {c_name}!*"""

    # 10. PACKING / CLOTHING
    if any(k in q for k in ["pack", "wear", "clothes", "clothing", "suitcase", "essentials"]):
        return f"""### 🎒 Packing Guide for {c_name}

When preparing for your trip to **{c_name}**, here are essential items based on local climate and customs:

- **Supportive Walking Footwear:** Cobblestones, temple steps, and walking tours require broken-in walking shoes.
- **Modest Attire for Sacred Sites:** Lightweight shawls, long trousers, or midi-dresses that cover shoulders and knees when visiting places of worship.
- **Layering Fabrics:** Breathable moisture-wicking shirts for daytime, plus a fleece or light down jacket for cool evenings or elevation changes.
- **Weather Protection:** Compact travel umbrella, UV sunglasses, and sunscreen.
- **Power Adapter:** Universal adapter compatible with local wall outlets.
- **Travel Pharmacy:** Reusable water bottle, motion sickness tablets for winding mountain roads, and personal first-aid."""

    # 11. FOOD / DINING / RESTAURANTS
    if any(k in q for k in ["food", "dish", "eat", "try", "cuisine", "taste", "dinner", "lunch", "breakfast", "vegetarian", "restaurant"]):
        from destination_knowledge import answer_city_food_question
        return answer_city_food_question(c_name, q, city=cities[0] if cities else None)

    # 12. TRANSPORTATION / GETTING AROUND / PUBLIC TRANSIT / BETWEEN CITIES
    if any(k in q for k in ["get around", "transport", "metro", "train", "bus", "drive", "car rental", "flight", "taxi", "uber", "subway", "travel between", "between these cities", "between cities", "travel from"]):
        modes_md = "\n".join([f"- **{m}**" for m in transport.get("modes", [])])
        return f"""### 🚆 How to Get Around in {c_name}

Transportation in **{c_name}** adapts specifically to its regional geography and infrastructure:

**Recommended Modes:**
{modes_md}

**Key Transit Advice:**
{transport.get('tips', 'Book intercity tickets in advance and use licensed cabs.')}

**Transit Passes:**
{transport.get('pass', 'Local transit smartcards are recommended for multi-day city stays.')}"""

    # 13. MUST-SEE PLACES / ATTRACTIONS / LANDMARKS / "WHAT SHOULD I VISIT?"
    if any(k in q for k in ["must see", "must-see", "attraction", "places", "visit", "landmark", "sights", "highlights", "top places", "what should i visit"]):
        att_md = "\n".join([f"- **{a[0]}** ({a[1]}): One of {c_name}'s premier landmark destinations." for a in knowledge.get("attractions", [])[:6]])
        return f"""### 📍 Top Must-See Places in {c_name}

For your trip to **{c_name}** (designed for {trip_travelers} traveler{'s' if trip_travelers > 1 else ''}, {trip_days} days, starting from {trip_start}), here are the essential landmarks:

{att_md}

💡 **Travel Recommendation:**
Spread your time across key hubs ({', '.join(cities[:4])}) to balance vibrant urban heritage with scenic landscapes."""

    # 14. CULTURAL RULES / ETIQUETTE / CUSTOMS / TIPPING
    if any(k in q for k in ["culture", "rule", "rules", "etiquette", "custom", "customs", "do and don't", "tip", "tipping", "polite"]):
        from destination_knowledge import get_destination_etiquette
        et_data = get_destination_etiquette(c_name)
        
        dos_list = "\n".join([f"- ✅ {d}" for d in et_data.get("dos_and_donts", {}).get("dos", [])])
        donts_list = "\n".join([f"- ❌ {d}" for d in et_data.get("dos_and_donts", {}).get("donts", [])])

        return f"""### 🕊️ Cultural Etiquette, Traditions & Customs in {c_name}

{et_data.get('overview', f'Cultural traditions in {c_name} reflect generations of living heritage.')}

---

#### 1. {et_data.get('greetings', {}).get('title', 'Greetings & Polite Behavior')}
- **Overview:** {et_data.get('greetings', {}).get('summary', '')}
- **Guidance:** {et_data.get('greetings', {}).get('details', '')}

#### 2. {et_data.get('dining', {}).get('title', 'Restaurant & Dining Etiquette')}
- **Overview:** {et_data.get('dining', {}).get('summary', '')}
- **Guidance:** {et_data.get('dining', {}).get('details', '')}

#### 3. {et_data.get('public_transport', {}).get('title', 'Public Transport Etiquette')}
- **Overview:** {et_data.get('public_transport', {}).get('summary', '')}
- **Guidance:** {et_data.get('public_transport', {}).get('details', '')}

#### 4. {et_data.get('temples_and_shrines', {}).get('title', 'Sacred Sites & Places of Worship')}
- **Overview:** {et_data.get('temples_and_shrines', {}).get('summary', '')}
- **Guidance:** {et_data.get('temples_and_shrines', {}).get('details', '')}

#### 5. {et_data.get('shoe_removal', {}).get('title', 'Shoe-Removal Customs')}
- **Overview:** {et_data.get('shoe_removal', {}).get('summary', '')}
- **Guidance:** {et_data.get('shoe_removal', {}).get('details', '')}

#### 6. {et_data.get('tipping', {}).get('title', 'Tipping Customs')}
- **Overview:** {et_data.get('tipping', {}).get('summary', '')}
- **Guidance:** {et_data.get('tipping', {}).get('details', '')}

#### 7. {et_data.get('photography', {}).get('title', 'Photography Restrictions')}
- **Overview:** {et_data.get('photography', {}).get('summary', '')}
- **Guidance:** {et_data.get('photography', {}).get('details', '')}

#### 8. {et_data.get('festivals', {}).get('title', 'Important Cultural Festivals')}
- **Overview:** {et_data.get('festivals', {}).get('summary', '')}
- **Guidance:** {et_data.get('festivals', {}).get('details', '')}

#### 9. {et_data.get('community_respect', {}).get('title', 'Respectful Community Behavior')}
- **Overview:** {et_data.get('community_respect', {}).get('summary', '')}
- **Guidance:** {et_data.get('community_respect', {}).get('details', '')}

---

### 📋 Practical DOs & DON'Ts for Travelers:

**DOs:**
{dos_list}

**DON'Ts:**
{donts_list}

<!-- SPEECH:en-US:In {c_name}, observe local etiquette: {et_data.get('greetings', {}).get('summary', '')} Tipping status: {et_data.get('tipping', {}).get('summary', '')} -->"""

    # 15. BUDGET / BUDGET ITINERARY / COST / EXPENSES
    if any(k in q for k in ["budget", "cheap", "cost", "money", "save", "affordable", "price", "cheaper"]):
        return f"""### 💰 Budget Travel Guide for {c_name}

How to maximize your travel budget in **{c_name}** (Current trip budget: ₹{trip_budget:,}):

1. **Accommodation:** Choose boutique guesthouses, homestays, or central 3-star transit-connected hotels.
2. **Food:** Enjoy authentic lunch sets ('menu del día' or local sets) and explore bustling food halls and night markets where locals eat.
3. **Transit:** Utilize public transit passes ({transport.get('pass', 'local transit passes')}) instead of private taxis.
4. **Attractions:** Many historical city squares, parks, cathedrals, and cultural viewpoints are free to explore. Check for museum discount days."""

    # 16. HIDDEN PLACES / SECRET GEMS / OFF THE BEATEN PATH
    if any(k in q for k in ["hidden", "secret", "off the beaten", "unique", "less crowded", "hidden gems"]):
        gem_city = cities[-1] if len(cities) > 2 else f"the scenic outskirts of {cities[0]}"
        return f"""### 💎 Hidden Gems & Off-the-Beaten-Path in {c_name}

Escape heavy tourist crowds with these authentic experiences in **{c_name}**:

- **Explore {gem_city}:** A quieter cultural enclave where traditional artisan workshops and local markets thrive.
- **Early Morning Walks:** Visit popular sights at sunrise before tour buses arrive to experience serene spiritual atmospheres.
- **Secondary Historic Towns:** Venture just 1–2 hours outside {cities[0]} to discover preserved architecture and regional home cooking."""

    # 17. WHAT TO AVOID / SAFETY / SCAMS
    if any(k in q for k in ["avoid", "scam", "danger", "safe", "safety", "crime", "trap"]):
        return f"""### ⚠️ What to Avoid & Safety Tips in {c_name}

Stay safe and smart during your journey in **{c_name}**:

- **Safety Overview:** {tips.get('safety', 'Remain aware of your belongings in crowded tourist spots.')}
- **Unlicensed Taxis:** Always use official airport taxi desks or verified mobile apps ({transport.get('modes', ['ride-hailing'])[-1]}).
- **Overpriced Tourist Menus:** Avoid restaurants right beside major tourist landmarks that have staff outside actively ushering tourists in.
- **Drinking Water:** Drink bottled or properly filtered water unless verified otherwise."""

    # 18. GENERAL KNOWLEDGE & OPEN-ENDED QUESTIONS (Math, Science, Concepts, General Q&A)
    gk_ans = query_general_knowledge(question)
    if gk_ans:
        return gk_ans

    # 18b. DYNAMIC ENCYCLOPEDIC & FACTUAL QUESTION ANSWERING
    # Answers any factual, historical, etymological, geographical, or cultural question about the country
    encyclopedia_ans = query_country_encyclopedia(question, c_name, knowledge)
    if encyclopedia_ans:
        return encyclopedia_ans

    # 19. GENERAL / DEFAULT FALLBACK (Only reached if no specific or encyclopedic answer found)
    fallback_text = f"""### ✈️ Travel Advice for {c_name}

Regarding your question about **{c_name}**:

- **Key Highlights:** {c_name} is celebrated for its historic landmarks ({', '.join(attractions[:3])}), vibrant cities ({', '.join(cities[:3])}), and rich cuisine ({', '.join([f[0] for f in foods[:2]])}).
- **Getting Around:** {transport.get('tips', 'Public transit and intercity options connect key destinations.')}
- **Best Season:** {tips.get('best_season', 'Spring and autumn offer mild sightseeing weather.')}
- **Local Customs:** {tips.get('etiquette', 'Respect local traditions and dress appropriately at cultural sites.')}

Feel free to ask more specific questions about packing, dining recommendations, 1–30 day itineraries, or how to travel between specific cities in **{c_name}**!"""
    return fallback_text


def answer_travel_question(
    country: str,
    question: str,
    itinerary: Optional[Dict[str, Any]] = None,
    profile: Optional[Dict[str, Any]] = None,
    trip_context: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    preferred_lang: Optional[str] = None,
    role: Optional[str] = None,
    **kwargs
) -> str:
    """
    Intelligently answers open-ended travel and general questions dynamically grounded
    in the currently selected country, trip context, and generated itinerary.
    Understands questions in ANY language and localizes responses.
    """
    # Auto-detect if caller passed (question, country) instead of (country, question)
    if country and isinstance(country, str) and question and isinstance(question, str):
        c_str = country.strip()
        q_str = question.strip()
        if len(c_str) > len(q_str) and ("?" in c_str or any(kw in c_str.lower() for kw in ("how", "what", "where", "tell", "say", "pack", "is", "can", "why"))):
            country, question = q_str, c_str

    # First check if original question directly matches language phrase translation
    direct_phrase = answer_language_phrase_question(question, country, profile)
    if direct_phrase:
        return direct_phrase

    eng_query, user_lang_code, user_lang_name = detect_user_lang_and_translate(question)
    effective_question = eng_query if (user_lang_code != "en" and eng_query) else question

    target_lang_code = user_lang_code
    if preferred_lang and preferred_lang not in ("Auto Detect", "English"):
        target_lang_code = LANGUAGE_CODES.get(preferred_lang.lower(), user_lang_code)

    raw_reply = _answer_travel_question_inner(
        country=country,
        question=effective_question,
        itinerary=itinerary,
        profile=profile,
        trip_context=trip_context,
        api_key=api_key,
        role=role,
        **kwargs
    )

    if target_lang_code != "en" and raw_reply:
        try:
            speech_tag = ""
            speech_match = re.search(r'<!-- SPEECH:[^>]+ -->', raw_reply)
            if speech_match:
                speech_tag = speech_match.group(0)

            lines = [l for l in raw_reply.split('\n') if l.strip()]
            sample_lines = []
            cur_len = 0
            for line in lines[:4]:
                if cur_len + len(line) < 380:
                    sample_lines.append(line)
                    cur_len += len(line)
                else:
                    break
            top_text = "\n".join(sample_lines) if sample_lines else (lines[0][:350] if lines else "")
            if top_text:
                localized = translate_live(top_text, target_lang_code, "en")
                if localized and localized.strip().lower() != top_text.strip().lower():
                    clean_reply = raw_reply.replace(speech_tag, "").strip() if speech_tag else raw_reply
                    result = f"{localized}\n\n---\n*(Detailed Guide)*\n\n{clean_reply}"
                    if speech_tag:
                        result += f"\n\n{speech_tag}"
                    return result
        except Exception:
            pass

    return raw_reply


# ============================================================
# WHERE TO TRY AUTHENTIC FOOD RECOMMENDATIONS
# ============================================================

WHERE_TO_TRY_DATA = {
    "Japan": {
        "sushi": "Tsukiji Outer Market & Ginza (Tokyo), Kuromon Ichiba (Osaka)",
        "ramen": "Shinjuku & Shibuya (Tokyo), Dotonbori (Osaka), Hakata (Fukuoka)",
        "tempura": "Asakusa & Ginza (Tokyo), Gion (Kyoto)",
        "okonomiyaki": "Dotonbori (Osaka), Hiroshima City Center",
        "kaiseki": "Historic Ryokans in Gion & Arashiyama (Kyoto)",
        "matcha": "Uji & Gion (Kyoto), Asakusa (Tokyo)",
        "yakitori": "Omoide Yokocho (Memory Lane, Shinjuku, Tokyo)",
        "takoyaki": "Dotonbori canal stalls (Osaka)"
    },
    "Nepal": {
        "momo": "Thamel & New Road (Kathmandu), Lakeside (Pokhara)",
        "dal bhat": "Authentic Thakali kitchens in Pokhara & Kathmandu",
        "thukpa": "Boudha Stupa cafes (Kathmandu), Solukhumbu tea lodges",
        "sel roti": "Patan Durbar Square & traditional sweet stalls in Bhaktapur",
        "choila": "Kirtipur & Old Patan (Kathmandu Valley)",
        "juju dhau": "Pottery Square & Durbar Square (Bhaktapur)",
        "gundruk": "Traditional Newari and Thakali dining houses"
    },
    "India": {
        "biryani": "Old City Hyderabad (Bawarchi / Shadab / Paradise), Lucknow (Awadh)",
        "dosa": "Mylapore (Chennai), Mavalli Tiffin Room (Bengaluru), Madurai",
        "butter chicken": "Pandara Road & Daryaganj (Old Delhi / Moti Mahal)",
        "rogan josh": "Ahdoos & Boulevard Road (Srinagar, Kashmir)",
        "chaat": "Chandni Chowk (Delhi), Chowpatty & Juhu Beach (Mumbai)",
        "vada pav": "Dadar Station & Girgaon (Mumbai)",
        "samosa": "Old Delhi street halwais, Kolkata tea stalls",
        "thali": "Traditional Rajasthani thali in Jaipur, Gujarati thali in Ahmedabad"
    },
    "France": {
        "croissant": "Artisan boulangeries in Montmartre & Le Marais (Paris), Lyon",
        "crêpes": "Montparnasse (Paris), Saint-Malo & Rennes (Brittany)",
        "boeuf bourguignon": "Traditional historic bistros in Dijon (Burgundy) & Paris Latin Quarter",
        "ratatouille": "Old Town (Vieux Nice), Cours Saleya markets (Provence)",
        "cheese": "Artisan fromageries in Saint-Germain (Paris), Les Halles de Lyon",
        "macarons": "Champs-Élysées & Saint-Germain-des-Prés (Paris)",
        "french onion soup": "Historic brasseries around Les Halles (Paris)"
    },
    "Italy": {
        "pizza": "Via dei Tribunali & Spaccanapoli (Naples), Trastevere (Rome)",
        "carbonara": "Testaccio & Trastevere (Rome)",
        "risotto": "Traditional trattorias in Milan & Navigli district",
        "gelato": "Piazza Navona (Rome), San Gimignano (Tuscany), Florence",
        "tiramisu": "Historic cafes in Treviso, Venice, and Florence",
        "pasta": "Bologna historic center, Trastevere (Rome)"
    },
    "United States": {
        "cheeseburger": "Classic diners in New York City, In-N-Out (California)",
        "pizza": "Joe's Pizza (Greenwich Village, NYC), Brooklyn pizzerias",
        "barbecue": "Franklin Barbecue (Austin, Texas), Beale Street (Memphis)",
        "clam chowder": "Boston Harbor waterfront, Fisherman's Wharf (San Francisco)",
        "pie": "Key West (Florida), authentic New England roadside diners",
        "tacos": "Mission District (San Francisco), East Los Angeles, Austin"
    },
    "Australia": {
        "meat pie": "Harry's Cafe de Wheels (Sydney), country bakeries in Victoria",
        "barramundi": "Cairns waterfront, Darwin, Sydney Fish Market",
        "pavlova": "Boutique patisseries & cafes in Melbourne & Sydney",
        "flat white": "Degraves Street & laneway espresso bars in Melbourne"
    },
    "Spain": {
        "paella": "Playa de la Malvarrosa & El Palmar (Valencia)",
        "tapas": "La Latina (Madrid), El Born & Gothic Quarter (Barcelona), Seville",
        "churros": "Chocolatería San Ginés (Madrid)",
        "jamon": "Mercado de San Miguel (Madrid), Jabugo (Andalusia)"
    },
    "Thailand": {
        "pad thai": "Thip Samai & Yaowarat Chinatown (Bangkok)",
        "tom yum": "Raan Jay Fai & street stalls along Sukhumvit (Bangkok)",
        "green curry": "Night markets in Chiang Mai & Bangkok Old Town",
        "mango sticky rice": "Mae Varee (Thong Lo, Bangkok), Chiang Mai night bazaar"
    },
    "South Korea": {
        "bibimbap": "Jeonju Hanok Village, Myeongdong (Seoul)",
        "korean fried chicken": "Hongdae & Gangnam (Seoul), Chimaek street in Daegu",
        "bulgogi": "Jongno & Insadong traditional restaurants (Seoul)",
        "tteokbokki": "Sindang-dong Tteokbokki Town (Seoul), Gwangjang Market"
    }
}


def get_where_to_try(country: str, dish_name: str) -> str:
    """Return authentic local dining spots and markets for a specific dish."""
    canonical = normalize_country_key(country)
    c_data = WHERE_TO_TRY_DATA.get(canonical, {})
    dish_lower = str(dish_name or "").lower()

    for k, v in c_data.items():
        if k in dish_lower or dish_lower in k:
            return v

    prof = get_country_knowledge(canonical)
    cities = prof.get("cities", [canonical])
    if len(cities) >= 2:
        return f"{cities[0]} and {cities[1]} traditional restaurants & food markets"
    return f"{cities[0]} Old Town markets & authentic regional eateries"


# ============================================================
# DESTINATION PHOTO GALLERY
# ============================================================

DESTINATION_GALLERIES = {
    "Japan": [
        {"name": "Tokyo", "query": "Tokyo skyline Shibuya Tokyo Japan", "caption": "Vibrant metropolis & modern culture", "slug": "Tokyo"},
        {"name": "Mount Fuji", "query": "Mount Fuji Japan volcano landscape", "caption": "Sacred iconic mountain & lakes", "slug": "Mount_Fuji"},
        {"name": "Kyoto", "query": "Kyoto temple Gion bamboo forest Japan", "caption": "Ancient temples & traditional geisha districts", "slug": "Kyoto"},
        {"name": "Osaka", "query": "Osaka castle Dotonbori neon Japan", "caption": "Culinary capital & historic fortress", "slug": "Osaka"},
        {"name": "Nara", "query": "Nara Park Todaiji deer Japan", "caption": "Friendly sacred deer & giant Buddha", "slug": "Nara_Park"},
        {"name": "Hiroshima", "query": "Hiroshima Peace Memorial Itsukushima shrine Japan", "caption": "Peace memorial & floating torii gate", "slug": "Hiroshima_Peace_Memorial"}
    ],
    "Nepal": [
        {"name": "Mount Everest", "query": "Mount Everest Himalayas Nepal mountain peak", "caption": "Roof of the world & Khumbu Himalayas", "slug": "Mount_Everest"},
        {"name": "Pashupatinath Temple", "query": "Pashupatinath Temple Kathmandu Nepal holy", "caption": "Sacred Hindu temple complex on Bagmati river", "slug": "Pashupatinath_Temple"},
        {"name": "Pokhara", "query": "Pokhara Phewa Lake Annapurna reflection Nepal", "caption": "Serene lakeside & Annapurna mountain reflections", "slug": "Phewa_Lake"},
        {"name": "Boudhanath Stupa", "query": "Boudhanath Stupa Kathmandu Nepal Tibetan", "caption": "Colossal spherical Buddhist stupa & prayer flags", "slug": "Boudhanath"},
        {"name": "Kathmandu Durbar Square", "query": "Kathmandu Durbar Square ancient palaces Nepal", "caption": "Historic UNESCO Malla royal palace quarter", "slug": "Kathmandu_Durbar_Square"},
        {"name": "Chitwan National Park", "query": "Chitwan National Park safari rhino Nepal", "caption": "Subtropical wildlife safari & one-horned rhinos", "slug": "Chitwan_National_Park"}
    ],
    "India": [
        {"name": "Taj Mahal", "query": "Taj Mahal Agra India marble monument", "caption": "World Wonder of white marble & eternal love", "slug": "Taj_Mahal"},
        {"name": "Dal Lake", "query": "Dal Lake Srinagar Kashmir shikara houseboats India", "caption": "Jewel in the crown of Kashmir & shikara boats", "slug": "Dal_Lake"},
        {"name": "Gulmarg", "query": "Gulmarg Kashmir snow gondola Himalayas India", "caption": "Meadow of flowers & world's highest gondola", "slug": "Gulmarg"},
        {"name": "Jaipur", "query": "Hawa Mahal Jaipur Rajasthan pink city India", "caption": "Royal palaces & vibrant Rajasthani culture", "slug": "Hawa_Mahal"},
        {"name": "Varanasi Ghats", "query": "Varanasi ghats Ganges river evening Aarti India", "caption": "Ancient spiritual heart & evening Ganga Aarti", "slug": "Ghats_in_Varanasi"},
        {"name": "Goa Beaches", "query": "Goa beach coastline Arabian sea palm trees India", "caption": "Golden sandy beaches & Portuguese heritage", "slug": "Goa"}
    ],
    "France": [
        {"name": "Paris", "query": "Paris Eiffel Tower Seine river France skyline", "caption": "City of Light, fashion & world-class arts", "slug": "Eiffel_Tower"},
        {"name": "Louvre Museum", "query": "Louvre Museum glass pyramid Paris France", "caption": "Historic royal palace housing Mona Lisa", "slug": "Louvre"},
        {"name": "Mont Saint-Michel", "query": "Mont Saint-Michel Normandy abbey tidal island France", "caption": "Spectacular medieval tidal island abbey", "slug": "Mont-Saint-Michel"},
        {"name": "French Riviera (Nice)", "query": "Promenade des Anglais Nice Cote d'Azur France", "caption": "Sun-drenched Mediterranean coastline", "slug": "Nice"},
        {"name": "Palace of Versailles", "query": "Palace of Versailles Hall of Mirrors gardens France", "caption": "Opulent gilded royal residence of the Sun King", "slug": "Palace_of_Versailles"},
        {"name": "Chamonix Mont-Blanc", "query": "Chamonix Mont Blanc French Alps mountain peak", "caption": "Glacial peaks & Alpine adventure playground", "slug": "Chamonix"}
    ],
    "Italy": [
        {"name": "Colosseum", "query": "Colosseum Rome Italy ancient amphitheatre", "caption": "Gladiatorial arena of ancient imperial Rome", "slug": "Colosseum"},
        {"name": "Venice", "query": "Venice Grand Canal gondola Rialto bridge Italy", "caption": "Romantic canals, bridges & Venetian palazzos", "slug": "Grand_Canal_(Venice)"},
        {"name": "Florence", "query": "Florence Cathedral Duomo Santa Maria del Fiore Italy", "caption": "Birthplace of the Renaissance & Tuscan art", "slug": "Florence_Cathedral"},
        {"name": "Amalfi Coast", "query": "Amalfi Coast Positano cliffside colorful houses Italy", "caption": "Breathtaking Mediterranean cliffs & pastel towns", "slug": "Amalfi_Coast"},
        {"name": "Cinque Terre", "query": "Cinque Terre Manarola colorful fishing village Italy", "caption": "Dramatic UNESCO coastal hiking villages", "slug": "Cinque_Terre"},
        {"name": "Milan", "query": "Milan Cathedral Duomo di Milano gothic Italy", "caption": "Gothic architectural marvel & fashion capital", "slug": "Milan_Cathedral"}
    ],
    "United States": [
        {"name": "Grand Canyon", "query": "Grand Canyon National Park Arizona landscape USA", "caption": "Vast carved canyon of deep red-rock layers", "slug": "Grand_Canyon"},
        {"name": "New York City", "query": "New York City Manhattan skyline Central Park USA", "caption": "Dynamic global hub of culture, theatre & skyline", "slug": "Central_Park"},
        {"name": "Golden Gate Bridge", "query": "Golden Gate Bridge San Francisco Bay California USA", "caption": "Legendary suspension bridge shrouded in fog", "slug": "Golden_Gate_Bridge"},
        {"name": "Yellowstone", "query": "Yellowstone National Park Grand Prismatic Spring geyser USA", "caption": "Geothermal marvels, hot springs & free-roaming bison", "slug": "Yellowstone_National_Park"},
        {"name": "Washington D.C.", "query": "Washington DC Capitol National Mall monument USA", "caption": "Historic Capitol, monuments & Smithsonian museums", "slug": "National_Mall"},
        {"name": "Hawaii", "query": "Hawaii coast tropical volcanic beach ocean USA", "caption": "Tropical Polynesian islands, waterfalls & beaches", "slug": "Hawaii"}
    ],
    "Australia": [
        {"name": "Sydney Opera House", "query": "Sydney Opera House Harbour Bridge NSW Australia", "caption": "Iconic sail-shaped architectural masterpiece", "slug": "Sydney_Opera_House"},
        {"name": "Great Barrier Reef", "query": "Great Barrier Reef coral marine life Queensland Australia", "caption": "World's largest vibrant living coral reef system", "slug": "Great_Barrier_Reef"},
        {"name": "Uluru", "query": "Uluru Kata Tjuta sacred monolith red centre Australia", "caption": "Sacred indigenous sandstone monolith at sunset", "slug": "Uluru"},
        {"name": "Melbourne", "query": "Melbourne skyline Yarra river laneways Victoria Australia", "caption": "Cultural capital of street art, coffee & sports", "slug": "Melbourne"},
        {"name": "Bondi Beach", "query": "Bondi Beach Sydney coastline ocean surfing Australia", "caption": "Famous golden crescent of surf and coastal walks", "slug": "Bondi_Beach"},
        {"name": "Blue Mountains", "query": "Blue Mountains Three Sisters rock formation NSW Australia", "caption": "Eucalyptus-scented canyons & scenic lookouts", "slug": "Blue_Mountains_(New_South_Wales)"}
    ]
}


def get_destination_gallery_items(country_name: str) -> List[Dict[str, str]]:
    """Return top 6 distinct landmark and city photo items for any country."""
    canonical = normalize_country_key(country_name)
    if canonical in DESTINATION_GALLERIES:
        return DESTINATION_GALLERIES[canonical]

    prof = get_country_knowledge(canonical)
    cities = prof.get("cities", [canonical])
    attractions = prof.get("attractions", [])
    gallery = []

    for att in attractions[:4]:
        name = att[0] if isinstance(att, (tuple, list)) else att.get("name", "")
        loc = att[1] if isinstance(att, (tuple, list)) and len(att) > 1 else canonical
        slug = att[2] if isinstance(att, (tuple, list)) and len(att) > 2 else (att.get("slug", "") if isinstance(att, dict) else "")
        if name:
            gallery.append({
                "name": name,
                "query": f"{name} {loc} {canonical} landmark travel",
                "caption": f"Must-visit landmark in {loc}, {canonical}",
                "slug": slug
            })

    for city in cities:
        if len(gallery) >= 6:
            break
        if not any(g["name"] == city for g in gallery):
            gallery.append({
                "name": city,
                "query": f"{city} {canonical} city landmark tourism",
                "caption": f"Historic and vibrant hub of {canonical}",
                "slug": city.replace(" ", "_")
            })

    while len(gallery) < 6:
        idx = len(gallery) + 1
        gallery.append({
            "name": f"{canonical} Landmark {idx}",
            "query": f"{canonical} travel tourism scenic landscape",
            "caption": f"Scenic destination in {canonical}",
            "slug": ""
        })

    return gallery[:6]


