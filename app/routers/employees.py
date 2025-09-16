from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime, date
from fastapi.encoders import jsonable_encoder
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.db import employees_collection
from typing import Optional

router = APIRouter(prefix="/employees", tags=["employees"])
# Helper to convert MongoDB doc
def doc_to_employee(doc: dict) -> dict:
    if not doc:
        
        return None
    doc["id"] = str(doc["_id"])
    doc.pop("_id")
    if isinstance(doc.get("joining_date"), (datetime, date)):
        doc["joining_date"] = doc["joining_date"].strftime("%Y-%m-%d")
    return doc

def to_datetime(d: Optional[date]) -> Optional[datetime]:
    if d:
        return datetime.combine(d, datetime.min.time())
    return None

@router.post("/", response_model=EmployeeOut, status_code=201)
async def create_employee(emp: EmployeeCreate):
    if await employees_collection.find_one({"employee_id": emp.employee_id}):
        raise HTTPException(status_code=400, detail="employee_id already exists")
    doc = jsonable_encoder(emp)
    if emp.joining_date:
        doc["joining_date"] = to_datetime(emp.joining_date)
    result = await employees_collection.insert_one(doc)
    new_doc = await employees_collection.find_one({"_id": result.inserted_id})
    return doc_to_employee(new_doc)

@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee(employee_id: str):
    doc = await employees_collection.find_one({"employee_id": employee_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Employee not found")
    return doc_to_employee(doc)

@router.put("/{employee_id}", response_model=EmployeeOut)
async def update_employee(employee_id: str, emp: EmployeeUpdate):
    update_data = emp.dict(exclude_unset=True)
    if "joining_date" in update_data:
        update_data["joining_date"] = to_datetime(update_data["joining_date"])
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")
    result = await employees_collection.update_one({"employee_id": employee_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    doc = await employees_collection.find_one({"employee_id": employee_id})
    return doc_to_employee(doc)

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    result = await employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Deleted successfully"}

@router.get("/")
async def list_employees(department: Optional[str] = Query(None)):
    query = {}
    if department:
        query["department"] = department
    cursor = employees_collection.find(query).sort("joining_date", -1)
    results = [doc_to_employee(doc) async for doc in cursor]
    return results
