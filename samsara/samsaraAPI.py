import numbers
import requests
import threading
import time 

units_url = "https://api.samsara.com/fleet/vehicles/stats/feed"
trailers_url = "https://api.samsara.com/v1/fleet/assets/locations"

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer samsara_api_Yjj8WcbrcKv8Glc0fq8tkaF2Qm7UzD"
}

params = {
    "types": "gps",
    "decorations": "obdOdometerMeters"
}

data = []
trailers_data = []
num = {
    'trucks': 0,
    'trailers': 0
}
temp_num = {
    'trucks': 0,
    'trailers': 0
}

###################



class Control:
    started = False
    UPS = 4   # update in soconds

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


def alarm(req_data):
    for d in data:
        if d['id'] == str(req_data['id']):
            d['alarm'] = req_data['alarm']
            print(d['alarm'])
            break

def trailer_alarm(req_data):
    for d in trailers_data:
        if d['id'] == req_data['id']:
            if req_data['alarm']:
                d['alarm'] = True
                if d['speedMilesPerHour'] == 0:
                    d['alarm_mode'] = 1
                else:
                    d['alarm_mode'] = 0
            else:
                d['alarm_signal'] = False
                d['alarm'] = False
            ##
            

            print('*')
            break

loopControl = Control()

def update_units():
    response = requests.request("GET", units_url, headers=headers, params=params).json()
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
                if d['speed'] != 0:
                    temp_num['trucks'] += 1
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
                'location': r['gps'][0]['reverseGeo']['formattedLocation'],
                'alarm': False,
                'alarm_mode': 0,
                'alarm_signal': False
                })


def update_trailers():
    response = requests.request("GET", trailers_url, headers=headers).json()
    for r in response['assets']:
        is_present = False
        for d in trailers_data:
            if d['id'] == r['id']:
                is_present = True
                if d['alarm']:
                    if d['alarm_mode'] == 0:
                        if r['location'][0]['speedMilesPerHour'] == 0:
                            d['alarm_signal'] = True
                            print('*********************', d['name'])
                    else:
                        if r['location'][0]['speedMilesPerHour'] != 0:
                            d['alarm_signal'] = True
                            print('*********************', d['name'])

                d['name'] = r['name']
                d['assetSerialNumber'] = r['assetSerialNumber']
                d['engineHours'] = r['engineHours']
                d['location'] = r['location'][0]['location']
                d['latitude'] = r['location'][0]['latitude']
                d['longitude'] = r['location'][0]['longitude']
                d['speedMilesPerHour'] = r['location'][0]['speedMilesPerHour']
                if d['speedMilesPerHour'] != 0:
                    temp_num['trailers'] += 1
                d['timeMs'] = r['location'][0]['timeMs']
                break
        if not is_present:
            trailers_data.append({
                'id': r['id'],
                'name': r['name'],
                'assetSerialNumber': r['assetSerialNumber'],
                'engineHours': r['engineHours'],
                'location': r['location'][0]['location'],
                'latitude': r['location'][0]['latitude'],
                'longitude': r['location'][0]['longitude'],
                'speedMilesPerHour': r['location'][0]['speedMilesPerHour'],
                'timeMs': r['location'][0]['timeMs'],
                'alarm': False,
                'alarm_mode': 0,
                'alarm_signal': False
                })
    # print(trailers_data)


def loop():
    temp_num['trucks'] = 0
    update_units()
    temp_num['trailers'] = 0
    update_trailers()
    ##### applying into real num list
    num['trucks'] = temp_num['trucks']
    num['trailers'] = temp_num['trailers']

    
        
    # print(data)
    # print("###################################")

# loopControl.start_looping()

# {'id': 281474979933674, 'name': 'T-1030', 'assetSerialNumber': None, 'engineHours': 0, 'cable': {'assetType': 'Trailer'}, 'location': [{'location': '25 Bond 
# Street, Haverhill, MA, 01832', 'latitude': 42.75900362, 'longitude': -71.11928433, 'speedMilesPerHour': 0, 'timeMs': 1653584955036}]}

# {'id': '281474979402267', 'name': 'Unit-000459', 'gps': [{'decorations': {'obdOdometerMeters': {'value': 1004633180}}, 'time': '2022-05-25T15:13:41.999Z', 'latitude': 41.24579395, 'longitude': -81.24902857, 'headingDegrees': 273.9, 'speedMilesPerHour': 71.463, 'reverseGeo': {'formattedLocation': 'Ohio Turnpike, Freedom Township, OH, 44288'}, 'isEcuSpeed': True}]}
# with open('data.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['vehicleId', 'timestamp', 'latitude', 'longitude', 'odometer'])
#     while True:
#         response = requests.request("GET", units_url, headers=headers, params=params).json()
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