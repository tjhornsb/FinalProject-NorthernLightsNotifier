import requests, json, geocoder, astral, geopy, time, math, re, smtplib, datetime, os
from time import time, sleep, mktime
from timezonefinder import TimezoneFinder
from astral.sun import sun
from astral import moon
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

'''Update Current Time - Primary Method '''
def now_time():
    currentTime = mktime(datetime.datetime.utcnow().timetuple())
    now = datetime.datetime.now()
    timeObj = [now, currentTime]
    return(timeObj)

''' Logging '''
def logging(message):
    Y = now_time()[0].year
    M = now_time()[0].month
    D = now_time()[0].day
    hour = now_time()[0].strftime("%H")
    min = now_time()[0].strftime("%M")
    # Logging of emails to a text file
    target = "AuroraLog.txt"
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if file == target:
                path1 = os.path.join(root, file)
            else:
                path1 = os.path.join(root, target)
    with open(path1, "a") as f:
        f.write("\n___________________________________________________________________________\n" +str(M) + "-" + str(D) + "-" + str(Y) +"\n"+ str(hour) + ":" + str(min) + "\n" + message + "\n\n___________________________________________________________________________\n")
        f.close()
        pass

''' APIs, Credentials, and Global email Variables '''
# https://openweathermap.org/current
try:
    credTarget = "creds.json"
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if file == credTarget:
                credFile = open(os.path.join(root, file))
                credJson = json.load(credFile)

                openWeather_API_Key = credJson['openWeather_API_Key']

                # https://towardsdatascience.com/automate-email-sending-with-python-74128c7ca89a
                bot_email = 'weatherbotsupreme@gmail.com'
                bot_password = credJson['bot_password']
                HOST_ADDRESS = 'smtp.gmail.com'
                HOST_PORT = 587

except:
    message = "File 'creds.json' not found or not configured properly"
    print(message)
    logging(message)

''' Update Current Location - Primary Method'''
def location_update():
    # https://geocoder.readthedocs.io/
    g = geocoder.ip('me')
    lati = g.latlng[0]
    lngi = g.latlng[1]
    city = g.city
    state = g.state
    # https://geopy.readthedocs.io/en/stable/
    # https://www.geeksforgeeks.org/get-the-city-state-and-country-names-from-latitude-and-longitude-using-python/
    cunt = geopy.geocoders.Nominatim(user_agent="geoapiExercises")
    location = cunt.reverse(str(lati)+","+str(lngi))
    address = location.raw['address']
    country = address.get('country_code')
    country = country.upper()
    obj = TimezoneFinder()
    tz_info = obj.timezone_at(lat = lati, lng = lngi)
    return_info = [lati, lngi, city, state, country, tz_info]
    return return_info

'''Supplemental data for AuroraMain - dusk time'''
# Primary Dusk Time Method [Supplemental data for AuroraMain()]
def dusk_time():
    loc_update = location_update()
    lati = loc_update[0]
    lngi = loc_update[1]
    city = loc_update[2]
    state = loc_update[3]
    country = loc_update[4]
    tz_info = loc_update[5]

    Y = now_time()[0].year
    M = now_time()[0].month
    D = now_time()[0].day

    region_info = state+", "+country
    loc = astral.LocationInfo(name=city, region=region_info, timezone=tz_info, latitude=lati, longitude=lngi)
    s = astral.sun.sun(loc.observer, date=datetime.date(Y, M, D))
    duskTime = s["dusk"]
    duskTime = mktime(duskTime.timetuple())
    return(duskTime)

'''Supplemental data for AuroraMain - moon phase'''
def MoonPhase():
    moonphase = astral.moon.phase(now_time()[0])
    if moonphase <= 2:
        status = "New Moon"
    elif 2 < moonphase < 7:
        status = "Waxing crescent"
    elif 7 <= moonphase <= 8:
        status = "First Quarter"
    elif 8 < moonphase < 13:
        status = "Waxing gibbous"
    elif 13 <= moonphase <= 15:
        status = "Full Moon"
    elif 15 < moonphase < 20:
        status = "Waning gibbous"
    elif 20 <= moonphase <= 21:
        status = "Last Quarter"
    elif 21 < moonphase <= 30:
        status = "Waning crescent"
    return status

''' Weather Data - Primary Method (API call) '''
def Weather():
    loc_update = location_update()
    lati = loc_update[0]
    lngi = loc_update[1]
    weatherURL = "https://api.openweathermap.org/data/2.5/weather?lat="+str(lati)+"&lon="+str(lngi)+"&appid="+openWeather_API_Key
    weather_response = requests.get(weatherURL)
    return(weather_response)

