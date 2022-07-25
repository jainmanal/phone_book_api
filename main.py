
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
import app.models as models
from app.db import get_db, engine
import app.models as models
import app.schemas as schemas
from app.repositories import UserDetailRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post('/user-details', tags=["users"],response_model=schemas.UserDetail,status_code=201)
async def create_user(user_request: schemas.UserDetailCreate, db: Session = Depends(get_db)):
    
    db_user = UserDetailRepo.fetch_by_phone(db, phone=user_request.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone Number already exists!")

    return await UserDetailRepo.create(db=db, user=user_request)

@app.get('/user-details', tags=["users"],response_model=List[schemas.UserDetail])
def get_all_users(last_name: Optional[str] = None,db: Session = Depends(get_db)):
    
    if last_name:
        users =[]
        db_user = UserDetailRepo.fetch_by_last_name(db,last_name)
        users.append(db_user)
        return users
    else:
        return UserDetailRepo.fetch_all(db)


@app.get('/user-details/{user_detail_id}', tags=["users"],response_model=schemas.UserDetail)
def get_user(user_detail_id: int,db: Session = Depends(get_db)):
    
    db_user = UserDetailRepo.fetch_by_id(db,user_detail_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found with the given ID")
    return db_user

@app.delete('/user-details/{user_detail_id}', tags=["users"])
async def delete_user(user_detail_id: int,db: Session = Depends(get_db)):
    
    db_user = UserDetailRepo.fetch_by_id(db,user_detail_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found with the given ID")
    await UserDetailRepo.delete(db,user_detail_id)
    return "User deleted successfully!"

@app.put('/user-details/{user_detail_id}', tags=["users"],response_model=schemas.UserDetail)
async def update_user(user_detail_id: int,user_request: schemas.UserDetail, db: Session = Depends(get_db)):
    
    db_user = UserDetailRepo.fetch_by_id(db, user_detail_id)
    if db_user:
        update_user_encoded = jsonable_encoder(user_request)
        db_user.first_name = update_user_encoded['first_name']
        db_user.last_name = update_user_encoded['last_name']
        db_user.phone = update_user_encoded['phone']
        return await UserDetailRepo.update(db=db, user_data=db_user)
    else:
        raise HTTPException(status_code=400, detail="User not found with the given ID")
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)