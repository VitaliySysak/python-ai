import pandas as pd
from data_explorer import DataExplorer
from missing_value_handler import MissingValueHandler
from categorical_encoder import CategoricalEncoder
from feature_scaler import FeatureScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import cross_val_score
import numpy as np

df = pd.read_csv("./datasets/most_watched_anime_dataset_100_entries.csv")

# Виконайте розвідувальний аналіз даних (EDA) для розуміння структури даних, виявлення відсутніх значень та викидів.
explorer = DataExplorer(df)
explorer.describe_data()
explorer.find_missing_values()
explorer.visualize_data()

outliers_ratings = explorer.find_outliers("Ratings")
outliers_budget = explorer.find_outliers("Budget (in Million USD)")
outliers_duration = explorer.find_outliers("Duration per Episode (minutes)")

# Обробіть відсутні значення (заповніть або видаліть).
missing_handler = MissingValueHandler(df)
missing_handler.fill_missing_numerics(strategy='median')
missing_handler.fill_missing_categoricals()

print("\nКількість пустих значень: ")
print(df.isnull().sum(), "\n")

# Перетворіть категоріальні ознаки в числові за допомогою one-hot encoding або label encoding.
encoder = CategoricalEncoder(df)

# One-hot encoding
df = encoder.encode_onehot(['Most Watched in Country'])

# Label encoding
df = encoder.encode_label(['Anime Name', 'Animation Studio Name', 'Genre'])

print(df.head(3))

# Масштабування
scaler = FeatureScaler(df)
df = scaler.scale_numeric()

print(df.head(3))

target_column = 'Ratings'

X = df.drop(columns=[target_column])
y = df[target_column]

# train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

pipeline = Pipeline([
    ('model', RandomForestRegressor(n_estimators=100, random_state=55))
])

# Навчання моделі
pipeline.fit(X_train, y_train)

# Передбачення на тестовому наборі
y_pred = pipeline.predict(X_test)

# Оцінка моделі
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Крос-валідація
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='r2')

print(r2, rmse, cv_scores.mean())


rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """
    Навчає модель, робить передбачення та обчислює MSE, RMSE, R².
    """
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"\nОцінка моделі: {model.__class__.__name__}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R-squared (R²): {r2:.4f}")

def model_cross_validate(model, preprocessor, X, y, cv=5):
    """
    Оцінює стабільність моделі за допомогою крос-валідації.
    """
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    scores = cross_val_score(pipeline, X, y, cv=cv, scoring='r2')
    
    print(f"\nКрос-валідація моделі: {model.__class__.__name__}")
    print(f"R² scores: {np.round(scores, 4)}")
    print(f"Середній R²: {np.mean(scores):.4f}")
    print(f"Стандартне відхилення R²: {np.std(scores):.4f}")

evaluate_model(rf_model, X_train, y_train, X_test, y_test)
model_cross_validate(rf_model, preprocessor='passthrough', X=X, y=y, cv=5)

# Нажаль у датасеті зовсім немає чітких залежностей і передбачити щось з даного набору неможливо ☹️