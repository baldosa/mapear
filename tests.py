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
content = {
    "classification": [
        0,
        10000,
        30000,
        60000,
        120000,
        240000,
        350000
    ],
    "colors": [
        "#ffffe5",
        "#f7fcb9",
        "#d9f0a3",
        "#addd8e",
        "#78c679",
        "#41ab5d",
        "#238443",
        "#006837",
        "#004529"
    ],
    "data": [
        {
            "id": "02",
            "monto_microcreditos": 275384984.5599999
        },
        {
            "id": "06",
            "monto_microcreditos": 502870891.97999984
        },
        {
            "id": "10",
            "monto_microcreditos": 22789465.459999997
        },
        {
            "id": "14",
            "monto_microcreditos": 70081152.59
        },
        {
            "id": "18",
            "monto_microcreditos": 111354957.93000004
        },
        {
            "id": "22",
            "monto_microcreditos": 68863566.04
        },
        {
            "id": "26",
            "monto_microcreditos": 8856537.399999999
        },
        {
            "id": "30",
            "monto_microcreditos": 49822963.31000001
        },
        {
            "id": "34",
            "monto_microcreditos": 99315708.33999999
        },
        {
            "id": "38",
            "monto_microcreditos": 122844086.42000002
        },
        {
            "id": "42",
            "monto_microcreditos": 654900
        },
        {
            "id": "46",
            "monto_microcreditos": 34268549.29
        },
        {
            "id": "50",
            "monto_microcreditos": 80328252.66
        },
        {
            "id": "54",
            "monto_microcreditos": 171044977.08
        },
        {
            "id": "58",
            "monto_microcreditos": 26414143.44
        },
        {
            "id": "62",
            "monto_microcreditos": 51082182.01000003
        },
        {
            "id": "66",
            "monto_microcreditos": 135168573.46999997
        },
        {
            "id": "70",
            "monto_microcreditos": 7760468.98
        },
        {
            "id": "74",
            "monto_microcreditos": 35113007.059999995
        },
        {
            "id": "78",
            "monto_microcreditos": 229362
        },
        {
            "id": "82",
            "monto_microcreditos": 122376888.91
        },
        {
            "id": "86",
            "monto_microcreditos": 31186988.860000003
        },
        {
            "id": "90",
            "monto_microcreditos": 102167942.77999997
        },
        {
            "id": "94",
            "monto_microcreditos": 3322515.05
        }
    ],
    "datatable": True,
    "datos": "monto_microcreditos",
    "legend": True,
    "provincia": "id",
    "title": "Test"
}
#%%
df = pd.DataFrame(content['data'])
file = 'data/provincias-na.json'
gdf = gpd.read_file(file)
df = pd.merge(gdf, df, right_on='id', left_on=content['provincia'])
df[content['datos']] = df[content['datos']].round(decimals=2)
#%%
# color settings
cmap_colors = pltcolors.LinearSegmentedColormap.from_list(
    "", content['colors'])

# plot
ax = df.plot(column=content['datos'],
            cmap=cmap_colors,
            figsize=(30, 13),
            edgecolor="grey",
            linewidth=1,
            legend=content['legend'],
            scheme="userdefined",
            classification_kwds={'bins': content['classification']})

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
        by=content['datos'], ascending=False).head(25)
    table_vals = df_table.values.tolist()

    the_table = plt.table(cellText=table_vals,
                        colWidths=[0]*len(table_vals),
                        colLabels=col_labels,
                        loc='right', zorder=3)
    the_table.auto_set_column_width(col=list(range(len(table_vals))))

#plt.show()
# df_table.to_excel(f'maps/GBA.xlsx')
# plt.savefig(f'maps/GBA.png', dpi=250, orientation='lanscape')
plt.show()
plt.close()

#%%
plt.show()


