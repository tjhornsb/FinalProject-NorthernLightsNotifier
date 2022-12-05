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

## **API Setup**
API:
  [https://openweathermap.org/price#weather](https://openweathermap.org/price#weather) (Free Edition)
    This API key is for the ``openWeather_API_Key`` variable
    Generated with default settings
    
Email:


## **E-mail setup**
  Please follow this guide for creating a gmail bot account so that your instance of the program can send notification emails
[https://towardsdatascience.com/automate-email-sending-with-python-74128c7ca89a](https://towardsdatascience.com/automate-email-sending-with-python-74128c7ca89a)
 - Make a new gmail account and change the settings to allow it to run in untrusted apps
 - Update the ``bot_email`` variable with whatever email you have for this new account
 - In ``creds.json`` update the ``bot_password`` Variable with the password for this gmail account
 - Update the "toList" array in ``creds.json`` to be a list of emails you wish to send to

  **(ONLY USE PERSONAL EMAILS OR EMAILS OF PEOPLE WHO HAVE EXPRESSLY CONSENTED TO HAVE AUTOMATED EMAILS SENT TO THEM)**

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

## **Task Scheduler Setup**
Create a batch file containing the following code and name it something along the lines of ``Notifier.bat``
```
@echo off
python3 C:\Users\XXXXX\Desktop\FinalProject-NorthernLightsNotifier\NorthernLights.py
```
Next, launch task Scheduler, click the ``Action`` tab, and then select the ``Create Task`` option.
On the ``General`` tab, name the task something memorable, like ``NotifierAutorun``, select the ``Run whether user is logged on or not`` option, check the box for ``Run with highest privileges``, and choose ``Windows 10`` from the ``Cofigure for:`` dropdown menu.
Now go to the ``Triggers`` tab and click the ``New...`` button, select ``At startup`` from the ``Begin the task:`` dropdown menu, ensure that the ``Enabled`` box is checked, and click ``OK``.
Next, go into the ``Actions`` tab and click the ``New...`` button, ensure that ``Start a program`` is selected from the ``Action:`` dropdown and enter the filepath to the batchfile you created in the ``Program/Script:`` field, finally, click ``OK``.
No setting need to be modified in the ``Conditions`` or ``Settings`` tabs, and the ``OK`` button can be clicked to create the task.
Following these steps should ensure that the python file is run whenever your computer is started.


*Regards,*
*Trevor*

