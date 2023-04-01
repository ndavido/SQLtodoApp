from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///todo.db",echo=False, future = True)

# Items
class Item(Base):
    __tablename__ = "items"
    itemId = Column(Integer, primary_key = True, autoincrement = True)
    owner = Column(String, ForeignKey("users.name"))
    name = Column(String, nullable = False)
    description = Column(String, nullable = True)
    timeStamp = Column(DateTime, nullable = False, default = datetime.utcnow)
    users = relationship("User", back_populates="items")
    
    
class User(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String, nullable = False)
    name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    itemId = Column(Integer, ForeignKey("items.itemId"))
    items = relationship("Item", back_populates="users")
    
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
