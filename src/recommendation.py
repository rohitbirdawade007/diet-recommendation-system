# -*- coding: utf-8 -*-
"""src/recommendation.py - Rich diet advice for each predicted diet label."""

DIET_ADVICE = {
    'Balanced': {
        'color': '#2d6a4f', 'gradient': 'linear-gradient(135deg,#2d6a4f,#1b4332)',
        'icon': '⚖️', 'tagline': 'Optimal nutrition for long-term health and vitality',
        'description': 'A balanced diet provides all essential nutrients by incorporating a wide variety of foods in the right proportions. It supports overall well-being, stable energy levels, and disease prevention.',
        'calories': '1800-2400 kcal/day',
        'foods_to_eat': ['Fresh fruits and vegetables','Whole grains (brown rice, oats)','Lean proteins (chicken, fish, tofu)','Healthy fats (olive oil, avocados)','Nuts and seeds','Low-fat dairy or alternatives'],
        'foods_to_avoid': ['Highly processed foods','Added sugars','Trans fats','Excessive sodium','Refined carbohydrates','Sugary drinks'],
        'meal_plan': {'breakfast':'Oatmeal topped with fresh fruit and walnuts','lunch':'Mixed green salad with grilled chicken and vinaigrette','dinner':'Baked salmon, sweet potato, and roasted asparagus','snacks':'Greek yogurt | Carrot sticks with hummus'},
        'key_nutrients': ['Vitamins A, C, E','Dietary fiber','Protein (0.8-1g per kg)','Calcium','Iron'],
    },
    'Diabetic': {
        'color': '#b94040', 'gradient': 'linear-gradient(135deg,#b94040,#7f2020)',
        'icon': '🩸', 'tagline': 'Control blood sugar through smart food choices',
        'description': 'A diabetic-friendly diet focuses on controlling blood sugar levels through careful carbohydrate management, high-fiber intake, and lean proteins to avoid blood glucose spikes.',
        'calories': '1500-2000 kcal/day',
        'foods_to_eat': ['Non-starchy vegetables (spinach, broccoli)','Whole grains (quinoa, barley)','Lean proteins','Legumes and beans','Low-glycemic fruits (berries, apples)','Healthy fats'],
        'foods_to_avoid': ['Sugary beverages','White bread, pasta, and rice','Fried foods','High-sugar desserts','Sweetened yogurt','Alcohol'],
        'meal_plan': {'breakfast':'Steel-cut oatmeal with berries + 2 boiled eggs','lunch':'Grilled chicken salad + quinoa','dinner':'Baked salmon + steamed broccoli + brown rice','snacks':'Apple with almond butter | Handful of walnuts'},
        'key_nutrients': ['Fiber (25-35 g/day)','Omega-3 fatty acids','Magnesium','Chromium','Vitamin D & B12'],
    },
    'Heart Healthy': {
        'color': '#c44f8a', 'gradient': 'linear-gradient(135deg,#c44f8a,#8a2560)',
        'icon': '❤️', 'tagline': 'Protect your cardiovascular system with wholesome foods',
        'description': 'A heart-healthy diet is rich in fruits, vegetables, whole grains, and healthy fats while limiting saturated fats, trans fats, and sodium to lower cholesterol and blood pressure.',
        'calories': '1600-2200 kcal/day',
        'foods_to_eat': ['Fatty fish (salmon, mackerel)','Berries and citrus fruits','Oats and whole grains','Nuts (walnuts, almonds)','Olive oil and avocados','Dark leafy greens'],
        'foods_to_avoid': ['Red meat and processed meats','Butter and lard','High-sodium snacks','Trans fats (partially hydrogenated oils)','Refined carbs','Excessive alcohol'],
        'meal_plan': {'breakfast':'Smoothie with spinach, berries, flaxseed, and oat milk','lunch':'Tuna salad with olive oil on whole wheat bread','dinner':'Grilled chicken, quinoa, and roasted Brussels sprouts','snacks':'Unsalted almonds | Orange slices'},
        'key_nutrients': ['Omega-3 fatty acids','Potassium','Soluble fiber','Antioxidants','Plant sterols'],
    },
    'High Protein': {
        'color': '#1a7a6e', 'gradient': 'linear-gradient(135deg,#1a7a6e,#0d4d44)',
        'icon': '💪', 'tagline': 'Fuel muscle growth and recovery',
        'description': 'A high-protein diet supports muscle repair, growth, and metabolism. It is ideal for active individuals or those aiming to build lean body mass while feeling fuller for longer.',
        'calories': '2000-2800 kcal/day',
        'foods_to_eat': ['Lean meats (chicken breast, turkey)','Eggs and egg whites','Greek yogurt and cottage cheese','Lentils and beans','Protein powders (whey, plant-based)','Tofu and tempeh'],
        'foods_to_avoid': ['Empty calorie snacks','High-fat processed meats (sausage, bacon)','Sugary cereals','Alcohol','Refined grains lacking protein'],
        'meal_plan': {'breakfast':'3-egg omelette with spinach + whole wheat toast','lunch':'Turkey wrap with black beans and avocado','dinner':'Grilled steak (lean cut) + quinoa + green beans','snacks':'Protein shake | Edamame'},
        'key_nutrients': ['Protein (1.6-2.2g per kg)','BCAAs (Leucine, Isoleucine, Valine)','Iron','Zinc','Vitamin B-complex'],
    },
    'Low Carb': {
        'color': '#c8813a', 'gradient': 'linear-gradient(135deg,#c8813a,#8a5520)',
        'icon': '🥑', 'tagline': 'Burn fat and improve insulin sensitivity',
        'description': 'A low-carb diet minimizes carbohydrate intake and emphasizes proteins and healthy fats. It is highly effective for weight loss and stabilizing blood sugar levels.',
        'calories': '1400-1800 kcal/day',
        'foods_to_eat': ['Meat and poultry','Seafood','Eggs','Non-starchy above-ground vegetables','Nuts and seeds','High-fat dairy (cheese, butter)'],
        'foods_to_avoid': ['Sugar and sweets','Grains (wheat, rice, oats)','Starchy vegetables (potatoes, corn)','High-sugar fruits (bananas, grapes)','Legumes and beans','Diet/low-fat products (often contain sugar)'],
        'meal_plan': {'breakfast':'Scrambled eggs with bacon and avocado','lunch':'Grilled chicken Caesar salad (no croutons)','dinner':'Zucchini noodles with beef meatballs and marinara sauce','snacks':'Macadamia nuts | Cheese slices'},
        'key_nutrients': ['Healthy fats (Monounsaturated)','Electrolytes (Sodium, Potassium, Magnesium)','Protein','Dietary fiber (from veggies)'],
    },
}

def get_diet_advice(diet_label):
    return DIET_ADVICE.get(diet_label, DIET_ADVICE.get('Balanced', {}))

def get_all_diets():
    return DIET_ADVICE