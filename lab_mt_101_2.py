import cv2
import numpy as np


def load_image(image_path):
    image = cv2.imread(image_path)
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image


# Преобразование в полутоновое изображение
def to_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale Image", gray_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return gray_image


# Бинаризация с ручным выбором порога
def manual_threshold(image, lower, upper=None, range_threshold=False):
    if range_threshold:
        binary = cv2.inRange(image, lower, upper)
    else:
        _, binary = cv2.threshold(image, lower, 255, cv2.THRESH_BINARY)
    cv2.imshow("Manual Threshold", binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return binary


# Глобальная бинаризация методом Оцу
def otsu_global_threshold(image):
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("Otsu Global Threshold", binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return binary


# Локальная бинаризация методом Оцу с разбиением на фрагменты
def otsu_local_threshold(image, grid_size=16):
    h, w = image.shape
    binary = np.zeros((h, w), dtype=np.uint8)
    for y in range(0, h, grid_size):
        for x in range(0, w, grid_size):
            block = image[y:y + grid_size, x:x + grid_size]
            _, block_thresh = cv2.threshold(block, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            binary[y:y + grid_size, x:x + grid_size] = block_thresh
    cv2.imshow("Otsu Local Threshold", binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return binary


# Иерархическая бинаризация методом Оцу
def otsu_hierarchical_threshold(image, min_size=16):
    def recursive_otsu(img):
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        h, w = img.shape
        if h > min_size and w > min_size:
            top_left = recursive_otsu(img[:h // 2, :w // 2])
            top_right = recursive_otsu(img[:h // 2, w // 2:])
            bottom_left = recursive_otsu(img[h // 2:, :w // 2])
            bottom_right = recursive_otsu(img[h // 2:, w // 2:])
            return np.vstack((np.hstack((top_left, top_right)), np.hstack((bottom_left, bottom_right))))
        return binary

    binary_hierarchical = recursive_otsu(image)
    cv2.imshow("Otsu Hierarchical Threshold", binary_hierarchical)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return binary_hierarchical


# Функция квантования по яркости
def quantize_image(image, num_levels):
    # Находим интервал для каждого уровня
    level_interval = 256 // num_levels
    quantized_image = (image // level_interval) * level_interval
    cv2.imshow(f"Quantized Image - {num_levels} Levels", quantized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return quantized_image


if __name__ == "__main__":
    image_path = "images.jpg"
    image = load_image(image_path)
    gray_image = to_grayscale(image)

    # Ручная бинаризация
    manual_binary = manual_threshold(gray_image, lower=127)

    # Глобальная бинаризация методом Оцу
    otsu_global = otsu_global_threshold(gray_image)

    # Локальная бинаризация методом Оцу
    otsu_local = otsu_local_threshold(gray_image, grid_size=16)

    # Иерархическая бинаризация методом Оцу
    otsu_hierarchical = otsu_hierarchical_threshold(gray_image)

    # Квантование по яркости
    num_levels = 8  # Количество уровней квантования
    quantized_image = quantize_image(image, num_levels)
