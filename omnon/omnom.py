from pathlib import Path
import sys
import random

import pygame
from PIL import Image

from .omnon_exceptions import Glutton

SCREEN_SIZE = (1600, 900)


class Piece(object):
    def __init__(self, postion, surface):
        self.postion = postion
        self.surface = surface
        pass
    
    def draw(self):
        pass

    def bite(self):
        pass

    def spit(self):
        pass


class Puzzle(object):
    def __init__(self, grid_size=(10,10), grid_surface_texture=Path('media/default.jpg')):
        self.grid_size = grid_size
        self.generate_pieces()
        self.pieces = []
        self.im = Image.open(grid_surface_texture)
    
    def set_grid_size(self, size):
        self.grid_size = size
        generate_pieces()

    def generate_pieces(self):
        piece_size = (
            im.width // self.grid_size[0],
            im.height // self.grid_size[1]
        )

        crop_coords = (0, 0, piece_size[0], piece_size[1])

        for idx_y, y in enumerate(range(im.width // self.grid_size[1])):
            for idx_x, x in enumerate(range(im.height // self.grid_size[0])):
                surface = im.crop(crop_coords)
                p = Piece((idx_x, idx_y), surface)
                self.pieces.append(p)

    def get_piece(self, coordinate):
        pass



def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    puzzle = Puzzle()

    piece = None

    gameDisplay.fill((255,255,255))

    while(True):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                new_piece = puzzle.get_piece(pygame.mouse.get_pos())
                if piece is not None:
                    raise(Glutton(piece.position, new_piece))
                else:
                    piece = new_piece
                
            