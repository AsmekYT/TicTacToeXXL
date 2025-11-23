import pygame


class Figure(pygame.sprite.Sprite):
    def __init__(self, img, pos_x, pos_y):
        super().__init__()
        self.image = img
        self.rect = pygame.Rect(pos_x, pos_y, self.image.get_width(), self.image.get_height())


class Board(pygame.sprite.Sprite):
    CROSS_IMG = None
    CIRCLE_IMG = None
    FRAME_IMG = None

    WIN_COMBINATIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    def __init__(self, scale, pos_x, pos_y, make_transparent_after_winning):
        super().__init__()
        self.scale = scale
        self.make_transparent_after_winning = make_transparent_after_winning
        self.available = True
        self.placing = True
        self.winner = None

        if Board.CROSS_IMG is None:
            Board.CROSS_IMG = pygame.image.load('Textures/Cross.png').convert_alpha()
            Board.CIRCLE_IMG = pygame.image.load('Textures/Circle.png').convert_alpha()
            Board.FRAME_IMG = pygame.image.load('Textures/Frame.png').convert_alpha()

        self.cross = pygame.transform.scale(Board.CROSS_IMG, ((Board.CROSS_IMG.get_width() / 8) * self.scale,
                                                              (Board.CROSS_IMG.get_height() / 8) * self.scale))
        self.circle = pygame.transform.scale(Board.CIRCLE_IMG, ((Board.CIRCLE_IMG.get_width() / 8) * self.scale,
                                                                (Board.CIRCLE_IMG.get_height() / 8) * self.scale))
        self.frame = pygame.transform.scale(Board.FRAME_IMG, (106 * scale, 106 * scale))

        self.rect = pygame.Rect(pos_x, pos_y, 102 * scale, 102 * scale)

        self.status = [""] * 9
        self.figures = pygame.sprite.Group()

        w_div = self.rect.w / 2.914
        h_div = self.rect.h / 2.914

        self.slots = [
            (self.rect.x, self.rect.y),
            (self.rect.x + w_div, self.rect.y),
            (self.rect.x + w_div * 2, self.rect.y),
            (self.rect.x, self.rect.y + h_div),
            (self.rect.x + w_div, self.rect.y + h_div),
            (self.rect.x + w_div * 2, self.rect.y + h_div),
            (self.rect.x, self.rect.y + h_div * 2),
            (self.rect.x + w_div, self.rect.y + h_div * 2),
            (self.rect.x + w_div * 2, self.rect.y + h_div * 2)
        ]

    def place(self, position, player):
        if self.status[position] == "":
            self.status[position] = player
            img = self.cross if player == "X" else self.circle
            new_fig = Figure(img, self.slots[position][0], self.slots[position][1])
            self.figures.add(new_fig)

    def checkDraw(self):
        if "" not in self.status and self.winner is None:
            self.available = False
            return True
        return False

    def checkVictory(self):
        if self.winner:
            return self.winner

        for a, b, c in Board.WIN_COMBINATIONS:
            if self.status[a] == self.status[b] == self.status[c] and self.status[a] != "":
                self.winner = self.status[a]
                self.available = False

                if self.make_transparent_after_winning:
                    self.apply_transparency()

                return self.winner

        self.checkDraw()
        return None

    def apply_transparency(self):
        for fig in self.figures:
            fig.image = fig.image.copy()
            fig.image.set_alpha(85)