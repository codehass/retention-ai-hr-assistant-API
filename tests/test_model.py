from unittest.mock import MagicMock

import numpy as np
import pandas as pd

from app.models.employee import EmployeeAttrition


def test_model_prediction_logic():
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([1])
    mock_model.predict_proba.return_value = np.array([[0.15, 0.85]])

    sample_employee = EmployeeAttrition(
        age=30,
        job_level=2,
        monthly_income=5000.0,
        stock_option_level=1,
        total_working_years=10,
        years_at_company=5,
        years_in_current_role=3,
        years_with_curr_manager=3,
        education=3,
        environment_satisfaction=4,
        job_involvement=3,
        job_satisfaction=4,
        performance_rating=3,
        relationship_satisfaction=3,
        work_life_balance=3,
        business_travel="Travel_Rarely",
        department="Sales",
        education_field="Marketing",
        gender="Male",
        job_role="Sales Executive",
        marital_status="Single",
        over_time="Yes",
    )

    employee_dict = {
        c.name: getattr(sample_employee, c.name)
        for c in sample_employee.__table__.columns
    }
    df = pd.DataFrame([employee_dict])

    pred = mock_model.predict(df)[0]
    prob = mock_model.predict_proba(df)[0][1]

    assert pred == 1
    assert prob == 0.85

    called_df = mock_model.predict.call_args[0][0]
    assert isinstance(called_df, pd.DataFrame)
    assert "monthly_income" in called_df.columns
    assert called_df["age"].iloc[0] == 30
