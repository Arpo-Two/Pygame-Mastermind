import pygame
import random
pygame.init()
pygame.font.init()
talt = 650
tlarg= 1250
box = talt * 3 // 4
pygame.display.set_caption('Mastermind')
fonte = pygame.font.SysFont('Candaras', 250)
small = pygame.font.SysFont('Candaras', 80)


red = (255, 0, 0)
yellow = (255, 255, 0)
orange = (255, 102, 0)
green = (0, 204, 0)
blue = (0, 0, 255)
pink = (255, 0, 255)
purple = (102, 0, 104)
black = (0, 0, 0)
white = (255, 255, 255)

color_sequence = [red, yellow, orange, green, blue, pink, purple]
sequence = ['red', 'yellow', 'orange', 'green', 'blue', 'pink', 'purple']

win = pygame.display.set_mode((tlarg, talt), pygame.FULLSCREEN)


class Game(object):
    def __init__(self):
        self.answer = ''
        self.hidden = True
        self.selected = [0, 0]
        self.tries = 0
        self.array = []
        self.evaluations = []
        self.state = 0


game = Game()


def draw_lines():
    for x in range(11):
        pygame.draw.line(win, black, (x * tlarg // 11, 0), (x * tlarg // 11, talt), 3)
    pygame.draw.line(win, black, (0, talt * 3 // 4), (tlarg * 10 // 11, talt * 3 // 4), 3)


def dr(x1, x2, y1, y2):
    return((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def new_row():
    game.array.append([0, 0, 0, 0])


def new_game():
    game.answer = []
    for _ in range(4):
        r = random.randint(0, len(sequence) - 1)
        game.answer.append([sequence[r], color_sequence[r]])
    game.hidden = True
    game.selected = [0, 0]
    game.tries = 0
    game.array = []
    game.evaluations = []
    game.state = 0
    new_row()


def draw_answer(hidden):
    for x in range(4):
        pygame.draw.circle(win, game.answer[x][1], (tlarg * 21 // 22, 2 * talt // 13 + x * talt * 3 // 13), talt // 13)
        pygame.draw.circle(win, black, (tlarg * 21 // 22, 2 * talt // 13 + x * talt * 3 // 13), talt // 13, 3)
    if hidden:
        pygame.draw.rect(win, (153, 51, 0), (tlarg * 10 // 11, 0, tlarg, talt))


def draw_selected():
    pygame.draw.rect(win, (153, 204, 0), (game.selected[0] * tlarg // 11, game.selected[1] * box // 4, tlarg // 11,
                                          box // 4), 8)


def draw_balls():
    for row in enumerate(game.array):
        for ball in enumerate(row[1]):
            pygame.draw.circle(win, color_sequence[ball[1]], (tlarg // 22 + row[0] * tlarg // 11, 2 * box // 13 +
                                                              ball[0] * box // 4), box // 13)
            pygame.draw.circle(win, black, (tlarg // 22 + row[0] * tlarg // 11, 2 * box // 13 + ball[0] * box // 4),
                               box // 13, 3)


def draw_evaluation():
    for row in enumerate(game.evaluations):
        for ball in enumerate(row[1]):
            if ball[0] == 0:
                pos = 2 * tlarg // 77 + row[0] * tlarg // 11, box + 2 * (talt - box) // 8
            elif ball[0] == 1:
                pos = 5 * tlarg // 77 + row[0] * tlarg // 11, box + 2 * (talt - box) // 8
            elif ball[0] == 2:
                pos = 2 * tlarg // 77 + row[0] * tlarg // 11, box + 5 * (talt - box) // 8
            else:
                pos = 5 * tlarg // 77 + row[0] * tlarg // 11, box + 5 * (talt - box) // 8

            if ball[1] == 0:
                pygame.draw.circle(win, white, pos, (talt - box) // 8)
                pygame.draw.circle(win, black, pos, (talt - box) // 8, 3)
            else:
                pygame.draw.circle(win, black, pos, (talt - box) // 8)


def evaluate_position(given, right):

    result = []
    adjusted = []
    provisory = given.copy()
    for a in right:
        adjusted.append(sequence.index(a[0]))

    for ball in range(len(provisory)):
        if provisory[ball] == adjusted[ball]:
            result.append(1)
            provisory[ball] = 8
            adjusted[ball] = 9

    for ball in range(len(provisory)):
        if provisory[ball] in adjusted:
            result.append(0)
            adjusted[adjusted.index(provisory[ball])] = 9
            provisory[ball] = 8

    return result


new_game()
run = True
while run:
    if game.state == 0:
        win.fill((99, 99, 99))
        draw_lines()
        draw_answer(game.hidden)
        draw_balls()
        draw_selected()
        draw_evaluation()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_UP and game.selected[1] > 0:
                    game.selected[1] -= 1
                if event.key == pygame.K_DOWN and game.selected[1] < 3:
                    game.selected[1] += 1
                if event.key == pygame.K_RIGHT and game.array[game.selected[0]][game.selected[1]] < 6:
                    game.array[game.selected[0]][game.selected[1]] += 1
                if event.key == pygame.K_LEFT and game.array[game.selected[0]][game.selected[1]] > 0:
                    game.array[game.selected[0]][game.selected[1]] -= 1
                if event.key == pygame.K_SPACE and game.tries < 10:
                    game.evaluations.append(evaluate_position(game.array[game.tries], game.answer))
                    if evaluate_position(game.array[game.tries], game.answer) == [1, 1, 1, 1]:
                        game.state = 1
                    elif game.tries == 9:
                        game.state = -1
                    if game.tries < 9:
                        game.selected[0] += 1
                        new_row()
                    game.tries += 1
    else:
        game.hidden = False
        if game.state == 1:
            win.fill((50, 150, 50))
            win.blit(fonte.render('YOU WIN', False, black), (220, 0))
        else:
            win.fill((150, 50, 50))
            win.blit(fonte.render('YOU LOSE', False, black), (200, 0))

        pygame.draw.circle(win, (50, 50, 150), (tlarg * 2 // 7, 450), tlarg // 7)
        pygame.draw.circle(win, black, (tlarg * 2 // 7, 450), tlarg // 7, 20)
        win.blit(small.render('  New Game', False, black), (tlarg // 7, 420))

        pygame.draw.circle(win, (50, 50, 150), (tlarg * 5 // 7, 450), tlarg // 7)
        pygame.draw.circle(win, black, (tlarg * 5 // 7, 450), tlarg // 7, 20)
        win.blit(small.render('   See board', False, black), (tlarg * 4 // 7, 420))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dr(pygame.mouse.get_pos()[0], tlarg * 2// 7, pygame.mouse.get_pos()[1], 450) < tlarg // 7:
                    new_game()
                elif dr(pygame.mouse.get_pos()[0], tlarg * 5// 7, pygame.mouse.get_pos()[1], 450) < tlarg // 7:
                    game.state = 0


    pygame.display.update()
