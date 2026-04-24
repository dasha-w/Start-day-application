# Start-day-application
A python CLI application designed to help you start your day with a boost of inspiration and practical weather insights. 

The user can choose to fetch random advice, quotes, and jokes from API endpoints and can search for advice with a keyword.

The user can also get real-time weather data for a city of choice. The application offers to display the current weather, 
the forecast for today, and generate clothing advice based on the forecast.

## Features
- **Daily Inspiration**
  - Random joke
  - Famous quotes
  - Random advice slip
  - Keyword-based advice slip search
- **Weather forecast**

  Get current conditions and daily forecast for any city worldwide
- **Clothing advice**
    
    Analyzes temperature, wind, rain, and UV-index to suggest appropriate clothing for the day
- **User friendly interface**

    Colorful output, interactive menus, and input validation

## Installation
1. Clone or download the repository
2. Create a virtual environment (recommended)
3. Install dependencies  
    ```pip install -r requirements.txt```
4. Configure API Key
    - Open or create config.py
    - Replace placeholder WEATHER_API_KEY with or add your own key from [WeatherAPI.com](https://www.weatherapi.com/)

## Usage
Run the main script  
```python main.py```

### Menu options
1. Get some inspiration: Access jokes, quotes, and advice.
2. Get the weather forecast:
   - View current weather.
   - View today's forecast.
   - Get clothing advice based on the forecast.
3. Quit: Exit the application.

## Project Structure

- ```main.py```: Entry point and main menu loop  
- ```weather.py```: Handles WeatherAPI integration, data parsing, and weather display  
- ```clothing_advice.py```: Logic for analyzing weather data and generating clothing recommendations    
- ```inspiration.py```: Integration with JokeFather, ZenQuotes, and AdviceSlip APIs  
- ```search_advice.py```: Specific logic for keyword-based advice searching  
- ```helpers.py```: Utility functions (date parsing, input validation, constants)  
- ```config.py```: Stores API keys (do not commit to public repos!)  
- ```requirements.txt```: Python dependencies

## Dependencies 

- ```requests```: For API calls.
- ```colorama```: For colored terminal output.
- ```prettytable```: For formatted weather tables.
- ```datetime```: Standard library for date handling.

## Notes

- The clothing advice logic filters weather data between 8:00 AM and 8:00 PM.  
- If an inspiration API fails, the application gracefully falls back to hardcoded messages.  
- All user inputs are validated to prevent crashes.
