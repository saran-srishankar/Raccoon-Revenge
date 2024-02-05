"""A1: The main program for the Raccoon Raiders game.  There are no tasks for
you to do in this module

CSC148, Winter 2022

This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of this
code, whether as given or with any changes, are expressly prohibited.

Authors: Diane Horton, Sadia Sharmin, Dina Sabie,
         Sophia Huynh, and Jonathan Calver

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Diane Horton, Sadia Sharmin, Dina Sabie,
                   Sophia Huynh, and Jonathan Calver.

=== Module Description ===
This module contains the main program that calls upon the classes specified in
a1.py.
"""

import sys
from random import random, shuffle
from typing import Dict, List, Optional

import pygame
import a1

# Feel free to modify any of these constant values.

# Game Screen dimensions in pixels
SCREEN_WIDTH = 1500  # 1165
SCREEN_HEIGHT = 600  # 733

# Dimensions of the game board, in squares.
BOARD_WIDTH = 10  # 20
BOARD_HEIGHT = 10  # 15

# Number of each type of Character to include in a random game
NUM_RACCOONS = 4
NUM_GARBAGE_CANS = 4
NUM_RECYCLING_BINS = int(BOARD_HEIGHT * BOARD_WIDTH * 0.25)

# Number of milliseconds to wait between iterations of the main game loop.
# This changes the speed of the game. The main player can move at most
# once every LOOP_DELAY milliseconds.
LOOP_DELAY = 100

# Fraction of garbage cans that are to be locked at the start of the game.
FRACTION_LOCKED = 0.1

# Fraction of "smart" raccoons
FRACTION_SMART = 0.5

# Character icons
BACKGROUND_ICON = 'icons/background.png'
GARBAGE_CAN_OPEN_ICON = 'icons/open.png'
GARBAGE_CAN_CLOSED_ICON = 'icons/closed.png'
PERSON_ICON = 'icons/person.png'
SMART_RACCOON_ICON = 'icons/smart.png'
RACCOON_ICON = 'icons/raccoon.png'
RECYCLING_ICON = 'icons/recycling.png'
RACCOON_IN_BIN_ICON = 'icons/raccoon_in_bin.png'


def make_image(icon_file: str, width: int, height: int) -> pygame.surface:
    """
    A helper function for loading <icon_file> as a pygame image
    and scaling it to have dimensions <width> and <height>
    """
    pic = pygame.image.load(icon_file)
    return pygame.transform.scale(pic, (width, height))


