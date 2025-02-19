
import requests
import json
from bs4 import BeautifulSoup

def get_html(url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'}
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    # print(response.text)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)
    return response.text

def get_weather(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    date = soup.find_all('div', class_='dates short-d')[0].text
    weather = {}

    table = soup.find('table', class_='weather-today short')
    rows = table.find_all('tr')
    weather[date] = {}

    for row in rows:
        weather_day=row.find('td', class_='weather-day').text
        conditions = row.find('td',class_='weather-temperature').find('div')['title']
        feeling =row.find('td',class_='weather-feeling').text
        probability = row.find('td',class_='weather-probability').text
        pressure = row.find('td', class_='weather-pressure').text
        wind_direction = row.find('td',class_='weather-wind').find_all('span')[0]['title']
        wind_speed = row.find('td',class_='weather-wind').find_all('span')[1].text
        humidity = row.find('td',class_='weather-humidity').text
        weather[date][weather_day] = {
            'conditions': conditions,
            'feeling': feeling,
            'probability': probability,
            'pressure': pressure,
            'wind_direction': wind_direction,
            'wind_speed': wind_speed,
            'humidity': humidity
        }
    return weather

def write_weather_json (weather: dict):
    with open ('weather.json', 'w', encoding='utf-8') as file:
        json.dump(weather, file, indent=2, ensure_ascii=False)


# soup.find
# soup.find_all

URL = 'https://world-weather.ru/pogoda/russia/saint_petersburg/7days/'
html = get_html(url=URL)
weather = get_weather(html)
write_weather_json(weather)


# отладка
# оператор распаковки *
# print(*rows, sep='\n')
