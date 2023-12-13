import sys
import os
from pathlib import Path
from typing import Tuple, List
from dataclasses import dataclass
from collections import defaultdict
from matplotlib import pyplot as plt
from my_exception import NotSupportedFileTypeError

BYTE_ORDER = 'little'
CMD_SET = set(["binarize"])
METHOD_SET = set(["Otsu"])
COLOR_ORDER = ["Blue", "Red", "Green", "Reserved"]

@dataclass
class FileHeader:
    bfType : bytes
    bfSize : bytes
    bfReserved1 : bytes
    bfReserved2 : bytes
    bfOffBits : bytes

@dataclass
class InfoHeader:
    bcSize : bytes
    bcWidth : bytes
    bcHeight : bytes
    bcPlanes : bytes
    bcBitCount : bytes
    biCompression : bytes
    biSizeImage : bytes
    biXPixPerMeter : bytes
    biYPixPerMeter : bytes
    biClrUsed : bytes
    biCirImportant : bytes

@dataclass
class ColorPalette:
    rgbBlue : bytes
    rgbGreen : bytes
    rgbRed : bytes
    rgbReserved : bytes
    
def read_win_bmp(path_file_in: Path) -> Tuple[FileHeader, InfoHeader, dict, list]:
    with path_file_in.open('rb') as fp_in:
        # header
        ## file header
        bfType = fp_in.read(2)
        if bfType != b"BM":
            raise NotSupportedFileTypeError(
                f"This file is not Windows bitmap. This file magic number is {bfType}"
                )
        bfSize = fp_in.read(4)
        bfReserved1 = fp_in.read(2)
        bfReserved2 = fp_in.read(2)
        bfOffBits = fp_in.read(4)
        
        file_header = FileHeader(
            bfType=bfType, bfSize=bfSize,
            bfReserved1=bfReserved1, bfReserved2=bfReserved2,
            bfOffBits=bfOffBits
        )

        ## info header
        bcSize = fp_in.read(4)
        if int.from_bytes(bcSize, BYTE_ORDER) == 12:
            raise NotSupportedFileTypeError(
                "This file is OS/2 Bitmap. Not supported."
            )
        if int.from_bytes(bcSize, BYTE_ORDER) != 40:
            raise NotSupportedFileTypeError(
                f"Windows bit map's info header must be 40 bytes. Not supported.¥n bcSize : {int.from_bytes(bcSize, BYTE_ORDER)}"
            )

        bcWidth = fp_in.read(4)
        bcHeight = fp_in.read(4)
        bcPlanes = fp_in.read(2)
        bcBitCount = fp_in.read(2)

        bit_per_pixcel = int.from_bytes(bcBitCount, BYTE_ORDER)
        if bit_per_pixcel == 32:
            pass
        else:
            raise NotSupportedFileTypeError(
                f"This file type is not supported.¥n bit_per_pixcel : {bit_per_pixcel}."
            )

        biCompression = fp_in.read(4)
        biCompression_int = int.from_bytes(biCompression, BYTE_ORDER)
        if biCompression_int == 0:
            pass
        else:
            raise NotSupportedFileTypeError(
                f"This file type is not supported.¥nbiCompression : {biCompression_int}."
            )

        biSizeImage = fp_in.read(4)
        biXPixPerMeter = fp_in.read(4)
        biYPixPerMeter = fp_in.read(4)
        biClrUsed = fp_in.read(4)
        biCirImportant = fp_in.read(4)
        
        info_header = InfoHeader(
            bcSize=bcSize, bcWidth=bcWidth,
            bcHeight=bcHeight, bcPlanes=bcPlanes,
            bcBitCount=bcBitCount, biCompression=biCompression,
            biSizeImage=biSizeImage, biXPixPerMeter=biXPixPerMeter,
            biYPixPerMeter=biYPixPerMeter, biClrUsed=biClrUsed,
            biCirImportant=biCirImportant
        )
        
        # palettes
        palettes = {}
        ## color paret
        if 1 <= int.from_bytes(bcBitCount, BYTE_ORDER) and int.from_bytes(bcBitCount, BYTE_ORDER) <= 8:
            num_color_paret = int.from_bytes(biClrUsed, BYTE_ORDER)
            if biClrUsed == 0:
                num_color_paret = int.from_bytes(bcBitCount, BYTE_ORDER)
            
            for i in range(num_color_paret):
                rgbBlue = fp_in.read(1)
                rgbGreen = fp_in.read(1)
                rgbRed = fp_in.read(1)
                rgbReserved = fp_in.read(1)
                palettes[i] = ColorPalette(
                    rgbBlue=rgbBlue, rgbGreen=rgbGreen,
                    rgbRed=rgbRed, rgbReserved=rgbReserved
                )
    
        height = int.from_bytes(info_header.bcHeight, BYTE_ORDER)
        width = int.from_bytes(info_header.bcWidth, BYTE_ORDER)
        
        
        # image
        img = []
        for i in range(height):
            line = []
            for _ in range(width):
                pixcel = []
                for k in range(bit_per_pixcel//8):
                    pixcel.append(int.from_bytes(fp_in.read(1), BYTE_ORDER))
                line.append(pixcel)
            img.append(line)
        img.reverse()
        
    return file_header, info_header, palettes, img

def write_win_bmp(path_file_out: Path, file_header: FileHeader,
                  info_header: InfoHeader, palettes: dict, img : List):
    with path_file_out.open('wb') as fp_out:
        # header
        ## file header
        fp_out.write(file_header.bfType)
        if file_header.bfType != b"BM":
            raise NotSupportedFileTypeError(
                f"This file is not Windows bitmap. This file magic number is {file_header.bfType}"
                )
        fp_out.write(file_header.bfSize)
        fp_out.write(file_header.bfReserved1)
        fp_out.write(file_header.bfReserved2)
        fp_out.write(file_header.bfOffBits)

        ## info header
        fp_out.write(info_header.bcSize)
        fp_out.write(info_header.bcWidth)
        fp_out.write(info_header.bcHeight)
        fp_out.write(info_header.bcPlanes)
        fp_out.write(info_header.bcBitCount)
        fp_out.write(info_header.biCompression)
        fp_out.write(info_header.biSizeImage)
        fp_out.write(info_header.biXPixPerMeter)
        fp_out.write(info_header.biYPixPerMeter)
        fp_out.write(info_header.biClrUsed)
        fp_out.write(info_header.biCirImportant)

        # color palettes
        for i in range(len(palettes)):
            fp_out.write(palettes[i].rgbBlue)
            fp_out.write(palettes[i].rgbGreen)
            fp_out.write(palettes[i].rgbRed)
            fp_out.write(palettes[i].rgbReserved)
        
        # image
        img.reverse()
        height = int.from_bytes(info_header.bcHeight, BYTE_ORDER)
        width = int.from_bytes(info_header.bcWidth, BYTE_ORDER)
        bit_per_pixcel = int.from_bytes(info_header.bcBitCount, BYTE_ORDER)
        for i in range(height):
            for j in range(width):
                for k in range(bit_per_pixcel//8):
                    fp_out.write(img[i][j][k].to_bytes(length=1, byteorder=BYTE_ORDER))

def generate_histgram(img: list, bit_per_pixcel: int, height: int, width: int,
                      power_of_two: bool = False) -> list:
    histgram = []
    if bit_per_pixcel == 8:
        histgram.append(defaultdict(int))
    elif bit_per_pixcel == 24:
        histgram.append(defaultdict(int))
        histgram.append(defaultdict(int))
        histgram.append(defaultdict(int))
    elif bit_per_pixcel == 32:
        histgram.append(defaultdict(int))
        histgram.append(defaultdict(int))
        histgram.append(defaultdict(int))
        histgram.append(defaultdict(int))
              
    else:
        print(f'Cannot support this file bit_per_pixcel.\nbpp is {bit_per_pixcel}.', file=sys.stderr)
        sys.exit(1)
    
    for i in range(height):
        for j in range(width):
            for k in range(bit_per_pixcel//8):
                value = img[i][j][k]
                if power_of_two:
                    value *= value
                histgram[k][value] += 1
    
    return histgram

def generate_cumulativeSum_count(histgram: list, index_histgram: int, power_of_two: bool = False) -> defaultdict:
    cumulativeSum_count = defaultdict(int)
    cur_histgram = histgram[index_histgram]
    cumulativeSum_count[0] = cur_histgram[0]
    stop = 256
    if power_of_two:
        stop = 256**2
    for value in range(1,stop):
        cumulativeSum_count[value] = cumulativeSum_count[value-1] + cur_histgram[value]
    return cumulativeSum_count

def generate_cumulativeSum_valueXcount(histgram: list, index_histgram: int, power_of_two: bool = False) -> defaultdict:
    cumulativeSum_valueXcount = defaultdict(int)
    cur_histgram = histgram[index_histgram]
    cumulativeSum_valueXcount[0] = 0 * cur_histgram[0]
    stop = 256
    if power_of_two:
        stop = 256**2
    for value in range(1,stop):
        cumulativeSum_valueXcount[value] = cumulativeSum_valueXcount[value-1] + (value * cur_histgram[value])
        
    return cumulativeSum_valueXcount

def discriminatn_analysis_method(img: list, bit_per_pixcel: int, height: int, width: int, apply_dim: int) -> Tuple[int, float]:
    # get histgram
    histgram_noraml = generate_histgram(img, bit_per_pixcel, height, width, power_of_two=False)
    
    # cummulative sum
    cumulativeSum_count = generate_cumulativeSum_count(histgram_noraml, apply_dim, power_of_two=False)
    cumulativeSum_valueXcount = generate_cumulativeSum_valueXcount(histgram_noraml, apply_dim, power_of_two=False)    
    
    threshold_best = -1
    variance_between_class_max = -1
    for threshold in range(1,255):
        # mean
        ## total
        sum_total = cumulativeSum_valueXcount[255]
        num_total = cumulativeSum_count[255]
        try:
            mu_total = sum_total / num_total
        except ZeroDivisionError:
            mu_total = 0
        
        ## class1 (value <= threshold)
        sum_class1 = cumulativeSum_valueXcount[threshold]
        num_class1 = cumulativeSum_count[threshold]
        try:
            mu_class1 = sum_class1 / num_class1
        except ZeroDivisionError:
            mu_class1 = 0
        
        ## class2 (value > threshold)
        sum_class2 = cumulativeSum_valueXcount[255] - cumulativeSum_valueXcount[threshold]
        num_class2 = cumulativeSum_count[255] - cumulativeSum_count[threshold]
        try:
            mu_class2 = sum_class2 / num_class2
        except ZeroDivisionError:
            mu_class2 = 0
        
        # occurence probability
        ## class1
        try:
            oc_probability_class1 = num_class1 / num_total
        except ZeroDivisionError:
            oc_probability_class1 = 0

        ## class2
        try:
            oc_probability_class2 = num_class2 / num_total
        except ZeroDivisionError:
            oc_probability_class2 = 0
        
        # between-class variance
        variance_between_class = oc_probability_class1*(mu_class1 - mu_total)**2 + oc_probability_class2*(mu_class2 - mu_total)**2
        
        if variance_between_class_max < variance_between_class:
            threshold_best = threshold
            variance_between_class_max = variance_between_class
    
    return threshold_best, variance_between_class_max

def binarization(img: list, bit_per_pixcel: int, height: int, width: int, apply_dim: int, threshold: int) -> list:
    for i in range(height):
        for j in range(width):
            for dim in range(bit_per_pixcel//8):
                if dim == apply_dim:       
                    if img[i][j][dim] >= threshold:
                        img[i][j][dim] = 255
                    else:
                        img[i][j][dim] = 0
                else:
                    img[i][j][dim] = 0
    return img

def defaultDictHistgrams2List(histgram: list, bit_per_pixcel: int):
    histgram_list = []
    for i in range(bit_per_pixcel//8):
        histgram_cur = []
        for value in range(256):
            histgram_cur.append(histgram[i][value])
        histgram_list.append(histgram_cur)
    return histgram_list

def plot_histgram(img: list, bit_per_pixcel: int, height: int, width: int):
    if bit_per_pixcel == 8:
        pass
    elif bit_per_pixcel == 24:
        pass
    elif bit_per_pixcel == 32:
        pass
    else:
        print("This bit_per_pixcel {bit_per_pixcel} is not supported.", sys.stderr)
    
    x = list(range(256))
    histgrams_defaultdict = generate_histgram(img, bit_per_pixcel, height, width, False)
    histgrams_list = defaultDictHistgrams2List(histgrams_defaultdict, bit_per_pixcel) 
    
    
    fig, ax = plt.subplots(1, bit_per_pixcel//8)
    
    if bit_per_pixcel == 8:
        ax.plot(x, histgrams_list[0])
        ax.set_xlabel("value")
        ax.set_ylabel("histgram frequency")
        ax.set_title("")
        return fig, ax

    for i in range(bit_per_pixcel//8):
        ax[i].plot(x, histgrams_list[i])
        ax[i].set_xlabel("value")
        ax[i].set_ylabel("histgram frequency")
        ax[i].set_title(COLOR_ORDER[i])
    
    
    return fig, ax
    
        
def process(img: list, bit_per_pixcel: int, height: int, width: int, cmd: str, method: str, apply_dim: int):
    if cmd == "binarize":
        threhsold = -1
        if method == "Otsu":
            print("calculate threshold with Otsu's method.")
            threhsold, variance_between_class = discriminatn_analysis_method(img, bit_per_pixcel, height, width, apply_dim)
            print(f"threshold : {threhsold}, variance_between_class : {variance_between_class}")
        else:
            print(f"{method} is not supported.")
        
        binarization(img, bit_per_pixcel, height, width, apply_dim, threhsold)
    

def main(argv: list):
    if len(argv) < 3:
        print(f'There are few arguments. len(argv) is {len(argv)}\nusage: python main.py input_file output_file [cmd method apply_dim]', file=sys.stderr)
        sys.exit(1)
    elif len(argv) > 6:
        print(f'Too many arguments. len(argv) is {len(argv)}\nusage: python main.py input_file output_file [cmd method apply_dim]', file=sys.stderr)
        sys.exit(1)
    elif len(argv) != 6:
        print('usage: python main.py input_file output_file [cmd method apply_dim]', file=sys.stderr)
        sys.exit(1)
    
    # get file path
    file_input = argv[1]
    file_output = argv[2]
    path_file_input = Path(file_input)
    path_file_output = Path(file_output)
    print(f'path_file_input : {path_file_input}')
    print(f'path_file_output : {path_file_output}')
    
    # get cmd and method
    cmd = ""
    method = ""
    if len(argv) == 6:
        cmd = argv[3]
        method = argv[4]
        apply_dim = int(argv[5])
    
    if cmd not in CMD_SET:
        print(f"{cmd} is not supported.", file=sys.stderr)
    if method not in METHOD_SET:
        print(f"{method} is not supported.", file=sys.stderr)
    
    file_header, info_header, color_palletes, img = read_win_bmp(path_file_input)
    bit_per_pixcel = int.from_bytes(info_header.bcBitCount, BYTE_ORDER)
    height = int.from_bytes(info_header.bcHeight, BYTE_ORDER)
    width = int.from_bytes(info_header.bcWidth, BYTE_ORDER)
    process(img, bit_per_pixcel, height, width, cmd, method, apply_dim)
    write_win_bmp(file_output, file_header, info_header, color_palletes, img)
    
    

if __name__ == '__main__':
    args = sys.argv
    main(args)