from sqlalchemy.orm import Session
from database import Employee

def get_employees(db: Session):
    return db.query(Employee).all()

def create_employee(db: Session, name: str, birthday: str):
    db_employee = Employee(name=name, birthday=birthday)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
