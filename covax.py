import requests
import beepy
import time

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

# Put the dates you want (even though the API returns a week's schedule)
dates=['03-05-2021','04-05-2021','05-05-2021', '06-05-2021', '07-05-2021','08-05-2021']


while True: 
    for date in dates: 
        try:
            url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=294&date='+date
            response = requests.get(url, headers=headers)
            responseJSON = response.json()
            for center in responseJSON['centers']:
                for session in center['sessions']: 
                    if session['min_age_limit'] == 18 and session['available_capacity'] > 1:
                        dataJSON = {
                            'name' : center['name'],
                            'pincode' : center['pincode'],
                            'date' : session['date'],
                            'slots' : session['slots'],
                            'min_age_limit' : session['min_age_limit'],
                            'available_capacity': session['available_capacity']
                        }
                        print(dataJSON)
                        print()
                        # Put your the pincodes closest to you
                        if dataJSON['pincode'] in [560078,560076,560011]: 
                            beepy.beep(sound='success')
                            beepy.beep(sound='success')
                        else:
                            beepy.beep(sound='coin')
                    
            print("Searched Response for date "+date)
        except:
            print("Some Error for date "+date)
        finally: 
            # beepy.beep(sound='coin')
            time.sleep(2)
    time.sleep(5)
