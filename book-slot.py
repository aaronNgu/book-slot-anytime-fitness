import requests
import pytz
import json
from datetime import timedelta, datetime, date, time

API_BASE_URL = "https://api.muuvlabs.com"

def get_date_two_days_from_today():
    today = date.today()
    twoDays = timedelta(days=2)
    return today + twoDays

def convert_to_epoch_time_in_millisec(dateTime):
    targetDateTime = pytz.timezone('America/Los_Angeles').localize(dateTime)
    targetDateTime = targetDateTime.astimezone(pytz.timezone('GMT-0'))
    epochStartTime = pytz.timezone('GMT-0').localize(datetime(1970, 1, 1))
    return int((targetDateTime - epochStartTime).total_seconds() * 1000)
 
def get_time_slots_for_club(club):
    """club is the 4 digit code that represents the gym for a specific location"""
    print(f"getting time slot for {club}")
    getTimeSlotURL = f"{API_BASE_URL}/anytime/clubs/{club}"
    response = requests.get(getTimeSlotURL)
    response.raise_for_status()
    json_response = response.json()
    return json_response["time_slots"]

def check_if_slot_open(timeSlots, time):
    """ Given an epoch time return true if the specified time has open slots"""
    for timeSlot in timeSlots:
        if timeSlot['start_int'] == time:
            return timeSlot['advance_spots_open'] > 0
    return False

def post_token(keyfob, lastName):
    print(f"getting access token for {lastName}")
    getAuthURL = "https://memberauth.anytimefitness.com/memberLookup"
    redirectUrl = "https://reserve.anytimefitness.com/account/auth"
    response = requests.post(getAuthURL, 
                        data={'keyfob':keyfob, 'lastName': lastName, 'redirectUrl': redirectUrl},
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        allow_redirects=False)
    response.raise_for_status()
    
    token = response.headers['Location']
    token = token.split("token=")
    return token[1]

def post_cookie(access_token):
    """ returns a session with valid cookie given the access_token"""
    print(f"getting cookie session")
    getCookieURL = f"{API_BASE_URL}/anytime/users/token"
    session = requests.Session()
    response = session.post(getCookieURL,
            headers={"Content-Type": "application/json"},
            data=access_token)
    response.raise_for_status()
    return session

def post_time_slot(session, club, epochTime):
    print(f"making booking for time slot")
    bookSlotURL = f"{API_BASE_URL}/anytime/reservations"
    try:
        response = session.post(bookSlotURL,
                        json={"club_ident":str(club),"start_int": int(epochTime)},
                        headers={"Content-Type": "application/json"})
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error while making post request to book slot: {http_err}")
        return False
    except Exception as err:
        print(f"Other error while making post request to book slot: {err}")
        return False
    return True


def book_slots(config):
    keyfob = config["keyfob"]
    lastname = config["lastname"]
    club = config["club"]
    times = config["times"]
    twoDaysFromNow = get_date_two_days_from_today()

    dayOfTheWeek = twoDaysFromNow.weekday() + 1
    # date for two days from now not specified in config
    if str(dayOfTheWeek) not in times.keys():
        return 

    targetTime = times[str(dayOfTheWeek)].split(":")
    targetTime = time(int(targetTime[0]), int(targetTime[1]))
    targetDateTimeEpoch = convert_to_epoch_time_in_millisec(datetime.combine(twoDaysFromNow, targetTime))
    time_slots = get_time_slots_for_club(club)
    if (not check_if_slot_open(time_slots, targetDateTimeEpoch)):
        # TODO: figure out what to do here
        print(f"No Available time slots at {targetTime} on {twoDaysFromNow}")
        return 
    accessToken = post_token(keyfob, lastname)
    session = post_cookie(accessToken)
    if (not post_time_slot(session, club, targetDateTimeEpoch)):
        print(f"book time slot unsuccessful, retrying")
        if (not post_time_slot(session, club, targetDateTimeEpoch)):
            print(f"book time slot unsucessful on second attempt. aborting")

if __name__ == "__main__":
    print("starting program")
    with open('config.json') as config_file:
        data = json.load(config_file)
        for person in data:
            book_slots(person)
