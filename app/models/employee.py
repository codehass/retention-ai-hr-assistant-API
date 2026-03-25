from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class EmployeeAttrition(Base):
    __tablename__ = "employee_attrition"

    id = Column(Integer, primary_key=True, index=True)

    age = Column(Integer, nullable=False)
    job_level = Column(Integer, nullable=False)
    monthly_income = Column(Float, nullable=False)
    stock_option_level = Column(Integer, nullable=False)
    total_working_years = Column(Integer, nullable=False)
    years_at_company = Column(Integer, nullable=False)
    years_in_current_role = Column(Integer, nullable=False)
    years_with_curr_manager = Column(Integer, nullable=False)

    education = Column(Integer, nullable=False)
    environment_satisfaction = Column(Integer, nullable=False)
    job_involvement = Column(Integer, nullable=False)
    job_satisfaction = Column(Integer, nullable=False)
    performance_rating = Column(Integer, nullable=False)
    relationship_satisfaction = Column(Integer, nullable=False)
    work_life_balance = Column(Integer, nullable=False)

    business_travel = Column(String(50), nullable=False)
    department = Column(String(100), nullable=False)
    education_field = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=False)
    job_role = Column(String(100), nullable=False)
    marital_status = Column(String(20), nullable=False)
    over_time = Column(String(20), nullable=False)

    predictions = relationship("PredictionHistory", back_populates="employee")
