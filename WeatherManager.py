import requests
from datetime import datetime, timezone, timedelta
class WeatherManager:
    def __init__(self, key_api):
        self.key_api = key_api
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather?'
    def get_weather(self,city):

            params = {
                'q': city,
                'appid': self.key_api,
                'units': 'metric',
                'lang': 'pl'
            }
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                utc_time = datetime.now(timezone.utc)
                local_city_time=utc_time+timedelta(seconds=data['timezone'])
                formatted_time=local_city_time.strftime('%H:%M')

                return {
                    "temp": data['main']['temp'],
                    "opis": data['weather'][0]['description'],
                    "wilgotnosc": data['main']['humidity'],
                    "icon_code": data['weather'][0]['icon'],
                    "lat": data['coord']['lat'],
                    "lon": data['coord']['lon'],
                    "czas": formatted_time
                }
            except requests.exceptions.HTTPError:
                print("Nie znaleziono takiego miasta. Spróbuj ponownie.")
            except Exception as e:
                print(f"Wystąpił błąd: {e}")
                return None

    def get_air_quality(self, lat, lon):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.key_api}"
        try:
            response = requests.get(url)
            data = response.json()

            aqi = data['list'][0]['main']['aqi']

            skala = {
                1: ("Świetna", "#2ecc71"),
                2: ("Dobra", "#f1c40f"),
                3: ("Umiarkowana", "#e67e22"),
                4: ("Zła", "#e74c3c"),
                5: ("Bardzo zła", "#8e44ad")
            }
            return skala.get(aqi, "Nieznana")
        except:
            return "Brak danych"