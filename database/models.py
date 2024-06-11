from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    water_metrics = relationship('Metric', back_populates='user')


class Rates(Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True)
    electric_rate = Column(Float)
    water_rate = Column(Float)
    drainage = Column(Float)


class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    water_usage = Column(Float)
    electric_usage = Column(Float)
    user = relationship('User', back_populates='metrics')
