import pandas as pd
import numpy as np
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import handle
import read_data


def firt(df_race, df_driver):
    f, axes = plt.subplots(9, 3, figsize=(20, 24))
    df_numeric = pd.DataFrame(df_race[['grid', 'points', 'year', 'round', 'age']])
    plt.tight_layout()
    count = 0
    for var in df_numeric:
        sns.histplot(data=df_numeric[var], ax=axes[count, 0])
        sns.boxplot(data=df_numeric[var], orient="h", ax=axes[count, 1])
        sns.violinplot(data=df_numeric[var], orient="h", ax=axes[count, 2])
        count += 1
    df_numeric_1 = pd.DataFrame(df_driver[['totalRaces', 'winRate', 'fastestLapRate', 'qualifyingWinRate']])
    for var in df_numeric_1:
        sns.histplot(data=df_numeric_1[var], ax=axes[count, 0])
        sns.boxplot(data=df_numeric_1[var], orient="h", ax=axes[count, 1])
        sns.violinplot(data=df_numeric_1[var], orient="h", ax=axes[count, 2])
        count += 1


def Categorical(df_race):
    f, axes = plt.subplots(3, 1, figsize=(20, 30))
    df_cat = pd.DataFrame(df_race[['grid', 'points', 'age', 'rank']])
    count = 0
    for col in df_cat:
        if col != 'rank':
            sns.boxplot(data=df_race, x=col, y='rank',
                        order=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                               '17', '18', '19', '20', '\\N'], ax=axes[count])
    plt.figure(figsize=(17, 12))
    sns.heatmap(df_race.corr(), annot=True)
    plt.show()


def im(point_year_divided, age_year):
    # Loop through each team
    # Column name is ID of each team
    point_first_half_all = []
    whole_year_point_all = []
    for column in point_year_divided:
        point_year_driver_divided = point_year_divided[column].unstack()
        point_first_half = []
        whole_year_point = []
        ages = []
        age_one_year = age_year[column].unstack()
        point_year_driver_divided = pd.merge(point_year_driver_divided, age_one_year, on='date')
        # Loop through each year
        for row in point_year_driver_divided.iterrows():
            if not np.isnan(row[1][0]) and not np.isnan(row[1][1]) and (
                    not np.isnan(row[1][2]) or not np.isnan(row[1][3])):
                if not np.isnan(row[1][2]):
                    age = row[1][2]
                else:
                    age = row[1][3]
                ages.append(age)
                point_first_half.append(row[1][1])
                point_first_half_all.append((row[1][1], age))
                whole_year_point.append(row[1][0] + row[1][1])
                whole_year_point_all.append(row[1][0])
        new_df = pd.DataFrame(
            {'first_half_point': point_first_half, 'ages': ages, 'whole_year_point': whole_year_point})
        sns.scatterplot(x='first_half_point', y='whole_year_point', data=new_df)
        plt.show()


if __name__ == '__main__':
    # 获取元数据
    df_race, races, circuits, drivers, constructor_results, laptimes, qualifying, driver_standings = read_data.getcsv()
    # 经过合并处理
    df_driver, df_race = handle.engineer(df_race, drivers, races, driver_standings)

    df_drivers = handle.ser(laptimes, df_driver, qualifying, df_race)
    point_year_divided, age_year = handle.clasity(df_race)
    # 作图
    Categorical(df_race)
    im(point_year_divided, age_year)