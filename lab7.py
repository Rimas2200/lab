import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class Matrix:
    def __init__(self, data):
        self.data = data

    def load_from_bmp(self, filename):
        image = Image.open(filename).convert('L')
        self.data = np.array(image)

    def show_image(self):
        plt.imshow(self.data, cmap='gray')
        plt.axis('off')
        plt.show()

    def binarize(self, threshold=127):
        self.data = np.where(self.data >= threshold, 255, 0)

    def apply_boundary_extraction(self):
        height, width = self.data.shape
        boundary_matrix = np.zeros((height, width), dtype=np.uint8)

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                if self.data[i, j] == 0:
                    if (
                        self.data[i-1, j-1] == 255 or
                        self.data[i-1, j] == 255 or
                        self.data[i-1, j+1] == 255 or
                        self.data[i, j-1] == 255 or
                        self.data[i, j+1] == 255 or
                        self.data[i+1, j-1] == 255 or
                        self.data[i+1, j] == 255 or
                        self.data[i+1, j+1] == 255
                    ):
                        boundary_matrix[i, j] = 255

        self.data = boundary_matrix

# Создаем объект класса Matrix
matrix = Matrix(None)

# Файл с мудла
matrix.load_from_bmp('lena1_1.bmp')

# Отображаем исходное изображение
matrix.show_image()

# Преобразуем и отображаем бинарную матрицу
matrix.binarize()
matrix.show_image()

# Выделяем(если можно так сказать) границы
matrix.apply_boundary_extraction()

# Отображаем полученную матрицу границы
matrix.show_image()