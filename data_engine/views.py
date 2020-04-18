from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from googletrans import Translator

translator = Translator()

BASE_URL = "https://corona.lmao.ninja/v2/"
# Create your views here.


def get_global_data():
    """ Returns global count of total cases, recovery, and deaths. """
    req1 = requests.get(BASE_URL + f"all")
    req2 = requests.get(BASE_URL + f"all", params={"yesterday": True})
    if req1.status_code == 200 and req2.status_code == 200:
        return {"today": req1.json(), "yesterday": req2.json()}
    else:
        return None


def get_top_10_data(sort_by="cases"):
    req = requests.get(BASE_URL + f"countries?sort={sort_by}")
    if req.status_code == 200:
        return req.json()
    else:
        return None


def get_country_data(country="India"):
    """Returns data of a specific country."""
    req1 = requests.get(BASE_URL + f"countries/{country}", params={"yesterday": False})
    req2 = requests.get(BASE_URL + f"countries/{country}", params={"yesterday": True})
    if req1.status_code == 200 and req2.status_code == 200:
        return {"today": req1.json(), "yesterday": req2.json()}
    else:
        return None


def get_indian_state_data(state="Maharashtra"):
    """" Returns data of specific state from Maharashtra in India. """
    url = "https://api.covid19india.org/state_district_wise.json"
    payload = {}
    headers = {}
    req = requests.request("GET", url, headers=headers, data=payload)
    if req.status_code == 200:
        return req.json()[state]['districtData']
    else:
        return None
