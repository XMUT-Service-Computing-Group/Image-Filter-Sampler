import random

from PIL import Image
from flask import request


# 获得图片文件数据
def getimage():
    # 获取传入的params参数
    params = request.args.to_dict()
    path = params.get('path')
    name = params.get('name')
    if path is not None and name is not None:
        return 'path和name参数不能同时存在'
    if path is not None and name is None:
        image = Image.open(path)
        return image
    elif name is not None and path is None:
        image = Image.open('input/' + name)
        return image


def blend():
    params = request.args.to_dict()
    count = int(params.get('count'))
    if count < 10 or count > 100:
        return 'count的范围是[10,100]'
    ft = int(count * 0.2) if int(count * 0.2) <= 7 else 7  # ft = fine-tune 表示微调的数量
    count = count - ft
    if count % 3 == 1:
        countR = countG = count // 3
        countB = count // 3 + 1
    elif count % 3 == 2:
        countR = countG = count // 3 + 1
        countB = count // 3
    elif count % 3 == 0:
        countR = countG = countB = count // 3
    with open("output/RGB.txt", "w") as f:
        f.write("输出图片的滤镜RGB值：\n")
    getblend(ft, 25, 25, 25)
    getblend(countR, 255 // countR, 0, 0)
    getblend(countG, 0, 255 // countG, 0)
    getblend(countB, 0, 0, 255 // countB)
    return "ok"


def getrandom(count):
    return random.randint(0, 255 // count)


def getblend(count, r, g, b):
    image = getimage()
    if image == 'path和name参数不能同时存在':
        return image
    i = 1
    ft = ['25,0,0', '0,25,0', '0,0,25', '25,25,0', '25,0,25', '0,25,25', '25,25,25']
    random.shuffle(ft)
    isR = False
    isG = False
    isB = False
    name = ''
    if r == 0:
        isR = True
    if g == 0:
        isG = True
    if b == 0:
        isB = True
    imageFilter = Image.new("RGB", image.size, (0, 0, 0))
    Image.blend(image, imageFilter, 0).save('output/原图.png')
    data = open("output/RGB.txt", 'a')
    print('------------------------------', file=data)
    while i <= count:
        if r == g == b == 25 and count <= 7:
            imageFilter = Image.new("RGB", image.size, (
                int(ft[i - 1].split(',')[0]), int(ft[i - 1].split(',')[1]), int(ft[i - 1].split(',')[2])))
            Image.blend(image, imageFilter, 0.1).save(
                'output/' + '(' + ft[i - 1].split(',')[0] + ',' + ft[i - 1].split(',')[1] + ',' + ft[i - 1].split(',')[
                    2] + ')' + '.png')
            print('(' + ft[i - 1].split(',')[0] + ',' + ft[i - 1].split(',')[1] + ',' + ft[i - 1].split(',')[
                2] + ')', file=data)
        else:
            if isR:
                r = getrandom(count)
            if isG:
                g = getrandom(count)
            if isB:
                b = getrandom(count)
            imageFilter = Image.new("RGB", image.size, (r * i, g * i, b * i))
            Image.blend(image, imageFilter, 0.1).save(
                'output/' + '(' + str(r * i) + ',' + str(g * i) + ',' + str(b * i) + ')' + '.png')
            print('(' + str(r * i) + ',' + str(g * i) + ',' + str(b * i) + ')', file=data)
        i += 1
    data.close()
    return "ok"
