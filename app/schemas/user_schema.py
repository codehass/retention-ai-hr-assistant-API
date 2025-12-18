from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import datetime


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
