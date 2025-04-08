import pandas as pd
from pandas.api.types import is_object_dtype

class CategoricalEncoder:
    def __init__(self, df):
        self.df = df

    def encode_onehot(self, columns):
        for col in columns:
            if is_object_dtype(self.df[col]):
                dummies = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
                self.df = pd.concat([self.df, dummies], axis=1)
                self.df.drop(col, axis=1, inplace=True)
                print(f"One-hot кодування застосовано до '{col}'")
        return self.df

    def encode_label(self, columns):
        for col in columns:
            if is_object_dtype(self.df[col]):
                self.df[col] = pd.factorize(self.df[col])[0]
                print(f"Label encoding застосовано до '{col}'")
        return self.df