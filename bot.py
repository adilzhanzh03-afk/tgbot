import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# ======== Токен через переменные окружения ========
TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

user_data = {}

# ================= СТАРТ =================
@dp.message(CommandStart())
async def start(message: types.Message):
    user_data[message.from_user.id] = {"score": 0}
    await message.answer(
        "Сегодня 8ое марта🌷\n"
        "Хоть я и не рядом физически, но я все равно всегда с тобой🌸\n\n"
        "Введи пароль, чтобы продолжить…"
    )

@dp.message()
async def password_check(message: types.Message):
    if message.from_user.id not in user_data:
        return
    if "stage" not in user_data[message.from_user.id]:
        if message.text == "Ботик":
            user_data[message.from_user.id]["stage"] = "quiz"
            await message.answer("Доступ получен💕")
            await asyncio.sleep(2)
            await message.answer("Квест начинается 🎮")
            await asyncio.sleep(1)
            await send_question_1(message)
        else:
            await message.answer("Подсказка!\nКак я тебя мило называю?")

# ================= ВОПРОС 1 =================
async def send_question_1(message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Через друзей", callback_data="q1_0")],
            [InlineKeyboardButton(text="В мюзикле", callback_data="q1_1")],
            [InlineKeyboardButton(text="Случайно встретились", callback_data="q1_2")],
            [InlineKeyboardButton(text="Знакомы с детства", callback_data="q1_3")]
        ]
    )
    await message.answer("1️⃣ Как мы познакомились?", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("q1"))
async def question_1(callback: types.CallbackQuery):
    await callback.answer()
    if callback.data == "q1_1":
        user_data[callback.from_user.id]["score"] += 1
    await callback.message.edit_reply_markup()
    await asyncio.sleep(1)
    await callback.message.answer("Следующий вопрос...")
    await asyncio.sleep(1)
    await send_question_2(callback.message)

# ================= ВОПРОС 2 =================
async def send_question_2(message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="20.10.07", callback_data="q2_0")],
            [InlineKeyboardButton(text="17.07.08", callback_data="q2_1")],
            [InlineKeyboardButton(text="14.03.25", callback_data="q2_2")],
            [InlineKeyboardButton(text="07.03.25", callback_data="q2_3")]
        ]
    )
    await message.answer("2️⃣ Когда мы начали встречаться?", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("q2"))
async def question_2(callback: types.CallbackQuery):
    await callback.answer()
    if callback.data == "q2_2":
        user_data[callback.from_user.id]["score"] += 1
    await callback.message.edit_reply_markup()
    await asyncio.sleep(1)
    await callback.message.answer("Еще один вопрос...")
    await asyncio.sleep(1)
    await send_question_3(callback.message)

# ================= ВОПРОС 3 =================
async def send_question_3(message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Кошек", callback_data="q3_0")],
            [InlineKeyboardButton(text="Собак", callback_data="q3_1")]
        ]
    )
    await message.answer("3️⃣ Что я люблю больше?", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("q3"))
async def question_3(callback: types.CallbackQuery):
    await callback.answer()
    if callback.data == "q3_0":
        user_data[callback.from_user.id]["score"] += 1
        await callback.message.answer("Но тебя люблю больше всего 😝")
        await asyncio.sleep(1.5)
    await callback.message.edit_reply_markup()
    await asyncio.sleep(1)
    await send_question_4(callback.message)

# ================= ВОПРОС 4 =================
async def send_question_4(message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Я", callback_data="q4_0")],
            [InlineKeyboardButton(text="Ты", callback_data="q4_1")]
        ]
    )
    await message.answer("4️⃣ Кто первый написал?", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("q4"))
async def question_4(callback: types.CallbackQuery):
    await callback.answer()
    if callback.data == "q4_0":
        user_data[callback.from_user.id]["score"] += 1
    await callback.message.edit_reply_markup()
    await asyncio.sleep(1)
    await send_question_5(callback.message)

# ================= ВОПРОС 5 =================
async def send_question_5(message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="q5_0")],
            [InlineKeyboardButton(text="Нет", callback_data="q5_1")]
        ]
    )
    await message.answer("5️⃣ Скучаю ли я по тебе?", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("q5"))
async def question_5(callback: types.CallbackQuery):
    await callback.answer()
    if callback.data == "q5_0":
        user_data[callback.from_user.id]["score"] += 1
        await callback.message.answer("Оч сильно скучашки 😕🫶🏽")
        await asyncio.sleep(1.5)
    await callback.message.edit_reply_markup()
    score = user_data[callback.from_user.id]["score"]
    await asyncio.sleep(2)
    await callback.message.answer(f"Ты набрала {score}/5 ❤️")
    if score == 5:
        await callback.message.answer("жаным, все знаешь💗")
    else:
        await callback.message.answer("ничего, страшного наверное просто забыла🤍")
    await asyncio.sleep(2)
    await callback.message.answer("10 причин почему я тебя люблю 💖")
    await asyncio.sleep(2)
    await send_reasons(callback.message)

# ================= 10 ПРИЧИН =================
reasons = [
    "1️⃣ Я люблю тебя за то, как ты умеешь быть нежной даже тогда, когда злишься.",
    "2️⃣ Я люблю твой голос — даже через километры он для меня самый родной.",
    "3️⃣ Я люблю твои глаза(именно в их я и влюбился).",
    "4️⃣ Я люблю твою искренность.",
    "5️⃣ Я люблю как ты поддерживаешь меня.",
    "6️⃣ Я люблю как ты переживаешь за меня.",
    "7️⃣ Я люблю тебя за то что ты настоящая.",
    "8️⃣ Я люблю за то что стараешься ради нас.",
    "9️⃣ Я люблю что ты защищаешь мое имя за моей спиной.",
    "🔟 Я люблю тебя просто за то что ты есть."
]

async def send_reasons(message):
    for i in range(10):
        await message.answer_photo(
            photo=types.FSInputFile(f"photo{i+1}.jpg"),
            caption=reasons[i]
        )
        await asyncio.sleep(2)
    await send_timer(message)

# ================= ТАЙМЕР =================
async def send_timer(message):
    target_date = datetime(2026, 5, 1)
    now = datetime.now()
    diff = target_date - now
    days = diff.days
    await message.answer(f"До нашей встречи ⏳(1 мая): {days} дней")
    await asyncio.sleep(3)
    await send_final(message)

# ================= ФИНАЛ =================
async def send_final(message):
    await message.answer("Ну вот и пришло время для моего поздравления:")
    await asyncio.sleep(2)
    await message.answer_video(types.FSInputFile("final.mp4"))
    await asyncio.sleep(3)
    await message.answer("💖 В 14:00 ТЕБЯ ЖДЕТ СЮРПРИЗ ❤️\nНИКУДА НЕ УХОДИ🫣🤫")

# ================= ЗАПУСК =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
