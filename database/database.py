from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager


class Database:
    def __init__(self, db_uri):
        self._engine = create_engine(db_uri)
        self._session_factory = sessionmaker(bind=self._engine)
        self._session = scoped_session(self._session_factory)

    @property
    def engine(self):
        return self._engine

    @contextmanager
    def session_scope(self):
        session = self._session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Database operation failed: {e}")
        finally:
            session.close()

    def get_session(self):
        return self._session()

    def close(self):
        self._session.remove()
        return "Database closed successfully."
