#%%
import matplotlib
import io
import base64
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as pltcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
# matplotlib.use('Agg')
# %matplotlib inline


#%%
df = gpd.read_file('data/provincias-na.json')
df
#%%
df = df.drop(columns=['centr_lon'])
df = df.drop(columns=['centr_lat'])
df = df.drop(columns=['nombre'])

#%%
df.to_file("data/provincias-na.json", driver='GeoJSON')


#%%
df.drop(15, inplace=True)
df