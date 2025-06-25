
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

API_TOKEN = '7696167680:AAGv7CjZmeBb8bXRvKY9dm8tdTxuCuwoZLE'
admin_chat_id = '7908968114'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главное меню
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton("📋 Меню"),
    KeyboardButton("📍 Адрес"),
)

# Меню еды
food_menu = {
    "Шашлык куриный": "17 сомони",
    "Шашлык Кима": "13 сомони",
    "Оши плов": "15 сомони",
    "Куртоб": "20 сомони"
}

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("Хуш омадед ба Peshras! ⬇️", reply_markup=menu)

@dp.message_handler(lambda m: m.text == "📋 Меню")
async def send_menu(msg: types.Message):
    text = "📋 Меню:\n\n"
    for item, price in food_menu.items():
        text += f"🍽 {item} — {price}\n"
    await msg.answer(text)

@dp.message_handler(lambda m: m.text == "📍 Адрес")
async def ask_address(msg: types.Message):
    await msg.answer("Илтимос, адреси худро равон кунед.")

@dp.message_handler()
async def forward_order(msg: types.Message):
    await msg.answer("✅ Заказ қабул шуд! Мо ба наздикӣ занг мезанем.")
    await bot.send_message(admin_chat_id, f"📥 ЗАКАЗ:\n{msg.text}\n👤 Аз: @{msg.from_user.username or msg.from_user.full_name}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
