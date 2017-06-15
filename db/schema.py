from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Email(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))


class Facebook_user(Base):
    __tablename__ ='facebook_user'
    id = Column(Integer, primary_key=True)
    user_fb_id = Column(String(100), nullable=False)
    name = Column(String(20), nullable=False)
    profile_image = Column(String(250), nullable=False)
    cover_url = Column(String(250))
    profile_link = Column(String((250)))
    gender = Column(String(10))
    age = Column(Integer)
    verified = Column(Boolean)
    timezone = Column(Integer)
    update_time = Column(String(120))
    total_friends = Column(Integer)
    email_id = Column(Integer, ForeignKey('email.id'))
    email = relationship(Email)

