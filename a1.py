from __future__ import annotations

from random import shuffle
from typing import List, Tuple, Optional, Union, Dict

# Each raccoon moves every this many turns
RACCOON_TURN_FREQUENCY = 20

# Directions dx, dy
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [LEFT, UP, RIGHT, DOWN]


def get_shuffled_directions() -> List[Tuple[int, int]]:
    """
    Provided helper that returns a shuffled copy of DIRECTIONS.
    You should use this where appropriate
    """
    to_return = DIRECTIONS[:]
    shuffle(to_return)
    return to_return


class GameBoard:
    """A game board on which the game is played.

    === Public Attributes ===
    ended:
        whether this game has ended or not
    turns:
        how many turns have passed in the game
    width:
        the number of squares wide this board is
    height:
        the number of squares high this board is


    === Representation Invariants ===
    turns >= 0
    width > 0
    height > 0
    No tile in the game contains more than 1 character, except that a tile
    may contain both a Raccoon and an open GarbageCan.

    === Sample Usage ===
    See examples in individual method docstrings.
    """
    # === Private Attributes ===
    # _player:
    #   the player of the game
    # _board:
    #   a dictionary of a list of Characters used to keep track of all
    #   Characters on the board.  The keys will be the 2-tuples of valid
    #   integers which are on the board.  For each key, a list will exist to
    #   represent the characters on that specific tile on the board.  If no
    #   characters exist then the list will be empty.  If there is multiple
    #   characters (in the case of an open garbage bin and a racoon) then the
    #   list will have two characters, an open garbage bin and a raccoon
    #   character, in that order.
    # _raccoons:
    #    A list of all the raccoons on the gameboard, whether they are trapped
    #    or not.
    # _garbage_bins:
    #    A list of all the garbage bins on the gameboard.

    ended: bool
    turns: int
    width: int
    height: int
    _player: Optional[Player]
    _board: Dict[List[Union[Character, None]]]
    _raccoons: List[Raccoon]
    _garbage_bins: List[GarbageCan]

    def __init__(self, w: int, h: int) -> None:
        """Initialize this Board to be of the given width <w> and height <h> in
        squares. A board is initially empty (no characters) and no turns have
        been taken.

        >>> b = GameBoard(3, 3)
        >>> b.width == 3
        True
        >>> b.height == 3
        True
        >>> b.turns == 0
        True
        >>> b.ended
        False
        """
        self.ended = False
        self.turns = 0

        self.width = w
        self.height = h

        self._player = None
        d = {}
        for i in range(self.width):
            for j in range(self.height):
                d[(i, j)] = []
        self._board = d

        self._raccoons = []

        self._garbage_bins = []

    def place_character(self, c: Character) -> None:
        """Record that character <c> is on this board.

        This method should only be called from Character.__init__.

        The decisions you made about new private attributes for class GameBoard
        will determine what you do here.

        Preconditions:
        - c.board == self
        - Character <c> has not already been placed on this board.
        - The tile (c.x, c.y) does not already contain a character, with the
        exception being that a Raccoon can be placed on the same tile where
        an unlocked GarbageCan is already present.

        Note: The testing will depend on this method to set up the board,
        as the Character.__init__ method calls this method.

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)  # when a Raccoon is created, it is placed on b
        >>> b.at(1, 1)[0] == r  # requires GameBoard.at be implemented to work
        True
        """
        # Note: we can assume that on_board(c.x, c.y) is True

        # if <c> is a Player object
        if isinstance(c, Player):
            self._player = c

        elif isinstance(c, Raccoon):
            self._raccoons.append(c)
            # if <c> is a Raccoon object then we add it to the list of raccoons
            if self._board[(c.x, c.y)]:
                char = self._board[(c.x, c.y)][0]
                if isinstance(char, GarbageCan) and not char.locked:
                    c.inside_can = True
        # if <c> is Raccoon object and there exists an open GarbageCan on the
        # tile, then we have to make sure c.inside_can is changed to True

        elif isinstance(c, GarbageCan):
            self._garbage_bins.append(c)

        self._board[(c.x, c.y)].append(c)

    def at(self, x: int, y: int) -> List[Character]:
        """Return the characters at tile (x, y).

        If there are no characters or if the (x, y) coordinates are not
        on the board, return an empty list.
        There may be as many as two characters at one tile,
        since a raccoon can climb into a garbage can.

        Note: The testing will depend on this method to allow us to
        access the Characters on your board, since we don't know how
        you have chosen to store them in your private attributes,
        so make sure it is working properly!

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)
        >>> b.at(1, 1)[0] == r
        True
        >>> p = Player(b, 0, 1)
        >>> b.at(0, 1)[0] == p
        True
        """
        if not self.on_board(x, y):
            return []
        else:
            return self._board[(x, y)]

    def to_grid(self) -> List[List[chr]]:
        """
        Return the game state as a list of lists of chrs (letters) where:

        'R' = Raccoon
        'S' = SmartRaccoon
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        Each inner list represents one row of the game board.

        >>> b = GameBoard(3, 2)
        >>> _ = Player(b, 0, 0)
        >>> _ = Raccoon(b, 1, 1)
        >>> _ = GarbageCan(b, 2, 1, True)
        >>> b.to_grid()
        [['P', '-', '-'], ['-', 'R', 'C']]
        """
        lst = []
        # Set up lst so that it has the same number of empty inner lists as the
        # number of rows in the GameBoard
        for _ in range(self.height):
            lst.append([])

        for j in range(self.height):
            for i in range(self.width):  # So (i, j) is the tile (i, j)
                # on the board
                lst_of_chars = self._board[(i, j)]

                if not lst_of_chars:  # if lst_of_chars empty
                    lst[j].append('-')

                # So we can assume lst_of_chars not empty list
                else:
                    last_char = lst_of_chars[-1]
                    ch = last_char.get_char()
                    lst[j].append(ch)

        return lst

    def __str__(self) -> str:
        """
        Return a string representation of this board.

        The format is the same as expected by the setup_from_grid method.

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 1)
        >>> print(b)
        ---
        -R-
        >>> _ = Player(b, 0, 0)
        >>> _ = GarbageCan(b, 2, 1, False)
        >>> print(b)
        P--
        -RO
        >>> str(b)
        'P--\\n-RO'
        """
        grid_list = self.to_grid()
        s = ''
        for row in grid_list:
            for ch in row:
                s += ch
            s += '\n'
        return s.strip()

    def setup_from_grid(self, grid: str) -> None:
        """
        Set the state of this GameBoard to correspond to the string <grid>,
        which represents a game board using the following chars:

        'R' = Raccoon not in a GarbageCan
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        There is a newline character between each board row.

        >>> b = GameBoard(4, 4)
        >>> b.setup_from_grid('P-B-\\n-BRB\\n--BB\\n-C--')
        >>> str(b)
        'P-B-\\n-BRB\\n--BB\\n-C--'
        """
        lines = grid.split("\n")
        width = len(lines[0])
        height = len(lines)
        self.__init__(width, height)  # reset the board to an empty board
        y = 0
        for line in lines:
            x = 0
            for char in line:
                if char == 'R':
                    Raccoon(self, x, y)
                elif char == 'S':
                    SmartRaccoon(self, x, y)
                elif char == 'P':
                    Player(self, x, y)
                elif char == 'O':
                    GarbageCan(self, x, y, False)
                elif char == 'C':
                    GarbageCan(self, x, y, True)
                elif char == 'B':
                    RecyclingBin(self, x, y)
                elif char == '@':
                    GarbageCan(self, x, y, False)
                    Raccoon(self, x, y)  # always makes it a Raccoon
                    # Note: the order mattered above, as we have to place the
                    # Raccoon BEFORE the GarbageCan (see the place_character
                    # method precondition)
                x += 1
            y += 1

    # a helper method you may find useful in places
    def on_board(self, x: int, y: int) -> bool:
        """Return True iff the position x, y is within the boundaries of this
        board (based on its width and height), and False otherwise.
        """
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def give_turns(self) -> None:
        """Give every turn-taking character one turn in the game.

        The Player should take their turn first and the number of turns
        should be incremented by one. Then each other TurnTaker
        should be given a turn if RACCOON_TURN_FREQUENCY turns have occurred
        since the last time the TurnTakers were given their turn.

        After all turns are taken, check_game_end should be called to
        determine if the game is over.

        Precondition:
        self._player is not None

        >>> b = GameBoard(4, 3)
        >>> p = Player(b, 0, 0)
        >>> r = Raccoon(b, 1, 1)
        >>> b.turns
        0
        >>> for _ in range(RACCOON_TURN_FREQUENCY - 1):
        ...     b.give_turns()
        >>> b.turns == RACCOON_TURN_FREQUENCY - 1
        True
        >>> (r.x, r.y) == (1, 1)  # Raccoon hasn't had a turn yet
        True
        >>> (p.x, p.y) == (0, 0)  # Player hasn't had any inputs
        True
        >>> p.record_event(RIGHT)
        >>> b.give_turns()
        >>> (r.x, r.y) != (1, 1)  # Raccoon has had a turn!
        True
        >>> (p.x, p.y) == (1, 0)  # Player moved right!
        True
        """
        self._player.take_turn()
        self.turns += 1  # PROVIDED, DO NOT CHANGE

        if self.turns % RACCOON_TURN_FREQUENCY == 0:  # PROVIDED, DO NOT CHANGE
            for raccoon in self._raccoons:
                raccoon.take_turn()

        self.check_game_end()  # PROVIDED, DO NOT CHANGE

    def handle_event(self, event: Tuple[int, int]) -> None:
        """Handle a user-input event.

        The board's Player records the event that happened, so that when the
        Player gets a turn, it can make the move that the user input indicated.
        """
        self._player.record_event(event)

    def check_game_end(self) -> Optional[int]:
        """Check if this game has ended. A game ends when all the raccoons on
        this game board are either inside a can or trapped.

        If the game has ended:
        - update the ended attribute to be True
        - Return the score, where the score is given by:
            (number of raccoons trapped) * 10 + the adjacent_bin_score
        If the game has not ended:
        - update the ended attribute to be False
        - return None

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 0)
        >>> _ = Player(b, 0, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> b.check_game_end() is None
        True
        >>> b.ended
        False
        >>> _ = RecyclingBin(b, 2, 0)
        >>> b.check_game_end()
        11
        >>> b.ended
        True
        """
        for raccoon in self._raccoons:
            if not raccoon.check_trapped():
                self.ended = False
                return None

        self.ended = True
        trapped_num = self.trapped_num()
        return trapped_num * 10 + self.adjacent_bin_score()

    def adjacent_bin_score(self) -> int:
        """
        Return the size of the largest cluster of adjacent recycling bins
        on this board.

        Two recycling bins are adjacent when they are directly beside each other
        in one of the four directions (up, down, left, right).

        See Task #5 in the handout for ideas if you aren't sure how
        to approach this problem.

        >>> b = GameBoard(3, 3)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> print(b)
        B--
        -B-
        --B
        >>> b.adjacent_bin_score()
        1
        >>> _ = RecyclingBin(b, 2, 1)
        >>> print(b)
        B--
        -BB
        --B
        >>> b.adjacent_bin_score()
        3
        >>> _ = RecyclingBin(b, 0, 1)
        >>> print(b)
        B--
        BBB
        --B
        >>> b.adjacent_bin_score()
        5
        """
        pass

    # === Helper Methods === #
    def movebins(self, bins_list: List[RecyclingBin], direction: Tuple[int,
                                                                       int]) \
            -> None:
        """Moves all the recycling bins in bins_list.
        Pre-condition: the bins_list gives us a collection of RecyclingBin
        objects currently on self and are capable of moving in <direction>."""
        bins_list_reversed = bins_list.copy()
        bins_list_reversed.reverse()
        for rbin in bins_list_reversed:
            rbin._move(direction)

    def get_garbage(self) -> List[GarbageCan]:
        """Gives access to private attribute _garbage_bins."""
        return self._garbage_bins

    def trapped_num(self) -> int:
        """Returns the number of trapped Raccoon on the gameboard."""
        num = 0
        for raccoon in self._raccoons:
            if raccoon.check_trapped():
                num += 1
        return num


