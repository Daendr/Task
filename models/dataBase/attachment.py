from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import declarative_base
from databaseUtils.sqlBase import SQLBase


class Attachment(declarative_base(), SQLBase):
    __tablename__ = 'attachment'

    id = Column(Integer, primary_key=True)
    content = Column(LargeBinary, nullable=False)
    content_type = Column(String, nullable=False)
    test_id = Column(Integer, nullable=False)

    def __init__(self, content, content_type, test_id):
        self.content = content
        self.content_type = content_type
        self.test_id = test_id
