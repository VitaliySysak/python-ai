import numpy as np
import matplotlib.pyplot as plt

class DataExplorer:
    def __init__(self, df):
        self.df = df

    def describe_data(self):
        print("Інформація про дані:")
        print(self.df.info())
        print("\nОпис числових змінних:")
        print(self.df.describe())

    def find_missing_values(self):
        print("\nКількість відсутніх значень по кожній колонці:")
        print(self.df.isnull().sum())

    def visualize_data(self):
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        self.df[numeric_cols].hist(figsize=(15, 10))
        plt.suptitle("Гістограми числових змінних", fontsize=16)
        plt.tight_layout()
        plt.show()

    def find_outliers(self, column):
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        print(f"\nЗнайдено {len(outliers)} викидів у колонці '{column}'")
        return outliers