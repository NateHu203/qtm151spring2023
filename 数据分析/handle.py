import os
import pandas as pd
import numpy as np
from datetime import datetime


def engineer(df_race, drivers, races, driver_standings):
    # feature engineer
    # Change mydata type from string to datetime
    df_race['dob'] = pd.to_datetime(df_race['dob'])
    df_race['date'] = pd.to_datetime(df_race['date'])

    dates = datetime.today() - df_race['dob']
    age = dates.dt.days / 365
    df_race['age'] = round(age)

    df_driver = drivers.copy()
    df_driver['totalWins'] = 0

    race_dates = races[['raceId', 'date']]
    # adding dates to each race
    driver_standings = driver_standings.merge(race_dates[['raceId', 'date']], how='left', on='raceId')

    # Convert the "date" column to a datetime object
    driver_standings['date'] = pd.to_datetime(driver_standings['date'])

    # Create a new column 'year' to extract the year from the 'date' column
    driver_standings['year'] = driver_standings['date'].dt.year

    # count the number of races each driver has driven in
    num_races_per_driver = driver_standings.groupby('driverId')['raceId'].nunique()
    num_races_per_driver_df = num_races_per_driver.reset_index()
    num_races_per_driver_df = num_races_per_driver_df.rename(columns={'raceId': 'totalRaces'})

    for index, row in df_driver.iterrows():
        driverId = row['driverId']

        # filtering out rows with ['driverId'] == driverId
        driver_standings_csv_driverId = driver_standings[driver_standings['driverId'] == driverId]

        # Group the dataframe by year and find the maximum date for each year
        latest_day_in_year = driver_standings_csv_driverId.groupby(driver_standings_csv_driverId['date'].dt.year)[
            'date'].max()

        # Use the latest day in each year to filter the original dataframe
        filtered_dataframe = driver_standings_csv_driverId.loc[
            driver_standings_csv_driverId['date'].isin(latest_day_in_year)]

        total_wins = filtered_dataframe['wins'].sum()

        index = df_driver.index[df_driver['driverId'] == driverId].tolist()[0]
        df_driver.at[index, 'totalWins'] = total_wins

        df_driver = df_driver.merge(num_races_per_driver_df, how='left', on='driverId')

        # calculate win rate and drop totalWins columns
        df_driver['winRate'] = df_driver['totalWins'] / df_driver['totalRaces']
        df_driver = df_driver.drop(['totalWins'], axis=1)
        df_driver['dob'] = pd.to_datetime(df_driver['dob'])
        df_driver['age'] = 2023 - df_driver['dob'].dt.year
        print(df_driver.head())
        return df_driver, df_race


def ser(laptimes,  df_driver, qualifying, df_race):
    # Group the dataframe by raceId and find the index of the row with the minimum milliseconds
    idx = laptimes.groupby('raceId')['milliseconds'].idxmin()

    # Use the index to select the rows with the minimum milliseconds for each raceId
    df_min_milliseconds = laptimes.loc[idx]

    # Sort the result by raceId
    df_min_milliseconds.sort_values('raceId', inplace=True)

    counts = pd.DataFrame(df_min_milliseconds['driverId'].value_counts())
    counts.columns = ['totalFastestLaps']
    counts['driverId'] = counts.index
    counts.reset_index(drop=True, inplace=True)

    # adding totalFastestLaps to df maindata_wnames
    df_driver = df_driver.merge(counts, how='left', on='driverId')
    df_driver = df_driver.fillna(0)

    # calculate fastest lap rate and drop totalFastestLaps
    df_driver['fastestLapRate'] = df_driver['totalFastestLaps'] / df_driver['totalRaces']
    df_driver = df_driver.drop(['totalFastestLaps'], axis=1)

    # PRINT CURRENT DATASET
    print(df_driver.head())

    position_1_counts = qualifying[qualifying['position'] == 1].groupby('driverId')['position'].count().reset_index()

    # Rename the 'position' column to 'position_1_count'
    position_1_counts = position_1_counts.rename(columns={'position': 'position_1_count'})

    # # Print the resulting DataFrame
    # position_1_counts.head()

    # merge
    df_driver = df_driver.merge(position_1_counts, how='left', on='driverId')
    df_driver = df_driver.fillna(0)

    # calculate fastest lap rate and drop totalFastestLaps
    df_driver['qualifyingWinRate'] = df_driver['position_1_count'] / df_driver['totalRaces']
    df_driver = df_driver.drop(['position_1_count'], axis=1)

    # filling in NaN values for qualifyingWinRate
    df_driver.fillna(0, inplace=True)

    # Number of mydata point
    print("Number of mydata point for race dataframe: " + str(df_race.shape[0]))
    print("Number of mydata point for driver dataframe: " + str(df_driver.shape[0]))

    print("Data frame driver information")
    print(df_driver.info())
    return df_driver



 # Clasify race as the first half and second half by a new variable first_half
def clasity(df_race):
    driver_result_withdate_divided = df_race.copy()
    driver_result_withdate_divided['firstHalf'] = (driver_result_withdate_divided['date'].dt.month <= 6).astype(int)

    driver_result_withdate_groupby_year_divided = driver_result_withdate_divided.groupby(
        [driver_result_withdate_divided['date'].dt.year, driver_result_withdate_divided['firstHalf'],
         driver_result_withdate_divided['driverId']])
    point_year_divided = driver_result_withdate_groupby_year_divided["points"].sum().unstack()

    age_year = driver_result_withdate_groupby_year_divided["age"].mean().unstack()
    return point_year_divided, age_year