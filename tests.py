#%%
from PIL import Image
from textwrap import wrap
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
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
#bottom_right = (1.4, 0.1)

content = {
    "data":[{"Código":74,"Total prestaciones PACH per cápita":114.05231071276813},{"Código":"02","Total prestaciones PACH per cápita":166.89022208667708},{"Código":"14","Total prestaciones PACH per cápita":174.76769243042722},{"Código":"82","Total prestaciones PACH per cápita":206.36935565874847},{"Código":"26","Total prestaciones PACH per cápita":227.98515494495908},{"Código":"50","Total prestaciones PACH per cápita":232.25149899162855},{"Código":"86","Total prestaciones PACH per cápita":285.6783585621371},{"Código":"18","Total prestaciones PACH per cápita":300.2126149066605},{"Código":"42","Total prestaciones PACH per cápita":350.39976229535637},{"Código":"62","Total prestaciones PACH per cápita":408.2176883669293},{"Código":"58","Total prestaciones PACH per cápita":428.95755936613875},{"Código":"30","Total prestaciones PACH per cápita":432.9430691051191},{"Código":"70","Total prestaciones PACH per cápita":471.88685090058203},{"Código":"90","Total prestaciones PACH per cápita":474.4596578892707},{"Código":"54","Total prestaciones PACH per cápita":479.2974738641427},{"Código":"46","Total prestaciones PACH per cápita":581.5087883800768},{"Código":"66","Total prestaciones PACH per cápita":590.5813042290878},{"Código":"10","Total prestaciones PACH per cápita":606.1399751587481},{"Código":"78","Total prestaciones PACH per cápita":665.7789925020098},{"Código":"22","Total prestaciones PACH per cápita":667.3852504813036},{"Código":"06","Total prestaciones PACH per cápita":676.6826799351307},{"Código":"94","Total prestaciones PACH per cápita":742.5731871857558},{"Código":"34","Total prestaciones PACH per cápita":1096.0113649695222},{"Código":"38","Total prestaciones PACH per cápita":1151.4888873898824}],
    "colors":["#eff3ff","#bdd7e7","#6baed6","#2171b5"],
    "provincia":"Código",
    "datos":"Total prestaciones PACH per cápita",
    "title":"TITLO",
    "classification":["114.05231071276813","350.39976229535637","742.5731871857558","1151.4888873898824"],
    "datatable":True,
    "legend":True,
    "con_antartida": True,
    }
#%%
file_sin_antartida = 'data/provincias_sin_antartida.geojson'
file_con_antartida = 'data/provincias_con_antartida.geojson'

# dataframes
df_data = pd.DataFrame(content['data'])
df_data['id'] = df_data[content['provincia']]


gdf_sin_antartida = gpd.read_file(file_sin_antartida)

# si tengo antártida como option lo levanto 
if content['con_antartida']:
    gdf_con_antartida = gpd.read_file(file_con_antartida)
    df_data_con_antartidad = pd.merge(
        gdf_con_antartida, df_data, right_on='id', left_on='id')


df_data = pd.merge(gdf_sin_antartida, df_data, right_on='id', left_on='id')

df_data[content['datos']] = df_data[content['datos']].round(0).astype(int)

# color settings
cmap_colors = pltcolors.LinearSegmentedColormap.from_list(
    "", content['colors'])


df_data
#%%
# big plot
f, ax = plt.subplots(figsize=(30, 13))
df_data.plot(ax=ax, column=content['datos'],
        cmap=cmap_colors,
        figsize=(30, 13),
        edgecolor="grey",
        linewidth=0.4,
        legend=content['legend'],
        scheme="userdefined",
        classification_kwds={'bins': [int(float(i)) for i in content['classification']]})

# CABA PLOT
ax_caba = zoomed_inset_axes(ax, 10, loc=7)

minx,miny,maxx,maxy =  df_data.query('id == "02"').total_bounds
ax_caba.set_xlim(minx, maxx)
ax_caba.set_ylim(miny, maxy)
df_data.query('id == "02"').plot(
    ax=ax_caba,
    column=content['datos'],
    cmap=cmap_colors,
    figsize=(30, 13),
    edgecolor="grey",
    linewidth=0.4,
    scheme="userdefined",
    classification_kwds={'bins': [int(float(i)) for i in content['classification']]}
)

dual_ax = mark_inset(ax, ax_caba, loc1=1, loc2=1, fc="none", ec="0.5")

# chart settings
ax.axes.xaxis.set_ticklabels([])
ax.axes.yaxis.set_ticklabels([])
ax_caba.axes.xaxis.set_ticklabels([])
ax_caba.axes.yaxis.set_ticklabels([])

# save file to bytess
arg_file = io.BytesIO()
plt.savefig(arg_file, format='png', bbox_inches='tight')


#%%
if content['con_antartida']:
    f, ax_tdf = plt.subplots(figsize=(2, 2))
    df_data_con_antartidad.plot(
        ax=ax_tdf,
        column=content['datos'],
        cmap=cmap_colors,
        figsize=(30, 13),
        edgecolor="grey",
        linewidth=0.4,
        scheme="userdefined",
        classification_kwds={'bins': [float(i)
                                    for i in content['classification']]}
    )
    minx, miny, maxx, maxy =  df_data_con_antartidad.query('id == "94"').total_bounds
    ax_tdf.set_xlim(minx, maxx)
    ax_tdf.set_ylim(miny, maxy)
    plt.setp(ax_tdf.get_xticklabels(), visible=False)
    plt.setp(ax_tdf.get_yticklabels(), visible=False)

    # save file
    tdf_file = io.BytesIO()
    plt.savefig(tdf_file, format='png', bbox_inches='tight')

    # merge pngs
    background = Image.open(arg_file)
    foreground = Image.open(tdf_file)

    background.paste(foreground, tuple(map(lambda i, j: i - j-10, background.size, foreground.size)), foreground)

    background.save(arg_file)
#%%
from PIL import Image

background = Image.open('arg.png')
foreground = Image.open('tdf.png')

background.paste(foreground, tuple(map(lambda i, j: i - j-10, background.size, foreground.size)), foreground)

background.save('test.png')


#%%
width, height = background.size

print(background.size)
print(foreground.size)
print(tuple(map(lambda i, j: i - j-15, background.size, foreground.size)))


#%%
#bottom_right = (1.4, 0.1)

from textwrap import wrap

content['datos'][:int(len(content['datos'])/2)]

"\n".join(wrap(content['datos'], 20))

#%%
df_data = pd.DataFrame(content['data'])
df_data['id'] = df_data[content['provincia']]

#%%
df_data.iloc[0]