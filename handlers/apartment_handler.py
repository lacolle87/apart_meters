from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup


class AddApartment(StatesGroup):
    waiting_for_apartment_name = State()
    waiting_for_apartment_address = State()


class ApartmentHandler:
    def __init__(self, apartment_service):
        self.apartment_service = apartment_service

    @staticmethod
    async def add_apartment_start(message: Message, state: FSMContext):
        await message.answer("Please enter the apartment name:")
        await state.set_state(AddApartment.waiting_for_apartment_name)

    @staticmethod
    async def apartment_name_entered(message: Message, state: FSMContext):
        await state.update_data(apartment_name=message.text)
        await message.answer("Please enter the apartment address:")
        await state.set_state(AddApartment.waiting_for_apartment_address)

    async def apartment_address_entered(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        apartment_name = user_data['apartment_name']
        apartment_address = message.text
        self.apartment_service.add_apartment(apartment_name, apartment_address)
        await message.answer(f"Apartment '{apartment_name}' at '{apartment_address}' added successfully.")
        await state.clear()
