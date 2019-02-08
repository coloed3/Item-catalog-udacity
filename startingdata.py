from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User, engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

""" 
creating the fake data for our database, working on collecting descriptions
sports 
"""
category1 = Category(id=1, name='')
category2 = Category(id=2, name='')
category3 = Category(id=3, name='')
category4 = Category(id=4, name='')
category5 = Category(id=5, name='')
category6 = Category(id=6, name='')
category7= Category(id=7, name='')
category8 = Category(id=8, name='')
category9 = Category(id=9, name='')
category10 = Category(id=10, name='')
category11 = Category(id=11, name='')


session.add(category1)
session.add(category2)
session.add(category3)
session.add(category4)
session.add(category5)
session.add(category6)
session.add(category7)
session.add(category8)
session.add(category9)
session.add(category10)
session.add(category11)