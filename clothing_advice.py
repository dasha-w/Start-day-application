from collections import Counter

from helpers import parse_date, DEGREE_SYMBOL

#========= VARIABLES ============
KEY_FILTERS_CLOTHING_WEATHER = ['temp_c', 'condition', 'wind_kph', 'precip_mm', 'feelslike_c', 'will_it_rain',
                                'chance_of_rain', 'uv', "will_it_snow"]
TEMP_THRESHOLD = {'cold' : 5, 'chilly' : 10, 'mild' : 15, 'mild/warm' : 20, 'warm' : 25}
WIND_THRESHOLD = {'windy':30, 'strong_wind':45}
UV_THRESHOLD = {'medium':3, 'high':6}
TEMP_RANGE_THRESHOLD = {'medium': 6, 'high':10}
RAIN_CHANCE_THRESHOLD = 10 #chance of rain higher than 10%
RAIN_MM_THRESHOLD = 1 #1 mm rain


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
    descriptives['temp_range'] = round(descriptives['max_temp'] - descriptives['min_temp'],2)

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

    advice = {}

    #temperature
    avg_temp = descriptives['feel_avg_temp']
    if avg_temp <= TEMP_THRESHOLD['cold']:
        advice['temp'] = "It's going to feel cold today. Bundle up!\nWear warm layers, a thick coat, hat and scarf."
    elif avg_temp <= TEMP_THRESHOLD['chilly']:
        advice['temp'] = ("It's going to feel chilly today. Dress warmly.\n"
                          "Wear a warm coat or a sweater and light jacket. Consider bringing a scarf.")
    elif avg_temp <= TEMP_THRESHOLD['mild']:
        advice['temp'] = "It's going to feel mild today.\nWear layers and consider a transitional jacket."
    elif avg_temp <= TEMP_THRESHOLD['mild/warm']:  # 15-20
        advice['temp'] = ("It's going to feel mild/ warm today. Layering is advisable.\n"
                          "Depending on personal preference and other weather factors, you can wear short- or longsleeve clothing.")
    elif avg_temp <= TEMP_THRESHOLD['warm']:
        advice['temp'] ="It's going to feel warm today.\nT-shirt weather! Wear light clothing."
    else:  # >25C
        advice['temp'] = "It's going to feel hot today!\nWear breathable clothing and seek out shade."


    # temperature range
    temp_range = descriptives['temp_range']
    if temp_range > TEMP_RANGE_THRESHOLD['high']:
        advice['range'] = f'There will be a big temperature range today (range: {temp_range}{DEGREE_SYMBOL}C). Layering is key!\n'
    elif temp_range > TEMP_RANGE_THRESHOLD['medium']:
        advice['range'] = f"Expect some temperature variation today (range: {temp_range}{DEGREE_SYMBOL}C).\n"
    else:
        advice['range'] = "Temperature will be fairly consistent throughout the day.\n"


    # advice when rain
    rain_chance = descriptives['avg_chance_rain']
    rain_tot = descriptives['tot_precip']

    if not descriptives['will_it_rain']:
        if rain_chance > RAIN_CHANCE_THRESHOLD: #if 10, chance of rain higher than 10%
            advice['rain'] = (f'It should not rain today. Although there is a {rain_chance}% '
                              f'chance of rain.\nPack a lightweight raincoat just in case.')
        else:
            advice['rain'] = 'It should not rain today.'
    elif descriptives['will_it_rain']:
        if rain_tot < RAIN_MM_THRESHOLD:
            advice['rain'] = (f'There will be some rain today, but if timed correctly you should stay dry.\n'
                              f'    The chance of rain is {rain_chance}% with a total of '
                              f'{rain_tot} mm rain forecast.')
        else: #if will_it_rain is True and more than RAIN_MM_THRESHOLD rain is predicted
            advice['rain'] = (f'Consider carrying an umbrella - it will rain today. The chance of rain is '
                          f'{rain_chance}% with a total of {rain_tot} mm rain forecast.')

    # advice snow
    if descriptives['will_it_snow']:
        advice['snow'] = ("It's going to snow today! Make sure your outer layers are warm and waterproof and "
                          "definitely bring gloves.")

    # advice wind
    avg_wind = descriptives['avg_wind']
    if avg_wind > WIND_THRESHOLD['windy']:
        advice['wind'] = f"It's going to be windy today with {avg_wind}kph winds. A windbreaker might come in handy."
    elif avg_wind > WIND_THRESHOLD['strong_wind']:
        advice['wind'] = f"There wil be strong winds of {avg_wind} kph. Wear a windbreaker and be careful outside!"

    # advice UV
    uv_index = descriptives['max_uv']
    start_advice = f"The max UV-index will be {uv_index}.\n"
    if uv_index > UV_THRESHOLD['medium']:
        advice['uv'] = start_advice + f'    Apply sunscreen before going outside.'
    elif uv_index > UV_THRESHOLD['high']:
        advice['uv'] = start_advice + f"    Protect your skin with sunscreen and a hat! The sun is fierce today with an max UV-index of {uv_index}"

    return advice


def print_clothing_advice(location:str, date:str, descriptives:dict, advice:dict):

    print(f'This clothing advice is based on the forecast for {location} on {date} '
          f'between 8am and 8pm:\n'
          f'-----------------------------------\n ')
    # advice temp
    print(f"The average 'feel-like' temperature (accounting for humidity and windchill) today "
          f"will be {descriptives['feel_avg_temp']}{DEGREE_SYMBOL}C")
    print(advice['temp'])
    print(f'    {advice['range']}')

    if 'rain' in advice:
        print(advice['rain'])

    if 'snow' in advice:
        print(advice['snow'])

    if 'wind' in advice:
        print(advice['wind'])

    if 'uv' in advice:
        print(advice['uv'])


def display_clothing_advice(weather):
    """
    Extract forecast weather data from 8am to 8pm and print clothing advice.
    :param weather: weather data dictionary for today and chosen city
    :return: Print clothing advice
    """
    #get location and date
    location = weather['location']['name']
    date = parse_date(weather['forecast']['forecastday'][0]['date'])


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

    advice = generate_clothing_advice(descriptives)

    print_clothing_advice(location, date, descriptives, advice)



