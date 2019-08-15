import telebot
import datetime
from telegramcalendar import create_calendar
from telebot import types

telebot.apihelper.proxy = {'https': 'socks5://userproxy:password@ip:port'}
bot = telebot.TeleBot("YOUR-TOKEN")
current_shown_dates={}


@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict

    markup = create_calendar(now.year, now.month)
    bot.send_message(message.chat.id, "Please, choose a date", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'DAY' in call.data[0:13])
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)

    if (saved_date is not None):
        day=call.data[11:]
        print(day)
        date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
        bot.send_message(chat_id, str(date))
        bot.answer_callback_query(call.id, text="")

    else:
        # add your reaction for shown an error
        pass


@bot.callback_query_handler(func=lambda call: 'NEXT-MONTH' in call.data)
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if (saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        # add your reaction for shown an error
        pass


@bot.callback_query_handler(func=lambda call: 'PREV-MONTH' in call.data)
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        # add your reaction for shown an error
        pass


@bot.callback_query_handler(func=lambda call: "IGNORE" in call.data)
def ignore(call):
    bot.answer_callback_query(call.id, text="smth wrong")


bot.polling()
