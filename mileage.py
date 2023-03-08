import stravalib
import pickle
import datetime
import time

# Strava API client setup
client = stravalib.Client()
MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = open('client.secret').read().strip().split(',')
RESULT = []
current_year = datetime.datetime.now().year

class Week:
    def __init__(self, week, mileage, week_avg):
        self.week = week
        self.mileage = mileage
        self.week_avg = week_avg

# def setup_token():
    # One time authentication steps
    # print (f"Client ID and secret read from file: {MY_STRAVA_CLIENT_ID}")

    # Print URL to receive code
    # url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='http://127.0.0.1:5000/authorization', scope=['read_all','profile:read_all','activity:read_all'])
    # print(url)
    # CODE = '3b49305bef25f3763fbac76c2a588b4008755a69'

    # Use code received to get access token and save
    # access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)
    # with open('access_token.pickle', 'wb') as f:
    #     pickle.dump(access_token, f)

def check_token():
    # Read access token
    with open('access_token.pickle', 'rb') as f:
        access_token = pickle.load(f)

    # Check if access token is expired and needs refreshed    
    if time.time() > access_token['expires_at']:
        print('Token has expired, will refresh')
        refresh_response = client.refresh_access_token(client_id=MY_STRAVA_CLIENT_ID, 
                                                client_secret=MY_STRAVA_CLIENT_SECRET, 
                                                refresh_token=access_token['refresh_token'])
        access_token = refresh_response
        with open('access_token.pickle', 'wb') as f:
            pickle.dump(refresh_response, f)
        print('Refreshed token saved to file')

        client.access_token = refresh_response['access_token']
        client.refresh_token = refresh_response['refresh_token']
        client.token_expires_at = refresh_response['expires_at']
            
    else:
        print('Token still valid, expires at {}'
            .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))

        client.access_token = access_token['access_token']
        client.refresh_token = access_token['refresh_token']
        client.token_expires_at = access_token['expires_at']

def athlete_info():
    check_token()
    athlete = client.get_athlete()
    return athlete.firstname

def check_activities():
    check_token()

    # Get the authenticated athlete's activities
    activities = client.get_activities(after = datetime.datetime(current_year, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ'), before = datetime.datetime(current_year + 1, 1, 1).strftime('%Y-%m-%dT%H:%M:%SZ'))
 
    # Create an empty dictionary to store the weekly mileage and empty array to store result
    weekly_mileage = {}
    RESULT = []

    # Loop through each activity
    for activity in activities:

        # Get the start date of the activity
        start_date = activity.start_date.date()

        # Calculate the number of miles for the activity
        miles = activity.distance.num / 1609.34

        # Determine the week number of the start date
        week_number = start_date.isocalendar()[1]

        # Add the mileage to the weekly mileage dictionary
        if week_number in weekly_mileage:
            weekly_mileage[week_number] += miles
        else:
            weekly_mileage[week_number] = miles

    # Calculate the total mileage for the year
    total_mileage = sum(weekly_mileage.values())

    # Ask the user for their mileage goal for the year
    goal = goal_rem = 1200

    # Calculate the number of weeks in a year
    week_num = 1

    # Calculate the average weekly mileage needed to achieve the goal
    average_mileage = goal / 52

    # Compare the average weekly mileage to the actual weekly mileage
    for week, mileage in reversed(weekly_mileage.items()):
        week_num = week
        RESULT.append(Week(week, mileage, average_mileage))
        goal_rem = goal_rem - mileage
        average_mileage = goal_rem / (53 - week_num)

    leftwks = 53 - week_num
    leftavg = goal_rem / leftwks
    estavg = ((total_mileage - RESULT[-1].mileage) / (week_num - 1)) * 52

    # Append the total mileage for the year
    RESULT.append(f"<b>Total mileage for the year:</b> {total_mileage:.3f} miles")
    
    # Append the average mileage needed each remaining week
    RESULT.append(f"<b>Weekly average remaining to make {goal} miles:</b> {leftavg:.3f} miles/week")

    # Append the total remaining weeks
    RESULT.append(f"<b>Remaining weeks:</b> {leftwks} weeks")
    
    # Append estimated total if continuing on same mileage avg
    RESULT.append(f"<b>If you continue at this weekly average you will walk:</b> {estavg:.3f} miles in {current_year}")

    return RESULT