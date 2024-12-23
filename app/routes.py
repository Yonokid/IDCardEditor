from flask import render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from app import app
from reader import *
import hashlib
import ast
import psycopg2
from dotenv import load_dotenv
from io import BytesIO

ALLOWED_EXTENSIONS = {'bin', 'crd'}
app.config['SECRET_KEY'] = 'super cool secret key'
app.jinja_env.globals.update(len=len)
app.jinja_env.globals.update(str=str)
byte_data = dict()

load_dotenv()

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
            header = b'\x03\x36\x00\x01\x81\x41\x54\x06\xF7\x04\x16\x09\x03\x89\x03\x87'
            if file_content[:16] != header:
                return redirect(request.url)
            hashed_filename = hashlib.sha256(file_content).hexdigest() + '.bin'
            byte_data[hashed_filename] = file_content
            return redirect(url_for('edit_file', name=hashed_filename))
    return render_template('index.html')

@app.route('/card/<name>')
def edit_file(name):
    card = read_card(BytesIO(byte_data[name]))
    static_data = []
    static_data.append(read_txt('app/static/prefectures.txt'))
    static_data.append(read_txt('app/static/avatar_gender.txt'))
    static_data.append(read_txt('app/static/bgm_volume.txt'))
    static_data.append(read_txt('app/static/make.txt'))
    static_data.append(read_txt('app/static/car_prefectures.txt'))
    static_data.append(read_txt('app/static/car_hirigana.txt'))
    static_data.append(read_txt('app/static/courses.txt'))
    static_data.append(read_txt('app/static/cup.txt'))
    static_data.append(read_txt('app/static/tachometer.txt'))
    static_data.append(read_txt('app/static/aura.txt'))
    static_data.append(read_txt('app/static/class.txt'))
    static_data.append(read_txt('app/static/titles.txt'))
    return render_template('card.html', title='Home', card=card, name=name, data=static_data)

@app.route('/download/<name>', methods=["GET", "POST"])
def download(name):
    card = read_card(BytesIO(byte_data[name]))
    for key in card:
        form_value = request.form.get(f"key_{key}")
        if form_value is not None:
            card[key][0] = form_value
    new_data = BytesIO(byte_data[name])
    user_id = card["User ID"][0]
    times = card["Courses"][0]
    username = card["Driver Name"][0]
    if card["Upload Scores"][0]:
        new_user_id = upload_times(user_id, username, times)
    else:
        new_user_id = user_id
    write_card(new_data, card, new_user_id)
    new_data.seek(0)
    response = send_file(new_data, as_attachment=True, download_name='SBZZ_card.bin')
    return response

@app.route('/leaderboard')
def view_leaderboard():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    cursor.execute('SELECT username, times FROM leaderboard')
    leaderboard = dict()
    all_data = cursor.fetchall()
    for username, times in all_data:
        times_dict = ast.literal_eval(times)
        for course in times_dict:
            if course not in leaderboard:
                leaderboard[course] = []
            current_time = time_to_ms(times_dict[course]['Time'])
            if current_time == 0:
                continue
            if len(leaderboard[course]) < 10:
                leaderboard[course].append({'Username': username, 'Time': current_time,
                                            'Car Make': times_dict[course]['Car Make'],
                                            'Car Model': times_dict[course]['Car Model']})
            else:
                leaderboard[course].sort(key=lambda x: x['Time'])
                if current_time < leaderboard[course][-1]['Time']:
                    leaderboard[course][-1] = {'Username': username, 'Time': current_time,
                                                'Car Make': times_dict[course]['Car Make'],
                                                'Car Model': times_dict[course]['Car Model']}
            leaderboard[course].sort(key=lambda x: x['Time'])
            leaderboard[course] = leaderboard[course][:10]
    for course in leaderboard:
        for i in range(len(leaderboard[course])):
            leaderboard[course][i]["Time"] = ms_to_time(leaderboard[course][i]["Time"])
    conn.close()
    return render_template('leaderboard.html', title='Leaderboard', leaderboard=leaderboard)
