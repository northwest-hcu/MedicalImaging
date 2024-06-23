import matplotlib.pyplot as plt
from PIL import Image
import sys
import numpy as np
from gui import plot

def get_bin_map(path: str) -> np.ndarray[np.ndarray]:
    im = Image.open(path)
    # im = add_margin(im, 10, 10, 10, 10, 255)
    bin_map = np.asarray(im)
    width = bin_map.shape[0]
    height = bin_map.shape[1]
    print(f"{width}:{height}")
    return bin_map, width, height

def rotate_bin_map(bin_map: np.ndarray[np.ndarray], degree: int) -> np.ndarray[np.ndarray]:
    bin_map.dtype = 'uint8'
    im = Image.fromarray(bin_map)
    im = im.rotate(degree, fillcolor=(255), expand=1)
    bin_map = np.asarray(im)
    return bin_map

def filter_bin_map(bin_map: np.ndarray[np.ndarray], threshold: float=255/2) -> np.ndarray[np.ndarray]:
    filtered_bin_map = [[255 if b > threshold else 0 for b in map] for map in bin_map]
    return np.asarray(filtered_bin_map)
    

def add_margin(img, top, right, bottom, left, color):
    width, height = img.size
    new_width = width + right + left
    new_height = height + top + bottom
    im = Image.new(img.mode, (new_width, new_height), color)
    im.paste(img, (left, top))
    return im

# 境目を取得
def get_border(width_diff: np.ndarray, height_diff: np.ndarray) -> tuple[int]:
    # print(f"{np.max(width_diff)}:{np.max(width_diff)}")
    return np.argmax(np.fabs(width_diff)), np.argmax(np.fabs(height_diff))

# 最大の傾きの大きさ取得
def get_max_value(width_diff: np.ndarray, height_diff: np.ndarray) -> tuple[float]:
    width_diff_index, height_diff_index = get_border(width_diff, height_diff)
    width_diff_max = np.fabs(width_diff)[width_diff_index]
    height_diff_max = np.fabs(height_diff)[height_diff_index]
    if width_diff_max > height_diff_max:
        return width_diff_max
    else:
        return height_diff_max

def check_border(width_diff: np.ndarray, height_diff: np.ndarray) -> bool:
    threshold = 5
    width_diff_max, height_diff_max = get_border(width_diff, height_diff)
    return width_diff_max > threshold or height_diff_max > threshold

def get_diff_line(bin_map, axis=0) -> np.ndarray:
    mean_line = np.mean(bin_map, axis=axis)
    diff_line = np.diff(mean_line, n=1)
    return diff_line

if __name__ == "__main__":
    # ファイルの読み込み
    path = "../images/large/image01.pgm"
    bin_map, width, height = get_bin_map(path)
    bin_map = filter_bin_map(bin_map)

    # 回転角度の決定
    max_diffs = np.empty(360)
    for deg in range(360):
        rotated_bin_map = rotate_bin_map(bin_map, deg)
        print(rotated_bin_map.dtype)
        width_diff = get_diff_line(rotated_bin_map, axis=0)
        height_diff = get_diff_line(rotated_bin_map, axis=1)
        max_diffs[deg] = get_max_value(width_diff, height_diff)
        # print(max_diffs[deg])
    
    correct_deg = np.argmax(max_diffs)
    print(correct_deg)
    bin_map = rotate_bin_map(bin_map, correct_deg)
    width_diff = get_diff_line(bin_map, axis=0)
    height_diff = get_diff_line(bin_map, axis=1)

    # plot
    plot(bin_map, width_diff, height_diff)

   