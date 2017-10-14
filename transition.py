import pygame
import random

SQUARE_SIZE = 32


class Transition:

    def __init__(self, surface):
        self.surface = surface
        self.surface_rect = self.surface.get_rect()
        self.rows = self.surface_rect.height // SQUARE_SIZE
        self.columns = self.surface_rect.width // SQUARE_SIZE
        self.white_squares = list(range(self.columns * self.rows))
        self.black_squares = []
        self.black_square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.black_square.fill((0, 0, 0))
        self.black_square.convert()

    def draw(self):
        for s in self.black_squares:
            x = s % self.columns
            y = s // self.columns
            self.surface.blit(self.black_square, (x * SQUARE_SIZE, y * SQUARE_SIZE))

    def is_finished(self):
        if self.white_squares:
            return False
        else:
            return True

    def update_random(self):
        if self.white_squares:
            for _ in range(5):
                rand_square = random.choice(self.white_squares)
                self.white_squares.remove(rand_square)
                self.black_squares.append(rand_square)

    def update(self):
        if self.white_squares:
            for _ in range(3):
                self.black_squares.append(self.white_squares.pop())

    def order_swirl(self):
        gathered_l = []
        for i in range(min(self.rows // 2, self.columns // 2)):
            gathered_l += self.white_squares[(self.columns + 1) * i: self.columns + self.columns * i - i - 1]
            gathered_l += self.white_squares[i * self.columns + (self.columns - 1) - i:
                                             (self.rows - i - 1) * self.columns: self.columns]
            temp_bottom = self.white_squares[i + self.columns * (self.rows - i - 1) + 1:
                                             self.columns * (self.rows - i) - i]
            temp_bottom.reverse()
            gathered_l += temp_bottom
            temp_left = self.white_squares[i * (self.columns + 1) + self.columns:
                                           (self.rows - i) * self.columns: self.columns]
            temp_left.reverse()
            gathered_l += temp_left
        self.white_squares = gathered_l
        self.white_squares.reverse()
