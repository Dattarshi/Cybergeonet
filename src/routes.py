from flask import Blueprint, render_template, request
import yaml
import os

main = Blueprint('main', __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
data_path = os.path.join(BASE_DIR, "data", "resources.yaml")

def load_resources():
    with open(data_path, "r") as stream:
        resources_yaml = yaml.safe_load(stream)
    return resources_yaml["resources"]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/downloads')
def downloads():
    query = request.args.get('query', '').lower()
    resources = load_resources()

    # Filter based on search query
    if query:
        resources = [r for r in resources if query in r['name'].lower() or query in r['type'].lower()]

    return render_template('downloads.html', resources=resources, query=query)
