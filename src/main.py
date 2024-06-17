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
    im.rotate(degree, fillcolor=(255))
    bin_map = np.asarray(im)
    return bin_map

def filter_bin_map(bin_map: np.ndarray[np.ndarray], threshold=255/2) -> bin_map:
    return np.where(bin_map < threshold, 0, 255)

def get_diff_line(bin_map, axis=0) -> np.ndarray:
    mean_line = np.mean(bin_map, axis=axis)
    diff_line = np.diff(mean_line, n=1)
    return diff_line

if __name__ == "__main__":
    print(sys.argv)
    margin = 0.04
    path = "../images/large/image04.pgm"
    for deg in range(90):
        bin_map, width, height = get_bin_map(path, deg)
        fig = plt.figure(figsize=(8, 8))
        image_ax = fig.add_axes((0+margin, 0.3+margin, 0.7-margin*2, 0.7-margin*2))
        image_ax.set_xticks([])
        image_ax.set_yticks([])
        plt.set_cmap('binary_r')

        width_ax = fig.add_axes([0+margin, 0+margin, 0.7-margin*2, 0.3-margin*2])
        height_ax = fig.add_axes([0.7+margin, 0.3+margin, 0.3-margin*2, 0.7-margin*2])
        
        width_ax.plot(np.arange(width), np.mean(bin_map, axis=0) / 255)
        height_ax.plot(np.mean(bin_map, axis=1) / 255, np.arange(height))
        width_ax.plot(np.arange(width), np.var(bin_map, axis=0) / (255*255))
        height_ax.plot(np.var(bin_map, axis=1) / (255*255), np.arange(height))

        width_ax.set_xlim([0, width])
        height_ax.set_ylim([0, height])
        width_ax.set_ylim([0, 1])
        height_ax.set_xlim([0, 1])

        width_ax.set_xticks([])
        height_ax.set_yticks([])

        width_ax.yaxis.tick_right()
        height_ax.xaxis.tick_bottom()

        image_ax.imshow(bin_map)
    plt.show()
