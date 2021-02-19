
from flask import Flask, render_template, request, Response, send_file


import matplotlib
import io
import base64
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as pltcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
matplotlib.use('Agg')


app = Flask(__name__)

html = '''
<html>
    <body>
        <img src="data:image/png;base64,{}" />
    </body>
</html>
'''

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def mapping():
    content = request.json

    # dataframes
    df = pd.DataFrame(content['data'])
    file = 'data/provincias-noantartida.json'
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
                 linewidth=1,
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
            by=content['datos'], ascending=False).head(25)
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


