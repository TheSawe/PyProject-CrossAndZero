from typing import Tuple

import pygame
import time

pygame.init()

# Custom tools
size_of_window = 400  # не больше размера экрана
number_of_cell = 3  # не больше 50
thickness: int = 2  # 2 или 3 по вкусу
margin = 30  # не больше чем size_of_window

if size_of_window // margin <= 2.5 or number_of_cell > 50 or thickness not in [2, 3]:
    print('No way you don\'t listen to my instruction')
    exit()

screen = pygame.display.set_mode((size_of_window, size_of_window))
is_work = True
move = True
field = ['' for x in range(number_of_cell * number_of_cell)]

size_of_windowCell = (size_of_window - margin * 2) / number_of_cell

pygame.draw.rect(screen, (255, 255, 255),
                 pygame.Rect(margin, margin, size_of_window - margin * 2, size_of_window - margin * 2),
                 thickness)

for step in range(1, number_of_cell):
    startPosX = margin + size_of_windowCell * step - thickness
    startPosY = margin
    endPosX = size_of_window - (size_of_window - margin - size_of_windowCell * step) - thickness
    endPosY = size_of_window - margin - thickness

    pygame.draw.line(screen, (255, 255, 255), start_pos=(startPosX, startPosY), end_pos=(endPosX, endPosY),
                     width=thickness)

for step in range(1, number_of_cell):
    startPosX = margin
    startPosY = margin + size_of_windowCell * step
    endPosX = size_of_window - margin - thickness
    endPosY = size_of_window - (size_of_window - margin - size_of_windowCell * step)

    pygame.draw.line(screen, (255, 255, 255), start_pos=(startPosX, startPosY), end_pos=(endPosX, endPosY),
                     width=thickness)


def which_cube(mouse_pos: tuple):
    global move

    positions = []
    coefficient = -1
    rand = 1
    values = []
    for iteration in range(number_of_cell * number_of_cell):
        i = iteration
        if iteration < number_of_cell:
            values.append(round(margin + size_of_windowCell / 2 + size_of_windowCell * (i // rand), 1))
        if iteration % number_of_cell == 0:
            coefficient += 1
        positions.append((values[iteration - (number_of_cell * (iteration // number_of_cell))],
                          round(margin + size_of_windowCell / 2 + size_of_windowCell * coefficient, 1)))
    (x, y) = mouse_pos
    mindifference = size_of_window
    for posX, posY in positions:
        if abs(posX - x) + abs(posY - y) < mindifference:
            mindifference = abs(posX - x) + abs(posY - y)
            pare = (posX, posY)
    if field[positions.index(pare)] in ['X', 'O']:
        print('Место уже занято')
        move = not move
        return size_of_window * 2, size_of_window * 2
    else:
        if move:
            field[positions.index(pare)] = 'X'
        else:
            field[positions.index(pare)] = 'O'
        return pare


def draw_cross():
    (x, y) = which_cube(pos)
    const = ((size_of_windowCell ** 2 + size_of_windowCell ** 2) ** 0.5) * (1 / 3)
    pygame.draw.line(screen, (255, 0, 0), start_pos=(x - const, y - const),
                     end_pos=(x + const, y + const), width=thickness)
    pygame.draw.line(screen, (255, 0, 0), start_pos=(x + const, y - const),
                     end_pos=(x - const, y + const),
                     width=thickness)


def draw_circle():
    (x, y) = which_cube(pos)
    pygame.draw.circle(screen, (0, 0, 255), (x, y), size_of_windowCell // 2 - thickness, thickness)


def end_game():
    time.sleep(2)
    quit()


while is_work:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_work = False
        elif event.type == pygame.MOUSEBUTTONUP:
            type_arr = [[] for _ in range(number_of_cell)]

            if move:
                pos = pygame.mouse.get_pos()
                draw_cross()
                pygame.display.flip()
                for index, el in enumerate(field):
                    type_arr[index // number_of_cell].append(el)
                for els in type_arr:
                    x = 0
                    for el in els:
                        if el.lower() == 'x':
                            x += 1
                    if x == number_of_cell:
                        print('Победил X')
                        end_game()
                move = not move
            elif not move:
                pos = pygame.mouse.get_pos()
                draw_circle()
                pygame.display.flip()
                for index, el in enumerate(field):
                    type_arr[index // number_of_cell].append(el)
                for els in type_arr:
                    o = 0
                    for el in els:
                        if el.lower() == 'o':
                            o += 1
                    if o == number_of_cell:
                        print('Победил O')
                        end_game()
                move = not move
    pygame.display.flip()
pygame.quit()
