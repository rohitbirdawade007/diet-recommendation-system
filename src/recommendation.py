# -*- coding: utf-8 -*-
"""
src/recommendation.py -- Rich diet advice mapped to each predicted diet label.
Calorie ranges use plain hyphens to avoid encoding issues across platforms.
"""

DIET_ADVICE = {
    "Diabetic": {
        "color":       "#ef4444",
        "gradient":    "linear-gradient(135deg,#ef4444,#b91c1c)",
        "icon":        "\U0001fa78",   # 🩸  blood drop
        "tagline":     "Control blood sugar through smart food choices",
        "description": (
            "A diabetic-friendly diet focuses on controlling blood sugar levels "
            "through careful carbohydrate management, high-fiber intake, and lean "
            "proteins. Keeping meals consistent in portion size and timing is key."
        ),
        "calories": "1500-2000 kcal/day",
        "foods_to_eat": [
            "Non-starchy vegetables (broccoli, spinach, kale, cauliflower)",
            "Whole grains (quinoa, barley, steel-cut oats)",
            "Lean proteins (chicken breast, fish, tofu, eggs)",
            "Legumes (lentils, chickpeas, black beans)",
            "Low-glycemic fruits (berries, apples, pears, cherries)",
            "Healthy fats (avocado, olive oil, walnuts, chia seeds)",
        ],
        "foods_to_avoid": [
            "Sugary beverages and fruit juices",
            "White bread, pasta, and refined rice",
            "Fried and ultra-processed foods",
            "High-sugar desserts, candies, and pastries",
            "Sweetened yogurt and flavored dairy products",
            "Alcohol -- especially beer and sweet cocktails",
        ],
        "meal_plan": {
            "breakfast": "Steel-cut oatmeal with berries and chia seeds + 2 boiled eggs",
            "lunch":     "Grilled chicken salad with olive oil dressing + side of quinoa",
            "dinner":    "Baked salmon with steamed broccoli and a small portion of brown rice",
            "snacks":    "Apple slices with almond butter  |  A handful of walnuts",
        },
        "key_nutrients": [
            "Fiber (25-35 g/day)",
            "Omega-3 fatty acids",
            "Magnesium",
            "Chromium",
            "Vitamin D & B12",
        ],
    },

    "Low Carb": {
        "color":       "#f59e0b",
        "gradient":    "linear-gradient(135deg,#f59e0b,#b45309)",
        "icon":        "\U0001f951",   # 🥑  avocado
        "tagline":     "Burn fat efficiently with reduced carbohydrate intake",
        "description": (
            "A low-carbohydrate diet reduces daily carb intake to encourage fat "
            "burning, improve insulin sensitivity, and support weight management. "
            "Focus on healthy fats and quality proteins as primary energy sources."
        ),
        "calories": "1400-1800 kcal/day",
        "foods_to_eat": [
            "Meat & poultry (beef, chicken, turkey, pork)",
            "Fatty fish (salmon, mackerel, sardines, tuna)",
            "Eggs (all preparations)",
            "Low-carb vegetables (zucchini, cauliflower, leafy greens, peppers)",
            "Nuts & seeds (almonds, walnuts, chia, flaxseed)",
            "Cheese, Greek yogurt, and full-fat dairy",
            "Avocados and extra-virgin olive oil",
        ],
        "foods_to_avoid": [
            "Bread, pasta, white rice, and cereals",
            "Sugary foods, sweets, and desserts",
            "Starchy vegetables (potatoes, corn, peas)",
            "High-sugar fruits (bananas, grapes, mangoes)",
            "Beer and sugary cocktails",
            "Processed 'low-fat' products packed with sugar",
        ],
        "meal_plan": {
            "breakfast": "Scrambled eggs with sauteed spinach and half an avocado",
            "lunch":     "Lettuce-wrapped burger with cheese, bacon, tomato, and mustard",
            "dinner":    "Grilled rib-eye steak with cauliflower mash and roasted asparagus",
            "snacks":    "Cheese cubes  |  Hard-boiled eggs  |  Celery with almond butter",
        },
        "key_nutrients": [
            "Healthy fats (60-70% of calories)",
            "Quality protein (20-25%)",
            "Electrolytes: sodium, potassium, magnesium",
            "Fiber from non-starchy vegetables",
        ],
    },

    "Heart Healthy": {
        "color":       "#ec4899",
        "gradient":    "linear-gradient(135deg,#ec4899,#9d174d)",
        "icon":        "\u2764\ufe0f",  # ❤️  heart
        "tagline":     "Protect your heart with every bite",
        "description": (
            "A heart-healthy diet emphasises foods that lower LDL cholesterol, "
            "reduce blood pressure, and minimize systemic inflammation. Built on "
            "the Mediterranean dietary pattern, it prioritizes plant foods, "
            "whole grains, and omega-3-rich fish."
        ),
        "calories": "1600-2200 kcal/day",
        "foods_to_eat": [
            "Fatty fish rich in omega-3 (salmon, tuna, mackerel, trout)",
            "Whole grains (oats, whole wheat, farro, bulgur)",
            "Colorful fruits and vegetables (5+ servings/day)",
            "Legumes (beans, lentils, chickpeas)",
            "Olive oil and avocados as primary fat sources",
            "Nuts (walnuts, almonds, pistachios)",
            "Dark chocolate (70%+ cacao) in moderation",
        ],
        "foods_to_avoid": [
            "Trans fats and partially hydrogenated oils",
            "Processed and red meats (hot dogs, deli meats, bacon)",
            "High-sodium packaged foods and added table salt",
            "Sugary beverages, sweets, and pastries",
            "Refined carbohydrates and white flour products",
            "Excessive alcohol",
        ],
        "meal_plan": {
            "breakfast": "Overnight oats with blueberries, walnuts, and ground flaxseed",
            "lunch":     "Mediterranean salad with grilled tuna, olives, tomatoes, feta, and olive oil",
            "dinner":    "Baked salmon with roasted Mediterranean vegetables and quinoa",
            "snacks":    "Mixed nuts  |  Apple with walnut butter  |  2 squares dark chocolate",
        },
        "key_nutrients": [
            "Omega-3 fatty acids (EPA & DHA)",
            "Fiber (30+ g/day)",
            "Antioxidants (vitamins C & E)",
            "Potassium & folate",
            "Plant sterols/stanols",
        ],
    },

    "High Protein": {
        "color":       "#06b6d4",
        "gradient":    "linear-gradient(135deg,#06b6d4,#0369a1)",
        "icon":        "\U0001f4aa",   # 💪  flexed bicep
        "tagline":     "Build muscle and recover faster with protein power",
        "description": (
            "A high-protein diet supports muscle hypertrophy, exercise recovery, "
            "and satiety. Ideal for active individuals pursuing muscle gain or body "
            "recomposition. Protein should be distributed evenly across 4-5 meals."
        ),
        "calories": "2000-2800 kcal/day",
        "foods_to_eat": [
            "Chicken breast, turkey, lean beef, and pork tenderloin",
            "Fish and seafood (tuna, shrimp, salmon, tilapia)",
            "Eggs and egg whites",
            "Greek yogurt (plain, 0%) and cottage cheese",
            "Whey or plant-based protein powders",
            "Legumes (edamame, lentils, kidney beans, black beans)",
            "Tofu, tempeh, and seitan",
        ],
        "foods_to_avoid": [
            "Processed meats (sausages, hot dogs, deli meats)",
            "Deep-fried and battered foods",
            "Sugary drinks, pastries, and candy",
            "Alcohol -- impairs protein synthesis and recovery",
            "Empty-calorie snacks (chips, crackers)",
            "Excessive refined carbohydrates",
        ],
        "meal_plan": {
            "breakfast": "4-egg veggie omelette + Greek yogurt parfait with granola",
            "lunch":     "Grilled chicken breast bowl with quinoa, broccoli, and hummus",
            "dinner":    "Lean beef stir-fry with edamame, bell peppers, and brown rice",
            "snacks":    "Protein shake  |  Cottage cheese with fruit  |  Turkey roll-ups",
        },
        "key_nutrients": [
            "Protein: 1.6-2.2 g per kg of bodyweight",
            "BCAAs (leucine, isoleucine, valine)",
            "Creatine monohydrate",
            "Iron & zinc",
            "Vitamin B12 & D3",
        ],
    },

    "Balanced": {
        "color":       "#10b981",
        "gradient":    "linear-gradient(135deg,#10b981,#047857)",
        "icon":        "\u2696\ufe0f",  # ⚖️  balance scale
        "tagline":     "All nutrients in perfect harmony for lifelong health",
        "description": (
            "A balanced diet provides all essential macronutrients and micronutrients "
            "in optimal proportions to maintain energy, wellbeing, and long-term "
            "health. It emphasises variety, moderation, and whole, minimally "
            "processed foods across all food groups."
        ),
        "calories": "1800-2400 kcal/day",
        "foods_to_eat": [
            "Variety of colorful fruits and vegetables (aim for the rainbow)",
            "Whole grains (oats, brown rice, whole wheat, quinoa)",
            "Lean proteins (chicken, fish, eggs, legumes, low-fat dairy)",
            "Low-fat dairy or fortified plant-based alternatives",
            "Healthy fats (avocado, olive oil, nuts, seeds)",
            "Hydrating foods (cucumber, watermelon, celery)",
            "Herbs and spices for flavor without extra sodium",
        ],
        "foods_to_avoid": [
            "Ultra-processed and fast foods",
            "Trans fats and hydrogenated oils",
            "Excessive added sugars (>10% of total calories)",
            "High-sodium packaged snacks",
            "Sugary beverages (sodas, energy drinks, sweetened juices)",
            "Excessive alcohol",
        ],
        "meal_plan": {
            "breakfast": "Whole grain toast with smashed avocado + a fresh berry smoothie",
            "lunch":     "Grilled chicken wrap with mixed greens, tomatoes, and hummus",
            "dinner":    "Baked cod with roasted sweet potato and steamed mixed vegetables",
            "snacks":    "Mixed fruit bowl  |  Hummus with veggie sticks  |  Trail mix",
        },
        "key_nutrients": [
            "All macronutrients in balance (50% carbs / 25% protein / 25% fat)",
            "Vitamins A, C, D, E, and K",
            "B-complex vitamins",
            "Calcium, iron, and zinc",
            "Prebiotic fiber for gut health",
        ],
    },
}


def get_diet_advice(diet_label: str) -> dict:
    """Return the advice dict for a given diet label (exact match)."""
    return DIET_ADVICE.get(diet_label, DIET_ADVICE["Balanced"])


def get_all_diets() -> dict:
    """Return all diet advice entries (suitable for /api/diets endpoint)."""
    return DIET_ADVICE
