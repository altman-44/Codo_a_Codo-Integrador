import os
from sqlalchemy.orm import relationship
from db.connection import Base
from sqlalchemy import Column, Integer, ForeignKey, String, ForeignKey

class StudentContact(Base):
    __tablename__ = 'student_contacts'

    studentId = Column(Integer, ForeignKey('students.id'), primary_key=True)
    student = relationship('Student', back_populates='contacts')
    relationship = Column(String(os.getenv('FIELD_CHECK_STUDENT_CONTACT_RELATIONSHIP_LENGTH')), primary_key=True)
    name = Column(String(os.getenv('FIELD_CHECK_NAME_LENGTH')), nullable=False)
    phone = Column(Integer, nullable=False)