import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
import json
import os
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

with open("menu.json", "r", encoding="utf-8") as f:
    menu = json.load(f)

user_carts = {}

def get_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in menu:
        keyboard.add(InlineKeyboardButton(
            text=f"{item['name']} - {item['price']} сомонӣ",
            callback_data=f"add_{item['id']}"
        ))
    keyboard.add(InlineKeyboardButton(text="📥 Сабад", callback_data="view_cart"))
    return keyboard

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Хуш омадед ба Peshras! Менюи хӯрокҳоро бинед ва фармоиш диҳед:", 
                         reply_markup=get_menu_keyboard())

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_carts:
        user_carts[user_id] = []

    if callback.data.startswith("add_"):
        item_id = callback.data.split("_")[1]
        for item in menu:
            if str(item["id"]) == item_id:
                user_carts[user_id].append(item)
                await callback.answer(f"{item['name']} илова шуд!")
                return

    if callback.data == "view_cart":
        cart = user_carts.get(user_id, [])
        if not cart:
            await callback.message.answer("Сабади шумо холӣ аст.")
            return
        text = "📦 Сабади шумо:
"
        total = 0
        for item in cart:
            text += f"- {item['name']} - {item['price']} сомонӣ
"
            total += item["price"]
        text += f"
Ҷамъи умумӣ: {total} сомонӣ"
        text += "

Барои тасдиқи фармоиш, рақами телефон ва суроғаи худро нависед."
        await callback.message.answer(text)
        return

@dp.message()
async def handle_contact(message: types.Message):
    user_id = message.from_user.id
    cart = user_carts.get(user_id, [])
    if not cart:
        await message.answer("Сабади шумо холӣ аст.")
        return
    order_text = f"🆕 Фармоиши нав аз {message.from_user.full_name} (@{message.from_user.username}):
"
    total = 0
    for item in cart:
        order_text += f"- {item['name']} - {item['price']} сомонӣ
"
        total += item["price"]
    order_text += f"
Ҷамъи умумӣ: {total} сомонӣ"
    order_text += f"

📞 Маълумот аз муштарӣ: {message.text}"

    await bot.send_message(chat_id="7696167680", text=order_text)
    await message.answer("Фармоиши шумо қабул шуд! Ташаккур барои боварӣ. 🚀")

    user_carts[user_id] = []

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())