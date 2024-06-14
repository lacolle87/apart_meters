from sqlalchemy.orm import Session
from database.models import Apartment


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
            self.logger.error(f"Error fetching apartment by name: {e}")
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
