from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker,relationship,backref

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, String, Float
import os
# Replace 'sqlite:///rfg.db' with your path to database
#psql -h localhost -U postgres intuitionmachine
PROJECT_ROOT= os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(PROJECT_ROOT,'/Flask-Graphene-SQLAlchemy/test.db'))
print(SQLALCHEMY_DATABASE_URI)
engine = create_engine('postgresql://postgres:admin@localhost/aimarket')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	email = Column(Text)
	username = Column(Text)


class Category(Base):
	__tablename__="category"
	id = Column(Integer, primary_key=True)
	name = Column(Text)

class Product(Base):
	__tablename__="product"
	id=Column(Integer, primary_key=True)
	name = Column(Text)
	description=Column(Text)
	author_id = Column(Integer,ForeignKey('users.id'))
	author = relationship(User,backref=backref("products",uselist=True,cascade='delete,all'))
	added_on = Column(DateTime,default=func.now())
	category_id = Column(Integer,ForeignKey('category.id'))
	category=relationship(Category,backref=backref("products",uselist=True,cascade='delete,all'))

class Offer(Base):
	__tablename__="offer"
	id=Column(Integer,primary_key=True)
	amount = Column(Float)
	offerdescription = Column(Text)
	product_id = Column(Integer,ForeignKey('product.id'))
	product=relationship(Product,backref=backref("offers",uselist=True,cascade='delete,all'))	
	user_id = Column(Integer,ForeignKey('users.id'))
	user=relationship(User,backref=backref("offers",uselist=True,cascade='delete,all'))

