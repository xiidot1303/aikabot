from datetime import datetime, date, timedelta
import requests
import json
import random
import string
from yandex_geocoder import Client
from decimal import Decimal
from geopy.geocoders import Nominatim

async def get_user_ip(request):
    x_forwarded_for = await request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = await request.META.get('REMOTE_ADDR')
    return ip

async def datetime_now():
    now = datetime.now()
    return now

async def time_now():
    now = datetime.now()
    return now.time()

async def today():
    today = date.today()
    return today

async def send_request(url, data=None, headers=None, type='get'):
    if type == 'get':
        response = requests.get(url, params=data, headers=headers)
        content = json.loads(response.content)
        headers = response.headers
    else:
        response = requests.post(url, json=data, headers=headers)
        content = json.loads(response.content)
        headers = response.headers

    return content, headers


async def generate_random_symbols(length):
    symbols = string.ascii_letters + string.digits
    return ''.join(random.choice(symbols) for _ in range(length))

async def get_address_by_coordinates(lat, lon):
    try:
        geolocator = Nominatim(user_agent="AIKAbot")
        location = geolocator.reverse((lat, lon), language="ru")
        address = location.address
    except Exception as ex:
        print(ex)
        address = None
    return address

async def generate_google_map_link(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"