class Character:
    """A character that has (x,y) coordinates and is associated with a given
    board.

    This class is abstract and should not be directly instantiated.

    NOTE: To reduce the amount of documentation in subclasses, we have chosen
    not to repeat information about the public attributes in each subclass.
    Remember that the attributes are not inherited, but only exist once we call
    the __init__ of the parent class.

    === Public Attributes ===
    board:
        the game board that this Character is on
    x, y:
        the coordinates of this Character on the board

    === Representation Invariants ===
    x, y are valid coordinates in board (i.e. board.on_board(x, y) is True)
    """
    board: GameBoard
    x: int
    y: int

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Character with board <b>, and
        at tile (<x>, <y>).

        When a Character is initialized, it is placed on board <b>
        by calling the board's place_character method. Refer to the
        preconditions of place_character, which must be satisfied.
        """
        self.board = b
        self.x, self.y = x, y
        self.board.place_character(self)  # this associates self with the board!
        #  The above line allows the board to know which characters are on it

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Move this character to the tile

        (self.x + direction[0], self.y + direction[1]) if possible. Each child
        class defines its own version of what is possible.

        Return True if the move was successful and False otherwise.

        """
        raise NotImplementedError

    def _move(self, direction: Tuple[int, int]) -> None:
        """Moving a single character <self> in <direction>.
        Pre-condition: <self> can be moved in <direction> on the board
        self.board.  (So additionally we can assume (self.x + direction[0],
        self.y + direction[1]) is on the board.)"""
        b = self.board
        # Delete location of <self> on self.board
        b.at(self.x, self.y).clear()

        # Change the (x,y) coordinates of <self>
        self.x, self.y = self.x + direction[0], self.y + direction[1]

        # Update new location of <self> on self.board
        b.at(self.x, self.y).extend([self])

    def get_char(self) -> chr:
        """
        Return a single character (letter) representing this Character.
        """
        raise NotImplementedError


