import pygame
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("lab2")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
W = (255, 255, 255)

center_x = width // 2
center_xx = width // 4
center_y = height // 2
center_yy = height // 4


radius = 200

angle = math.pi

divisions = 5  # Количество делений
division_angle = math.pi / divisions  # Угол между делениями

running = True
while running:
    screen.fill((255, 255, 255))

    pygame.draw.arc(screen, BLACK, (center_x - radius, center_y - radius, radius * 2, radius * 2),
                    0, math.pi, 3)

    # Отрисовка стрелки
    arrow_length = 100
    arrow_end_x = center_x + radius * math.cos(angle)
    arrow_end_y = center_y + radius * math.sin(angle)
    pygame.draw.line(screen, RED, (center_x, center_y), (arrow_end_x, arrow_end_y), 5)
    division_length = 20
    # Отрисовка делений
    for i in range(-2, divisions -2):
        division_end_x = center_x + radius * math.cos(i * division_angle - math.pi/2)
        division_end_y = center_y + radius * math.sin(i * division_angle - math.pi/2)
        pygame.draw.line(screen, BLACK, (center_x, center_y), (division_end_x, division_end_y), 2)
        division_end_x = center_x + (radius - division_length) * math.cos(i * division_angle - math.pi / 2)
        division_end_y = center_y + (radius - division_length) * math.sin(i * division_angle - math.pi / 2)
        pygame.draw.line(screen, W, (center_x, center_y), (division_end_x, division_end_y), 4)

    pygame.display.flip()  # Обновление экрана

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and angle <= math.pi*2:
                print(angle)
                angle += 0.1
            elif event.key == pygame.K_s and angle != math.pi:
                angle -= 0.1
                print(angle)

pygame.quit()