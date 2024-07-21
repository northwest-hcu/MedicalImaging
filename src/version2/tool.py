from PIL import Image
import numpy as np
from typing import TypeAlias, Literal

Bit: TypeAlias = int # 0 < bit < 255
Wave: TypeAlias = np.ndarray[Bit]
Bitmap: TypeAlias = np.ndarray[Wave]
Direction: TypeAlias = Literal['LEFT', 'RIGHT', 'TOP', 'BOTTOM']

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

def bitmap2wave(bitmap: Bitmap, direction: Direction='LEFT') -> Wave:
    bm = bitmap.copy()
    if direction == 'LEFT':
        axis = WIDTH_DIRECTION
    elif direction == 'RIGHT':
        axis = WIDTH_DIRECTION
        bm = np.fliplr(bm)
    elif direction == 'TOP':
        axis = HEIGHT_DIRECTION
    elif direction == 'BOTTOM':
        axis = HEIGHT_DIRECTION
        bm = np.flipud(bm)
    # 黒い箇所があるか
    hit = np.any(bm == 0, axis=axis)
    # 最初に黒い部分に当たった位置
    peaks = np.argmax(bm == 0, axis=axis)
    # 波形のリスト 0～(サイズ - 1)
    wave = np.asarray([
                peak if h else bm.shape[axis] - 1 
                for peak, h in zip(peaks, hit)
            ])
    if direction == 'RIGHT':
        # wave = np.flip(wave)
        wave = np.asarray([(bitmap.shape[axis] - 1) - bit for bit in wave])
    if direction == 'BOTTOM':
        wave = np.asarray([(bitmap.shape[axis] - 1) - bit for bit in wave])
    return wave

# 2値化関数
def filter_bitmap(bitmap: Bitmap, border: int = int(255 / 2)) -> Bitmap:
    filtered_bitmap = np.where(bitmap < border, 0, 255)
    return filtered_bitmap

# 波形解析 山の頂点を取得
def get_peaks(wave: Wave) -> tuple[list[Bit]]:
    wave_length = wave.shape[0]
    maximum = np.max(wave)
    # 左からの波形
    left_side_wave = wave.copy()
    # 右からの波形
    right_side_wave = wave.copy()
    right_side_wave = np.flip(right_side_wave)
    left_side_peak = 0
    right_side_peak = 0
    # 左からの波形の上がっている部分を取得
    left_side_peaks = []
    for i in range(wave_length):
        if left_side_wave[i] > left_side_peak:
            left_side_peak = left_side_wave[i]
            left_side_peaks.append(i)
        if left_side_wave[i] == maximum:
            break
    # 右からの波形の上がっている部分を取得
    right_side_peaks = []
    for i in range(wave_length):
        if right_side_wave[i] > right_side_peak:
            right_side_peak = right_side_wave[i] 
            right_side_peaks.append(i)
        if right_side_wave[i] == maximum:
            break

    # 右からの波形は反転しているためもう一度反転させる
    right_side_peaks = [(wave_length - 1) - right_side_peak for right_side_peak in right_side_peaks]
    right_side_peaks = np.flip(right_side_peaks)

    return left_side_peaks, right_side_peaks

def cut_threshold(value: int, maximum: int, minimum: int=0) -> int:
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value

def get_mid_range(wave: Wave, peaks: list[Bit]) -> list[Bit]:
    peaks_wave = np.zeros(wave.shape[0], dtype=np.int16)
    for i in range(wave.shape[0]):
        if i in peaks:
            peaks_wave[i] = wave[i]
        elif peaks[-1] >= i:
            start, end = get_span(i, peaks)
            if (end - start) == 0:
                peaks_wave[i] = wave[i]
                continue
            rate = (wave[end] - wave[start]) / (end - start)
            peaks_wave[i] = cut_threshold(int((i - start) * rate + wave[start]), wave.shape[0])
    return peaks_wave

def get_span(index: int, peaks: list[Bit]) -> tuple[Bit]:
    for i in range(len(peaks)):
        if peaks[i] > index:
            return peaks[i - 1], peaks[i]

def fix_wave(wave: Wave, left_side_peaks: list[Bit], right_side_peaks: list[Bit]) -> Wave:
    wave_length = wave.shape[0]
    max_value = np.max(wave)
    left_side_peaks_wave = get_mid_range(wave, left_side_peaks)
    right_side_peaks_wave = get_mid_range(wave, right_side_peaks)
    # 無波形領域 -> 右肩上がり領域 -> 上辺領域 -> 右肩下がり領域 -> 無波形領域
    peak_wave = np.zeros(wave_length, dtype=np.int16)
    for i in range(wave_length):
        # 右肩上がり領域
        if i >= left_side_peaks[0] and i <= left_side_peaks[-1]:
            peak_wave[i] = left_side_peaks_wave[i]
        # 上辺領域
        if i >= left_side_peaks[-1] and i <= right_side_peaks[0]:
            peak_wave[i] = max_value
        # 右肩下がり領域
        if i >= right_side_peaks[0] and i <= right_side_peaks[-1]:
            peak_wave[i] = right_side_peaks_wave[i]
    peak_wave = np.asarray(peak_wave)
    return peak_wave

def create_mask(left_wave: Wave, right_wave: Wave, top_wave: Wave, bottom_wave: Wave) -> Bitmap:
    mask_bitmap = np.ones((left_wave.shape[0], top_wave.shape[0]), dtype=np.int16)
    for i, bit in enumerate(left_wave):
        try:
            mask_bitmap[i, 0:bit] = 0
        except Exception as err:
            print(err)
            print(i, bit)
    for i, bit in enumerate(right_wave):
        mask_bitmap[i, bit:top_wave.shape[0] - 1] = 0
    for i, bit in enumerate(top_wave):
        mask_bitmap[0:bit, i] = 0
    for i, bit in enumerate(bottom_wave):
        mask_bitmap[bit:left_wave.shape[0] - 1, i] = 0
    return mask_bitmap

def move_mean(wave: Wave, size: int=10) -> Wave:
    ones = np.ones(size) / size
    mean_wave = np.convolve(wave, ones, mode="same")
    mean_wave = np.asarray([int(bit + 0.5) for bit in mean_wave])
    return mean_wave