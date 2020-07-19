import json
import plotly.express as px
import pandas as pd
from collections import Counter 
from datetime import datetime
def convert_time(iso_string):
    """Converts and ISO formatted time into a human readable format.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        A time formatted like: Hour:Minute AM/PM
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%I:%M %p')

def format_temperature(temp_input):
    """formats the input temperature

    Args:
        temp_in_celcius: integer representing a temperature.
    Returns:
        integer representing a temperature in the required format.
    """
    temp_formatted = round(float(temp_input),1)
    return(temp_formatted)

def format_temperature1(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and 'degrees celcius.'
    """
    temp = str(temp)
    DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"
    return f"{temp}{DEGREE_SYBMOL}"


def count_occurence(l): 
    """Converts raw weather data into meaningful text.

    Args:
        l: list used to check for occurrences of key value
    Returns:
        A list with the key value and the count of occurrences.
    """
    c = Counter(l) 
    l1 = [] 
    for key,value in c.items(): 
        l1.append([key,value]) 
    return l1 

def process_weather(forecast_file):
    """Converts raw weather data into meaningful text.

    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """
    with open(forecast_file) as json_file:
        fcast = json.load(json_file)

    temp_list = {}
    temp_rf_list = {}
    weather_text = []
    rainhours = []
    rain24hm =[]
    daylighth = []
    uv_list = {}

    for n in fcast:
        time = convert_time(n['LocalObservationDateTime'])
        temp = format_temperature(n['Temperature']['Metric']['Value'])
        uv = n['UVIndex']
        temp_rf = format_temperature(n['RealFeelTemperature']['Metric']['Value'])
        temp_list[time] = temp
        temp_rf_list[time] = temp_rf
        uv_list[time] = uv
        text = n['WeatherText']
        rain24h = n['PrecipitationSummary']['Past24Hours']['Metric']['Value']
        rain = n['HasPrecipitation']
        daylight =n['IsDayTime']
        weather_text.append(text)
        rainhours.append(rain)
        rain24hm.append(rain24h)
        daylighth.append(daylight)
        
    n = len(fcast)
    min_time = min(temp_list, key=temp_list.get)
    min_value = temp_list[min_time]
    max_time = max(temp_list, key=temp_list.get)
    max_value = temp_list[max_time]
    max_uv_time = max(uv_list, key=uv_list.get)
    max_uv_value = uv_list[max_uv_time]
    rainhours = count_occurence(rainhours)[0][1]
    daylighth = count_occurence(daylighth)[0][1]


    text_output = f"{n} Hour Overview\
\n    The lowest temperature was {format_temperature1(str(min_value))}, and occurred at {min_time}.\
\n    The highest temperature was {format_temperature1(str(max_value))}, and occurred at {max_time}.\
\n    Precipitation for the last 24 hours was {sum(rain24hm)}mm.\
\n    During the past {n} hours, precipitaion was recorded for {rainhours} hours.\
\n    The number of daylight hours in the past {n} hours was {daylighth} hours.\
\n    The maximum UV index was {max_uv_value}, and occurred at {max_uv_time}.\
"  

    table1 = pd.DataFrame.from_dict(temp_list, orient='index', columns=['Temperature'])
    table_rf = pd.DataFrame.from_dict(temp_rf_list, orient='index', columns=['Real Feel'])
    table1['Real Feel'] = table_rf
    # print(table1)

    fig1 = px.box(table1)
    fig1.update_layout(       
        title = {
            'text':'Minimum & Real Feel Temperature Distribution',
            'y':0.988,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        plot_bgcolor = 'white',
        xaxis = dict( title_text='Measure', showgrid=False, linecolor='black'),
        yaxis = dict(title_text='Temperature (°C)', showgrid=False, linecolor='black')
    )
    fig1.show()

    table2 = pd.DataFrame(count_occurence(weather_text), columns=['Weather Text','Count of Occurrence'])
    # print(table2)
    fig2 = px.bar(table2, x='Weather Text', y='Count of Occurrence')
    fig2.update_layout(       
        title = {
            'text':'Occurrences of Weather Text Categories',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        plot_bgcolor = 'white',
        xaxis = dict( showgrid=False, linecolor='black'),
        yaxis = dict(showgrid=False, linecolor='black')
    ) 
    fig2.update_yaxes(tick0=0, dtick=1)
    fig2.show()

    f = open("part3_output.txt", "w")
    f.writelines(text_output)
    f.close()



if __name__ == "__main__":
    print(process_weather("data/historical_6hours.json"))