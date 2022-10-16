import pandas as pd
import numpy as np
import os

from src.utils import *
from src.config import *

from src.features.build_features import create_features

raw_path = '../../data/raw/'

if __name__ == '__main__':

    train = pd.read_csv(os.path.join(raw_path, 'train.csv'))
    test = pd.read_csv(os.path.join(raw_path, 'test.csv'))

    train_features = create_features(train, True)
    test_features = create_features(test, False)

    train_features.to_csv('../../data/processed/train_features.csv')
    test_features.to_csv('../../data/processed/test_features.csv')
