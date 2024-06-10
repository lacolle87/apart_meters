from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Database:
    _engine = None
    _session = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine('sqlite:///water_metrics.db')
        return self._engine

    @property
    def session(self):
        if self._session is None:
            self._session = sessionmaker(bind=self.engine)
        return self._session

    @property
    def get_metrics(self):
        def get_metrics_for_user(user_id):
            try:
                session = self.session()
                metrics = session.query(WaterMetric.amount, WaterMetric.unit).filter_by(user_id=user_id).all()
                return metrics
            except Exception as e:
                print(f"Error fetching metrics: {e}")
                return []

        return get_metrics_for_user

    @property
    def add_metrics(self):
        def add_metrics_for_user(user_id, amount, unit):
            try:
                session = self.session()
                metric = WaterMetric(user_id=user_id, amount=amount, unit=unit)
                session.add(metric)
                session.commit()
                return amount, unit
            except Exception as e:
                print(f"Error adding metrics: {e}")

        return add_metrics_for_user

    @property
    def close_database(self):
        try:
            if self._session is not None:
                self._session.close_all()
        except Exception as e:
            print(f"Error closing database: {e}")

        return


class WaterMetric(Base):
    __tablename__ = 'water_metrics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Float)
    unit = Column(String)


Base.metadata.create_all(Database().engine)
