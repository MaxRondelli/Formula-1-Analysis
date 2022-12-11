import fastf1 as ff1
import pandas as pd
import numpy as np
import math
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

# -------------- DRIVER 1 --------------
print("\nChoose one of the following driver.")
print(session.results['Abbreviation'])
while count == 4:
    driver_1 = input("\nWrite the driver 1:")
    for i in session.results['Abbreviation']:
        if i == driver_1:
            laps_driver_1 = session.laps.pick_driver(driver_1) 
            fastest_driver_1 = laps_driver_1.pick_fastest() 
            telemetry_driver_1 = fastest_driver_1.get_telemetry() 

            count = 5

    if count == 4:
        print("\nDriver's abbreviation incorrect. Try again.")
        
# -------------- DRIVER 2 --------------
print("\nChoose one of the following driver.")
print(session.results['Abbreviation'])
while count == 5:
    driver_2 = input("\nWrite the driver 2:")
    for i in session.results['Abbreviation']:
        if i == driver_2:
            laps_driver_2 = session.laps.pick_driver(driver_2) 
            fastest_driver_2 = laps_driver_2.pick_fastest() 
            telemetry_driver_2 = fastest_driver_2.get_telemetry() 

            count = -1

    if count == 5:
        print("\nDriver's abbreviation incorrect. Try again.")
        
# Variables for the plots
team_driver_1 = fastest_driver_1['Team']
team_driver_2 = fastest_driver_2['Team']

driver_speed_1 = telemetry_driver_1['Speed']
driver_speed_2 = telemetry_driver_2['Speed']

driver_throttle_1 = telemetry_driver_1['Throttle']
driver_throttle_2 = telemetry_driver_2['Throttle']

driver_brake_1 = telemetry_driver_1['Brake']
driver_brake_2 = telemetry_driver_2['Brake']

driver_gear_1 = telemetry_driver_1['nGear']
driver_gear_2 = telemetry_driver_2['nGear']

driver_distance_1 = telemetry_driver_1['Distance']
driver_distance_2 = telemetry_driver_2['Distance']

# Plot configuration
plot_size = [15,15]
plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1}"
plot_ratios = [1, 3, 2, 1, 1, 2, 1]
plot_filename = plot_title.replace(" ", " ") + ".png"

plt.rcParams['figure.figsize'] = [20, 15]
fig, ax = plt.subplots(7, gridspec_kw={'height_ratios': [5, 5, 5, 5, 5, 7, 7]})

# Subplot 1: Speed
ax[0].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver_1, color = ff1.plotting.team_color(team_driver_1))
ax[0].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver_2, color = ff1.plotting.team_color(team_driver_2))
ax[0].set(ylabel='Speed')
ax[0].legend(loc="lower right")

# Subplot 2: Throttle
ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
ax[1].set(ylabel='Throttle')

# Subplot 3: Brake
ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
ax[2].set(ylabel='Brake')

# Subplot 4: Gear
ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
ax[3].set(ylabel='Gear')

# Subplot 5: RPM
ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
ax[4].set(ylabel='RPM')

def longAcceleration():
    driver_time_1 = (telemetry_driver_1['Time'] / np.timedelta64(1, 's')).astype(float)
    driver_time_2 = (telemetry_driver_2['Time'] / np.timedelta64(1, 's')).astype(float)
    
    driver_speed_1 = telemetry_driver_1['Speed']
    driver_speed_2 = telemetry_driver_2['Speed']
    
    raw_acceleration_data_1 = []
    raw_acceleration_data_2 = []

    for i in driver_time_1.index:
        if i > 0 and i < driver_time_1.size:
            s_p = driver_speed_1.iloc[i-1]            # Previous speed
            s_f = driver_speed_1.iloc[i]              # Current speed
            t_p = driver_time_1.iloc[i-1]             # Previous time
            t_f = driver_time_1.iloc[i]               # Current time

            with np.errstate(divide='ignore', invalid = 'ignore'):
                acc = ((s_f - s_p) / 3.6) / (t_f - t_p)
                g_force = acc / 9.81
                raw_acceleration_data_1.append(g_force)
               
            acceleration_data_1 = [v for v in raw_acceleration_data_1 if not (math.isinf(v) or math.isnan(v) or v < -6.0 or v > 6)]

    for i in driver_time_2.index:
            if i > 0 and i < driver_time_2.size:
                s_p = driver_speed_2.iloc[i-1]          # Previous speed
                s_f = driver_speed_2.iloc[i]            # Current speed
                t_p = driver_time_2.iloc[i-1]           # Previous time
                t_f = driver_time_2.iloc[i]             # Current time

                with np.errstate(divide='ignore', invalid = 'ignore'):
                    acc = ((s_f - s_p) / 3.6) / (t_f - t_p)
                    g_force = acc / 9.81
                    raw_acceleration_data_2.append(g_force)
                    
                acceleration_data_2 = [v for v in raw_acceleration_data_2 if not (math.isinf(v) or math.isnan(v) or v < -6.0 or v > 6)]

    # Subplot 5: Longitudinal Acceleration
    ax[5].plot(acceleration_data_1, label = driver_1, color = ff1.plotting.team_color(team_driver_1))
    ax[5].plot(acceleration_data_2, label = driver_2, color = ff1.plotting.team_color(team_driver_2))
    ax[5].set_ylabel("Long Acc")

            
def latAcceleration():
    if grand_prix == "Imola":
        if driver_1 == "VER" or driver_2 == "VER":
            driver = "VER"
            laps_driver = session.laps.pick_driver(driver) 
            fastest_driver = laps_driver.pick_fastest() 
            telemetry_driver = fastest_driver.get_telemetry() 
            team_driver = fastest_driver['Team']
                    
            driver_time = (telemetry_driver['Time'] / np.timedelta64(1, 's')).astype(float)
            driver_speed = telemetry_driver['Speed']
            
            excel_data = pd.read_excel('Dataset/tempi_curve.xlsx')                  # Load xlsx file
            df = pd.DataFrame(excel_data)                                           # Read the values of the file in the dataframe
        
            raw_acceleration_data = []

            for i in df.index:
                for j in driver_time.index:
                    if df['Start time'][i] <= driver_time[j] <= df['End time'][i]:
                        radius = df['Radius'][i]
                        speed = driver_speed[j]
                        
                        with np.errstate(divide='ignore', invalid = 'ignore'):
                                speed_ms = speed / 3.6                               # Speed in meters/seconds
                                acceleration = (math.pow(speed_ms, 2)) / radius
                                g_force = acceleration / 9.81
                                raw_acceleration_data.append(g_force)    

                        acceleration_data = [v for v in raw_acceleration_data if not (math.isinf(v) or math.isnan(v) or v > 6.0 or v == 0)]    
            
            # Subplot 6: Lateral Acceleration
            ax[6].plot(acceleration_data, label = driver, color = ff1.plotting.team_color(team_driver))
            ax[6].set(ylabel='Lat Acc')       
        
longAcceleration()
latAcceleration()

# using padding
fig.tight_layout(pad=2.5)
plt.show()