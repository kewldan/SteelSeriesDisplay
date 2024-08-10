from PIL.Image import Palette, Dither, Image


def image_to_bitmap(image: Image) -> list[int]:
    bmp = image.convert("1", palette=Palette.ADAPTIVE, dither=Dither.FLOYDSTEINBERG)

    w, h = image.size

    arr = list(bmp.getdata())

    bmp.close()

    if len(arr) < w * h:
        rows = []
        for r in range(0, len(arr), len(arr) // w):
            rows.append(arr[r:r + len(arr) // h - 1])
        for i, r in enumerate(rows):
            if len(r) < w:
                rows[i].extend([0] * (w - len(r)))
        if len(rows) < h:
            rows.extend([[0] * w] * (h - len(rows)))
        arr = [a for b in rows for a in b]

    new_arr = []
    temp_byte = ''
    for c in arr:
        if int(c) > 1:
            c = 1
        temp_byte += str(c)
        if len(temp_byte) == 8:
            new_arr.append(int(temp_byte, 2))
            temp_byte = ''
    return new_arr


