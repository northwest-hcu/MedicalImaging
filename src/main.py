import matplotlib.pyplot as plt
from PIL import Image
import sys
import numpy as np
from gui import plot, im_plot
from typing import TypeAlias

Bitmap: TypeAlias = np.ndarray[np.ndarray[int]]
WIDTH_DIRECTION = 1
HEIGHT_DIRECTION = 0


def path2im(path: str) -> Image:
    im = Image.open(path)
    return im

def im2bitmap(im: Image) -> Bitmap:
    bitmap = np.asarray(im)
    bitmap = bitmap.astype(np.int16)
    return bitmap

def bitmap2im(bitmap: Bitmap) -> Image:
    bitmap = bitmap.astype(np.uint8)
    im = Image.fromarray(bitmap)
    return im

def add_margin(im: Image, top: int, right: int, bottom: int, left: int, color: int):
    width, height = im.size
    new_width = width + right + left
    new_height = height + top + bottom
    expand_im = Image.new(im.mode, (new_width, new_height), color)
    expand_im.paste(im, (left, top))
    return expand_im

def rotate_img(im: Image, degree: int, fillcolor=255):
    rotated_im = im.rotate(degree, expand=True, fillcolor=(fillcolor))
    return rotated_im

def get_diff_bitmap(bitmap: Bitmap, axis: int = WIDTH_DIRECTION) -> Bitmap:
    new_bitmap = np.diff(bitmap, n=1, axis=axis)
    return new_bitmap

def filter_bitmap(bitmap: Bitmap, border: int = int(255 / 2)):
    filtered_bitmap = np.where(bitmap < border, 0, 255)
    return filtered_bitmap

def spread_black(bitmap: Bitmap):
    height, width = bitmap.shape
    new_bitmap = bitmap.copy()
    left_index, top_index, right_index, bottom_index = -1, -1, -1, -1

    h = 0
    # 左端の座標探索 x軸
    while h < height:
        left_array = (new_bitmap[h, :] == 255)
        left_index = np.argmax(left_array)
        if left_array[left_index]:
            break
        h = h + 1

    # 上端の頂点座標探索 y軸
    w = 0
    while w < width:
        top_array = (new_bitmap[:, w] == 255)
        top_index = np.argmax(top_array)
        if top_array[top_index]:
            break
        w = w + 1

    h = height - 1
    # 右端の頂点座標探索 x軸
    while h >= 0:
        right_array = (new_bitmap[h, :] == 255)
        right_index = np.argmax(right_array)
        if right_array[right_index]:
            break
        h = h - 1

    w = width - 1
    # 下端の頂点座標探索 x軸
    while w >= 0:
        bottom_array = (new_bitmap[:, w] == 255)
        bottom_index = np.argmax(bottom_array)
        if bottom_array[bottom_index]:
            break
        w = w - 1

    print(top_index, left_index, bottom_index, right_index)

    new_bitmap[top_index:bottom_index, left_index:right_index] = 255
    return new_bitmap

if __name__ == "__main__":
    # ファイルの読み込み
    for i in range(5):
        path = f"../images/large/image0{i+1}.pgm"
        path = f"../images/large/image04.pgm"
        im = path2im(path)
        bitmap = im2bitmap(im)
        width_diff_bitmap = get_diff_bitmap(bitmap, axis=WIDTH_DIRECTION)
        height_diff_bitmap = get_diff_bitmap(bitmap, axis=HEIGHT_DIRECTION)
        diff_bitmap = get_diff_bitmap(width_diff_bitmap, axis=HEIGHT_DIRECTION)
        filtered_bitmap = filter_bitmap(bitmap)
        threshold = 254
        # for deg in range(50):
        #     rotated_bitmap = im2bitmap(
        #         rotate_img(
        #             bitmap2im(filtered_bitmap),
        #             deg
        #         )
        #     )
        #     width_mean = np.mean(rotated_bitmap, axis=WIDTH_DIRECTION)
        #     height_mean = np.mean(rotated_bitmap, axis=HEIGHT_DIRECTION)
        #     if np.max(width_mean) > threshold or np.max(height_mean) > threshold:
        #         print(f"{deg}° : {width_mean} : {height_mean} ")
        #         plot(rotated_bitmap, width_mean, height_mean, title=path + f"[rotate: {deg}°]")
        sb = spread_black(filtered_bitmap)
        im_plot(bitmap, title=path)
        im_plot(width_diff_bitmap, title=path + "[width diff]")
        im_plot(height_diff_bitmap, title=path + "[height diff]")
        im_plot(filtered_bitmap, title=path + "[filtered]")
        im_plot(sb, title=path + "[spread black]")
        plot(bitmap, np.mean(width_diff_bitmap, axis=WIDTH_DIRECTION), np.mean(height_diff_bitmap, axis=HEIGHT_DIRECTION))
        plot(filtered_bitmap, np.mean(filtered_bitmap, axis=WIDTH_DIRECTION), np.mean(filtered_bitmap, axis=HEIGHT_DIRECTION))
        break
    input()

   