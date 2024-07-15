from tool import (
    # Bit,
    Wave,
    Bitmap,
    Direction,
    WIDTH_DIRECTION,
    HEIGHT_DIRECTION,
    path2im,
    im2bitmap,
    bitmap2im,
    bitmap2wave,
    filter_bitmap,
    get_peaks
)
from graph import (
    bitmap_plot,
    wave_plot,
    relative_plot
)
import numpy as np

if __name__=='__main__':
    path = "../images/large/image04.pgm"
    bitmap = im2bitmap(path2im(path))
    filtered_bitmap = filter_bitmap(bitmap)
    # bitmap_plot(filtered_bitmap)
    left_wave = bitmap2wave(filtered_bitmap, direction='LEFT')
    right_wave = bitmap2wave(filtered_bitmap, direction='RIGHT')
    top_wave = bitmap2wave(filtered_bitmap, direction='TOP')
    bottom_wave = bitmap2wave(filtered_bitmap, direction='BOTTOM')
    image_ax, left_ax, right_ax, top_ax, bottom_ax = relative_plot(
        filtered_bitmap,
        left_wave,
        right_wave,
        top_wave,
        bottom_wave
    )
    # 左側の波形の補助線
    left_wave_left_peak, left_wave_right_peak = get_peaks(
        # 左側は上が小さくなるので反転させる
        np.asarray([(left_wave.shape[0] - 1) - bit for bit in left_wave])
    )
    left_wave_peaks = np.asarray([left_wave_left_peak, left_wave_right_peak])
    # 左側は波形が90度傾くのでx軸とy軸を入れ替える
    left_ax.plot(
        [left_wave[peak] for peak in left_wave_peaks],
        left_wave_peaks
    )
    # 右側の波形の補助線
    right_wave_left_peak, right_wave_right_peak = get_peaks(
        right_wave
    )
    right_wave_peaks = np.asarray([right_wave_left_peak, right_wave_right_peak])
    # 右側は波形が90度傾くのでx軸とy軸を入れ替える
    right_ax.plot(
        [right_wave[peak] for peak in right_wave_peaks],
        right_wave_peaks
    )
    # 上側の波形の補助線
    top_wave_left_peak, top_wave_right_peak = get_peaks(
        # 上側は上が小さくなるので反転させる
        np.asarray([(top_wave.shape[0] - 1) - bit for bit in top_wave])
    )
    top_wave_peaks = np.asarray([top_wave_left_peak, top_wave_right_peak])
    top_ax.plot(
        top_wave_peaks,
        [top_wave[peak] for peak in top_wave_peaks]
    )
    # 下側の波形の補助線
    bottom_wave_left_peak, bottom_wave_right_peak = get_peaks(
        bottom_wave
    )
    bottom_wave_peaks = np.asarray([bottom_wave_left_peak, bottom_wave_right_peak])
    bottom_ax.plot(
        bottom_wave_peaks,
        [bottom_wave[peak] for peak in bottom_wave_peaks]
    )

    
    # グラフが閉じないように待機
    input()


