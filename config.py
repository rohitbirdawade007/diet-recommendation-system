import os
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH  = os.path.join(DATA_DIR, 'diet_recommendation_dataset_1000.csv')

MODEL_PATHS = {
    'logistic_regression': os.path.join(MODELS_DIR, 'logistic_regression.pkl'),
    'decision_tree':       os.path.join(MODELS_DIR, 'decision_tree.pkl'),
    'random_forest':       os.path.join(MODELS_DIR, 'random_forest.pkl'),
    'xgboost':             os.path.join(MODELS_DIR, 'xgboost.pkl'),
    'ann':                 os.path.join(MODELS_DIR, 'ann_model.pkl'),
}