import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Завантаження даних
class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            df = pd.read_csv(self.file_path)
            print("Дані успішно завантажено.")
            return df
        except FileNotFoundError:
            print(f"Помилка: файл '{self.file_path}' не знайдено.")
            return None

# 2. Розвідувальний аналіз даних (EDA)
class DataExplorer:
    def __init__(self, df):
        self.df = df

    def add_categorial_if_none(self):
        categorical_columns = self.df.select_dtypes(include=['category']).columns
        if len(categorical_columns) > 0:
            print("DataFrame вже містить категоріальні стовпці.")
        else:
            numeric_columns = self.df.select_dtypes(include=np.number).columns
            if len(numeric_columns) == 0:
                print("DataFrame не містить числових стовпців, необхідних для аналізу.")
            else:
                first_numeric_column = numeric_columns[0]
                bins = [self.df[first_numeric_column].min() - 1,
                        self.df[first_numeric_column].median(),
                        self.df[first_numeric_column].max() + 1]
                labels = ["category1", "category2"]
                categorial_column = "categorial"
                self.df[categorial_column] = pd.cut(self.df[first_numeric_column], bins=bins, labels=labels, right=False).astype('category')
                print (f"Додано стовпець з категоріальною змінною: {categorial_column}")

    def describe_data(self):
        print("Опис даних:")
        print(self.df.info())       # Інформація про типи даних та кількість непустих значень
        print(self.df.describe())   # Статистичні характеристики числових змінних

    def visualize_data(self):
        try:
            self.df.hist(figsize=(15, 12))
            plt.show()
        except:
            print("\nCannot visualize the histogram: categorical data.")

    def find_missing_values(self):
        print("\nВідсутні значення:")
        print(self.df.isnull().sum())

    def find_outliers(self, column):
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        print(f"\nВикиди в колонці '{column}':")
        print(outliers)

# 3. Обробка відсутніх значень
class MissingValueHandler:
    def __init__(self, df):
        self.df = df

    def fill_missing_values(self, columns, strategy='median'):
        for column in columns:
            if not pd.api.types.is_numeric_dtype(self.df[column]):
                continue
            if self.df[column].isnull().any():
                if strategy == 'median':
                    fill_value = self.df[column].median()
                elif strategy == 'mean':
                    fill_value = self.df[column].mean()
                elif strategy == 'mode':
                    fill_value = self.df[column].mode()[0]
                else:
                    raise ValueError("Невідома стратегія заповнення відсутніх значень.")
                self.df[column].fillna(fill_value, inplace=True)
                print(f"Відсутні значення в колонці '{column}' заповнено ({strategy}).")

# 4. Кодування категоріальних змінних
class CategoricalEncoder:
    def __init__(self, df):
        self.df = df

    def encode_onehot(self, columns):
        print(self.df.head(1))
        for column in columns:
            if self.df[column].dtype == 'category' or self.df[column].dtype == 'object':    # Перевірка, чи є змінна категоріальною
                dummies = pd.get_dummies(self.df[column], prefix=column, drop_first=True)   # drop_first для зменшення кількості колонок
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

# 5. Масштабування функцій (Min-Max Scaling)
class FeatureScaler:
    def __init__(self, df):
        self.df = df

    def scale_features(self, columns):
        for column in columns:
            if pd.api.types.is_numeric_dtype(self.df[column]):  # Перевірка, чи є змінна числовою
                min_val = self.df[column].min()
                max_val = self.df[column].max()
                self.df[column] = (self.df[column] - min_val) / (max_val - min_val)
                print(f"Колонка '{column}' масштабована.")

# 6. Розділення даних на навчальний та тестовий набір
class DataSplitter:
    def __init__(self, df, target_column):
        self.df = df
        self.target_column = target_column

    def split_data(self, test_size=0.2, random_state=42):
        # Випадкове перемішування індексів
        indices = self.df.index.tolist()
        np.random.seed(random_state)
        np.random.shuffle(indices)

        # Розділення індексів на навчальну та тестову вибірки
        split_index = int(len(indices) * (1 - test_size))
        train_indices = indices[:split_index]
        test_indices = indices[split_index:]

        # Створення навчальної та тестової вибірок
        X_train = self.df.loc[train_indices].drop(self.target_column, axis=1)
        y_train = self.df.loc[train_indices][self.target_column]
        X_test = self.df.loc[test_indices].drop(self.target_column, axis=1)
        y_test = self.df.loc[test_indices][self.target_column]

        print("Дані розділено на навчальний та тестовий набори.")
        return X_train, X_test, y_train, y_test


def process_data_titanic(file_path):
    # Завантаження даних
    data_loader = DataLoader(file_path)
    df = data_loader.load_data()

    if df is not None:
        # Розвідувальний аналіз даних (EDA)
        data_explorer = DataExplorer(df)
        data_explorer.describe_data()
        data_explorer.visualize_data()
        data_explorer.find_missing_values()
        data_explorer.find_outliers('age')

        # Обробка відсутніх значень
        missing_handler = MissingValueHandler(df)
        missing_handler.fill_missing_values(['age', 'fare'], strategy='median')

        # Кодування категоріальних змінних
        encoder = CategoricalEncoder(df)
        encoder.encode_onehot(['sex', 'embarked'])
        encoder.encode_label(['class', 'embark_town'])  # Альтернативно, label encoding

        # Масштабування функцій
        scaler = FeatureScaler(df)
        scaler.scale_features(['age', 'fare'])

        # Розділення даних на навчальний та тестовий набір
        splitter = DataSplitter(df, 'survived')
        X_train, X_test, y_train, y_test = splitter.split_data()

        # Подальша робота з даними (навчання моделі, тощо)
        print("\nГотові дані для навчання моделі:")
        print("X_train:\n", X_train.head())
        print("y_train:\n", y_train.head())
        print("X_test:\n", X_test.head())
        print("y_test:\n", y_test.head())


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    process_data_titanic(file_path=os.path.join(dir_path, "titanic.csv"))
