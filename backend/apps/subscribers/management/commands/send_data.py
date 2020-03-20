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

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

class Command(BaseCommand):
    help = 'Displays current time'

    def get_percent_increase(self, today, yesterday):
        if yesterday == 0:
            return 100
        return round(100 * ((today - yesterday) / yesterday), 2)

    def handle(self, *args, **kwargs):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        newsapi = NewsApiClient(api_key='73f7c089599649bba9b424d607de2c38')
        bitly_auth_token = requests.post(
            'https://api-ssl.bitly.com/oauth/access_token', auth=(BITLY_ACCOUNT, BITLY_PASSWORD)).text
        c = bitly_api.Connection(access_token=bitly_auth_token)
        
        articles = {
            'business': newsapi.get_top_headlines(
                country='us', category='business', q='coronavirus')['articles'][:1],
            'science' :newsapi.get_top_headlines(
                country='us', category='science', q='coronavirus')['articles'][:1],
            'health': newsapi.get_top_headlines(
                country='us', category='health', q='coronavirus')['articles'][:1],
            'sports' :newsapi.get_top_headlines(
                country='us', category='sports', q='coronavirus')['articles'][:1]
        }
        for key in articles:
            for article in articles[key]:
                article['url'] = c.shorten(article['url'])['url']
            
        today = datetime.date.today() - datetime.timedelta(days=1)
        yesterday = (today - datetime.timedelta(days=1)).strftime("%m-%d-%Y")
        today = today.strftime("%m-%d-%Y")

        
        data = requests.get(
            f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{today}.csv')
        while data.status_code == 404:
            print('waiting for update')
            print('sleeping for 60 seconds')
            time.sleep(60)
            data = requests.get(
                f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{today}.csv')
        else:
            print('ready!')
        todays_data = list(csv.DictReader(data.text.splitlines()))
        data = requests.get(
            f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{yesterday}.csv')
        yesterdays_data = list(csv.DictReader(data.text.splitlines()))
        world_data = {
            'confirmed': sum(map(lambda latest: int(latest['Confirmed']), todays_data)),
            'last_confirmed': sum(map(lambda latest: int(latest['Confirmed']), yesterdays_data)),
            'deaths': sum(map(lambda latest: int(latest['Deaths']), todays_data)),
            'last_deaths': sum(map(lambda latest: int(latest['Deaths']), yesterdays_data)),
            'recovered': sum(map(lambda latest: int(latest['Recovered']), todays_data)),
            'last_recovered': sum(map(lambda latest: int(latest['Recovered']), yesterdays_data)),
        }

        world_data['confirmed_increase'] = self.get_percent_increase(world_data['confirmed'], world_data['last_confirmed'])
        world_data['recovered_increase'] = self.get_percent_increase(world_data['recovered'], world_data['last_recovered'])
        world_data['deaths_increase'] = self.get_percent_increase(world_data['deaths'], world_data['last_deaths'])

        
        for sub in Subscriber.objects.filter(verified=True):
            location = json.loads(sub.location)
            country_code = pycountry.countries.search_fuzzy(location.get('country'))[0].alpha_2

            today_country_locations = [
                location for location in todays_data if (location['Country/Region'] == country_code or location['Country/Region'] == location.get('country'))]
            last_country_locations = [
                location for location in yesterdays_data if (location['Country/Region'] == country_code or location['Country/Region'] == location.get('country'))]
            country_data = {
                'name': location.get('country'),
                'confirmed': sum(map(lambda latest: int(latest['Confirmed']), today_country_locations)),
                'last_confirmed': sum(map(lambda latest: int(latest['Confirmed']), last_country_locations)),
                'recovered': sum(map(lambda latest: int(latest['Recovered']), today_country_locations)),
                'last_recovered': sum(map(lambda latest: int(latest['Recovered']), last_country_locations)),
                'deaths': sum(map(lambda latest: int(latest['Deaths']), today_country_locations)),
                'last_deaths': sum(map(lambda latest: int(latest['Deaths']), last_country_locations))
            }
            country_data['confirmed_increase'] = self.get_percent_increase(country_data['confirmed'], country_data['last_confirmed'])
            country_data['recovered_increase'] = self.get_percent_increase(country_data['recovered'], country_data['last_recovered'])
            country_data['deaths_increase'] = self.get_percent_increase(country_data['deaths'], country_data['last_deaths'])

            if location['country'] == 'United States':
                state = abbrev_us_state[location['administrative_area_level_1']]
            else: 
                state = location['administrative_area_level_1']

            state_data = [
                location for location in today_country_locations if location['Province/State'] == state][0]
            last_state_data = [
                location for location in last_country_locations if location['Province/State'] == state][0]

            state_confirmed_increase = self.get_percent_increase(int(state_data['Confirmed']), int(last_state_data['Confirmed']))
            state_recovered_increase = self.get_percent_increase(int(state_data['Recovered']), int(last_state_data['Recovered']))
            state_death_increase = self.get_percent_increase(int(state_data['Deaths']), int(last_state_data['Deaths']))

            if sub.option:
                option_string = "To stop receiveing news articles, simply reply \"RESET\""
            else:
                option_string = "To add news articles to your daily updates, reply \"RENEW\""

            message = f""" \n
COVID-19 Updater \n
---------------- \n
World Data:  \n
    Confirmed: { world_data['confirmed']} \n
    { world_data['confirmed_increase']}% change \n
    Deaths: { world_data['deaths']}\n
    { world_data['deaths_increase']}% change \n
    Recoverd: {world_data['recovered']}\n
    { world_data['recovered_increase']}% change \n
\n
{ country_data['name']}: \n
    Confirmed: { country_data['confirmed']} \n
    { country_data['confirmed_increase']}% change \n
    Deaths: { country_data['deaths']}\n
    { country_data['deaths_increase']}% change \n
    Recoverd: {country_data['recovered']}\n
    { country_data['recovered_increase']}% change \n
\n
{ state }: \n
    Confirmed: { state_data['Confirmed']} \n
    { state_confirmed_increase}% change \n
    Deaths: { state_data['Deaths']}\n
    { state_death_increase}% change \n
    Recoverd: {state_data['Recovered']}\n
    { state_recovered_increase}% change \n
    
\n

At anytime, text "STOP" to unsubscribe from this number. \n
{option_string}
"""         
            client.messages.create(
                    body=message,
                    from_="13523204710",
                    to=sub.telephone
                )
            if sub.option:
                message = f"""
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
                client.messages.create(
                    body=message,
                    from_="13523204710",
                    to=sub.telephone
                )


