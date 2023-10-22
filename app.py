from flask import Flask
# from flask import request
# from flask import render_template
# import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello world</p>"

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     html = '''<!DOCTYPE html>
# <html lang="ja">
#     <head>
#         <title>Windows BMP File Processing</title>
#         <meta charset="utf-8">
#     </head>
#     <body>
#         <h1>Windows BMP File Processing</h1>
#         <form method="POST" enctype="multipart/form-data">
#             <input type="file" name="file">
#             <input type="submit" value="アップロード">
#         </form>
#         <h2>processing button<h2>
#         <ul>
#             <li><button>binarize</button></li>
#         </ul>
#         <p><button>download BMP File</p>
#     </body>
# </hmtl>'''
    # if request.method == 'POST':
    #     file_posted = request.files['file']
    #     file_posted.save(os.path.join('./img/', file_posted.filename))
    #     return f"{file_posted.filename}がアップロードされました。"
    #     # return "upload sucessfully"
    # else:
    #     return render_template('index.html')

if __name__ == '__main__':
    app.run()

