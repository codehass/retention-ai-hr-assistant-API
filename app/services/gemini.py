import logging
from typing import Any

from google import genai

from app.core.config import settings

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def gemini_service(employee: Any, prediction: Any, response_schema: type) -> str:
    prompt = f"""
        Act as an expert HR Consultant.
        Analyze this employee profile and provide 3 concrete, operational retention actions.

        Context:
        - Role: {employee.job_role}
        - Department: {employee.department}
        - Years at Company: {employee.years_at_company}
        - Churn Probability: {prediction.churn_probability * 100}%

        The plan must be tailored to their role and seniority.
        Format: Return only the 3 points.


        Output:
        Return ONLY data that respects this schema:
        {response_schema}
        """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": response_schema.model_json_schema(),
            },
        )
        return response.text
    except Exception as e:
        logger.error("Gemini API error: %s", str(e))
        raise
