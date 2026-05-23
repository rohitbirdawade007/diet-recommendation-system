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
