import fastf1 as ff1
import pandas as pd
import numpy as np
from fastf1 import plotting 
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection

# Enable the cache
ff1.Cache.enable_cache('cache')

# Enable plotting settings 
ff1.plotting.setup_mpl()

# Choosing an f1 session 
year = int(input("Choose a year between 2015 and 2022 for the session: "))
grand_prix_list = ff1.get_event_schedule(year)
print(grand_prix_list['Location'])

grand_prix = input("\nChoose a Grand Prix from the list:")   
session_type = input("\nChoose session's type (Q or R): ")

session = ff1.get_session(year, grand_prix, session_type)
session.load() # Load the session

print("\nChoose one of the following driver.")
print(session.results['Abbreviation'])
driver = input("\nWrite the driver:")
laps_driver = session.laps.pick_driver(driver)
fastest_driver = laps_driver.pick_fastest()
telemetry_driver = fastest_driver.get_telemetry()

# Team color for plot
team_driver = laps_driver['Team'].iloc[0]
color = ff1.plotting.team_color(team_driver)

# Set the size of the plot
plt.rcParams['figure.figsize'] = [20, 15]
fig, ax = plt.subplots(2, gridspec_kw={'height_ratios': [5,5]})

# Subplot 1: Speed
ax[0].plot(telemetry_driver['Distance'], telemetry_driver['Speed'], label = driver, color = color)
ax[0].set(ylabel = "Speed")
ax[0].legend(loc = "lower right")

distance_values = np.array(telemetry_driver['Distance'].values)
speed_values = np.array(telemetry_driver['Speed'].values)
brake_values = np.array(telemetry_driver['Brake'].values)
time_values = np.array(telemetry_driver['Time'].values)

def longAcceleration():
    acceleration = list()
    
    for i in range(0, distance_values.size): 
        if i == 0:      
            acceleration.append(i)     
        else:
            tmp = i-1            
    
            v_p = speed_values[tmp] # previous speed 
            v_f = speed_values[i] # final speed
            t_p = time_values[tmp] / np.timedelta64(1, 's') # previous time 
            t_f = time_values[i] / np.timedelta64(1, 's') # final time
                        
            acc = (v_f - v_p) / (t_f - t_p)                 
            acceleration.append(acc)
    
        i += 1

    # Subplot 2: Longitudinal Acceleration
    ax[1].plot(telemetry_driver['Distance'], acceleration, label = driver, color = color)
    ax[1].set_ylabel("Long Acc")
    ax[1].set_ylim([-400, 400])
    
longAcceleration()
plt.show()