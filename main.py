import sys
import os
from pathlib import Path
from typing import Tuple
from dataclasses import dataclass

BYTE_ORDER = 'little'

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
    
def read_win_bmp(path_file_in: str) -> Tuple[FileHeader, InfoHeader, dict, list]:
    if not os.path.exists(path_file_in):
        print('input file does not exist.\n{path_file_in}', file=sys.stderr)
        sys.exit(1)
    with open(path_file_in, 'rb') as fp_in:
        # header
        ## file header
        bfType = fp_in.read(2)
        if bfType.decode('utf-8') != "BM":
            print(f'This file is not Windows bigtmap. Signature is {bfType.decode(encoding="utf-8")}', file=sys.stderr)
            fp_in.close()
            sys.exit(1)
            
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
        if int.from_bytes(bcSize, BYTE_ORDER) != 40:
            print(f'This file is not Windows bigtmap.', file=sys.stderr)
            fp_in.close()
            sys.exit(1)

        bcWidth = fp_in.read(4)
        bcHeight = fp_in.read(4)
        bcPlanes = fp_in.read(2)
        bcBitCount = fp_in.read(2)
        bit_per_pixcel = int.from_bytes(bcBitCount, BYTE_ORDER)
        
        if bit_per_pixcel == 8:
            pass
        elif bit_per_pixcel == 24:
            pass
        elif bit_per_pixcel == 32:
            pass
        else:
            print(f'Cannot support this file bit_per_pixcel.\nbpp is {bit_per_pixcel}.', file=sys.stderr)
            fp_in.close()
            sys.exit(1)
        
        biCompression = fp_in.read(4)
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
            num_color_paret = -1
            if biClrUsed == 0:
                num_color_paret = bcBitCount
            
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
                    pixcel.append(int.from_bytes(fp_in.read(1)))
                line.append(pixcel)
            img.append(line)
        img.reverse()
        
    return file_header, info_header, palettes, img

def write_win_bmp(path_file_out :str, file_header : FileHeader,
                  info_header: InfoHeader, palettes : dict, img : list):
    
    with open(path_file_out, 'wb') as fp_out:
        # write
        fp_out = open(path_file_out, 'wb')

        # header
        ## file header
        fp_out.write(file_header.bfType)
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
                    fp_out.write(img[i][j][k].to_bytes())

def main(argv: list):
    if len(argv) < 3:
        print(f'There are few arguments. len(argv) is {len(argv)}\nusage: python main.py [input_file] [output_file]', file=sys.stderr)
        sys.exit(1)
    if len(argv) > 3:
        print(f'Too many arguments. len(argv) is {len(argv)}\nusage: python main.py [input_file] [output_file]', file=sys.stderr)
        sys.exit(1)
        
    file_input = argv[1]
    file_output = argv[2]
    path_file_input = Path(file_input).resolve()
    path_file_output = Path(file_output).resolve()
    print(f'path_file_input : {path_file_input}')
    print(f'path_file_output : {path_file_output}')
    
    file_header, info_header, color_palletes, img = read_win_bmp(path_file_input)
    write_win_bmp(file_output, file_header, info_header, color_palletes, img)
    
    

if __name__ == '__main__':
    args = sys.argv
    main(args)