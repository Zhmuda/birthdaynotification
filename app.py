from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt
import auth_service
import employee_service
import notification_service
import database

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    password: str

class Employee(BaseModel):
    name: str
    birthday: str

class Subscription(BaseModel):
    user_id: int
    employee_id: int

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
async def login(user: User, db: Session = Depends(get_db)):
    if auth_service.authenticate_user(db, user.username, user.password):
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@app.get("/employees")
async def get_employees(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return employee_service.get_employees(db)

@app.post("/employees")
async def create_employee(employee: Employee, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return employee_service.create_employee(db, employee.name, employee.birthday)

@app.post("/subscribe")
async def subscribe(subscription: Subscription, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return notification_service.subscribe(db, subscription.user_id, subscription.employee_id)

@app.post("/unsubscribe")
async def unsubscribe(subscription: Subscription, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return notification_service.unsubscribe(db, subscription.user_id, subscription.employee_id)
