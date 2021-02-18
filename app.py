
from flask import Flask, render_template, request, Response, send_file


import matplotlib
import io
import base64
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as pltcolors
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
    # get content
    content = request.json
    # make dataframes
    df = pd.DataFrame(content['data'])
    file = 'data/provincias.json'
    gdf = gpd.read_file(file)
    df = pd.merge(gdf, df, right_on='id', left_on=content['provincia'])

    
    # settings
    cmap_colors = pltcolors.LinearSegmentedColormap.from_list(
        "", content['colors'])
    
    # # plot bebings
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)

    # # plot plots
    # df.plot(
    #     column=content['datos'],
    #     ax=ax,
    #     cmap=cmap_colors,
    # )

    # fig = plt.figure()
    ax = df.plot(
        column=content['datos'],
        cmap=cmap_colors,
        edgecolor="grey",
        linewidth=1,
        legend=True,
        classification_kwds={'bins': content['classification']}
        )
    # leg = ax.get_legend()
    # leg.set_bbox_to_anchor((0.8, 0.05, 0.2, 0.2))
    plt.title(content['title'])


    aio = io.BytesIO()
    plt.savefig(aio, format='png')
    data = base64.encodestring(aio.getvalue())


    return data

@app.route('/help')
def help():
    return "Returns help"


if __name__ == '__main__':
    app.run()


