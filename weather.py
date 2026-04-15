import requests
from colorama import Fore, Style

from clothing_advice import display_clothing_advice
from config import WEATHER_API_KEY
from helpers import ask_repeat, parse_date, DEGREE_SYMBOL, SEPERATOR_BIG, SEPERATOR_SMALL
from prettytable import PrettyTable, TableStyle

## ================= VARIABLES =====================
WIND_DIR_MAP = {
    'N': 'Northern', 'S': 'Southern', 'E': 'Eastern', 'W': 'Western',
    'NE': 'Northeastern', 'NW': 'Northwestern', 'SE': 'Southeastern', 'SW': 'Southwestern',
    'NNE': 'North-northeastern','ENE': 'East-northeastern', 'ESE': 'East-southeastern', 'SSE': 'South-southeastern',
    'SSW': 'South-southwestern','WSW': 'West-southwestern', 'WNW': 'West-northwestern', 'NNW': 'North-northwestern'
}


#================ FUNCTIONS =====================
def print_weather_menu():
    print(f"\n{SEPERATOR_BIG}\nThese are your options: \n"
          f"{SEPERATOR_SMALL}\n"
          f'{Fore.BLUE}{Style.BRIGHT}1. Get the current weather conditions\n'
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

    url = "https://api.weatherapi.com/v1/forecast.json"
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
    Asks user for city name. Input cannot be empty. User can quit the search.
    :return: string or None
    """
    while True:
        city = input(f"{SEPERATOR_SMALL}\nEnter a city name to check the weather (q to quit search): ").strip()

        if city.lower() == 'q':
            return None

        if not city:
            print("\nCity name cannot be empty. Please enter a city name: ")
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
        print(f"\n{Style.BRIGHT}Found {location['name']} in region: {location['region']} and country: {location['country']}")

        while True:
            correct_city = input(f'{SEPERATOR_SMALL}\nIs this the city you want to see the weather forecast for? (y/n): ').lower().strip()
            if correct_city in ['yes', 'y']:
                return True
            elif correct_city in ['n', 'no']:
                return False
            else:
                print(f"\n{Fore.RED}Invalid input.{Fore.RESET} Please enter 'y' or 'n'.")

    except KeyError as e:
        print(f'{Fore.RED}Missing expected data:{Fore.RESET} {e}')
        return False


# ============ GET VALIDATED WEATHER DATA ==============
def run_validated_weather_data():
    """
    Handles iteration of getting weather data and validating
    :return:
        1) None - if user quits city input
           Bool - True - if data found & city confirmed
                - False - if city rejected or no data found for city
        2) None - if 1 is None or False
           Dict - if 1 is True
    """

    city = get_city()

    if city is None:
        print("Quitting search for weather. Returning to menu.")
        return None, None

    data = get_weather_in_city(city)
    parsed = parse_weather_api(data)

    if not parsed['found']: # if no data from api - function returns
        print(f'\n{Fore.RED}No data found{Fore.RESET}: {parsed['error']}')
        return False, None

    if not check_city(parsed['weather']):  # found data & city - check if city is the one you want to see
        print('\nAsking for city again...')
        return False, None

    return True, parsed['weather']


#============= CURRENT WEATHER =======================

def get_current_weather(weather:dict)->dict:

    current_dict = {}

    current_dict['location'] = weather['location']['name']
    current_dict['date'] = parse_date(weather['forecast']['forecastday'][0]['date'])

    #parse current weather
    weather_current = weather['current']
    # time
    current_dict['time'] = weather_current['last_updated'][11:]

    #temp
    current_dict['temp'] = f'{weather_current['temp_c']}{DEGREE_SYMBOL}C'
    current_dict['feels_temp'] = f'{weather_current['feelslike_c']}{DEGREE_SYMBOL}C'

    # rain
    current_dict['rain'] = f'{weather_current['precip_mm']} mm'

    # wind
    current_dict['wind_kph'] = f'{weather_current['wind_kph']} kph'
    current_dict['wind_dir'] = WIND_DIR_MAP.get(weather_current['wind_dir'], weather_current['wind_dir']) #fallback

    # UV & condition
    current_dict['uv'] = weather_current['uv']
    current_dict['condition'] = weather_current['condition']['text']

    return current_dict


def display_current_weather(current: dict):
    """
    Extract current weather data and print.
    :param weather: weather data dictionary for today and chosen city
    :return: Print current weather
    """
    print(f'\n{Fore.BLUE}{Style.BRIGHT}The current weather in {current['location']} at {current['time']}')

    table = PrettyTable()
    table.align = 'l'
    table.header = False
    table.border = True
    table.padding_width = 2
    table.add_rows(
        [
            ["Temperature:", current['temp']],
            ["Perceived temperature:", current['feels_temp']],
            ["Precipitation:",  current['rain']],
            ["Wind:", f'{current['wind_kph']} in {current['wind_dir']} direction'],
            ["UV index:", current['uv']],
            ["Condition:", current['condition']]
        ]
    )
    print(table)


#=============== WEATHER FORECAST TODAY ==============
def get_forecast_weather(weather: dict)-> dict:
    """
    Extract relevant weather data into dict for printing function
    :param weather: dict
    :return: smaller dict
    """
    forecast = {}

    forecast['location'] = weather['location']['name']
    forecast['date'] = parse_date(weather['forecast']['forecastday'][0]['date'])

    # parse forecast for today
    weather_forecast = weather['forecast']['forecastday'][0]['day']

    #temp
    forecast['min_temp'] = f'{weather_forecast['mintemp_c']}{DEGREE_SYMBOL}C'
    forecast['max_temp'] = f'{weather_forecast['maxtemp_c']}{DEGREE_SYMBOL}C'
    forecast['avg_temp'] = f'{weather_forecast['avgtemp_c']}{DEGREE_SYMBOL}C'

    # rain
    forecast['rain_chance'] = f'{weather_forecast['daily_chance_of_rain']} %'
    forecast['rain_mm'] = f'{weather_forecast['totalprecip_mm']} mm'

    # snow
    snow = weather_forecast['daily_will_it_snow']
    if snow == 1: # if it will snow
        forecast['snow_chance'] = f'{weather_forecast['daily_chance_of_snow']} %'
        forecast['snow_cm'] = f'{weather_forecast['totalsnow_cm']} cm'

    # UV & condition
    forecast['uv'] = weather_forecast['uv']
    forecast['condition'] = weather_forecast['condition']['text']

    return forecast


def display_forecast_weather(forecast:dict):

    print(f'\n{Fore.BLUE}{Style.BRIGHT}Forecast for {forecast['location']} on {forecast['date']}')

    table = PrettyTable()
    table.align = 'l'
    table.header = False
    table.border = True
    table.padding_width = 2
    table.add_rows(
        [
            ["Temperature between:", f'{forecast['min_temp']} - {forecast['max_temp']}'],
            ["Average temperature:", forecast['avg_temp']],
            ["Chance of rain:", forecast['rain_chance']],
            ["Total rain:", forecast['rain_mm']],
            ["UV index:", forecast['uv']],
            ["Condition:", forecast['condition']]
        ]
    )

    # Add snow to table if there is snow
    if 'snow_chance' in forecast:
        table.add_rows(
            [
                ["Chance of snow:", forecast['snow_chance']],
                ["Total snow:", forecast['snow_cm']]
            ]
        )

    print(table)


# =========== DISPLAY LOOP ==================
def display_loop(option):
    """
    Uses validated weather data to control loop. If checks (data found and user accepts city found and does not
    quit) are passed, weather data is displayed according to 'option'
    :param option: str 'current', 'forecast' or 'clothing' calls different display functions
    :return: None
    """
    while True:
        success, weather_data = run_validated_weather_data()

        if success is None: # User chose 'q' when searching for city - break loop
            break

        if not success: # No data of city found or user rejects found city - restart loop
            continue

        match option:
            case 'current':
                current = get_current_weather(weather_data)
                display_current_weather(current)
                if not ask_repeat("1. Get the current weather conditions"):
                    return

            case 'forecast':
                forecast = get_forecast_weather(weather_data)
                display_forecast_weather(forecast)
                if not ask_repeat("2. Get the weather forecast for today"):
                    return

            case 'clothing':
                display_clothing_advice(weather_data)
                if not ask_repeat("3. Get clothing advice for today's weather forecast"):
                    return

            case _:
                print("Action parameter not properly defined. Should be 'current', 'forecast', or 'clothing'")
                break


# =================== WEATHER SUBMENU LOOP ==================
def weather_loop():
    """
    function controls loop over submenu weather and calls functions for different options.
    :return: None
    """
    while True:
        print_weather_menu()

        try:
            choose_weather = int(input("Please choose an option: "))

            action_completed = False

            match choose_weather:
                case 1:
                    display_loop('current')
                    action_completed = True

                case 2:
                    display_loop('forecast')
                    action_completed = True

                case 3:
                    display_loop('clothing')
                    action_completed = True

                case 4:
                    return

                case _:
                    print(f'{Fore.RED}Invalid choice.{Fore.RESET} \nPlease choose between options 1 - 4. ')

            if action_completed:
                if not ask_repeat("2. Get the weather forecast"):  # end menu cycle - ask if want to repeat
                    return

        except ValueError as e:
            print(f"{Fore.RED}Invalid input{Fore.RESET} -- Error: {e}\n \n{Style.BRIGHT}Please enter a digit.")


