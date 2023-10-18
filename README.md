# About This Repository
This repository is used to manage the programs created in the Image Information Processing Theory lectures.
The lectures cover windows bmp files.

## features
Supported features are as follows:
- Binarization
    - Otsu's method

## usage
The execution method is as follows:

```
$ python main.py INPUT_FILE OUTPUT_FILE [CMD METHOD APPLY_DIM] 
```

### about CMD
- binarize
Performs binarization on the APPLY_DIM dimension of the imput file. The threshold is calculated according to METHOD.

#### about METHOD
- Otsu
use Otsu's method
