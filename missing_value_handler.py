import numpy as np

class MissingValueHandler:
    def __init__(self, df):
        self.df = df

    def fill_missing_numerics(self, strategy='median'):
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            if self.df[col].isnull().sum() > 0:
                if strategy == 'mean':
                    value = self.df[col].mean()
                elif strategy == 'mode':
                    value = self.df[col].mode()[0]
                else:
                    value = self.df[col].median()
                self.df[col] = self.df[col].fillna(value)

                print(f"Заповнено пропуски в числовій колонці '{col}' ({strategy})")

    def fill_missing_categoricals(self):
        cat_cols = self.df.select_dtypes(include='object').columns
        for col in cat_cols:
            if self.df[col].isnull().sum() > 0:
                value = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(value)
                print(f"Заповнено пропуски в категоріальній колонці '{col}' (mode)")