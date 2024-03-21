from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base


class Session(declarative_base()):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    session_key = Column(String)
    created_time = Column(DateTime)
    build_number = Column(Integer)
