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

    if message.text == "rak":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "RAK":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Rak":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Раксиз":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Рак":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Раксиз":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Раклар":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "raklar":
     bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Raklar":
      bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Rakslar":
      bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Rakchalar":
      bot.send_message(message.chat.id, '🦞🦀♋️')

    elif message.text == "Raks":
      bot.send_message(message.chat.id, '🦞🦀♋️')

bot.polling()