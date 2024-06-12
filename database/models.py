from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True)
    first_name = Column(String)
    apartment_id = Column(Integer, ForeignKey('apartments.id'))
    in_location = Column(Boolean)
    metrics = relationship('Metric', back_populates='user')
    is_admin = Column(Boolean, default=False)


class Rate(Base, TimestampMixin):
    __tablename__ = 'rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    electric_rate = Column(Float, nullable=False)
    water_rate = Column(Float, nullable=False)
    drainage_rate = Column(Float, nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartments.id'))


class Apartment(Base, TimestampMixin):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)


class Metric(Base, TimestampMixin):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    water_usage = Column(Float, nullable=False)
    electric_usage = Column(Float, nullable=False)
    user = relationship('User', back_populates='metrics')
