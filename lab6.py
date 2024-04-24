import pygame
import math
from datetime import datetime

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("lab6")

# Функция для преобразования угла в радианы
def degrees_to_radians(degrees):
    return degrees * math.pi / 180

# Функция для отрисовки часовой стрелки
def draw_hour_hand(hour, minute):
    angle = degrees_to_radians((hour % 12) * 30 + minute * 0.5)
    length = 80
    thickness = 6
    pygame.draw.line(screen, BLACK, (200, 200), (200 + length * math.sin(angle), 200 - length * math.cos(angle)), thickness)

# Функция для отрисовки минутной стрелки
def draw_minute_hand(minute):
    angle = degrees_to_radians(minute * 6)
    length = 120
    thickness = 4
    pygame.draw.line(screen, BLUE, (200, 200), (200 + length * math.sin(angle), 200 - length * math.cos(angle)), thickness)

# Функция для отрисовки секундной стрелки
def draw_second_hand(second):
    angle = degrees_to_radians(second * 6)
    length = 140
    thickness = 2
    pygame.draw.line(screen, RED, (200, 200), (200 + length * math.sin(angle), 200 - length * math.cos(angle)), thickness)

# Функция для отрисовки делений и чисел
def draw_divisions():
    numbers = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rotated_numbers = numbers[1:] + numbers[:1]  # Сдвигаем числа на одну позицию вправо

    for i, number in enumerate(rotated_numbers):
        angle = degrees_to_radians(i * 30)
        inner_radius = 140
        outer_radius = 160
        inner_point = (200 + inner_radius * math.sin(angle), 200 - inner_radius * math.cos(angle))
        outer_point = (200 + outer_radius * math.sin(angle), 200 - outer_radius * math.cos(angle))
        pygame.draw.line(screen, BLACK, inner_point, outer_point, 2)

        # Определение координат для чисел
        text_radius = 120
        text_x = 200 + text_radius * math.sin(angle) - 8
        text_y = 200 - text_radius * math.cos(angle) - 8

        # Отрисовка чисел
        font = pygame.font.Font(None, 24)
        text = font.render(str(number), True, BLACK)
        screen.blit(text, (text_x, text_y))

# Функция для отрисовки окружности
def draw_clock_boundary():
    pygame.draw.circle(screen, BLACK, (200, 200), 160, 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(WHITE)

    # Получение текущего времени
    current_time = datetime.now().time()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second

    # Отрисовка окружности
    draw_clock_boundary()

    # Отрисовка часовой, минутной и секундной стрелок
    draw_hour_hand(hour, minute)
    draw_minute_hand(minute)
    draw_second_hand(second)

    # Отрисовка делений и чисел
    draw_divisions()

    # Отображение изменений на экране
    pygame.display.flip()

pygame.quit()