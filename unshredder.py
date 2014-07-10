from PIL import Image

image = Image.open("_dunya.jpg")
data = image.getdata()
SHREDS = 10
unshredded = Image.new("RGBA", image.size)
width, height = image.size
shred_width = width / SHREDS
pairs = {}
check = -1


def get_pixel_value(x, y, _image):
    pixel = _image.getdata()[y * _image.size[0] + x]
    return pixel


def diff_compare(right, left):
    r, g, b = 0, 0, 0
    diff = 0
    for i in range(height):
        right_pixel = get_pixel_value(shred_width - 1, i, right)
        left_pixel = get_pixel_value(0, i, left)
        r = abs(right_pixel[0] - left_pixel[0])
        g = abs(right_pixel[1] - left_pixel[1])
        b = abs(right_pixel[2] - left_pixel[2])
        diff += r + g + b
    return diff


def slice_image(shred_index):
    x1, y1 = shred_width * shred_index, 0
    x2, y2 = x1 + shred_width, height
    crop = image.crop((x1, y1, x2, y2))
    shred = Image.new("RGBA", (shred_width, height))
    shred.paste(crop, (0, 0))
    return shred

for i in range(SHREDS):
    pairs[i] = {0: -1, 1: 0}

for i in range(SHREDS):
    lowestShred, lowestCount = -1, -1
    for j in range(SHREDS):
        shered_a, shered_b = slice_image(i), slice_image(j)

        diff = diff_compare(shered_a, shered_b)

        if lowestCount == -1 or diff < lowestCount:
            lowestShred = j
            lowestCount = diff

    if pairs[lowestShred][0] == -1 or pairs[lowestShred][1] > lowestCount:
        pairs[lowestShred][0] = i
        pairs[lowestShred][1] = lowestCount

for i in range(SHREDS):
    for j in range(SHREDS):
        if pairs[j][0] == check:
            check = j
            unshredded.paste(slice_image(j), (shred_width * i, 0))
            break

unshredded.save("final.jpg")