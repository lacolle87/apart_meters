from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup


class AddUser(StatesGroup):
    waiting_for_user_name = State()


class UserHandler:
    def __init__(self, user_service, logger):
        self.user_service = user_service
        self.logger = logger

    @staticmethod
    async def add_user_start(message: Message, state: FSMContext):
        await message.answer("Please enter your username:")
        await state.set_state(AddUser.waiting_for_user_name)

    async def user_entered(self, message: Message, state: FSMContext):
        chat_id, user_name = message.text.split(" ")
        try:
            user = self.user_service.add_user(chat_id, user_name, first_name=user_name, apartment_id=1, in_location=True)
            if user:
                await message.answer(f"User {user_name} added successfully.")
            else:
                await message.answer("Failed to add user. Please try again.")
        except Exception as ex:
            error_message = "Failed to add user. Please try again."
            self.logger.error(f"Error adding user: {ex}")
            await message.answer(error_message)
        finally:
            await state.clear()
