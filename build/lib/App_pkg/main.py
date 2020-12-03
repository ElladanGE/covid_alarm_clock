"""Main module for covid_alarm_clock-19 alarm clock. This module runs the alarm clock."""

from flask import *
from App_pkg.time_conversion import *
import requests
import json
import sched
import time
import pyttsx3
import logging
import os
from uk_covid19 import Cov19API

# Configuring basic logging
logging.basicConfig(level=logging.INFO, filename='sys.log', encoding='utf-8')

# Alarm clock
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

# Opening config file
config_path = (os.path.dirname(__file__)) + "/config_file.json"

with open(config_path, 'r') as f:
    json_file = json.load(f)
keys = json_file["API_keys"]
location = json_file["Location"]
sources = json_file["News-sources"]
notif_time = int(json_file["Notif_period"]["time"])
threshold = int(json_file["threshold"]["number"])

# Covid19 local cases api
covid_struct = {
    "cases_and_deaths": {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate",
        "cumCasesBySpecimenDateRate": "cumCasesBySpecimenDateRate"
    }
}
api = Cov19API(
    filters=["areaName=" + location["my-city"]],
    structure=covid_struct["cases_and_deaths"],
    latest_by="newCasesByPublishDate"
)


def news_api():
    """Uses news API and returns a dictionary containing news """
    news_base_url = "https://newsapi.org/v2/top-headlines?"
    news_api_key = keys["news"]
    country = location["country"]
    news_url = news_base_url + "country=" + country + "&apiKey=" + news_api_key
    n_api = requests.get(news_url)
    return n_api.json()


def top_news(news: dict) -> tuple[list, list]:
    """Returns a tuple containing a list of top news stories and their respective urls

        If status code is not 200, logs error and returns empty tuple.
    """
    top_stories = []
    urls = []
    my_sources = sources["my-sources"]
    if news['status'] != 'ok':
        logging.error(news['message'])
        return [], []
    for articles in news["articles"]:
        if articles["source"]["name"] in my_sources:
            top_stories.append(articles["title"])
            urls.append(articles['url'])
    return top_stories, urls


def read_news() -> None:
    """Announces top news stories from top_news()"""
    if top_news(news_api()) == ([], []):
        return None
    engine1 = pyttsx3.init()
    stories = top_news(news_api())[0]
    for titles in stories:
        engine1.say(titles)
        engine1.runAndWait()
    logging.info("Local news was announced at: " + time.strftime("%H:%M", time.localtime()))


def weather_api() -> Response:
    """Returns weather Api response"""
    weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"
    weather_api_key = keys["weather"]
    city_name = location["my-city"]
    weather_url = weather_base_url + "appid=" + weather_api_key + "&q=" + city_name + "&units=metric"
    return requests.get(weather_url)


def loc_weather() -> None:
    """Announces local weather

        If weather api response is not 200: returns None
    """
    engine2 = pyttsx3.init()
    w_response = weather_api()
    if w_response.status_code != 200:
        logging.error(w_response.json()['message'])
        return None
    x = w_response.json()
    content = "The current temperature in " + location["my-city"] + " is " + str(x["main"]["temp"]) + " °C"
    engine2.say(content)
    engine2.runAndWait()
    logging.info("Local weather was announced at: " + time.strftime("%H:%M", time.localtime()))


def local_covid_cases() -> None:
    """Uses Uk Gov. API to announce number of local covid_alarm_clock-19 cases

        If covid_alarm_clock api response isn't 200: returns None
    """
    engine3 = pyttsx3.init()
    response = requests.get("https://api.coronavirus.data.gov.uk/v1/data", params=api.api_params, timeout=10)
    if response.status_code != 200:
        logging.error(response.json()['response'])
        return None
    data = api.get_json()["data"][0]
    date = data["date"]
    new_cases = data['newCasesByPublishDate']
    engine3.say("On " + str(date) + " there are " + str(new_cases) + " new cases of covid_alarm_clock-19 in " + location["my-city"])
    engine3.runAndWait()
    # Log alarm
    logging.info("Local covid_alarm_clock cases were announced at: " + time.strftime("%H:%M", time.localtime()))


def national_covid_cases() -> str:
    """Uses Uk Gov. Api to return a string of the number of latest national covid_alarm_clock-19 cases.

        If covid_alarm_clock Api response isn't 200: Returns error message
    """
    national_api = Cov19API(
        filters=["areaName=England"],
        structure=covid_struct["cases_and_deaths"],
        latest_by="newCasesByPublishDate"
    )
    response = requests.get("https://api.coronavirus.data.gov.uk/v1/data", params=national_api.api_params, timeout=10)
    if response.status_code != 200:
        logging.error(response.json()['response'])
        return "An error has occurred, see logging for more details."
    national_data = national_api.get_json()["data"][0]
    local_data = api.get_json()["data"][0]
    national_new_cases = national_data['newCasesByPublishDate']
    local_new_cases = local_data['newCasesByPublishDate']
    date = national_data["date"]
    return "On " + str(date) + " there are " + str(national_new_cases) + " new cases of covid_alarm_clock-19 in England  and " + \
           str(local_new_cases) + " in Exeter."


