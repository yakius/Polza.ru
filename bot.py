import telebot
from telebot import types
from config import *


bot = telebot.TeleBot(TOKEN)

# 1.1.1 Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я ваш помощник. Я могу помочь вам с выбором продуктов, "
        "оформлением заказов и предоставлением информации. Чем я могу помочь вам сегодня?"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Консультация", "Каталог товаров", "Связаться с менеджером", "F.A.Q.", "Оформить заказ", "Подписаться на рассылку")
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# 1.1.2 Сегментация
@bot.message_handler(func=lambda message: message.text == "Консультация")
def consultation(message):
    bot.send_message(message.chat.id, "Какова ваша основная цель? (Набор массы, Снижение веса, Увеличение силы)")
    bot.register_next_step_handler(message, process_goal)

def process_goal(message):
    goal = message.text
    bot.send_message(message.chat.id, "Какой у вас уровень подготовки? (Начинающий, Средний, Продвинутый)")
    bot.register_next_step_handler(message, lambda msg: process_level(msg, goal))

def process_level(message, goal):
    level = message.text
    # Здесь можно добавить логику для предложений на основе цели и уровня
    bot.send_message(message.chat.id, f"Спасибо! Ваша цель: {goal}, Уровень: {level}. Мы подберем для вас продукты.")

# 1.1.3 Каталог / описание продуктов
@bot.message_handler(func=lambda message: message.text == "Каталог товаров")
def show_catalog(message):
    catalog_message = "Вот наш каталог:\n1. Продукт A\n2. Продукт B\n3. Продукт C\n\nНажмите на товар для получения более подробной информации."
    bot.send_message(message.chat.id, catalog_message)

# 1.1.4 Формирование заказа или заявки
@bot.message_handler(func=lambda message: message.text == "Оформить заказ")
def order(message):
    bot.send_message(message.chat.id, "Пожалуйста, введите ваше имя:")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Пожалуйста, введите ваш телефон:")
    bot.register_next_step_handler(message, lambda msg: process_phone(msg, name))

def process_phone(message, name):
    phone = message.text
    bot.send_message(message.chat.id, "Пожалуйста, укажите адрес доставки:")
    bot.register_next_step_handler(message, lambda msg: finalize_order(msg, name, phone))

#

def finalize_order(message, name, phone):
    address = message.text
    # Здесь необходимо сохранить информацию о заказе
    bot.send_message(message.chat.id, f"Ваш заказ оформлен!\nИмя: {name}, Телефон: {phone}, Адрес: {address}")

# 1.1.5 Подключение «живого» менеджера
@bot.message_handler(func=lambda message: message.text == "Связаться с менеджером")
def connect_manager(message):
    # Уведомляем менеджера
    manager_message = f"Пользователь @{message.from_user.username} хочет связаться с менеджером. Контакт: {message.from_user.first_name} {message.from_user.last_name}."
    bot.send_message(MANAGER_CHAT_ID, manager_message)

    bot.send_message(message.chat.id, "Ваш запрос отправлен менеджеру. Он свяжется с вами в ближайшее время.")

# 1.1.7 Подписка на рассылку / канал
@bot.message_handler(func=lambda message: message.text == "Подписаться на рассылку")
def subscribe(message):
    bot.send_message(message.chat.id, "Вы успешно подписались на обновления!")

# 1.1.6 Частые вопросы (F.A.Q.)
@bot.message_handler(func=lambda message: message.text == "F.A.Q.")
def faq(message):
    faq_message = "Здесь часто задаваемые вопросы: \n1. Доставка\n2. Гарантия\n3. Возврат\n4. Скидки"
    bot.send_message(message.chat.id, faq_message)

# Запуск бота
bot.polling()



