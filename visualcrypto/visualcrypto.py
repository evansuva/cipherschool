#
# Visual Cryptography Cookbook
# for UVA GenCyber 2018
#
# David Evans
# 14 June 2018
#

### This requires the svgwrite and PIL modules are installed. 
### If they are not already installed, you should be able to
###  install them by running:
###     pip install svgwrite
###     pip install pillow

import svgwrite # for generating graphics
from PIL import Image # for reading a bitmap image

# We'll use standard Python random, even though it is not cryptographically secure! 
# If you were planning to use any of these ciphers to protect nuclear secrets (please
# don't!), you should replace this with a cryptographic random nubmer generator,
# like the one provided by PyCrypto. After version 3.6, Python will provide the
# secrets module, with a cryptographic random number generator.
import random 

def random_sequence(n):
    """
    Returns a random sequence of bits (0 or 1) of length n.
    """
    return [random.choice([0, 1]) for i in range(n)]

def xor(a, b):
    """
    Returns the exclusive or (XOR) of the two input bits.
    """
    assert a in [0, 1]
    assert b in [0, 1]
    return (a + b) % 2

def otp(m, k):
    """
    Encrypts m using key k as a one-time pad.
    This simple returns the xor of each corresponding message and key bit.
    """
    assert len(m) == len(k)
    return [xor(mm, kk) for mm, kk in zip(m, k)]

def draw_block(svgdoc, xpos, ypos, blockx, blocky, color = "black"):
    """
    Draws a block at position (xpos, ypos) that is filled with the solid color.
    """
    svgdoc.add(svgdoc.rect(insert = (xpos * blockx, ypos * blocky),
                           size = (str(blockx) + "px", 
                                   str(blocky) + "px"),
                           stroke_width = "1",
                           stroke = "black",
                           fill = color))

def triangle_encoding(svgdoc, xpos, ypos, blockx, blocky, code):
    """
    Fills the block at (xpos, ypos) with a triangle encoding according to the code.
    code = 0 colors the traingle from the top-right to bottom-left corner;
    code = 1 colors the triangle from the top-left to bottom-right corner.
    """
    svgdoc.add(svgdoc.polygon(points=[(xpos * blockx, ypos * blocky), 
                                      (xpos * blockx + blockx, ypos * blocky + blocky),
                                      (xpos * blockx, ypos * blocky + blocky) if code
                                      else (xpos * blockx + blockx, ypos * blocky),
                                      (xpos * blockx, ypos * blocky)],
                              fill='black'))

