import requests
from config import WEATHER_API_KEY
from helpers import ask_repeat

## ================= VARIABLES =====================
WIND_DIR_MAP = {
    'N': 'Northern', 'S': 'Southern', 'E': 'Eastern', 'W': 'Western',
    'NE': 'Northeastern', 'NW': 'Northwestern', 'SE': 'Southeastern', 'SW': 'Southwestern',
    'NNE': 'North-northeastern','ENE': 'East-northeastern', 'ESE': 'East-southeastern', 'SSE': 'South-southeastern',
    'SSW': 'South-southwestern','WSW': 'West-southwestern', 'WNW': 'West-northwestern', 'NNW': 'North-northwestern'
}
KEY_FILTERS_CURRENT_WEATHER = ['temp_c', 'condition', 'wind_kph', 'precip_mm', 'feelslike_c', "uv", "wind_dir",
                               'last_updated']
KEY_FILTERS_FORECAST_WEATHER = ['maxtemp_c', 'avgtemp_c', 'mintemp_c', 'totalprecip_mm', 'daily_will_it_rain',
                                'daily_chance_of_rain','condition', 'uv']

#================ FUNCTIONS =====================
def print_weather_menu():
    print(f"These are your options: \n"
          f"---------------------------\n"
          f'1. Get the current weather conditions\n'
          f"2. Get the weather forecast for today\n"
          f"3. Get clothing advice for today's weather forecast\n"
          f"4. Back\n")

# ============ GET WEATHER DATA FROM API ============
def get_weather_in_city(city):
    """
    Get data from weather api. Returns weather data or None on failure
    No check for status code -- will be handles in parse_weather_api
    :param city: city name string
    :return: json response OR None
    """

    API_KEY = WEATHER_API_KEY

    url = "http://api.weatherapi.com/v1/forecast.json?"
    params = {"key": API_KEY, "aqi": "no", "q":city}

    try:
        response = requests.get(url, params = params)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f'Error {e}')
        return None
    except ValueError:
        print(f'Invalid JSON response from API')
        return None


#============= PARSE WEATHER OUTPUT =================
def parse_weather_api(weather_data):
    """
    Normalize API response into standard format
    Handles errors from API. If statuscode != 200, the api should return JSON containing 'error'
    :param weather_data: json from weather api
    :return: {'found': bool, 'weather': dict, 'error': None or str
    """
    result = {'found': False, 'weather': {}, 'error': None}

    if weather_data is None:
        result['error'] = 'No data received from API'

    elif 'error' in weather_data:
        result['error'] = weather_data.get('error', {}).get('message', 'Unknown API error')

    elif 'location' in weather_data and 'forecast' in weather_data:
        result['found'] = True
        result['weather'] = weather_data

    else:
        print(f'Unexpected API response structure: {weather_data}')
        result['error'] = 'Unexpected API response structure'

    return result


#============= GET INPUT CITY AND CONFIRM CITY =============
def get_city():
    """
    Asks user for city name. Input cannot be empty
    :return: string
    """
    while True:
        city = input("Enter a city name to check the weather: ").strip()

        if not city:
            print("City name cannot be empty. Please enter a city name: ")
            continue

        return city


def check_city(weather_data):
    """
    From API data the location is shown.
    User is asked if the location is indeed the city the user wants the weather information for
    :param weather_data: parsed weather_data within a dict
    :return: bool - True if confirmed, False if not
    """
    try:
        location = weather_data['location']
        print(f"Found {location['name']} in region: {location['region']} and country: {location['country']}\n")

        while True:
            correct_city = input(f'Is this the city you want to see the weather forecast for? (y/n): ').lower()
            if correct_city in ['yes', 'y']:
                return True
            elif correct_city in ['n', 'no']:
                return False
            else:
                print("\nInvalid input. Please enter 'y' or 'n'.")

    except KeyError as e:
        print(f'Missing expected data: {e}')
        return False


# ============ GET VALIDATED WEATHER DATA ==============
def run_validate_weather_data():
    """
    Handles iteration of getting weather data and validating
    :return: bool - True if data found & city confirmed, False if not
            & None or dict with weather data
    """

    city = get_city()
    data = get_weather_in_city(city)
    parsed = parse_weather_api(data)

    if not parsed['found']: # if no data from api - function returns
        print(f'No data found: {parsed['error']}')
        return False, None

    if not check_city(parsed['weather']):  # found data & city - check if city is the one you want to see
        print('Asking for city again...\n')
        return False, None

    return True, parsed['weather']


#============= CURRENT WEATHER =======================

def display_current_weather(weather):
    """

    :param weather:
    :return: print current weather
    """
    location = weather['location']

    #---- EXTRACT CURRENT WEATHER ----
    current_weather = {key: weather['current'][key] for key in KEY_FILTERS_CURRENT_WEATHER}
    current_weather['condition'] = current_weather['condition']['text']
    current_weather['wind_dir'] = WIND_DIR_MAP.get(current_weather['wind_dir'], current_weather['wind_dir']) #fallback

    print(f"\n----------------------\n"
          f"The current weather in {location['name']}, {location['country']} at {current_weather['last_updated'][11:]} is:\n"
          f"Temperature: {current_weather['temp_c']}{chr(176)}C \n"
          f"Perceived temperature: {current_weather['feelslike_c']}{chr(176)}C \n"
          f"Precipitation: {current_weather['precip_mm']} mm\n"
          f"Wind: {current_weather['wind_kph']} kph in {current_weather['wind_dir']} direction\n"
          f"Condition: {current_weather['condition']}\n"
          f"")



def current_weather_loop():
    while True:
        success, weather_data = run_validate_weather_data()

        if not success: # loop back if no data of city rejected
            continue

        display_current_weather(weather_data)

        if not ask_repeat("1. Get the current weather conditions"):
            return


#=============== WEATHER FORECAST TODAY ==============
def display_forecast_weather(weather):
    pass


def forecast_weather_loop():
    while True:
        success, weather_data = run_validate_weather_data()

        if not success:  # loop back if no data of city rejected
            continue

        display_forecast_weather(weather_data)

        if not ask_repeat("2. Get the weather forecast for today"):
            return

#============= CLOTHING ADVICE ===================
def display_clothing_advice(weather):
    pass


def clothing_advice_loop():
    while True:
        success, weather_data = run_validate_weather_data()

        if not success:  # loop back if no data of city rejected
            continue

        display_clothing_advice(weather_data)

        if not ask_repeat("3. Get clothing advice for today's weather forecast"):
            return



# =================== WEATHER SUBMENU LOOP ==================
def weather_loop():
    while True:
        print_weather_menu()

        try:
            choose_weather = int(input("Please choose an option: "))

            match choose_weather:
                case 1:
                    current_weather_loop()

                case 2:
                    forecast_weather_loop()

                case 3:
                    clothing_advice_loop()

                case 4:
                    return

                case _:
                    print(f'\033[31mInvalid choice.\033[0m Please choose between options 1 - 4. ')

            if not ask_repeat("2. Get the weather forecast"):  # end menu cycle - ask if want to repeat
                return

        except ValueError as e:
            print(f"\033[31mInvalid input\033[0m - error: {e} \nPlease enter a digit.\n")


weather_loop()