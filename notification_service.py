from sqlalchemy.orm import Session
from database import Subscription

def subscribe(db: Session, user_id: int, employee_id: int):
    if not db.query(Subscription).filter(Subscription.user_id == user_id, Subscription.employee_id == employee_id).first():
        db_subscription = Subscription(user_id=user_id, employee_id=employee_id)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return {"message": "Subscribed"}
    return {"message": "Already subscribed"}

def unsubscribe(db: Session, user_id: int, employee_id: int):
    db_subscription = db.query(Subscription).filter(Subscription.user_id == user_id, Subscription.employee_id == employee_id).first()
    if db_subscription:
        db.delete(db_subscription)
        db.commit()
        return {"message": "Unsubscribed"}
    return {"message": "Not subscribed"}

def get_subscribers(db: Session, employee_id: int):
    return db.query(Subscription).filter(Subscription.employee_id == employee_id).all()
