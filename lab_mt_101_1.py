# -*- coding: utf-8 -*-
import cv2
import numpy as np


# 1. Загрузка изображения
def load_image(image_path):
    image = cv2.imread(image_path)
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image


# 2. Цветовая коррекция изображений
# 2.1 Коррекция с опорным цветом
def reference_color_correction(image, reference_color):
    correction_factors = np.array(reference_color, dtype=np.float32) / 255.0
    corrected_image = image.astype(np.float32) * correction_factors.reshape(1, 1, 3)
    corrected_image = np.clip(corrected_image, 0, 255).astype(np.uint8)
    return corrected_image


# 2.2 Метод серого мира
def gray_world_correction(image):
    avg_r = image[:, :, 2].mean()
    avg_g = image[:, :, 1].mean()
    avg_b = image[:, :, 0].mean()
    avg_gray = (avg_r + avg_g + avg_b) / 3
    correction_factors = (avg_gray / avg_r, avg_gray / avg_g, avg_gray / avg_b)
    corrected_image = image.copy().astype(np.float32)
    corrected_image[:, :, 2] *= correction_factors[0]
    corrected_image[:, :, 1] *= correction_factors[1]
    corrected_image[:, :, 0] *= correction_factors[2]
    corrected_image = np.clip(corrected_image, 0, 255).astype(np.uint8)
    return corrected_image


# 2.3 По виду функции преобразования
def custom_transform_correction(image, transform_function):
    if image.shape[-1] == 3:
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    else:
        image_bgr = image
    corrected_image_bgr = np.zeros_like(image_bgr)
    for i in range(3):
        corrected_image_bgr[:, :, i] = transform_function(image_bgr[:, :, i])
    corrected_image_rgb = cv2.cvtColor(corrected_image_bgr, cv2.COLOR_BGR2RGB)
    return corrected_image_rgb


# 4. Коррекция на основе гистограммы
# 4.1 Нормализация гистограммы
def histogram_normalization(image):
    normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    return normalized_image


# 4.2 Эквализация гистограммы
def histogram_equalization(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    return equalized_image


def main():
    image_path = "images.jpg"
    image = load_image(image_path)

    reference_color = [250, 200, 200]
    ref_corrected = reference_color_correction(image, reference_color)
    cv2.imshow("Correction with reference color", ref_corrected)
    cv2.waitKey(0)

    gray_world_image = gray_world_correction(image)
    cv2.imshow("Gray World Method", gray_world_image)
    cv2.waitKey(0)

    def transform_function(channel):
        return cv2.normalize(channel, None, 0, 255, cv2.NORM_MINMAX)

    normalized_image = custom_transform_correction(image, transform_function)
    cv2.imshow("Custom Transform Correction", normalized_image)
    cv2.waitKey(0)

    # Коррекция на основе гистограммы
    normalized_image = histogram_normalization(image)
    cv2.imshow("Histogram Normalization", normalized_image)
    cv2.waitKey(0)

    equalized_image = histogram_equalization(image)
    cv2.imshow("Histogram Equalization", equalized_image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
