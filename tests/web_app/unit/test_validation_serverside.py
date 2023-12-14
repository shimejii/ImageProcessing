from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

from app import app
import pytest
from pathlib import Path

# バリデーション サーバーサイド
## 正常
## type : windows bit map
## bpp : 32
## compression : 0
def test_validation_serverside_normal_case_1():
    app.config['TESTING'] = True
    client = app.test_client()


    file_name_in = "./s_bmp/win-32.bmp"
    path_file_input = Path(file_name_in)

    # post /upload
    with path_file_input.open('rb') as file:
        response = client.post('/upload', data={'file': (file, 'win-32.bmp')})
    assert b'Redirecting' in response.data

    # redirect and get
    response_after_redirect = client.get(response.headers['Location'], follow_redirects=True)
    # print(str(response_after_redirect.data))
    assert b'Upload Windows BMP file'
    assert b'process windows bitmap file' in response_after_redirect.data

# バリデーション サーバーサイド
## 異常
## type : windows bit map
## bpp : 32
## compression : 0
def test_validation_serverside_abnormal_case_1():
    app.config['TESTING'] = True
    client = app.test_client()

    file_name_in = "./s_bmp/win-32.bmp"
    path_file_input = Path(file_name_in)

    # post /upload
    with path_file_input.open('rb') as file:
        response = client.post('/upload', data={'other_name': (file, 'win-32.bmp')})
    assert b'Redirecting' in response.data

    # redirect and get
    response_after_redirect = client.get(response.headers['Location'], follow_redirects=True)
    # print(str(response_after_redirect.data))
    assert b'Upload Windows BMP file'
    assert b'No file part' in response_after_redirect.data

# バリデーション サーバーサイド
## 異常
## type : no selected
## bpp : ?
## compression : ?
# def test_validation_serverside_abnormal_case_2():
#     app.config['TESTING'] = True
#     client = app.test_client()

#     file_name_in = "./クリスマス.png"
#     path_file_input = Path(file_name_in)

#     # post /upload
#     response = client.post('/upload', data={'file': ""})
#     assert b'Redirecting' in response.data

#     # redirect and get
#     response_after_redirect = client.get(response.headers['Location'], follow_redirects=True)
#     # print(str(response_after_redirect.data))
#     assert b'Upload Windows BMP file'
#     assert b'No selected file' in response_after_redirect.data


# バリデーション サーバーサイド
## 異常
## type : png
## bpp : ?
## compression : ?
def test_validation_serverside_abnormal_case_3():
    app.config['TESTING'] = True
    client = app.test_client()

    file_name_in = "./クリスマス.png"
    path_file_input = Path(file_name_in)

    # post /upload
    with path_file_input.open('rb') as file:
        response = client.post('/upload', data={'file': (file, 'クリスマス.png')})
    assert b'Redirecting' in response.data

    # redirect and get
    response_after_redirect = client.get(response.headers['Location'], follow_redirects=True)
    # print(str(response_after_redirect.data))
    assert b'Upload Windows BMP file'
    assert b'Not suport this file format' in response_after_redirect.data


# バリデーション サーバーサイド
## 異常
## type : os/2 Bitmap
## bpp : 24
## compression : 0?
def test_validation_serverside_abnormal_case_4():
    app.config['TESTING'] = True
    client = app.test_client()

    file_name_in = "./s_bmp/os-24.bmp"
    path_file_input = Path(file_name_in)

    # post /upload
    with path_file_input.open('rb') as file:
        response = client.post('/upload', data={'file': (file, 'os-24.bmp')})
    assert b'Redirecting' in response.data

    # redirect and get
    response_after_redirect = client.get(response.headers['Location'], follow_redirects=True)
    # print(str(response_after_redirect.data))
    assert b'Upload Windows BMP file'
    assert b'This file is OS/2 Bitmap. Not supported.' in response_after_redirect.data