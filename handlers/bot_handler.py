from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from utils.utils import format_metrics
from services.metric import MetricService
from services.apartment import ApartmentService
from services.user import UserService
from handlers.middleware import AuthMiddleware


class AddApartment(StatesGroup):
    waiting_for_apartment_name = State()
    waiting_for_apartment_address = State()


class AddMetrics(StatesGroup):
    waiting_for_metrics = State()


class AddUser(StatesGroup):
    waiting_for_user_name = State()


class BotHandler:
    def __init__(self,
                 router: Router,
                 user_service: UserService,
                 apartment_service: ApartmentService,
                 metric_service: MetricService,
                 logger
                 ):
        self.router = router
        self.user_service = user_service
        self.apartment_service = apartment_service
        self.metric_service = metric_service
        self.logger = logger
        self.setup_handlers()

    def setup_handlers(self):
        self.router.message.middleware(AuthMiddleware(self.user_service))

        @self.router.message(Command('start'))
        async def send_welcome(message: Message):
            await message.answer("Welcome! Send me your water metrics in the format: 'amount unit', e.g., '200 ml'.")

        @self.router.message(Command('help'))
        async def help_message(message: Message):
            await message.answer(
                "You can send your water intake metrics in the format: 'amount unit', e.g., '200 ml'.\n"
                "Commands:\n"
                "/start - Start the bot\n"
                "/help - Get help\n"
                "/metrics - View your water metrics\n"
                "/addmetrics - Add your water and electric metrics\n"
                "/addapartment - Add a new apartment")

        @self.router.message(Command('metrics'))
        async def view_metrics(message: Message):
            user_id = message.from_user.id
            metrics = self.metric_service.get_metrics_for_user(user_id)
            response = format_metrics(metrics)
            await message.answer(response)

        @self.router.message(Command('addapartment'))
        async def add_apartment_start(message: Message, state: FSMContext):
            await message.answer("Please enter the apartment name:")
            await state.set_state(AddApartment.waiting_for_apartment_name)

        @self.router.message(AddApartment.waiting_for_apartment_name)
        async def apartment_name_entered(message: Message, state: FSMContext):
            await state.update_data(apartment_name=message.text)
            await message.answer("Please enter the apartment address:")
            await state.set_state(AddApartment.waiting_for_apartment_address)

        @self.router.message(AddApartment.waiting_for_apartment_address)
        async def apartment_address_entered(message: Message, state: FSMContext):
            user_data = await state.get_data()
            apartment_name = user_data['apartment_name']
            apartment_address = message.text
            self.apartment_service.add_apartment(apartment_name, apartment_address)
            await message.answer(f"Apartment '{apartment_name}' at '{apartment_address}' added successfully.")
            await state.clear()

        @self.router.message(Command('addmetrics'))
        async def add_metrics_start(message: Message, state: FSMContext):
            await message.answer(
                "Please enter the water and electric metrics in the format: 'water electric', e.g., '200 150'.")
            await state.set_state(AddMetrics.waiting_for_metrics)

        @self.router.message(AddMetrics.waiting_for_metrics)
        async def metrics_entered(message: Message, state: FSMContext):
            chat_id = message.from_user.id
            try:
                water, electric = map(float, message.text.split())
                recorded_metric = self.metric_service.add_metrics_for_user(chat_id, water, electric)
                if recorded_metric:
                    await message.answer(
                        f"Recorded: Water - {recorded_metric.water_usage}, "
                        f"Electricity - {recorded_metric.electric_usage}")
                else:
                    await message.answer("Failed to record metrics. Please try again.")
            except ValueError:
                await message.answer("Invalid format. Please send in the format: 'water electric', e.g., '200 150'.")
                return
            await state.clear()

        @self.router.message(Command('adduser'))
        async def add_user_start(message: Message, state: FSMContext):
            await message.answer("Please enter your username:")
            await state.set_state(AddUser.waiting_for_user_name)

        @self.router.message(AddUser.waiting_for_user_name)
        async def user_entered(message: Message, state: FSMContext):
            chat_id, user_name = message.text.split(" ")
            try:
                user = self.user_service.add_user(chat_id,
                                                  user_name,
                                                  first_name=user_name,
                                                  apartment_id=1,
                                                  in_location=True
                                                  )
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
