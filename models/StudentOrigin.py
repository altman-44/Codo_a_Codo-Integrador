import os
from sqlalchemy.orm import relationship
from db.connection import Base
from sqlalchemy import Column, Integer, String

class StudentOrigin(Base):
    __tablename__ = 'student_origins'

    id = Column(Integer, primary_key=True)
    name = Column(String(os.getenv('FIELD_CHECK_STUDENT_ORIGIN_NAME_LENGTH')), nullable=False)
    students = relationship('Student', back_populates='origin')