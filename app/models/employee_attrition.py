from sqlalchemy import Column, Integer, Float, String
from ..db.database import Base


class EmployeeAttrition(Base):
    __tablename__ = "employee_attrition"

    id = Column(Integer, primary_key=True, index=True)

    Age = Column(Float, nullable=False)
    JobLevel = Column(Integer, nullable=False)
    MonthlyIncome = Column(Float, nullable=False)
    StockOptionLevel = Column(Integer, nullable=False)
    TotalWorkingYears = Column(Float, nullable=False)
    YearsAtCompany = Column(Float, nullable=False)
    YearsInCurrentRole = Column(Float, nullable=False)
    YearsWithCurrManager = Column(Float, nullable=False)

    Education = Column(Integer, nullable=False)
    EnvironmentSatisfaction = Column(Integer, nullable=False)
    JobInvolvement = Column(Integer, nullable=False)
    JobSatisfaction = Column(Integer, nullable=False)
    PerformanceRating = Column(Integer, nullable=False)
    RelationshipSatisfaction = Column(Integer, nullable=False)
    WorkLifeBalance = Column(Integer, nullable=False)

    BusinessTravel = Column(String, nullable=False)
    Department = Column(String, nullable=False)
    EducationField = Column(String, nullable=False)
    Gender = Column(String, nullable=False)
    JobRole = Column(String, nullable=False)
    MaritalStatus = Column(String, nullable=False)
    OverTime = Column(String, nullable=False)
