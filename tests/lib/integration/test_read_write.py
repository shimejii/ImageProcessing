import main
import sys
from pathlib import Path
import subprocess
import time
from my_exception import NotSupportedFileTypeError
import pytest


# コピー
## 正常
## type : windows bit map
## bpp : 32
## compression : 0
def test_read_and_write__case_normal_1():
    file_name_in = "./s_bmp/win-32.bmp"
    file_name_out = "./out_case_normal_1.bmp"
    path_file_input = Path(file_name_in)
    path_file_output = Path(file_name_out)

    file_header, info_header, color_palletes, img = main.read_win_bmp(path_file_input)
    main.write_win_bmp(path_file_output, file_header, info_header, color_palletes, img)
    res = subprocess.check_output("diff ./s_bmp/win-32.bmp ./out_case_normal_1.bmp", shell=True)
    assert res == b""

# コピー
## 異常1
## type : jpeg
## bpp : ?
## compression : ?
def test_read_and_write__case_abnormal_1():
    file_name_in = "./s_bmp/85873432_163x291.jpeg"
    file_name_out = "./out_case_abnormal_1.bmp"
    path_file_input = Path(file_name_in)
    path_file_output = Path(file_name_out)

    with pytest.raises(NotSupportedFileTypeError) as e:
        file_header, info_header, color_palletes, img = main.read_win_bmp(path_file_input)
    assert str(e.value)[:-11] == "This file is not Windows bitmap. This file magic number is "


# コピー
## 異常2
## type : os/2 Bitmap
## bpp : 24
## compression : 0?
def test_read_and_write__case_abnormal_2():
    file_name_in = "./s_bmp/os-24.bmp"
    file_name_out = "./out_case_abnormal_2.bmp"
    path_file_input = Path(file_name_in)
    path_file_output = Path(file_name_out)

    with pytest.raises(NotSupportedFileTypeError) as e:
        file_header, info_header, color_palletes, img = main.read_win_bmp(path_file_input)
    assert str(e.value) == "This file is OS/2 Bitmap. Not supported."

# コピー
## 異常3
## type : windows bitmap
## bpp : 24
## compression : 0?
def test_read_and_write__case_abnormal_3():
    file_name_in = "./s_bmp/win-24.bmp"
    file_name_out = "./out_case_abnormal_3.bmp"
    path_file_input = Path(file_name_in)
    path_file_output = Path(file_name_out)

    with pytest.raises(NotSupportedFileTypeError) as e:
        file_header, info_header, color_palletes, img = main.read_win_bmp(path_file_input)
    assert str(e.value) == "This file type is not supported.¥n bit_per_pixcel : 24."

# コピー
## 異常4
## type : windows bitmap
## bpp : 24
## compression : 1?

## sample画像なし

# コピー
## 異常5
## type : windows bitmap
## bpp : 32
## compression : 0
## sample画像なし
def test_read_and_write__case_abnormal_5():
    file_name_in = "./s_bmp/no_file_path.bmp"
    file_name_out = "./out_case_abnormal_5.bmp"
    path_file_input = Path(file_name_in)
    path_file_output = Path(file_name_out)

    with pytest.raises(FileNotFoundError) as e:
        file_header, info_header, color_palletes, img = main.read_win_bmp(path_file_input)
    assert str(e.value) == "[Errno 2] No such file or directory: 's_bmp/no_file_path.bmp'"

