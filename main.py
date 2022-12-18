# Color Pattern Website
import numpy as np
import extcolors
from colormap import rgb2hex
from PIL import Image
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
# import os
import base64
from io import BytesIO

allowed_file_types = {'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'}


def check_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_file_types


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret_key'
# app.config['UPLOAD_FOLDER'] = 'static/files'
Bootstrap(app)


# class UploadFileForm(FlaskForm):
#     file = FileField("File")
#     submit = SubmitField("Upload File")

# Color extracting function
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
        percent = ((round(int(occurence) * 100 / result)))
        color = {'c_code': c_code, 'percent': percent}
        colors.append(color)
    return colors


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET,POST'])
def home():
    # For demo vision
    image_file = 'try2.png'
    colors_x = extcolors.extract_from_path(image_file, tolerance=11, limit=11)
    colors = color_to_pallet(colors_x)
    img = Image.open(image_file).convert('RGB')
    img = img.resize((300, 300))
    with BytesIO() as buf:
        img.save(buf, 'jpeg')
        image_bytes = buf.getvalue()
    encoded_string = base64.b64encode(image_bytes).decode()
    # Getting uploaded file
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file attached in request')
            return redirect(url_for('home'))
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('home'))
        if file and check_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img = Image.open(file.stream).convert('RGB')
            img = img.resize((300, 300))
            # Working with stream
            with BytesIO() as buf:
                img.save(buf, 'jpeg')
                image_bytes = buf.getvalue()
            encoded_string = base64.b64encode(image_bytes).decode()
            # file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename))
            # We don't need to save for this project.

            # Extracting colors
            colors_x = extcolors.extract_from_path(file, tolerance=11, limit=11)
            colors = color_to_pallet(colors_x)

        return render_template('index.html', img_data=encoded_string, colors=colors)
    return render_template("index.html", img_data=encoded_string, colors=colors)

# For displaying images
@app.route('/display/<filename>')
def display_image(filename=""):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
