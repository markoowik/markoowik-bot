import telebot
from telebot import types
import tokin

from question import save_question_to_file, get_unanswered_questions, mark_question_as_answered
import os
from dotenv import load_dotenv


bot = telebot.TeleBot(tokin.TOKEN)

load_dotenv()

TOKEN = os.getenv(tokin.TOKEN)

should_save_question = {}

ADMIN_USERNAME = ["markow", "markoowik"]


@bot.message_handler(commands=["start"])
def welcome(message):
    welcome_str = "👋 Привет, {0.first_name}!, я <b>markoowik</b>, Front-End разработчик. Можете ознакомиться с информациями по кнопке ниже!".format(
        message.from_user, bot.get_me())
    project_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    git_key = types.KeyboardButton("GitHub")
    git_key2 = types.KeyboardButton("Discord")
    git_key3 = types.KeyboardButton("Проекты")
    question = types.KeyboardButton("❓ Задать вопрос!")
    project_keyboard.add(git_key, git_key2, git_key3, question)
    bot.send_message(message.chat.id, welcome_str, parse_mode="html", reply_markup=project_keyboard)


@bot.message_handler(func=lambda message: message.text in ["GitHub", "Discord", "Проекты", "❓ Задать вопрос!"])
def send_info(message):
    chat_id = message.chat.id
    if message.text == "GitHub":
        git_link_keyboard = types.InlineKeyboardMarkup()
        git_link = types.InlineKeyboardButton(text="🌐 GitHub", url="https://github.com/markoowik?tab=repositories")
        git_link_keyboard.add(git_link)
        bot.send_message(message.chat.id, "🌐 По кнопке ниже можно перейти на мой репозиторий GitHub", reply_markup=git_link_keyboard)
    elif message.text == "Discord":
        discord_keyboard = types.InlineKeyboardMarkup()
        discord_link = types.InlineKeyboardButton(text="🌐 Discord", url="https://discord.gg/GsW5FpN2")
        discord_keyboard.add(discord_link)
        bot.send_message(message.chat.id, "🌐 По кнопке ниже можно перейти на мой сервер Discord", reply_markup=discord_keyboard)
    elif message.text == "Проекты":
        project_info(message.chat.id)
    elif message.text == "❓ Задать вопрос!":
        prompt_for_question(chat_id)


@bot.message_handler(commands=["project"])
def project_info(chat_id):
    photo_urls = [
        open("image/markoowik-dev.jpeg", "rb"),
        open("image/pizza1.jpeg", "rb")
    ]  # Replace with your photo URLs
    captions = [
        "💻 markoowik-dev - здесь вы можете заказать себе сайты, телеграм боты и т.д!",
        "🍕 Pizza - здесь вы моежет заказать пиицу на сайте не выоходя из дома.",
    ]  # Corresponding captions for each photo
    links = [
        "https://markoowik.github.io/markoowik-dev/",
        "https://markoowik.github.io/Pizza/"
    ]

    try:
        for photo_path, caption, link in zip(photo_urls, captions, links):
            link_keyboard = types.InlineKeyboardMarkup()
            link_button = types.InlineKeyboardButton(text="Подробнее", url=link)
            link_keyboard.add(link_button)
            bot.send_photo(chat_id, photo_path, caption=caption, reply_markup=link_keyboard)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при отправке фото: {str(e)}")


@bot.message_handler(func=lambda message: message.text == "❓ Задать вопрос!")
def prompt_for_question(chat_id):
    should_save_question[chat_id] = True
    bot.send_message(chat_id, "Пожалуйста, введите ваш вопрос.")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    user_profile_link = f"https://t.me/{message.from_user.username}" if message.from_user.username else "No username"
    if should_save_question.get(chat_id, False) and message.text != "❓ Задать вопрос!":
        response = save_question_to_file(chat_id, user_name, message.text, user_profile_link)
        bot.send_message(chat_id, response)
        should_save_question[chat_id] = False


@bot.message_handler(commands=["list"])
def list_questions(message):
    if message.from_user.username in ADMIN_USERNAME:
        questions = get_unanswered_questions()
        if questions:
            for question in questions:
                bot.send_message(message.chat.id, f"User: {question['user_name']} ({question['profile_link']})\nQuestion: {question['question']}")
        else:
            bot.send_message(message.chat.id, "Нет неотвеченных вопросов.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")



@bot.message_handler(commands=["answer_question"])
def answer_question(message):
    args = message.text.split(maxsplit=2)  # Expected format: /answer_question <chat_id> <question_text> <response>
    if len(args) >= 4:
        chat_id = args[1]
        question_text = args[2]
        response = args[3]
        bot.send_message(chat_id, f"Ответ на ваш вопрос: {response}")
        mark_question_as_answered(chat_id, question_text)
    else:
        bot.send_message(message.chat.id, "Используйте формат: /answer_question <chat_id> <вопрос> <ответ>")



bot.polling(none_stop=True)
print(TOKEN)