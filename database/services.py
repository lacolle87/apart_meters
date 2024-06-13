from sqlalchemy.orm import Session
from database.models import User, Rate, Apartment, Metric


class UserService:
    def __init__(self, session: Session, logger):
        self.session = session
        self.logger = logger

    def get_user_by_chat_id(self, chat_id: int):
        try:
            return self.session.query(User).filter_by(chat_id=chat_id).one_or_none()
        except Exception as e:
            self.logger.error(f"Error fetching user by chat_id: {e}")
            return None

    def add_user(self, chat_id: int, username: str, first_name: str, apartment_id: int, in_location: bool):
        try:
            user = User(
                chat_id=chat_id,
                username=username,
                first_name=first_name,
                apartment_id=apartment_id,
                in_location=in_location,
            )
            self.session.add(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error adding user: {e}")
            return None

    def make_admin(self, chat_id: int):
        try:
            user = self.get_user_by_chat_id(chat_id)
            if user:
                user.is_admin = True
                self.session.commit()
                return user
            else:
                self.logger.error(f"User with chat_id {chat_id} not found")
                return None
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error making user admin: {e}")
            return None

    def remove_admin(self, chat_id: int):
        try:
            user = self.get_user_by_chat_id(chat_id)
            if user:
                user.is_admin = False
                self.session.commit()
                return user
            else:
                self.logger.error(f"User with chat_id {chat_id} not found")
                return None
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error removing admin from user: {e}")
            return None


class RateService:
    def __init__(self, session: Session, logger):
        self.session = session
        self.logger = logger

    def get_rate_by_apartment_name(self, apartment_name: str):
        try:
            apartment = self.session.query(Apartment).filter_by(name=apartment_name).one_or_none()

            if not apartment:
                self.logger.error(f"Apartment with name {apartment_name} not found")
                return None

            apartment_id = apartment.id

            rate = (
                self.session.query(Rate)
                .join(Apartment)
                .filter(Apartment.id == apartment_id)
                .one_or_none()
            )

            if not rate:
                self.logger.info(f"No rate found for apartment name: {apartment_name}")

            return rate
        except Exception as e:
            self.logger.error(f"Error fetching rate by apartment name: {e}")
            return None

    def add_rate(self, electric_rate: float, water_rate: float, drainage_rate: float, apartment_name: str):
        try:
            apartment = self.session.query(Apartment).filter_by(name=apartment_name).one_or_none()

            if not apartment:
                self.logger.error(f"Apartment with name {apartment_name} not found")
                return None

            apartment_id = int(apartment.id)

            rate = Rate(
                electric_rate=electric_rate,
                water_rate=water_rate,
                drainage_rate=drainage_rate,
                apartment_id=apartment_id
            )
            self.session.add(rate)
            self.session.commit()
            return rate
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error adding rate: {e}")
            return None

    def update_rate(self, apartment_name: str, electric_rate: float = None, water_rate: float = None,
                    drainage_rate: float = None):
        try:
            apartment = self.session.query(Apartment).filter_by(name=apartment_name).one_or_none()
            if not apartment:
                self.logger.error(f"Apartment with name {apartment_name} not found")
                return None

            rate = self.session.query(Rate).filter_by(apartment_id=apartment.id).one_or_none()
            if not rate:
                self.logger.error(f"Rate for apartment {apartment_name} not found")
                return None

            if electric_rate is not None:
                rate.electric_rate = electric_rate
            if water_rate is not None:
                rate.water_rate = water_rate
            if drainage_rate is not None:
                rate.drainage_rate = drainage_rate

            self.session.commit()
            return rate
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error updating rate: {e}")
            return None


class ApartmentService:
    def __init__(self, session: Session, logger):
        self.session = session
        self.logger = logger

    def get_apartment_by_id(self, apartment_id: int):
        try:
            return self.session.query(Apartment).filter_by(id=apartment_id).one_or_none()
        except Exception as e:
            self.logger.error(f"Error fetching apartment by id: {e}")
            return None

    def get_apartment_by_name(self, apartment_name: str):
        try:
            return self.session.query(Apartment).filter_by(name=apartment_name).one_or_none()
        except Exception as e:
            self.logger.error(f"Error fetching apartment by id: {e}")
            return None

    def add_apartment(self, name: str, address: str):
        try:
            apartment = Apartment(
                name=name,
                address=address
            )
            self.session.add(apartment)
            self.session.commit()
            return apartment
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error adding apartment: {e}")
            return None


class MetricService:
    def __init__(self, session: Session, logger):
        self.session = session
        self.logger = logger

    def get_metrics_for_user(self, user_id: int):
        try:
            return self.session.query(Metric.water_usage, Metric.electric_usage).filter_by(user_id=user_id).all()
        except Exception as e:
            self.logger.error(f"Error fetching metrics: {e}")
            return []

    def add_metrics_for_user(self, chat_id: int, water: float, electricity: float):
        try:
            user = self.session.query(User).filter_by(chat_id=chat_id).first()
            user_id = int(user.id)

            if user:
                metric = Metric(
                    user_id=user_id,
                    water_usage=water,
                    electric_usage=electricity
                )
                self.session.add(metric)
                self.session.commit()
                return metric
            else:
                self.logger.error(f"User with chat_id {chat_id} not found.")
                return None

        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error adding metrics: {e}")
            return None
