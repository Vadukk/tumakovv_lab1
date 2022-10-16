import pandas as pd
import numpy as np

import os
from catboost import CatBoostClassifier

from src.config import *
from src.utils import *

def predict_values():
    df = pd.read_csv('../../data/processed/test_features.csv')
    df.set_index('ID', inplace=True)

    for target in TARGETS:
        model = CatBoostClassifier()

        model.load_model(f'model_{target}', format='cbm')
        model_features = features_per_target[target]

        df[target] = model.predict(df[model_features])
        df[target] = df[target].astype(int)

    df[TARGETS].to_csv('../../data/solution.csv', )


if __name__ == '__main__':
    predict_values()