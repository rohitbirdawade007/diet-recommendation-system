# 🥗 DietAI — AI-Powered Diet Recommendation System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00?style=flat&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-0099CC?style=flat)](https://xgboost.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

> An end-to-end machine-learning system that recommends a personalised diet plan based on a patient's health profile. Trained on a real-world Kaggle dataset with **5 ML models**, served via a **Flask REST API**, and presented through a premium **dark-mode single-page web app**.

---

## ✨ Features

- **5 ML Models** — Logistic Regression, Decision Tree, Random Forest, XGBoost, ANN (Keras)
- **Imbalance handling** — Class weighting and sample weighting applied across all models
- **REST API** — Flask backend with 5 JSON endpoints
- **Premium UI** — Dark glassmorphism design, animated hero, Chart.js comparison dashboard, meal plan cards
- **Auto BMI** — BMI auto-calculated as the user types height and weight
- **Model switcher** — Select any of the 5 models directly in the UI
- **One-click deploy** — `render.yaml` for free Render.com deployment

---

## 🗂 Project Structure

```
Diet-Recommendation-System/
│
├── data/
│   └── diet_recommendation_dataset_1000.csv
│
├── models/                         ← Generated after training
│   ├── logistic_regression.pkl
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── ann_model.h5
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── model_metrics.json
│
├── src/
│   ├── preprocessing.py            ← Data loading, scaling, encoding
│   ├── train_models.py             ← Train all 5 models
│   ├── evaluate.py                 ← Metrics + comparison charts
│   ├── predict.py                  ← Inference with caching
│   └── recommendation.py          ← Diet advice database
│
├── static/
│   ├── index.html                  ← Single-page app
│   ├── css/style.css               ← Dark glassmorphism theme
│   └── js/app.js                   ← SPA logic + Chart.js
│
├── app.py                          ← Flask REST API
├── config.py                       ← Paths, hyperparams, label maps
├── requirements.txt
├── render.yaml                     ← Render.com deploy config
└── README.md
```

---

## 📊 Dataset

**Source:** [Diet Recommendation Dataset — Kaggle](https://www.kaggle.com/datasets/rohitsbirdawade/diet-dataset)

| Feature | Description |
|---|---|
| Age | Patient age |
| Gender | 0 = Female, 1 = Male |
| Height_cm | Height in centimetres |
| Weight_kg | Weight in kilograms |
| BMI | Body Mass Index |
| Activity_Level | 0 = Sedentary, 1 = Moderate, 2 = Active |
| Sugar_Level | Blood glucose (mg/dL) |
| Cholesterol | Cholesterol (mg/dL) |
| Goal | 0 = Weight Loss, 1 = Maintenance, 2 = Muscle Gain |
| **Diet** (target) | Diabetic · Low Carb · Heart Healthy · High Protein · Balanced |

> Dataset is imbalanced (Diabetic 54 %, Balanced 4 %). Class weighting is applied to all models.

---

## 🧠 Models

| Model | Library | Class Balancing |
|---|---|---|
| Logistic Regression | scikit-learn | `class_weight='balanced'` |
| Decision Tree | scikit-learn | `class_weight='balanced'` |
| Random Forest | scikit-learn | `class_weight='balanced'` |
| XGBoost | xgboost | `compute_sample_weight('balanced')` |
| ANN (Neural Network) | TensorFlow/Keras | `class_weight` dict passed to `fit()` |

---

## 🚀 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/diet-recommendation-system.git
cd diet-recommendation-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train all models
```bash
python src/train_models.py
```

### 4. Evaluate and generate charts
```bash
python src/evaluate.py
```

### 5. Run the Flask app
```bash
python app.py
```

Visit **http://localhost:5000** 🎉

---

## 🌐 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Serve the web UI |
| `POST` | `/api/predict` | Get diet prediction |
| `GET` | `/api/models` | All model accuracy metrics |
| `GET` | `/api/diet-info/<diet>` | Info for one diet |
| `GET` | `/api/diets` | All diet advice |
| `GET` | `/api/stats` | Dataset statistics |

### Example — predict request
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 35, "Gender": 1, "Height_cm": 175, "Weight_kg": 80,
    "BMI": 26.1, "Activity_Level": 1, "Sugar_Level": 120,
    "Cholesterol": 200, "Goal": 0, "model": "random_forest"
  }'
```

---

## ☁️ Deploy to Render.com (Free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and configures everything
5. Click **Deploy** — done! 🚀

> The build command trains all models on first deploy so no pre-trained files need to be committed.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask 3.0 + Flask-CORS |
| ML | scikit-learn, XGBoost, TensorFlow/Keras |
| Frontend | HTML5 + CSS3 (Glassmorphism) + Vanilla JS |
| Charts | Chart.js 4 |
| Fonts | Google Fonts (Outfit + Inter) |
| Hosting | Render.com (Flask) |

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">Made with ❤️ using Python, Flask & Machine Learning</p>
