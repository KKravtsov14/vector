import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __len__(self):
        return sqrt((self.x ** 2) + (self.y ** 2))

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y

        else:
            return Vector(other * self.x, other * self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def int_pair(self):
        return (int(self.x), int(self.y))


class Line(Vector):

    def __init__(self):
        super().__init__()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        return (points[deg].mul(alpha)).add(self.get_point(points, alpha, deg - 1).mul(1-alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        result = []
        for i in range(count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def set_points(self, points, speeds):
        for point in range(len(points)):
            points[point] = points[point].add(speeds[point])
            if points[point].x > SCREEN_SIZE[0] or points[point].x < 0:
                speeds[point] = (- speeds[point].x, speeds[point].y)
            if points[point].y > SCREEN_SIZE[1] or points[point].y < 0:
                speeds[point] = (speeds[point].x, -speeds[point].y)

class Joint(Line):
    def __init__(self):
        super().__init__()

    def get_joint(self, points, count):
        if len(points) < 3:
            return []
        result = []
        for i in range(-2, len(points) - 2):
            pnt = []
            pnt.append((points[i].add(points[i + 1])).mul(0.5))
            pnt.append(points[i + 1])
            pnt.append((points[i].add(points[i + 2])).mul(0.5))

            result.extend(self.get_points(pnt, count))
        return result

def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))

def draw_points(points, style="points", width=4, color=(255, 255, 255)):
    if style == "line":
        for point_number in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                                 (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)

    elif style == "points":
        for point in points:
            pygame.draw.circle(gameDisplay, color,
                                (int(point.x), int(point.y)), width)

if __name__ == '__main__':
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(Vector(event.pos[0], event.pos[1]))
                speeds.append(Vector(random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        draw_points(points)
        self = ''
        draw_points(Joint.get_joint(self, points, steps), "line", 4, color)

        if not pause:
            Line.set_points(self, points, speeds)
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)