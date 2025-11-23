import pygame
import math
from Classes import Board

pygame.display.init()
pygame.font.init()

ScreenSize = pygame.display.get_desktop_sizes()
current_w = ScreenSize[0][0] if ScreenSize else 800
current_h = ScreenSize[0][1] if ScreenSize else 600

print(ScreenSize)
FPS = 60
gameOn = True
currentTurn = 0

FIGURE_O = "O"
FIGURE_X = "X"

canvas = pygame.display.set_mode((current_w, current_h))
clock = pygame.time.Clock()

scale = current_w / 192
print(scale)

font = pygame.font.SysFont('Bahnschrift', round(5 * scale))
fontBig = pygame.font.SysFont('Bahnschrift', round(10 * scale))
fontColor = (0, 0, 0)

try:
    backgroundORG = pygame.image.load('textures/bg.png').convert()
    background = pygame.transform.scale(backgroundORG,
                                        (backgroundORG.get_width() * scale, backgroundORG.get_height() * scale))

    icon_cross = pygame.image.load('Textures/Cross.png').convert_alpha()
    icon_cross = pygame.transform.scale(icon_cross, (5 * scale, 5 * scale))

    icon_circle = pygame.image.load('Textures/Circle.png').convert_alpha()
    icon_circle = pygame.transform.scale(icon_circle, (5 * scale, 5 * scale))
except Exception as e:
    print(f"Błąd ładowania: {e}")
    gameOn = False

mainBoard = Board(scale, 45 * scale, 3 * scale, False)
boards_list = []

for i in range(9):
    newBoard = Board(scale / 3.185, mainBoard.slots[i][0], mainBoard.slots[i][1], True)
    boards_list.append(newBoard)


def detectWhichBoardDoesMouseTouch():
    for board in boards_list:
        if board.rect.collidepoint(pygame.mouse.get_pos()):
            return board
    return None


def placeOnEveryBoard():
    for board in boards_list:
        if board.available:
            board.placing = True
        else:
            board.placing = False


def movePlacement(dest):
    target_board = boards_list[dest]

    if not target_board.available:
        placeOnEveryBoard()
    else:
        for b in boards_list:
            b.placing = False
        target_board.placing = True


while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameOn = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == True:
                touched_board = detectWhichBoardDoesMouseTouch()

                if touched_board and touched_board.placing:
                    slotCenterDist = []
                    for i in touched_board.slots:
                        center_x = i[0] + touched_board.rect.w * (4.5 / 32)
                        center_y = i[1] + touched_board.rect.h * (4.5 / 32)
                        slotCenterDist.append(math.dist((center_x, center_y), pygame.mouse.get_pos()))

                    newFigurePlacePos = slotCenterDist.index(min(slotCenterDist))

                    if touched_board.status[newFigurePlacePos] == "":
                        current_turn_symbol = FIGURE_O if currentTurn % 2 == 0 else FIGURE_X

                        touched_board.place(newFigurePlacePos, current_turn_symbol)
                        winner = touched_board.checkVictory()

                        board_index = boards_list.index(touched_board)

                        if winner:
                            mainBoard.place(board_index, winner)
                            mainBoard.checkVictory()

                        currentTurn += 1
                        movePlacement(newFigurePlacePos)

    canvas.blit(background, (0, 0))
    displayTurn = math.floor((currentTurn) / 2) + 1

    for i, board in enumerate(boards_list):
        for figure in board.figures:
            canvas.blit(figure.image, figure.rect)

        if board.placing and mainBoard.winner is None:
            canvas.blit(board.frame, (board.rect.x - 2 * board.scale, board.rect.y - 2 * board.scale))

    for figure in mainBoard.figures:
        canvas.blit(figure.image, figure.rect)

    canvas.blit(font.render(f'Tura: {displayTurn}', True, fontColor), (5 * scale, 90 * scale))
    canvas.blit(font.render(f'Nastepny:', True, fontColor), (5 * scale, 100 * scale))

    next_icon = icon_cross if currentTurn % 2 != 0 else icon_circle
    canvas.blit(next_icon, (30 * scale, 100 * scale))

    if mainBoard.winner:
        canvas.blit(fontBig.render(f'Wygral {mainBoard.winner}!', True, fontColor), (149 * scale, 50 * scale))
        for board in boards_list:
            board.placing = False
    elif not mainBoard.available:
        canvas.blit(fontBig.render(f'REMIS!', True, fontColor), (149 * scale, 50 * scale))

    pygame.display.flip()
    clock.tick(FPS)