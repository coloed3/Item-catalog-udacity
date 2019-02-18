from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    picture = Column(String(250))
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'
    """below will aloow the URLS to view a category by name not by the id given 
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)

    @property
    def serialize(self):
        """should return object in a serializable format
        if found https://stackoverflow.com/questions/17066074/modelserializer-using-model-property
        """
        return{
            'id': self.id,
            'name': self.name
        }


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    """below will aloow the URLS to view a category by name not by
        the id given 
    """
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String(250))
    category_name = Column(Integer, ForeignKey('category.name'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category_name,
        }


engine = create_engine('sqlite:///catalogsdatabase.db')
""" below function, was taken from this documentation,
PRAGMA on will allow sqlite to  enable foreign key constraints 
http://www.sqlitetutorial.net/sqlite-foreign-key/
 """


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Base.metadata.create_all(engine)
