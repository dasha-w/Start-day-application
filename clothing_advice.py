"""
Module for generating clothing advice based on weather forecast data.
Analyzes temperature, wind, rain, snow, and UV-index between 8am and 8pm.
"""

from collections import Counter

from colorama import Fore, Style

from helpers import parse_date, DEGREE_SYMBOL, SEPERATOR_SMALL

#========= VARIABLES ============
KEY_FILTERS_CLOTHING_WEATHER = ["temp_c", "condition", "wind_kph", "precip_mm", "feelslike_c", "will_it_rain",
                                "chance_of_rain", "uv", "will_it_snow"]
# temperature threshold in celsius
TEMP_THRESHOLD = {"cold" : 5, "chilly" : 10, "mild" : 15, "mild/warm" : 20, "warm" : 25}
# wind threshold in kph
WIND_THRESHOLD = {"windy":30, "strong_wind":45}
# UV index threshold
UV_THRESHOLD = {"medium":3, "high":6}
# temperature range threshold (max - min temperature)
TEMP_RANGE_THRESHOLD = {"medium": 6, "high":10}
# rain probability threshold in %
RAIN_CHANCE_THRESHOLD = 10
# rain amount threshold in mm
RAIN_MM_THRESHOLD = 1


def get_forecast_descriptives(filtered_hourly: list[dict[str, str|float|int]]) -> dict:
    """
    Get descriptive weather values from a list of hourly forecast data.
    :param:
        filtered_hourly (list[dict]): List of dictionaries with list. Each item list in dict is an hour.
    :return:
        dict: dictionary of descriptive statistics
        (temperature (min, max, avg, range, feel), wind, uv, snow, rain, condition)
    """

    descriptives = {} # todo in 1 variable statement zetten - niet hele tijd desciprtive['key']

    # --- Temperature ---
    descriptives["min_temp"] = min(hour["temp_c"] for hour in filtered_hourly)
    descriptives["max_temp"] = max(hour["temp_c"] for hour in filtered_hourly)
    descriptives["avg_temp"] = round(sum(hour["temp_c"] for hour in filtered_hourly) / len(filtered_hourly), 2)
    descriptives["temp_range"] = round(descriptives["max_temp"] - descriptives["min_temp"],2)

    # --- Feels like temperature ---
    descriptives["feel_min_temp"] = min(hour["feelslike_c"] for hour in filtered_hourly)
    descriptives["feel_max_temp"] = max(hour["feelslike_c"] for hour in filtered_hourly)
    descriptives["feel_avg_temp"] = round(sum(hour["feelslike_c"] for hour in filtered_hourly) / len(filtered_hourly), 2)


    # --- Wind & UV ---
    descriptives["avg_wind"] = round(sum(hour["wind_kph"] for hour in filtered_hourly) / len(filtered_hourly), 2)
    descriptives["max_uv"] = max(hour["uv"] for hour in filtered_hourly)

    # --- most common condition (str) ---
    conditions = [hour["condition"] for hour in filtered_hourly]
    count_conditions = Counter(conditions)
    descriptives["most_common_condition"] = count_conditions.most_common(1)[0][0]
    # if multiple have the highest count, first in alphabet is returned

    # --- Rain ---
    descriptives["tot_precip"] = round(sum(hour["precip_mm"] for hour in filtered_hourly))
    # krijg to echt float met veel achter komma zonder round() ??
    descriptives["avg_chance_rain"] = round(sum(hour["chance_of_rain"] for hour in filtered_hourly) / len(filtered_hourly))
    descriptives["will_it_rain"] = True if sum(hour["will_it_rain"] for hour in filtered_hourly) > 0 else False

    # --- Snow ---
    descriptives["will_it_snow"] = True if sum(hour["will_it_snow"] for hour in filtered_hourly) > 0 else False

    return descriptives


