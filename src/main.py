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
    relative_plot
)

if __name__=='__main__':
    path = "../images/large/image01.pgm"
    bitmap = im2bitmap(path2im(path))
