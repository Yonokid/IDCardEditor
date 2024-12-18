from flask import render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from app import app
from reader import *
import hashlib
import shutil
import vercel_blob
from dotenv import load_dotenv

ALLOWED_EXTENSIONS = {'bin', 'crd'}

dotenv.load_dotenv()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_file(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

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
            file_content = file.read()
            hashed_filename = hashlib.sha256(file_content).hexdigest() + '.bin'
            card_path = os.path.join('app\\card', hashed_filename)
            vercel_blob.put(card_path, file.read(), {})
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
