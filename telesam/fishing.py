from telethon import TelegramClient, events

import requests
import threading

# Use your own values from my.telegram.org
api_id = 19317786
api_hash = 'e2d1af44a00ed24df364699452b2134f'
client = TelegramClient('session', api_id, api_hash)



# client = TelegramClient('anon', api_id, api_hash)


# api_id = 19217253
# api_hash = 'a54f03b2dbe152fd65e26e4549ec8fe9'



# async def main():
#     async for message in client.iter_messages(-1001279009032):
#         print(message)
#         print('************************')

# with client:
#     client.loop.run_until_complete(main())




# class Control:
#     started = False
#     UPS = 4   # update in soconds

#     def get_status(self):
#         if self.started:
#             return "started"
#         else:
#             return "stopped"
#     # functions to control main loop <<<<<<

#     def start_looping(self):
#         if not self.started:
#             self.started = True
#             set_interval(loop, self.UPS)

#     def stop_looping(self):
#         self.started = False

#     # >>>>>>>>>>>>>>>>>>>


# def set_interval(func, sec):

#     def func_wrapper():
#         set_interval(func, sec)
#         func()

#     if loopControl.started:
#         t = threading.Timer(sec, func_wrapper)
#         t.start()
#         return t




# loopControl = Control()


# def loop():
#     ##### applying into real num list
#     num['trucks'] = temp_num['trucks']
#     num['trailers'] = temp_num['trailers']

    
# loopControl.start_looping()



# Use your own values from my.telegram.org

myChannelIDs = [-1001279009032, -1001170427503, -1001200307642, -1001588755123, -1001260797603]

words = ['']

@client.on(events.NewMessage(chats=myChannelIDs))
async def my_event_handler(event):
    for w in words:
        if w in event.text:
            print(event.text)
            print('*********************')

client.start()
client.run_until_disconnected()