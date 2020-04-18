from data_engine.views import get_global_data, get_country_data, get_indian_state_data
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from translator.views import detect_lang, translate
from .utils import countries, indian_states_list
from twilio.rest import Client
from django.conf import settings
# Create your views here.

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


@csrf_exempt
def message_processor(request):
    msg = request.POST.get('Body', '')
    request_lang = detect_lang(msg)
    if request_lang in ['hi', 'mrhi', 'himr', 'mr']: request_lang = 'mr'
    to_translate = True if request_lang != 'en' else False
    message = translate(msg, 'en') if to_translate else msg
    if message.lower() in ['all', 'global', 'world']:
        data = data_processor(1)
        if data is not None:
            response = response_builder(1, request_lang, data=data)
        else:
            response_builder(0, request_lang)
    elif message.lower() == 'top 10':
        data = data_processor(2)
        if data is not None:
            response = response_builder(2, request_lang, data=data)
        else:
            response = response_builder(0, request_lang)
    elif message in countries:
        data = data_processor(3, country=message)
        if to_translate: message = translate(message, lang=request_lang)
        if data is not None:
            response = response_builder(3, request_lang, data=data, country=message.capitalize())
        else:
            response = response_builder(0, request_lang)
    elif message in indian_states_list:
        data = data_processor(4, state=message)
        if to_translate: message = translate(message, lang=request_lang)
        if data is not None:
            response = response_builder(4, request_lang, data=data, state=message)
        else:
            response = response_builder(0, request_lang)
    else:
        response = response_builder(0, request_lang)
    response_message = MessagingResponse()
    response_message.message(response)
    return HttpResponse(str(response_message))


def data_processor(requested_data, state=None, country=None):
    if requested_data == 1:
        data = get_global_data()
    elif requested_data == 2:
        pass
    elif requested_data == 3:
        data = get_country_data(country)
    elif requested_data == 4:
        data = get_indian_state_data(state=state)
    return data


