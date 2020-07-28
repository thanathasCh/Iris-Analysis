from flask import Flask, request, render_template, url_for
import os
import numpy as np
import cv2
from copy import deepcopy

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/processImage", methods=["POST"])
def processImage():
    return "In progress"


if __name__ == "__main__":
    app.run(debug=True)
