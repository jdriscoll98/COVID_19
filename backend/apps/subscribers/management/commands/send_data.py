from django.core.management.base import BaseCommand
import requests
import json
from apps.subscribers.models import Subscriber
import pycountry
from pprint import pprint
from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
from newsapi import NewsApiClient
import bitly_api

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

    def handle(self, *args, **kwargs):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        newsapi = NewsApiClient(api_key='73f7c089599649bba9b424d607de2c38')
        api = "https://coronavirus-tracker-api.herokuapp.com/v2"
        world_data = requests.get(f"{api}/latest").json()['latest']
        locations = requests.get(f"{api}/locations").json()['locations']
        response = requests.post(
            'https://api-ssl.bitly.com/oauth/access_token', auth=('jackdriscoll777@gmail.com', 'Quavo2016!'))
        auth_token = response.text
        c = bitly_api.Connection(access_token=auth_token)
        
        articles = {
            'business': newsapi.get_top_headlines(
                country='us', category='business', q='coronavirus')['articles'][:3],
            'science' :newsapi.get_top_headlines(
                country='us', category='science', q='coronavirus')['articles'][:3],
            'entertainment': newsapi.get_top_headlines(
                country='us', category='entertainment', q='coronavirus')['articles'][:3],
            'sports' :newsapi.get_top_headlines(
                country='us', category='sports', q='coronavirus')['articles'][:3]
        }
        for key in articles:
            for article in articles[key]:
                article['url'] = c.shorten(article['url'])['url']
            

        for sub in Subscriber.objects.filter(verified=True):
            if sub.option == 'both' or sub.option == 'one':
                location = json.loads(sub.location)
                country_code = pycountry.countries.search_fuzzy(location.get('country'))[0].alpha_2
                country_locations = [location for location in locations if location['country_code'] == country_code]
                country_latest = list(map(lambda location: location['latest'], country_locations))
                country_data = {
                    'name': location.get('country'),
                    'confirmed': sum(map(lambda latest: latest['confirmed'], country_latest)),
                    'recovered': sum(map(lambda latest: latest['recovered'], country_latest)),
                    'deaths': sum(map(lambda latest: latest['deaths'], country_latest))
                }
                state = abbrev_us_state[location['administrative_area_level_1']]
                state_locations = [location for location in country_locations if location['province'] == state]
                state_latest = list(
                    map(lambda location: location['latest'], state_locations))
                state_data = {
                    'name': state,
                    'confirmed': sum(map(lambda latest: latest['confirmed'], state_latest)),
                    'recovered': sum(map(lambda latest: latest['recovered'], state_latest)),
                    'deaths': sum(map(lambda latest: latest['deaths'], state_latest))
                }
                message = f""" \n
COVID-19 Updater \n
---------------- \n
World Data:  \n
    Confirmed: { world_data['confirmed']} \n
    Deaths: { world_data['deaths']}\n
    Recoverd: {world_data['recovered']}\n
\n
{ country_data['name']}: \n
    Confirmed: { country_data['confirmed']} \n
    Deaths: { country_data['deaths']}\n
    Recoverd: {country_data['recovered']}\n
\n
{ state_data['name']}: \n
    Confirmed: { state_data['confirmed']} \n
    Deaths: { state_data['deaths']}\n
    Recoverd: {state_data['recovered']}\n
\n
"""
                client.messages.create(
                    body=message,
                    from_="13523204710",
                    to=sub.telephone
                )
            if sub.option == 'both' or sub.option == 'two':
                message = f"""
News Articles
-------------
Health / Science:
{articles['science'][0]['title']}
{articles['science'][0]['url']}

{articles['science'][1]['title']}
{articles['science'][1]['url']}

{articles['science'][2]['title']}
{articles['science'][2]['url']}


Business:
{articles['business'][0]['title']}
{articles['business'][0]['url']}

{articles['business'][1]['title']}
{articles['business'][1]['url']}

{articles['business'][2]['title']}
{articles['business'][2]['url']}

Entertainment:
{articles['entertainment'][0]['title']}
{articles['entertainment'][0]['url']}

{articles['entertainment'][1]['title']}
{articles['entertainment'][1]['url']}

{articles['entertainment'][2]['title']}
{articles['entertainment'][2]['url']}


Sports:
{articles['sports'][0]['title']}
{articles['sports'][0]['url']}

{articles['sports'][1]['title']}
{articles['sports'][1]['url']}

{articles['sports'][2]['title']}
{articles['sports'][2]['url']}

"""
                client.messages.create(
                    body=message,
                    from_="13523204710",
                    to=sub.telephone
                )


            





