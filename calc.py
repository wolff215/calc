import stravalib
import pickle
import datetime
import time

result = []

# Strava API client setup
client = stravalib.Client()
MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = open('client.secret').read().strip().split(',')
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
        # print('Token has expired, will refresh')
        refresh_response = client.refresh_access_token(client_id=MY_STRAVA_CLIENT_ID, 
                                                client_secret=MY_STRAVA_CLIENT_SECRET, 
                                                refresh_token=access_token['refresh_token'])
        access_token = refresh_response
        with open('access_token.pickle', 'wb') as f:
            pickle.dump(refresh_response, f)
        # print('Refreshed token saved to file')

        client.access_token = refresh_response['access_token']
        client.refresh_token = refresh_response['refresh_token']
        client.token_expires_at = refresh_response['expires_at']
            
    else:
        # print('Token still valid, expires at {}'
            # .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))

        client.access_token = access_token['access_token']
        client.refresh_token = access_token['refresh_token']
        client.token_expires_at = access_token['expires_at']


def athlete_info():
    athlete = client.get_athlete()
    return athlete.firstname

def check_activities():
    check_token()
    # Get the authenticated athlete's activities
    activities = client.get_activities(after = "2023-01-01T06:00:00Z", before = "2024-1-1T06:00:00Z")
 
    # Create an empty dictionary to store the weekly mileage
    weekly_mileage = {}
    #result = []
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
    goal = 1200 #float(input("Enter your mileage goal for the year (in miles): "))

    # Calculate the number of weeks in a year
    num_weeks = 52
    mileage_inc = 0
    week_num = 1

    # Calculate the average weekly mileage needed to achieve the goal
    average_mileage = goal / num_weeks

    # Compare the average weekly mileage to the actual weekly mileage
    for week, mileage in reversed(weekly_mileage.items()):
        if mileage > average_mileage:
            result.append(f"<b>Week {week}:</b> {mileage:.2f} miles (ahead of goal of {average_mileage:.2f} miles)")
        else:
            result.append(f"<b>Week {week}:</b> {mileage:.2f} miles (behind goal of {average_mileage:.2f} miles)")
        average_mileage = (goal - mileage) / (num_weeks - week)
        week_num = week

    # Print the total mileage for the year
    result.append(f"<b>Total mileage for the year:</b> {total_mileage:.2f} miles")

    leftwks = 52 - week_num
    leftavg = (goal - total_mileage) / leftwks

    result.append(f"<b>Weekly average remaining to make 1200 miles:</b> {leftavg:.3f} miles/week")

    result.append(f"<b>Remaining weeks:</b> {leftwks} weeks")

    return result