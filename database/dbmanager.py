from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from database.models import Base


class Database:
    def __init__(self, db_uri, logger):
        self._engine = self._create_engine(db_uri)
        self._session_factory = self._create_session_factory(self._engine)
        self._session = self._create_scoped_session(self._session_factory)
        self.logger = logger

        self._create_tables_if_not_exists()

    @staticmethod
    def _create_engine(db_uri):
        return create_engine(db_uri)

    @staticmethod
    def _create_session_factory(engine):
        return sessionmaker(bind=engine)

    @staticmethod
    def _create_scoped_session(session_factory):
        return scoped_session(session_factory)

    def _create_tables_if_not_exists(self):
        self.logger.info("Creating tables if they don't exist...")
        Base.metadata.create_all(self._engine)

    @property
    def engine(self):
        return self._engine

    @contextmanager
    def session_scope(self):
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Session rollback due to error: {e}")
            raise
        finally:
            session.close()

    def get_session(self):
        return self._session()

    def close(self):
        self._session.remove()
        return "Database closed successfully."
