import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')
import country_data
from country_data import get_traditional_clothing
from app import get_food_cards

sample_countries = [
    'Mexico', 'Egypt', 'Greece', 'Saudi Arabia', 'Argentina', 'Kenya',
    'Turkey', 'Switzerland', 'Portugal', 'Peru', 'Morocco', 'New Zealand',
    'Sweden', 'Norway', 'Ireland', 'Netherlands', 'South Africa'
]

print('=== TESTING ATTIRE & FOOD ON ADDITIONAL COUNTRIES ===', flush=True)
for c in sample_countries:
    clothing = get_traditional_clothing(c)
    attires = clothing.get('attires') or [clothing.get('women'), clothing.get('men')]
    attires = [a for a in attires if a]
    cards = get_food_cards(c)
    names = [a.get('name') for a in attires]
    print(f'{c}:', flush=True)
    print(f'  Attires ({len(attires)}): {names}', flush=True)
    for a in attires:
        an = a.get('name')
        aimg = bool(a.get('image'))
        print(f'    - {an}: has_image={aimg}', flush=True)
    fnames = [f.get('name') for f in cards]
    print(f'  Food ({len(cards)}): {fnames}', flush=True)
    for f in cards:
        fn = f.get('name')
        fimg = bool(f.get('image'))
        print(f'    - {fn}: has_image={fimg}', flush=True)
