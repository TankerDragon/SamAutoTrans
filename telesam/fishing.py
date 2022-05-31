from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = 15193518
api_hash = '504ab7ab95614155f137244e819b5e91'

# 5314855946:AAEuyH09krJPgoAxjNeqvV68nCVNQtZ3pNE
client = TelegramClient('anon', api_id, api_hash)



async def main():
    # me = await client.get_me()

    # print(me.first_name)

    # username = me.username
    
    # print(username)
    # print(me.phone)

    # print(await client.get_peer_id('me'))






    # You can print all the dialogs/conversations that you are part of:
    # async for dialog in client.iter_dialogs():
    #     # with open('data.csv', 'w') as csvfile:
    #     print('*/*/*/*/*/*/*/*')
    #     print(dialog)
            # writer.writerow(dialog)
            # writer.writerow([dialog.name, dialog.id, dialog.username, dialog.phone, dialog.status])
                
        # print(dialog.name, 'has ID', dialog.id)

    # # You can send messages to yourself...
    # await client.send_message('me', 'Assalomu alaykum!')
    # # ...to some chat ID
    # await client.send_message(-330604, 'Hello, group!')
    # # ...to your contacts
    # await client.send_message('+998977340770', 'Hello, Saidbek!')
    # # ...or even to any username
    # await client.send_message('@Alex_Dsp', 'Testing Telegrammmmmm!')

    # for a in range(100):  #998200
    #      await client.send_message('@Alex_Dsp', 'Assalomu alaykum, hojiaka! Man Azizbekning robotiman - ' + str(a))
    
    # ELD Team has ID -678356502
    
    # You can, of course, use markdown in your messages:
    # message = await client.send_message(
    #     'me',
    #     'This message has bold, code, italics and '
    #     'a [nice website](https://example.com)!',
    #     link_preview=False
    # )

    # Sending a message returns the sent message object, which you can use
    # print(message.raw_text)

    # You can reply to messages directly if you have a message object
    # await message.reply('Cool!')

    # Or send files, songs, documents, albums...
  #  await client.send_file('me', '/home/me/Pictures/holidays.jpg')

    # # You can print the message history of any chat:
    async for message in client.iter_messages(-1001279009032):
        print(message)
        print('************************')

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        # if message.photo:
        #     path = await message.download_media()
        #     print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(main())