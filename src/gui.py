import matplotlib.pyplot as plt
import numpy as np

def plot(bin_map: np.ndarray[np.ndarray], width_diff: np.ndarray[float], height_diff: np.ndarray[float], margin: float=0.05):
    fig = plt.figure("window title", figsize=(8, 8))
    image_ax = fig.add_axes((0+margin, 0.3+margin, 0.7-margin*2, 0.7-margin*2))
    image_ax.set_xticks([])
    image_ax.set_yticks([])
    plt.set_cmap('binary_r')

    width_mean_ax = fig.add_axes([0+margin, 0+margin, 0.7-margin*2, 0.3-margin*2])
    height_mean_ax = fig.add_axes([0.7+margin, 0.3+margin, 0.3-margin*2, 0.7-margin*2])

    width_diff_ax = width_mean_ax.twinx()
    height_diff_ax = height_mean_ax.twiny()

    width_mean_ax.plot(np.arange(bin_map.shape[0]), np.mean(bin_map, axis=0) / 255, color="blue")
    height_mean_ax.plot(np.mean(bin_map, axis=1) / 255, np.arange(bin_map.shape[1]), color="blue")

    width_diff_ax.plot(np.arange(width_diff.shape[0]), width_diff, color="orange")
    height_diff_ax.plot(height_diff, np.arange(height_diff.shape[0]), color="orange")
    
    width_mean_ax.set_xlim([0, bin_map.shape[0]])
    height_mean_ax.set_ylim([bin_map.shape[1], 0])
    width_diff_ax.set_xlim([0, bin_map.shape[0]])
    height_diff_ax.set_ylim([bin_map.shape[1], 0])

    width_mean_ax.yaxis.tick_right()
    height_mean_ax.xaxis.tick_bottom()
    width_mean_ax.xaxis.tick_bottom()
    height_mean_ax.yaxis.tick_right()

    width_diff_ax.yaxis.tick_left()
    height_diff_ax.xaxis.tick_top()
    # # width_diff_ax.xaxis.tick_top()
    # # height_diff_ax.yaxis.tick_left()

    width_mean_ax.grid()
    height_mean_ax.grid()

    width_mean_ax.set_ylim([0, 1])
    height_mean_ax.set_xlim([0, 1])

    width_diff_ax.set_ylim([-10, 10])
    height_diff_ax.set_xlim([-10, 10])

    width_mean_ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    height_mean_ax.set_xticks([0, 0.25, 0.5, 0.75, 1])

    image_ax.imshow(bin_map)
    plt.show(block=False)
    input()
