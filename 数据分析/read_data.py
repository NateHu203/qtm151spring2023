import pandas as pd
import seaborn as sns
sns.set()
import os




def getcsv():
    circuits = pd.read_csv("mydata/circuits.csv")
    constructor_results = pd.read_csv('mydata/constructor_results.csv', delimiter=',')

    qualifying = pd.read_csv('mydata/qualifying.csv', delimiter=',')
    qualifying = qualifying[['driverId','position']]

    laptimes = pd.read_csv('mydata/lap_times.csv', delimiter=',')
    laptimes = laptimes[['raceId','driverId','lap','milliseconds']]

    drivers = pd.read_csv('mydata/drivers.csv', delimiter=',')
    driver_standings = pd.read_csv('mydata/driver_standings.csv', delimiter=',')
    driver_result = pd.read_csv('mydata/results.csv', delimiter=',')

    races = pd.read_csv('mydata/races.csv', delimiter=',')
    races_date = races[['date', 'circuitId', 'raceId']]
    races_date['date'] = pd.to_datetime(races_date['date'])

    # merge
    df1 = pd.merge(driver_result, races, on ='raceId')
    df_race= pd.merge(df1, drivers, on = 'driverId')

    posterior_data = ['laps', 'milliseconds', 'fastestLap', 'fastestLapTime', 'fastestLapSpeed', 'statusId', 'time_x', 'time_y', 'positionOrder']
    df_race = df_race.drop(columns=posterior_data)

    # Drop redundant positon and positionText column
    df_race = df_race.drop(columns=['position',  'positionText', 'number_x', 'sprint_date', 'sprint_time', 'driverRef', 'number_y', 'nationality', 'url_x', 'url_y', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'quali_date', 'quali_time', 'fp3_date', 'fp3_time', 'name'])
    return df_race, races, circuits, drivers, constructor_results, laptimes, qualifying, driver_standings


















