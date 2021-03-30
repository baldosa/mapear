#%%
from PIL import Image
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
import numpy as np

content = {"data":[
    {'cod': '74',   'val': 114.05231071276813},
    {'cod': '02', 'val': 166.89022208667708},
    {'cod': '14', 'val': 174.76769243042722},
    {'cod': '82', 'val': 206.36935565874847},
    {'cod': '26', 'val': 227.98515494495908},
    {'cod': '50', 'val': 232.25149899162855},
    {'cod': '86', 'val': 285.6783585621371},
    {'cod': '18', 'val': 300.2126149066605},
    {'cod': '42', 'val': 350.39976229535637},
    {'cod': '62', 'val': 408.2176883669293},
    {'cod': '58', 'val': 428.95755936613875},
    {'cod': '30', 'val': 432.9430691051191},
    {'cod': '70', 'val': 471.88685090058203},
    {'cod': '90', 'val': 474.4596578892707},
    {'cod': '54', 'val': 479.2974738641427},
    {'cod': '46', 'val': 581.5087883800768},
    {'cod': '66', 'val': 590.5813042290878},
    {'cod': '10', 'val': 606.1399751587481},
    {'cod': '78', 'val': 665.7789925020098},
    {'cod': '22', 'val': 667.3852504813036},
    {'cod': '06', 'val': 676.6826799351307},
    {'cod': '94', 'val': 742.5731871857558},
    {'cod': '34', 'val': 1096.0113649695222},
    {'cod': '38', 'val': 1151.4888873898824},
    ],"colors":["#ffffe5","#f7fcb9","#d9f0a3","#addd8e","#78c679","#41ab5d","#238443","#006837","#004529"],
    "provincia": "cod",
    "val": "monto_microcreditos",
    "title":"","classification":["0","10000","30000","60000","120000","240000","350000"],
    "datatable":True,"legend":True}


#%%

print(content)
# dataframes
df = pd.DataFrame(content['data'])
df['id'] = df[content['provincia']]
file = 'data/provincias_sin_antartida.geojson'
gdf = gpd.read_file(file)
df = pd.merge(gdf, df, right_on=['id'], left_on='id')
df[content['datos']] = df[content['datos']].round(decimals=2)

# color settings
cmap_colors = pltcolors.LinearSegmentedColormap.from_list(
    "", content['colors'])

# plot
ax = df.plot(column=content['datos'],
             cmap=cmap_colors,
             figsize=(30, 13),
             edgecolor="grey",
             linewidth=0.4,
             legend=content['legend'],
             scheme="userdefined",
             classification_kwds={'bins': [float(i) for i in content['classification']]})

ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
plt.title(content['title'])

# legend
if content['legend']:
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1.4, 0.05, 0.2, 0.2))

# datatable
if content['datatable']:
    col_labels = ['Provincia', 'Cantidad']
    df_table = df[['name', content['datos']]].sort_values(
        by='name', ascending=True).head(25)
table_vals = df_table.values.tolist()

the_table = plt.table(cellText=table_vals,
                        colWidths=[0]*len(table_vals),
                        colLabels=col_labels,
                        loc='right', zorder=3)
the_table.auto_set_column_width(col=list(range(len(table_vals))))

# bytesio output
aio = io.BytesIO()

plt.savefig(aio, format='png', bbox_inches='tight')
data = base64.encodestring(aio.getvalue())


# %%
# gdf


df

# %%
df1 = pd.merge(gdf, df, right_on='id', left_on='cod')
