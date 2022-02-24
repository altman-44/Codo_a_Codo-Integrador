import os
from db.connection import Base
from sqlalchemy import Column, String


class Location(Base):
    __tablename__ = 'locations'

    country = Column(String(os.getenv('FIELD_CHECK_COUNTRY_LENGTH')), primary_key=True)
    region = Column(String(os.getenv('FIELD_CHECK_REGION_LENGTH')), primary_key=True)
    city = Column(String(os.getenv('FIELD_CHECK_CITY_LENGTH')), primary_key=True, default='')