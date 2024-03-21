from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from databaseUtils.sqlBase import SQLBase


class Author(declarative_base(), SQLBase):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    login = Column(String)
    email = Column(String)

    def __init__(self, name, login, email):
        self.name = name
        self.login = login
        self.email = email
