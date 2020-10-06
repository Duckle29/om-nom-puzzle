from pathlib import Path
import sys
import os
from random import random
from math import hypot

import pygame as pg

from omnon_exceptions import Glutton
from config import colors

SCREEN_SIZE = (1600, 900)

media_dir = Path('media')


class Piece(object):
    def __init__(self, home, size, mother_surface, sample_position, snap_radius=None):
        """[summary]

        Args:
            position (3-tuple): Upper left coordinate of the piece and Z-depth
            surface (pygame.Surface): [description]
        """
        self.home = home
        self.surface = mother_surface.subsurface((sample_position, size))
        self.rect = self.surface.get_rect(topleft=home)

        if snap_radius is None:
            self.snap_radius = self.rect.width/2
        else:
            self.snap_radius = snap_radius

        self.border_thickness = 3

    def drop(self):
        if hypot(self.rect.left - self.home[0], self.rect.top - self.home[1]) <= self.snap_radius:
            self.rect.topleft = self.home

    def draw(self):
        if self.rect.topleft == self.home:
            return self.surface, self.rect.topleft

        else:
            border_rect = (
                (0,0),
                (self.rect.width + self.border_thickness*2, self.rect.height + self.border_thickness*2)
            )
            surf = pg.Surface(border_rect[1])
            surf.fill(colors['piece_border'], border_rect)
            surf.blit(self.surface, (self.border_thickness,self.border_thickness))
            
            return (surf, (self.rect.left - self.border_thickness, self.rect.top - self.border_thickness))


class Puzzle(object):
    
    pieces = []

    def __init__(self, grid_surface_texture, puzzle_rect, scramble_rect, grid_size=(10,10)):
        """Generates a puzzle with the provided image as surface

        Args:
            grid_surface_texture (pygame.Surface): The image used as the puzzle surface
            puzzle_rect (4-tuple): The rect representing the puzzle area (x,y,w,h)
            scramble_size (4-tuple): The rect to scramble the pieces to  (x,y,w,h)
            grid_size (tuple, optional): the grid to split the image into for the puzzle. Defaults to (10,10).
        """

        self.surface = grid_surface_texture
        self.puzzle_rect = puzzle_rect
        self.scramble_rect = scramble_rect
        self.grid_size = grid_size

        self.generate_pieces()
        self.scramble()

    def scramble(self):
        for piece in self.pieces:
            x = self.scramble_rect.left + (self.scramble_rect.width - piece.rect.width)*random()
            y = self.scramble_rect.top + (self.scramble_rect.height - piece.rect.height)*random()
            piece.rect.topleft = x,y

    def generate_pieces(self):
        piece_size = (
            self.surface.get_width() // self.grid_size[0],
            self.surface.get_height() // self.grid_size[1]
        )

        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                piece_home = x*piece_size[0] + self.puzzle_rect[0], y*piece_size[1] + self.puzzle_rect[1]
                sample_position = x*piece_size[0], y*piece_size[1]
                p = Piece( piece_home, piece_size, self.surface, sample_position )

                self.pieces.append(p)

    def get_piece(self, coordinate):
        """Return the last piece found to contain coordinate

        Args:
            coordinate (2-tuple): The coordinate to look for a piece at (x,y)

        Returns:
            Piece: The puzzle piece the mouse was over
        """
        
        selected_piece = None
        for piece in self.pieces:
            if piece.rect.collidepoint(coordinate):
                selected_piece = piece
        
        return selected_piece


def draw_background(surf, offset):
    
    padding = 5

    surf.fill(colors['background'])
    surf.fill(colors['lines'], (offset-padding, offset-padding, surf.get_width()/2 + 2*padding, surf.get_height()-offset*2 + padding*2))
    surf.fill(colors['puzzle_area'], (offset, offset, surf.get_width()/2, surf.get_height()-offset*2))


def main():
    offset = 30
    pg.init()

    clock = pg.time.Clock()
    screen = pg.display.set_mode(SCREEN_SIZE)
    draw_background(screen, offset)
    
    puzzle_img = pg.image.load('media/default.png').convert()

    # Scale the image so that it fits in the assigned area.
    main_surf = pg.transform.scale(puzzle_img, (screen.get_width()//2, screen.get_height()-offset*2))
    main_surf_rect = main_surf.get_rect(topleft=(offset, offset))

    w = screen.get_width() - offset*2 - main_surf_rect.right
    h = screen.get_height() - offset*2
    scramble_rect = pg.Rect((main_surf_rect.right + offset, offset), (w,h))

    puzzle = Puzzle(main_surf, main_surf_rect, scramble_rect, (10,15))
    piece = None

    while(True):
        pg.display.flip()
        clock.tick(120)

        if piece is not None:
            piece.rect.center = pg.mouse.get_pos()

        draw_background(screen, offset)

        to_blit = []
        for p in puzzle.pieces:
            to_blit.append(p.draw())

        screen.blits(to_blit)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if piece is not None:
                    raise(Glutton(piece.rect.topleft, new_piece.rect.topleft))
                else:
                    piece = puzzle.get_piece(pg.mouse.get_pos())
            elif event.type == pg.MOUSEBUTTONUP:
                if piece is not None:
                    piece.drop()
                    piece = None
            
            elif event.type == pg.KEYDOWN:
                if event.key == ord('r'):
                    puzzle.scramble()

if os.getcwd() != "C:\\Users\\mikke\\projects\\om-nom-puzzle\\omnon":
    print(os.getcwd())
    os.chdir('omnom')
main()
