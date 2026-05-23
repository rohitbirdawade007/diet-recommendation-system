# -*- coding: utf-8 -*-
"""src/recommendation.py - Rich diet advice for each predicted diet label."""

DIET_ADVICE = {
    'Diabetic': {
        'color': '#b94040', 'gradient': 'linear-gradient(135deg,#b94040,#7f2020)',
        'icon': '\U0001fa78', 'tagline': 'Control blood sugar through smart food choices',
        'description': 'A diabetic-friendly diet focuses on controlling blood sugar levels through careful carbohydrate management, high-fiber intake, and lean proteins.',
        'calories': '1500-2000 kcal/day',
        'foods_to_eat': ['Non-starchy vegetables','Whole grains (quinoa, barley)','Lean proteins','Legumes','Low-glycemic fruits','Healthy fats'],
        'foods_to_avoid': ['Sugary beverages','White bread and pasta','Fried foods','High-sugar desserts','Sweetened yogurt','Alcohol'],
        'meal_plan': {'breakfast':'Steel-cut oatmeal with berries + 2 boiled eggs','lunch':'Grilled chicken salad + quinoa','dinner':'Baked salmon + steamed broccoli + brown rice','snacks':'Apple with almond butter | Walnuts'},
        'key_nutrients': ['Fiber (25-35 g/day)','Omega-3 fatty acids','Magnesium','Chromium','Vitamin D & B12'],
    },
}

def get_diet_advice(diet_label): return DIET_ADVICE.get(diet_label, DIET_ADVICE.get('Balanced', {}))
def get_all_diets(): return DIET_ADVICE