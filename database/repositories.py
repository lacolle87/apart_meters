from database.models import WaterMetric


class WaterMetricRepository:
    def __init__(self, session):
        self.session = session

    def get_metrics_for_user(self, user_id):
        try:
            return self.session.query(WaterMetric.amount, WaterMetric.unit).filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error fetching metrics: {e}")
            return []

    def add_metrics_for_user(self, user_id, amount, unit):
        try:
            metric = WaterMetric(user_id=user_id, amount=amount, unit=unit)
            self.session.add(metric)
            self.session.commit()
            return amount, unit
        except Exception as e:
            self.session.rollback()
            print(f"Error adding metrics: {e}")
            return None
