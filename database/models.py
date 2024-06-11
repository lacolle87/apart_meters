from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True)
    first_name = Column(String)
    metrics = relationship('Metric', back_populates='user')
    apartment_id = Column(Integer, ForeignKey('appartments.id'))
    in_location = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Rates(Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    electric_rate = Column(Float)
    water_rate = Column(Float)
    drainage_rate = Column(Float)
    apartment_id = Column(Integer, ForeignKey('appartments.id'))
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Appartments(Base):
    __tablename__ = 'appartments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Metrics(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    water_usage = Column(Float)
    electric_usage = Column(Float)
    user = relationship('User', back_populates='metrics')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
