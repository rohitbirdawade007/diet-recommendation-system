# 🌿 DietAI - AI-Powered Diet Recommendation System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-189AB4)](https://xgboost.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-2d6a4f)](LICENSE)
[![GitHub commits](https://img.shields.io/github/commit-activity/t/rohitbirdawade007/diet-recommendation-system)](https://github.com/rohitbirdawade007/diet-recommendation-system)

> **An end-to-end Machine Learning system** that recommends personalised diet plans (Balanced, Diabetic, Heart Healthy, High Protein, Low Carb) based on a patient's health profile. Built with Flask REST API + premium Organic Nature-themed web UI.

**Live Demo:** https://diet-recommendation-system-q5m7.onrender.com

---
# DietAI - Diet Recommendation System
## Project Architecture

```
DietAI/
├── data/                   # Dataset CSV
├── models/                 # Trained .pkl artifacts + charts
├── src/
│   ├── preprocessing.py    # Data loading, encoding, scaling
│   ├── train_models.py     # Train 5 ML models
│   ├── evaluate.py         # Metrics, charts, confusion matrix
│   ├── predict.py          # Inference with caching
│   └── recommendation.py   # Diet advice database
├── static/
│   ├── index.html          # Single-page app
│   ├── css/style.css       # Organic nature theme
│   └── js/app.js           # SPA logic (fetch, charts, BMI calc)
├── app.py                  # Flask REST API
├── config.py               # Central config
├── requirements.txt        # Python dependencies
├── render.yaml             # Render.com deploy config
└── README.md
```

## Input Features

| Feature | Type | Description |
|---|---|---|
| Age | int | Patient age in years |
| Gender | int | 0 = Female, 1 = Male |
| Height_cm | float | Height in centimetres |
| Weight_kg | float | Weight in kilograms |
| BMI | float | Body Mass Index (auto-calculated) |
| Activity_Level | int | 1=Sedentary, 2=Light, 3=Moderate, 4=Active, 5=Very Active |
| Sugar_Level | float | Blood sugar level (mg/dL) |
| Cholesterol | float | Cholesterol level (mg/dL) |
| Goal | int | 1=Weight Loss, 2=Maintain, 3=Muscle Gain |

## Diet Categories

| Diet | Calories | Focus |
|---|---|---|
| Balanced | 1800-2400 kcal/day | All macronutrients in harmony |
| Diabetic | 1500-2000 kcal/day | Blood sugar control |
| Heart Healthy | 1600-2200 kcal/day | Cardiovascular protection |
| High Protein | 2000-2800 kcal/day | Muscle building and recovery |
| Low Carb | 1400-1800 kcal/day | Fat burning and insulin sensitivity |

## Tech Stack

| Layer | Technology |
|---|---|
| ML Framework | scikit-learn 1.3+, XGBoost 2.0 |
| Backend | Flask 3.0, Flask-CORS, Gunicorn |
| Frontend | Vanilla HTML5 / CSS3 / JavaScript |
| Charts | Chart.js 4.x |
| Fonts | Google Fonts (Outfit + Inter) |
| Deployment | Render.com (free tier) |
| Version Control | Git / GitHub |

## License

MIT License — free to use for educational and personal projects.

---
Made with by Rohit Birdawade


