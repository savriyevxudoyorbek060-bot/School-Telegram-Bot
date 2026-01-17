import telebot
from telebot import types
import os

# ================= TOKEN =================
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi. Render Environment Variables ni tekshiring.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= SINFLAR =================

classes = ["Tayyorlov"]

class_structure = {
    1: ["A", "B"],
    2: ["A", "B"],
    3: ["A", "B"],
    4: ["A", "B", "D"],
    5: ["A", "B"],
    6: ["A", "B", "D", "E"],
    7: ["A", "B", "D"],
    8: ["A", "B", "D"],
    9: ["A", "B"],
    10: ["A", "B", "D"],
    11: ["A", "B"]
}

for sinf, harflar in class_structure.items():
    for h in harflar:
        classes.append(f"{sinf}-{h}")

# ================= DARS JADVALI =================

schedules = {
    "10-A": {
        "Dushanba": [
            "Algebra",
            "Geografiya",
            "Tarbiya",
            "Ona tili",
            "I.M.H.Y."
        ],
        "Seshanba": [
            "Ingliz tili",
            "Kimyo",
            "O‘zbekiston tarixi",
            "Geometriya",
            "Adabiyot"
        ],
        "Chorshanba": [
            "Informatika",
            "Algebra",
            "Biologiya",
            "Rus tili",
            "Ona tili",
            "Geografiya",
            "Jismoniy tarbiya"
        ],
        "Payshanba": [
            "Ingliz tili",
            "Adabiyot",
            "Algebra",
            "Kimyo",
            "Fizika",
            "Jismoniy tarbiya",
            "Texnologiya"
        ],
        "Juma": [
            "Kelajak soati",
            "Rus tili",
            "Jahon tarixi",
            "Huquq",
            "Biologiya",
            "I.M.H.Y."
        ],
        "Shanba": [
            "Fizika",
            "Informatika",
            "Geometriya"
        ]
    }
}

# ================= KITOBLAR =================

books = {
    # "10-A": {
    #     "Algebra": "https://example.com/algebra.pdf"
    # }
}

user_state = {}

# ================= START =================

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for c in classes:
        markup.add(c)

    bot.send_message(
        message.chat.id,
        "🏫 <b>Sinfni tanlang:</b>",
        reply_markup=markup
    )

# ================= SINIF TANLASH =================

@bot.message_handler(func=lambda m: m.text in classes)
def class_selected(message):
    user_state[message.chat.id] = {"class": message.text}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📅 Dars jadvali")
    markup.add("📘 Kitoblar")
    markup.add("🔙 Orqaga")

    bot.send_message(
        message.chat.id,
        f"✅ <b>{message.text}</b> tanlandi.\nBo‘limni tanlang:",
        reply_markup=markup
    )

# ================= ORQAGA =================

@bot.message_handler(func=lambda m: m.text == "🔙 Orqaga")
def back(message):
    start(message)

# ================= DARS JADVALI =================

@bot.message_handler(func=lambda m: m.text == "📅 Dars jadvali")
def schedule_menu(message):
    cls = user_state.get(message.chat.id, {}).get("class")

    if cls not in schedules:
        bot.send_message(message.chat.id, "❌ Bu sinf uchun jadval yo‘q")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in schedules[cls]:
        markup.add(day)
    markup.add("🔙 Orqaga")

    bot.send_message(
        message.chat.id,
        "📅 <b>Hafta kunini tanlang:</b>",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in [
    "Dushanba", "Seshanba", "Chorshanba",
    "Payshanba", "Juma", "Shanba"
])
def show_day(message):
    cls = user_state.get(message.chat.id, {}).get("class")

    lessons = schedules.get(cls, {}).get(message.text)
    if not lessons:
        bot.send_message(message.chat.id, "❌ Bu kun uchun jadval yo‘q")
        return

    text = f"📘 <b>{cls}</b> — <b>{message.text}</b>\n\n"
    for i, fan in enumerate(lessons, 1):
        text += f"{i}. {fan}\n"

    bot.send_message(message.chat.id, text)

# ================= KITOBLAR =================

@bot.message_handler(func=lambda m: m.text == "📘 Kitoblar")
def books_menu(message):
    cls = user_state.get(message.chat.id, {}).get("class")
    class_books = books.get(cls)

    if not class_books:
        bot.send_message(message.chat.id, "❌ Kitoblar hali qo‘shilmagan")
        return

# ================= RUN =================

print("Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)
