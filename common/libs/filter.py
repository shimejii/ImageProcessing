from collections import defaultdict
from typing import Tuple
import sys

FILTER_SET = set(['SOBEL'])
FILTERS = defaultdict()
# define filters
## sobel filter
FILTER_SOBEL = defaultdict(list)
FILTER_SOBEL['horizontal'] = [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
]

FILTER_SOBEL['vertical'] = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
]
FILTERS['SOBEL'] = FILTER_SOBEL

def get_filter(name_filter: str)->Tuple[int, defaultdict]:
    if not name_filter in FILTER_SET:
        print(f'{name_filter} is not supported.', file=sys.stderr)
        return 1, None
    return 0, FILTERS[name_filter]

def apply_filter(img: list, img_next: list, bit_per_pixcel: int, height: int, width: int, filter: list, apply_dim: int):
    for y in range(1, height-1):
        l = []
        for x in range(1, width-1):
            pixcel = []
            n_value = -1
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    n_value += img[y-i][x-j][apply_dim] * filter[i+1][j+1]
                    
            if n_value < 0:
                n_value = 0
            if n_value > 255:
                n_value = 255
            
            for i in range(bit_per_pixcel//8):
                if i == apply_dim:
                    pixcel.append(n_value)
                else:
                    pixcel.append(img[y][x][i])      
            l.append(pixcel) 
        img_next.append(l)
    return 0, img_next, height-2, width-2

