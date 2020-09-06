from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_from_directory
import os

import maze

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/mapgen', methods=['POST'])
def mapgen():
    req_data = request.get_json()

    return maze.build_maze(req_data, app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')