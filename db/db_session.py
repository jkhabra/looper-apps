from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schema import Email, Facebook_user, Base
import os

def get_session():
    engine = create_engine('sqlite:///db/facebook.db')
    print(os.path.exists('db/facebook.db'))

    if os.path.exists('db/facebook.db'):
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session
    else:
        Base.metadata.create_all(engine)
        return  get_session()
