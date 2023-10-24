from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import os
import main
import sys

FILE_PATH = ""

app = Flask(__name__, static_folder='/tmp/')

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def home():
    global FILE_PATH 
    if request.method == 'POST':
        file_posted = request.files['file']
        FILE_PATH = os.path.join('/tmp/', file_posted.filename)
        file_posted.save(FILE_PATH)
        return redirect('/process')
    return render_template('upload.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST' and request.form.get('process') == 'binarize':
        # binarization
        file_header, info_header, color_palletes, img = main.read_win_bmp(FILE_PATH)
        bit_per_pixcel = int.from_bytes(info_header.bcBitCount, main.BYTE_ORDER)
        height = int.from_bytes(info_header.bcHeight, main.BYTE_ORDER)
        width = int.from_bytes(info_header.bcWidth, main.BYTE_ORDER)
        cmd = request.form.get('process')
        method = request.form.get('binarize-method')
        apply_dim = int(request.form.get('apply_dim'))
        print(f'cmd : {cmd}¥nmethod : {method}¥n, apply_dim : {apply_dim}¥n', sys.stdout)
        main.process(img, bit_per_pixcel, height, width, cmd, method, apply_dim)
        main.write_win_bmp(FILE_PATH, file_header, info_header, color_palletes, img)
    return render_template('process.html', filepath=FILE_PATH[1:])

if __name__ == '__main__':
    app.run()

