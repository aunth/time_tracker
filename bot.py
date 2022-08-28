from main import *
import telebot
from telebot import types
import os
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

def button_and_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    start_tracking = types.InlineKeyboardButton("Start tracking", callback_data="start")
    end_tracking = types.InlineKeyboardButton("End tracking", callback_data="end")
    worked_hours = types.InlineKeyboardButton("Check worked hours", callback_data="check_last")
    worked_period = types.InlineKeyboardButton("Check worked period", callback_data="check_all")
    clean = types.InlineKeyboardButton("Clear", callback_data="clear")
    markup.add(start_tracking, end_tracking, worked_period, worked_hours, clean)
    return markup

@bot.message_handler(commands=["start"])
def greeting(message):
    greet = bot.send_message(message.chat.id, "Hello i'm time tracker bot. I can track i can coutn how much time you spend on computer. Type something to begin")
    button_and_keyboard()
    main_variable(message.chat.id)
    bot.register_next_step_handler(greet, main)

@bot.message_handler(content_types=['text'])
def main(message):
    markup = button_and_keyboard()
    bot.send_message(message.chat.id, "Choose what you want to do", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    try:
        if call.message:
            if call.data == "start":
                clock_on()
                bot.send_message(call.message.chat.id, "You are tracked")
            elif call.data == "end":
                result = clock_off()
                bot.send_message(call.message.chat.id, result)
            elif call.data == "check_last":
                tracked_work = check_worked_hours()
                bot.send_message(call.message.chat.id, tracked_work)
            elif call.data == "check_all":
                all_tracked_work = check_worked_periods()
                bot.send_message(call.message.chat.id, all_tracked_work)
            else:
                result = clean_table()
                bot.send_message(call.message.chat.id, result)
    except Exception as e:
        print(f"{e}")


    

bot.infinity_polling(timeout=10, long_polling_timeout = 5)