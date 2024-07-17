from graph import (
    bitmap_plot
)
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

import cv2
import numpy as np

# 画像の読み込み
image = cv2.imread("../images/large/image04.pgm")

# グレースケール変換
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ノイズ除去 (ガウシアンフィルタ)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 二値化 (大津の二値化)
ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 輪郭抽出
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 輪郭の描画
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# 結果の表示
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

bitmap_plot(
    im2bitmap(image)
)
input()