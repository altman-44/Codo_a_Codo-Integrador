from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Employee(Base):
    # __tablename__ = 'employee_accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    area = Column(String)
    profile_img = Column(String)
    organization_id = Column(Integer, ForeignKey('organization_accounts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    organization = relationship('Organization', back_populates='employees')

    def __init__(self, name, surname, organization_id, user_id, area=None):
        self.name = name
        self.surname = surname
        self.organization_id = organization_id
        self.user_id = user_id
        if area:
            self.area = area