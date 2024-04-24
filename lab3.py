import numpy as np
import pygame

class Vector:
    def __init__(self, start_point, x, y):
        self.start_point = start_point  # начальная точка вектора
        self.end_point = np.array([start_point[0] + x, start_point[1] + y], dtype=np.float32)  # конечная точка вектора

    def drawVector(self, screen):
        pygame.draw.line(screen, (250, 0, 0), self.start_point, self.end_point.astype(int), 2)  # линия вектора

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

            pygame.draw.polygon(screen, (250, 0, 0), [self.end_point.astype(int), arrow_left.astype(int), arrow_right.astype(int)])  # полигон стрелки

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
    def __add__(self, other):
        if isinstance(other, Vector):
            start_point = self.start_point
            end_point = self.end_point + other.end_point - other.start_point
            return Vector(start_point, end_point[0] - start_point[0], end_point[1] - start_point[1])
        else:
            pass

    def __mul__(self, other):
        if isinstance(other, Vector):
            start_point = self.start_point
            end_point = self.start_point + (self.end_point - self.start_point) * (other.end_point - other.start_point)
            return Vector(start_point, end_point[0] - start_point[0], end_point[1] - start_point[1])
        else:
            pass

    def triangle_from_vectors(self, other):
        if isinstance(other, Vector):
            vector_product = np.cross(self.get_components(), other.get_components())
            if vector_product != 0:
                start_point = self.start_point
                end_point = self.start_point + vector_product
                return Triangle(start_point, end_point[0] - start_point[0], end_point[1] - start_point[1])
            return None

class Triangle:
    def __init__(self, start_point, width, height):
        self.start_point = np.array(start_point)
        self.width = width
        self.height = height

    def drawTriangle(self, screen):
        end_point1 = self.start_point + np.array([self.width, 0])
        end_point2 = self.start_point + np.array([0, self.height])
        pygame.draw.polygon(screen, (255, 0, 0), [self.start_point, end_point1, end_point2])


def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()

    vector1 = Vector([200, 300], 200, 70)
    vector2 = Vector([400, 300], 100, 0)

    result_vector = None  # Добавленная переменная для результирующего вектора
    draw_result = False
    alt_pressed = False
    multiply_vectors = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    vector1.rotate(np.pi / 6)
                elif event.key == pygame.K_RIGHT:
                    vector1.rotate(-np.pi / 6)
                elif event.key == pygame.K_UP:
                    vector1.translate(10, 0)
                elif event.key == pygame.K_DOWN:
                    vector1.translate(0, -10)
                elif event.key == pygame.K_a:
                    vector1.translate(0, 10)
                elif event.key == pygame.K_d:
                    vector1.translate(-10, 0)
                elif event.key == pygame.K_w:
                    vector1.scale(1.9)
                elif event.key == pygame.K_MINUS:
                    vector1.scale(0.9)
                elif event.key == pygame.K_SPACE:
                    draw_result = True
                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    alt_pressed = True
                elif event.key == pygame.K_m:  # Добавленное условие для активации умножения векторов
                    multiply_vectors = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    draw_result = False
                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    alt_pressed = False

        result_vector = vector1 + vector2

        screen.fill((178, 34, 34))
        vector1.drawVector(screen)
        vector2.drawVector(screen)

        if draw_result and not alt_pressed:
            result_vector.drawVector(screen)

        if multiply_vectors:  # Добавленная проверка флага для умножения векторов
            result_vector = vector1 * vector2
            result_vector.drawVector(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
