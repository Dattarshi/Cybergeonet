from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import yaml

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/downloads/')
ALLOWED_EXTENSIONS = {'pdf', 'ps1', 'json', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

            # Optional: Update resources.yaml (for auto-display)
            update_yaml(resource_name, file.filename, category)

            flash('✅ Resource submitted successfully!', 'success')
            return redirect(url_for('main.submit'))

        flash('⚠️ Invalid file type!', 'error')

    return render_template('submit.html')
