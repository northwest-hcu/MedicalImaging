import matplotlib.pyplot as plt
from PIL import Image
import sys
import numpy as np

def get_bin_map(path: str) -> np.ndarray[np.ndarray]:
    im = Image.open(path)
    bin_map = np.asarray(im)
    width = bin_map.shape[0]
    height = bin_map.shape[1]
    print(f"{width}:{height}")
    return bin_map, width, height

def rotate_bin_map(bin_map: np.ndarray[np.ndarray], degree: int) -> np.ndarray[np.ndarray]:
    im = Image.fromarray(bin_map)
    im = im.rotate(degree, fillcolor=(255))
    bin_map = np.asarray(im)
    return bin_map

def filter_bin_map(bin_map: np.ndarray[np.ndarray], threshold: float=255/2) -> np.ndarray[np.ndarray]:
    return np.where(bin_map < threshold, 0, 255)

def check_bin_map(bin_map: np.ndarray[np.ndarray]) -> int:
    width_max = np.max(np.sum(bin_map, axis=0))
    height_max = np.max(np.sum(bin_map, axis=1))
    print(f"{width_max}:{height_max}")
    return width_max == 255 * bin_map.shape[0] or height_max == 255 * bin_map.shape[1]

def get_diff_line(bin_map, axis=0) -> np.ndarray:
    mean_line = np.mean(bin_map, axis=axis)
    print(mean_line.shape)
    diff_line = np.diff(mean_line, n=1)
    return diff_line

if __name__ == "__main__":
    print(sys.argv)
    margin = 0.05
    path = "../images/large/image04.pgm"
    bin_map, width, height = get_bin_map(path)
    deg = 35
    bin_map = rotate_bin_map(bin_map, deg)
    no_rotated = check_bin_map(bin_map)
    fig = plt.figure("window title", figsize=(8, 8))
    image_ax = fig.add_axes((0+margin, 0.3+margin, 0.7-margin*2, 0.7-margin*2))
    image_ax.set_xticks([])
    image_ax.set_yticks([])
    plt.set_cmap('binary_r')

    width_ax = fig.add_axes([0+margin, 0+margin, 0.7-margin*2, 0.3-margin*2])
    height_ax = fig.add_axes([0.7+margin, 0.3+margin, 0.3-margin*2, 0.7-margin*2])
    
    width_ax.plot(np.arange(width), np.mean(bin_map, axis=0) / 255)
    height_ax.plot(np.mean(bin_map, axis=1) / 255, np.arange(height))
    print(get_diff_line(bin_map, axis=0))
    width_ax.plot(np.arange(width - 1), get_diff_line(bin_map, axis=0))
    height_ax.plot(get_diff_line(bin_map, axis=1), np.arange(height - 1))

    width_ax.set_xlim([0, width])
    height_ax.set_ylim([0, height])
    width_ax.set_ylim([-1, 1])
    height_ax.set_xlim([-1, 1])

    # width_ax.set_xticks([])
    # height_ax.set_yticks([])

    width_ax.yaxis.tick_right()
    height_ax.xaxis.tick_bottom()
    width_ax.xaxis.tick_bottom()
    height_ax.yaxis.tick_right()
    width_ax.grid()
    height_ax.grid()

    image_ax.imshow(bin_map)
    plt.show(block=False)
    input()