class RaccoonRaiders:
    """The user interface for the Raccoon Raiders game!

    === Public Attributes ===
    width:
        width of the underlying game board
    height:
        height of the underlying game board
    square_size:
        size of each square in the game
    """
    # === Private Attributes ===
    # _board:
    #     the board containing the state of the game
    # _screen:
    #     the pygame screen to draw the stage on
    # _icon_map:
    #     the mapping from character (letter) representation to image icons
    # _background_tile:
    #     image icon for the background
    # _last_state:
    #     the string representation of the last board state that was drawn

    width: int
    height: int
    square_size: int
    _board: a1.GameBoard
    _screen: pygame.Surface
    _icon_map: Dict[chr, pygame.Surface]
    _background_tile: pygame.Surface
    _last_state: Optional[List[List[chr]]]

    def __init__(self, w: int, h: int, board_string: str = "") -> None:
        """Initialize this game to be of the given width <w> and height <h> in
        squares. If <board_string> is not specified, then a random board
        is generated. Otherwise, GameBoard.setup_from_grid is used to populate
        the board.
        """

        self._board = a1.GameBoard(w, h)

        if board_string:
            self._board.setup_from_grid(board_string)
        else:
            populate_board(self._board,
                           NUM_RACCOONS,
                           NUM_GARBAGE_CANS,
                           NUM_RECYCLING_BINS)

        self.square_size = min(int(SCREEN_WIDTH / w),
                               int(SCREEN_HEIGHT / h))

        # Initialize a window of these pixel dimensions for display
        self._screen = pygame.display.set_mode((w * self.square_size,
                                                h * self.square_size)
                                               )

        # a function defined for convenience that we use to set up the
        # _icon_map below.
        def image_loader(x: str) -> pygame.surface:
            return make_image(x, self.square_size, self.square_size)

        # Initialize the background tile
        self._background_tile = image_loader(BACKGROUND_ICON)

        self._icon_map = {'R': image_loader(RACCOON_ICON),
                          'S': image_loader(SMART_RACCOON_ICON),
                          'C': image_loader(GARBAGE_CAN_CLOSED_ICON),
                          'O': image_loader(GARBAGE_CAN_OPEN_ICON),
                          '@': image_loader(RACCOON_IN_BIN_ICON),
                          'B': image_loader(RECYCLING_ICON),
                          'P': image_loader(PERSON_ICON)
                          }

        self._last_state = None
        self.height, self.width = self._board.height, self._board.width

    def draw(self) -> None:
        """
        Draw the given board state using pygame and also print it to the
        terminal in a text representation.
        """
        state = self._board.to_grid()
        changed = self._last_state != state
        if changed:  # also print the board to the console, feel free to remove
            print(f'\n{self._board}')
        self._last_state = state

        for x in range(len(state[0])):  # will fail until Task #1 is done
            for y in range(len(state)):
                c = state[y][x]
                rectangle = pygame.Rect(x * self.square_size,
                                        y * self.square_size,
                                        self.square_size, self.square_size)
                # Draw the icon onto the rectangle.
                self._screen.blit(self._background_tile, (x * self.square_size,
                                                          y * self.square_size))
                if c in self._icon_map:
                    self._screen.blit(self._icon_map[c], rectangle)

        # Update the screen.
        pygame.display.flip()

    def play(self) -> None:
        """
        Play the game!
        """
        while not self._board.ended:
            pygame.time.wait(LOOP_DELAY)
            # Handle all inputs that are in the event queue,
            # i.e., that occurred since the last iteration.
            self._handle_user_input()

        # game has ended, print message
        score = self._board.check_game_end()
        print(f"Game has ended. Your score is {score}")

        pygame.font.init()
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        # now print the text
        text_surface = font.render(f"Your Score: {score}",
                                   False, (0, 0, 0))
        self._screen.blit(text_surface, dest=(0,
                                              (self.square_size
                                               * self.height) // 2))
        pygame.display.flip()
        # Keep the screen on after the game has ended. You need to
        # close the pygame window to end the program.
        while True:
            pygame.time.wait(LOOP_DELAY * 5)
            for event in pygame.event.get():
                # Stop if user closed the window.
                if event.type == pygame.constants.QUIT:
                    sys.exit()

    def _handle_user_input(self) -> None:
        """Handle user input, give characters their turns, and
        redraw the game board.
        """
        for event in pygame.event.get():  # process all key presses
            # Stop if user closed the window.
            if event.type == pygame.constants.QUIT:
                sys.exit()
            if event.type == pygame.constants.KEYDOWN:
                dx, dy = None, None
                if event.key == pygame.constants.K_DOWN:
                    dx, dy = 0, 1
                if event.key == pygame.constants.K_LEFT:
                    dx, dy = -1, 0
                if event.key == pygame.constants.K_RIGHT:
                    dx, dy = 1, 0
                if event.key == pygame.constants.K_UP:
                    dx, dy = 0, -1
                if dx is not None:
                    self._board.handle_event((dx, dy))
        # Give every character a turn in the game and draw the board.
        self._board.give_turns()
        self.draw()


# this depends on your place_character method in the GameBoard class
# in order to work, since
# Character.__init__ relies on GameBoard.place_character!
def populate_board(board: a1.GameBoard, num_raccoons: int,
                   num_cans: int, num_bins: int) -> None:
    """Place characters on this board.

    The board will have one player at the top-left corner of the board,
    and the given number of raccoons, garbage cans and recycling bins
    all at random, not already occupied, locations on the board.

    FRACTION_LOCKED and FRACTION_SMART dictate the probability that
    each GarbageCan is locked and
    each Raccoon is a SmartRaccoon, respectively.

     Precondition:
        - num_raccoons >= 0
        - num_cans >= 0
        - num_bins >= 0
        - num_raccoons + num_bins + num_cans + 1 <= number of locations
          on the board!
        - board is initially empty

    >>> b = a1.GameBoard(3, 1)
    >>> populate_board(b,1,0,1)
    >>> str(b) in ['PRB', 'PBR', 'PSB', 'PBS']
    True
    """
    a1.Player(board, 0, 0)

    # get the set of all possible locations on the board and
    # randomly place characters in them.
    availables = []
    for i in range(board.width):
        for j in range(board.height):
            availables.append((i, j))
    availables.remove((0, 0))

    shuffle(availables)

    for _ in range(num_raccoons):
        x, y = availables.pop()
        if random() <= FRACTION_SMART:
            a1.SmartRaccoon(board, x, y)
        else:
            a1.Raccoon(board, x, y)

    for _ in range(num_cans):
        x, y = availables.pop()
        locked = random() <= FRACTION_LOCKED
        a1.GarbageCan(board, x, y, locked)

    for _ in range(num_bins):
        x, y = availables.pop()
        a1.RecyclingBin(board, x, y)


if __name__ == '__main__':
    random_game = False  # set to True to play on a random board
    if random_game:
        rc = RaccoonRaiders(BOARD_WIDTH,
                            BOARD_HEIGHT)
        # for random board, you can adjust settings at top of this file
    else:
        # game board from handout animation
        game_string = "P-O----S\n---BBB-\n------B-\n-BRBB-O-\n" \
                      "---B-B--\n--O---S-"
        rc = RaccoonRaiders(8, 6, game_string)

        # uncomment the below for bin moving demo in handout
        # game_string = "R-P-B-BB--O "
        # rc = RaccoonRaiders(len(game_string), 1, game_string)

    rc.play()
