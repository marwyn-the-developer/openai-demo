from application import app
from flask import render_template, request, flash, redirect
import os
import openai
from PIL import Image
from io import BytesIO

ALLOWED_EXTENSIONS = set(['png'])

API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = API_KEY


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files["image"]
        if file and allowed_file(file.filename):
            image = Image.open(file)
            image = make_square(image)
            image_bytes_io = BytesIO()
            image.save(image_bytes_io, "PNG")
            image_bytes = image_bytes_io.getvalue()
            api_response = openai.Image.create_variation(
                image=image_bytes,
                n=1,
                size="1024x1024",
            )

            return api_response
    return render_template("index.html")



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im