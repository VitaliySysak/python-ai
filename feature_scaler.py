import numpy as np
from sklearn.preprocessing import MinMaxScaler

class FeatureScaler:
    def __init__(self, df):
        self.df = df

    def scale_numeric(self):
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        scaler = MinMaxScaler()
        self.df[numeric_cols] = scaler.fit_transform(self.df[numeric_cols])
        print(f"Масштабовано {len(numeric_cols)} числових ознак методом Min-Max Scaling.")
        return self.df