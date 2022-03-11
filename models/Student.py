import datetime
import os
from sqlalchemy.orm import relationship
from db.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, Date, DateTime

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    organizationId = Column(Integer, ForeignKey('organization_accounts.id'))
    organization = relationship('Organization', back_populates='students')
    originId = Column(Integer, ForeignKey('student_origins.id'), nullable=False)
    origin = relationship('StudentOrigin', back_populates='students')
    name = Column(String(os.getenv('FIELD_CHECK_NAME_LENGTH')), nullable=False)
    surname = Column(String(os.getenv('FIELD_CHECK_SURNAME_LENGTH')), nullable=False)
    entryDate = Column(Date, nullable=False)
    school = Column(String(os.getenv('FIELD_CHECK_SCHOOL_LENGTH')), nullable=True)
    observations = Column(String, nullable=True)
    phone = Column(Integer, nullable=True)
    recommendedBy = Column(String(os.getenv('FIELD_CHECK_STUDENT_RECOMMENDED_BY_LENGTH')), nullable=True)
    year = Column(String(os.getenv('FIELD_CHECK_STUDENT_YEAR_LENGTH')), nullable=False)
    yearUpdatedAt = Column(DateTime, nullable=False, onupdate=datetime.datetime.now)
    locationCountry = Column(String(os.getenv('FIELD_CHECK_COUNTRY_LENGTH')), ForeignKey('locations.country'), nullable=False)
    locationRegion = Column(String(os.getenv('FIELD_CHECK_REGION_LENGTH')), ForeignKey('locations.region'), nullable=False)
    locationCity = Column(String(os.getenv('FIELD_CHECK_CITY_LENGTH')), ForeignKey('locations.city'), nullable=False)
    # location = relationship('Location', foreign_keys="['locationCountry', 'locationRegion', 'locationCity']", back_populates='students')
    location = relationship('Location',
    primaryjoin='and_(Location.country == foreign(Student.locationCountry),'
    'Location.region == foreign(Student.locationRegion), '
    'Location.city == foreign(Student.locationCity))')
    contacts = relationship('StudentContact', back_populates='student')

    def __init__(self, organization_id, name, surname, entryDate, year, location, origin, school=None, phoneCodes=None, recommendedBy=None):
        self.organizationId = organization_id
        self.name = name
        self.surname = surname
        self.entryDate = entryDate
        self.year = year
        self.location = location
        self.origin = origin
        self.school = school
        self.phone = ''.join(phoneCodes)
        self.recommendedBy = recommendedBy
        # Falta origin, location y contacts

    def validateFields(self):
        if self.organizationId and self.name and self.surname and self.entryDate and self.year:
            return True
        return False