import json
import plotly.express as px
import pandas as pd
from datetime import datetime

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and 'degrees celcius.'
    """
    temp = str(temp)
    DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"
    return f"{temp}{DEGREE_SYBMOL}"

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%A %d %B %Y')


def convert_f_to_c(temp_in_farenheit):
    """Converts an temperature from farenheit to celcius

    Args:
        temp_in_farenheit: integer representing a temperature.
    Returns:
        An integer representing a temperature in degrees celcius.
    """
    temp_cel = round(float((temp_in_farenheit - 32)*(5/9)),1)
    return(temp_cel)


def calculate_mean(total, num_items):
    """Calculates the mean.
    
    Args:
        total: integer representing the sum of the numbers.
        num_items: integer representing the number of items counted.
    Returns:
        An integer representing the mean of the numbers.
    """
    calc_mean = round((total)/(num_items),1)
    return((calc_mean))


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

    temp_min_list = {}
    temp_max_list = {}
    rf_list = {}
    rfs_list = {}

    for n in fcast['DailyForecasts']:
        date = convert_date(n['Date'])
        temp_min = convert_f_to_c(n['Temperature']['Minimum']['Value'])
        temp_max = convert_f_to_c(n['Temperature']['Maximum']['Value'])
        temp_min_list[date] = temp_min
        temp_max_list[date] = temp_max

        # print(date,temp_min,temp_max)

        rf = convert_f_to_c(n['RealFeelTemperature']['Minimum']['Value'])
        rf_list[date] = rf
        rfs = convert_f_to_c(n['RealFeelTemperatureShade']['Minimum']['Value'])
        rfs_list[date] = rfs

    # print(f"{temp_min_list} \n{temp_max_list}")
        
    table1 = pd.DataFrame.from_dict(temp_min_list, orient="index", columns=['Min'])
    table_max = pd.DataFrame.from_dict(temp_max_list, orient="index", columns=['Max'])
    table1['Max'] = table_max
    # print(table1)

    table2 = pd.DataFrame.from_dict(temp_min_list, orient="index", columns=['Minimum'])
    table_rf = pd.DataFrame.from_dict(rf_list, orient="index", columns=['Real Feel'])
    table2['Real Feel'] = table_rf
    table_rfs = pd.DataFrame.from_dict(rfs_list, orient="index",columns=['Real Feel Shade'])
    table2['Real Feel Shade'] = table_rfs
    # print(table2)


    fig1 = px.line(table1)
    fig1.update_traces(mode = 'lines+markers')
    fig1.update_layout(     
        title = {
            'text':'Daily Temperature Trend',
            'y':0.988,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        plot_bgcolor = 'white',
        legend_title= 'Temperature Range',
        xaxis = dict( title_text='Date', showgrid=False, linecolor='black'),
        yaxis = dict(title_text='Temperature (°C)', showgrid=False, linecolor='black')
    )
    fig1.update_yaxes(tick0=0, dtick=1)
    fig1.show()

    fig2 = px.scatter(table2)
    fig2.data[0].update(mode='lines')
    fig2.data[1].update(mode='lines', line=dict(color='royalblue', dash='dash'))
    fig2.data[2].update(mode='markers', marker=dict(color='slategrey', size=12))
    fig2.update_layout(       
        title = {
            'text':'Daily Real Feel & Real Feel Shade Trend',
            'y':0.988,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        plot_bgcolor = 'white',
        legend_title= 'Temperature Range',
        xaxis = dict( title_text='Date', showgrid=False, linecolor='black'),
        yaxis = dict(title_text='Temperature (°C)', showgrid=False, linecolor='black')
    ) 
    fig2.update_yaxes(tick0=0, dtick=1)
    fig2.show()


  



if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))

