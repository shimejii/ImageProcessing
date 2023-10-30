from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import os
import main
import sys

FILE_PATH = ""
FILE_HEADER = None
INFO_HEADER = None
COLOR_PALLETES = None
IMG = None
BIT_PER_PIXCEL = None
HEIGHT = None
WIDTH = None
HISTGRAMS_DICT = None
HISTGRAMS = None

app = Flask(__name__, static_folder='/tmp/')

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def home():
    global FILE_PATH 
    global FILE_HEADER
    global INFO_HEADER
    global COLOR_PALLETES
    global BIT_PER_PIXCEL
    global HEIGHT
    global WIDTH

    if request.method == 'POST':
        # save img
        file_posted = request.files['file']
        FILE_PATH = os.path.join('/tmp/', file_posted.filename)
        file_posted.save(FILE_PATH)

        # load img
        FILE_HEADER, INFO_HEADER, COLOR_PALLETES, IMG = main.read_win_bmp(FILE_PATH)
        BIT_PER_PIXCEL = int.from_bytes(INFO_HEADER.bcBitCount, main.BYTE_ORDER)
        HEIGHT = int.from_bytes(INFO_HEADER.bcHeight, main.BYTE_ORDER)
        WIDTH = int.from_bytes(INFO_HEADER.bcWidth, main.BYTE_ORDER)

        # hisrgram
        HISTGRAMS_DICT = main.generate_histgram(IMG, BIT_PER_PIXCEL, HEIGHT, WIDTH, False)
        HISTGRAMS = main.defaultDictHistgrams2List(HISTGRAMS_DICT, BIT_PER_PIXCEL)
        return render_template('process.html', filepath=FILE_PATH[1:], histgrams=HISTGRAMS)
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

