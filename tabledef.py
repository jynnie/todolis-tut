from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True)
    username    = Column(String)
    email       = Column(String)
    password    = Column(String)
    todos       = relationship('Todo', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Todo(Base):
    __tablename__ = "todos"

    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey('users.id'))
    content     = Column(String)

Base.metadata.create_all(engine)
