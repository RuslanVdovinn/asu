"""
Интерактивный подбор HSV-диапазона для выделения объекта.
Запуск: python trackbars.py <путь_к_изображению>
Пример: python trackbars.py bus.jpg
"""

import sys
import cv2
import numpy as np
from PIL import Image


def nothing(x):
    """Заглушка для трекбаров"""
    pass


def main():
    # --- 1. Проверяем аргументы командной строки ---
    if len(sys.argv) < 2:
        print("Использование: python trackbars.py <путь_к_изображению>")
        print("Пример:        python trackbars.py bus.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    img = cv2.imread(image_path)
    rgb = False
    if img is None:
        img = np.array(Image.open(image_path))
        rgb = True

    if img is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        print("Проверьте путь и формат файла (JPEG, PNG, BMP...).")
        sys.exit(1)

    print(f"Изображение загружено: {image_path}")
    print(f"Размер: {img.shape[1]} × {img.shape[0]} пикселей")
    print()
    print("Двигайте ползунки, чтобы подобрать диапазон HSV.")
    print("Нажмите ESC для выхода.")
    print()

    if rgb:
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    else:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('Trackbars', cv2.WINDOW_NORMAL)
    # cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Mask',     cv2.WINDOW_NORMAL)
    # cv2.namedWindow('Result',   cv2.WINDOW_NORMAL)

    cv2.resizeWindow('Trackbars', 1000, 200)
    # cv2.resizeWindow('Original',  640, 480)
    cv2.resizeWindow('Mask',      800, 640)
    # cv2.resizeWindow('Result',    800, 640)

    # hue: 0-179
    cv2.createTrackbar('H_min', 'Trackbars', 0,   179, nothing)
    cv2.createTrackbar('H_max', 'Trackbars', 179, 179, nothing)
    # saturation: 0-255
    cv2.createTrackbar('S_min', 'Trackbars', 0,   255, nothing)
    cv2.createTrackbar('S_max', 'Trackbars', 255, 255, nothing)
    # value (яркость): 0-255
    cv2.createTrackbar('V_min', 'Trackbars', 0,   255, nothing)
    cv2.createTrackbar('V_max', 'Trackbars', 255, 255, nothing)

    while True:
        h_min = cv2.getTrackbarPos('H_min', 'Trackbars')
        h_max = cv2.getTrackbarPos('H_max', 'Trackbars')
        s_min = cv2.getTrackbarPos('S_min', 'Trackbars')
        s_max = cv2.getTrackbarPos('S_max', 'Trackbars')
        v_min = cv2.getTrackbarPos('V_min', 'Trackbars')
        v_max = cv2.getTrackbarPos('V_max', 'Trackbars')

        # создаём маску
        low  = np.array([h_min, s_min, v_min], dtype=np.uint8)
        high = np.array([h_max, s_max, v_max], dtype=np.uint8)
        mask = cv2.inRange(hsv, low, high)

        # применяем маску к оригиналу
        # result = cv2.bitwise_and(img, img, mask=mask)

        # cv2.imshow('Original', img)
        cv2.imshow('Mask', mask)
        # cv2.imshow('Result', result)

        # выход по ESC
        key = cv2.waitKey(1) & 0xFF
        if key == 27:   # 27 = Esc
            break
        # выход по 'q'
        if key == ord('q'):
            break

    # итоговые значения
    print("=" * 50)
    print("Подобранный диапазон HSV:")
    print(f"color_low = ({h_min}, {s_min}, {v_min})")
    print(f"color_high = ({h_max}, {s_max}, {v_max})")
    print()
    print("Готовый код для вставки:")
    print(f"color_low = np.array([{h_min}, {s_min}, {v_min}])")
    print(f"color_high = np.array([{h_max}, {s_max}, {v_max}])")
    print(f"mask = cv2.inRange(hsv, color_low, color_high)")
    print("=" * 50)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()