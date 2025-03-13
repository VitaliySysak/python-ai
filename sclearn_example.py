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

def show_df_info(df, col_for_hist=None):
    print(df.head())
    print(df.info())
    print(df.describe())
    print(df.columns.to_list())
    if col_for_hist:
        sns.histplot(df[col_for_hist])
        plt.show()

def clean_category_column(df, cat_to_update, freq=5):
    counts = df[cat_to_update].value_counts()
    categories_to_remove = counts[counts < freq].index
    df = df[~df[cat_to_update].isin(categories_to_remove)]
    return df

def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"Модель: {model.__class__.__name__}")
    print(f'Mean Squared Error: {mse}')
    print(f'Root Mean Squared Error: {rmse}')
    print(f'R-squared: {r2}')

def model_cross_validate(model, preprocessor, X, y):
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('model', model)])
    scores = cross_val_score(pipeline, X, y, cv=5, scoring='r2', error_score='raise')
    print("\nКрос-валідація моделі:")
    print(f"R2 scores: {scores}")
    print(f"Середній R2: {np.mean(scores)}")
    print(f"Стандартне відхилення R2: {np.std(scores)}")


file_name = "USA_cars_datasets.csv"
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, file_name)

df = pd.read_csv(file_path)
# ['Unnamed: 0', 'price', 'brand', 'model', 'year', 'title_status', 'mileage', 'color', 'vin', 'lot', 'state', 'country', 'condition']
df.drop(['Unnamed: 0', "title_status", "vin", "lot", "state", "country", "condition"], axis=1, inplace=True)
numerical_cols = df.select_dtypes(include=np.number).columns
categorical_cols = df.select_dtypes(include='object').columns

for col in categorical_cols:
    df = clean_category_column(df, col)

target_col = "price"
numerical_cols = numerical_cols.drop(target_col)
X = df.drop(target_col, axis=1)
y = df[target_col]
show_df_info(df, target_col)

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),       # MinMaxScaler(), RobustScaler()
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(sparse_output=True, handle_unknown='ignore'))
])
# TODO: Comment prev. element and uncomment the next lines to use LabelEncoding
# categorical_transformer = SimpleImputer(strategy='most_frequent')
# le = LabelEncoder()
# for col in categorical_cols:
#     X[col] = le.fit_transform(X[col])

preprocessor = ColumnTransformer(transformers=[
    ('num', numerical_transformer, numerical_cols),
    ('cat', categorical_transformer, categorical_cols)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)
print(X_train_transformed[0])

models = [
    RandomForestRegressor(n_estimators=100, random_state=42),
    LinearRegression(),
]

model = models[1]
evaluate_model(model, X_train_transformed, y_train, X_test_transformed, y_test)
model_cross_validate(model, preprocessor, X, y)
