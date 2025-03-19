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
from typing import Literal, Optional
from pandas.api.types import is_numeric_dtype

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

class DataProcessor(DataLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.df = self.load_data()

    # Підготовка даних:
    # Виконайте розвідувальний аналіз даних (EDA) для розуміння структури даних, виявлення відсутніх значень та викидів.
    # Обробіть відсутні значення (заповніть або видаліть).
    # Видаліть викиди, якщо вони присутні.
    def data_overview(self):
        print(self.df.head(), "\n")
        print(self.df.info(), "\n")
        print(self.df.describe(), "\n")
        print(self.df.columns.to_list(), "\n")

    def show_missing_values(self):
        print(self.df.isna().sum())
    
    def handle_numeric_missing_values(self, cols, strategy: Literal["mean", "median", "mode", "drop"] = "median"):
        if self.df is None:
            return
        
        for col in self.df[cols]:
            if is_numeric_dtype(self.df[col]):
                missing_ratio = self.df[col].isnull().mean()
                if missing_ratio > 0.7:
                    self.df = self.df.drop(columns=[col])
                    continue
            
                if self.df[col].isnull().sum() > 0:
                    if strategy == "mean":
                        self.df[col] = self.df[col].fillna(self.df[col].mean()).round(2)
                    elif strategy == "median":
                        self.df[col] = self.df[col].fillna(self.df[col].median()).round(2)
                    elif strategy == "mode":
                        self.df[col] = self.df[col].fillna(self.df[col].mode()[0]).round(2)
                    elif strategy == "drop":
                        self.df = self.df.dropna()

    def handle_categoric_missing_values(self, cols: str):
        if self.df is None:
            return
        for col in cols:
            if self.df[col].isna().sum() > 0:
                self.df = self.df.dropna(subset=[col])

    # Перетворіть категоріальні ознаки в числові за допомогою one-hot encoding або label encoding.
    # Масштабуйте числові ознаки за допомогою StandardScaler або MinMaxScaler.
    # Видаліть непотрібні ознаки.
    # Використовуйте ColumnTransformer і Pipeline для організації етапів підготовки даних.

    def encode_onehot(self, columns):
        for column in columns:
            if self.df[column].dtype == 'category' or self.df[column].dtype == 'object':  
                dummies = pd.get_dummies(self.df[column], prefix=column, drop_first=True)  
                self.df = pd.concat([self.df, dummies], axis=1)
                self.df.drop(column, axis=1, inplace=True)

    def scale_features(self, columns):
        for column in columns:
            if pd.api.types.is_numeric_dtype(self.df[column]):
                min_val = self.df[column].min()
                max_val = self.df[column].max()
                self.df[column] = (self.df[column] - min_val) / (max_val - min_val)
                print(f"Колонка '{column}' масштабована.")
    
    # Розбиття даних:
    # Розділіть набір даних на навчальний та тестовий набори у співвідношенні 80/20 або іншому відповідному співвідношенні.
    def split_data(self, target_col: str, drop_cols, test_size):
        X = self.df.drop(columns=drop_cols)
        y = self.df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=101)
        return X_train, X_test, y_train, y_test

data_processor = DataProcessor("./datasets/most_watched_anime_dataset_100_entries.csv")

# data_processor.data_info()

# data_processor.show_missing_values()

data_processor.handle_numeric_missing_values(cols=["Ratings"], strategy="mean")
data_processor.handle_categoric_missing_values(cols=["Anime Name"])

# data_processor.show_missing_values()


data_processor.encode_onehot(["Most Watched in Country"])
data_processor.scale_features(["Budget (in Million USD)", "Duration per Episode (minutes)"])

X_train, X_test, y_train, y_test = data_processor.split_data(
    target_col="Budget (in Million USD)",
    drop_cols=["Animation Studio Name"],
    test_size=0.2
)

print(data_processor.df["Budget (in Million USD)"])

# Вибір моделі:
# Виберіть модель машинного навчання, яка підходить для вашої задачі (класифікація або регресія).
# Використовуйте Pipeline для об'єднання етапів підготовки даних та навчання моделі.
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
numeric_features = ['Ratings', 'Number of Episodes', 'Release Year', 'Duration per Episode (minutes)']
categorical_features = ['Most Watched in Country', 'Animation Studio Name', 'Genre']

# Обробка числових і категорійних змінних
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

linear_model = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', LinearRegression())])

forest_model = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

models = {'Linear Regression': linear_model, 'Random Forest': forest_model}
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)  
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {'MAE': mae, 'RMSE': rmse, 'R²': r2}



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


