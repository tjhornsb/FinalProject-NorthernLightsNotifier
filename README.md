# NorthernLightsNotifier

## About
I made this program as a personal automation script for a class final project, but I want to make it available for anyone to use.
The main goal of this project was to notify me whenever there is a good probability of viewing the Northern Lights (Aurora Borealis)

Full project functionality includes:
 - The ability to notify someone / a list of people if there is a good probability for seeing the Northern Lights within the next 3 hours based on their current location.
 - Automatic logging so that past emails that have been sent are archived in a text file for review

## **Required Packages**
These are the Packages / Libraries used in the program
```requests, json, geocoder, astral, geopy, time, math, re, smtplib, datetime, os, timezonefinder, email```

These commands will install necessary packages that are not included with Python 3\
```python3 -m pip install --upgrade pip```\
```python3 -m pip install requests, geocoder, astral, geopy, datetime, timezonefinder```

## **Credential Setup**

  Create a new file in the main directory called ``creds.json``

  Format the ``creds.json`` file as follows:

```json
{
"openWeather_API_Key":"YOUR API KEY HERE",
"bot_password":"YOUR BOT GMAIL PASSWORD HERE",
"toList":
[
"email1@email.com",
"email2@email.com"
]
}
```

## **APIs Setup**

  https://openweathermap.org/price#weather (Free Edition)
    This API key is for the ``openWeather_API_Key`` variable
    Generated with default settings

## **E-mail setup**
 - Make a new gmail account and change the settings to allow it to run in untrusted apps
 - Update the ``bot_email`` variable with whatever email you have for this new account
 - In ``creds.json`` update the ``bot_password`` Variable with the password for this gmail account
 - Update the "toList" array in ``creds.json`` to be a list of emails you wish to send to

  **(ONLY USE PERSONAL EMAILS OR EMAILS OF PEOPLE WHO HAVE EXPRESSLY CONSENTED TO HAVE AUTOMATED EMAILS SENT TO THEM)**

## **Task Scheduler Setup**

*Regards,*
*Trevor*

