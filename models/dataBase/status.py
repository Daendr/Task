from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class Status(declarative_base()):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
