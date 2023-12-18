from flask import Flask
from flask import flash
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for
from flask_session import Session
from my_exception import NotSupportedFileTypeError
from pathlib import Path
from typing import Dict
from typing import List
from werkzeug.utils import secure_filename
import os
import main
import sys

# UPLOAD_FOLDER = '/tmp/'
UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = {'bmp', 'rle', 'dib'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# flask automatically set .env variables if python-dotenv is installed
# In the development environment, secret_key is already exported.
app.secret_key = os.environ.get('SECRET_KEY', '')
if app.secret_key == '':
    raise ValueError('secret_key is not loaded')

SESSION_TYPE='filesystem'
app.config.from_object(__name__)
Session(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_posted = request.files['file']

        if file_posted.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if not allowed_file(file_posted.filename):
            flash('Not suport this file format')
            return redirect(request.url)
        
        if file_posted and allowed_file(file_posted.filename):
            # save img
            filename = secure_filename(file_posted.filename)
            filepath = Path(app.config['UPLOAD_FOLDER'] + filename)
            file_posted.save(filepath)
            # return redirect(url_for('process', name=filename))

            # load img
            ## excluding unsupported bmp files.
            ## not discernible from the extension.
            try:
                _, _, _, _ = main.read_win_bmp(filepath)
            except NotSupportedFileTypeError as e:
                flash(str(e))
                return redirect(request.url)
            session['file_path'] = str(filepath)
            return redirect(url_for('process'))
        # return redirect('/process')
    return render_template('upload.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    filepath = str(session.get('file_path', ''))
    try:
        file_header, info_header, color_palletes, img = main.read_win_bmp(Path(filepath))
    except (NotSupportedFileTypeError, OSError) as e:
        flash(str(e))
        redirect(url_for('upload'))
    bit_per_pixcel = int.from_bytes(info_header.bcBitCount, main.BYTE_ORDER)
    height = int.from_bytes(info_header.bcHeight, main.BYTE_ORDER)
    width = int.from_bytes(info_header.bcWidth, main.BYTE_ORDER)

    # image process
    if request.method == 'POST':
        cmd = request.form.get('process')
        if request.form.get('process') == 'binarize':
        ## binarization
            method = request.form.get('binarize-method')
            apply_dim = int(request.form.get('apply_dim'))
            print(f'cmd : {cmd}¥nmethod : {method}¥n, apply_dim : {apply_dim}¥n', sys.stdout)
            main.process(img, bit_per_pixcel, height, width, cmd, method, apply_dim)
            main.write_win_bmp(Path(filepath), file_header, info_header, color_palletes, img)

    histgram_d: Dict = main.generate_histgram(img, bit_per_pixcel, height, width, False)
    histgram_l: List = main.defaultDictHistgrams2List(histgram_d, bit_per_pixcel)
    return render_template('process.html', filepath=filepath, histgrams=histgram_l)


if __name__ == '__main__':
    app.run()

