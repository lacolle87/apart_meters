from sqlalchemy.orm import Session
from database.models import Rate, Apartment


class RateService:
    def __init__(self, session: Session, logger):
        self.session = session
        self.logger = logger

    def get_rate_by_apartment_name(self, apartment_name: str):
        try:
            rate = (
                self.session.query(Rate)
                .join(Apartment)
                .filter(name=apartment_name)
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

            rate = Rate(
                electric_rate=electric_rate,
                water_rate=water_rate,
                drainage_rate=drainage_rate,
                apartment_id=apartment.id
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
            rate = (
                self.session.query(Rate)
                .join(Apartment)
                .filter(name=apartment_name)
                .one_or_none()
            )

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
