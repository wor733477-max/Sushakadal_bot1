import os
import telebot
import random
import re
from telebot import types

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN не найден в переменных окружения")

bot = telebot.TeleBot(TOKEN)

# ===== ЗАГРУЗКА СЛОВАРЯ ИЗ НЕСКОЛЬКИХ ФАЙЛОВ =====

DAL_FILES = ['dal_1.txt', 'dal_2.txt']


def load_dal_words(files):
    all_words = []

    for filename in files:
        if not os.path.exists(filename):
            print(f'ОШИБКА: файл {filename} не найден')
            continue

        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        blocks = re.split(r'\n\s*\n', text)
        words = [block.strip() for block in blocks if block.strip()]
        all_words.extend(words)

    if not all_words:
        raise RuntimeError("Словарные файлы пусты или не найдены")

    print(f'Загружено слов: {len(all_words)}')
    return all_words


WORDS = load_dal_words(DAL_FILES)


def get_random_dal_word():
    return random.choice(WORDS)

# ===== КЛАВИАТУРА =====


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
    keyboard.add(types.KeyboardButton('Словесо'))
    return keyboard

# ===== ХЕНДЛЕРЫ =====


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Новые словеса, сушки, беспредел.",
        reply_markup=main_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == 'Словесо')
def send_word(message):
    bot.send_message(
        message.chat.id,
        "Бери, друг сердечный 🪶"
    )

    bot.send_message(
        message.chat.id,
        get_random_dal_word(),
        reply_markup=main_keyboard()
    )

# ===== ЗАПУСК =====

bot.infinity_polling(skip_pending=True)

