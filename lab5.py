import pygame
import math

pygame.init()

GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Animating Square")

# Начальные координаты и скорости движения и вращения квадрата
x = 300
y = 250
speed_y = 0.3
angle = 0
rotation_speed = 0.3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Проверка нажатия
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        y += speed_y
        angle += rotation_speed

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Расчет координат вершин квадрата с учетом угла поворота
    vertices = [
        (x, y),
        (x + 200, y),
        (x + 200, y + 200),
        (x, y + 200)
    ]

    # Поворот вершин квадрата вокруг центра
    rotated_vertices = []
    center_x = x + 100
    center_y = y + 100
    for vertex in vertices:
        translated_x = vertex[0] - center_x
        translated_y = vertex[1] - center_y
        rotated_x = translated_x * math.cos(angle) - translated_y * math.sin(angle)
        rotated_y = translated_x * math.sin(angle) + translated_y * math.cos(angle)
        final_x = rotated_x + center_x
        final_y = rotated_y + center_y
        rotated_vertices.append((final_x, final_y))

    # Отрисовка квадрата
    pygame.draw.polygon(screen, GREEN, rotated_vertices)

    # Отрисовка красной точки
    pygame.draw.circle(screen, RED, (int(center_x), int(center_y)), 3)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()