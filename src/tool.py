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
def get_peaks(wave: Wave) -> tuple[Bit]:
    wave_length = wave.shape[0]
    # 左からの波形
    left_side_wave = wave.copy()
    # 右からの波形
    right_side_wave = wave.copy()
    right_side_wave = np.flip(right_side_wave)
    # 左からの波形のpeak地点の初期化
    left_side_peak = wave_length - 1
    # 右からの波形のpeak地点の初期化
    right_side_peak = wave_length - 1
    
    left_side_diff = np.diff(left_side_wave)
    left_side_peak = np.argmax(left_side_diff < 0)
    right_side_diff = np.diff(right_side_wave)
    right_side_peak = np.argmax(right_side_diff < 0)

    right_side_peak = (wave_length - 1) - right_side_peak
    return left_side_peak, right_side_peak

def fix_wave(wave: Wave, left_peak: Bit, right_peak: Bit) -> Wave:
    rate = (wave[right_peak] - wave[left_peak]) / right_peak - left_peak
    peak_range = np.arange(left_peak, right_peak + 1, 1, dtype=np.int16)
    peak_range = peak_range * rate + wave[left_peak]
    print(wave[left_peak], wave[right_peak], rate)
    peak_wave = [
        bit
        if i < left_peak or i > right_peak 
        else int(peak_range[i - left_peak])
        for i, bit in enumerate(wave)]
    peak_wave = np.asarray(peak_wave)
    return peak_wave