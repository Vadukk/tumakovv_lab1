import pandas as pd
import numpy as np
import os
from catboost import CatBoostClassifier

from src.config import *
from src.utils import *


def train_models():
    df = pd.read_csv('../../data/processed/train_features.csv')

    for target in TARGETS:
        threshold = model_threshold_per_target[target]
        model_params = model_params_per_target[target]
        model_features = features_per_target[target]
        model = CatBoostClassifier(**model_params)

        model.fit(df[model_features], df[target])

        model.set_probability_threshold(threshold)

        model.save_model(f'model_{target}',
                          format="cbm",
                          export_parameters=None,
                          pool=None)


if __name__ == '__main__':
    train_models()




