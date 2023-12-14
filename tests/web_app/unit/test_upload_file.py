from pathlib import Path
import subprocess
import difflib

# SAVE_DIR = '/tmp/'
SAVE_DIR = './static/'


# 画像データ保存
## 正常
## type : windows bit map
## bpp : 32
## compression : 0
def test_save_upload_file__case_normal_1():
    # rm *.bmp
    cmd0 = f'rm {SAVE_DIR}*.bmp'
    ls_ret0 = subprocess.run(cmd0, capture_output=True, text=True, shell=True)
    # print(ls_ret0.stdout)

    # ls
    cmd1 = ['ls', '-1', SAVE_DIR]
    ls_ret1 = subprocess.run(cmd1, capture_output=True, text=True)

    # file upload
    file_name_in = "./s_bmp/win-32.bmp"
    file_path_in = Path(file_name_in).resolve()
    url = 'http://127.0.0.1:5000/'

    cmd2 = ['curl', '-X', 'POST', '-F', f'file=@{file_path_in}', url]
    ret = subprocess.run(cmd2)
    # print(ret.returncode)
    assert ret.returncode == 0

    # ls
    cmd3 = ['ls', '-1', SAVE_DIR]
    ls_ret3 = subprocess.run(cmd3, capture_output=True, text=True)

    # get file name
    differ = difflib.Differ()
    result = differ.compare((ls_ret1.stdout).splitlines(), (ls_ret3.stdout).splitlines())

    filename_saved = ""
    for line in result:     
        if line[0] == '+' and line[-3:] == "bmp":
            filename_saved = line[2:]
            break
    assert filename_saved !=  ""
    
    cmd4 = ['diff', str(file_path_in), SAVE_DIR + str(filename_saved)]
    ret = subprocess.run(cmd4)
    assert ret.returncode == 0

# 画像データ保存
## 異常
## type : png
## bpp : ?
## compression : ?
def test_save_upload_file__case_abnormal_1():
    # rm *.png
    cmd0 = f'rm {SAVE_DIR}*.png'
    ls_ret0 = subprocess.run(cmd0, capture_output=True, text=True, shell=True)
    # print(ls_ret0.stdout)

    # ls
    # cmd1 = ['ls', '-1', SAVE_DIR]
    cmd1 = f"ls {SAVE_DIR} | grep png"
    ls_ret1 = subprocess.run(cmd1, capture_output=True, text=True, shell=True)
    assert ls_ret1.stdout == ""

    # file upload
    file_name_in = "./クリスマス.png"
    file_path_in = Path(file_name_in).resolve()
    url = 'http://127.0.0.1:5000/'

    cmd2 = ['curl', '-X', 'POST', '-F', f'file=@{file_path_in}', url]
    ret = subprocess.run(cmd2)
    assert ret.returncode == 0

    # ls
    cmd3 = f"ls {SAVE_DIR} | grep png"
    ls_ret3 = subprocess.run(cmd3, capture_output=True, text=True, shell=True)
    assert ls_ret3.stdout == ""

