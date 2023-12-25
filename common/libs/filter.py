from collections import defaultdict
from typing import List
from typing import Tuple
import sys

FILTER_SET = set(['SOBEL', 'RIGHT_4', 'RIGHT_25', 'RIGHT_50', 'WHITE'])
FILTERS = defaultdict()
# define filters
## sobel filter
FILTER_SOBEL = []
horizontal = [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
]

vertical = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
]

FILTER_SOBEL.append(horizontal)
FILTER_SOBEL.append(vertical)
FILTERS['SOBEL'] = FILTER_SOBEL

## parallee movement filter
FILTER_para_move_right_4 = [
    [1,0,0,0,0,0,0,0,0]
]
FILTERS['RIGHT_4'] = [FILTER_para_move_right_4]

## parallel movement filter
FILTER_para_move_right_25 = [
    [1] + [0 for _ in range(25*2)]
]
FILTERS['RIGHT_25'] = [FILTER_para_move_right_25]

## parallel movement filter
FILTER_para_move_right_50 = [
    [1] + [0 for _ in range(50*2)]
]
FILTERS['RIGHT_50'] = [FILTER_para_move_right_50]

## mosaic
FILTER_white = [
    [1,1,1],
    [1,1,1],
    [1,1,1]
]
FILTERS['WHITE'] = [FILTER_white]


def get_filter(name_filter: str)->Tuple[int, defaultdict]:
    if not name_filter in FILTER_SET:
        print(f'{name_filter} is not supported.', file=sys.stderr)
        return 1, None
    return 0, FILTERS[name_filter]

def apply_filter(img: List, bit_per_pixcel: int, height: int,
                 width: int, filter: List, apply_dims: List[int]) -> Tuple[List, int, int]:
    # assert len(filter) == 2, f"len(filter) must be 2.\nlen(filter) : {len(filter)}"
    filter_height = len(filter)
    filter_width =  len(filter[0])
    assert filter_height % 2 == 1, f"filter_height must be odd number.\nfilter_height : {filter_width}"
    assert filter_width % 2 == 1, f"filter_width must be odd number.\nfilter_width : {filter_width}"
    assert height >= filter_height, f" The height of the image must be greater than or equal to the height of the filter.\nfilter_height : {filter_height}\nheight : {height}"
    assert width >= filter_width, f" The width of the image must be greater than or equal to the width of the filter.\nfilter_width : {filter_width}\nwidth : {width}"

    img_applied = []
    for y in range(filter_height//2, height-filter_height//2):
        l = []
        for x in range(filter_width//2, width-(filter_width//2)):
            pixcel = []
            for color_dim in range(bit_per_pixcel//8):
                if color_dim not in apply_dims:
                    pixcel.append(img[y][x][color_dim])
                    continue
                n_value = 0
                for j in range(-(filter_height//2), (filter_height//2)+1):
                    for i in range(-(filter_width//2), (filter_width//2)+1):
                        n_value += img[y+j][x+i][color_dim] * filter[j+(filter_height//2)][i+(filter_width//2)]
            
                if n_value < 0:
                    n_value = 0
                if n_value > 255:
                    n_value = 255
                pixcel.append(n_value)
            l.append(pixcel) 
        img_applied.append(l)
        height_next = height-2*(filter_height//2)
        width_next = width-2*(filter_width//2)
    return img_applied, height_next, width_next
