from database.models import Metric


class MetricRepository:
    def __init__(self, session, logger):
        self.logger = logger
        self.session = session

    def get_metrics_for_user(self, user_id):
        try:
            return self.session.query(Metric.water_usage, Metric.electric_usage).filter_by(user_id=user_id).all()
        except Exception as e:
            self.logger.error(f"Error fetching metrics: {e}")
            return []

    def add_metrics_for_user(self, user_id, water, electricity):
        try:
            metric = Metric(user_id=user_id, water_usage=water, electric_usage=electricity)
            self.session.add(metric)
            self.session.commit()
            return water, electricity
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error adding metrics: {e}")
            return None
