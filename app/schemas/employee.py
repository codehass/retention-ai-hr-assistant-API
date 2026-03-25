from typing import Literal

from pydantic import BaseModel, Field


class EmployeeAttritionRequest(BaseModel):
    age: int = Field(..., ge=18, le=70, description="Employee age")
    job_level: int = Field(..., ge=1, le=5, description="Job level (1-5)")
    monthly_income: float = Field(..., gt=0, description="Monthly income")
    stock_option_level: int = Field(..., ge=0, le=3, description="Stock option level")
    total_working_years: int = Field(
        ..., ge=0, le=50, description="Total working years"
    )
    years_at_company: int = Field(..., ge=0, le=50, description="Years at company")
    years_in_current_role: int = Field(
        ..., ge=0, le=20, description="Years in current role"
    )
    years_with_curr_manager: int = Field(
        ..., ge=0, le=20, description="Years with current manager"
    )

    education: Literal[1, 2, 3, 4, 5] = Field(
        ...,
        description="1: Below College, 2: College, 3: Bachelor, 4: Master, 5: Doctor",
    )
    environment_satisfaction: Literal[1, 2, 3, 4] = Field(
        ..., description="1: Low, 2: Medium, 3: High, 4: Very High"
    )
    job_involvement: Literal[1, 2, 3, 4] = Field(
        ..., description="1: Low, 2: Medium, 3: High, 4: Very High"
    )
    job_satisfaction: Literal[1, 2, 3, 4] = Field(
        ..., description="1: Low, 2: Medium, 3: High, 4: Very High"
    )
    performance_rating: Literal[1, 2, 3, 4] = Field(
        ..., description="1: Low, 2: Good, 3: Excellent, 4: Outstanding"
    )
    relationship_satisfaction: Literal[1, 2, 3, 4] = Field(
        ..., description="1: Low, 2: Medium, 3: High, 4: Very High"
    )
    work_life_balance: Literal[1, 2, 3, 4] = Field(
        ..., description="1: Bad, 2: Good, 3: Better, 4: Best"
    )

    business_travel: str
    department: str
    education_field: str
    gender: str
    job_role: str
    marital_status: str
    over_time: str

    model_config = {"str_to_lower": True, "populate_by_name": True}
