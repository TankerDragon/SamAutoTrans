import telebot

API_KEY = "5339801635:AAGdVeFOHIAtZPf6LZf6DPM0CCrkehbOWg0"

bot = telebot.TeleBot(API_KEY)

print(("*working"))


@bot.message_handler(commands=['/rules', 'rules'])
def greet(message):
    bot.reply_to(message, "WATTAFUCK?")
    print(message)

# @bot.message_handler()
# def any(message):
#     bot.reply_to(message, "WATTATHUCK?")
#     print(message)

def listener(messages):
    for m in messages:
        print(m)
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            if "#trailer" in text:
                bot.reply_to(m, "good")
            else:
                bot.reply_to(m, "wrong")
            # bot.send_message(chatid, text)



bot.set_update_listener(listener) #register listener

bot.polling()