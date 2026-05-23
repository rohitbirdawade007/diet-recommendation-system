import os
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

DATA_FILE = 'diet_recommendation_dataset_1000.csv'
DATA_PATH = os.path.join(DATA_DIR, DATA_FILE)