from unittest.mock import MagicMock

import numpy as np
import pandas as pd

from app.models.employee_attrition import EmployeeAttrition


def test_model_prediction_logic():
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([1])
    mock_model.predict_proba.return_value = np.array([[0.15, 0.85]])

    sample_employee = EmployeeAttrition(
        Age=30.0,
        JobLevel=2,
        MonthlyIncome=5000.0,
        StockOptionLevel=1,
        TotalWorkingYears=10.0,
        YearsAtCompany=5.0,
        YearsInCurrentRole=3.0,
        YearsWithCurrManager=3.0,
        Education=3,
        EnvironmentSatisfaction=4,
        JobInvolvement=3,
        JobSatisfaction=4,
        PerformanceRating=3,
        RelationshipSatisfaction=3,
        WorkLifeBalance=3,
        BusinessTravel="Travel_Rarely",
        Department="Sales",
        EducationField="Marketing",
        Gender="Male",
        JobRole="Sales Executive",
        MaritalStatus="Single",
        OverTime="Yes",
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
    assert "MonthlyIncome" in called_df.columns
    assert called_df["Age"].iloc[0] == 30.0
