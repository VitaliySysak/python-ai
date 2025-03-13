# Використовуючи вибраний вами набір даних, побудуйте модель машинного навчання, яка прогнозує цільову змінну на основі інших ознак.
# Вибраний набір даних, відповідно до ваших інтересів, рекомендовано завантажити з сайту https://www.kaggle.com/datasets ;
# За основу можна взяти приклад коду, приєднаний до цього завдання (sclearn_example.py).

# Рекомендації:
# Виберіть набір даних, який вам цікавий, з Kaggle або інших джерел.
# Зосередьтеся на розумінні кожного кроку та експериментуйте з різними методами та параметрами.
# Документуйте свій код та результати.

# Основне завдання

# Завантаження даних:
# Завантажте набір даних з CSV-файлу, бази даних або іншого джерела.
# Перетворіть дані в Pandas DataFrame для зручності аналізу.

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler,  OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            df = pd.read_csv(self.file_path)

            return df
        except FileNotFoundError:
            print(f"Error: file '{self.file_path}' not found.")

            return None

class CategoricalEncoder:
    def __init__(self, df):
        self.df = df

    def encode_onehot(self, columns):
        print(self.df.head(1))
        for column in columns:
            if self.df[column].dtype == 'category' or self.df[column].dtype == 'object':  
                dummies = pd.get_dummies(self.df[column], prefix=column, drop_first=True)  
                self.df = pd.concat([self.df, dummies], axis=1)
                self.df.drop(column, axis=1, inplace=True)
                print(f"Колонка '{column}' закодована за допомогою one-hot encoding.")
        print(self.df.head(1))

    def encode_label(self, columns):
        print(self.df.head(1))
        for column in columns:
            if self.df[column].dtype == 'object':
                self.df[column] = pd.factorize(self.df[column])[0]
                print(f"Колонка '{column}' закодована за допомогою label encoding.")
        print(self.df.head(1))

class DataProcessor(DataLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.df = self.load_data()

    # Підготовка даних:
    # Виконайте розвідувальний аналіз даних (EDA) для розуміння структури даних, виявлення відсутніх значень та викидів.
    # Обробіть відсутні значення (заповніть або видаліть).
    # Видаліть викиди, якщо вони присутні.
    def data_info(self):
        print(self.df.head(), "\n")
        print(self.df.info(), "\n")
        print(self.df.describe(), "\n")
        print(self.df.columns.to_list(), "\n")
    
    def clean_data(self, key_column):
        if (self.df.isna().sum()[key_column] >= 1):
            self.df = self.df[key_column].dropna()
            print(f"Count of missing values after cleaning: {self.df[key_column].isna().sum()}")
        else:
            print("No missing values found by key column")

    # Перетворіть категоріальні ознаки в числові за допомогою one-hot encoding або label encoding.
    # Масштабуйте числові ознаки за допомогою StandardScaler або MinMaxScaler.
    # Видаліть непотрібні ознаки.
    # Використовуйте ColumnTransformer і Pipeline для організації етапів підготовки даних.



# Розбиття даних:
# Розділіть набір даних на навчальний та тестовий набори у співвідношенні 80/20 або іншому відповідному співвідношенні.



# Вибір моделі:
# Виберіть модель машинного навчання, яка підходить для вашої задачі (класифікація або регресія).
# Використовуйте Pipeline для об'єднання етапів підготовки даних та навчання моделі.



# Навчання моделі:
# Навчіть обрану модель на навчальному наборі даних.



# Передбачення:
# Зробіть передбачення на тестовому наборі даних.



# Оцінка моделі:
# Оцініть якість моделі за допомогою відповідних метрик.
# Виконайте крос-валідацію для оцінки стійкості моделі.



# Підвищення якості моделі:
# Використовуючи методи підвищення якості моделі, добитися параметра R2 > 0.5 при крос-валідації з 5 фолдами.



# Додаткове завдання - оптимізація моделі:
# Налаштуйте гіперпараметри моделі для покращення її якості.
# Спробуйте різні моделі машинного навчання та порівняйте їхні результати.


data_processor = DataProcessor("./datasets/most_watched_anime_dataset_100_entries.csv")

# data_processor.data_info()
data_processor.clean_data("Anime Name")