from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button1, button2)
kb.add(button3)

kb1 = InlineKeyboardMarkup(resize_keyboard=True)
but1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.add(but1, but2)

kb2 = InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
but3 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
but4 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
but5 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
but6 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb2.add(but3, but4, but5, but6)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('files/product1.jpeg', 'rb') as imj:
        await message.answer_photo(imj, 'Product1 |' 'Description | 1000р')
    with open('files/product2.jpeg', 'rb') as imj:
        await message.answer_photo(imj, 'Product2 |' 'Description | 2000р')
    with open('files/product3.jpeg', 'rb') as imj:
        await message.answer_photo(imj, 'Product3 |' 'Description | 3000р')
    with open('files/product4.jpeg', 'rb') as imj:
        await message.answer_photo(imj, 'Product4 |' 'Description | 4000р')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def send_calories(message, state):
    await state.update_data(growth=message.text)
    await message.answer('введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = float(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])
    cal = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий {cal}')
    await state.finish()

@dp.message_handler(text='Информация')
async def all_messages(message):
    await message.answer('ВВедите команду /start, чтобы начать общение')


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
