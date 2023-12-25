import main
import sys
from pathlib import Path
# import subprocess
# import time
# from my_exception import NotSupportedFileTypeError
import pytest
import filter

@pytest.fixture
def setup():
    # load bmp
    file_name_in = "./s_bmp/win-32.bmp"
    _, info_header, _, img = main.read_win_bmp(Path(file_name_in))
    bit_per_pixcel = int.from_bytes(info_header.bcBitCount, main.BYTE_ORDER)
    height = int.from_bytes(info_header.bcHeight, main.BYTE_ORDER)
    width = int.from_bytes(info_header.bcWidth, main.BYTE_ORDER)

    # apply filter
    filter_name = "SOBEL"
    _, fil = filter.get_filter(filter_name)
    sobel_0 = fil[0]
    apply_dim = [0]
    img_applied, height_applied, width_applied = filter.apply_filter(img, bit_per_pixcel, height, width, sobel_0, apply_dim)

    return img, bit_per_pixcel, height, width, img_applied, height_applied, width_applied

# 畳み込み
## filter : sobel[0]
### [
###     [-1, -2, -1],
###     [0, 0, 0],
###     [1, 2, 1]
### ]
## input :  windows bitmap file
### [
###     [43, 43, 43],
###     [52, 43, 43],
###     [52, 43, 43]
### ]
### bpp : 32
### compression : 0
### position : upper left
### apply_dims : [0]
def test_convolution_with_sobel0__case_upper_left(setup):
    _, _, height, width, img_applied, height_applied, width_applied = setup
    assert height - 2 == height_applied
    assert width - 2 == width_applied
    value = -1 * 43 -2 * 43 -1 * 43 + 0 * 52 + 0 * 43 + 0 * 43 + 1 * 52 + 2 * 43 + 1 * 43
    print()
    print(value)
    print()
    if value > 255:
        value = 255
    if value < 0:
        value = 0
    
    assert img_applied[0][0][0] == value
