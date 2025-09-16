from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Common fields
class EmployeeBase(BaseModel):
    name: Optional[str]
    department: Optional[str]
    salary: Optional[float]
    joining_date: Optional[date]   # accepts "YYYY-MM-DD"
    skills: Optional[List[str]]

# Schema for creating a new employee
class EmployeeCreate(EmployeeBase):
    employee_id: str = Field(..., example="E123")

# Schema for updating employee (all fields optional)
class EmployeeUpdate(EmployeeBase):
    pass

# Schema for returning data (with MongoDB id included)
class EmployeeOut(EmployeeCreate):
    id: Optional[str]
