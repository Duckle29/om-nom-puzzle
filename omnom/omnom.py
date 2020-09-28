from pathlib import Path
import sys
import os
from random import random

import pygame

from omnon_exceptions import Glutton
from config import colors

SCREEN_SIZE = (1600, 900)

media_dir = Path('media')


class Piece(object):
    def __init__(self, home, size, mother_surface, sample_position, position):
        """[summary]

        Args:
            position (2-tuple): Upper left coordinate of the piece
            surface (pygame.Surface): [description]
        """
        self.home = (home[0], home[1])
        self.surface = mother_surface.subsurface((sample_position, size))
        self.center = (size[0]/2 + home[0], size[1]/2 + home[1])
        self.position = (0,0)

    def draw(self):
        pass


class Puzzle(object):
    
    pieces = []

    def __init__(self, grid_surface_texture, position, puzzle_size, grid_size=(10,10)):
        self.surface = grid_surface_texture
        self.position = position
        self.grid_size = grid_size
        self.puzzle_size = puzzle_size
        self.generate_pieces()
        
        
    def set_grid_size(self, size):
        self.grid_size = size
        generate_pieces()

    def generate_pieces(self):
        piece_size = (
            self.surface.get_width() // self.grid_size[0],
            self.surface.get_height() // self.grid_size[1]
        )

        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                p = Piece(
                    (
                        x*piece_size[0] + self.position[0],
                        y*piece_size[1] + self.position[1]
                    ),
                    piece_size, 
                    self.surface, 
                    (
                        x*piece_size[0], 
                        y*piece_size[1]
                    )
                )

                self.pieces.append(p)

    def get_piece(self, coordinate):
        pass

    def drop_piece(self, coordinate):
        pass


def draw_background(surf, offset):
    
    padding = 5

    surf.fill(colors['background'])
    surf.fill(colors['lines'], (offset-padding, offset-padding, surf.get_width()/2 + 2*padding, surf.get_height()-offset*2 + padding*2))
    surf.fill(colors['puzzle_area'], (offset, offset, surf.get_width()/2, surf.get_height()-offset*2))


def main():
    offset = 30
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    
    puzzle_img = pygame.image.load('media/default.jpg').convert()
    main_surf = pygame.transform.scale(puzzle_img, (screen.get_width()//2, screen.get_height()-offset*2))

    puzzle = Puzzle(main_surf, (offset, offset), main_surf.get_size())

    while(True):
        pygame.display.flip()
        clock.tick(60)

        draw_background(screen, offset)

        to_blit = []
        for p in puzzle.pieces:
            to_blit.append((p.surface, p.position))

        screen.blits(to_blit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if piece is not None:
                    raise(Glutton(piece.position, new_piece))
                else:
                    piece = puzzle.get_piece(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONUP:
                if piece is not None:
                    piece = puzzle.drop_piece(piece)

if os.getcwd() != "C:\\Users\\mikke\\projects\\om-nom-puzzle\\omnon":
    print(os.getcwd())
    os.chdir('omnom')
main()
