import matplotlib.pyplot as plt
from PIL import Image
import sys
import numpy as np
from gui import plot, im_plot
from typing import TypeAlias
from rembg import remove

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

def get_diff_line(line: np.ndarray[int]) -> np.ndarray[float]:
    new_line = np.diff(line, n=1)
    return new_line

def filter_bitmap(bitmap: Bitmap, border: int = int(255 / 2)):
    filtered_bitmap = np.where(bitmap < border, 0, 255)
    return filtered_bitmap

def spread_black(bitmap: Bitmap, margin: int=10):
    height, width = bitmap.shape
    new_bitmap = bitmap.copy()
    
    # 左辺方向
    for h in range(height):
        for w in range(1, width):
            if new_bitmap[h, w - 1] >= new_bitmap[h, w] - margin and not new_bitmap[h, w - 1] == 0:
                # print(f"{new_bitmap[h, w - 1]} >= {new_bitmap[h, w]}")
                new_bitmap[h, w - 1] = 0
            else:
                break

    return new_bitmap

if __name__ == "__main__":
    # ファイルの読み込み
    for i in range(5):
        path = f"../images/large/image0{i+1}.pgm"
        path = f"../images/large/image02.pgm"
        im = path2im(path)
        bitmap = im2bitmap(im)
        width_diff_bitmap = get_diff_bitmap(bitmap, axis=WIDTH_DIRECTION)
        height_diff_bitmap = get_diff_bitmap(bitmap, axis=HEIGHT_DIRECTION)
        diff_bitmap = get_diff_bitmap(width_diff_bitmap, axis=HEIGHT_DIRECTION)
        filtered_bitmap = bitmap # filter_bitmap(bitmap)
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
        sb1 = spread_black(filtered_bitmap)
        sb2 = im2bitmap(rotate_img(bitmap2im(spread_black(im2bitmap(rotate_img(bitmap2im(filtered_bitmap), 90)))), -90))
        sb3 = im2bitmap(rotate_img(bitmap2im(spread_black(im2bitmap(rotate_img(bitmap2im(filtered_bitmap), 180)))), -180))
        sb4 = im2bitmap(rotate_img(bitmap2im(spread_black(im2bitmap(rotate_img(bitmap2im(filtered_bitmap), 270)))), -270))
        # 変更点を取得
        sb1_diff = sb1 != filtered_bitmap
        sb2_diff = sb2 != filtered_bitmap
        sb3_diff = sb3 != filtered_bitmap
        sb4_diff = sb4 != filtered_bitmap
        # 変更の重複点を取得
        sb_diff_1_2 = (sb1_diff * 1 + sb2_diff * 1) == 2
        sb_diff_2_3 = (sb2_diff * 1 + sb3_diff * 1) == 2
        sb_diff_3_4 = (sb3_diff * 1 + sb4_diff * 1) == 2
        sb_diff_4_1 = (sb4_diff * 1 + sb1_diff * 1) == 2
        sb_diff_all = np.where((sb_diff_1_2 * 1 + sb_diff_2_3 * 1 + sb_diff_3_4 * 1 + sb_diff_3_4 * 1) > 1, 255, 0)
        
        im_plot(sb_diff_1_2, title="sb_diff_1_2")
        im_plot(sb_diff_2_3, title="sb_diff_2_3")
        im_plot(sb_diff_3_4, title="sb_diff_3_4")
        im_plot(sb_diff_4_1, title="sb_diff_4_1")
        im_plot(sb_diff_all, title="sb_diff_all")
        # im_plot(bitmap, title=path)
        # im_plot(width_diff_bitmap, title=path + "[width diff]")
        # im_plot(height_diff_bitmap, title=path + "[height diff]")
        im_plot(filtered_bitmap, title=path + "[filtered]")
        im_plot(sb1, title=path + "[spread black 0]")
        im_plot(sb2, title=path + "[spread black 90]")
        im_plot(sb3, title=path + "[spread black 180]")
        im_plot(sb4, title=path + "[spread black 270]")
        # im_plot(sb, title=path + "[spread black all]")
        plot(bitmap, np.mean(width_diff_bitmap, axis=WIDTH_DIRECTION), np.mean(height_diff_bitmap, axis=HEIGHT_DIRECTION))
        plot(filtered_bitmap, np.mean(filtered_bitmap, axis=WIDTH_DIRECTION), np.mean(filtered_bitmap, axis=HEIGHT_DIRECTION))
        break
    input()

   