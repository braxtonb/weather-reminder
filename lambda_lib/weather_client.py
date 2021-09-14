import os
import json
import datetime
import requests

class WeatherClient:
    OPEN_WEATHER_MAP_API = os.getenv('OPEN_WEATHER_MAP_API')
    DEFAULT_ZIP_CODE = '10021'

    @classmethod
    def get_four_day_forecast(cls, zip_code=None):
        if not zip_code:
            zip_code = cls.DEFAULT_ZIP_CODE

        try:
            # api.openweathermap.org/data/2.5/forecast?zip={zip code},{country code}&appid={API key}
            URL = f'https://api.openweathermap.org/data/2.5/forecast?zip={zip_code}&units=imperial&appid={cls.OPEN_WEATHER_MAP_API}'

            r = requests.get(URL)

            return r.json()
        except requests.exceptions.RequestException as e:
            print('Unable to get 4 day forecast')
            print(str(e))
            raise e

    @classmethod
    def get_five_day_three_hour_step_forecast_formatted(cls, zip_code=None) -> str:
        if not zip_code:
            zip_code = cls.DEFAULT_ZIP_CODE

        forecasts = cls.get_four_day_forecast(zip_code)
        city_name = forecasts['city']['name']
        formatted_forecasts = []

        # track 12 hour forecast each day
        for i in range(0, len(forecasts['list']), 4):
            forecast = forecasts['list'][i]

            try:
                forecast_datetime = datetime.datetime.fromtimestamp(forecast['dt'])
                forecast['dt_formatted'] = f'{forecast_datetime:%a, %b %d %-I:%M %p}'
                forecast['weather_description'] = forecast['weather'][0]['description']
                forecast['weather_icon'] = cls.get_icon_url(forecast['weather'][0]['icon'])

                del forecast['dt']
                del forecast['dt_txt']
                del forecast['weather']

                formatted_forecasts.append(forecast)
            except KeyError as e:
                print(str(e))
                print('Unable to parse keys, skipping forecast')
            except Exception as e:
                print(str(e))
                print('Unable to format, skipping forecast')

        return json.dumps({'city_name': city_name, 'forecasts': formatted_forecasts})

    @classmethod
    def get_icon_url(cls, icon):
        return f'https://openweathermap.org/img/wn/{icon}@2x.png'