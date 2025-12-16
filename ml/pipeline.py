from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import pandas as pd

from sklearn.model_selection import GridSearchCV


def prepare_data(
    df, numerical_features=None, categorical_features=None, target="Attrition"
):
    df_copy = df.copy()

    categorical_features_df = df_copy[categorical_features]
    numerical_features_df = df_copy[numerical_features]
    target_df = df_copy[target]

    data_prepared = pd.concat(
        [categorical_features_df, numerical_features_df, target_df], axis=1
    )

    data_prepared[target] = data_prepared[target].map({"Yes": 1, "No": 0})

    X = data_prepared.drop(columns=[target])
    y = data_prepared[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, data_prepared
