# Daily Commute Text
A Pythons script project utilizing Google Maps/Twilio/OpenWeatherMap API, AWS EC2 instance, and cron job to automatically text you information (trip duration, estimated arrival time, weather) about your daily work commute.

## **Table of Contents:**
- [Current Features and Developments](https://github.com/chan2git/daily_commute_text/new/main?readme=1#current-features-and-developments)

- [API Setup](https://github.com/chan2git/daily_commute_text/new/main?readme=1#api-setup)

- [Hosting/AWS EC2 Instance](https://github.com/chan2git/daily_commute_text/new/main?readme=1#hostingaws-ec2-instance)

- [Installation and Prep](https://github.com/chan2git/daily_commute_text/new/main?readme=1#installation-and-prep)

- [Automation and Scheduling](https://github.com/chan2git/daily_commute_text/new/main?readme=1#automation-and-scheduling)





## Current Features and Developments
- Estimated commute/arrival time utilizing Google Maps API
- Text alert to recipient phone number utilizing Twilio API
- Weather information (forecast, temperature, humidity) utilizing OpenWeatherMap API
- Hosted on AWS EC2 Instance (Ubuntu)
- Cron job to automatically run script on designated schedule




## API Setup
### Google Maps API
Visit https://console.google.com to begin registration for your Google Maps API credentials. After registration, be sure to search for the Directions API as it will need to be enabled under your profie.

**Google Maps Directions API documentation:**
https://developers.google.com/maps/documentation/directions/overview


### Twilio API
Visit https://twilio.com to begin registration for your Twilio API credentials. After registration, be sure to enable a Twilio phone number, which will be the number sending the text messages.

Please note that recicpient phone numbers need to be verified before they can receive Twilio text messages.

**Twilio SMS API documentation:**
https://www.twilio.com/docs/sms


### OpenWeatherMap API
Visit https://openweathermap.org to begin registration for your OpenWeatherMap API credentials.

**OpenWeather Map Current Weather API documentation:**
https://openweathermap.org/current




## Hosting/AWS EC2 Instance
This project is hosted on a AWS EC2 instance running Ubuntu. AWS Free Tier membership provides two EC2 instances (one Linux, one Windows) that can each run 750 hours/month, which effectively allows the instances to run constantly without incurring charges or needing tier upgrade for the scope of this project.

**AWS**:
https://aws.amazon.com


## Installation and Prep
### Source Code

Use the `wget` command to directly download the main .py and .env files:
```
wget https://raw.githubusercontent.com/chan2git/daily_commute_text/main/daily_commute_text.py
```
```
wget https://raw.githubusercontent.com/chan2git/daily_commute_text/main/.env
```


### Python and Required Modules
If needed, run the following bash commands in your Ubuntu terminal to install Python and required modules:
```
pip install python
```
```
pip install requests
```

```
pip install googlemaps
```

```
pip install twilio
```
```
pip install python-dotenv
```

### .env
The .env file available in this repo is a template. The key names corresponds to variable names found within project script. At a minimum, download the .env file and simply replace the template values in the key-value pairings with the appropriate credentials by using a terminal text editor such as `nano`.

Alternatively, instead of downlading the repo's .env file, you could create your own .env directly within your Ubuntu instance by using `nano`. Be sure to match the key names with the variable names it's meant to access (see template). If you make any changes, you must ensure that corresponding key names/variable names match so that the credentials and data can be referenced correctly.

Ensure that the .env file is located in the same directory as daily_commute_text.py

**.env template:**
```
a_secret1 = "Google Maps API key"
a_secret2 = "starting address"
a_secret3 = "ending address"


b_secret1 = "Twilio account SID"
b_secret2 = "Twilio account token"
b_secret3 = "Twilio phone number"
b_secret4 = "Recpient phone number"


c_secret1 = "OpenWeatherMap API key"
c_secret2 = "city name"
```


### Executable Permissions
Ensure that the script is executable by enabling executable permissions with command:
```
chmod +x daily_commute_text.py
```





### Setting the Correct Timezone
Double check your Ubuntu instance timezone by running the `timedatectl` command. If the timezone is not correct, it will unintentionally affect your cron job schedule and `datetime` related data.

To list all available timezones, run the command:
```
timedatectl list-timezones
```

To filter for a specific region, you can pipe in `grep` and the keyword. For example, to display a list of all timezones matching "America", run the command:
```
timedatectl list-timezones | grep "America"
```

To change your timezone (using **America/New_York** as an example), run the following command using `sudo`:
```
sudo timedatectl set-timezone America/New_York
```

### Hashbang (optional)
A hashbang is a sequence of text placed at the beginning of a script file that typically references and specifies the path to the interpreter (e.g. Python, Bash, etc) that is to be used. Since this script project uses Python, we can give it a Python hashbang, which would eliminate the need to specify the interpreter (in this case, Python3) when setting up our cron job or running the script.

First, double check the Python/Python3 interpreter path by running the command:
```
which python3
```
As an example, I may get the response that the python3 interpreter is located in `/usr/bin/python3`. Next, run the `nano daily_commute_text.py` command to edit the Python script, add `#!/usr/bin/python3` to the very first line of the script file, then save and close.

If you don't add a Python hashbang, to run your script you need to specify the interpreter such as `python3 daily_commute_text.py`. If you add a Python hasbang, you can simply run `./daily_commute_text.py`.



### CRLF to LF Conversion
Test your script by running it in terminal. If you get a error that says something similar to */usr/bin/python3^M: bad interpreter: no such file or directory"*, you may need to convert the script file's line endings from CRLF (Windows) to LF (Linux). If needed, follow the steps below:

Install `dos2unix` with `sudo` by running command:
```
sudo apt-get install dos2unix
```

Convert your script by running command:
```
dos2unix daily_commute_text.py
```




## Automation and Scheduling
### Cron Job
Given the free EC2 instances with AWS Free Tier, we can utilize cron jobs for this project's scope. A cron job is typically Unix/Linux-based and is an automated job or scheduled task that runs at a designated interval or schedule. Using cron jobs, we can schedule our script to run every Monday through Friday at 7:00am.

To set up a cron job, first run the command:
```
crontab -e
```
This will open up a nano-like display. Then you will need to add/modify the below in (without any hashes):
```
0 7 * * 1-5 /home/ubuntu/daily_commute_text.py
```


For additional help with learning cron job syntax, visit: https://www.hostinger.com/tutorials/cron-job

