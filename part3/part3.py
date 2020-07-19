import json
import plotly.express as px
import pandas as pd
from collections import Counter 
from datetime import datetime

def format_temperature(temp_input):
    """formats the input temperature

    Args:
        temp_in_celcius: integer representing a temperature.
    Returns:
        integer representing a temperature in the required format.
    """
    temp_formatted = round(float(temp_input),1)
    return(temp_formatted)

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
    day = 0

    for n in fcast:
        day = day + 1
        temp = format_temperature(n['Temperature']['Metric']['Value'])
        temp_rf = format_temperature(n['RealFeelTemperature']['Metric']['Value'])
        temp_list[day] = temp
        temp_rf_list[day] = temp_rf
        # print(temp,temp_rf)
        text = n['WeatherText']
        # print(text)
        weather_text.append(text)

    
    print(f"{temp_list} \n{temp_rf_list}")
    # print(set(weather_text))


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
    # fig1.show()

    table2 = pd.DataFrame(count_occurence(weather_text), columns=['Weather Text','Count of Occurrence'])
    print(table2)
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



f = open("demofile2.txt", "a")
f.write("Now the file has more content!")
f.close()

#open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read())
    



    


    


  



if __name__ == "__main__":
    print(process_weather("data/historical_6hours.json"))