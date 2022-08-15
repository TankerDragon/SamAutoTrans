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

# def listener(messages):
#     for m in messages:
#         print(m)
#         chatid = m.chat.id
#         if m.content_type == 'text':
#             text = m.text
#             if "#trailer" in text:
#                 bot.reply_to(m, "good")
#             else:
#                 bot.reply_to(m, "wrong")
# bot.set_update_listener(listener) 



@bot.message_handler(content_types=['text'])
def handle_text(message):
    arr = message.text.split("\n")
    print(arr)

    if "rak" in message.text:
    #  bot.send_message(message.chat.id, '🦀')
     bot.reply_to(message, '🦀')

    elif "RAK" in message.text:
     bot.reply_to(message, '🦀')

    elif "Rak" in message.text:
     bot.reply_to(message, '🦀')

    elif "Раксиз" in message.text:
     bot.reply_to(message, '🦀')

    elif "Рак" in message.text:
     bot.reply_to(message, '🦀')

    elif "Раксиз" in message.text:
     bot.reply_to(message, '🦀')

    elif "Раклар" in message.text:
     bot.reply_to(message, '🦀')

    elif "raklar" in message.text:
     bot.reply_to(message, '🦀')

    elif "Raklar" in message.text:
      bot.reply_to(message, '🦀')

    elif "Rakslar" in message.text:
      bot.reply_to(message, '🦀')

    elif "Rakchalar" in message.text:
      bot.reply_to(message, '🦀')

    elif "Raks" in message.text:
      bot.reply_to(message, '🦀')

bot.polling()