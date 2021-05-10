import requests
import beepy
import time

from datetime import datetime, timedelta

  
headers = {
    'authority': 'cdn-api.co-vin.in',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'authorization':'',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'origin': 'https://selfregistration.cowin.gov.in',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://selfregistration.cowin.gov.in/',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
}

today = datetime.now() # or today = datetime.today()

# District ID is representative of City/Area
# For more IDs - 
# # Get state IDs - 
# # # GET https://cdn-api.co-vin.in/api/v2/admin/location/states
# # Get district IDs - 
# # # GET https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state_id>

# Current entry is for BBMP/Bangalore Urban
district_ids = ['294','265']

# Put your the pincodes closest to you
required_pincodes={560078,560076,560011}
# Put your the vaccine you are looking for
required_vaccine={"COVAXIN","COVISHIELD"}
# Put the age slot (18/45)
required_age=45

while True: 
    for days in range(6):
        dateObj = today + timedelta(days)
        date = dateObj.strftime("%d-%m-%Y")
        for district_id in district_ids: 
            try:
                url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id='+district_id+'&date='+date
                response = requests.get(url, headers=headers)
                responseJSON = response.json()
                for center in responseJSON['centers']:
                    for session in center['sessions']: 
                        if session['min_age_limit'] == required_age and session['available_capacity'] > 1 and session['vaccine'] in required_vaccine:
                            dataJSON = {
                                'name' : center['name'],
                                'pincode' : center['pincode'],
                                'date' : session['date'],
                                'slots' : session['slots'],
                                'min_age_limit' : session['min_age_limit'],
                                'available_capacity': session['available_capacity'],
                                'vaccine': session['vaccine'],
                                'fee_type': center['fee_type']
                            }
                            print()
                            if dataJSON['pincode'] in required_pincodes: 
                                print(dataJSON)
                                beepy.beep(sound='success')
                            else:
                                print(dataJSON)
                                # beepy.beep(sound='coin')
                        
                print("Searched Response for date "+date)
            except:
                print("Some Error for date "+date)
            finally: 
                # beepy.beep(sound='coin')
                time.sleep(2)
    time.sleep(5)
