from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

from app import app
import pytest
from pathlib import Path

# set-cookie heaer の受け取り
## 正常
## type : windows bit map
## bpp : 32
## compression : 0
def test_issue_set_cookie_header_normal_case_1():
    app.config['TESTING'] = True
    client = app.test_client()


    file_name_in = "./s_bmp/win-32.bmp"
    path_file_input = Path(file_name_in)

    # post /upload
    with path_file_input.open('rb') as file:
        response = client.post('/upload', data={'file': (file, 'win-32.bmp')})
    assert b'Redirecting' in response.data
    assert 'Set-Cookie' in response.headers
    # print(response.headers)
    # print(type(response.headers))

# set-cookie heaer の受け取り
## 正常
## type : os/2 bitmap
## bpp : 32
## compression : 0
def test_issue_set_cookie_header_abnormal_case_1():
    app.config['TESTING'] = True
    client = app.test_client()


    file_name_in = "./s_bmp/os-24.bmp"
    path_file_input = Path(file_name_in)

    # post /upload
    with path_file_input.open('rb') as file:
        response = client.post('/upload', data={'file': (file, 'os-24.bmp')})
    assert b'Redirecting' in response.data
    assert 'Set-Cookie' in response.headers

