from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import maze

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/mapgen', methods=['POST'])
def mapgen():
    return maze.build_maze()
