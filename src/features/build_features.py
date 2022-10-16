import pandas as pd
import numpy as np

from src.config import *
from src.utils import *


def create_features(data : pd.DataFrame, is_train : bool) -> pd.DataFrame:
    
    if is_train:
        data['Пол'].fillna('Ж', inplace=True)  # 54-701-009-01
        data['Время засыпания'].replace('12:00:00', '00:00:00', inplace=True)  # 54-002-054-02
        data.loc[data['Частота пасс кур'].isna() == False, 'Пассивное курение'] = 1  # 54-001-079-01
    
    else:
        data['Статус Курения'].replace('Никогда не курил', 'Никогда не курил(а)', inplace=True)  # 54-701-037-01
        data['Время засыпания'].replace('09:00:00', '21:00:00', inplace=True)  # 54-602-001-01
        data['Время засыпания'].replace('00:00:30', '00:30:00', inplace=True)  # 54-103-014-01
        data['Время пробуждения'].replace('00:06:00', '06:00:00', inplace=True)
        
    no_time = (data['Время засыпания'] == data['Время пробуждения'])
    data.loc[no_time, ['Время засыпания']] = '23:00:00'
    data.loc[no_time, ['Время пробуждения']] = '07:00:00'
    
    data.fillna(0, inplace=True)
    
    features = data[['ID']].copy()
    
    if is_train:
        for target in TARGETS:
            features[target] = data[target] == 1 
            
    for name, column, values in base_features:
        features[name] = data[column].isin(values)
        
    features['Возраст курения'] = data['Возраст курения']
    features['Сигарет в день'] = data['Сигарет в день']
    features['Возраст алког'] = data['Возраст алког']
    features['Образование - Уровень'] = data['Образование'].str[0].astype(int)
    
    features['Одинокий мужчина'] = features['Пол - М'] & features['Семья - живет один']
    features['Одинокая женщина'] = (~features['Пол - М']) & features['Семья - живет один']

    features['Без работы и не на пенсии'] = (~features['Вы работаете?']) & (~features['Выход на пенсию'])

    features['Сигарет в день (сейчас)'] = features['Сигарет в день']
    features.loc[features['Статус Курения - Бросил(а)'], 'Сигарет в день (сейчас)'] = 0
    
    features['Частота пасс кур'] = data['Частота пасс кур'].apply(second_hand_smoke_count)

    features['Болезнь легких'] = features['Хроническое заболевание легких'] | features['Бронхиальная астма'] | features['Туберкулез легких']
    features['Инфекционная болезнь'] = features['Гепатит'] | features['ВИЧ/СПИД']
    features['Хроническая болезнь'] = features['Болезнь легких'] | features['Инфекционная болезнь'] | features['Сахарный диабет'] | features['Онкология']
    features['Регулярный прием лекарственных средств без болезней из опроса'] = (features['Хроническая болезнь'] == False) & features['Регулярный прием лекарственных средств']
    features['Больной'] = features['Хроническая болезнь'] | features['Прекращение работы по болезни'] | features['Регулярный прием лекарственных средств']
    features['Травмы / переломы'] = features['Травмы за год'] | features['Переломы']
    features['Идеальное здоровье'] = (features['Больной'] == False) & (features['Травмы / переломы'] == False)
    features['Без вредных привычек'] = features['Статус Курения - Никогда не курил(а)'] & features['Алкоголь - никогда не употреблял']
    features['Бросил вредную привычку'] = features['Статус Курения - Бросил(а)'] | features['Алкоголь - ранее употреблял']
    features['Макс. возраст вредной привычки'] = features[['Возраст курения', 'Возраст алког']].max(axis=1)
    features['Само совершенство'] = features['Идеальное здоровье'] & features['Без вредных привычек'] & (features['Пассивное курение'] == False)
    features['Активное или пассивное курение'] = features['Пассивное курение'] | features['Статус Курения - Курит']
    
    features['Продолжительность сна'] = 8 + data['Время пробуждения'].apply(wakeup_time) \
                                   - data['Время засыпания'].apply(sleep_time)
    
    features[features.columns[1:]] = features[features.columns[1:]].astype(float)
    features = features.set_index('ID')
    return features

