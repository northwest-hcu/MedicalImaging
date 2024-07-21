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
    get_peaks,
    fix_wave,
    create_mask
)
from graph import (
    bitmap_plot,
    wave_plot,
    relative_plot
)
import numpy as np

if __name__=='__main__':
    path = "../../images/large/image04.pgm"
    bitmap = im2bitmap(path2im(path))
    # border = np.mean(bitmap)
    border = np.max(bitmap) - np.std(bitmap)
    filtered_bitmap = filter_bitmap(bitmap, border=int(border))
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
    left_wave_left_peaks, left_wave_right_peaks = get_peaks(
        # 左側は上が小さくなるので反転させる
        np.asarray([(left_wave.shape[0] - 1) - bit for bit in left_wave])
    )
    # 左側は波形が90度傾くのでx軸とy軸を入れ替える
    left_ax.plot(
        [left_wave[peak] for peak in left_wave_left_peaks],
        left_wave_left_peaks
    )
    left_ax.plot(
        [left_wave[peak] for peak in left_wave_right_peaks],
        left_wave_right_peaks
    )
    left_ax.plot(
        (np.min(left_wave), np.min(left_wave)),
        (left_wave_left_peaks[-1], left_wave_right_peaks[0])
    )
    # 右側の波形の補助線
    right_wave_left_peaks, right_wave_right_peaks = get_peaks(
        right_wave
    )
    # 右側は波形が90度傾くのでx軸とy軸を入れ替える
    right_ax.plot(
        [right_wave[peak] for peak in right_wave_left_peaks],
        right_wave_left_peaks
    )
    right_ax.plot(
        [right_wave[peak] for peak in right_wave_right_peaks],
        right_wave_right_peaks
    )
    right_ax.plot(
        (np.max(right_wave), np.max(right_wave)),
        (right_wave_left_peaks[-1], right_wave_right_peaks[0])
    )
    # 上側の波形の補助線
    top_wave_left_peaks, top_wave_right_peaks = get_peaks(
        # 上側は上が小さくなるので反転させる
        np.asarray([(top_wave.shape[0] - 1) - bit for bit in top_wave])
    )
    top_ax.plot(
        top_wave_left_peaks,
        [top_wave[peak] for peak in top_wave_left_peaks]
    )
    top_ax.plot(
        top_wave_right_peaks,
        [top_wave[peak] for peak in top_wave_right_peaks]
    )
    top_ax.plot(
        (top_wave_left_peaks[-1], top_wave_right_peaks[0]),
        (np.min(top_wave), np.min(top_wave))
    )
    # 下側の波形の補助線
    bottom_wave_left_peaks, bottom_wave_right_peaks = get_peaks(
        bottom_wave
    )
    bottom_ax.plot(
        bottom_wave_left_peaks,
        [bottom_wave[peak] for peak in bottom_wave_left_peaks]
    )
    bottom_ax.plot(
        bottom_wave_right_peaks,
        [bottom_wave[peak] for peak in bottom_wave_right_peaks]
    )
    bottom_ax.plot(
        (bottom_wave_left_peaks[-1], bottom_wave_right_peaks[0]),
        (np.max(bottom_wave), np.max(bottom_wave))
    )
    # 補助線と波形の結合（上）
    left_wave = np.asarray([
        left_wave.shape[0] - 1 - bit 
        for bit in
        fix_wave(
            np.asarray([
                left_wave.shape[0] - 1 - bit 
                for bit in left_wave
            ]), 
            left_wave_left_peaks, 
            left_wave_right_peaks
        )
    ])
    right_wave = fix_wave(right_wave, right_wave_left_peaks, right_wave_right_peaks)
    top_wave = np.asarray([
        top_wave.shape[0] - 1 - bit 
        for bit in
        fix_wave(
            np.asarray([
                top_wave.shape[0] - 1 - bit 
                for bit in top_wave
            ]), 
            top_wave_left_peaks, 
            top_wave_right_peaks
        )
    ])
    bottom_wave = fix_wave(bottom_wave, bottom_wave_left_peaks, bottom_wave_right_peaks)
    
    image_ax, left_ax, right_ax, top_ax, bottom_ax = relative_plot(
        bitmap,
        left_wave,
        right_wave,
        top_wave,
        bottom_wave
    )

    mask_bitmap = create_mask(
        left_wave,
        right_wave,
        top_wave,
        bottom_wave
    )

    masked_bitmap = bitmap * mask_bitmap
    # 最低値に合わせる
    # black = np.min(bitmap) + np.std(bitmap) / 10
    black = np.min(bitmap)
    masked_bitmap = np.where(masked_bitmap == 0, black, masked_bitmap)
    bitmap_plot(masked_bitmap)

    # グラフが閉じないように待機
    input()


