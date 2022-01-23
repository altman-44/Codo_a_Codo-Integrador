from sqlalchemy.sql.expression import null
from db.connection import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password