def response_builder(requested_data, language, data=None, state=None, country=None):
    if requested_data == 0:
        error_message = {
            'mr': f"काही त्रुटी आली आहे. कृपया पुन्हा प्रयत्न करा.",
            'en': f"An error has occurred. Please try again."
        }
        response = error_message[language]
    elif requested_data == 1:
        total_cases = data['today']['cases']
        active_cases = data['today']['active']
        recovered_cases = data['today']['recovered']
        total_deaths = data['today']['deaths']
        yesterday_total_cases = data['yesterday']['cases']
        yesterday_active_cases = data['yesterday']['active']
        yesterday_recovered_cases = data['yesterday']['recovered']
        yesterday_total_deaths = data['yesterday']['deaths']
        all_details_message = {
            'mr': f"जगातील कोरोणा व्हायरसची (कोविड-19) माहीती:\n\n "
                  f":::: आजचा डेटा ::::\n"
                  f"टोटल संख्या: {total_cases}\n "
                  f"सक्रिय संख्या: {active_cases}\n"
                  f"बरे झालेल्यांची संख्या: {recovered_cases}\n"
                  f"टोटल मृत्यूंची संख्या: {total_deaths}\n\n"
                  f":::: कालचा डेटा ::::\n"
                  f"टोटल संख्या: {yesterday_total_cases}\n "
                  f"सक्रिय संख्या: {yesterday_active_cases}\n"
                  f"बरे झालेल्यांची संख्या: {yesterday_recovered_cases}\n"
                  f"टोटल मृत्यूंची संख्या: {yesterday_total_deaths}\n\n\n"
                  f"अस्वीकरणः ही माहिती एका एपीआय वरून दिली गेली आहे, ज्यांचे सूत्र \n"
                  f"https://www.worldometers.info/coronavirus/ \nवेबसाइट आहे. ",
            'en': f"Global covid19 information:\n\n"
                  f":::: Today's Data ::::\n"
                  f"Total cases: {total_cases}\n "
                  f"Active cases: {active_cases}\n "
                  f"Recovered cases: {recovered_cases}\n"
                  f"Total deaths: {total_deaths}\n\n"
                  f":::: Yesterday's Data ::::\n"
                  f"Total cases: {yesterday_total_cases}\n "
                  f"Active cases: {yesterday_active_cases}\n "
                  f"Recovered cases: {yesterday_recovered_cases}\n"
                  f"Total deaths: {yesterday_total_deaths}\n\n\n"
                  f"Disclaimer: The info is brought to you from an API, who's source is\n "
                  f"https://www.worldometers.info/coronavirus/ \n"
        }
        response = all_details_message[language]
    elif requested_data == 2:
        pass
    elif requested_data == 3:
        total_cases = data['today']['cases']
        today_cases = data['today']['todayCases']
        active_cases = data['today']['active']
        recovered_cases = data['today']['recovered']
        critical_cases = data['today']['critical']
        total_deaths = data['today']['deaths']
        today_deaths = data['today']['todayDeaths']
        yesterday_total_cases = data['yesterday']['cases']
        yesterday_today_cases = data['yesterday']['todayCases']
        yesterday_active_cases = data['yesterday']['active']
        yesterday_recovered_cases = data['yesterday']['recovered']
        yesterday_critical_cases = data['yesterday']['critical']
        yesterday_total_deaths = data['yesterday']['deaths']
        yesterday_today_deaths = data['yesterday']['todayDeaths']
        country_specific_message = {
            'mr': f"{country} मधील कोरोणा व्हायरसची माहीत:\n\n"
                  f":::: आजचा डेटा ::::\n"
                  f"टोटल संख्या: {total_cases}\n "
                  f"नवीन केसेस नोंदवले: {today_cases}\n"
                  f"सक्रिय संख्या: {active_cases}\n "
                  f"बरे झालेल्यांची संख्या: {recovered_cases}\n"
                  f"गांभीर्यांची संख्या:{critical_cases}\n"
                  f"टोटल मृत्यूंची संख्या: {total_deaths}\n "
                  f"मृत्यूंची संख्या: {today_deaths}\n\n"
                  f":::: कालचा डेटा ::::\n"
                  f"टोटल संख्या: {yesterday_total_cases}\n "
                  f"नवीन केसेस नोंदवले: {yesterday_today_cases}\n"
                  f"सक्रिय संख्या: {yesterday_active_cases}\n "
                  f"बरे झालेल्यांची संख्या: {yesterday_recovered_cases}\n"
                  f"गांभीर्यांची संख्या:{yesterday_critical_cases}\n"
                  f"टोटल मृत्यूंची संख्या: {yesterday_total_deaths}\n "
                  f"मृत्यूंची संख्या: {yesterday_today_deaths}\n\n\n"
                  f"अस्वीकरणः ही माहिती एका एपीआय वरून दिली गेली आहे, ज्यांचे स्रोत \n"
                  f"https://www.worldometers.info/coronavirus/ \nवेबसाइट आहे. ",
            'en': f"{country}'s corona virus (COVID-19) Info: \n\n"
                  f":::: Today's Data ::::\n"
                  f"Total cases: {total_cases}\n"
                  f"New cases reported: {today_cases}\n"
                  f"Active cases: {active_cases}\n"
                  f"Recovered cases: {recovered_cases}\n"
                  f"Critical cases: {critical_cases}\n"
                  f"Total deaths: {total_deaths}\n"
                  f"Deaths: {today_deaths}\n\n"
                  f"::::Yesterday's Data::::\n"
                  f"Total cases: {yesterday_total_cases}\n"
                  f"New cases reported: {yesterday_today_cases}\n"
                  f"Active cases: {yesterday_active_cases}\n"
                  f"Recovered cases: {yesterday_recovered_cases}\n"
                  f"Critical cases: {yesterday_critical_cases}\n"
                  f"Total deaths: {yesterday_total_deaths}\n"
                  f"Deaths: {yesterday_today_deaths}\n\n\n"
                  f"Disclaimer: The info is brought to you from an API, who's source is\n "
                  f"https://www.worldometers.info/coronavirus/ \n"
        }
        response = country_specific_message[language]
    elif requested_data == 4:
        if language == 'mr': language = 'hi'
        translated_state = translate(state, language)
        state_specific_message = {
            "hi": {
                'initial': f"\n\nजिल्ह्या नुसार {translated_state}ची माहिती.\n",
                'disclaimer': "\n\nवरील माहिती एपीआय द्वारे ह्या \n"
                              "https://www.covid19india.org/ संकेस्थळावरुन प्राप्त केली आहे.",
            },
            "en": {
                'initial': f"\n\nDistrict wise data of {translated_state} state:\n",
                'disclaimer': "\n\nThis information is sourced from an API of https://www.covid19india.org/ website."
            }
        }
        temp_list = [state_specific_message[language]['initial']]
        for district_name, district_data in sorted(data.items()):
            district_name = translate(district_name, language)
            temp_list.append(f"{district_name}: {district_data['confirmed']}\n")
        temp_list.append(state_specific_message[language]['disclaimer'])
        response = "".join(temp_list)
    return response


@csrf_exempt
def send_notification_to_all(request):
    users = [
        'whatsapp:+919561355450',
        'whatsapp:+919833838177',
        'whatsapp:+919260012001',
        'whatsapp:+919763793454',
        'whatsapp:+919527042054',
        'whatsapp:+919881382848',
        'whatsapp:+918830078097',
        'whatsapp:+919096081092'
    ]
    for user in users:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body="All errors have been fixed and now along with today's data, "
                 "you'll get yesterday's data as well.\n\n\n"
                 "सर्व त्रुटी फिक्स केल्या गेल्या आहेत आणि आता आजच्या डेटासह, आपल्याला कालचा डेटा देखील मिळेल.",
            to=user
        )
    return HttpResponse(str("Done"))
