import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

logger = logging.getLogger(__name__)


class MLService:
    _instance: "MLService | None" = None
    _model: Any | None = None

    def __new__(cls) -> "MLService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._model is None:
            self._load_model()

    def _load_model(self) -> None:
        model_path = Path(__file__).parent.parent.parent / "ml" / "model_smote.pkl"
        try:
            self._model = joblib.load(model_path)
            logger.info("ML model loaded successfully from %s", model_path)
        except FileNotFoundError as exc:
            logger.error("ML model not found at %s", model_path)
            raise RuntimeError(f"ML model not found at {model_path}") from exc
        except Exception as e:
            logger.error("Failed to load ML model: %s", str(e))
            raise RuntimeError(f"Failed to load ML model: {e}") from e

    def predict(self, data: pd.DataFrame) -> tuple[int, float]:
        if self._model is None:
            raise RuntimeError("ML model not loaded")

        # Map snake_case (schema) to PascalCase (model expectation)
        mapping = {col: "".join(word.capitalize() for word in col.split("_")) for col in data.columns}
        data_mapped = data.rename(columns=mapping)

        # For some specific columns if capitalization differs from simple PascalCase
        # but based on the error message, simple PascalCase seems to be what it wants.

        probability = self._model.predict_proba(data_mapped)[0][1]
        prediction = 1 if probability >= 0.5 else 0
        return prediction, probability

    def get_feature_importance(self, data: pd.DataFrame) -> dict[str, float]:
        if self._model is None:
            raise RuntimeError("ML model not loaded")

        if hasattr(self._model, "feature_importances_"):
            importances = self._model.feature_importances_
            # Map features to PascalCase to match the model's training features
            features = ["".join(word.capitalize() for word in col.split("_")) for col in data.columns]
            return dict(zip(features, importances, strict=True))
        return {}


ml_service = MLService()
