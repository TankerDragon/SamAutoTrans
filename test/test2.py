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

    



class ContextManager(): 
    def __init__(self): 
        print('init method called') 
            
    def __enter__(self): 
        print('enter method called') 
        loopControl.start_looping()

        return self
        
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        print('exit method called') 
        loopControl.stop_looping()

    
    
with ContextManager() as manager: 
    print('with statement block')