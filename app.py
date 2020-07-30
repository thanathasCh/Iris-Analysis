from flask import Flask, request, render_template, url_for
import numpy as np
import cv2
from urllib.request import urlopen

from python_code import backend

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/processImage", methods=["POST"])
def processImage():
    '''
        'image': 'a',
        'limitedWidth': limitedWidth,
        'currentX': currentX,
        'currentY': currentY,
        'currentWidth': currentWidth,
        'currentHeight': currentHeight
    '''

    img = cv2.imdecode(np.fromstring(urlopen(request.form['userImagePath']).file.read(), np.uint8), 1)
    limitWidth = int(request.form['limitedWidth'])
    currentX = int(request.form['currentX'])
    currentY = int(request.form['currentY'])
    currentWidth = int(request.form['currentWidth'])
    currentHeight = int(request.form['currentHeight'])

    backend.start(img, limitWidth, currentX, currentY, currentHeight, currentWidth)
    
    return 'done'


if __name__ == "__main__":
    app.run(debug=True)
