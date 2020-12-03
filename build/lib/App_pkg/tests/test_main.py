"""This module will test different components of the main module such as news, weather and covid_alarm_clock API"""

import requests
import json
from uk_covid19 import Cov19API
import os
from App_pkg.main import news_api
from App_pkg.main import top_news
from App_pkg.main import config_path
from App_pkg.main import weather_api


# Opening config file

with open(config_path, 'r') as f:
    test_json_file = json.load(f)
test_keys = test_json_file["API_keys"]
test_location = test_json_file["Location"]
test_sources = test_json_file["News-sources"]
test_covid_struct = {
    "cases_and_deaths": {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }
}


def test_covid_api() -> None:
    """Tests if Uk Gov. Covid Api is working as expected"""
    test_api = Cov19API(
        filters=["areaName=" + test_location["my-city"]],
        structure=test_covid_struct["cases_and_deaths"],
        latest_by="newCasesByPublishDate"
    )
    response = requests.get("https://api.coronavirus.data.gov.uk/v1/data", params=test_api.api_params, timeout=10)
    assert response.status_code == 200


def test_weather_api() -> None:
    """Test if weather Api is working as expected"""
    response = weather_api()
    assert response.status_code == 200


def test_news_api() -> None:
    """Test if news Api is working as expected"""
    assert (news_api())['status'] == 'ok'


def test_top_news():
    """Test if top_news reads dictionary correctly"""
    test_news_file = (os.path.dirname(__file__))+"/gb-news.json"
    with open(test_news_file, 'r') as f:
        test_news = json.load(f)
    assert top_news(test_news) == (["Pandora paying all staff in full through pandemic - BBC News"],
                                   ["https://www.bbc.com/news/business-54862615"])