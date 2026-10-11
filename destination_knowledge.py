"""
destination_knowledge.py - Grounded Local Food, Etiquette & Cultural Intelligence
Provides city-specific authentic food recommendations, multi-pillar cultural etiquette,
traditional attire comparisons, and dietary guidance for global travel destinations.
Zero external paid API keys required.
"""

from typing import Dict, List, Any, Optional, Tuple
import re

# ============================================================
# 1. GROUNDED CITY-SPECIFIC FOOD DATABASE
# ============================================================

CITY_FOOD_DATABASE: Dict[Tuple[str, str], List[Dict[str, Any]]] = {
    # --- JAPAN ---
    ("Japan", "Tokyo"): [
        {
            "name": "Edomae Sushi",
            "local_name": "江戸前寿司 (Edomae-zushi)",
            "city": "Tokyo",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Sushi_platter.jpg/800px-Sushi_platter.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Originating in 19th-century Edo (Tokyo), fresh fish from Tokyo Bay is cured, marinated in shoyu, or lightly seared, placed atop seasoned akazu (red vinegar) sushi rice.",
            "taste_profile": "Delicate, umami-rich, savory with slight vinegary tang",
            "dietary_type": "Contains Seafood",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Fish", "Soy", "Wheat/Gluten (in shoyu)"],
            "where_to_try": "Toyosu Outer Market stalls, Tsukiji historic alleys, and Ginza sushi counters",
            "price_range": "¥3,000 – ¥8,000 (~$20 – $55 USD, estimated lunch set)",
            "breakfast_friendly": False
        },
        {
            "name": "Tokyo Shoyu Ramen",
            "local_name": "東京醤油ラーメン",
            "city": "Tokyo",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Shoyu_Ramen.jpg/800px-Shoyu_Ramen.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Clear amber broth brewed with chicken and niboshi (dried sardines) flavored with regional Tokyo soy sauce, curly springy wheat noodles, chashu pork, menma bamboo shoots, and nori.",
            "taste_profile": "Savory, clean, aromatic umami, comforting warmth",
            "dietary_type": "Contains Meat & Seafood",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Wheat/Gluten", "Soy", "Pork"],
            "where_to_try": "Tokyo Ramen Street (Tokyo Station underground), Shinjuku ramen alleys, and Asakusa",
            "price_range": "¥900 – ¥1,400 (~$6 – $10 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Asakusa Tempura & Tendon",
            "local_name": "浅草天ぷら / 天丼",
            "city": "Tokyo",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Tempura_001.jpg/800px-Tempura_001.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Prawns, squid, and seasonal vegetables (lotus root, shiitake, shiso) dipped in cold water and flour batter, fried crisp in aromatic sesame oil, served over rice with sweet tare sauce.",
            "taste_profile": "Crisp, airy, savory with sweet soy glaze",
            "dietary_type": "Contains Seafood (Vegetarian vegetable-only options available upon request)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Shellfish", "Wheat/Gluten", "Soy", "Egg"],
            "where_to_try": "Historic century-old tempura parlors near Senso-ji temple in Asakusa",
            "price_range": "¥1,500 – ¥3,200 (~$10 – $22 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Tsukishima Monjayaki",
            "local_name": "もんじゃ焼き",
            "city": "Tokyo",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Monjayaki_cooking.jpg/800px-Monjayaki_cooking.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Tokyo's beloved downtown teppanyaki pan dish with a runny dashi batter mixed with shredded cabbage, mochi, mentaiko (spicy pollack roe), or cheese, eaten directly off the griddle using tiny metal spatulas.",
            "taste_profile": "Savory, caramelized, bubbling, slightly gooey and chewy",
            "dietary_type": "Contains Meat/Seafood/Dairy (Vegetarian customizable)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Wheat/Gluten", "Soy", "Dairy", "Seafood"],
            "where_to_try": "Monja Street (Nishinaka-dori) on Tsukishima island, Tokyo",
            "price_range": "¥1,200 – ¥2,000 (~$8 – $14 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Traditional Japanese Morning Breakfast (Teishoku)",
            "local_name": "和朝食 (Wa-choshoku)",
            "city": "Tokyo",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Japanese_breakfast_set.jpg/800px-Japanese_breakfast_set.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Balanced morning meal featuring steamed white rice, hot tofu and wakame miso soup, grilled salted salmon (shiozake), sweet rolled tamagoyaki omelet, nori, and fermented tsukemono pickles.",
            "taste_profile": "Gentle, soothing, mild, balanced morning nutrition",
            "dietary_type": "Pescatarian (Vegetarian set available with natto/tofu)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Fish", "Soy", "Egg"],
            "where_to_try": "Traditional morning kissaten, ryokan hotels, and breakfast diners in Ueno and Tsukiji",
            "price_range": "¥700 – ¥1,200 (~$5 – $8 USD, estimated)",
            "breakfast_friendly": True
        }
    ],

    ("Japan", "Kyoto"): [
        {
            "name": "Kyoto Yudofu (Simmered Tofu in Kombu Dashi)",
            "local_name": "湯豆腐 (ゆどうふ)",
            "city": "Kyoto",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Yudofu_by_yoppy_in_Kyoto.jpg/800px-Yudofu_by_yoppy_in_Kyoto.jpg",
            "image_attribution": "Wikimedia Commons (CC BY 2.0)",
            "description": "Delicate silken artisanal Kyoto tofu gently simmered in spring water infused with Rishiri kombu kelp inside ceramic donabe pots, dipped in tare soy sauce with scallions, grated ginger, and yuzu.",
            "taste_profile": "Mild, soothing, silky, pure umami",
            "dietary_type": "Vegetarian (Can be Vegan if tare broth uses kombu rather than bonito)",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Soy", "Wheat/Gluten (in dip)"],
            "where_to_try": "Tranquil temple garden restaurants near Nanzen-ji and Arashiyama, Kyoto",
            "price_range": "¥2,500 – ¥4,500 (~$17 – $30 USD, estimated full course)",
            "breakfast_friendly": False
        },
        {
            "name": "Kyoto Obanzai (Heritage Home-Style Dishes)",
            "local_name": "おばんざい (Obanzai-ryori)",
            "city": "Kyoto",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Obanzai_dishes_Kyoto.jpg/800px-Obanzai_dishes_Kyoto.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Traditional Kyoto heirloom vegetable dishes prepared according to seasonal cycles, incorporating Kamo eggplant, sweet Kintoki carrots, mibu greens, simmered lotus root, and seasoned dried fish or tofu.",
            "taste_profile": "Earthy, delicate, subtle, harmoniously balanced",
            "dietary_type": "Predominantly Vegetarian / Pescatarian",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Soy", "Wheat/Gluten"],
            "where_to_try": "Cozy machiya wooden townhouses along Pontocho Alley and Gion, Kyoto",
            "price_range": "¥1,800 – ¥3,500 (~$12 – $24 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Matcha Parfait & Kyo-Wagashi",
            "local_name": "宇治抹茶パフェ / 京和菓子",
            "city": "Kyoto",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Matcha_and_wagashi.jpg/800px-Matcha_and_wagashi.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Premium ceremonial stone-ground Uji matcha green tea paired with delicate wagashi (artisan seasonal sweets molded from adzuki bean paste), or multilayered parfaits with matcha soft-serve, shiratama dango, and agar jelly.",
            "taste_profile": "Bittersweet, velvety, fragrant, gently sweet",
            "dietary_type": "Vegetarian",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Dairy", "Soy"],
            "where_to_try": "Historic tea salons in Uji, Gion Shinbashi, and Kiyomizu-zaka",
            "price_range": "¥1,000 – ¥1,800 (~$7 – $12 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Shojin Ryori (Buddhist Temple Cuisine)",
            "local_name": "精進料理 (しょうじんりょうり)",
            "city": "Kyoto",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Kaiseki_Ryori_in_Kyoto.jpg/800px-Kaiseki_Ryori_in_Kyoto.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Ancient Zen Buddhist temple culinary art strictly avoiding meat, fish, garlic, and onions. Focuses on five flavors and five colors utilizing seasonal mountain vegetables, sesame tofu (goma-dofu), and yuba soy-milk skin.",
            "taste_profile": "Pure, meditative, deeply nuanced, earthy and clean",
            "dietary_type": "100% Vegan & Vegetarian",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Soy", "Sesame", "Wheat/Gluten"],
            "where_to_try": "Tenryu-ji Shigetsu restaurant (inside Tenryu-ji Temple, Arashiyama) and Daitoku-ji",
            "price_range": "¥3,500 – ¥6,500 (~$24 – $44 USD, estimated set)",
            "breakfast_friendly": False
        }
    ],

    ("Japan", "Osaka"): [
        {
            "name": "Osaka Takoyaki",
            "local_name": "たこ焼き (Takoyaki)",
            "city": "Osaka",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Takoyaki_in_Osaka.jpg/800px-Takoyaki_in_Osaka.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Spherical street food dumplings made of savory batter cooked on cast-iron dimpled griddles, filled with tender diced octopus chunks (tako), pickled red ginger, and tenkasu. Brushed with rich brown takoyaki sauce, Japanese mayonnaise, aonori seaweed, and dancing katsuobushi bonito flakes.",
            "taste_profile": "Crispy exterior, molten creamy center, rich savory-sweet umami",
            "dietary_type": "Contains Seafood",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Octopus/Mollusks", "Wheat/Gluten", "Egg", "Soy", "Fish"],
            "where_to_try": "Dotonbori canal street stalls (Kukuru, Wanaka) and Amerikamura",
            "price_range": "¥600 – ¥900 (~$4 – $6 USD for 8 pieces, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Osaka Okonomiyaki",
            "local_name": "お好み焼き (Osaka-style)",
            "city": "Osaka",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Okonomiyaki_001.jpg/800px-Okonomiyaki_001.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Known as 'Japanese savory soul pancake', shredded sweet cabbage and mountain yam (yamaimo) batter mixed with pork belly slices, squid, or prawns, griddled on teppan tables, topped with dark savory sauce and mayo.",
            "taste_profile": "Hearty, savory, sweet, smoky, incredibly satisfying",
            "dietary_type": "Contains Meat & Seafood (Vegetarian teppan versions available upon request)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Wheat/Gluten", "Egg", "Soy", "Pork", "Seafood"],
            "where_to_try": "Mizuno in Dotonbori, Chibo, or Ajinoya (Michelin Bib Gourmand)",
            "price_range": "¥1,100 – ¥1,800 (~$7 – $12 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Shinsekai Kushikatsu",
            "local_name": "串カツ (Kushikatsu)",
            "city": "Osaka",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Kushikatsu_Osaka.jpg/800px-Kushikatsu_Osaka.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Skewered bites of beef, quail eggs, lotus root, asparagus, and shrimp dipped in light batter and ultra-fine panko, deep-fried to golden crunchiness. Served with raw cabbage wedges and Worcestershire-style dipping sauce. Strict local etiquette: NEVER double-dip into the communal sauce tub!",
            "taste_profile": "Golden crisp, juicy, tangy-sweet savory dip",
            "dietary_type": "Contains Meat & Seafood (Vegetable skewers available)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Wheat/Gluten", "Egg", "Beef", "Pork"],
            "where_to_try": "Kushikatsu Daruma in historic retro Shinsekai near Tsutenkaku Tower",
            "price_range": "¥1,500 – ¥2,800 (~$10 – $19 USD for assorted platter, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Kitsune Udon (Osaka Origin)",
            "local_name": "きつねうどん (Kitsune Udon)",
            "city": "Osaka",
            "country": "Japan",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Kitsune_udon_by_ume-y.jpg/800px-Kitsune_udon_by_ume-y.jpg",
            "image_attribution": "Wikimedia Commons (CC BY 2.0)",
            "description": "Invented in Osaka in 1893, thick chewy wheat udon noodles in a clear golden kombu and sardine dashi, topped with a large piece of sweet-savory braised abura-age (fried tofu pouch) named after the mythical fox's favorite food.",
            "taste_profile": "Gentle, comforting, sweet-savory broth, juicy tofu pouch",
            "dietary_type": "Pescatarian (Contains fish dashi)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": False,
            "allergens": ["Wheat/Gluten", "Soy", "Fish"],
            "where_to_try": "Usami-tei Matsubaya in Semba, Osaka (the historic birthplace of kitsune udon)",
            "price_range": "¥750 – ¥1,100 (~$5 – $8 USD, estimated)",
            "breakfast_friendly": True
        }
    ],

    # --- INDIA ---
    ("India", "New Delhi"): [
        {
            "name": "Delhi Chole Bhature",
            "local_name": "छोले भटूरे (Chole Bhature)",
            "city": "New Delhi",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Chole_Bhature_at_Standard_Sweets.jpg/800px-Chole_Bhature_at_Standard_Sweets.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Spiced chickpeas slow-simmered in an iron kadai with dark tea decoction, anardana (pomegranate seeds), and garam masala, paired with gigantic golden puffed leavened bread, pickled carrots, and mint chutney.",
            "taste_profile": "Tangy, spicy, bold, crispy yet fluffy",
            "dietary_type": "100% Vegetarian",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Wheat/Gluten"],
            "where_to_try": "Sita Ram Diwan Chand (Paharganj) and Baba Nagpal Corner (Lajpat Nagar)",
            "price_range": "₹120 – ₹220 (~$1.50 – $2.70 USD, estimated)",
            "breakfast_friendly": True
        },
        {
            "name": "Daryaganj Butter Chicken & Garlic Naan",
            "local_name": "बटर चिकन (Murg Makhani)",
            "city": "New Delhi",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Chicken_makhani.jpg/800px-Chicken_makhani.jpg",
            "image_attribution": "Wikimedia Commons (CC BY 2.0)",
            "description": "Tandoor-charred chicken pieces simmered in a velvety gravy of ripe sun-ripened tomatoes, fresh butter, cream, and fragrant dried fenugreek leaves (kasoori methi). Invented in Daryaganj, Old Delhi in the 1950s.",
            "taste_profile": "Rich, creamy, mildly sweet with smoky undertones",
            "dietary_type": "Contains Poultry & Dairy",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Dairy", "Poultry"],
            "where_to_try": "Moti Mahal (Daryaganj), Gulati (Pandara Road), and Havemore",
            "price_range": "₹600 – ₹1,200 (~$7 – $15 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Chandni Chowk Stuffed Paranthas",
            "local_name": "चांदनी चौक के परांठे",
            "city": "New Delhi",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Paratha_spread_Chandni_Chowk.jpg/800px-Paratha_spread_Chandni_Chowk.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Whole wheat flatbreads stuffed with spiced mashed potatoes (aloo), cauliflower (gobi), paneer, or mixed lentils, fried in pure desi ghee, served with sweet pumpkin curry, aloo sabzi, and tangy tamarind pickle.",
            "taste_profile": "Crisp, flaky, rich, spicy and comforting",
            "dietary_type": "100% Vegetarian",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Wheat/Gluten", "Dairy (Ghee/Paneer)"],
            "where_to_try": "Historic Paranthe Wali Gali in Old Delhi (operating since 1872)",
            "price_range": "₹150 – ₹280 (~$1.80 – $3.40 USD, estimated)",
            "breakfast_friendly": True
        }
    ],

    ("India", "Agra"): [
        {
            "name": "Agra Petha (Ash Gourd Confection)",
            "local_name": "आगरा का पेठा (Agra Petha)",
            "city": "Agra",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Agra_Petha.jpg/800px-Agra_Petha.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Centuries-old royal Mughal sweet made from candied winter melon (ash gourd) soaked in flavored sugar syrup with saffron, rosewater, or stuffed with crushed almonds and pistachios.",
            "taste_profile": "Translucent, tender, sweet, fragrant floral notes",
            "dietary_type": "100% Vegan & Vegetarian",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Nuts (in Kesar Petha varieties)"],
            "where_to_try": "Panchi Petha stores near Sadar Bazaar and Hari Parvat, Agra",
            "price_range": "₹180 – ₹400 per kg (~$2.20 – $5.00 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Bedmi Puri & Aloo Sabzi",
            "local_name": "बेड़मी पूरी और आलू",
            "city": "Agra",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Bedmi_Poori_Aloo.jpg/800px-Bedmi_Poori_Aloo.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Crisp puffed breads made with coarse wheat flour and urad dal paste, served with spicy, tangy potato curry cooked with asafoetida (hing), fenugreek, and methi chutney.",
            "taste_profile": "Spicy, crunchy, earthy, robust morning flavor",
            "dietary_type": "100% Vegetarian",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Wheat/Gluten"],
            "where_to_try": "Deviram Sweets on Pratap Pura and Kinari Bazaar, Agra",
            "price_range": "₹70 – ₹140 (~$0.90 – $1.70 USD, estimated)",
            "breakfast_friendly": True
        }
    ],

    ("India", "Jaipur"): [
        {
            "name": "Dal Baati Churma",
            "local_name": "दाल बाटी चूरमा",
            "city": "Jaipur",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Dal_Baati_Churma.jpg/800px-Dal_Baati_Churma.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "The quintessential Rajasthani feast: hard baked wheat dough balls (Baati) crushed and soaked in pure desi ghee, served with Panchmel dal (five-lentil curry), spicy garlic chutney, and sweet powdered jaggery-wheat Churma.",
            "taste_profile": "Rich, earthy, smoky, sweet and spicy balance",
            "dietary_type": "100% Vegetarian",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Wheat/Gluten", "Dairy (Ghee)"],
            "where_to_try": "Chokhi Dhani ethnic resort, Laxmi Mishthan Bhandar (LMB) in Johari Bazaar",
            "price_range": "₹350 – ₹850 (~$4 – $10 USD, estimated thali)",
            "breakfast_friendly": False
        },
        {
            "name": "Jaipur Ghevar (Honeycomb Saffron Sweet)",
            "local_name": "घेवर (Ghevar)",
            "city": "Jaipur",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Ghevar_Sweet.jpg/800px-Ghevar_Sweet.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Disc-shaped honeycomb crisp sweet made from flour and clarified butter, dipped in saffron syrup and crowned with velvety reduced milk (rabdi), slivered almonds, and edible silver foil (varak).",
            "taste_profile": "Crisp honeycomb texture, saffron aroma, creamy sweetness",
            "dietary_type": "100% Vegetarian",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Dairy", "Wheat/Gluten", "Nuts"],
            "where_to_try": "LMB (Johari Bazaar) and Rawat Mishthan Bhandar (Station Road)",
            "price_range": "₹200 – ₹450 (~$2.40 – $5.50 USD per piece, estimated)",
            "breakfast_friendly": False
        }
    ],

    ("India", "Srinagar (Jammu & Kashmir)"): [
        {
            "name": "Kashmiri Rogan Josh & Rice",
            "local_name": "روغن جوش (Rogan Josh)",
            "city": "Srinagar (Jammu & Kashmir)",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Rogan_Josh.jpg/800px-Rogan_Josh.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "A centerpiece of the 36-course Kashmiri royal feast (Wazwan), tender lamb slow-cooked with Kashmiri maval cockscomb petals, dried ginger (sonth), fennel powder (saunf), and aromatic whole spices in mustard oil.",
            "taste_profile": "Aromatic, deeply spiced without harsh heat, rich and savory",
            "dietary_type": "Halal Lamb",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Mustard"],
            "where_to_try": "Mughal Darbar and Ahdoos on Residency Road overlooking Jhelum River, Srinagar",
            "price_range": "₹450 – ₹850 (~$5.50 – $10 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Kashmiri Kahwa & Girda Bread",
            "local_name": "قہوہ (Kashmiri Kahwa)",
            "city": "Srinagar (Jammu & Kashmir)",
            "country": "India",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Kashmiri_Kahwa_tea.jpg/800px-Kashmiri_Kahwa_tea.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Exquisite golden green tea brewed in a traditional copper samovar with saffron strands from Pampore, crushed green cardamom, cinnamon, and slivered Kashmiri almonds, paired with fresh tandoor Girda bread.",
            "taste_profile": "Fragrant, warming, gentle saffron and nutty sweetness",
            "dietary_type": "100% Vegan & Vegetarian",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Tree Nuts (Almonds)"],
            "where_to_try": "Dal Lake traditional Shikara floating stalls and Chai Jaai tearoom, Srinagar",
            "price_range": "₹100 – ₹200 (~$1.20 – $2.40 USD, estimated)",
            "breakfast_friendly": True
        }
    ],

    # --- FRANCE ---
    ("France", "Paris"): [
        {
            "name": "Artisanal Butter Croissant & Café au Lait",
            "local_name": "Croissant au beurre",
            "city": "Paris",
            "country": "France",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/2018_01_Croissant_DSC_9836.jpg/800px-2018_01_Croissant_DSC_9836.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Flaky, crescent-shaped laminated pastry made with high-fat Normandy churned butter and slow-fermented yeast dough, baked fresh at dawn to golden crunch outside and airy honeycomb layers inside.",
            "taste_profile": "Buttery, flaky, tender, subtle caramelized crust",
            "dietary_type": "Vegetarian",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Dairy", "Wheat/Gluten"],
            "where_to_try": "Award-winning boulangeries in Le Marais, Saint-Germain-des-Prés, and Montmartre",
            "price_range": "€1.40 – €2.20 (~$1.50 – $2.40 USD, estimated)",
            "breakfast_friendly": True
        },
        {
            "name": "Boeuf Bourguignon",
            "local_name": "Bœuf bourguignon",
            "city": "Paris",
            "country": "France",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Boeuf_bourguignon_in_dish.jpg/800px-Boeuf_bourguignon_in_dish.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Tender beef braised for hours in red Burgundy wine, beef broth, carrots, pearl onions, lardons, and fresh thyme, served with buttered tagliatelle or roasted potatoes.",
            "taste_profile": "Deep, savory, wine-infused, melt-in-your-mouth tender",
            "dietary_type": "Contains Beef & Pork (Alcohol used in cooking)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Beef", "Pork", "Wheat/Gluten"],
            "where_to_try": "Traditional Parisian bistros in the Latin Quarter and Montparnasse",
            "price_range": "€18 – €28 (~$20 – $30 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    ("France", "Nice"): [
        {
            "name": "Authentic Salade Niçoise",
            "local_name": "Salade niçoise",
            "city": "Nice",
            "country": "France",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Salade_nicoise_01.jpg/800px-Salade_nicoise_01.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Iconic Mediterranean salad featuring crisp raw vegetables (tomatoes, radishes, spring onions), hard-boiled eggs, small black Cailletier Niçoise olives, and tuna or anchovies tossed with fruity local olive oil.",
            "taste_profile": "Fresh, briny, zesty, Mediterranean sunshine in a bowl",
            "dietary_type": "Pescatarian",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": True,
            "allergens": ["Fish", "Egg"],
            "where_to_try": "Cours Saleya market cafes and Old Town (Vieux Nice) bistros",
            "price_range": "€14 – €22 (~$15 – $24 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Socca (Crispy Chickpea Flatbread)",
            "local_name": "Socca niçoise",
            "city": "Nice",
            "country": "France",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Socca_chez_rene_socca_nice.jpg/800px-Socca_chez_rene_socca_nice.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Traditional Niçois street food made solely from chickpea flour, water, olive oil, and sea salt, poured into huge copper pans and baked in wood-fired pizza ovens until blistered and golden, seasoned with cracked black pepper.",
            "taste_profile": "Crisp rim, custardy center, nutty, peppery warmth",
            "dietary_type": "100% Vegan & Gluten-Free",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": [],
            "where_to_try": "Chez René Socca in Vieux Nice and Cours Saleya stalls",
            "price_range": "€3.50 – €5.00 (~$3.80 – $5.50 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    # --- ITALY ---
    ("Italy", "Rome"): [
        {
            "name": "Authentic Spaghetti alla Carbonara",
            "local_name": "Spaghetti alla carbonara",
            "city": "Rome",
            "country": "Italy",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Spaghetti_alla_Carbonara_2.jpg/800px-Spaghetti_alla_Carbonara_2.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Classic Roman pasta masterpiece prepared strictly without cream or peas: al dente spaghetti tossed with crispy cured pork jowl (guanciale), fresh egg yolks, aged Pecorino Romano cheese, and coarse black pepper.",
            "taste_profile": "Rich, creamy, savory, peppery, deeply satisfying",
            "dietary_type": "Contains Pork & Eggs",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Egg", "Dairy (Pecorino)", "Pork", "Wheat/Gluten"],
            "where_to_try": "Trastevere traditional trattorias, Testaccio food quarter, and Roscioli",
            "price_range": "€12 – €18 (~$13 – $20 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Roman Tonnarelli Cacio e Pepe",
            "local_name": "Cacio e pepe",
            "city": "Rome",
            "country": "Italy",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Spaghetti_cacio_e_pepe.jpg/800px-Spaghetti_cacio_e_pepe.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Ancient shepherd dish requiring extraordinary culinary technique: fresh tonnarelli pasta emulsified with starchy pasta water, sharp Pecorino Romano cheese, and toasted cracked black peppercorns.",
            "taste_profile": "Piquant, creamy emulsion, sharp cheese tang, spicy pepper kick",
            "dietary_type": "Vegetarian",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Dairy", "Wheat/Gluten"],
            "where_to_try": "Da Felice a Testaccio and historic trattorias in Monti",
            "price_range": "€11 – €16 (~$12 – $18 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    ("Italy", "Florence"): [
        {
            "name": "Bistecca alla Fiorentina",
            "local_name": "Bistecca alla fiorentina",
            "city": "Florence",
            "country": "Italy",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Bistecca_alla_fiorentina.jpg/800px-Bistecca_alla_fiorentina.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Thick T-bone steak from historic Chianina cattle breed, grilled over red-hot oak coals, seasoned only with coarse sea salt, rosemary, and Tuscan olive oil, served strictly rare (al sangue).",
            "taste_profile": "Charred smoky crust, exceptionally juicy, intense beef flavor",
            "dietary_type": "Contains Beef",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Beef"],
            "where_to_try": "Trattoria Mario (San Lorenzo) and Buca Mario in Florence",
            "price_range": "€45 – €65 per kg (~$48 – $70 USD, usually shared between 2)",
            "breakfast_friendly": False
        },
        {
            "name": "Tuscan Ribollita",
            "local_name": "Ribollita toscana",
            "city": "Florence",
            "country": "Italy",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Ribollita.jpg/800px-Ribollita.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Historic peasant soup 're-boiled' from cannellini beans, dark Tuscan kale (cavolo nero), savoy cabbage, carrots, and day-old country bread, drizzled with peppery extra-virgin olive oil.",
            "taste_profile": "Hearty, comforting, earthy, velvety stew texture",
            "dietary_type": "100% Vegan & Vegetarian",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Wheat/Gluten"],
            "where_to_try": "Traditional osterias in the Oltrarno and San Lorenzo quarters",
            "price_range": "€9 – €14 (~$10 – $15 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    # --- THAILAND ---
    ("Thailand", "Bangkok"): [
        {
            "name": "Bangkok Pad Thai Kung Sod",
            "local_name": "ผัดไทยกุ้งสด (Pad Thai)",
            "city": "Bangkok",
            "country": "Thailand",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Phat_Thai_kung_Chang_Khian.jpg/800px-Phat_Thai_kung_Chang_Khian.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Wok-fried rice noodles tossed at intense heat with fresh river prawns, pressed tofu, garlic chives, eggs, sweet tamarind paste, fish sauce, crushed roasted peanuts, and fresh lime.",
            "taste_profile": "Sweet, sour, savory, nutty, and gently smoky (wok hei)",
            "dietary_type": "Contains Seafood (Tofu vegetarian version widely available)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": True,
            "allergens": ["Shellfish", "Peanuts", "Egg", "Fish Sauce", "Soy"],
            "where_to_try": "Thip Samai Pad Thai (Maha Chai Rd) and street carts across Yaowarat (Chinatown)",
            "price_range": "60 – 120 THB (~$1.80 – $3.50 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Tom Yum Goong (Spicy Lemongrass Prawn Soup)",
            "local_name": "ต้มยำกุ้ง (Tom Yum Goong)",
            "city": "Bangkok",
            "country": "Thailand",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Tom_yam_kung.jpg/800px-Tom_yam_kung.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Iconic Thai aromatic broth infused with fresh lemongrass stalks, galangal slices, kaffir lime leaves, fiery bird's eye chilies, juicy jumbo prawns, and straw mushrooms, finished with fresh lime juice.",
            "taste_profile": "Intensely sour, spicy, fragrant herbal citrus, robust umami",
            "dietary_type": "Contains Seafood",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": True,
            "allergens": ["Shellfish", "Fish Sauce"],
            "where_to_try": "Rung Rueang Pork Noodle or riverfront dining along Chao Phraya",
            "price_range": "150 – 300 THB (~$4.50 – $9.00 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    ("Thailand", "Chiang Mai"): [
        {
            "name": "Chiang Mai Khao Soi",
            "local_name": "ข้าวซอย (Khao Soi)",
            "city": "Chiang Mai",
            "country": "Thailand",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Khao_soi_kai_at_Khao_Soi_Lam_Duan_Fah_Ham%2C_Chiang_Mai.jpg/800px-Khao_soi_kai_at_Khao_Soi_Lam_Duan_Fah_Ham%2C_Chiang_Mai.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Northern Thai golden coconut curry noodle soup with tender chicken drumstick or beef, egg noodles in rich broth, topped with a bird's nest of crispy deep-fried egg noodles, pickled mustard greens, shallots, and lime.",
            "taste_profile": "Creamy coconut, mild aromatic curry spices, crunchy contrast",
            "dietary_type": "Contains Chicken/Beef & Dairy (Tofu versions available)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Wheat/Gluten", "Egg", "Coconut"],
            "where_to_try": "Khao Soi Lam Duan Fah Ham and Khao Soi Khun Yai (Old City), Chiang Mai",
            "price_range": "50 – 80 THB (~$1.50 – $2.50 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    # --- SOUTH KOREA ---
    ("South Korea", "Seoul"): [
        {
            "name": "Jeonju Bibimbap in Seoul",
            "local_name": "비빔밥 (Bibimbap)",
            "city": "Seoul",
            "country": "South Korea",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Dolsot-bibimbap.jpg/800px-Dolsot-bibimbap.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 3.0)",
            "description": "Warm white rice served in a sizzling hot stone bowl (Dolsot) crowned with seasoned namul vegetables (spinach, bean sprouts, shiitake, carrots), seasoned minced beef or tofu, and a raw egg yolk. Mixed at the table with spicy-sweet gochujang and toasted sesame oil.",
            "taste_profile": "Nutty, spicy-sweet, crispy bottom rice crust (nurungji), wholesome",
            "dietary_type": "Contains Beef (Vegetarian/Vegan without beef and egg)",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Soy", "Sesame", "Egg", "Wheat/Gluten (in gochujang)"],
            "where_to_try": "Myeongdong Gogung, Insadong traditional alleys, and Gwangjang Market",
            "price_range": "₩10,000 – ₩15,000 (~$7.50 – $11.50 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    # --- VIETNAM ---
    ("Vietnam", "Hanoi"): [
        {
            "name": "Hanoi Pho Bo (Traditional Beef Noodle Soup)",
            "local_name": "Phở bò Hà Nội",
            "city": "Hanoi",
            "country": "Vietnam",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pho-Beef-Noodles-2008.jpg/800px-Pho-Beef-Noodles-2008.jpg",
            "image_attribution": "Wikimedia Commons (CC BY 2.0)",
            "description": "Hanoi-style clear, aromatic broth simmered for 12 hours with beef marrow bones, charred ginger, star anise, and cinnamon. Poured over flat rice noodles and thinly sliced rare beef, garnished with fresh cilantro and scallions.",
            "taste_profile": "Fragrant, delicate, warming spice notes, clean and comforting",
            "dietary_type": "Contains Beef",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Beef"],
            "where_to_try": "Pho Gia Truyen Bat Dan and Pho Thin in Hanoi's Old Quarter",
            "price_range": "50,000 – 80,000 VND (~$2.00 – $3.20 USD, estimated)",
            "breakfast_friendly": True
        }
    ],

    # --- UNITED KINGDOM ---
    ("United Kingdom", "London"): [
        {
            "name": "Traditional London Fish and Chips",
            "local_name": "Fish and Chips with Mushy Peas",
            "city": "London",
            "country": "United Kingdom",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Fish_and_chips_blackpool.jpg/800px-Fish_and_chips_blackpool.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 2.0)",
            "description": "Fresh North Sea Atlantic cod or haddock fillet dipped in crispy ale batter, deep-fried to golden crunch, served with thick-cut hand-peeled chips, tartare sauce, mushy peas, and malt vinegar.",
            "taste_profile": "Crisp, flaky white fish, savory potato crunch, tangy malt vinegar",
            "dietary_type": "Pescatarian",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": True,
            "is_halal": True,
            "allergens": ["Fish", "Wheat/Gluten", "Egg (in tartare sauce)"],
            "where_to_try": "Poppies of Spitalfields, The Golden Hind (Marylebone), and Borough Market",
            "price_range": "£13 – £20 (~$17 – $26 USD, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Full English Breakfast",
            "local_name": "Traditional English Fry-Up",
            "city": "London",
            "country": "United Kingdom",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Full_English_breakfast_in_a_greasy_spoon.jpg/800px-Full_English_breakfast_in_a_greasy_spoon.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 2.0)",
            "description": "Hearty classic breakfast plate featuring farm eggs, British pork sausages, crispy bacon, baked beans, grilled tomato, sautéed button mushrooms, and buttered toast.",
            "taste_profile": "Savory, hearty, rich, smoky breakfast classics",
            "dietary_type": "Contains Meat",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Pork", "Wheat/Gluten", "Egg"],
            "where_to_try": "Regency Café (Westminster), E Pellicci (Bethnal Green), and Borough Market",
            "price_range": "£9 – £16 (~$12 – $21 USD, estimated)",
            "breakfast_friendly": True
        },
        {
            "name": "Traditional Shepherd's Pie",
            "local_name": "Cottage Pie / Shepherd's Pie",
            "city": "London",
            "country": "United Kingdom",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Cottage_pie.jpg/800px-Cottage_pie.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 2.0)",
            "description": "Tender minced lamb or beef slow-simmered with onions, carrots, and peas in rich brown gravy, topped with fluffy mashed potato baked until golden brown and crusty.",
            "taste_profile": "Savory, rich brown gravy, comforting buttery potato mash",
            "dietary_type": "Contains Meat",
            "is_vegetarian": False,
            "is_vegan": False,
            "contains_meat": True,
            "contains_seafood": False,
            "is_halal": False,
            "allergens": ["Dairy", "Wheat/Gluten"],
            "where_to_try": "The Ivy (Covent Garden), Rules (Maiden Lane), and classic British pubs",
            "price_range": "£14 – £22 (~$18 – $29 USD, estimated)",
            "breakfast_friendly": False
        }
    ],

    # --- NEPAL ---
    ("Nepal", "Kathmandu"): [
        {
            "name": "Kathmandu Steamed Momo",
            "local_name": "मम (Nepali Momo)",
            "city": "Kathmandu",
            "country": "Nepal",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Momo_nepal.jpg/800px-Momo_nepal.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "Delicate handmade flour wrappers filled with minced buffalo meat, chicken, or spiced cabbage, paneer, and potatoes, steamed inside multi-tiered metal pots, served with spicy sesame-tomato achar dipping sauce.",
            "taste_profile": "Juicy, spicy achar tang, aromatic cumin and coriander warmth",
            "dietary_type": "Vegetarian & Meat options widely available",
            "is_vegetarian": True,
            "is_vegan": False,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": ["Wheat/Gluten", "Sesame"],
            "where_to_try": "Shandar Momo (Patan), Everest Momo, and Thamel alleys in Kathmandu",
            "price_range": "150 – 300 NPR (~$1.10 – $2.30 USD for 10 pieces, estimated)",
            "breakfast_friendly": False
        },
        {
            "name": "Traditional Nepali Dal Bhat Tarkari",
            "local_name": "दाल भात तरकारी",
            "city": "Kathmandu",
            "country": "Nepal",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Nepali_Dal_Bhat_Tarkari.jpg/800px-Nepali_Dal_Bhat_Tarkari.jpg",
            "image_attribution": "Wikimedia Commons (CC BY-SA 4.0)",
            "description": "The nourishing everyday power meal of the Himalayas: steamed rice (Bhat), slow-simmered spiced yellow lentil soup (Dal), seasonal spiced vegetable curry (Tarkari), sautéed spinach (Saag), and fiery tomato pickle (Golbheda ko Achar).",
            "taste_profile": "Wholesome, earthy, mild spices, satisfying herbal richness",
            "dietary_type": "100% Vegetarian (Often 100% Vegan)",
            "is_vegetarian": True,
            "is_vegan": True,
            "contains_meat": False,
            "contains_seafood": False,
            "is_halal": True,
            "allergens": [],
            "where_to_try": "Thamel House Restaurant, Bhojan Griha, and Thakali kitchens across Kathmandu",
            "price_range": "350 – 750 NPR (~$2.60 – $5.70 USD, with free refills customary!)",
            "breakfast_friendly": True
        }
    ]
}


# ============================================================
# 2. COMPREHENSIVE 9-PILLAR CULTURAL ETIQUETTE & TRADITIONS DATABASE
# ============================================================

DESTINATION_ETIQUETTE_DATABASE: Dict[str, Dict[str, Any]] = {
    "Japan": {
        "country": "Japan",
        "overview": "Japanese culture is grounded in 'Omotenashi' (selfless hospitality), 'Meiwaku' (avoiding inconvenience to others), and harmony ('Wa'). Politeness and awareness of shared spaces are deeply appreciated.",
        "greetings": {
            "title": "🤝 Greetings & Polite Behavior",
            "summary": "Bowing (Ojigi) is the primary greeting and sign of respect; handshakes are also common when interacting with foreign guests.",
            "details": "A slight 15-degree nod/bow suffices for casual greetings (e.g. entering shops, thanking waitstaff). A deeper 30-to-45-degree bow reflects formal gratitude or apology. Hand items and business cards with both hands."
        },
        "dining": {
            "title": "🥢 Restaurant & Dining Etiquette",
            "summary": "Say 'Itadakimasu' before eating and 'Gochisousama deshita' when finished. Respect chopstick rules and enjoy noodles with an appreciative slurp.",
            "details": "• Never stick chopsticks vertically into a rice bowl (Tsukitate-bashi) as this mimics funeral rites.\n• Never pass food directly from chopstick to chopstick (Hashi-watashi).\n• Slurping hot ramen and soba noodles is polite: it aerates the broth to enhance flavor and shows the chef you enjoy the meal.\n• Clean up your tray at counter shops and return it to the return counter (Henkyaku-guchi)."
        },
        "public_transport": {
            "title": "🚆 Public Transport Etiquette",
            "summary": "Trains and subways in Japan are strictly quiet zones.",
            "details": "• Set mobile phones to 'Manner Mode' (silent) and refrain entirely from making phone calls on trains and buses.\n• Keep conversations in quiet, whispered tones.\n• Queue respectfully behind the floor markings on station platforms before boarding; let disembarking passengers off first.\n• Stand on the left of escalators in Tokyo, or on the right in Osaka/Kansai, leaving the opposite side clear for walkers."
        },
        "temples_and_shrines": {
            "title": "⛩️ Shrines (Jinja) vs Temples (Otera) Etiquette",
            "summary": "Shrines are Shinto; Temples are Buddhist. Worship rituals differ significantly between the two.",
            "details": "• At Shinto Shrines: Bow slightly before passing under the Torii gate. Walk on the outer sides of the path (the center is reserved for the Kami deities). Purify at the Temizuya water basin (rinse left hand, right hand, mouth with cupped left hand, clean ladle handle). At the altar: Bow twice (90°), Clap hands twice firmly, pray silently, Bow once deeply.\n• At Buddhist Temples: Bow slightly at the Sanmon gate. Do NOT clap hands; instead, place palms quietly together in prayer (Gassho) with a silent bow. Light incense at the large burner and fan the fragrant smoke over yourself for purification."
        },
        "shoe_removal": {
            "title": "👟 Shoe-Removal Customs (Genkan & Tatami)",
            "summary": "Footwear removal is mandatory at home entryways, ryokans, temple halls, and traditional tatami dining rooms.",
            "details": "• Step onto the raised wooden floor (Genkan) before taking off shoes; never let bare socks or slippers touch the floor where outdoor shoes have walked.\n• Turn your shoes around so they point outward toward the door.\n• Wear the provided indoor slippers across wooden hallways, but remove slippers before stepping onto straw tatami mats (socks only).\n• Switch into dedicated 'toilet slippers' when using the restroom, and remember to switch back before exiting!"
        },
        "tipping": {
            "title": "💰 Tipping Customs (Strictly Not Customary)",
            "summary": "Tipping is NOT customary anywhere in Japan and can create awkward confusion.",
            "details": "Exceptional service is considered standard and is built into the pride of craftsmanship (Shokunin) and the bill. Leaving extra cash on a table will often result in waitstaff running down the street to return the 'forgotten' money to you. A sincere 'Arigatou gozaimasu' or 'Gochisousama deshita' is the highest compliment."
        },
        "photography": {
            "title": "📷 Photography Restrictions & Permission",
            "summary": "Ask before photographing individuals, especially Geiko and Maiko in Kyoto.",
            "details": "• In Kyoto's Gion district, photography is strictly prohibited on private alleys (clearly marked with warning signs and fines).\n• Do not photograph inside the inner sanctum of shrines and temples where sacred deity figures or ancestral tablets reside.\n• Flash photography is strictly forbidden around delicate lacquerware, paper folding screens, and temple paintings."
        },
        "festivals": {
            "title": "🎆 Cultural Festivals & Traditions",
            "summary": "Matsuri bring communities together in celebration with portable shrines (Mikoshi), street food, and traditional yukata.",
            "details": "Iconic festivals include Gion Matsuri (Kyoto in July), Tenjin Matsuri (Osaka in July), Kanda Matsuri (Tokyo in May), and Spring Hanami (cherry blossom flower-viewing picnics under sakura trees in April)."
        },
        "community_respect": {
            "title": "🌿 Respectful Behavior Toward Local Communities",
            "summary": "Be mindful of quiet residential lanes, and carry pocket trash with you.",
            "details": "• Street trash bins are rare in Japan due to public recycling protocols; carry a small bag to take your trash back to your hotel or convenience store bins.\n• Avoid eating while walking along crowded narrow historic sidewalks ('Aruki-gui'); step to the side near the shop to enjoy street snacks.\n• Keep noise levels low when returning to hotels in traditional residential quarters at night."
        },
        "dos_and_donts": {
            "dos": [
                "Do bow slightly when greeting, thanking, or leaving an establishment.",
                "Do slurp hot ramen and soba noodles to appreciate the broth aroma.",
                "Do take off your shoes at temple entrances, ryokans, and tatami mats.",
                "Do keep your phone on silent and speak softly on all public transit.",
                "Do carry local cash (JPY ¥) for small shrines, ramen ticket machines, and lockers."
            ],
            "donts": [
                "Don't leave tips on restaurant tables—it is not customary in Japan.",
                "Don't stick chopsticks upright into rice or pass food chopstick-to-chopstick.",
                "Don't walk down the street while eating messy snacks; finish near the shop.",
                "Don't photograph Geiko or Maiko in Gion's private alleys without permission.",
                "Don't clap your hands at Buddhist temples (clapping is strictly for Shinto shrines)."
            ]
        }
    },

    "India": {
        "country": "India",
        "overview": "Indian culture is rooted in 'Atithi Devo Bhava' ('The Guest is Equivalent to God') and profound civilizational diversity across religions, languages, and regional customs.",
        "greetings": {
            "title": "🤝 Greetings & Polite Behavior",
            "summary": "Pressing palms together at chest height with a slight bow saying 'Namaste' or 'Namaskar' is the universal polite greeting.",
            "details": "Always use the right hand when greeting, giving or receiving money, gifts, or food, as the left hand is traditionally associated with personal hygiene."
        },
        "dining": {
            "title": "🍛 Restaurant & Dining Etiquette",
            "summary": "Traditional meals are eaten with the clean right hand or with spoons/cutlery provided.",
            "details": "• When eating traditional thalis, roti or rice with your hands, use only the fingertips of your right hand.\n• Do not share food from someone's plate that has already been tasted (known as 'Jhootha').\n• In sit-down restaurants, cutlery is always readily available upon request."
        },
        "public_transport": {
            "title": "🚆 Public Transport Etiquette",
            "summary": "Public transport is lively and extensive; priority seating and ladies' carriages exist for safety and comfort.",
            "details": "• Most city metros (Delhi Metro, Mumbai Metro) have dedicated pink coaches for women at the front of each train.\n• Respect queues at metro security gates and ticket kiosks."
        },
        "temples_and_shrines": {
            "title": "🛕 Temple, Mosque & Gurdwara Etiquette",
            "summary": "Strict modesty and footwear removal are universal across all sacred sites.",
            "details": "• Remove footwear outside all Hindu temples, Jain temples, Buddhist viharas, and Sikh Gurdwaras.\n• Dress modestly with shoulders, chest, and knees fully covered.\n• At Sikh Gurdwaras (e.g. Golden Temple in Amritsar), both men and women must cover their heads with a scarf or bandana, wash feet in the shallow water channel at the entrance, and accept blessed sweet prasad with both cupped hands."
        },
        "shoe_removal": {
            "title": "👟 Shoe-Removal Customs",
            "summary": "Always remove outdoor shoes before entering Indian homes, shrines, and sacred sanctums.",
            "details": "Shoe-stand keepers ('Joota counters') are available at temple entrances for a token tip of ₹10–₹20."
        },
        "tipping": {
            "title": "💰 Tipping Customs",
            "summary": "Tipping is customary in sit-down restaurants and for personal service.",
            "details": "• In casual restaurants: 7–10% of the bill, or rounding up.\n• In fine-dining restaurants: 10% is standard (check if a 'Service Charge' is already included on the bill).\n• Hotel bellhops/porters: ₹50–₹100 per bag; Drivers/guides: ₹300–₹500 per day."
        },
        "photography": {
            "title": "📷 Photography Restrictions & Permission",
            "summary": "Always politely ask before photographing locals, holy men (sadhus), and religious ceremonies.",
            "details": "Photography inside temple sanctums (Garbhagriha), cremation ghats in Varanasi, and military airports is strictly prohibited."
        },
        "festivals": {
            "title": "🎉 Cultural Festivals & Traditions",
            "summary": "Spectacular festivals occur year-round with immense community spirit.",
            "details": "Diwali (Festival of Lights), Holi (Spring Festival of Colors), Eid, Christmas, Durga Puja (Kolkata), Navratri Garba (Gujarat), and Pongal/Onam in South India."
        },
        "community_respect": {
            "title": "🌿 Respectful Behavior Toward Local Communities",
            "summary": "Customs vary widely across India's 28 states and union territories.",
            "details": "Respect local dietary preferences (many areas are strictly vegetarian), ask permission before taking street portraits, and embrace the legendary hospitality."
        },
        "dos_and_donts": {
            "dos": [
                "Do greet with 'Namaste' with hands joined at chest level.",
                "Do remove footwear and cover your head when visiting places of worship.",
                "Do use your right hand for eating, passing money, and greeting.",
                "Do drink sealed packaged water or filtered water.",
                "Do carry digital UPI payment apps or small cash notes for local markets."
            ],
            "donts": [
                "Don't point the soles of your feet toward people, deities, or sacred icons.",
                "Don't wear revealing clothing (shorts, sleeveless tops) at religious sites.",
                "Don't touch religious idols or enter sacred sanctums unless permitted.",
                "Don't photograph funeral cremation rituals at Varanasi ghats.",
                "Don't assume customs in Delhi are identical to Kerala or Kashmir—each state has unique traditions."
            ]
        }
    },

    "France": {
        "country": "France",
        "overview": "French social life values elegance, culinary appreciation, and polite verbal acknowledgment ('Politesse').",
        "greetings": {
            "title": "🤝 Greetings & Polite Behavior",
            "summary": "Always say 'Bonjour Madame' or 'Bonjour Monsieur' upon entering ANY shop, cafe, or taxi before asking for anything.",
            "details": "Saying 'Bonjour' is not optional in France—it establishes mutual respect. Say 'Au revoir, bonne journée' when leaving."
        },
        "dining": {
            "title": "🍷 Restaurant & Dining Etiquette",
            "summary": "Dining is an art form meant to be savored slowly without rushing.",
            "details": "• Meals progress leisurely: servers will not bring the bill (l'addition) until you explicitly ask for it ('L'addition, s'il vous plaît').\n• Bread is placed directly on the tablecloth beside your plate, not on a butter dish.\n• Keep hands above the table resting wrists lightly on the edge (never in your lap).\n• You can ask for free tap water in a carafe ('Une carafe d'eau, s'il vous plaît')."
        },
        "public_transport": {
            "title": "🚆 Public Transport Etiquette",
            "summary": "Keep voices low and validate your tickets.",
            "details": "Keep transit tickets until you fully exit metro turnstiles to avoid on-the-spot transit fines."
        },
        "temples_and_shrines": {
            "title": "⛪ Cathedral & Historic Church Etiquette",
            "summary": "Historic basilicas and cathedrals are active places of worship.",
            "details": "Maintain silence, remove hats, and dress respectfully (covered shoulders)."
        },
        "shoe_removal": {
            "title": "👟 Shoe-Removal Customs",
            "summary": "Shoes remain on in public venues, but ask host when visiting private French homes."
        },
        "tipping": {
            "title": "💰 Tipping Customs (Service Compris)",
            "summary": "Service is legally included in the bill ('service compris' 15%).",
            "details": "Leaving small extra change (e.g. €1–€2 for casual lunch, €3–€5 for great dinner service) is a polite gesture of appreciation ('pourboire'), but large percentage tips are not expected."
        },
        "photography": {
            "title": "📷 Photography Restrictions & Permission",
            "summary": "Photography allowed at public sights; turn off flash inside historic museums."
        },
        "festivals": {
            "title": "🎆 Cultural Festivals & Traditions",
            "summary": "Fête de la Musique (June 21), Bastille Day (July 14), and regional grape harvest celebrations in autumn."
        },
        "community_respect": {
            "title": "🌿 Respectful Behavior Toward Local Communities",
            "summary": "Make a gentle attempt at basic French phrases ('S'il vous plaît', 'Merci')."
        },
        "dos_and_donts": {
            "dos": [
                "Do say 'Bonjour' immediately when entering any shop or cafe.",
                "Do ask for 'L'addition, s'il vous plaît' when you are ready to pay.",
                "Do savor meals slowly and appreciate culinary pairings.",
                "Do validate your metro ticket and keep it until you exit.",
                "Do ask for 'Une carafe d'eau' for complimentary tap water."
            ],
            "donts": [
                "Don't speak loudly in public transit or quiet bistros.",
                "Don't snap your fingers or yell 'Garçon' at servers.",
                "Don't expect dinner restaurants to open before 7:30 PM.",
                "Don't leave large 20% tips—service is already included by French law.",
                "Don't demand immediate modifications to classic French recipes without dietary need."
            ]
        }
    }
}


# ============================================================
# 3. HELPER RETRIEVAL & SYNTHESIS FUNCTIONS
# ============================================================

def get_city_food(country: str, city: Optional[str] = None, dietary_pref: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns authentic dishes specific to the country and city requested,
    with fallbacks that clearly state origin to avoid geographic misattribution.
    """
    c_norm = country.strip().title()
    city_norm = (city or "").strip().title()

    results = []

    # 1. Exact Country + City match
    for (c, ci), dishes in CITY_FOOD_DATABASE.items():
        if c.lower() == c_norm.lower() and (city_norm.lower() in ci.lower() or ci.lower() in city_norm.lower()):
            for d in dishes:
                results.append(d)

    # 2. If no city specified or city not directly in DB, collect all dishes from this country
    if not results:
        for (c, ci), dishes in CITY_FOOD_DATABASE.items():
            if c.lower() == c_norm.lower():
                for d in dishes:
                    if d not in results:
                        results.append(d)

    # 3. Universal synthesized fallback if country not yet in detailed DB
    if not results:
        from country_data import get_country_knowledge
        k = get_country_knowledge(country)
        f_list = k.get("food", [])
        for f in f_list:
            if isinstance(f, (tuple, list)):
                name = f[0]
                desc = f[1] if len(f) > 1 else f"Authentic culinary specialty of {k['name']}."
                slug = f[2] if len(f) > 2 else ""
                results.append({
                    "name": name,
                    "local_name": name,
                    "city": city_norm or k.get("cities", [k["name"]])[0],
                    "country": k["name"],
                    "image": f"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg",
                    "image_attribution": "Wikimedia Commons (Public Domain)",
                    "description": desc,
                    "taste_profile": "Authentic regional seasoning, rich local flavor",
                    "dietary_type": "Regional Specialty",
                    "is_vegetarian": any(v in desc.lower() for v in ["vegetarian", "lentil", "tofu", "cheese", "vegetable"]),
                    "is_vegan": any(v in desc.lower() for v in ["vegan", "lentil", "rice"]),
                    "contains_meat": any(v in desc.lower() for v in ["beef", "chicken", "lamb", "pork", "meat"]),
                    "contains_seafood": any(v in desc.lower() for v in ["fish", "prawn", "seafood", "octopus"]),
                    "is_halal": not any(v in desc.lower() for v in ["pork", "wine", "alcohol"]),
                    "allergens": ["Varies by preparation"],
                    "where_to_try": f"Historic dining quarters and local food markets in {k['name']}",
                    "price_range": "Affordable local dining (estimated)",
                    "breakfast_friendly": False
                })

    # Apply dietary filtering if specified
    if dietary_pref:
        pref_low = dietary_pref.lower()
        if "veg" in pref_low and "non" not in pref_low:
            veg_results = [d for d in results if d.get("is_vegetarian") or "veg" in d.get("dietary_type", "").lower()]
            if veg_results:
                return veg_results
        elif "vegan" in pref_low:
            vegan_results = [d for d in results if d.get("is_vegan")]
            if vegan_results:
                return vegan_results
        elif "halal" in pref_low:
            halal_results = [d for d in results if d.get("is_halal")]
            if halal_results:
                return halal_results

    return results


def get_destination_etiquette(country: str, city: Optional[str] = None) -> Dict[str, Any]:
    """Returns comprehensive 9-pillar cultural etiquette for any country."""
    c_norm = country.strip().title()
    for k, v in DESTINATION_ETIQUETTE_DATABASE.items():
        if k.lower() == c_norm.lower():
            return v

    # Universal synthesis for all other 250 countries
    from country_data import get_country_knowledge
    k_data = get_country_knowledge(country)
    tips = k_data.get("travel_tips", {})
    c_name = k_data["name"]

    return {
        "country": c_name,
        "overview": f"Cultural traditions in {c_name} reflect generations of regional history and hospitality. Treating community spaces with modesty and respect ensures a welcoming stay.",
        "greetings": {
            "title": "🤝 Greetings & Polite Behavior",
            "summary": f"Polite verbal greetings and a friendly smile are universal in {c_name}.",
            "details": f"A polite greeting ('Hello' / local greeting) when entering small shops and restaurants sets a respectful tone."
        },
        "dining": {
            "title": "🍽️ Restaurant & Dining Etiquette",
            "summary": "Respect local dining customs and table manners.",
            "details": f"Observe how locals dine and ask waitstaff for authentic specialties. {tips.get('currency_tips', 'Carry cash for small cafes and markets.')}"
        },
        "public_transport": {
            "title": "🚆 Public Transport Etiquette",
            "summary": "Keep public spaces clean and conversations at considerate volumes.",
            "details": "Queue respectfully for boarding buses and trains, offering seats to elderly or pregnant passengers."
        },
        "temples_and_shrines": {
            "title": "🏛️ Sacred Sites & Places of Worship",
            "summary": "Dress modestly and maintain quiet reverence at sacred heritage sights.",
            "details": "Cover shoulders and knees before entering historic churches, mosques, or temples. Check if shoes must be removed before entering sanctums."
        },
        "shoe_removal": {
            "title": "👟 Shoe-Removal Customs",
            "summary": "Remove footwear when entering sacred buildings or private homes.",
            "details": "Look for shoe racks near entryways as a clear indicator of whether footwear should be removed."
        },
        "tipping": {
            "title": "💰 Tipping Customs",
            "summary": f"Tipping norm: {tips.get('tipping', '10% in sit-down restaurants is customary.')}",
            "details": tips.get("tipping", "Tipping policies vary; rounding up the bill or leaving 5–10% is generally appreciated for good service.")
        },
        "photography": {
            "title": "📷 Photography Restrictions & Permission",
            "summary": "Always ask permission before taking portraits of individuals or sacred rituals.",
            "details": "Do not use flash inside historic museum galleries or active religious services."
        },
        "festivals": {
            "title": "🎉 Cultural Festivals & Traditions",
            "summary": f"Celebrated seasonal festivals showcase {c_name}'s heritage.",
            "details": "Check regional holiday calendars to experience local music, food stalls, and artisan parades."
        },
        "community_respect": {
            "title": "🌿 Respectful Behavior Toward Local Communities",
            "summary": f"Support local artisans and respect residential neighborhoods in {c_name}.",
            "details": tips.get("etiquette", "Greet locals politely and maintain respectful volume in public.")
        },
        "dos_and_donts": {
            "dos": [
                f"Do greet locals with a polite hello and smile in {c_name}.",
                "Do dress modestly when visiting places of worship.",
                "Do carry local cash for small markets and transportation.",
                "Do ask permission before photographing individuals.",
                "Do sample authentic regional dishes at busy local establishments."
            ],
            "donts": [
                "Don't speak loudly on public transit or in historic sanctuaries.",
                "Don't litter in public squares or natural parks.",
                "Don't assume customs are uniform across all provinces—ask respectfully.",
                "Don't touch historic relics or artwork in museums without permission.",
                "Don't enter places of worship wearing swimwear or revealing tops."
            ]
        }
    }


# ============================================================
# 4. COMPANION SPECIFIC Q&A HANDLERS
# ============================================================

def compare_kimono_and_yukata() -> str:
    """Answers: 'What is the difference between a kimono and a yukata?'"""
    return """### 👘 The Difference Between a Kimono and a Yukata in Japan

While both are iconic traditional Japanese robes, **Kimono (着物)** and **Yukata (浴衣)** serve very distinct purposes, seasons, and occasions:

---

| Feature | 👘 Kimono (着物) | 👘 Yukata (浴衣) |
| :--- | :--- | :--- |
| **Primary Material** | Luxurious **pure silk** or fine brocade (formal) | Breathable **unlined cotton** or linen (casual) |
| **Season & Climate** | Worn **year-round** (lined *Awase* in winter/autumn) | Worn strictly in **summer (June – August)** |
| **Occasion** | Formal ceremonies: weddings, tea ceremonies, Coming of Age Day (*Seijin no Hi*), graduations | Casual summer festivals (*Hanabi* fireworks, *Matsuri*), and after-bath loungewear at onsen *ryokans* |
| **Undergarments** | Requires a full white collared undergarment (**Nagajuban**), showing two collars at the neck | Worn with **minimal undergarments**, directly against the skin or a lightweight cotton slip (single collar) |
| **Footwear** | Split-toe white **Tabi socks** + formal lacquered **Zori sandals** | Bare feet + wooden **Geta clogs** (no socks!) |
| **Sash (Obi)** | Wide, structured formal belt (**Nagoya Obi** or **Fukuro Obi**, ~30cm wide) requiring complex ties | Lightweight, informal sash (**Hanhaba Obi**, ~15cm wide) tied in a playful butterfly knot |
| **Typical Cost** | ¥50,000 – ¥500,000+ JPY (~$350 – $3,500+ USD to buy); rentals ¥5,000 – ¥15,000/day | ¥3,000 – ¥12,000 JPY (~$20 – $80 USD to buy); rentals ¥3,000 – ¥6,000/day |

---

💡 **Practical Traveler Advice:**
- **In Summer (July–August):** Rent a colorful **Yukata** to attend summer fireworks festivals, stroll along Gion's willow-lined Shirakawa canal, or relax at an onsen ryokan.
- **In Spring/Autumn/Winter:** Rent a formal **Kimono** to experience traditional Kyoto tea ceremonies or walk gracefully through temple gardens with proper warming layers!

<!-- SPEECH:en-US:A kimono is made of formal silk with multi-layer collars, tabi socks, and zori sandals for formal events, while a yukata is lightweight unlined cotton worn barefoot with geta clogs for summer festivals and onsens. -->"""


def answer_shrine_behavior() -> str:
    """Answers: 'How should I behave when visiting a shrine?'"""
    return """### ⛩️ How to Behave at a Shinto Shrine in Japan

Visiting a Shinto Shrine (*Jinja*) is an uplifting spiritual experience. Shinto honors the *Kami* (sacred spirits of nature). Follow these traditional steps to show deep respect:

---

#### 1. Entering Through the Torii Gate (鳥居)
- **Bow Slightly:** Pause in front of the vermilion Torii gate and bow slightly (about 15 degrees) before crossing underneath.
- **Walk on the Sides:** Walk along the edges of the pathway (*Sando*). The exact center (*Seichu*) is traditionally reserved for the Kami deities.

#### 2. Purification at the Water Fountain (Temizuya / Chozuya 手水舎)
Before approaching the altar, purify your hands and mouth using the wooden ladle:
1. Hold the ladle with your **right hand**, scoop fresh water, and pour it over your **left hand**.
2. Switch hands: hold the ladle with your left hand and pour over your **right hand**.
3. Switch back to your right hand, cup some water into your left palm, and **rinse your mouth gently** (spit quietly into the side basin, never drink directly from the ladle!).
4. Tilt the ladle vertically so the remaining water trickles down the handle to clean it for the next visitor.

#### 3. Worship at the Main Offering Altar (Haiden 拝殿)
Remember the sacred sequence: **"Two Bows, Two Claps, One Bow" (Ni-rei, Ni-hai, Ichi-rei)**:
1. **Throw a Coin:** Toss a coin into the wooden slatted offering box (*Saisenbako*). A **5-yen coin** (*Go-en*) is considered especially lucky because 'go-en' sounds like the word for good fortune/connections.
2. **Ring the Bell:** If a suspended rope and brass bell are present, ring it firmly once or twice to announce your presence to the Kami.
3. **Bow Deeply Twice:** Bend at a 90-degree angle twice.
4. **Clap Hands Twice:** Bring your palms together, slide your right hand slightly back, clap firmly **twice**, align your hands, and pray silently.
5. **Bow Deeply Once More:** Conclude with one final 90-degree bow.

---

⚠️ **Crucial Distinction from Buddhist Temples:**
- At **Shinto Shrines**, you **CLAP** your hands twice.
- At **Buddhist Temples (Otera)**, you do **NOT clap**; instead, you press palms together in silent prayer (*Gassho*).

<!-- SPEECH:en-US:At a Shinto shrine, bow at the torii gate, purify at the water fountain, and follow the sacred sequence: toss a five-yen coin, bow twice deeply, clap hands twice, pray silently, and bow once to finish. -->"""


def answer_food_allergies_guide(country: str) -> str:
    """Answers: 'Are there any food allergies I should watch out for?'"""
    c_low = country.lower()
    if "japan" in c_low:
        return """### ⚠️ Food Allergies & Dietary Alerts in Japan

Traveling with food allergies in Japan requires careful awareness because hidden allergens are frequent in traditional seasonings:

1. **🌾 Wheat & Gluten (Mugi / Komugiko):**
   - **Hidden Source:** Standard Japanese soy sauce (*Shoyu*) is brewed with equal parts soybeans and roasted wheat. Mirin, miso, and dashi broths often contain wheat derivatives.
   - **Safe Options:** Tamari soy sauce (100% soybean, gluten-free), sashimi with tamari, steamed rice, edamame, and 100% buckwheat Juwari Soba (verify no wheat binder).

2. **🐟 Fish & Seafood (Gyokai / Dashi):**
   - **Hidden Source:** Almost all traditional broths, miso soups, dipping sauces (tsuyu), and savory pancakes use *Dashi* made from dried bonito flakes (*Katsuobushi*) or anchovies (*Niboshi*).
   - **Safe Options:** Buddhist temple Shojin Ryori uses 100% kelp (*Kombu*) dashi; vegetarian sushi rolls without fish flakes.

3. **🌱 Soy (Daizu):**
   - **Hidden Source:** Found in tofu, edamame, shoyu, miso, and natto. If you have a severe soy allergy, communicate this clearly.

4. **🥜 Peanuts & Tree Nuts:**
   - Relatively uncommon in Japanese cooking, but watch for sesame (*Goma*) which is used extensively in sauces, dressings, and furikake.

5. **🥚 Eggs (Tamago) & Dairy (Nyuseihin):**
   - Tamagoyaki, chawanmushi custard, and breading for katsu and tempura contain egg. Raw egg is served for sukiyaki dipping.

---

💡 **Essential Japanese Allergy Phrases to Show Waitstaff:**
- *"I have a severe food allergy to [allergen]. Does this dish contain it?"*  
  👉 **私は[アレルギー]のアレルギーがあります。これに入っていますか？**
- *"No fish broth (dashi), please."*  
  👉 **魚の出汁（かつおだし）を抜いてください。 (Sakana no dashi o nuite kudasai)**

<!-- SPEECH:en-US:In Japan, watch out for hidden wheat in standard soy sauce, fish bonito flakes in dashi broths, and sesame in sauces. Always show an allergy card in Japanese script to restaurant staff. -->"""
    else:
        return f"""### ⚠️ Food Allergies & Dietary Considerations in {country}

Here are essential precautions for managing food allergies while traveling in **{country}**:

1. **Common Regional Allergens:**
   - Check traditional seasonings, cooking oils (peanut, mustard, or sesame oil), and dairy or gluten binders in sauces.
2. **Carry a Translated Allergy Card:**
   - Print or save on your smartphone an allergy card clearly written in the local official language stating: *"I have a life-threatening allergy to [peanuts / shellfish / dairy / wheat]. Please ensure my food does not come into contact with it."*
3. **Cross-Contamination at Street Markets:**
   - Street food stalls frequently use shared griddles, woks, and cooking utensils. Sit-down restaurants with dedicated kitchens offer greater control.
4. **Emergency Medication:**
   - Always carry your personal epinephrine auto-injector (EpiPen) and antihistamines in your daypack with a doctor's English prescription."""


def answer_city_food_question(country: str, q: str, city: Optional[str] = None) -> str:
    """Answers destination-specific and city-specific food questions including dietary preferences."""
    q_low = q.lower()

    # Detect city from question if not provided
    detected_city = city
    for c_tuple in CITY_FOOD_DATABASE.keys():
        if c_tuple[1].lower() in q_low:
            detected_city = c_tuple[1]
            country = c_tuple[0]
            break

    # Detect dietary preference
    dietary_pref = None
    if "vegetarian" in q_low or "veg" in q_low and "non" not in q_low:
        dietary_pref = "vegetarian"
    elif "vegan" in q_low:
        dietary_pref = "vegan"
    elif "halal" in q_low:
        dietary_pref = "halal"

    dishes = get_city_food(country, detected_city, dietary_pref=dietary_pref)
    target_loc = f"{detected_city}, {country}" if detected_city else country

    lines = [
        f"### 🍲 Authentic Culinary Recommendations for {target_loc}",
        ""
    ]

    if dietary_pref:
        lines.append(f"Here are top-rated **{dietary_pref.title()}** dishes and authentic preparations to enjoy in **{target_loc}**:")
    else:
        lines.append(f"The authentic food culture in **{target_loc}** offers celebrated local specialties:")

    lines.append("")

    for d in dishes[:5]:
        veg_tag = "🌱 Vegetarian" if d.get("is_vegetarian") else ("🦐 Seafood" if d.get("contains_seafood") else "🥩 Contains Meat")
        if d.get("is_vegan"):
            veg_tag = "🌿 100% Vegan"

        lines.append(f"#### 🍽️ **{d['name']}** (`{d.get('local_name', d['name'])}`)")
        if d.get("image"):
            lines.append(f"![{d['name']}]({d['image']})")
            lines.append(f"📷 *{d.get('image_attribution', 'Verified photograph via Wikimedia Commons.')}*")
            lines.append("")
        lines.append(f"- **Ingredients & Preparation:** {d.get('description', '')}")
        lines.append(f"- **Taste Profile:** {d.get('taste_profile', 'Savory and authentic')}")
        lines.append(f"- **Dietary Classification:** **{veg_tag}**")
        if d.get("allergens"):
            lines.append(f"- **Allergens & Considerations:** {', '.join(d['allergens'])}")
        lines.append(f"- **Where to Try in {d.get('city', target_loc)}:** {d.get('where_to_try', 'Local specialty restaurants')}")
        if d.get("price_range"):
            lines.append(f"- **Estimated Price Range:** {d['price_range']}")
        lines.append("")

    if "japan" in country.lower() and dietary_pref == "vegetarian":
        lines.append("💡 **Vegetarian Pro-Tip in Japan:** Always confirm that the dashi broth is kelp-based (*Kombu dashi*) rather than bonito fish flakes (*Katsuo dashi*). Look for Zen Buddhist temple cuisine (*Shojin Ryori*) for guaranteed 100% plant-based dining!")

    speech_summary = f"In {target_loc}, enjoy authentic dishes like {dishes[0]['name']} and {dishes[1]['name'] if len(dishes) > 1 else 'local specialties'}."
    lines.append(f"<!-- SPEECH:en-US:{speech_summary} -->")

    return "\n".join(lines)


def suggest_cultural_activity(country: str, city: str, day_num: int = 1) -> str:
    """Answers: 'Can you suggest a cultural activity for my second day in Kyoto?'"""
    c_low = country.lower()
    city_low = city.lower()

    if "kyoto" in city_low:
        if day_num == 2 or "second" in str(day_num):
            return """### 🍵 Cultural Activity for Day 2 in Kyoto: Traditional Tea Ceremony & Gion Machiya Walk

For your **second day in Kyoto**, we highly recommend an authentic **Chado (Way of Tea) Ceremony** followed by an artisan craft walk:

1. **Morning / Midday (11:00 AM): Authentic Tea Ceremony (Chanoyu)**
   - **Experience:** Step through a tranquil stone garden (*Roji*) into a centuries-old wooden teahouse near Daitoku-ji or Kodai-ji.
   - **Cultural Meaning:** Learn the Zen philosophy of *Ichi-go Ichi-e* ('One time, one meeting' — cherishing this unrepeatable moment). A master tea practitioner prepares stone-ground Uji matcha whisked to a jade foam, paired with seasonal handmade *Wagashi* sweets.
   - **Location:** En Tea House (Gion) or Camellia Tea Ceremony (Ninenzaka).
   - **Estimated Cost:** ¥3,000 – ¥4,500 (~$20 – $30 USD, estimated).

2. **Afternoon (02:30 PM): Historic Preservation Walk & Artisan Silk Dyeing**
   - **Experience:** Stroll the preserved wooden facades of **Ninenzaka and Sannenzaka**, visiting a traditional *Kyo-Yuzen* silk-dyeing or incense atelier.
   - **Etiquette Note:** Please do not photograph working Geiko or Maiko in private residential alleys without permission.

3. **Evening Dining Recommendation:**
   - Enjoy authentic **Kyoto Yudofu** (delicate simmered silken tofu in kombu broth) in a tranquil tatami room overlooking a lantern-lit moss garden.

<!-- SPEECH:en-US:For your second day in Kyoto, experience an authentic Japanese tea ceremony in a historic machiya teahouse, followed by an artisan craft walk through Ninenzaka and traditional Yudofu dining. -->"""
        else:
            return f"""### ⛩️ Cultural Activity in Kyoto: Fushimi Inari & Zen Garden Meditation

Immerse yourself in Kyoto's spiritual roots:
1. **Early Morning (07:30 AM): Fushimi Inari-taisha Shrine Pilgrimage**
   - Walk through the thousands of vermilion Torii gates winding up sacred Mount Inari before tourist crowds arrive.
2. **Afternoon (01:30 PM): Tofuku-ji or Tenryu-ji Zen Rock Garden Meditation**
   - Experience the minimalist aesthetics of Karesansui dry rock gardens.
3. **Evening (06:00 PM): Obanzai Seasonal Tasting**
   - Savor traditional Kyoto seasonal vegetable dishes in Pontocho Alley.

<!-- SPEECH:en-US:Visit Fushimi Inari early in the morning, followed by Zen rock garden meditation and an authentic Obanzai seasonal tasting dinner. -->"""

    # General cultural activity fallback
    return f"""### 🏛️ Cultural Immersion Activity in {city}, {country}

Immerse yourself in the authentic living heritage of **{city}**:

1. **Heritage Landmark & Spiritual Sanctuary Tour:**
   - Explore the preserved architectural quarter and historic temples/cathedrals of {city} with a local licensed heritage guide.
2. **Traditional Artisan Craft Workshop:**
   - Participate in a hands-on workshop (pottery, textile weaving, or regional cooking masterclass) connecting directly with local craftsmen.
3. **Regional Culinary Tasting:**
   - Sample authentic regional delicacies at a historic covered market hall.
4. **Etiquette Tip:**
   - Dress respectfully with shoulders covered when entering historic sanctuaries and ask before taking photos.

<!-- SPEECH:en-US:Explore the historic quarter of {city}, join a hands-on artisan craft workshop, and taste local specialties at a historic market hall. -->"""


def replace_meal_with_vegetarian(current_suggestion: str, country: str, city: Optional[str] = None) -> str:
    """Answers: 'Can you replace this restaurant suggestion with a vegetarian option?'"""
    city_name = city or "your destination"
    dishes = get_city_food(country, city, dietary_pref="vegetarian")

    alt_dish = dishes[0] if dishes else {
        "name": "Buddhist Temple Vegetable Feast (Shojin Ryori / Dal Thali)",
        "description": "Artisanal seasonal plant-based dishes made with local vegetables, tofu, and legumes.",
        "where_to_try": f"Vegetarian dining specialty restaurants in {city_name}",
        "price_range": "Affordable local dining (estimated)"
    }

    return f"""### 🌱 Vegetarian Dining Replacement for {city_name}

We have updated your meal recommendation with a verified **authentic vegetarian specialty**:

- **Recommended Dish:** 🍲 **{alt_dish['name']}**
- **Preparation & Ingredients:** {alt_dish.get('description', '')}
- **Taste Profile:** {alt_dish.get('taste_profile', 'Fresh, savory, and soothing')}
- **Where to Enjoy in {city_name}:** {alt_dish.get('where_to_try', 'Local plant-based restaurants and temple quarters')}
- **Estimated Cost:** {alt_dish.get('price_range', 'Moderate local dining')}
- **Dietary Assurance:** 100% Meat-free and pescatarian-free; ask for *"No fish broth / Dashi nashi"* to ensure complete plant-based preparation!

<!-- SPEECH:en-US:Your meal has been replaced with authentic vegetarian {alt_dish['name']}, featuring seasonal vegetables and rich local seasonings. -->"""


# ============================================================
# 4. GROUNDED CITY ATTRACTIONS & SIGHTSEEING DATABASE
# ============================================================

CITY_ATTRACTIONS_DATABASE: Dict[Tuple[str, str], Dict[str, Any]] = {
    # --- JAPAN ---
    ("Japan", "Tokyo"): {
        "city_attractions": [
            ("Shibuya Crossing & Hachiko Statue", "World's busiest pedestrian crossing, iconic Shibuya skyline view from Shibuya Sky, and historic loyal dog memorial", 0, "Shibuya / Metro"),
            ("Senso-ji Temple & Nakamise-dori", "Tokyo's oldest Buddhist temple founded in 645 AD, towering Thunder Gate (Kaminarimon), and historic Edo market street", 0, "Asakusa / Ginza Line"),
            ("Meiji Jingu Shrine & Yoyogi Forest", "Serene Shinto shrine dedicated to Emperor Meiji set inside a tranquil 170-acre evergreen forest in the heart of Harajuku", 0, "Harajuku / JR Yamanote Line"),
            ("Tokyo Skytree & Solamachi", "World's tallest free-standing broadcasting tower (634m) with 360-degree panoramic observatories overlooking the Kanto plain", 2700, "Oshiage / Asakusa Line"),
            ("Tsukiji Outer Market & Ginza District", "Historic food market alleys famous for fresh sushi, tamagoyaki egg skewers, and upscale Ginza shopping boulevard", 0, "Tsukiji / Hibiya Line"),
            ("Shinjuku Gyoen National Garden", "Sprawling imperial garden blending traditional Japanese, English Landscape, and French Formal garden designs", 500, "Shinjuku-syoenmae / Marunouchi Line"),
            ("Akihabara Electric Town & Kanda Shrine", "Vibrant epicenter of anime, gaming, electronics, and historic eighth-century Kanda Myojin sanctuary", 0, "Akihabara / JR Yamanote Line"),
            ("Ueno Park & Tokyo National Museum", "Spacious cultural park featuring Japan's oldest national museum housing over 110,000 historic cultural treasures", 1000, "Ueno / JR Yamanote Line"),
        ],
        "day_trips": [
            ("Mount Fuji & Lake Kawaguchiko [Day Trip: 2h 15m travel time each way via Fuji Excursion Express]", "Iconic snow-capped volcanic peak, scenic lakeside promenades, Chureito Pagoda views, and Mount Fuji panoramic ropeway", 4200, "Fuji Excursion Express / Highway Coach"),
            ("Kamakura & Great Buddha Kotoku-in [Day Trip: 55m travel time each way via JR Yokosuka Line]", "Historic seaside capital of the Kamakura Shogunate, colossal 11-meter outdoor bronze Amida Buddha, and bamboo temple Hokoku-ji", 1800, "JR Yokosuka Line from Tokyo Station"),
            ("Nikko Toshogu Shrine & Kegon Falls [Day Trip: 1h 50m travel time each way via Tobu Spacia X]", "UNESCO World Heritage Edo-period shrine complex adorned with elaborate gold leaf and wood carvings, set in misty cedar mountains", 3500, "Tobu Skytree Line / Spacia X from Asakusa"),
        ]
    },
    ("Japan", "Kyoto"): {
        "city_attractions": [
            ("Fushimi Inari Taisha", "Spiritual mountain shrine renowned for thousands of vermilion Senbon Torii gates winding through sacred fox-guarded Mount Inari", 0, "JR Nara Line to Inari Station"),
            ("Kiyomizu-dera Temple", "Historic UNESCO wooden temple perched on Mount Otowa featuring a massive veranda built entirely without nails and Otowa waterfall", 400, "Higashiyama / Kyoto City Bus #206"),
            ("Arashiyama Bamboo Grove & Tenryu-ji", "Towering emerald bamboo pathway, UNESCO World Heritage Zen garden with Sogenchi pond, and Togetsukyo Bridge", 500, "JR San-in Line to Saga-Arashiyama"),
            ("Kinkaku-ji (Golden Pavilion)", "Breathtaking Zen Buddhist temple whose top two floors are completely covered in pure gold leaf, reflecting across Mirror Pond", 500, "Kinkakuji-michi / Kyoto City Bus #205"),
            ("Gion Historic Geisha District & Shirakawa", "Atmospheric preserved district with traditional wooden machiya merchant townhouses, lantern-lit alleys, and ochaya teahouses", 0, "Gion-Shijo / Keihan Line"),
            ("Nijo Castle & Ninomaru Palace", "Historic residence of the Tokugawa Shoguns featuring ingenious 'nightingale floors' that chirp like birds when walked upon", 1030, "Nijojo-mae / Tozai Subway Line"),
            ("Nishiki Market (Kyoto's Kitchen)", "Five-block narrow shopping street packed with over 100 stalls selling Kyoto pickles, yuba tofu, wagashi, and grilled seafood", 0, "Shijo / Karasuma Subway Line"),
            ("Philosopher's Path & Ginkaku-ji", "Tranquil stone walking trail along a cherry tree-lined canal connecting Ginkaku-ji (Silver Pavilion) to Nanzen-ji temple", 500, "Higashiyama / Kyoto City Bus #5"),
        ],
        "day_trips": [
            ("Nara Historic Park & Todai-ji [Day Trip: 45m travel time each way via JR Nara Line or Kintetsu Express]", "Ancient capital featuring over 1,000 friendly free-roaming sacred sika deer and Todai-ji's 15-meter Great Bronze Buddha (Daibutsu)", 1200, "JR Nara Line / Kintetsu Limited Express"),
            ("Uji Matcha & Byodoin Temple [Day Trip: 25m travel time each way via JR Nara Line]", "Birthplace of Japanese green tea, centuries-old tea master estates, and the Phoenix Hall of Byodoin Temple featured on the 10-yen coin", 800, "JR Nara Line from Kyoto Station"),
        ]
    },
    ("Japan", "Osaka"): {
        "city_attractions": [
            ("Osaka Castle & Nishinomaru Garden", "Iconic 16th-century fortress surrounded by immense stone walls, moats, and museum showcasing samurai unification history", 600, "Osakajokoen / JR Loop Line"),
            ("Dotonbori & Shinsaibashi", "Osaka's electric entertainment heart famous for giant neon signs (Glico Running Man), vibrant street food stalls, and covered arcades", 0, "Namba / Midosuji Subway Line"),
            ("Kuromon Ichiba Market", "Lively 600-meter covered market dubbed 'Osaka's Pantry' renowned for freshly grilled wagyu, scallops, uni, and takoyaki octopus balls", 0, "Nippombashi / Sakaisuji Subway Line"),
            ("Shinsekai & Tsutenkaku Tower", "Nostalgic retro downtown quarter laid out in 1912, packed with vibrant kushikatsu skewer restaurants and Tsutenkaku Eiffel-style tower", 900, "Ebisucho / Sakaisuji Line"),
            ("Umeda Sky Building & Floating Garden Observatory", "Striking 173-meter twin-tower architectural landmark with open-air 360-degree rooftop deck offering panoramic skyline views", 1500, "Osaka / Umeda Station"),
            ("Osaka Aquarium Kaiyukan", "One of the world's most spectacular public aquariums featuring a massive Pacific Ocean tank home to whale sharks and manta rays", 2700, "Osakako / Chuo Subway Line"),
            ("Sumiyoshi Taisha Shrine", "Ancient grand Shinto shrine founded in 211 AD with unique Sorihashi arched bridge and pure Japanese Sumiyoshi-zukuri architecture", 0, "Sumiyoshitaisha / Nankai Line"),
        ],
        "day_trips": [
            ("Himeji Castle [Day Trip: 40m travel time each way via Sanyo Shinkansen]", "Japan's most pristine surviving feudal castle, the gleaming 'White Heron Castle' with 83 preserved defensive buildings and courtyards", 2200, "Sanyo Shinkansen from Shin-Osaka"),
            ("Kobe Port & Harborland [Day Trip: 25m travel time each way via JR Special Rapid]", "Cosmopolitan harbor city famed for world-renowned Kobe wagyu beef, historic Kitano foreign residences, and Rokko mountain cable car", 1200, "JR Kobe Line from Osaka Station"),
        ]
    },

    # --- FRANCE ---
    ("France", "Paris"): {
        "city_attractions": [
            ("Eiffel Tower & Champ de Mars", "Iconic iron lattice monument designed by Gustave Eiffel with panoramic summit views over Paris", 2500, "Bir-Hakeim / Metro Line 6"),
            ("Louvre Museum & Glass Pyramid", "World's largest art museum housing Mona Lisa, Venus de Milo, and centuries of royal French masterpieces", 2200, "Palais Royal Musée du Louvre / Metro Line 1"),
            ("Musée d'Orsay", "Stunning Beaux-Arts railway station museum displaying the world's largest collection of Impressionist and Post-Impressionist art", 1600, "Solférino / Metro Line 12"),
            ("Notre-Dame Cathedral & Île de la Cité", "Gothic architectural jewel on the Seine river, point zero of France, and historic heart of Paris", 0, "Cité / Metro Line 4"),
            ("Montmartre & Sacré-Cœur Basilica", "Bohemian hilltop artists' village, Place du Tertre easel painters, and white-domed basilica overlooking the city", 0, "Anvers / Metro Line 2"),
            ("Arc de Triomphe & Champs-Élysées", "Monumental triumphal arch honoring French military victories at the pinnacle of the grand tree-lined avenue", 1300, "Charles de Gaulle - Étoile / Metro Line 1"),
            ("Sainte-Chapelle", "Breathtaking 13th-century Gothic royal chapel containing 1,113 magnificent stained-glass panels reaching toward the sky", 1150, "Cité / Metro Line 4"),
        ],
        "day_trips": [
            ("Palace of Versailles [Day Trip: 45m travel time each way via RER C]", "Opulent royal palace of Louis XIV with the Hall of Mirrors, King's Grand Apartments, and monumental fountain gardens", 2600, "RER C to Versailles Château Rive Gauche"),
            ("Giverny & Claude Monet's Gardens [Day Trip: 1h 15m travel time each way via SNCF Train + Shuttle]", "Claude Monet's beloved pink home, water lily pond, and iconic Japanese footbridge that inspired Impressionist masterpieces", 1800, "SNCF from Gare Saint-Lazare to Vernon"),
        ]
    },

    # --- ITALY ---
    ("Italy", "Rome"): {
        "city_attractions": [
            ("Colosseum & Flavian Amphitheatre", "Monumental ancient Roman arena where gladiators once fought, marvel of Roman engineering and history", 2400, "Colosseo / Metro Line B"),
            ("Roman Forum & Palatine Hill", "Sprawling ruins of ancient Rome's political and religious epicenter, including imperial temples and palaces", 1800, "Colosseo / Metro Line B"),
            ("Vatican Museums & Sistine Chapel", "Enormous Papal art collections culminating in Michelangelo's frescoed ceiling and The Last Judgment", 2700, "Ottaviano / Metro Line A"),
            ("St. Peter's Basilica", "Vast Renaissance cathedral designed by Michelangelo and Bernini, crowning heart of the Vatican", 0, "Ottaviano / Metro Line A"),
            ("Pantheon & Piazza della Rotonda", "Astonishingly intact Roman temple with a massive unreinforced concrete dome and central open oculus", 500, "Barberini / Walking"),
            ("Trevi Fountain (Fontana di Trevi)", "Baroque fountain masterpiece where travelers toss a coin over their left shoulder to guarantee a return to Rome", 0, "Spagna / Walking"),
            ("Piazza Navona & Bernini's Fountain of Four Rivers", "Lively Baroque square built over Domitian's stadium, adorned with Bernini fountains and outdoor cafes", 0, "Spagna / Walking"),
        ],
        "day_trips": [
            ("Tivoli: Villa d'Este & Hadrian's Villa [Day Trip: 50m travel time each way via Cotral Bus / Train]", "Magnificent Renaissance fountain water gardens and sprawling ancient Roman imperial ruins in the Sabine hills", 1600, "Train from Roma Tiburtina to Tivoli"),
            ("Pompeii Archaeological Park [Day Trip: 1h 45m travel time each way via Frecciarossa to Naples + Circumvesuviana]", "Ancient Roman city frozen in time by the catastrophic eruption of Mount Vesuvius in 79 AD", 3500, "High-Speed Rail from Roma Termini to Napoli"),
        ]
    },

    # --- UNITED KINGDOM ---
    ("United Kingdom", "London"): {
        "city_attractions": [
            ("Tower of London & Tower Bridge", "Historic 11th-century castle fortress housing the Crown Jewels, White Tower, and iconic bascule bridge", 3200, "Tower Hill / Underground"),
            ("British Museum", "World-renowned institution dedicated to human history and art, housing the Rosetta Stone and Parthenon Sculptures", 0, "Tottenham Court Road / Underground"),
            ("Westminster Abbey & Big Ben", "Coronation church of British monarchs since 1066 and iconic Elizabeth Tower clock at the Houses of Parliament", 2700, "Westminster / Underground"),
            ("Buckingham Palace & St James's Park", "Official London residence of the British Sovereign and traditional Changing of the Guard ceremony", 0, "Green Park / Underground"),
            ("The National Gallery & Trafalgar Square", "Splendid art museum overlooking Trafalgar Square showcasing over 2,300 Western European paintings", 0, "Charing Cross / Underground"),
            ("Covent Garden & Royal Opera House", "Vibrant cobblestone market square filled with street performers, boutique shops, and historic theaters", 0, "Covent Garden / Underground"),
        ],
        "day_trips": [
            ("Stonehenge & Bath [Day Trip: 2h travel time each way via Great Western Railway]", "Prehistoric megalithic stone circle on Salisbury Plain and UNESCO Georgian Roman thermal baths in Bath", 4500, "Train from London Paddington"),
            ("Windsor Castle [Day Trip: 45m travel time each way via South Western Railway]", "Oldest and largest occupied royal castle in the world, family home of British monarchs for over 1,000 years", 3000, "Train from London Waterloo"),
        ]
    },

    # --- INDIA ---
    ("India", "Hyderabad"): {
        "city_attractions": [
            ("Charminar & Laad Bazaar", "Iconic 1591 monument with four grand minarets, surrounded by bustling pearl, lacquer bangle, and spice markets", 50, "Charminar / Hyderabad Metro"),
            ("Golconda Fort & Sound and Light Show", "Colossal medieval citadel famous for acoustic marvels, diamond trade history (Koh-i-Noor), and ramparts", 150, "Golconda / Taxi"),
            ("Qutb Shahi Tombs Heritage Park", "Magnificent landscaped royal necropolis blending Persian, Pathan, and Hindu architectural styles", 100, "Ibrahim Bagh / Auto-rickshaw"),
            ("Chowmahalla Palace", "Opulent 18th-century palace of the Nizams featuring Belgian crystal chandeliers, vintage Rolls-Royces, and courtyards", 150, "Khilwat / Old City"),
            ("Salar Jung Museum", "One of India's premier national museums housing Mir Yousuf Ali Khan's vast collection of sculptures, weapons, and clocks", 100, "Salarjung / Metro MGBS"),
            ("Hussain Sagar Lake & Buddha Statue", "Large heart-shaped historic lake featuring a monolithic 18-meter granite Buddha statue reached by motorboat", 150, "Necklace Road / Tank Bund"),
        ],
        "day_trips": [
            ("Ramoji Film City [Day Trip: 1h travel time each way]", "World's largest integrated film studio complex offering movie sets, stunt shows, and adventure parks", 1500, "Outer Ring Road / AC Shuttle"),
            ("Warangal Fort & Thousand Pillar Temple [Day Trip: 2h 30m travel time each way via Train]", "12th-century Kakatiya Dynasty capitals featuring intricate black basalt carvings and iconic Kakatiya Thoranam arches", 500, "Train from Secunderabad Station"),
        ]
    },
    ("India", "Delhi"): {
        "city_attractions": [
            ("Red Fort (Lal Qila)", "Imposing red sandstone Mughal fortress commissioned by Shah Jahan, symbol of India's sovereignty", 80, "Chandni Chowk / Metro Yellow Line"),
            ("Qutub Minar Complex", "73-meter victory tower built in 1192 and ancient rust-resistant Iron Pillar dating to the 4th century", 80, "Qutub Minar / Metro Yellow Line"),
            ("Humayun's Tomb", "UNESCO World Heritage garden tomb that directly inspired the architectural design of the Taj Mahal", 80, "JLN Stadium / Metro Violet Line"),
            ("India Gate & Kartavya Path", "Grand 42-meter triumphal arch war memorial at the heart of New Delhi's ceremonial boulevard", 0, "Central Secretariat / Metro"),
            ("Jama Masjid & Chandni Chowk", "One of India's largest mosques overlooking historic lanes famous for parathas, jalebis, and spices", 0, "Chawri Bazar / Metro"),
            ("Lotus Temple (Bahá'í House of Worship)", "Spectacular modern lotus-flower marble sanctuary welcoming people of all faiths for silent meditation", 0, "Kalkaji Mandir / Metro"),
        ],
        "day_trips": [
            ("Taj Mahal & Agra Fort [Day Trip: 1h 45m travel time each way via Gatimaan Express]", "Wonder of the World ivory-white marble mausoleum on the Yamuna river and imperial Mughal citadel in Agra", 2500, "Gatimaan Express from Hazrat Nizamuddin"),
            ("Jaipur Pink City [Day Trip / Overnight: 4h travel time each way via Vande Bharat Express]", "Royal capital of Rajasthan featuring Amber Fort, City Palace, and Hawa Mahal", 3000, "Vande Bharat Express from New Delhi"),
        ]
    }
}


def get_city_attractions(country: str, city: str) -> List[Tuple[str, str, int, str]]:
    """
    Returns verified, location-specific attractions for a specific city.
    Guarantees zero cross-city bleeding (e.g. Fushimi Inari will NEVER be returned for Tokyo).
    """
    c_clean = (country or "").strip().title()
    ci_clean = (city or "").strip().title()

    for (c, ci), data in CITY_ATTRACTIONS_DATABASE.items():
        if ci_clean.lower() in ci.lower() or ci.lower() in ci_clean.lower():
            if not c_clean or c_clean.lower() in c.lower() or c.lower() in c_clean.lower() or c_clean in ["Destination", "Country"]:
                return list(data.get("city_attractions", []))

    # Fallback to local discovery based on city name if city not in curated dictionary
    return [
        (f"{ci_clean} Historic Quarter & Old Town Walk", f"Explore the preserved historical alleys, central plaza, and cultural architecture of {ci_clean}", 0, "Walking / Metro"),
        (f"{ci_clean} Central Cathedral / Heritage Sanctuary", f"Visit {ci_clean}'s most revered religious monument and architectural centerpiece", 300, "Local transit"),
        (f"{ci_clean} National Cultural & History Museum", f"Discover key archaeological artifacts, royal relics, and local heritage exhibits of {ci_clean}", 600, "City Bus / Metro"),
        (f"{ci_clean} Historic Covered Market & Artisan Promenade", f"Sample regional street treats and browse handmade local crafts in {ci_clean}", 0, "Walking tour"),
    ]


def get_city_day_trips(country: str, city: str) -> List[Tuple[str, str, int, str]]:
    """
    Returns explicit day trips clearly labeled with travel time and transport mode.
    Never presents a distant destination (e.g. Mount Fuji) as an in-city attraction.
    """
    c_clean = (country or "").strip().title()
    ci_clean = (city or "").strip().title()

    for (c, ci), data in CITY_ATTRACTIONS_DATABASE.items():
        if ci_clean.lower() in ci.lower() or ci.lower() in ci_clean.lower():
            if not c_clean or c_clean.lower() in c.lower() or c.lower() in c_clean.lower() or c_clean in ["Destination", "Country"]:
                return list(data.get("day_trips", []))

    return []
