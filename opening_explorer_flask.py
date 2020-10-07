import json
from flask import Flask
from flask import render_template

import opening_explorer
import webbrowser
import time


app = Flask(__name__)


@app.route('/chessboard')
def chessboard():
    return render_template("html/opening_explorer.html")


# Have to load in flask to get local url_for images
@app.route('/chessboard_js')
def chessboard_js():
    return render_template("js/chessboard-1.0.0.min.js")


@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):  # Is called whenever javascript sends data
    opening_explorer.opening_explorer(jsdata)
    return jsdata


pythondata = None
@app.route('/getpythondata')  # Is called whenever javascript makes a request for the pythondata
def get_python_data():
    return json.dumps(pythondata)

time.sleep(1)
webbrowser.open('http://127.0.0.1:5000/chessboard', new=2)

