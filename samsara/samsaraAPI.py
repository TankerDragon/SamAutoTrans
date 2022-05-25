import requests
import threading
import time 

url = "https://api.samsara.com/fleet/vehicles/stats/feed"

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer samsara_api_Yjj8WcbrcKv8Glc0fq8tkaF2Qm7UzD"
}

params = {
    "types": "gps",
    "decorations": "obdOdometerMeters"
}

data = []


###################



class Control:
    started = False
    UPS = 5   # update in soconds

    def get_status(self):
        if self.started:
            return "started"
        else:
            return "stopped"
    # functions to control main loop <<<<<<

    def start_looping(self):
        if not self.started:
            self.started = True
            set_interval(loop, self.UPS)

    def stop_looping(self):
        self.started = False

    # >>>>>>>>>>>>>>>>>>>


def set_interval(func, sec):

    def func_wrapper():
        set_interval(func, sec)
        func()

    if loopControl.started:
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t




loopControl = Control()

def loop():
    response = requests.request("GET", url, headers=headers, params=params).json()
    for r in response['data']:
        is_present = False
        # print(i)
        # print(len(r['gps']))
        for d in data:
            if d['id'] == r['id']:
                is_present = True
                if 'decorations' in  r['gps'][0]:
                    d['odometer'] = r['gps'][0]['decorations']['obdOdometerMeters']['value']
                else:
                    d['odometer'] = None
                d['latitude'] = r['gps'][0]['latitude']
                d['longitude'] = r['gps'][0]['longitude']
                # d['headingDegrees'] = r['gps'][0]['headingDegrees']
                d['speed'] = r['gps'][0]['speedMilesPerHour']
                d['location'] = r['gps'][0]['reverseGeo']['formattedLocation']
                break
        if not is_present:
            data.append({
                'id': r['id'],
                'name': r['name'],
                'odometer': None,
                'latitude': r['gps'][0]['latitude'], 
                'longitude': r['gps'][0]['longitude'], 
                'speed': r['gps'][0]['speedMilesPerHour'], 
                'location': r['gps'][0]['reverseGeo']['formattedLocation']
                })
        
    # print(data)
    # print("###################################")

loopControl.start_looping()


# {'id': '281474979402267', 'name': 'Unit-000459', 'gps': [{'decorations': {'obdOdometerMeters': {'value': 1004633180}}, 'time': '2022-05-25T15:13:41.999Z', 'latitude': 41.24579395, 'longitude': -81.24902857, 'headingDegrees': 273.9, 'speedMilesPerHour': 71.463, 'reverseGeo': {'formattedLocation': 'Ohio Turnpike, Freedom Township, OH, 44288'}, 'isEcuSpeed': True}]}
# with open('data.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['vehicleId', 'timestamp', 'latitude', 'longitude', 'odometer'])
#     while True:
#         response = requests.request("GET", url, headers=headers, params=params).json()
#         print(response)
#         for vehicle in response["data"]:
#             for gps_ping in vehicle['gps']:
#                 if 'decorations' in gps_ping:
#                     odometer = gps_ping['decorations']['obdOdometerMeters']['value']
#                 else:
#                     odometer = None
#                 writer.writerow([
#                     vehicle['id'],
#                     gps_ping['time'],
#                     gps_ping['latitude'],
#                     gps_ping['longitude'],
#                     round(int(odometer)*0.000621371)
#                 ])
#         params['after'] = response['pagination']['endCursor']
#         if response['pagination']['hasNextPage'] == False:
#             time.sleep(5)