from flask import render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from app import app
from reader import *
import hashlib
import shutil

ALLOWED_EXTENSIONS = {'bin', 'crd'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_file(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            data = f.read()
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not file.filename:
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists('temp'):
                os.makedirs('temp')
            temp_path = os.path.join('temp', filename)
            file.save(temp_path)
            hashed_filename = hash_file(temp_path) + '.bin'
            card_path = os.path.join('app\\card', hashed_filename)
            shutil.copy(temp_path, card_path)
            os.remove(temp_path)
            return redirect(url_for('edit_file', name=hashed_filename))
    return render_template('index.html')

@app.route('/card/<name>')
def edit_file(name):
    card = read_card(f'app\\card\\{name}')
    return render_template('card.html', title='Home', card=card, name=name)

@app.route('/download/<name>', methods=["GET", "POST"])
def download(name):
    if request.method == "POST":
        card = read_card(f'app\\card\\{name}')
        for key in card:
            form_value = request.form.get(f"key_{key}")
            if form_value is not None:
                card[key][0] = form_value
        write_card(f'app\\card\\{name}', card)
    path = os.path.join('card', name)
    response = send_file(path, as_attachment=True, download_name='SBZZ_card.bin')
    return response
