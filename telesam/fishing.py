from hashlib import new
import string
from telethon import TelegramClient, events
import datetime

############
class Fish():
    def __init__(self, id, ch_id, ms_id, ti, te):
        self.id = id
        self.channel_id = ch_id
        self.message_id = ms_id
        self.time = ti
        self.text = te



# Use your own values from my.telegram.org
api_id = 19217253
api_hash = 'a54f03b2dbe152fd65e26e4549ec8fe9'

data = []
currend_id = 0


client = TelegramClient('session', api_id, api_hash)

myChannelIDs = [-1001279009032,  #UZBroker-cha
                -1001170427503,  #All about trucks
                -1001200307642,  #UTXL
                -1001588755123,  #redwood load requests
                -1001260797603,  #fedex ups amazon
                -1001446810164,  #Trucking Dispatching has ID 
                -1001400105693,  #Truckers.group has ID 
                -1001493152718,  #UZBroker - chat
                -1001405278937,  #Dispatch Time
                -1001730877604,  #GOLD All About TRUCKS
                -1001461660790,  # Trucking Dispatching Brokers
                -1001400105693,  #Truckers.group
                -1001446810164,  #Trucking Dispatching
                ]     

@client.on(events.NewMessage(chats=myChannelIDs))
async def my_event_handler(event):    
    # print(event.peer_id.channel_id)  #qaysi kanaldan keldi?
    # print('######', event)
    # if event.from_id != None:
        # print(event.from_id.user_id)     #.user_id   kim jo'natdi?
        
    # print(event.message.id)          #msg id 'si
    # print(event.date + datetime.timedelta(hours=5))  #jo'natilgan vaqt Toshkent vaqti
    # print(event.text)                #matn
    # print('********************************************************')
    data.append(Fish(currend_id, event.peer_id.channel_id, event.message.id, event.date + datetime.timedelta(hours=5), event.text))
    currend_id += 1
    print(len(data))
    # print(event)

client.start()
client.run_until_disconnected()

def get_data(id):
    fuk()

#bir sutka davomida chiqqan yuklarni hammasini DIV qilib olsin, 
#kerSSak bo'lganlarini, search qilib bersin. Type qilishi bilan filtrlanaversin.



# async def main():
#     for c in myChannelIDs:
#         ch = await client.get_entity(c)
#         print('channel ID: ', ch.id)
#         print('channel tutle: ', ch.title)
#         print('channel username: ', ch.username)
#         print()
    
# with client:
#     client.loop.run_until_complete(main())