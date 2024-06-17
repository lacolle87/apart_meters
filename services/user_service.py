from sqlalchemy.orm import Session
from database.models import User


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

    def get_admins(self):
        try:
            return self.session.query(User).filter_by(is_admin=True).all()
        except Exception as e:
            self.logger.error(f"Error fetching admins: {e}")
            return None
