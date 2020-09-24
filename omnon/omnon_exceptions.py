class Glutton(Exception):
    def __init__(self, carried_piece, new_piece):
        super().__init__("Someone's hungry. Attempted to bite piece at {carried_piece.pos} while carrying piece from {new_piece.pos}")