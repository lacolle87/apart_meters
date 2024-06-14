from sqlalchemy.orm import Session
from database.models import User, Metric


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

            if not user:
                self.logger.error(f"User with chat_id {chat_id} not found.")
                return None

            metric = Metric(
                user_id=user.id,
                water_usage=water,
                electric_usage=electricity,
                apartment_id=user.apartment
            )
            self.session.add(metric)
            self.session.commit()
            return metric
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error adding metrics: {e}")
            return None
