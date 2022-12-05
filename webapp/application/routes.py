from application import app
from flask import render_template, request, json, flash, redirect, send_file
from werkzeug.utils import secure_filename
import requests
import json
from dotenv import dotenv_values
import os
import openai
import base64

config = dotenv_values(".env")

API_KEY = config['OPENAI_API_KEY']

UPLOAD_FOLDER_ORIGINAL = 'images/originals'
UPLOAD_FOLDER_VARIATION = 'images/variations'
ALLOWED_EXTENSIONS = set(['png'])

openai.api_key = API_KEY


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        image = request.files["image"]

        if image and allowed_file(image.filename):
            original_image_save_path = os.path.join(UPLOAD_FOLDER_ORIGINAL,
                       secure_filename(image.filename))
    
            image.save(original_image_save_path)

            api_response = openai.Image.create_variation(
                image=open(original_image_save_path),
                n=1,
                size="1024x1024"
            )
            decoded_img = base64.b64decode(api_response)
            variation_image_save_path = os.path.join(UPLOAD_FOLDER_VARIATION,
                       secure_filename(image.filename))
            variation_img = open(variation_image_save_path, "wb")
            variation_img.write(decoded_img)
            variation_img.close()
            return send_file(variation_image_save_path, mimetype='image/png')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
