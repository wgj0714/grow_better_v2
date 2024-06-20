from sqlalchemy.orm import Session
#from models import Plant, Comments
import models
import schemas
import uuid

# plant, comment get 함수
def get_plant(db: Session):
    return db.query(models.Plant).all()

def get_comment_by_name(db: Session, target_plant_name: str):
    return db.query(models.Comment).filter_by(target_plant_name=target_plant_name).all()

def get_plants_by_grow_stage(db: Session, grow_stage: str):
    return db.query(models.Plant).filter_by(grow_stage=grow_stage).all()
      
# create plant, comment db
def create_plant(db: Session, plant_id: str, plant_info: schemas.PlantCreate):
    db_plant = models.Plant(**plant_info.model_dump(), plant_id = str(uuid.uuid1()))
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def create_comment(db: Session, comment_id: str, comment_info: schemas.CommentCreate):
    db_comment = models.Comment(**comment_info.model_dump(), comment_id = str(uuid.uuid1()))
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment.comment, db_comment.target_plant_name

def update_grow_stage(db: Session, target_plant_name: str, mean_score: int):
    target_plant = db.query(models.Plant).filter_by(plant_name=target_plant_name).first()
    plant_score = target_plant.height
    plant_score += mean_score * 5
    if plant_score == 100:
        result = "Boddhahood"
    elif plant_score >= 81 and plant_score <= 99:
        result = "Super Strong"
    elif plant_score >= 51 and plant_score <= 80:
        result = "Strong"
    elif plant_score >= 21 and plant_score <= 50:
        result = "SoSo"
    elif plant_score >= 11 and plant_score <= 20:
        result = "Coma"
    elif plant_score >= 1 and plant_score <= 10:
        result = "Almost death"    
    elif plant_score ==0 :
        result = "Death"
    target_plant.height = plant_score
    target_plant.grow_stage = result
    db.commit()
    return f"Update {target_plant_name}'s grow_stage and height"


def delete_with_name(db: Session, plant_name: str):
    obj = db.query(models.Plant).filter_by(plant_name = plant_name).first()
    db.delete(obj)
    db.commit()
    return db
