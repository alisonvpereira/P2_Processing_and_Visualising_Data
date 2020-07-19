import json
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

    header = str()
    body = str()
    temp_min_list = {}
    temp_max_list = {}

    for n in fcast['DailyForecasts']:
        date = convert_date(n['Date'])
        temp_min = convert_f_to_c(n['Temperature']['Minimum']['Value'])
        temp_max = convert_f_to_c(n['Temperature']['Maximum']['Value'])
        daytime = n['Day']['LongPhrase']
        daytime_rain = n['Day']['RainProbability']
        nighttime = n['Night']['LongPhrase']
        nighttime_rain = n['Night']['RainProbability']
        temp_min_list[date] = temp_min
        temp_max_list[date] = temp_max
        

        body = body + (f"\n-------- {date} --------\
\nMinimum Temperature: {format_temperature(temp_min)}\
\nMaximum Temperature: {format_temperature(temp_max)}\
\nDaytime: {daytime}\
\n    Chance of rain:  {daytime_rain}%\
\nNighttime: {nighttime}\
\n    Chance of rain:  {nighttime_rain}%\
\n")


    # temp_min_list[temp_min] = convert_f_to_c(n['Temperature']['Minimum']['Value'])
    # temp_max_list[temp_max] = convert_f_to_c(n['Temperature']['Minimum']['Value'])
    n = len(fcast['DailyForecasts'])
    min_date = min(temp_min_list, key=temp_min_list.get)
    min_value = temp_min_list[min_date]
    max_date = max(temp_max_list, key=temp_max_list.get)
    max_value = temp_max_list[max_date]
    min_mean = calculate_mean(sum(temp_min_list.values()),n)
    max_mean = calculate_mean(sum(temp_max_list.values()),n)
        
    header = f"{n} Day Overview\
\n    The lowest temperature will be {format_temperature(str(min_value))}, and will occur on {min_date}.\
\n    The highest temperature will be {format_temperature(str(max_value))}, and will occur on {max_date}.\
\n    The average low this week is {format_temperature(min_mean)}.\
\n    The average high this week is {format_temperature(max_mean)}."

    return(header+ "\n" + body + "\n")
        
        



if __name__ == "__main__":
    print(process_weather(test_data))