# Note: You can safely ignore PyCharm's warning about this class
# not implementing abstract method(s) from its parent class.
class TurnTaker(Character):
    """
    A Character that can take a turn in the game.

    This class is abstract and should not be directly instantiated.
    """

    def take_turn(self) -> None:
        """
        Take a turn in the game. This method must be implemented in any subclass
        """
        raise NotImplementedError


class RecyclingBin(Character):
    """A recycling bin in the game.

    === Sample Usage ===
    >>> rb = RecyclingBin(GameBoard(4, 4), 2, 1)
    >>> rb.x, rb.y
    (2, 1)
    """

    def move(self, direction: Tuple[int, int]) -> bool:
        """Move this recycling bin to tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return whether or not this move was successful.

        If the new tile is occupied by another RecyclingBin, push
        that RecyclingBin one tile away in the same direction and take
        its tile (as described in the Assignment 1 handout).

        If the new tile is occupied by any other Character or if it
        is beyond the boundaries of the board, do nothing and return False.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> rb = RecyclingBin(b, 0, 0)
        >>> rb.move(UP)
        False
        >>> rb.move(DOWN)
        True
        >>> b.at(0, 1) == [rb]
        True
        """
        bins_lst = [self]
        if self._accumulate(direction, bins_lst):
            self.board.movebins(bins_lst, direction)
            return True
        else:
            return False

    def _accumulate(self, direction: Tuple[int, int],
                    bins_lst: List[RecyclingBin]) -> bool:
        """this function basically adds all the recycling bins that will be
        moved if the direction is valid.  It returns True if the move is valid,
        and False if it isn't."""
        b = self.board
        num = 1
        while b.on_board(self.x + num * direction[0],
                         self.y + num * direction[1]):
            if not b.at(self.x + num * direction[0],
                        self.y + num * direction[1]):  # if the list is empty
                return True  # next spot is an empty space so we
                # can move the bins
            elif isinstance(b.at(self.x + num * direction[0],
                                 self.y + num * direction[1])[0],
                            RecyclingBin):
                bins_lst.append(b.at(self.x + num * direction[0],
                                     self.y + num * direction[1])[0])
                num += 1  # next tile has a recycling bin
            else:
                # next tile has another character
                return False
        return False

    def get_char(self) -> chr:
        """
        Return the character 'B' representing a RecyclingBin.
        """
        return 'B'