def generate_clothing_advice(descriptives: dict) -> dict:
    """
    Generate clothing advice strings based on weather discriptives

    :param:
        descriptives (dict): dictionary of weather stats from get_forecast_descriptives
    :return:
        dict: containing advice strings for temp, range, rain, wind, snow, UV
    """

    advice = {}

    # --- temperature ---
    avg_temp = descriptives["feel_avg_temp"]
    if avg_temp <= TEMP_THRESHOLD["cold"]:
        advice["temp"] = (f"It's going to feel {Fore.BLUE}cold{Style.RESET_ALL} today. Bundle up!\n"
                          ">    Wear warm layers, a thick coat, hat and scarf.")
    elif avg_temp <= TEMP_THRESHOLD["chilly"]:
        advice["temp"] = (f"It's going to feel {Fore.BLUE}chilly{Style.RESET_ALL} today. Dress warmly.\n"
                          ">    Wear a warm coat or a sweater and light jacket. Consider bringing a scarf.")
    elif avg_temp <= TEMP_THRESHOLD["mild"]:
        advice["temp"] = (f"It's going to feel {Fore.BLUE}mild{Style.RESET_ALL} today.\n"
                          ">    Wear layers and consider a transitional jacket.")
    elif avg_temp <= TEMP_THRESHOLD["mild/warm"]:  # 15-20
        advice["temp"] = (f"It's going to feel {Fore.BLUE}mild/ warm{Style.RESET_ALL} today. Layering is advisable.\n"
                          ">    Depending on personal preference and other weather factors, you can wear short- or longsleeve clothing.")
    elif avg_temp <= TEMP_THRESHOLD["warm"]:
        advice["temp"] = (f"It's going to feel {Fore.BLUE}warm{Style.RESET_ALL} today.\n"
                          f">   T-shirt weather! Wear light clothing.")
    else:  # >25C
        advice["temp"] = (f"It's going to feel {Fore.BLUE}hot{Style.RESET_ALL} today!\n"
                          f">   Wear breathable clothing and seek out shade.")


    # --- temperature range ---
    temp_range = descriptives["temp_range"]
    if temp_range > TEMP_RANGE_THRESHOLD["high"]:
        advice["range"] = (f"There will be a {Fore.BLUE}big temperature{Fore.RESET} range today (range: {temp_range}{DEGREE_SYMBOL}C). \n"
                           f">   Layering is key!\n")
    elif temp_range > TEMP_RANGE_THRESHOLD["medium"]:
        advice["range"] = f"Expect {Fore.BLUE}some temperature{Fore.RESET} variation today (range: {temp_range}{DEGREE_SYMBOL}C).\n"
    else:
        advice["range"] = f"Temperature will be {Fore.BLUE}fairly consistent{Fore.RESET} throughout the day.\n"


    # --- advice when rain ---
    rain_chance = descriptives["avg_chance_rain"]
    rain_tot = descriptives["tot_precip"]

    if not descriptives["will_it_rain"]:
        if rain_chance > RAIN_CHANCE_THRESHOLD: #if 10, chance of rain higher than 10%
            advice["rain"] = (f"It should {Fore.BLUE}not rain{Fore.RESET} today. Although there is a {rain_chance}% "
                              f"chance of rain.\n"
                              f">   Pack a lightweight raincoat just in case.")
        else:
            advice["rain"] = f"It should {Fore.BLUE}not rain{Fore.RESET} today."
    elif descriptives["will_it_rain"]:
        if rain_tot < RAIN_MM_THRESHOLD:
            advice["rain"] = (f"There will be {Fore.BLUE}some rain{Fore.RESET} today.\n"
                              f"The chance of rain is {rain_chance}% with a total of {rain_tot} mm rain forecast.\n"
                              f">   If timed correctly you should stay dry today.")
        else: #if will_it_rain is True and more than RAIN_MM_THRESHOLD rain is predicted
            advice["rain"] = (f"It {Fore.BLUE}will rain{Fore.RESET} today. The chance of rain is {rain_chance}% "
                              f"with a total of {rain_tot} mm rain forecast.\n"
                              f">   Consider carrying an umbrella. ")

    # --- advice snow ---
    if descriptives["will_it_snow"]:
        advice["snow"] = (f"It's going to {Fore.BLUE}snow{Fore.RESET} today! \n"
                          f">   Make sure your outer layers are warm and waterproof and definitely bring gloves.")

    # --- advice wind ---
    avg_wind = descriptives["avg_wind"]
    if avg_wind > WIND_THRESHOLD["windy"]:
        advice["wind"] = (f"It's going to be {Fore.BLUE}windy{Fore.RESET} today with {avg_wind}kph winds. \n"
                          f">   A windbreaker might come in handy.")
    elif avg_wind > WIND_THRESHOLD["strong_wind"]:
        advice["wind"] = (f"There wil be {Fore.BLUE}strong winds{Fore.RESET} of {avg_wind} kph. \n"
                          f">   Wear a windbreaker and be careful outside!")

    # --- advice UV ---
    uv_index = descriptives["max_uv"]
    start_advice = f"The max {Fore.BLUE}UV-index{Fore.RESET} will be {uv_index}.\n"
    if uv_index > UV_THRESHOLD["high"]:
        advice["uv"] = start_advice + f">   Protect your skin with sunscreen and a hat! The sun is fierce today!"
    elif uv_index > UV_THRESHOLD["medium"]:
        advice["uv"] = start_advice + f">   Apply sunscreen before going outside."

    return advice


def print_clothing_advice(location:str, date:str, descriptives:dict, advice:dict) -> None:
    """
    Print the formatted clothing advice to the console

    :param:
        location (str): Name of city
        date (str): Formatted date string
        descriptives (dict): Weather statistics
        advice (dict): Generated advice strings
    """

    print(f"\n{Fore.BLUE}This clothing advice is based on the forecast for {location} on {date} "
          f"between 8am and 8pm:\n{Fore.RESET}"
          f"{SEPERATOR_SMALL} ")
    # advice temp
    print(f"The average {Fore.BLUE}temperature{Fore.RESET} will {Style.BRIGHT}feel like{Style.RESET_ALL} "
          f"{descriptives["feel_avg_temp"]}{DEGREE_SYMBOL}C")

    print(advice["temp"])
    print(f"{advice["range"]}")

    if "rain" in advice: #TODO er is altijd rain in advice ?! check en beslis
        print(advice["rain"])

    if "snow" in advice:
        print(advice["snow"])

    if "wind" in advice:
        print(advice["wind"])

    if "uv" in advice:
        print(advice["uv"])


def display_clothing_advice(weather) -> None:
    """
    Main entry point for clothing advice.
    Extracts forecast from 8am - 8pm, calculates stats, and prints clothing advice

    :param:
        weather (dict): Raw weather data dictionary for API
    """
    # get location and date
    location = weather["location"]["name"]
    date = parse_date(weather["forecast"]["forecastday"][0]["date"])

    # filter forecast between 8am and 8pm (index 0 = hour 0:00)
    forecast_hourly = weather["forecast"]["forecastday"][0]["hour"][8:21]

    # filter dictionary by key for each hour in list - reduce data
    filtered_hourly = [
        {key: hour[key] for key in KEY_FILTERS_CLOTHING_WEATHER}
        for hour in forecast_hourly
    ]
    # extract condition text from nested dictionary
    for hour in filtered_hourly:
        hour["condition"] = hour["condition"]["text"]

    # generate statistics and advice
    descriptives = get_forecast_descriptives(filtered_hourly)
    advice = generate_clothing_advice(descriptives)

    # Output results
    print_clothing_advice(location, date, descriptives, advice)



