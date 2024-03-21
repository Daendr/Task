from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from databaseUtils.sqlBase import SQLBase


class Project(declarative_base(), SQLBase):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
