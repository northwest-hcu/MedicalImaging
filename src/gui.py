import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np

from typing import TypeAlias

Bitmap: TypeAlias = np.ndarray[np.ndarray[int]]
WIDTH_DIRECTION = 1
HEIGHT_DIRECTION = 0

def im_plot(bitmap: Bitmap, title: str="default") -> plt.Figure:
    fig = plt.figure(title, figsize=(8, 8))
    image_ax = fig.add_axes((0, 0, 1, 1))
    plt.set_cmap('binary_r')
    image_ax.imshow(bitmap)
    plt.show(block=False)
    return fig

def all_plot(
    bitmap: Bitmap,
    left_axis_data: np.ndarray[float],
    right_axis_data: np.ndarray[float],
    top_axis_data: np.ndarray[float],
    bottom_axis_data: np.ndarray[float],
    margin:float=0.05,
    title: str="window title") -> (plt.Figure, Axes, Axes, Axes, Axes):
    fig = plt.figure(title, figsize=(8, 8))
    image_ax = fig.add_axes((0.3+margin, 0.4-margin, 0.3, 0.3))
    image_ax.set_xticks([])
    image_ax.set_yticks([])
    plt.set_cmap('binary_r')
    left_axis = fig.add_axes((0+margin, 0.4-margin, 0.3, 0.3))
    right_axis = fig.add_axes((0.6+margin, 0.4-margin, 0.3, 0.3))
    top_axis = fig.add_axes((0.3+margin, 0.7-margin, 0.3, 0.3))
    bottom_axis = fig.add_axes((0.3+margin, 0.1-margin, 0.3, 0.3))

    left_axis.plot(left_axis_data, np.arange(bitmap.shape[HEIGHT_DIRECTION]), color='blue')
    right_axis.plot(right_axis_data, np.arange(bitmap.shape[HEIGHT_DIRECTION]), color='blue')
    top_axis.plot(np.arange(bitmap.shape[WIDTH_DIRECTION]), top_axis_data, color='blue')
    bottom_axis.plot(np.arange(bitmap.shape[WIDTH_DIRECTION]), bottom_axis_data, color='blue')

    left_axis.set_xlim([0, bitmap.shape[WIDTH_DIRECTION]])
    left_axis.set_ylim([bitmap.shape[HEIGHT_DIRECTION], 0])
    right_axis.set_xlim([0, bitmap.shape[WIDTH_DIRECTION]])
    right_axis.set_ylim([bitmap.shape[HEIGHT_DIRECTION], 0])
    top_axis.set_xlim([0, bitmap.shape[WIDTH_DIRECTION]])
    top_axis.set_ylim([bitmap.shape[HEIGHT_DIRECTION], 0])
    bottom_axis.set_xlim([0, bitmap.shape[WIDTH_DIRECTION]])
    bottom_axis.set_ylim([bitmap.shape[HEIGHT_DIRECTION], 0])

    left_axis.set_xticks([])
    left_axis.set_yticks([])
    right_axis.set_xticks([])
    right_axis.set_yticks([])
    # top_axis.set_xticks([])
    # top_axis.set_yticks([])
    # bottom_axis.set_xticks([])
    # bottom_axis.set_yticks([])

    image_ax.imshow(bitmap)
    plt.show(block=False)
    return fig, left_axis, right_axis, top_axis, bottom_axis


def plot(bin_map: np.ndarray[np.ndarray], width_axes: np.ndarray[float|int], height_axes: np.ndarray[float|int], margin:float=0.05, title: str="window title"):
    fig = plt.figure(title, figsize=(8, 8))
    image_ax = fig.add_axes((0+margin, 0.3+margin, 0.7-margin*2, 0.7-margin*2))
    image_ax.set_xticks([])
    image_ax.set_yticks([])
    plt.set_cmap('binary_r')

    width_mean_ax = fig.add_axes([0+margin, 0+margin, 0.7-margin*2, 0.3-margin*2])
    height_mean_ax = fig.add_axes([0.7+margin, 0.3+margin, 0.3-margin*2, 0.7-margin*2])

    # width_diff_ax = width_mean_ax.twinx()
    # height_diff_ax = height_mean_ax.twiny()

    width_mean_ax.plot(np.arange(bin_map.shape[0]), width_axes, color="blue")
    height_mean_ax.plot(height_axes, np.arange(bin_map.shape[1]), color="blue")

    # width_diff_ax.plot(np.arange(width_diff.shape[0]), width_diff, color="orange")
    # height_diff_ax.plot(height_diff, np.arange(height_diff.shape[0]), color="orange")
    
    width_mean_ax.set_xlim([0, bin_map.shape[0]])
    height_mean_ax.set_ylim([bin_map.shape[1], 0])
    # width_diff_ax.set_xlim([0, bin_map.shape[0]])
    # height_diff_ax.set_ylim([bin_map.shape[1], 0])

    width_mean_ax.yaxis.tick_right()
    height_mean_ax.xaxis.tick_bottom()
    width_mean_ax.xaxis.tick_bottom()
    height_mean_ax.yaxis.tick_right()

    # width_diff_ax.yaxis.tick_left()
    # height_diff_ax.xaxis.tick_top()
    # # width_diff_ax.xaxis.tick_top()
    # # height_diff_ax.yaxis.tick_left()

    width_mean_ax.grid()
    height_mean_ax.grid()

    # width_mean_ax.set_ylim([0, 1])
    # height_mean_ax.set_xlim([0, 1])

    # width_diff_ax.set_ylim([-10, 10])
    # height_diff_ax.set_xlim([-10, 10])

    # width_mean_ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    # height_mean_ax.set_xticks([0, 0.25, 0.5, 0.75, 1])

    image_ax.imshow(bin_map)
    plt.show(block=False)
