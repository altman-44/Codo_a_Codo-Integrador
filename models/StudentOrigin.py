import os
from sqlalchemy.orm import relationship
from db.connection import Base
from sqlalchemy import Column, Integer, String

ERR_MSG_ORIGIN_NAME_EMPTY = 'Debe especificar el origen del alumno'

class StudentOrigin(Base):
    __tablename__ = 'student_origins'

    id = Column(Integer, primary_key=True)
    name = Column(String(os.getenv('FIELD_CHECK_STUDENT_ORIGIN_NAME_LENGTH')), nullable=False)
    students = relationship('Student', back_populates='origin')

    def __init__(self, name):
        self.validateFields(name)
        self.name = name
        # Falta verificar si el nombre del origen ya existe

    def validateFields(self, name):
        assert name, ERR_MSG_ORIGIN_NAME_EMPTY