class Player(TurnTaker):
    """The Player of this game.

    === Sample Usage ===
    >>> b = GameBoard(3, 1)
    >>> p = Player(b, 0, 0)
    >>> p.record_event(RIGHT)
    >>> p.take_turn()
    >>> (p.x, p.y) == (1, 0)
    True
    >>> g = GarbageCan(b, 0, 0, False)
    >>> p.move(LEFT)
    True
    >>> g.locked
    True
    """
    # === Private Attributes ===
    # _last_event:
    #   The direction corresponding to the last keypress event that the user
    #   made, or None if there is currently no keypress event left to process
    _last_event: Optional[Tuple[int, int]]

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Player with board <b>,
        and at tile (<x>, <y>)."""

        TurnTaker.__init__(self, b, x, y)
        self._last_event = None

    def record_event(self, direction: Tuple[int, int]) -> None:
        """Record that <direction> is the last direction that the user
        has specified for this Player to move. Next time take_turn is called,
        this direction will be used.
        Precondition:
        direction is in DIRECTIONS
        """
        self._last_event = direction

    def take_turn(self) -> None:
        """Take a turn in the game.

        For a Player, this means responding to the last user input recorded
        by a call to record_event.
        """
        if self._last_event is not None:
            self.move(self._last_event)
            self._last_event = None

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Player to the tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return True if the move is successful.

        If the new tile is occupied by a Racooon, a locked GarbageCan, or if it
        is beyond the boundaries of the board, do nothing and return False.

        If the new tile is occupied by a movable RecyclingBin, the player moves
        the RecyclingBin and moves to the new tile.

        If the new tile is unoccupied, the player moves to that tile.

        If a Player attempts to move towards an empty, unlocked GarbageCan, the
        GarbageCan becomes locked. The player's position remains unchanged in
        this case. Also return True in this case, as the Player has performed
        the action of locking the GarbageCan.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> p = Player(b, 0, 0)
        >>> p.move(UP)
        False
        >>> p.move(DOWN)
        True
        >>> b.at(0, 1) == [p]
        True
        >>> _ = RecyclingBin(b, 1, 1)
        >>> p.move(RIGHT)
        True
        >>> b.at(1, 1) == [p]
        True
        """
        b = self.board
        if not b.on_board(self.x + direction[0], self.y + direction[1]):
            # next tile is not on the board
            return False
        else:
            # can assume next tile is on the board
            lst_of_chars = b.at(self.x + direction[0], self.y + direction[1])
            if not lst_of_chars:
                # the case where the next_tile is empty
                self._move(direction)
                return True
            elif lst_of_chars[-1].get_char() == 'O':
                # the case where next_tile has an open can
                lst_of_chars[-1].locked = True
                return True
            elif lst_of_chars[-1].get_char() == 'B':
                # the case where next_tile has a recycling bin
                if lst_of_chars[0].move(direction):
                    # if the bin can be moved, then move self
                    self._move(direction)
                    return True
                return False  # the bin(s) could not be moved
            return False  # the other cases

    def get_char(self) -> chr:
        """
        Return the character 'P' representing this Player.
        """
        return 'P'


