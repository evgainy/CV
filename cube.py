import cv2
import numpy as np
from sys import argv


Color = list[np.uint8, np.uint8, np.uint8]
Coord = tuple[int, int]


def get_RGB(high: int, img_size: int, coord: Coord) -> Color:
    """Определение цвета пикселя"""

    mid = img_size / 2
    scale = 255 / (img_size/3**0.5)

    r_shift = get_r_shift(mid, coord)
    r_val = get_color_with_shift(high, r_shift, scale)
    if r_val > 255 or r_val < 0:
        return np.zeros(3, dtype=np.uint8)

    g_shift = get_g_shift(mid, coord)
    g_val = get_color_with_shift(high, g_shift, scale)
    if g_val > 255 or g_val < 0:
        return np.zeros(3, dtype=np.uint8)

    b_shift = get_b_shift(mid, coord)
    b_val = get_color_with_shift(high, b_shift, scale)
    if b_val > 255 or b_val < 0:
        return np.zeros(3, dtype=np.uint8)

    return np.array([b_val, g_val, r_val])


def get_r_shift(mid: int, coord: Coord) -> int:
    """Сдвиг от центра в красном направлении"""
    axis_shift = mid + -(coord[0] + 3**0.5 * coord[1] + mid*(1 - 3**0.5)) / 2

    return axis_shift


def get_g_shift(mid: int, coord: Coord) -> int:
    """Сдвиг от чентра в зеленом направлении"""
    axis_shift = mid + (-coord[0] + 3**0.5 * coord[1] - mid*(1 + 3**0.5)) / 2

    return axis_shift


def get_b_shift(mid: int, coord: Coord) -> int:
    """Сдвиг от центра в синем направлении"""
    axis_shift = coord[0] - mid

    return axis_shift


def get_color_with_shift(high, shift, scale) -> int:
    """Определение значимости цвета по сдвигу"""
    mid_val = high / 3**0.5

    pixel_val = mid_val + shift * scale / 1.5**0.5

    return pixel_val


if __name__ == '__main__':
    high = int(argv[1])
    img_size = 201

    display = np.zeros((img_size, img_size, 3), np.uint8)

    for i in np.arange(img_size):
        for j in np.arange(img_size):
            display[i, j] = get_RGB(high=high, img_size=img_size, coord=(i, j))

    cv2.imwrite(f'data/cube/cube_u={high}.png', display)
