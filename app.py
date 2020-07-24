from flask import Flask, render_template, redirect, abort, request, jsonify
from utils import dl_picture, get_picture, valid, STORAGE, parse_caption, random_shota, latest_shota
from json import load, dumps
from os import path
from werkzeug.utils import secure_filename
from credentials import UPLOAD_TOKEN, ROOT_URL

app = Flask(__name__)
UPLOAD_FOLDER = 'img/shota'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
data_dir = 'data/'


@app.errorhandler(500)
def internal(e):
    return render_template('50x.html', e=e)


@app.errorhandler(404)
@app.errorhandler(405)
def not_found(_):
    return render_template('40x.html')


@app.route('/')
def home():
    return redirect(ROOT_URL + '/shota/random/', code=302)


@app.route('/api/gallery/', defaults={'count': 9})
@app.route('/api/gallery/<count>')
def api_gallery(count=9):
    return jsonify(pics=random_shota(int(count)))


@app.route('/api/random/')
def api_get_one():
    return random_shota(1)[0]


@app.route('/gallery/', defaults={'count': 9})
@app.route('/gallery/<count>')
def gallery(count=9):
    return render_template('gallery.html', pics=random_shota(int(count)))


@app.route('/random/')
def get_one():
    pic = random_shota(1)[0]
    return render_template('pic.html', pic=pic)


@app.route('/latest/', defaults={'count': 9})
@app.route('/latest/<count>')
def latest(count=9):
    pics = latest_shota(int(count))
    return render_template('gallery.html', pics=pics)


@app.route('/id/<id>/')
def show_by_id(id):
    meta_file = '{}{}.json'.format(data_dir, id)
    if path.isfile(meta_file):
        pic = load(open(meta_file, 'r'))
        return render_template('pic.html', pic=pic)
    else:
        abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.form.get('token') != UPLOAD_TOKEN:
        return 'Auth failed.'
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files.get('file')
    caption = request.form.get('caption')
    pic = dict()
    if caption:
        pic = parse_caption(caption)
    else:
        return 'FAILED'
    filename = request.form.get('filename')
    pic['id'] = filename.split('.')[0]
    with open('data/{}.json'.format(pic['id']), 'w') as f:
        f.write(dumps(pic, ensure_ascii=False))
        f.close()
    if file and allowed_file(filename):
        filename = secure_filename(filename)
        file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'OK'