class Raccoon(TurnTaker):
    """A raccoon in the game.

    === Public Attributes ===
    inside_can:
        whether or not this Raccoon is inside a garbage can

    === Representation Invariants ===
    inside_can is True iff this Raccoon is on the same tile as an open
    GarbageCan.

    === Sample Usage ===
    >>> r = Raccoon(GameBoard(11, 11), 5, 10)
    >>> r.x, r.y
    (5, 10)
    >>> r.inside_can
    False
    """
    inside_can: bool

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Raccoon with board <b>, and
        at tile (<x>, <y>). Initially a Raccoon is not inside
        of a GarbageCan, unless it is placed directly inside an open GarbageCan.
        """
        self.inside_can = False
        # since this raccoon may be placed inside an open garbage can,
        # we need to initially set the inside_can attribute
        # BEFORE calling the parent init, which is where the raccoon is actually
        # placed on the board.
        TurnTaker.__init__(self, b, x, y)

    def check_trapped(self) -> bool:
        """Return True iff this raccoon is trapped. A trapped raccoon is
        surrounded on 4 sides (diagonals don't matter) by recycling bins, other
        raccoons (including ones in garbage cans), the player, and/or board
        edges. Essentially, a raccoon is trapped when it has nowhere it could
        move.

        Reminder: A racooon cannot move diagonally.

        >>> b = GameBoard(3, 3)
        >>> r = Raccoon(b, 2, 1)
        >>> _ = Raccoon(b, 2, 2)
        >>> _ = Player(b, 2, 0)
        >>> r.check_trapped()
        False
        >>> _ = RecyclingBin(b, 1, 1)
        >>> r.check_trapped()
        True
        """
        for direction in DIRECTIONS:
            if self._can_move(direction):
                return False
        return True

    def _can_move(self, direction: Tuple[int, int]) -> bool:
        """Returns whether <self> (a Raccoon) can move in this direction.
        Valid moves include moving onto empty tiles or into garbage cans (both
        open and closed).
        This method does not enact the move - it just returns whether
        such a move in this direction is possible.
        This method does not assume that (self.x + direction[0],
        self.y + direction[1]) is on the board."""
        # (x, y) will be the candidate tile to move to
        x, y = self.x + direction[0], self.y + direction[1]
        b = self.board

        if not b.on_board(x, y):
            # (x,y) is not on the board
            return False
        else:
            # can assume (x,y) on the board
            if not b.at(x, y):  # if the tile at (x, y) is empty
                return True
            # can now assume b.at(x, y) is not empty
            elif b.at(x, y)[-1].get_char() in ['O', 'C']:
                # if the tile at (x, y) has only an open garbage bin (with no
                # raccoon in it) or a closed garbage bin
                return True
            else:
                return False

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Raccoon in <direction> and return whether
        or not this was successful.

        If the tile one tile over in that direction is occupied by the Player,
        a RecyclingBin, or another Raccoon, OR if the tile is not within the
        boundaries of the board, do nothing and return False.

        If the tile is occupied by an unlocked GarbageCan that has no Raccoon
        in it, this Raccoon moves there and we have two characters on one tile
        (the GarbageCan and the Raccoon). If the GarbageCan is locked, this
        Raccoon uses this turn to unlock it and return True.

        If a Raccoon is inside of a GarbageCan, it will not move. Do nothing and
        return False.

        Return True if the Raccoon unlocks a GarbageCan or moves from its
        current tile.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> r = Raccoon(b, 0, 0)
        >>> r.move(UP)
        False
        >>> r.move(DOWN)
        True
        >>> b.at(0, 1) == [r]
        True
        >>> g = GarbageCan(b, 1, 1, True)
        >>> r.move(RIGHT)
        True
        >>> r.x, r.y  # Raccoon didn't change its position
        (0, 1)
        >>> not g.locked  # Raccoon unlocked the garbage can!
        True
        >>> r.move(RIGHT)
        True
        >>> r.inside_can
        True
        >>> len(b.at(1, 1)) == 2  # Raccoon and GarbageCan are both at (1, 1)!
        True
        """
        b = self.board
        if self.inside_can:
            return False
        else:
            # Can assume now that the self is not in a garbage can.
            # Hence it has the ability to move
            if self._can_move(direction):
                x, y = self.x + direction[0], self.y + direction[1]
                char_lst = b.at(x, y)  # list of characters at (x,y)
                # case 1: (x,y) is empty
                if not char_lst:
                    self._move(direction)
                    return True
                # case 2: (x,y) has closed garbage can
                elif char_lst[-1].get_char() == 'C':
                    char_lst[-1].locked = False
                    return True
                # case 3: (x,y) has open garbage can
                elif char_lst[-1].get_char() == 'O':
                    self._move(direction)
                    self.inside_can = True
                    return True
            return False

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a Raccoon is in a GarbageCan, it stays where it is.

        Otherwise, it randomly attempts (if it is not blocked) to move in
        one of the four directions, with equal probability.

        >>> b = GameBoard(3, 4)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1.take_turn()
        >>> (r1.x, r1.y) in [(0, 1), (1, 0)]
        True
        >>> r2 = Raccoon(b, 2, 1)
        >>> _ = RecyclingBin(b, 2, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> r2.take_turn()  # Raccoon is trapped
        >>> r2.x, r2.y
        (2, 1)
        """
        if self.inside_can:
            return None

        # Can assume raccoon not in a garbage can.  hence it has possibility
        # of movement
        possible_dir = []
        for direction in DIRECTIONS:
            if self._can_move(direction):
                possible_dir.append(direction)

        if possible_dir:  # if this list is not empty
            shuffle(possible_dir)
            self.move(possible_dir[0])
        return None

    def get_char(self) -> chr:
        """
        Return '@' to represent that this Raccoon is inside a garbage can
        or 'R' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'R'


class SmartRaccoon(Raccoon):
    """A smart raccoon in the game.

    Behaves like a Raccoon, but when it takes a turn, it will move towards
    a GarbageCan if it can see that GarbageCan in its line of sight.
    See the take_turn method for details.

    SmartRaccoons move in the same way as Raccoons.

    === Sample Usage ===
    >>> b = GameBoard(8, 1)
    >>> s = SmartRaccoon(b, 4, 0)
    >>> s.x, s.y
    (4, 0)
    >>> s.inside_can
    False
    """

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a SmartRaccoon is in a GarbageCan, it stays where it is.

        A SmartRaccoon checks along the four directions for
        the closest non-occupied GarbageCan that has nothing blocking
        it from reaching that GarbageCan (except possibly the Player).

        If there is a tie for the closest GarbageCan, a SmartRaccoon
        will prioritize the directions in the order indicated in DIRECTIONS.

        If there are no GarbageCans in its line of sight along one of the four
        directions, it moves exactly like a Raccoon. A GarbageCan is in its
        line of sight if there are no other Raccoons, RecyclingBins, or other
        GarbageCans between this SmartRaccoon and the GarbageCan. The Player
        may be between this SmartRaccoon and the GarbageCan though.

        >>> b = GameBoard(8, 2)
        >>> s = SmartRaccoon(b, 4, 0)
        >>> _ = GarbageCan(b, 3, 1, False)
        >>> _ = GarbageCan(b, 0, 0, False)
        >>> _ = GarbageCan(b, 7, 0, False)
        >>> s.take_turn()
        >>> s.x == 5
        True
        >>> s.take_turn()
        >>> s.x == 6
        True
        """
        if self.inside_can:
            return None

        # Can assume self is not in a garbage can.

        direction = self._find_closest_path()
        if direction is None:
            Raccoon.take_turn(self)
            return None
        else:
            self._move(direction)
            return None

    def _find_closest_path(self) -> Optional[Tuple[int, int]]:
        """Returns the direction for <self> to travel in that is the closest
        direct path to an unoccupied garbage can, with tie-breaking defined by
        whichever direction appears first in DIRECTION.
        A valid direct path from a raccoon to an unoccupied garbage can is when
        the garbage can is in its line of sight and no other raccoon or
        garbage can interrupts the path (other than a player).
        Will return direction if a closest path exists. Otherwise, will return
        None."""
        d = []
        for direction in DIRECTIONS:
            tup = self._is_valid_path(direction)
            if tup[0]:
                d.append([direction, tup[1]])

        if not d:  # if d is empty
            return None
        else:
            min_path = d[0][1]
            min_direction = d[0][0]
            for lst in d:
                if lst[1] < min_path:
                    min_path = lst[1]
                    min_direction = lst[0]
            return min_direction

    def _is_valid_path(self, direction: Tuple[int, int]) -> Tuple[bool, int]:
        """Determines if there is a valid direct path from given <self> in
        <direction>.  If there is one, it returns a tuple where the first value
        is True and the second value is the length of the direct path.
        If no such path exists, returns (False, 0). """
        unoccupied_g = []
        b = self.board
        for gb in b.get_garbage():
            if len(b.at(gb.x, gb.y)) == 1:
                # No raccoon in gb so it's unoccupied
                unoccupied_g.append(gb)

        num = 1
        while b.on_board(self.x + num * direction[0],
                         self.y + num * direction[1]):
            char_lst = b.at(self.x + num * direction[0],
                            self.y + num * direction[1])

            # case 1: candidate tile is empty or has the player
            if not char_lst or char_lst[-1].get_char() == 'P':
                num += 1
            # case 2: candidate tile has a garbage can in unoccupied_g
            elif char_lst[-1].get_char() in ['C', 'O'] and \
                    char_lst[-1] in unoccupied_g:
                return True, num
            # case 3: meets a tile with another character in the way
            else:
                return False, 0
        return False, 0

    def get_char(self) -> chr:
        """
        Return '@' to represent that this SmartRaccoon is inside a Garbage Can
        and 'S' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'S'


class GarbageCan(Character):
    """A garbage can in the game.

    === Public Attributes ===
    locked:
        whether or not this GarbageCan is locked.

    === Sample Usage ===
    >>> b = GameBoard(2, 2)
    >>> g = GarbageCan(b, 0, 0, False)
    >>> g.x, g.y
    (0, 0)
    >>> g.locked
    False
    """
    locked: bool

    def __init__(self, b: GameBoard, x: int, y: int, locked: bool) -> None:
        """Initialize this GarbageCan to be at tile (<x>, <y>) and store
        whether it is locked or not based on <locked>.
        """

        Character.__init__(self, b, x, y)
        self.locked = locked

    def get_char(self) -> chr:
        """
        Return 'C' to represent a closed garbage can and 'O' to represent
        an open garbage can.
        """
        if self.locked:
            return 'C'
        return 'O'

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Garbage cans cannot move, so always return False.
        """
        return False


# A helper function you may find useful for Task #5, depending on how
# you implement it.
def get_neighbours(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Return the coordinates of the four tiles adjacent to <tile>.

    This does NOT check if they are valid coordinates of a board.

    >>> ns = set(get_neighbours((2, 3)))
    >>> {(2, 2), (2, 4), (1, 3), (3, 3)} == ns
    True
    """
    rslt = []
    for direction in DIRECTIONS:
        rslt.append((tile[0] + direction[0], tile[1] + direction[1]))
    return rslt


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': [],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', '__future__', 'math'],
        'disable': ['E1136'],
        'max-attributes': 15,
        'max-module-lines': 1600
    })
