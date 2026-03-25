import logging
import os
from typing import Any

import mlflow

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file://./mlruns")


class MLflowService:
    def __init__(self) -> None:
        self._initialized = False
        self._init_error = None

    def _ensure_initialized(self) -> None:
        if self._initialized:
            return

        if self._init_error:
            raise self._init_error

        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            mlflow.set_experiment("retention-ai-predictions")
            self._initialized = True
            logger.info("MLflow initialized with experiment: retention-ai-predictions")
        except Exception as e:
            self._init_error = e
            logger.warning("Failed to initialize MLflow: %s", str(e))
            raise

    def log_prediction(
        self,
        user_id: int,
        prediction_id: int,
        employee_data: dict[str, Any],
        prediction: int,
        probability: float,
        latency_ms: float,
    ) -> str | None:
        try:
            self._ensure_initialized()

            with mlflow.start_run(run_name=f"prediction-{prediction_id}") as run:
                mlflow.log_param("user_id", user_id)
                mlflow.log_param("prediction_id", prediction_id)
                mlflow.log_param("prediction", prediction)

                mlflow.log_metric("churn_probability", probability)
                mlflow.log_metric("latency_ms", latency_ms)

                for key, value in employee_data.items():
                    mlflow.log_param(f"emp_{key}", value)

                mlflow.set_tag("model_type", "attrition_prediction")
                mlflow.set_tag("prediction_type", "single")

                logger.info(
                    "Logged prediction %s: user=%s, prob=%.4f, latency=%.2fms",
                    prediction_id,
                    user_id,
                    probability,
                    latency_ms,
                )

                return run.info.run_id
        except Exception as e:
            logger.warning("Failed to log prediction to MLflow: %s", str(e))
            return None

    def log_retention_plan(
        self,
        prediction_id: int,
        plan_content: list[str],
        latency_ms: float,
    ) -> str | None:
        try:
            self._ensure_initialized()

            with mlflow.start_run(run_name=f"retention-plan-{prediction_id}") as run:
                mlflow.log_param("prediction_id", prediction_id)
                mlflow.log_param("plan_actions_count", len(plan_content))

                mlflow.log_metric("plan_generation_latency_ms", latency_ms)

                for i, action in enumerate(plan_content, 1):
                    mlflow.log_param(f"action_{i}", action)

                mlflow.set_tag("model_type", "gemini-2.5-flash")
                mlflow.set_tag("prediction_type", "retention_plan")

                logger.info(
                    "Logged retention plan for prediction %s: %d actions, latency=%.2fms",
                    prediction_id,
                    len(plan_content),
                    latency_ms,
                )

                return run.info.run_id
        except Exception as e:
            logger.warning("Failed to log retention plan to MLflow: %s", str(e))
            return None


mlflow_service = MLflowService()
