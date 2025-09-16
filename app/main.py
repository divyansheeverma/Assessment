from fastapi import FastAPI
from app.routers import employees,auth
from app.db import employees_collection


app = FastAPI(title="Employees API")

# include router
app.include_router(employees.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Welcome to Employees API"}