''' Unit Conversion method for Weather data '''
# Termerature Unit Conversion
def KeltoF(keltemp):
    keltemp = int(keltemp)
    cel = keltemp - 273.15
    far = cel*(9/5)+32
    return math.floor(far)


''' Aurora - Primary Method'''
def AuroraRun():
    outside = Weather().json()
    # Location Values
    city = outside["name"]
    state = location_update()[3]

    # Weather Values
    conditions = outside["weather"][0]["description"]
    cloud = outside["clouds"]["all"]
    temp = KeltoF(outside["main"]["temp"])
    windms = outside["wind"]["speed"]
    windmph = int(windms)*2.237
    windchill = KeltoF(outside["main"]["feels_like"])
    moonphase = MoonPhase()
    moon = moonphase

    # https://www.swpc.noaa.gov/communities/space-weather-enthusiasts
    auroraURL = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
    r = requests.get(auroraURL)
    src = r.text
    kpmsg = re.search(r'\d\d\d\d is (\d)', src)
    NOAAkpindex = kpmsg.group(1)
    NOAAkpindex = int(NOAAkpindex)

    outmsg = ""
    if NOAAkpindex > 0:
        boilerplate = " of seeing the lights tonight\n\tGreatest expected KP (3hr): " + str(NOAAkpindex) +"\n\nWeather Report for " + city + " " + state + "\n\tCurrent Cloud Coverage: " + str(cloud) + '%'+"\n\tCurrent Weather Conditions: " + str(conditions) + "\n\tMoon Phase: " + str(moon) + "\n\tCurrent Temp: " + str(temp) + " degrees" + "\n\tWindchill: " + str(windchill) + " degrees" + "\n\tCurrent wind speeds: " + str(windmph) + " MPH" + "\n\tSource: https://services.swpc.noaa.gov/text/3-day-forecast.txt\n\t(NOAA Geomagnetic Activity Observation and Forecast)"

        if (4 <= NOAAkpindex) and (cloud < 75):
            outmsg = "HIGH Possibility" + boilerplate
        elif (3 <= NOAAkpindex < 4) and (cloud <= 75):
            outmsg = "MEDIUM Possibility" + boilerplate
        elif (NOAAkpindex >= 3) and (cloud >= 75):
            outmsg = "LOW Possibility" + boilerplate
        elif ((int(now_time()) >= int(dusk_time())) and (moon == "Full moon" or "New Moon")) and (cloud <= 50):
            outmsg = "VERY LOW Possibility of seeing the lights tonight\n\tYou probably won't see the lights tonight, but it should be a good night for skywatching!\n\n\tCurrent Cloud Coverage is: " + str(cloud)+"%\n\tCurrent moon phase: "+moon+"\n\tCurrent KP: "+str(NOAAkpindex)
        elif cloud >= 75:
            outmsg = "VERY LOW Possibility" + boilerplate
    else:
        return
    return [outmsg, cloud, moon, NOAAkpindex]

''' E-Mail method '''
def sendMail(subject, messagetext, mailList):
    # Sending the email notifications to all addresses in the list passed into the method
    for address in mailList:
        message = MIMEMultipart()
        message['From'] = bot_email
        message['To'] = address
        message['Subject'] = subject
        textPart = MIMEText(messagetext)
        message.attach(textPart)
        server = smtplib.SMTP(host=HOST_ADDRESS, port=HOST_PORT)
        server.starttls()
        server.login(bot_email, bot_password)
        server.send_message(message)
        server.quit()

def NorthernLightsNotification():
    AuroraCall = AuroraRun()
    AuroraMsg = AuroraCall[0]
    sendList = credJson['toList']

    if len(AuroraMsg) != 0:
        sendMail("Northern Lights Forecast", AuroraMsg, sendList)
        logging(AuroraMsg)
        return
    else:
        return

''' Main Runtime '''
while True:
    hour = now_time()[0].strftime("%H")
    minute = now_time()[0].strftime("%M")
    timestamp = str(hour) + ":" + str(minute)

    print(timestamp)
    # Northern Lights Run Times (Midnight & 9:00 PM)
    if timestamp == "00:00" or timestamp == "21:00":
        NorthernLightsNotification()
        print("Aurora Alert Activated")

    # Sleep for 1 minute before checking the time again
    sleep(60 - time() % 60)

'''Manual Testing Call'''
# NorthernLightsNotification()
