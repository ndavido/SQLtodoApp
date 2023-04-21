#
# Name: Dawid Nalepa
# ID: 2209302
#

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///todo.db", echo=False, future=True)

#
# Items
#

class Item(Base):
    __tablename__ = "items"
    itemId = Column(Integer, primary_key=True, autoincrement=True)

    owner = Column(String, ForeignKey("users.userId"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timeStamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    sharedUser = Column(String, ForeignKey("users.userId"),
                        nullable=True, default=None)

    users = relationship("User", secondary="useritem",
                         back_populates="items", single_parent=True)

#
# Users
#

class User(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    sharedNotes = Column(Integer, ForeignKey("items.itemId"), nullable=True, default=None)

    items = relationship("Item", secondary="useritem",
                         back_populates="users", single_parent=True)

#
# User Items
#

class UserItem(Base):
    __tablename__ = "useritem"
    userId = Column(Integer, ForeignKey("users.userId"), primary_key=True)
    itemId = Column(Integer, ForeignKey("items.itemId"), primary_key=True)
    
    is_owner = Column(Boolean, nullable=False, default=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
