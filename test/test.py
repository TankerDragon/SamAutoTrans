# curl --request GET 'https://api.samsara.com/v1/fleet/trailers/assignments' \
# --header 'Authorization: Bearer TOKEN' \


# request GET \
#      --url https://api.samsara.com/v1/fleet/assets/locations \
#      --header 'Accept: application/json' \
#      --header 'Authorization: Bearer samsara_api_Yjj8WcbrcKv8Glc0fq8tkaF2Qm7UzD'
import requests
import threading
import time 

url = "https://api.samsara.com/v1/fleet/assets/locations"

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer samsara_api_Yjj8WcbrcKv8Glc0fq8tkaF2Qm7UzD"
}

params = {
    # "types": "gps",
    # "decorations": "obdOdometerMeters"
}


response = requests.request("GET", url, headers=headers).json()
# print(response)
i = 0
for r in response['assets']:
    print(i)
    print(r)
    i += 1