def period_notif(notif_list: list) -> None:
    """Adds 3 dictionaries to a list periodically (every hour) using a scheduled event :

        One dictionary for Covid-19 update
        One dictionary for news stories
        One dictionary for weather update

        Returns None
    """
    s.enter(notif_time, 1, period_notif, (notif_list,))
    w_response = weather_api()
    x = w_response.json()
    if w_response.status_code != 200:
        logging.error(w_response.json()['message'])
        notif_list.append(dict(title="Error", content="See logging for more details"))
        return None
    weather = "The current temperature in " + location["my-city"] + " is " + str(x["main"]["temp"]) + " °C"
    stories = ""
    urls = ""
    for news in top_news(news_api())[0]:
        stories += news + "\n"
    for url in top_news(news_api())[1]:
        urls += url + "\n"
    if stories == "":
        stories = "An error has occurred, see logging for more details"
    notif_list.clear()
    notif_list.append(dict(title="COVID Update", content=national_covid_cases()))
    notif_list.append(dict(title="News Update", content=(stories + urls)))
    notif_list.append(dict(title="Weather Update", content=weather))
    # Log notifications update
    logging.info("Notifications were updated")


def covid_rate(notif_list: list) -> None:
    """Checks to see if the number of covid_alarm_clock cases has passed a certain threshold"""
    response = requests.get("https://api.coronavirus.data.gov.uk/v1/data", params=api.api_params, timeout=10)
    new_cases = api.get_json()["data"][0]['newCasesByPublishDate']
    if response.status_code != 200:
        logging.error(response.json()['response'])
        return None
    if new_cases >= threshold:
        content = "The number of new covid_alarm_clock cases in Exeter has passed " + str(threshold) + " and is now " + \
                  str(new_cases)
        notif_list.append(dict(title="COVID Threshold", content=content))


# List containing notification dictionaries
notification_list = []
# List containing alarm dictionaries
alarm_list = []
# We call period_notif which will add hourly updates to our notification list
period_notif(notification_list)


# Initialise web page
@app.route('/')
@app.route('/index')
def schedule_event() -> None:
    """This functions retrieves user input arguments : alarm time, include news, include weather and creates alarms and
        notifications depending on the user input.

        Alarms are defined using sched and time modules. The content of alarms are then announced by a text-to-speech
        using pyttsx3 module. Alarms can contain covid_alarm_clock, news and weather updates.

        Notifications are defined using sched and time modules. The content of notifications are then displayed via text
        on the alarm web page. Notifications are updated automatically periodically.

        Returns None
    """
    s.run(blocking=False)
    # Get time and date set by user : returns None if no input was made
    alarm_time = request.args.get("alarm")
    # Alarm title
    label = request.args.get("two")
    # Returns not None if user decides to include a news update and/or weather update to alarm
    if_news = request.args.get("news")
    if_weather = request.args.get("weather")
    # If user presses "x" on alarm or notification, returns not None
    eject_alarm = request.args.get("alarm_item")
    eject_notif = request.args.get("notif")
    # The numerical day today
    today = str(time.strftime("%d %m", time.localtime())).split(" ")
    if alarm_time:
        # convert alarm_time to a delay using function from time_conversion
        alarm_day = alarm_time.split("T")[0].split("-")[2]
        alarm_month = alarm_time.split("T")[0].split("-")[1]
        alarm_time = alarm_time.split("T")[1]
        current_time = str(time.strftime("%H:%M", time.localtime()))
        delay = hhmm_to_seconds(alarm_time) - hhmm_to_seconds(current_time)
        # Explains content of alarm dependent on what user asked
        content = "Alarm set for the " + str(alarm_day) + "-" + str(alarm_month) + " at " + str(alarm_time) + \
                  " and contains daily covid_alarm_clock update "
        if if_weather is None and if_news is not None:
            content = "Alarm set for the " + str(alarm_day) + "-" + str(alarm_month) + " at " + str(alarm_time) + \
                      " and contains daily covid_alarm_clock update " + if_news
        if if_news is None and if_weather is not None:
            content = "Alarm set for the " + str(alarm_day) + "-" + str(alarm_month) + " at " + str(alarm_time) + \
                      " and contains daily covid_alarm_clock update " + if_weather
        if if_news is not None and if_weather is not None:
            content = "Alarm set for the " + str(alarm_day) + "-" + str(alarm_month) + " at " + str(alarm_time) + \
                      " and contains daily covid_alarm_clock update " + if_weather + " " + if_news
        # We add an alarm dictionary to our alarm
        alarm_list.append(
            dict(title=label, content=content, news=if_news, weather=if_weather, day=alarm_day, month=alarm_month,
                 delay=int(delay), scheduled=False))
        # Log new alarm clock
        logging.info("An alarm was created for " + str(alarm_time) + " on the " + str(alarm_day) + "-" +
                     str(alarm_month))
    # We go through our alarms list to check for possible alarms to set today
    for alarms in alarm_list:
        if eject_alarm == alarms['title']:
            # Removes alarm if user clicked "x"
            alarm_list.remove(alarms)
            # Log alarm removal
            logging.info("Alarm " + alarms['title'] + " was removed from alarms list")
        if alarms['day'] == today[0] and alarms['month'] == today[1]:
            # Checks if alarm is set for today
            if not alarms['scheduled']:
                # Checks if alarm has already be scheduled
                if if_news is not None:
                    s.enter(alarms['delay'], 1, read_news)
                if if_weather is not None:
                    # Set scheduler to read news and weather
                    s.enter(alarms['delay'], 1, loc_weather)
                # Set scheduler to read covid_alarm_clock update
                s.enter(alarms['delay'], 1, local_covid_cases)
                alarms['scheduled'] = True
    # We go through the notif list to remove notifications where user clicked "x"
    for notifs in notification_list:
        if eject_notif == notifs['title']:
            notification_list.remove(notifs)
            logging.info("Notification " + notifs['title'] + " was removed from notification list")
    # Check if threshold has been passed
    covid_rate(notification_list)

    return render_template('template.html', title="Alarm clock", image='favicon.jpg', alarms=alarm_list,
                           notifications=notification_list)


if __name__ == '__main__':
    app.run()
