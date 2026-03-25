from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from pydantic import BaseModel

from app.services.gemini import gemini_service


class RetentionPlan(BaseModel):
    action_1: str
    action_2: str
    action_3: str


@patch("app.services.gemini.client.models.generate_content")
def test_gemini_service_hr_retention(mock_generate):
    mock_response = MagicMock()
    mock_response.text = """
    {
        "action_1": "Offer a senior mentorship role.",
        "action_2": "Increase professional development budget by 15%.",
        "action_3": "Schedule a skip-level meeting to discuss career path."
    }
    """
    mock_generate.return_value = mock_response

    mock_employee = SimpleNamespace(
        job_role="Software Engineer", department="IT", years_at_company=3
    )
    mock_prediction = SimpleNamespace(churn_probability=0.45)

    result = gemini_service(
        employee=mock_employee,
        prediction=mock_prediction,
        response_schema=RetentionPlan,
    )

    assert "mentorship" in result
    assert "professional development" in result
    mock_generate.assert_called_once()

    _, kwargs = mock_generate.call_args
    assert "Software Engineer" in kwargs["contents"]
    assert "45.0%" in kwargs["contents"]
