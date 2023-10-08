import os
import datetime
import requests
import googlemaps      
import dotenv
from twilio.rest import Client as TwilioClient

dotenv.load_dotenv()

# A funcion that uses the Google Maps/Directions API to calculate the duration between start_addr and end_addr
def get_commute_duration():
    # References and stores the appropriate credential/data
    google_api = os.getenv("a_secret1")

    # Intialize and creates a Google maps client object and passes the API key
    gmaps = googlemaps.Client(key=google_api)

    # Defines the starting and destination addreses
    start_addr = os.getenv("a_secret2")
    end_addr = os.getenv("a_secret3")

    # runs the Google Map directions function and stores the result
    directions_result = gmaps.directions(start_addr, end_addr, mode = "driving")

    # Processes directions_results and stores the information related to trip duration
    first_leg = directions_result[0]['legs'][0]
    duration = first_leg['duration']['text']

    return duration



# A function that uses the Twilio API to create a message and send to a recipient's phone number
def send_text_message(message):
    # References and stores the appropriate credential/data
    twilio_account_sid = os.getenv("b_secret1")
    twilio_account_token = os.getenv("b_secret2")
    twilio_phone_num = os.getenv("b_secret3")

    # References and stores the appropriate credential/data
    recipient_phone_num = os.getenv("b_secret4")

    # Intializes and creates a Twilio client object and passes Twilio credentials
    twilio_client = TwilioClient(twilio_account_sid, twilio_account_token)

    # creates a Twilio message and defines it's to, from, and body data
    twilio_client.messages.create(
        to = recipient_phone_num,
        from_ = twilio_phone_num,
        body = message
    )
    


# A function that uses the OpenWeatherMap API to pull the temperature and forecast information for predetermined city
def get_weather():
    # References and stores the appropriate credential/data
    OWM_key = os.getenv("c_secret1")
    city = os.getenv("c_secret2")

    # Establishes the API call URL and passes the city name and API key to appropriate position in the URL, and submits a get request, and stores the response in var response
    request_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_key}&units=imperial"
    response = requests.get(request_url)

    # Turns response into json format and stores in var called data
    data = response.json()

    # Access the desired specific information in data, and stores in the corresponding named variables
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    humidity = data['main']['humidity']

    return weather, temp, humidity




duration = get_commute_duration()                       # Assigns the commute duration time between start/end addresses defined in the function to variable named duration             
current_time = datetime.datetime.now()                  # Assigns the current time to variable named current_time
weather = get_weather()                                 # Assigns the current weather info to variable named weather

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
    f"Daily Commute Text\n\n"
    f"Good morning!\n\n"
    f"This is your daily morning commute forecast.\n\n"
    f"The current weather reading is {weather[0]} with a temperature of {weather[1]}F and humidity of {weather[2]}% \n\n"
    f"The estimated commute time is {duration}. If you leave now, your estimated arrival time is: {arrival_time}."
)


# Calls the send_text_message function
send_text_message(message)