def draw_encoding(svgdoc, xpos, ypos, blockx, blocky, code):
    if code:
        svgdoc.add(svgdoc.rect(insert = (xpos * blockx, 
                                         ypos * blocky),
                               size = (str(blockx // 2) + "px", 
                                       str(blocky) + "px"),
                               stroke_width = "0",
                               stroke = "black",
                               fill = "rgb(0,0,0)"))
    else:
        svgdoc.add(svgdoc.rect(insert = (xpos * blockx + blockx // 2, 
                                         ypos * blocky),
                               size = (str(blockx // 2) + "px", 
                                       str(blocky) + "px"),
                               stroke_width = "0",
                               stroke = "black",
                               fill = "rgb(0,0,0)"))

def draw_matrix(svgdoc, m, width, height, plain=False, encoding=draw_encoding):
    columns = len(m[0])
    rows = len(m)
    xblock = width // columns
    yblock = xblock # keep the blocks square (don't use full height if necessary)
    # print("xblock = " + str(xblock) + " columns = " + str(columns))
    # print("size: " + str(xblock * columns) + " / " + str(width))
    for rindex in range(len(m)):
        for cindex in range(len(m[rindex])):
            if plain:
                draw_block(svgdoc, cindex, rindex, xblock, yblock, 
                           color = "rgb(0,0,0)" if m[rindex][cindex] else "rgb(255,255,255)")
            else:
                encoding(svgdoc, cindex, rindex, xblock, yblock, m[rindex][cindex])
                

def draw_both(svgdoc, m1, m2, width, height, plain=False, encoding=draw_encoding):
    columns = len(m1[0])
    assert len(m2[0]) == columns
    rows = len(m1)
    assert len(m2) == rows
    xblock = width // columns
    yblock = xblock # ysize // yrange
    for rindex in range(len(m1)):
        for cindex in range(len(m1[rindex])):
            encoding(svgdoc, cindex, rindex, xblock, yblock, m1[rindex][cindex])
            encoding(svgdoc, cindex, rindex, xblock, yblock, m2[rindex][cindex])

##
## encodings
## img   key 0     key 1
##       A   B     A   B
## 0   = 1   1  /  0   0
## 1   = 0   1  /  1   0
##       
## 1 = 1/0
## 0 = 0/1
## A = img 
## img = a xor b 
##   b = key xor img

ASPECT = (8.6 / 6.5)
xsize = 880
ysize = xsize  * ASPECT


def root_name(fname):
    ext = imgfile.find('.bmp')
    assert ext > 1
    ifname = imgfile[:ext]
    ifdir = ifname.rfind('/')
    if ifdir >= 0:
        ifname = imgfile[ifdir + 1:]
    ifname = outputdir + ifname

def generate_key(width, height):
    key = random_sequence(width * height)
    keymat = [[key[(r * width + c)] for c in range(width)] for r in range(height)]
    return keymat

def generate_image(keymat, image, width, height, outputdir="./", colored=True):
    print("Image size: " + str(width) + ", " + str(height))
    
    print ("Processing image: " + image.name + "...")
    imgname = image.name
    image = Image.open(imgname).convert('1')
    image = image.resize((width, height)) # , resample=0)

    ext = imgname.find('.bmp')
    assert ext > 1
    ifname = imgname[:ext]

    iwidth, iheight = image.size
    print ("iwidth, iheight: " + str(iwidth) + ", " + str(iheight))
    assert iwidth <= width
    assert iheight <= height

    imgmat = [[1 if c < iwidth and r < iheight and image.getpixel((c, r)) > 128 
               else 0 for c in range(width)] 
              for r in range(height)]

    bmat = [[xor(imgmat[r][c], keymat[r][c]) for c in range(width)] for r in range(height)]
    
    svgimg = svgwrite.Drawing(filename = ifname + "-plain.svg",
                              size = (str(xsize) + "px", str(ysize) + "px"))
    draw_matrix(svgimg, imgmat, xsize, ysize, plain=True, encoding=triangle_encoding)
    svgimg.save()
    
    svgb = svgwrite.Drawing(filename = ifname + "-share.svg",
                            size = (str(xsize) + "px", str(ysize) + "px"))
    if colored:
        svgb.add(svgb.rect(insert = (0, 0), size = (xsize, ysize), fill = 'rgb(200,200,255)'))

    draw_matrix(svgb, bmat, xsize, ysize, encoding=triangle_encoding)
    svgb.save()

if __name__ == "__main__":    
    from argparse import ArgumentParser
    import math

    parser = ArgumentParser()
    parser.add_argument("-s", "--seed", dest = "seed",
                        type=int,
                        help="set seed (key, a number) for random number generator")
    parser.add_argument("-g", "--size", dest = "size",
                        type=int, nargs = 2,
                        help = "set the image size (two numbers, horizontal, vertical")

    parser.add_argument("-x", "--xsize", dest = "xsize",
                        type=int,
                        help = "set the image size (horizontal; vertical is scaled to page)")

    parser.add_argument("-k", "--keyfile", dest = "keyfilename",
                        help="write key to output file")
    parser.add_argument("-c", "--colored", dest = "colored",
                        help="use a background color",
                        type = bool,
                        default = True)

    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")

    parser.add_argument("-i", "--image",
                        type=open,
                        dest="image")


    args = parser.parse_args()
    if args.seed:
        print ("Seed: " + str(args.seed))
        seed = args.seed
    else:
        import time
        seed = int(time.time())
        print ("No seed, using: " +str(seed))

    random.seed(int(seed))    

    if args.size:
        width = args.size[0]
        height = args.size[1]
        print ("Size: " + str(width) + ", " + str(height))
        assert not args.xsize
    elif args.xsize:
        width = args.xsize
        height = math.floor(width * ASPECT)
        print ("Size: " + str(width) + ", " + str(height))
    else:
        # read size from source image
        if len(args.images) < 1:
            print ("Error: must either provide a source image or specify size.")
        else:
            imgfile = args.images[0]
            im = Image.open(imgfile).convert('1')
            width, height = im.size

    keymat = generate_key(width, height)

    if args.keyfilename:
        keyfile = args.keyfilename
        print ("Writing key to: " + keyfile)
        svgkey = svgwrite.Drawing(filename = keyfile,
                                  size = (str(xsize) + "px", str(ysize) + "px"))
        if args.colored:

            svgkey.add(svgkey.rect(insert = (0, 0), size = (xsize, ysize), fill = "rgb(255,200,200)"))
        draw_matrix(svgkey, keymat, xsize, ysize, encoding=triangle_encoding)
        svgkey.save()

    if args.image:
        print ("Generating image: " + args.image.name)
        #for image in args.images:
        generate_image(keymat, args.image, width, height) # , colored)
