from tool import (
    # Bit,
    Wave,
    Bitmap,
    Direction,
    WIDTH_DIRECTION,
    HEIGHT_DIRECTION,
)
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np

# 画像の描画
def bitmap_plot(bitmap: Bitmap, ax: Axes=None, title: str="Window Title") -> None:
    if ax is None:
        fig = plt.figure(title, figsize=(8, 8))
        ax = fig.add_axes((0, 0, 1, 1))
    ax.imshow(bitmap, cmap='binary_r')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show(block=False)

# 波形の描画
def wave_plot(wave: Wave, ax: Axes=None, title: str="Window Title", transpose: bool=False) -> None:
    if ax is None:
        fig = plt.figure(title, figsize=(8, 8))
        ax = fig.add_axes((0, 0, 1, 1))
    if transpose:
        ax.plot(wave, np.arange(0, wave.shape[0]))
    else:
        ax.plot(np.arange(0, wave.shape[0]), wave)
    ax.set_xlim([0, wave.shape[0]])
    ax.set_ylim([wave.shape[0], 0])
    ax.set_xticks(np.arange(0, wave.shape[0], 300))
    ax.set_yticks(np.arange(0, wave.shape[0], 300))
    ax.set_aspect('equal')
    ax.xaxis.tick_top()
    ax.grid(True)
    plt.show(block=False)

# ++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++TTTTTTTTTTTT++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# +LLLLLLLLLLLL+IIIIIIIIIIII+RRRRRRRRRRRR+
# ++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++BBBBBBBBBBBB++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++

# 1単位: 0.025, +: 余白, T: Top, L: Left, I: 画像, R: Right, B: Bottom
# x軸要素は左から右, y軸要素は下から上

# 画像の4方向成分の描画
def relative_plot(
        bitmap: Bitmap, 
        left_wave: Wave, 
        right_wave: Wave, 
        top_wave: Wave, 
        bottom_wave: Wave,
        title: str | None=None,
        margin: float=0.025
    ) -> tuple[Axes, Axes, Axes, Axes, Axes]:
    fig = plt.figure(title, figsize=(8, 8))
    fig.tight_layout()
    image_ax = fig.add_subplot(3, 3, 5)
    left_ax = fig.add_subplot(3, 3, 4)
    right_ax = fig.add_subplot(3, 3, 6)
    top_ax = fig.add_subplot(3, 3, 2)
    bottom_ax = fig.add_subplot(3, 3, 8)
    bitmap_plot(bitmap, ax=image_ax)
    wave_plot(left_wave, ax=left_ax, transpose=True)
    wave_plot(right_wave, ax=right_ax, transpose=True)
    wave_plot(top_wave, ax=top_ax)
    wave_plot(bottom_wave, ax=bottom_ax)

    return image_ax, left_ax, right_ax, top_ax, bottom_ax
