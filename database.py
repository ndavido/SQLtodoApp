from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey

Base = declarative_base()
engine = create_engine("sqlite:///todo.db",echo=False, future = True)

# Items
class Item(Base):
    __tablename__ = "items"
    itemId = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String)
    
class User(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String, nullable = False)
    name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
