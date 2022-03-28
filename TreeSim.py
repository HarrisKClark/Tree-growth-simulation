import random
import pygame

WIDTH = 1000
HEIGHT = 600
FPS = 30
CELLSIZE = 3

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vascular Automata")


class ground:
    def __init__(self):
        self.color = (100, 60, 20)

class seed:
    def __init__(self):
        self.color = (120, 80, 40)
        self.age = 0

class tree:
    def __init__(self):
        self.color = (0, 120, 10)
        self.age = 0
        self.energy = 0

    def update_color(self):
        self.color = (0, 120 - self.age*5, 10)


def draw_cells(cells):
    for i in range(len(cells)):
        for j in range(len(cells[0])):
                x = i * CELLSIZE
                y = j * CELLSIZE
                pygame.draw.rect(WIN, cells[i][j].color, (x, y, CELLSIZE, CELLSIZE))


def update(cells):

    new_cells = [row[:] for row in cells]

    for i in range(len(new_cells)):
        for j in range(len(new_cells[0])):
            if type(new_cells[i][j]) is ground:
                if random.randint(0, 10000) == 4:
                    new_cells[i][j] = seed()

            elif type(new_cells[i][j]) is seed:
                if new_cells[i][j].age < 20:
                    new_cells[i][j].age += 1
                else:
                    new_cells[i][j] = tree()

            elif type(new_cells[i][j]) is tree:
                new_cells[i][j].update_color()

                if new_cells[i][j].age < 9:
                    new_cells[i][j].age += 0.5

                else:
                    if new_cells[i][j].energy < -1:
                        new_cells[i][j] = ground()

                    elif new_cells[i][j].energy < 10:
                        count = 1

                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                try:
                                    if type(new_cells[i + k][j + l]) is tree:
                                        count += 1
                                except IndexError:
                                    pass

                        new_cells[i][j].energy += 8-count

                    else:
                        new_cells[i][j].energy = 0
                        dir = random.choice([[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]])

                        try :
                            if type(new_cells[i + dir[0]][j + dir[1]]) is ground:
                                new_cells[i + dir[0]][j + dir[1]] = seed()

                        except IndexError:
                            pass

    draw_cells(new_cells)

    return new_cells


def main():
    run = True
    clock = pygame.time.Clock()

    cells = [[ground() for j in range(0, (HEIGHT // CELLSIZE))] for i in range(0, WIDTH // CELLSIZE)]

    while run:
        clock.tick(FPS)
        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    cells[x // CELLSIZE][y // CELLSIZE] = seed()
                except IndexError:
                    pass

        cells = update(cells)
        pygame.display.update()

if __name__ == '__main__':
    main()
