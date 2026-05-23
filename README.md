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
