import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


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


def model_pipeline(num_list, cat_list, model):

    numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])

    categorical_transformer = Pipeline(
        steps=[("encoder", OneHotEncoder(handle_unknown="ignore"))]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_list),
            ("cat", categorical_transformer, cat_list),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def evaluate_classifier(model, X_test, y_test):
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="binary")
    recall = recall_score(y_test, y_pred, average="binary")
    f1 = f1_score(y_test, y_pred, average="binary")

    return accuracy, precision, recall, f1


def train_and_evaluate(
    model_type,
    X_train,
    y_train,
    X_test,
    y_test,
    numerical_features,
    categorical_features,
):
    if model_type == "logistic":
        model = LogisticRegression(random_state=42, max_iter=1000)
    elif model_type == "randomForest":
        model = RandomForestClassifier(random_state=42)
    elif model_type == "gradientBoosting":
        model = GradientBoostingClassifier(random_state=42)
    else:
        raise ValueError("Invalid model type")

    pipeline = model_pipeline(numerical_features, categorical_features, model)
    pipeline.fit(X_train, y_train)

    return evaluate_classifier(pipeline, X_test, y_test)


def train_with_grid_search(
    model_type,
    X_train,
    y_train,
    X_test,
    y_test,
    numerical_features,
    categorical_features,
):
    param_grid_logistic = {
        "model__C": [0.1, 1, 10],
        "model__penalty": ["l2"],
        "model__solver": ["lbfgs"],
    }

    param_grid_rf = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 10, 20],
        "model__min_samples_split": [2, 5],
    }

    param_grid_gb = {
        "model__n_estimators": [100, 200],
        "model__learning_rate": [0.05, 0.1],
        "model__max_depth": [3, 5],
    }

    if model_type == "logistic":
        model = LogisticRegression(random_state=42, max_iter=1000)
        param_grid = param_grid_logistic

    elif model_type == "randomForest":
        model = RandomForestClassifier(random_state=42)
        param_grid = param_grid_rf

    elif model_type == "gradientBoosting":
        model = GradientBoostingClassifier(random_state=42)
        param_grid = param_grid_gb

    else:
        raise ValueError("Invalid model type")

    pipeline = model_pipeline(numerical_features, categorical_features, model)

    grid_search = GridSearchCV(
        pipeline, param_grid, cv=5, n_jobs=-1, scoring="accuracy"
    )

    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_score = grid_search.best_score_

    return evaluate_classifier(best_model, X_test, y_test), best_score
