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
year = int(input("Scegli un anno per la sessione tra il 2015 e 2022 compresi: "))
grand_prix_list = ff1.get_event_schedule(year)
print(grand_prix_list['Location'])

grand_prix = input("\nScegli un Grand Prix della sessione tra le seguenti opzioni: ")   
session_type = input("\nScegli la tipologia di sessione (Q o R): ")

session = ff1.get_session(year, grand_prix, session_type)
session.load()