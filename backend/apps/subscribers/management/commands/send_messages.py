from django.core.management.base import BaseCommand
import requests
import json
import csv
from apps.subscribers.models import Subscriber
import pycountry
from pprint import pprint
from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from config.settings import BITLY_ACCOUNT, BITLY_PASSWORD
from twilio.rest import Client
from newsapi import NewsApiClient
import bitly_api
import datetime
import time
import pytz

from .states import abbrev_us_state
from .country_codes import country_code as get_country_code

east = pytz.timezone('US/Eastern')

class Command(BaseCommand):
    help = 'Sends out messages to subscribers'

    ####### API / Data Setup #########
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # API Clients
        self.twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        newsapi = NewsApiClient(api_key='73f7c089599649bba9b424d607de2c38')
        bitly_auth_token = requests.post(
            'https://api-ssl.bitly.com/oauth/access_token', auth=(BITLY_ACCOUNT, BITLY_PASSWORD)).text
        bitly = bitly_api.Connection(access_token=bitly_auth_token)

        # Gather articles for the day
        articles = {
            'business': newsapi.get_top_headlines(
                country='us', category='business', q='coronavirus')['articles'][:1],
            'science': newsapi.get_top_headlines(
                country='us', category='science', q='coronavirus')['articles'][:1],
            'health': newsapi.get_top_headlines(
                country='us', category='health', q='coronavirus')['articles'][:1],
            'sports': newsapi.get_top_headlines(
                country='us', category='sports', q='coronavirus')['articles'][:1]
        }

        # Shorten urls for message
        for key in articles:
            for article in articles[key]:
                article['url'] = bitly.shorten(article['url'])['url']

        self.news_message = f"""
News Articles
-------------
Science:
{articles['science'][0]['title']}
{articles['science'][0]['url']}

Business:
{articles['business'][0]['title']}
{articles['business'][0]['url']}

Health:
{articles['health'][0]['title']}
{articles['health'][0]['url']}

Sports:
{articles['sports'][0]['title']}
{articles['sports'][0]['url']}
"""

        # Gather dates for data fetching
        today = datetime.datetime.now(east).today() - datetime.timedelta(days=1)
        self.yesterday = (today - datetime.timedelta(days=1)).strftime("%m-%d-%Y")
        self.today = today.strftime("%m-%d-%Y")
        

    ######## Utility functions ###########

    def get_percent_increase(self, today, yesterday):
        # Returns a string of the percent increase to be used in the message
        if yesterday == today:
            return 'No change'
        elif yesterday == 0:
            return f"100% increase"
        else:
            percent = round(100 * ((today - yesterday) / yesterday), 2)
            if percent > 0:
                return f'{percent}% increase'
            else:
                percent = abs(percent)
                return f'{percent}% decrease'

    def data_ready(self):
        # Wait until the data repo has updated
        data = requests.get(
            f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{self.today}.csv')
        while data.status_code != 200: 
            print('waiting for update')
            print('sleeping for 60 seconds')
            time.sleep(60)
            data = requests.get(
                f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{self.today}.csv')
        else:
            return True

    def format_data(self, date):
        data = requests.get(
            f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv')
        ## parse the csv into a list of dictionaries, each dict is a "location"
        return list(csv.DictReader(data.text.splitlines()))

    def collect_data(self, todays_data, yesterdays_data, name='World'):
        # Take the sum of the total confirmed, dead
        # Default name to world unless country is specified
        data = {
            'name': name,
            'confirmed': sum(map(lambda latest: int(latest['Confirmed']), todays_data)),
            'last_confirmed': sum(map(lambda latest: int(latest['Confirmed']), yesterdays_data)),
            'deaths': sum(map(lambda latest: int(latest['Deaths']), todays_data)),
            'last_deaths': sum(map(lambda latest: int(latest['Deaths']), yesterdays_data)),
            'recovered': sum(map(lambda latest: int(latest['Recovered']), todays_data)),
            'last_recovered': sum(map(lambda latest: int(latest['Recovered']), yesterdays_data)),
        }

        data['confirmed_increase'] = self.get_percent_increase(data['confirmed'], data['last_confirmed'])
        data['recovered_increase'] = self.get_percent_increase(data['recovered'], data['last_recovered'])
        data['deaths_increase'] = self.get_percent_increase(data['deaths'], data['last_deaths'])

        return data

    def get_country_locations(self, data, sub_location):
        country_code = get_country_code(sub_location.get('country'))
        return [location for location in data if (location['Country/Region'] == country_code or location['Country/Region'] == sub_location.get('country'))]

    def get_state_name(self, location):
        # States are abbreviated, provinces are not.
        if location['country'] == 'United States':
            state = abbrev_us_state[location['administrative_area_level_1']]
        else:
            state = location['administrative_area_level_1']
        return state

    def set_option_string(self, option):
        # option means the sub is subscribed to news articles
        if option:
            option_string = "To stop receiveing news articles, simply reply \"RESET\""
        else:
            option_string = "To add news articles to your daily updates, reply \"RENEW\""
        return option_string

    ######## Main Fucntion ##############

    def handle(self, *args, **kwargs):
        if self.data_ready():
            todays_data = self.format_data(self.today)
            yesterdays_data = self.format_data(self.yesterday)
            world_data = self.collect_data(todays_data, yesterdays_data)

            # Initialize message and subscribers
            update_bindings = []
            news_bindings = []
            update_message = ""

            # Loop through each subscriber to gather the data about their country / province

            # TODO: Find efficient way to gather data by grouping subs into countries and / or states
            for sub in Subscriber.objects.filter(verified=True):
                # Safety net try/catch, will remove after more testing
                try:
                    location = json.loads(sub.location) # create sub_location object

                    # get all states/provinces in country
                    today_country_locations = self.get_country_locations(todays_data, location)
                    last_country_locations = self.get_country_locations(yesterdays_data, location)

                    country_data = self.collect_data(today_country_locations, last_country_locations, location.get('country'))

                    state = self.get_state_name(location)
                  
                    # Single state/province already in dict format so no need to use collect_data
                    state_data = [location for location in today_country_locations if location['Province/State'] == state][0]
                    last_state_data = [location for location in last_country_locations if location['Province/State'] == state][0]

                    state_confirmed_increase = self.get_percent_increase(int(state_data['Confirmed']), int(last_state_data['Confirmed']))
                    state_recovered_increase = self.get_percent_increase(int(state_data['Recovered']), int(last_state_data['Recovered']))
                    state_death_increase = self.get_percent_increase(int(state_data['Deaths']), int(last_state_data['Deaths']))

                    option_string = self.set_option_string(sub.option)


                    update_message = f""" \n
COVID-19 Updater \n
---------------- \n
World Data:  \n
    Confirmed: { world_data['confirmed']} \n
    { world_data['confirmed_increase']} \n
    Deaths: { world_data['deaths']}\n
    { world_data['deaths_increase']}\n
    Recovered: {world_data['recovered']}\n
    { world_data['recovered_increase']}\n
\n
{ country_data['name']}: \n
    Confirmed: { country_data['confirmed']} \n
    { country_data['confirmed_increase']} \n
    Deaths: { country_data['deaths']}\n
    { country_data['deaths_increase']} \n
    Recovered: {country_data['recovered']}\n
    { country_data['recovered_increase']} \n
\n
{ state }: \n
    Confirmed: { state_data['Confirmed']} \n
    { state_confirmed_increase} \n
    Deaths: { state_data['Deaths']}\n
    { state_death_increase} \n
    Recovered: {state_data['Recovered']}\n
    { state_recovered_increase} \n
\n
At anytime, text "STOP" to unsubscribe from this number. \n
{option_string}
"""
                    # Create binding to send news bulk_text later
                    # Also send out unique update message
                    try:
                        binding = {
                            'binding_type': 'sms',
                            'address': sub.telephone
                        }
                        formatted_binding = json.dumps(binding)
                        
                        self.twilio.messages.create(
                            body=update_message,
                            from_="13523204710",
                            to=sub.telephone
                        )
                        if sub.option:
                            news_bindings.append(formatted_binding)
                    except Exception as e:
                        pass
                        # TODO: logs
                except Exception as e:
                    print(e)

        # Send out bulk news sms
        news = self.twilio.notify.services("IS5bfdb269815ad63f80b3ffa5414299f9")\
            .notifications.create(
            to_binding=news_bindings,
            body=self.news_message)










        
