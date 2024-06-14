from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ApartmentMixin:
    apartment_id = Column(Integer, ForeignKey('apartments.id'))


class User(Base, TimestampMixin, ApartmentMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True)
    first_name = Column(String)
    in_location = Column(Boolean)
    is_admin = Column(Boolean, default=False)


class Rate(Base, TimestampMixin, ApartmentMixin):
    __tablename__ = 'rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    electric_rate = Column(Float, nullable=False)
    water_rate = Column(Float, nullable=False)
    drainage_rate = Column(Float, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Apartment(Base, TimestampMixin):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String)
    users = relationship("User", backref="apartment", foreign_keys="[User.apartment_id]")
    rates = relationship("Rate", backref="apartment", foreign_keys="[Rate.apartment_id]")
    metrics = relationship("Metric", backref="apartment", foreign_keys="[Metric.apartment_id]")


class Metric(Base, TimestampMixin, ApartmentMixin):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    electric_usage = Column(Float, nullable=False)
    water_usage = Column(Float, nullable=False)
