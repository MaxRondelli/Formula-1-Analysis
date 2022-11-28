import fastf1 as ff1
import pandas as pd
import numpy as np
import math
import csv
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection

# Enable the cache
ff1.Cache.enable_cache('cache')

# Enable plotting settings 
ff1.plotting.setup_mpl()

# Choosing an f1 session 
count = 0
  
# -------------- YEAR SESSION --------------
while count == 0: 
    year = int(input("Choose a year between 2015 and 2022 for the session: "))
    if 2015 <= year <= 2022:
        grand_prix_list = ff1.get_event_schedule(year)
        print(grand_prix_list['Location'])
        count = 1
    else:
        print("\nYear not valid. Try again.")

# -------------- GRAND PRIX --------------
while count == 1:
    grand_prix = input("\nChoose a Grand Prix from the list:")
    for i in grand_prix_list['Location']:
        if i == grand_prix:
            count = 2

    if count == 1:
        print("\nGrand Prix not valid. Try Again")

# -------------- SESSION TYPE --------------
while count == 2:
    session_type = input("\nChoose session type: (FP1, FP2, FP3, Q, R): ")
    if session_type == "FP1" or session_type == "FP2" or session_type == "FP3" or session_type == "Q" or session_type == "R":
        session = ff1.get_session(year, grand_prix, session_type)
        count = 3
    else:
        print("\nSession not valid. Try again")

if count == 3:
    count = 4
    session.load()  # Load the session

# -------------- DRIVER --------------
print("\nChoose one of the following driver.")
print(session.results['Abbreviation'])
while count == 4:
    driver = input("\nWrite the driver:")
    for i in session.results['Abbreviation']:
        if i == driver:
            laps_driver = session.laps.pick_driver(driver)
            fastest_driver = laps_driver.pick_fastest()
            telemetry_driver = fastest_driver.get_telemetry()
            count = -1

    if count == 4:
        print("\nDriver's abbreviation incorrect. Try again.")

# Team color for plot
team_driver = laps_driver['Team'].iloc[0]
color = ff1.plotting.team_color(team_driver)

# Set the size of the plot
plt.rcParams['figure.figsize'] = [20, 15]
fig, ax = plt.subplots(3, gridspec_kw={'height_ratios': [5, 5, 5]})

# Subplot 1: Speed
ax[0].plot(telemetry_driver['Distance'], telemetry_driver['Speed'], label=driver, color = color)
ax[0].set(ylabel="Speed")
ax[0].legend(loc="lower right")


def longAcceleration():
    driver_time = (telemetry_driver['Time'] / np.timedelta64(1, 's')).astype(int)
    driver_speed = telemetry_driver['Speed']
    raw_acceleration_data = []

    for i in range(0, driver_time.size):

        s_p = driver_speed.iloc[i-1]            # Previous speed
        s_f = driver_speed.iloc[i]              # Current speed
        t_p = driver_time.iloc[i-1]             # Previous time
        t_f = driver_time.iloc[i]               # Current time

        with np.errstate(divide='ignore', invalid = 'ignore'):
            acc = ((s_f - s_p) / 3.6) / (t_f - t_p)
            raw_acceleration_data.append(acc)

        acceleration_data = [v for v in raw_acceleration_data if not (math.isinf(v) or math.isnan(v))]

    # Subplot 2: Longitudinal Acceleration
    ax[1].plot(acceleration_data, label="LEC", color = color)
    ax[1].set_ylabel("Long Acceleration")

def latAcceleration():
    if grand_prix == "Imola":
        excel_data = pd.read_excel('Dataset/data_imola_circuit.xlsx') # Load xlsx file
        # Read the values of the file in the dataframe
        df = pd.DataFrame(excel_data)
        
        # |V^2| / r
        
        circuit_distance = telemetry_driver['Distance']
        driver_speed = telemetry_driver['Speed']
        raw_acceleration_data = []

        for i in df.index:
            for j in circuit_distance.index:
                if df['Start meters'][i] <= circuit_distance[j] <= df['End Meters'][i]:
                    radius = df['Radius'][i]
                    speed = driver_speed[j]
                    
                    with np.errstate(divide='ignore', invalid = 'ignore'):
                        acceleration = abs(math.pow(speed, 2)) / radius
                        raw_acceleration_data.append(acceleration)
            
                    print("--------------")
                    print("Start meters: ", df['Start meters'][i])
                    print("\nEnd meters: ", df['End Meters'][i])
                    print("\nCircuit distance: ", circuit_distance[j])
                    print("\nRadius: ", radius)
                    print("\nSpeed: ", speed)
                    print("\nAcceleration: ", acceleration)

                    acceleration_data = [v for v in raw_acceleration_data if not (math.isinf(v) or math.isnan(v))]                    
                    
        print("\n", acceleration_data)
        # Subplot 3: Lateral Acceleration
        ax[2].plot(acceleration_data, label="LEC", color = color)
        ax[2].set_ylabel("Lat Acceleration")
        
        
longAcceleration()
latAcceleration()
plt.show()