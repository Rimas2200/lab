import numpy as np
import pygame

class Vector:
    def __init__(self, start_point, x, y):
        self.start_point = start_point  # начальная точка вектора
        self.end_point = np.array([start_point[0] + x, start_point[1] + y], dtype=np.float32)  # конечная точка вектора

    def drawVector(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.start_point, self.end_point.astype(int), 2)  # линия вектора

        # стрелка
        arrow_size = 10
        direction = self.end_point - self.start_point  # направление вектора
        norm = np.linalg.norm(direction)  # норма вектора
        if norm != 0:
            direction /= norm
            arrow_point = self.end_point - direction * arrow_size  # конечная точка стрелки
            perpendicular = np.array([-direction[1], direction[0]], dtype=np.float32)  # перпендикуляр к направлению вектора
            arrow_left = arrow_point + perpendicular * arrow_size  # левая точка стрелки
            arrow_right = arrow_point - perpendicular * arrow_size  # правая точка стрелки

            pygame.draw.polygon(screen, (255, 255, 255), [self.end_point.astype(int), arrow_left.astype(int), arrow_right.astype(int)])  # полигон стрелки

    def translate(self, dx, dy):
        self.start_point[0] += dx  # перемещение по оси х
        self.start_point[1] += dy  # перемещение по оси у
        self.end_point[0] += dx  # перемещение оси х
        self.end_point[1] += dy  # перемещение оси у

    def rotate(self, angle):
        direction = self.end_point - self.start_point  # направление вектора
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]], dtype=np.float32)  # Матрица поворота
        rotated_direction = np.dot(rotation_matrix, direction)  # поворот направления вектора
        self.end_point = self.start_point + rotated_direction  # обновление конечной точки

    def scale(self, scale_factor):
        self.end_point = self.start_point + (self.end_point - self.start_point) * scale_factor  # масштабирование вектора
    # это функции сложения и умножения
    # def __add__(self, other):
    #     if isinstance(other, Vector):
    #         start_point = self.start_point
    #         end_point = self.end_point + other.end_point - other.start_point
    #         return Vector(start_point, end_point[0] - start_point[0], end_point[1] - start_point[1])
    #     else:
    #         pass
    #
    # def __mul__(self, scalar):
    #     if isinstance(scalar, (int, float)):
    #         start_point = self.start_point
    #         end_point = self.start_point + (self.end_point - self.start_point) * scalar
    #         return Vector(start_point, end_point[0] - start_point[0], end_point[1] - start_point[1])
    #     else:
    #         pass

def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()

    vector = Vector([200, 300], 200, 70)  # создание вектора

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    vector.rotate(np.pi / 6)  # поворот против часовой стрелки
                elif event.key == pygame.K_RIGHT:
                    vector.rotate(-np.pi / 6)  # поворот по часовой стрелке
                elif event.key == pygame.K_UP:
                    vector.translate(10, 0)  # перемещение вектора вверх
                elif event.key == pygame.K_DOWN:
                    vector.translate(-10, 0) # перемещение вектора вниз
                elif event.key == pygame.K_PLUS:
                    vector.scale(1.9) # +
                elif event.key == pygame.K_MINUS:
                    vector.scale(0.9) # -

        screen.fill((0, 0, 0))  # очистка экрана
        vector.drawVector(screen)  # отрисовка вектора на экране
        pygame.display.flip()  # обновление экрана
        clock.tick(60)  # ограничение частоты кадров

if __name__ == '__main__':
    main()

# а это пример использования функций сложения и умножения
# vector1 = Vector([0, 0], 3, 4)
# vector2 = Vector([2, 3], 4, 2)
#
# # сложения двух векторов
# vector_sum = vector1 + vector2
# print(vector_sum.start_point)  # [0, 0]
# print(vector_sum.end_point)  # [7, 6]
#
# # умножения вектора на скаляр
# scalar = 2.5
# scaled_vector = vector1 * scalar
# print(scaled_vector.start_point)  # [0, 0]
# print(scaled_vector.end_point)  # [7.5, 10.0]