import os
from db.connection import Base
from sqlalchemy import Column, String

CITY_DEFAULT_VALUE = ''

class Location(Base):
    __tablename__ = 'locations'

    country = Column(String(os.getenv('FIELD_CHECK_COUNTRY_LENGTH')), primary_key=True)
    region = Column(String(os.getenv('FIELD_CHECK_REGION_LENGTH')), primary_key=True)
    city = Column(String(os.getenv('FIELD_CHECK_CITY_LENGTH')), primary_key=True, default='')

    def __init__(self, country, region, city=CITY_DEFAULT_VALUE):
        self.country = country
        self.region = region
        self.city = city