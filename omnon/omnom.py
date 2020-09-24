from pathlib import Path
import sys
import random

import pygame

from .omnon_exceptions import Glutton

SCREEN_SIZE = (1600, 900)



class Piece(object):
    def __init__(self, postion, surface):
        self.postion = postion
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
        pass
    
    def set_grid_size(self, size):
        pass

    def generate_pieces(self):
        pass

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
                
            