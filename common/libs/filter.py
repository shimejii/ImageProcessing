from collections import defaultdict
from typing import Tuple
import sys

FILTER_SET = set(['SOBEL'])
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
FILTER_para_move_right = [
    [1,0,0,0,0,0,0,0,0]
]

def get_filter(name_filter: str)->Tuple[int, defaultdict]:
    if not name_filter in FILTER_SET:
        print(f'{name_filter} is not supported.', file=sys.stderr)
        return 1, None
    return 0, FILTERS[name_filter]

def apply_filter(img: list, img_next: list, 
                 bit_per_pixcel: int, height: int, 
                 width: int, filter: list, 
                 filter_dim: int, apply_dim: int)->Tuple[int, list, int, int]:
    for y in range(1, height-1):
        l = []
        for x in range(1, width-1):
            pixcel = []
            n_value = -1
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    n_value += img[y-i][x-j][apply_dim] * filter[filter_dim][i+1][j+1]
                    
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

def apply_full_filter(img: list, img_next: list, 
                 bit_per_pixcel: int, height: int, 
                 width: int, filter: list, apply_dim: int)->Tuple[int, list, int, int]:
    img_new_by_filter = []
    for idx_filter in range(len(filter)):
        img_new = []
        for y in range(1, height-1):
            l = []
            for x in range(1, width-1):
                pixcel = []
                n_value = -1
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        n_value += img[y-i][x-j][apply_dim] * filter[idx_filter][i+1][j+1]
                        
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
            img_new.append(l)
        img_new_by_filter.append(img_new)
    
    for y in range(height-2):
        l = []
        for x in range(width-2):
            pixcel = []
            for color_dim in range(bit_per_pixcel//8):
                value = 0
                for idx in range(len(img_new_by_filter)):
                    value += img_new_by_filter[idx][y][x][color_dim]
                if value < 0:
                    value = 0
                if value > 255:
                    value = 255
                pixcel.append(value)
            l.append(pixcel)
        img_next.append(l)
    return 0, img_next, height-2, width-2

