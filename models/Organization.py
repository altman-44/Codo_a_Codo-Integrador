from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Organization(Base):
    __tablename__ = 'organization_accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    # employees = relationship('Employee', back_populates='organization')
    students = relationship('Student', back_populates='organization')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id