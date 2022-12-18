# Color Pattern Website
import numpy as np
import extcolors
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from colormap import rgb2hex
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

# app = Flask(__name__)
# Bootstrap(app)

colors_x = extcolors.extract_from_path('img.png', tolerance=11, limit=11)


def color_to_pallet(pallet):
    colors_list = str(pallet).replace('([(', '').split(', (')[0:-1]
    df_rgb = [color.split('), ')[0] + ')' for color in colors_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colors_list]

    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]



    colors = []


    for c_code, occurence in zip(df_color_up, df_percent):
        result = sum(int(x) for x in df_percent)
        percent=((round(int(occurence)*100/result)))
        color = {'c_code': c_code, 'percent': percent}
        colors.append(color)
        print(color["percent"])
    return colors
print(color_to_pallet(colors_x))
# @app.route('/')
# def home():
#     colors = color_to_pallet(colors_x)
#     for color in colors:
#         print(color["c_code"])
#     return render_template("index.html", colors=colors)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
