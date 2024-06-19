from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from database import Base, engine
import uuid
import database

class Plant(Base):
    __tablename__ = "plants"

    plant_id = Column(String, primary_key=True) 
    plant_name = Column(String, index=True)
    species = Column(String, index=True)
    grow_stage = Column(String, index=True)
    height = Column(Integer, index=True)
    
    comments = relationship("Comment", back_populates="plants")


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(String, primary_key=True)
    target_plant_name = Column(String, ForeignKey("plants.plant_name"))
    comment = Column(String)
    mean_score = Column(Integer, index = True)
    time_stamp = Column(DateTime(timezone=True))
        
    plants = relationship("Plant", back_populates="comments")

# Create all tables in the database
Base.metadata.create_all(bind=engine)