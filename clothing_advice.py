from collections import Counter

#========= VARIABLES ============
KEY_FILTERS_CLOTHING_WEATHER = ['temp_c', 'condition', 'wind_kph', 'precip_mm', 'feelslike_c', 'will_it_rain',
                                'chance_of_rain', 'uv', "will_it_snow"]
DEGREE_SYMBOL = chr(176)


def get_forecast_descriptives(filtered_hourly: list[dict[str, str|float|int]]):
    """
    Get descriptive weather values from a list of hourly forecast data.
    :param filtered_hourly: List of dictionaries. List items are hours.
    :return: dictionary of descriptive statistics
    """

    descriptives = {}

    ### Temperature
    descriptives['min_temp'] = min(hour['temp_c'] for hour in filtered_hourly)
    descriptives['max_temp'] = max(hour['temp_c'] for hour in filtered_hourly)
    descriptives['avg_temp'] = round(sum(hour['temp_c'] for hour in filtered_hourly) / len(filtered_hourly), 2)
    descriptives['temp_range'] = descriptives['max_temp'] - descriptives['min_temp']

    ### Feelslike temperature
    descriptives['feel_min_temp'] = min(hour['feelslike_c'] for hour in filtered_hourly)
    descriptives['feel_max_temp'] = max(hour['feelslike_c'] for hour in filtered_hourly)
    descriptives['feel_avg_temp'] = round(sum(hour['feelslike_c'] for hour in filtered_hourly) / len(filtered_hourly), 2)


    ### Wind & UV
    descriptives['avg_wind'] = round(sum(hour['wind_kph'] for hour in filtered_hourly) / len(filtered_hourly), 2)
    descriptives['max_uv'] = max(hour['uv'] for hour in filtered_hourly)

    ###  most common condition str
    conditions = [hour['condition'] for hour in filtered_hourly]
    count_conditions = Counter(conditions)
    descriptives['most_common_condition'] = count_conditions.most_common(1)[0][0] # if multiple have highest count first in alphabet is returned

    # Rain
    descriptives['tot_precip'] = sum(hour['precip_mm'] for hour in filtered_hourly)
    descriptives['avg_chance_rain'] = round(sum(hour['chance_of_rain'] for hour in filtered_hourly) / len(filtered_hourly))
    descriptives['will_it_rain'] = True if sum(hour['will_it_rain'] for hour in filtered_hourly) > 0 else False

    # Snow
    descriptives['will_it_snow'] = True if sum(hour['will_it_snow'] for hour in filtered_hourly) > 0 else False

    return descriptives

def generate_clothing_advice(descriptives: dict) -> dict:
    pass

def print_clothing_advice(location:str, date:str, descirptives:dict, advice:dict):
    pass

def display_clothing_advice(weather):
    """
    Extract forecast weather data from 8am to 8pm and print clothing advice.
    :param weather: weather data dictionary for today and chosen city
    :return: Print clothing advice
    """
    #get location and date
    location = weather['location']['name']
    date = weather['forecast']['forecastday'][0]['date']

    #get forecast between 8am and 8pm (index 0 = hour 0:00)
    forecast_hourly = weather['forecast']['forecastday'][0]['hour'][8:21]

    # filter dictionary by key for each hour in list
    filtered_hourly = [
        {key: hour[key] for key in KEY_FILTERS_CLOTHING_WEATHER}
        for hour in forecast_hourly
    ]
    # extract condition text
    for hour in filtered_hourly:
        hour['condition'] = hour['condition']['text']

    descriptives = get_forecast_descriptives(filtered_hourly)

    print(f'This clothing advice is based on the forecast for {location} on {date} '
          f'between 8am and 8pm:\n'
          f'-----------------------------------\n ')
    # advice temp
    print(f"The average 'feel-like' temperature (accounting for humidity and windchill) today will be {descriptives['feel_avg_temp']}{DEGREE_SYMBOL}C")

    if descriptives['feel_avg_temp'] <= 5:
        print(f"    It's going to feel cold today. Bundle up!\n"
              f"    Wear warm layers, a thick coat, hat and scarf.")
    elif descriptives['feel_avg_temp'] <= 10:
        print(f"    It's going to feel chilly today. Dress warmly.\n"
              f"    Wear a warm coat or a sweater and light jacket. Consider bringing a scarf.")
    elif descriptives['feel_avg_temp'] <= 15:
        print(f"    It's going to feel mild today.\n"
              f"    Wear layers and consider a transitional jacket.")
    elif descriptives['feel_avg_temp'] <= 20:  # 15-20
        print(f"    It's going to feel mild/ warm today. Layering is advisable.\n"
              f"    Depending on personal preference and other weather factors, you can wear short- or longsleeve clothing.")
    elif descriptives['feel_avg_temp'] <= 25:
        print(f"    It's going to feel warm today.\n"
              f"    T-shirt weather! Wear light clothing.")
    else:  # >25C
        print(f"    It's going to feel hot today!\n"
              f"    Wear breathable clothing and seek out shade.")

    # advice temp range
    if descriptives['temp_range'] > 10:
        print(f'There will be a big temperature range today ({descriptives['temp_range']}{DEGREE_SYMBOL}C). Layering is key!\n')
    elif descriptives['temp_range'] > 6:
        print(f"Expect some temperature variation today ({descriptives['temp_range']}{DEGREE_SYMBOL}C).\n")
    else:
        print(f"Temperature will be fairly consistent throughout the day.\n")

    # advice when rain
    if not descriptives['will_it_rain']:
        if descriptives['avg_chance_rain'] > 10: #chance of rain higher than 10%
            print(f'It should not rain today. Although there is a {descriptives['avg_chance_rain']}% chance of rain.\n'
                  f'Pack a lightweight raincoat just in case.')
        else:
            print(f'It should not rain today.')
    elif descriptives['will_it_rain']:
        print(f'Consider carrying an umbrella - it will rain today. The chance of rain is {descriptives['avg_chance_rain']}% '
              f'with a total of {descriptives['tot_precip']} mm rain forecast.')

    # advice snow
    if descriptives['will_it_snow']:
        print(f"It's going to snow today! Make sure your outer layers are warm and waterproof and definitely bring gloves.")

    # advice wind
    if descriptives['avg_wind'] > 30:
        print(f"It's going to be windy today with {descriptives['avg_wind']}kph winds. A windbreaker might come in handy.")
    elif descriptives['avg_wind'] > 45:
        print(f"There wil be strong winds of {descriptives['avg_wind']} kph. Wear a windbreaker and be careful outside!")

    # advice UV
    print(f"The max UV-index will be {descriptives['max_uv']}")
    if descriptives['max_uv'] > 3:
        print(f"    Apply sunscreen before going outside.")
    elif descriptives['max_uv'] > 6:
        print(f"    Protect your skin with sunscreen and a hat! The sun is fierce today with an max UV-index of {descriptives['max_uv']}")



