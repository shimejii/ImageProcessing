from flask import Flask
from flask import flash
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from my_exception import NotSupportedFileTypeError
from werkzeug.utils import secure_filename
import os
import main
import sys
from pathlib import Path

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {'bmp', 'rle', 'dib'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'hogehoge'

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
            flash("successfully uploaded")
            return redirect(request.url)
        # return redirect('/process')
    return render_template('upload.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    global HISTGRAMS_DICT
    global HISTGRAMS
    if request.method == 'POST' and request.form.get('process') == 'binarize':
        # binarization
        cmd = request.form.get('process')
        method = request.form.get('binarize-method')
        apply_dim = int(request.form.get('apply_dim'))
        print(f'cmd : {cmd}¥nmethod : {method}¥n, apply_dim : {apply_dim}¥n', sys.stdout)
        main.process(IMG, BIT_PER_PIXCEL, HEIGHT, WIDTH, cmd, method, apply_dim)
        main.write_win_bmp(FILE_PATH, FILE_HEADER, INFO_HEADER, COLOR_PALLETES, IMG)
        HISTGRAMS_DICT = main.generate_histgram(IMG, BIT_PER_PIXCEL, HEIGHT, WIDTH, False)
        HISTGRAMS = main.defaultDictHistgrams2List(HISTGRAMS_DICT, BIT_PER_PIXCEL)
    return render_template('process.html', filepath=FILE_PATH[1:], histgrams=HISTGRAMS)

if __name__ == '__main__':
    app.run()

