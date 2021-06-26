from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_from_directory
from jinja2 import Environment, PackageLoader, select_autoescape
import jinja2
import os

import main_template
import maze
import overworld

app = Flask(__name__, static_url_path='/static')

# Jinja2 templates
env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

@app.route('/')
def main_page():
    t = env.get_template("index.html")
    form_data = main_template.generate_template()
    return t.render(systemname="Project Epsilon",formdata=form_data)

@app.route('/mapgen', methods=['POST'])
def mapgen():
    req_data = request.get_json()
    #return overworld.build_map(req_data, app)
    return maze.build_maze3D(req_data, app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')