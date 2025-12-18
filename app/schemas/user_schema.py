from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from typing import List


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class EmployeeAttritionRequest(BaseModel):
    Age: float
    JobLevel: int
    MonthlyIncome: float
    StockOptionLevel: int
    TotalWorkingYears: float
    YearsAtCompany: float
    YearsInCurrentRole: float
    YearsWithCurrManager: float

    Education: Literal[
        1, 2, 3, 4, 5
    ]  # 1: Below College, 2: College, 3: Bachelor, 4: Master, 5: Doctor
    EnvironmentSatisfaction: Literal[
        1, 2, 3, 4
    ]  # 1: Low, 2: Medium, 3: High, 4: Very High
    JobInvolvement: Literal[1, 2, 3, 4]  # 1: Low, 2: Medium, 3: High, 4: Very High
    JobSatisfaction: Literal[1, 2, 3, 4]  # 1: Low, 2: Medium, 3: High, 4: Very High
    PerformanceRating: Literal[
        1, 2, 3, 4
    ]  # 1: Low, 2: Good, 3: Excellent, 4: Outstanding
    RelationshipSatisfaction: Literal[
        1, 2, 3, 4
    ]  # 1: Low, 2: Medium, 3: High, 4: Very High
    WorkLifeBalance: Literal[1, 2, 3, 4]  # 1: Bad, 2: Good, 3: Better, 4: Best

    BusinessTravel: str
    Department: str
    EducationField: str
    Gender: str
    JobRole: str
    MaritalStatus: str
    OverTime: str


class RetentionPlanRequest(BaseModel):
    prediction_id: int


class RetentionPlanResponse(BaseModel):
    plan_id: int
    prediction_id: int
    retention_plan: list[str]
    status: str = "success"


class GeminiResponse(BaseModel):
    retention_plan: List[str] = Field(
        min_items=3,
        max_items=3,
    )


class RetentionPlanResponse(BaseModel):
    id: int
    prediction_id: int
    plan_content: list[str]

    model_config = ConfigDict(from_attributes=True)
