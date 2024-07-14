import matplotlib.pyplot as plt
from PIL import Image
import sys
import numpy as np
from gui import plot, im_plot, all_plot
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

def get_hit_wave(bitmap: Bitmap, axis: int=WIDTH_DIRECTION) -> np.ndarray[int]:
    hit = np.any(bitmap == 0, axis=axis)
    peaks = np.argmax(bitmap == 0, axis=axis)
    wave = [peak if h else bitmap.shape[axis] - 1 for peak, h in zip(peaks, hit)]
    return wave

def get_peak_point(peaks: np.ndarray[float], axis: int=WIDTH_DIRECTION) -> tuple[int]:
    # hit = np.any(bitmap == 0, axis=axis)
    # peaks = np.argmax(bitmap == 0, axis=axis)
    # peaks = [peak if hit else bitmap.shape[axis] for peak, hit in zip(np.argmax(bitmap == 0, axis=axis), np.any(bitmap == 0, axis=axis))]
    left_side_peaks = peaks.copy()
    right_side_peaks = peaks.copy()
    right_side_peaks.reverse()
    left_side_peak = len(left_side_peaks) - 1
    right_side_peak = len(right_side_peaks) - 1
    pre_diff = -float('Inf') 
    for i in range(left_side_peak):
        if i + 1 < len(left_side_peaks):
            diff = (left_side_peaks[i + 1] - left_side_peaks[i])
            if left_side_peaks[i] > left_side_peaks[i + 1]:
                left_side_peak = i #left_side_peaks[i]
                break
            if diff < pre_diff:
                left_side_peak = i #left_side_peaks[i]
                break
            else:
                pre_diff = diff
    pre_diff = -float('Inf') 
    for i in range(right_side_peak):
        if i + 1 < len(right_side_peaks):
            if right_side_peaks[i] > right_side_peaks[i + 1]:
                right_side_peak = i #right_side_peaks[i]
                break
            if diff < pre_diff:
                right_side_peak = i #right_side_peaks[i]
                break
            else:
                pre_diff = diff
    right_side_peak = len(peaks) - 1 - right_side_peak
    print(left_side_peak, right_side_peak)
    print("peaks left:({0}@{1}), right:({2}@{3})".format(peaks[left_side_peak], left_side_peak, peaks[right_side_peak], right_side_peak))
    return left_side_peak, right_side_peak
    
def area_axes(bitmap: Bitmap) -> tuple[np.ndarray[float]]:
    left_side = get_hit_wave(bitmap, axis=WIDTH_DIRECTION)
    right_side = [bitmap.shape[WIDTH_DIRECTION] - wave - 1 for wave in get_hit_wave(
            np.flip(bitmap, axis=WIDTH_DIRECTION),
            axis=WIDTH_DIRECTION
        )]
    top_side = get_hit_wave(bitmap, axis=HEIGHT_DIRECTION)
    bottom_side = [bitmap.shape[HEIGHT_DIRECTION] - wave - 1 for wave in get_hit_wave(
            np.flip(bitmap, axis=HEIGHT_DIRECTION),
            axis=HEIGHT_DIRECTION
        )]
    return left_side, right_side, top_side, bottom_side


if __name__ == "__main__":
    # ファイルの読み込み
    for i in range(5):
        path = f"../images/large/image0{i+1}.pgm"
        path = f"../images/large/image04.pgm"
        im = path2im(path)
        bitmap = im2bitmap(im)
        width_diff_bitmap = get_diff_bitmap(bitmap, axis=WIDTH_DIRECTION)
        height_diff_bitmap = get_diff_bitmap(bitmap, axis=HEIGHT_DIRECTION)
        filtered_bitmap = filter_bitmap(bitmap, border=np.mean(np.mean(bitmap)))
        left_side, right_side, top_side, bottom_side = area_axes(filtered_bitmap)

        all_plot(
            bitmap,
            left_side,
            right_side,
            top_side,
            bottom_side,
            title="area plot"
        )
        fig, left_axis, right_axis, top_axis, bottom_axis = all_plot(
            filtered_bitmap,
            left_side,
            right_side,
            top_side,
            bottom_side,
            title="area plot2"
        )
        # 左のグラフの修正
        print("fix left graph")
        left_side_peak, right_side_peak = get_peak_point([len(left_side) - l - 1 for l in left_side])
        left_axis.plot(
            [left_side[left_side_peak], left_side[right_side_peak]],
            [left_side_peak, right_side_peak],
            color='orange')
        left_axis.plot(np.arange(bitmap.shape[WIDTH_DIRECTION]), left_side, color='lime')
        print("fix right graph")
        # 右のグラフの修正
        left_side_peak, right_side_peak = get_peak_point([r for r in right_side])
        right_axis.plot(
            [right_side[left_side_peak], right_side[right_side_peak]],
            [left_side_peak, right_side_peak],
            color='orange')
        right_axis.plot(np.arange(bitmap.shape[WIDTH_DIRECTION]), right_side, color='lime')
        print("fix top graph")
        # 上グラフの修正
        left_side_peak, right_side_peak = get_peak_point([len(top_side) - t - 1 for t in top_side])
        top_axis.plot(
            [left_side_peak, right_side_peak],
            [top_side[left_side_peak], top_side[right_side_peak]],
            color='orange')
        top_axis.plot(np.arange(bitmap.shape[HEIGHT_DIRECTION]), top_side, color='lime')
        print("fix bottom graph")
        # 下グラフの修正
        left_side_peak, right_side_peak = get_peak_point([b for b in bottom_side])
        bottom_axis.plot(
            [left_side_peak, right_side_peak],
            [bottom_side[left_side_peak], bottom_side[right_side_peak]],
            color='orange')
        bottom_axis.plot(np.arange(bitmap.shape[HEIGHT_DIRECTION]), bottom_side, color='lime')
        plt.show(block=False)
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
        # plot(bitmap, np.mean(bitmap, axis=WIDTH_DIRECTION), np.mean(bitmap, axis=HEIGHT_DIRECTION), title="bitmap {0}".format(path))
        # plot(bitmap, get_hit_wave(bitmap, axis=HEIGHT_DIRECTION), get_hit_wave(bitmap, axis=WIDTH_DIRECTION), title="bitmap hitwave {0}".format(path))
        # plot(filtered_bitmap, np.mean(filtered_bitmap, axis=WIDTH_DIRECTION), np.mean(filtered_bitmap, axis=HEIGHT_DIRECTION), title="filtered {0}".format(path))
        # plot(filtered_bitmap, get_hit_wave(filtered_bitmap, axis=HEIGHT_DIRECTION), get_hit_wave(filtered_bitmap, axis=WIDTH_DIRECTION), title="filtered hit wave{0}".format(path))
        # plot(filtered_bitmap, get_hit_wave(np.flip(filtered_bitmap, axis=HEIGHT_DIRECTION), axis=HEIGHT_DIRECTION), get_hit_wave(np.flip(filtered_bitmap, axis=WIDTH_DIRECTION), axis=WIDTH_DIRECTION), title="reversed hit wave{0}".format(path))
        # plot(filtered_bitmap, np.mean(filtered_bitmap, axis=WIDTH_DIRECTION), np.mean(filtered_bitmap, axis=HEIGHT_DIRECTION))
        break
    input()

   