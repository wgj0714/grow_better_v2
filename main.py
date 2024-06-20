from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal
import models, crud, schemas
from rate_comments import CommentRater
import rate_comments
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')

with open("./prompt.txt", "r") as file:
    prompt = file.read()

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

@app.post("/users/{plant_id}/info")# response_model=schemas.Item)
def create_plant_info(plant_info: schemas.PlantCreate, db: Session= Depends(get_db)):
    return crud.create_plant(db=db, plant_info=plant_info, plant_id=str(uuid.uuid1()))

# @app.post("/users/{comment_id}/items")# response_model=schemas.Item)
# def create_comment_info(comment_id: int, comment_info: schemas.CommentCreate, db: Session= Depends(get_db)):
#     return crud.create_comment(db=db, comment_info=comment_info, comment_id=comment_id)

@app.post("/users/update/{comment_id}")
def update_plant_score(comment_info: schemas.CommentCreate, db: Session=Depends(get_db)):
    comment, target_plant_name = crud.create_comment(db=db, comment_info = comment_info, 
    comment_id=str(uuid.uuid1()))
    rater = CommentRater(comment, prompt, OPEN_API_KEY)
    result = rater.create_score()
    crud.update_grow_stage(db=db, target_plant_name=target_plant_name, mean_score=result)
    return "sucessful_making_comment_and_update_score"

@app.get("/users/all_plants")
def get_all_plants(db:Session=Depends(get_db)):
    return crud.get_plant(db=db)

@app.get("/users/get/{target_plant_name}")
def get_comment_by_plant_name(target_plant_name: str, db:Session=Depends(get_db)):
    return crud.get_comment_by_name(target_plant_name=target_plant_name, db=db)

@app.delete("/users/delete/{plant_name}")
def delete_plant(plant_name: str, db:Session=Depends(get_db)):
    crud.delete_with_name(db=db, plant_name=plant_name)
    return "sucessful_delete"

@app.get("/users/get/{grow_stage}")
def get_grow_stage(grow_stage: str, db:Session=Depends(get_db)):
    return crud.get_plants_by_grow_stage(db=db, grow_stage=grow_stage)

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

