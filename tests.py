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
import numpy as np

content = {"data":[{"id":"02","monto_microcreditos":275384.9845599999},{"id":"06","monto_microcreditos":502870.89197999984},{"id":"10","monto_microcreditos":22789.465459999996},{"id":"14","monto_microcreditos":70081.15259},{"id":"18","monto_microcreditos":111354.95793000003},{"id":"22","monto_microcreditos":68863.56604},{"id":"26","monto_microcreditos":8856.5374},{"id":"30","monto_microcreditos":49822.96331000001},{"id":"34","monto_microcreditos":99315.70833999998},{"id":"38","monto_microcreditos":122844.08642000002},{"id":"42","monto_microcreditos":654.9},{"id":"46","monto_microcreditos":34268.54929},{"id":"50","monto_microcreditos":80328.25266},{"id":"54","monto_microcreditos":171044.97708},{"id":"58","monto_microcreditos":26414.14344},{"id":"62","monto_microcreditos":51082.182010000026},{"id":"66","monto_microcreditos":135168.57346999997},{"id":"70","monto_microcreditos":7760.468980000001},{"id":"74","monto_microcreditos":35113.007059999996},{"id":"78","monto_microcreditos":229.362},{"id":"82","monto_microcreditos":122376.88891},{"id":"86","monto_microcreditos":31186.988860000005},{"id":"90","monto_microcreditos":102167.94277999997},{"id":"94","monto_microcreditos":3322.51505}],"colors":["#ffffe5","#f7fcb9","#d9f0a3","#addd8e","#78c679","#41ab5d","#238443","#006837","#004529"],"provincia":"id","datos":"monto_microcreditos","title":"","classification":["0","10000","30000","60000","120000","240000","350000"],"datatable":True,"legend":True}


#%%


# dataframes
df = pd.DataFrame(content['data'])
file = 'data/provincias_sin_antartida.geojson'
gdf = gpd.read_file(file)
df = pd.merge(gdf, df, right_on='id', left_on=content['provincia'])
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

# datatable
col_labels = ['Provincia', 'Cantidad']
df_table = df[['name', content['datos']]].sort_values(
    by='name', ascending=True).head(25)
table_vals = df_table.values.tolist()

the_table = plt.table(cellText=table_vals,
                        colWidths=[0]*len(table_vals),
                        colLabels=col_labels,
                        loc='right', zorder=3)
# legend
if content['legend']:
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1.4, 0.05, 0.2, 0.2))

# bytesio output
mapa = io.BytesIO()

plt.savefig(mapa, format='png', bbox_inches='tight')

#%%

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
rect = [0.2,0.2,0.7,0.7]
# %%

#%%
left_inset_ax.show()