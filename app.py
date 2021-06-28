
from flask import Flask, render_template, request, Response, send_file


import matplotlib
import io
import base64
from PIL import Image
from textwrap import wrap
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as pltcolors
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset

from mpl_toolkits.axes_grid1 import make_axes_locatable
matplotlib.use('Agg')


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def mapping():
    content = request.json
    
    # files
    file_sin_antartida = 'data/provincias_sin_antartida.geojson'
    file_con_antartida = 'data/provincias_con_antartida.geojson'

    # dataframes
    df_data = pd.DataFrame(content['data'])
    df_data['id'] = df_data[content['provincia']].astype(str)
    
    df_data[content['datos']] = df_data[content['datos']].astype(int)

    gdf_sin_antartida = gpd.read_file(file_sin_antartida)

    # si tengo antártida como option lo levanto 
    if content['antartida']:
        gdf_con_antartida = gpd.read_file(file_con_antartida)
        df_data_con_antartidad = pd.merge(
            gdf_con_antartida, df_data, right_on='id', left_on='id')



    df_data = pd.merge(gdf_sin_antartida, df_data, right_on='id', left_on='id')

    # color settings
    cmap_colors = pltcolors.LinearSegmentedColormap.from_list(
        "", content['colors'])


    # big plot
    f, ax = plt.subplots(figsize=(30, 13))
    df_data.plot(ax=ax, column=content['datos'],
            cmap=cmap_colors,
            figsize=(30, 13),
            edgecolor="grey",
            linewidth=0.4,
            legend=content['legend'],
            scheme="userdefined",
            classification_kwds={'bins': [float(i) for i in content['classification']]})

    plt.title(content['title'])

    
    # legend
    if content['legend']:
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((1.4, 0.1))

    # datatable
    if content['datatable']:
        col_labels = ['Provincia', "\n".join(wrap(content['datos'], 20))]
        df_table = df_data[['name', content['datos']]].sort_values(
            by='name', ascending=True).head(25)
        table_vals = df_table.values.tolist()

        the_table = plt.table(cellText=table_vals,
                              colWidths=[0]*len(table_vals),
                              colLabels=col_labels,
                              loc='right', zorder=3)
        the_table.auto_set_column_width(col=list(range(len(table_vals))))
        the_table.set_fontsize(14)
        the_table.scale(1, 1.7)

    # CABA PLOT
    ax_caba = zoomed_inset_axes(ax, 10, loc=7)

    minx,miny,maxx,maxy =  df_data.query('id == "02"').total_bounds
    ax_caba.set_xlim(minx, maxx)
    ax_caba.set_ylim(miny, maxy)
    df_data.plot(
        ax=ax_caba,
        column=content['datos'],
        cmap=cmap_colors,
        figsize=(30, 13),
        edgecolor="black",
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

    if content['antartida']:
        f, ax_tdf = plt.subplots(figsize=(2, 2))
        df_data_con_antartidad.plot(
            ax=ax_tdf,
            column=content['datos'],
            cmap=cmap_colors,
            figsize=(2, 2),
            edgecolor="grey",
            linewidth=0.4,
            scheme="userdefined",
            classification_kwds={'bins': [int(float(i))
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

        background.paste(foreground, (350, 823), foreground)
        
        arg_file = io.BytesIO()
        background.save(arg_file, format='PNG')

    data = base64.encodebytes(arg_file.getvalue())

    # freewilly
    del df_data
    del gdf_sin_antartida
    try:
        del gdf_con_antartida
        del df_data_con_antartidad
    except:
        pass

    return data


@app.route('/process-old', methods=['POST'])
def mapping_old():
    content = request.json

    # dataframes
    df = pd.DataFrame(content['data'])
    df['id'] = df[content['provincia']]
    file = 'data/provincias_sin_antartida.geojson'
    gdf = gpd.read_file(file)
    df = pd.merge(gdf, df, right_on='id', left_on='id')
    # df[content['datos']] = df[content['datos']].round(decimals=2)
    df[content['datos']] = df[content['datos']].astype(int)

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
    # ax.set_ylim([40.4, 47.2])
    # ax.set_xlim([7.0, 14.4])
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
    data = base64.encodebytes(aio.getvalue())

    # freewilly
    del df
    del gdf

    return data


@app.route('/help')
def help():
    return "Returns help"


@app.route('/test', methods=['POST'])
def mappingtest():
    return ''

if __name__ == '__main__':
    app.run()


