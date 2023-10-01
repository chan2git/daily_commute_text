import datetime
import googlemaps                           
from twilio.rest import Client as TwilioClient

# A funcion that uses the Google Maps/Directions API to calculate the duration between start_addr and end_addr
def get_commute_duration():
    google_api = "API key" # Replace with your Google Maps API key

    # Intialize and creates a Google maps client object and passes the API key
    gmaps = googlemaps.Client(key=google_api)

    # Defines the starting and destination addreses
    start_addr = "starting adress"
    end_addr = "destination address"

    # runs the Google Map directions function and stores the result
    directions_result = gmaps.directions(start_addr, end_addr, mode = "driving")

    # Processes directions_results and stores the information related to trip duration
    first_leg = directions_result[0]['legs'][0]
    duration = first_leg['duration']['text']

    return duration



# A function that uses the Twilio API to create a message and send to a recipient's phone number
def send_text_message(message):
    # Replace with your Twilio account SID, token, and phone number (format: "1##########"")
    twilio_account_sid = "account sid"
    twilio_account_token = "account token"
    twilio_phone_num = "twilio phone number"

    # Defines the recipient's phone number (format: "1##########"")
    recipient_phone_num = "recipient phone number"

    # Intializes and creates a Twilio client object and passes Twilio credentials
    twilio_client = TwilioClient(twilio_account_sid, twilio_account_token)

    # creates a Twilio message and defines it's to, from, and body data
    twilio_client.messages.create(
        to = recipient_phone_num,
        from_ = twilio_phone_num,
        body = message
    )
    



duration = get_commute_duration()                       # Assigns the commute duration time between start/end addresses defined in the function                
current_time = datetime.datetime.now()                  # Assigns the current time

# Splits up duration into individual indexes so that it can be processed
duration_parts = duration.split()

#intialize values for hours, minutes to 0
hours, minutes = 0, 0

# Processes duration_parts by identifying the string value of hour and min, and converting it to a int value to be stored in hours, minutes
for i in range(len(duration_parts)):
    if duration_parts[i] == "hour":
        hours = int(duration_parts[i - 1])
    elif duration_parts[i] == "mins":
        minutes = int(duration_parts[i - 1])

# Creates a timedelta object representing the duration of commute time. 
# commute_duration differs from duration because timedelta objects can be used to perform math operations with datetime objects
# whereas duration is the duration represented as a string
commute_duration = datetime.timedelta(hours=hours, minutes=minutes)

# Calculates the arrival time by adding current_time (datetime object) with commute_duration (timedelta object)
# Formats in HH:MM AM/PM format
arrival_time = (current_time + commute_duration).strftime('%I:%M %p')

# Creates the text body message to be stored in variable message, which will be used as an argument in send_text_message function
message = (
    f"\n\nGood morning!\n\n"
    f"This is your daily morning commute forecast. \n\n"
    f"The estimated commute time is: {duration}.\n"
    f"If you leave now, your estimated arrival time is: {arrival_time}."
)


# Calls the send_text_message function
send_text_message(message)




################################################ FOOTNOTES ################################################

#############################
# Version:    1.00          #
# Date:       09/30/2023    #
# Coder:      CH @chan2git  #
#############################

###############################################################################
# Learning Resources/Guides                                                   #
# https://googlemaps.github.io/google-maps-services-python/docs/index.html    #
#                                                                             #
# https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages/python   #
#                                                                             #
# ChatGPT                                                                     #
###############################################################################



