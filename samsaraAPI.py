import requests
import csv
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

response = requests.request("GET", url, headers=headers, params=params).json()
for i in range(len(response['data'])):
    print(i)
    print(response['data'][i])

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