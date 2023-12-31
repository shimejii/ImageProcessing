# About This Repository
This repository is used to manage the programs created in the Image Information Processing Theory lectures.
The lectures cover windows bmp files.

## Supported File Formats
| format | bitPerPixcel | compression | support or not |
| :---: | :---: | :---: | :---: |
| windows bitmap | 32 | 0 | o |
| windows bitmap | other | other | x |
| os/2 bitmap | other | other | x |
| other | other | other | x |



## Features
Supported features are as follows:
- Binarization
    - Otsu's method

## Usage
The execution method is as follows:

1. CLI

    ```
    git clone https://github.com/shimejii/ImageProcessing.git
    cd ImageProcessing
    PWD1=`pwd`
    python -m venv my_env
    pip install -r requirements.txt
    cd ./common/libs
    PWD2=`pwd`
    export PYTHONPATH=${PWD2}:${PWD1}:${PYTHONPATH}
    python main.py INPUT_FILE OUTPUT_FILE [CMD METHOD APPLY_DIM] 
    ```

2. Web browser

    please access [this web application](https://imgprocess-6f80676dca86.herokuapp.com/)


### about CMD
- binarize

    Performs binarization on the APPLY_DIM dimension of the imput file. The threshold is calculated according to METHOD.

#### about METHOD
- Otsu

    use Otsu's method

## bmp file sample
Please refer to the following site for [sample bmp files](https://www.setsuki.com/hsp/ext/s_bmp.zip)