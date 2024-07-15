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
    relative_plot
)

if __name__=='__main__':
    path = "../images/large/image04.pgm"
    bitmap = im2bitmap(path2im(path))
    filtered_bitmap = filter_bitmap(bitmap)
    bitmap_plot(filtered_bitmap)
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
    input()


