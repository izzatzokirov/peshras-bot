import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

menu = ["Ош", "Кебаб", "Мастоба", "Шашлык"]
cart = {}

markup = ReplyKeyboardMarkup(resize_keyboard=True)
for item in menu:
    markup.add(KeyboardButton(item))
markup.add(KeyboardButton("📥 Сабад"), KeyboardButton("📤 Пахн кардан"))

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer(
        "Хуш омадед ба Peshras! 🌟\nИн ҷо шумо метавонед хӯроки дӯстдоштаи худро ба осонӣ фармоиш диҳед.\n\nБарои оғоз, лутфан аз меню интихоб кунед:",
        reply_markup=markup
    )

@dp.message_handler(lambda msg: msg.text in menu)
async def add_to_cart(msg: types.Message):
    user_id = msg.from_user.id
    item = msg.text
    if user_id not in cart:
        cart[user_id] = []
    cart[user_id].append(item)
    await msg.reply(f"✅ {item} ба сабад илова шуд.")

@dp.message_handler(lambda msg: msg.text == "📥 Сабад")
async def view_cart(msg: types.Message):
    user_id = msg.from_user.id
    items = cart.get(user_id, [])
    if not items:
        await msg.reply("Сабад холи аст.")
    else:
        text = "📦 Дар сабади шумо:\n" + "\n".join(f"• {item}" for item in items)
        await msg.reply(text)

@dp.message_handler(lambda msg: msg.text == "📤 Пахн кардан")
async def checkout(msg: types.Message):
    user_id = msg.from_user.id
    items = cart.get(user_id, [])
    if not items:
        await msg.reply("Сабад холи аст.")
        return
    text = "🧾 Дархости нав:\n" + "\n".join(f"• {item}" for item in items)
    await bot.send_message(chat_id=ADMIN_ID, text=f"📬 Дархости аз {msg.from_user.full_name} (@{msg.from_user.username}):\n\n{text}")
    await msg.reply("✅ Дархост ба мо ирсол шуд. Мо зуд тамос мегирем!")
    cart[user_id] = []

if _name_ == "_main_":
    executor.start_polling(dp, skip_updates=True)
