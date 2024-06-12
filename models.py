from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine
import uuid

'''

DB Tables

'''



class Plant(Base):
    pass 

class Comments(Base):
    pass




# Create all tables in the database
Base.metadata.create_all(bind=engine)