from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from utils.utils import format_metrics


class AddMetrics(StatesGroup):
    waiting_for_metrics = State()


class MetricsHandler:
    def __init__(self, metric_service):
        self.metric_service = metric_service

    @staticmethod
    async def add_metrics_start(message: Message, state: FSMContext):
        await message.answer("Please enter the water and electric metrics in the format: 'water electric', e.g., '200 150'.")
        await state.set_state(AddMetrics.waiting_for_metrics)

    async def metrics_entered(self, message: Message, state: FSMContext):
        chat_id = message.from_user.id
        try:
            water, electric = map(float, message.text.split())
            recorded_metric = self.metric_service.add_metrics_for_user(chat_id, water, electric)
            if recorded_metric:
                await message.answer(
                    f"Recorded: Water - {recorded_metric.water_usage}, Electricity - {recorded_metric.electric_usage}")
            else:
                await message.answer("Failed to record metrics. Please try again.")
        except ValueError:
            await message.answer("Invalid format. Please send in the format: 'water electric', e.g., '200 150'.")
            return
        await state.clear()

    async def view_metrics(self, message: Message):
        user_id = message.from_user.id
        metrics = self.metric_service.get_metrics_for_user(user_id)
        response = format_metrics(metrics)
        await message.answer(response)
