from sqlalchemy.orm import Session
#from models import Plant, Comments
import models
import schemas
import uuid

def get_user(db: Session):
    return db.query(models.User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user_info(db: Session, user_info: schemas.UserCreate, user_id: int):
    db_user = models.User(**user_info.dict(), id = user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id = user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_with_id(db: Session, user_id: int):
    obj = db.query(models.User).filter_by(id = user_id).first()
    db.delete(obj)
    db.commit()
    return db