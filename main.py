import sys
import builtins
import io
from pathlib import Path
BYTE_ORDER = sys.byteorder


path_file_in = "./boy.bmp"

def is_path(f):
    return isinstance(f, (bytes, str, Path))

filename_in = ""
if isinstance(path_file_in, Path):
    filename_in = str(path_file_in.resolve())
elif is_path(path_file_in):
    filename_in = path_file_in


if filename_in:
    fp_in = builtins.open(filename_in, 'rb')

try:
    fp_in.seek(0)
except (AttributeError, io.UnsupportedOperation):
    fp_in = io.BytesIO(fp_in.read())

# header
## file header
bfType = fp_in.read(2)
if bfType.decode('utf-8') != "BM":
    print(f'This file is not Windows bigtmap. Signature is {bfType.decode(encoding="utf-8")}', file=sys.stderr)
    fp_in.close()
    exit()

bfSize = fp_in.read(4)
bfReserved1 = fp_in.read(2)
bfReserved2 = fp_in.read(2)
bfOffBits = fp_in.read(4)

## info header / core header
bcSize = fp_in.read(4)
if int.from_bytes(bcSize, BYTE_ORDER) != 40:
    print(f'This file is not Windows bigtmap.', file=sys.stderr)
    fp_in.close()
    exit()

bcWidth = fp_in.read(4)
bcHeight = fp_in.read(4)
bcPlanes = fp_in.read(2)
bcBitCount = fp_in.read(2)
biCompression = fp_in.read(4)
biSizeImage = fp_in.read(4)
biXPixPerMeter = fp_in.read(4)
biYPixPerMeter = fp_in.read(4)
biClrUsed = fp_in.read(4)
biCirImportant = fp_in.read(4)

parets = {}
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
        parets[i] = (rgbBlue, rgbGreen, rgbRed, rgbReserved)

height = int.from_bytes(bcHeight, BYTE_ORDER)
width = int.from_bytes(bcWidth, BYTE_ORDER)
img = []
for i in range(height):
    line = []
    for j in range(width):
        blue = int.from_bytes(fp_in.read(1), BYTE_ORDER)
        green = int.from_bytes(fp_in.read(1), BYTE_ORDER)
        red = int.from_bytes(fp_in.read(1), BYTE_ORDER)
        line.append((blue, green, red))
    img.append(line)
# print(img)
img.reverse()

# write
path_file_out = "./boy_reserved.bmp"
fp_out = open(path_file_out, 'wb')

# header
## file header
fp_out.write(bfType)
fp_out.write(bfSize)
fp_out.write(bfReserved1)
fp_out.write(bfReserved2)
fp_out.write(bfOffBits)

## info header
fp_out.write(bcSize)
fp_out.write(bcWidth)
fp_out.write(bcHeight)
fp_out.write(bcPlanes)
fp_out.write(bcBitCount)
fp_out.write(biCompression)
fp_out.write(biSizeImage)
fp_out.write(biXPixPerMeter)
fp_out.write(biYPixPerMeter)
fp_out.write(biClrUsed)
fp_out.write(biCirImportant)

for i in range(len(parets)):
    for j in range(4):
        fp_out.write(parets[i][j])

# image
# img.reverse()

for i in range(height):
    for j in range(width):
        blue = img[i][j][0]
        green = img[i][j][1]
        red = img[i][j][2]
        fp_out.write(int.to_bytes(blue))
        fp_out.write(int.to_bytes(green))
        fp_out.write(int.to_bytes(red))

fp_out.close()
