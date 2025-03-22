from flask import Blueprint, render_template, request, redirect, url_for, flash
import yaml
import os

main = Blueprint('main', __name__)

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'src', 'static', 'downloads')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'resources.yaml')
ALLOWED_EXTENSIONS = {'pdf', 'ps1', 'json', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load resources from YAML
def load_resources():
    with open(DATA_PATH, "r") as stream:
        resources_yaml = yaml.safe_load(stream)
    return resources_yaml.get("resources", [])

# Home route
@main.route('/')
def index():
    return render_template('index.html')

# Downloads page
@main.route('/downloads')
def downloads():
    query = request.args.get('query', '').lower()
    filter_type = request.args.get('filter', '').lower()
    resources = load_resources()

    # Apply type filter
    if filter_type:
        resources = [r for r in resources if r['type'].lower() == filter_type]

    # Apply keyword search
    if query:
        resources = [r for r in resources if query in r['name'].lower() or query in r['type'].lower()]

    return render_template('downloads.html', resources=resources, query=query)

# Submit resource form
@main.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        resource_name = request.form['name']
        category = request.form['category']
        file = request.files['file']

        if file and allowed_file(file.filename):
            save_path = os.path.join(UPLOAD_FOLDER, category)
            os.makedirs(save_path, exist_ok=True)
            file_path = os.path.join(save_path, file.filename)
            file.save(file_path)

            # Optional YAML update step
            update_yaml(resource_name, file.filename, category)

            flash('✅ Resource submitted successfully!', 'success')
            return redirect(url_for('main.submit'))

        flash('⚠️ Invalid file type!', 'error')

    return render_template('submit.html')

# Update YAML file dynamically
def update_yaml(name, file, category):
    with open(DATA_PATH, "r") as stream:
        data = yaml.safe_load(stream)
    if not data:
        data = {'resources': []}
    data['resources'].append({
        'name': name,
        'file': file,
        'type': category.upper()
    })
    with open(DATA_PATH, "w") as stream:
        yaml.dump(data, stream)

