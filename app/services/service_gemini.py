from google import genai
from ..config import settings


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def gemini_service(employee, prediction, response_schema):
    prompt = f"""
        Act as an expert HR Consultant. 
        Analyze this employee profile and provide 3 concrete, operational retention actions.
        
        Context:
        - Role: {employee.JobRole}
        - Department: {employee.Department}
        - Years at Company: {employee.YearsAtCompany}
        - Churn Probability: {prediction.churn_probability * 100}%
        
        The plan must be tailored to their role and seniority. 
        Format: Return only the 3 points.
    

        Output:
        Return ONLY data that respects this schema:
        {response_schema}
        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": response_schema.model_json_schema(),
        },
    )

    return response.text
