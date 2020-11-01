from flask import Flask, render_template, request, jsonify
import TestScript
import os
import werkzeug
import cv2
import io
import base64
import time
from PIL import Image

path = "C:/Classnotes/Dress-Virtual-Trialroom/static/"
fn = []
app = Flask(__name__)


def get_response_image(image_path):
    with open(image_path,"rb") as file:
        content = file.read()
    return content


def model_run():
    frontloc = path + fn[0]
    bentloc = path + fn[1]
    backloc = path + fn[2]
    shirtloc = path + fn[3]
    TestScript.start(frontloc, bentloc, backloc, shirtloc)
    encoded = get_response_image(path+"out.jpg")
    return encoded


def deleting_files():
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))


@app.route("/api/android",methods=['GET', 'POST'])
def api_call():
    incoming_files = list(request.files)
    print("Files recieved :",len(incoming_files))
    os.chdir(path)
    it = 1
    for file in incoming_files:
        image = request.files[file]
        filename = werkzeug.utils.secure_filename(image.filename)
        print(filename)
        print()
        abc = filename.split(".")
        fn.append(str(it) + "." + abc[-1])
        image.save(fn[it-1])
        print("File saved ",it)
        it = it + 1
    cypher = model_run()
    deleting_files()
    return cypher


@app.route("/", methods=['GET', 'POST'])
def home():
    return "HEllo World"


if __name__ == "__main__":
    app.run(host= '0.0.0.0')
