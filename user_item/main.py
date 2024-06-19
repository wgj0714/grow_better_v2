from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal
import models, crud, schemas
from rate_comments import CommentRater


app = FastAPI()

# Allow CORS for all origins (for simplicity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/")
def read_root():
    return {"message": "Welcome to the Plant Comment API"}

@app.post("/users/{user_id}/info")# response_model=schemas.Item)
def create_user_info(user_id: int, user_info: schemas.UserCreate, db: Session= Depends(get_db)):
    return crud.create_user_info(db=db, user_info=user_info, user_id=user_id)

@app.post("/users/{user_id}/items")# response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session= Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/users/{user_id}")
def get_users(db:Session=Depends(get_db)):
    return crud.get_user(db=db)

@app.get("/users/{user_email}")
def get_user_from_email(user_email: str, db:Session=Depends(get_db)):
    return crud.get_user_by_email(db=db, email=user_email)

@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int, db:Session=Depends(get_db)):
    crud.delete_with_id(db=db, user_id=user_id)
    return "sucessful_delete"


# @app.post("/plants/", response_model=schemas.PlantCreate)
# def create_plant(plant: schemas.PlantCreate, db: Session = Depends(get_db)):
#     pass

# @app.post("/plants/comment/")
# def comment_on_plant(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
#     pass
    
# @app.get("/plants/status/{plant_name}", response_model=schemas.Plant)
# def get_plant_status(plant_name: str, db: Session = Depends(get_db)):
#     pass


# @app.delete("/plants/status/{plant_name}")
# def delete_plant(plant_name: str, db: Session = Depends(get_db)):
#     pass

# @app.get("/plants/comments/{plant_name}", response_model=list[schemas.Comment])
# def get_comments_by_plant(plant_name: str, db: Session = Depends(get_db)):
#     pass

# @app.get("/plants/all", response_model=list[schemas.Plant])
# def get_all_plants(db: Session = Depends(get_db)):
#     pass

# @app.get("/plants/growth_stage/{growth_stage}", response_model=list[schemas.Plant])
# def get_plants_by_growth_stage(growth_stage: str, db: Session = Depends(get_db)):
#     pass

