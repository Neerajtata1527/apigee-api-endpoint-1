import os
from contextlib import asynccontextmanager
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Employee
from schemas import EmployeeCreate, EmployeeRead, EmployeeReplace, EmployeePatch


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convenient for this learning project. For production, use Alembic migrations.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Management API",
    description="A persistent CRUD API built with FastAPI and PostgreSQL (SQLite supported locally).",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])
def root():
    return {
        "message": "Employee Management API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["General"])
def health():
    return {"status": "ok"}


@app.post(
    "/employees",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Employees"],
)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@app.get("/employees", response_model=list[EmployeeRead], tags=["Employees"])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if skip < 0:
        raise HTTPException(status_code=400, detail="skip must be zero or greater")
    if not 1 <= limit <= 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")

    statement = select(Employee).order_by(Employee.id).offset(skip).limit(limit)
    return db.scalars(statement).all()


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeRead,
    tags=["Employees"],
)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeRead,
    tags=["Employees"],
)
def replace_employee(
    employee_id: int,
    payload: EmployeeReplace,
    db: Session = Depends(get_db),
):
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    for field, value in payload.model_dump().items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


@app.patch(
    "/employees/{employee_id}",
    response_model=EmployeeRead,
    tags=["Employees"],
)
def patch_employee(
    employee_id: int,
    payload: EmployeePatch,
    db: Session = Depends(get_db),
):
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Provide at least one field to update")

    for field, value in changes.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Employees"],
)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
