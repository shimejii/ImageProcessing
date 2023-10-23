from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import os

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

@app.route('/process')
def process():
    return render_template('process.html', filepath=FILE_PATH)

if __name__ == '__main__':
    app.run()

