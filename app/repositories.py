
from sqlalchemy.orm import Session

from . import models

from . import schemas


class UserDetailRepo:
    
 async def create(db: Session, user: schemas.UserDetailCreate):
        db_user = models.User_detail(first_name=user.first_name,last_name=user.last_name,phone=user.phone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
 def fetch_by_id(db: Session,_id):
     return db.query(models.User_detail).filter(models.User_detail.id == _id).first()
 
 def fetch_by_last_name(db: Session,last_name):
     return db.query(models.User_detail).filter(models.User_detail.last_name == last_name).first()

 def fetch_by_phone(db: Session,phone):
     return db.query(models.User_detail).filter(models.User_detail.phone == phone).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.User_detail).order_by("last_name").offset(skip).limit(limit).all()
 
 async def delete(db: Session,user_detail_id):
     db_user= db.query(models.User_detail).filter_by(id=user_detail_id).first()
     db.delete(db_user)
     db.commit()
     
     
 async def update(db: Session,user_data):
    updated_user = db.merge(user_data)
    db.commit()
    return updated_user
