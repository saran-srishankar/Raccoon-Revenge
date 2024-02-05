from a1 import *


def test_empty_gameboard_init() -> None:
    """Test GameBoard.__init__"""
    b = GameBoard(4, 3)
    assert b.width == 4
    assert b.height == 3
    assert b.turns == 0
    assert b.ended == False
    assert b._board == {(0,0): [], (1,0): [], (2,0): [], (3,0): [], (0,1): [],
                        (1,1): [], (2,1): [], (3,1): [], (0,2): [], (1, 2): [],
                        (2,2): [], (3,2): []}


def test_to_grid() -> None:
    """Test GameBoard.to_grid"""
    b = GameBoard(4, 3)
    p = Player(b, 0, 0)
    _ = SmartRaccoon(b, 2, 0)
    _ = Raccoon(b, 3, 0)
    _ = GarbageCan(b, 0, 1, True)
    _ = GarbageCan(b, 1, 1, False)
    _ = RecyclingBin(b, 2, 1)
    _ = GarbageCan(b, 1, 2, False)
    _ = Raccoon(b, 1, 2)

    assert b._player == p
    assert b.to_grid() == [['P', '-', 'S', 'R'], ['C', 'O', 'B', '-'],
                                ['-', '@', '-', '-']]


def test_recyclingbinmove1() -> None:
    b = GameBoard(4,2)
    rb1 = RecyclingBin(b, 0, 0)
    rb2 = RecyclingBin(b, 1, 0)
    assert rb1.move(RIGHT) == True
    assert b.at(0, 0) == []
    assert b.at(1, 0) == [rb1]
    assert b.at(2, 0) == [rb2]


def test_recyclingbinmove2() -> None:
    b = GameBoard(4,2)
    rb1 = RecyclingBin(b, 0, 0)
    rb2 = RecyclingBin(b, 1, 0)
    g = GarbageCan(b, 2, 0, True)
    assert rb1.move(RIGHT) == False
    assert b.at(0, 0) == [rb1]
    assert b.at(1, 0) == [rb2]
    assert b.at(2, 0) == [g]


def test_recyclingbinmove3() -> None:
    b = GameBoard(4,2)
    rb1 = RecyclingBin(b, 0, 0)
    rb2 = RecyclingBin(b, 1, 0)
    assert rb2.move(LEFT) == False
    assert b.at(0, 0) == [rb1]
    assert b.at(1, 0) == [rb2]


def test_player_move1() -> None:
    """Testing Player.move basic functionality on an open board via all
    directions."""
    b = GameBoard(4,3)
    p = Player(b, 0, 0)

    assert p.move(RIGHT) == True
    assert b.at(0, 0) == []
    assert b.at(1, 0) == [p]

    assert p.move(RIGHT) == True
    assert b.at(1, 0) == []
    assert b.at(2, 0) == [p]

    p.move(RIGHT)
    assert p.move(RIGHT) == False
    assert p.move(UP) == False
    assert p.move(DOWN) == True
    assert b.at(3, 0) == []
    assert b.at(3,1) == [p]
    assert p.move(LEFT) == True
    assert b.at(3, 1) == []
    assert b.at(2, 1) == [p]


def test_player_move2() -> None:
    """Test Player.move for making sure the player doesn't move when
    coming in contact with items like raccoons, locked garbage bins, and bins
    with raccoons in them."""
    b = GameBoard(4,3)
    p = Player(b, 1, 1)
    s = SmartRaccoon(b, 1, 0)
    r1 = Raccoon(b, 0, 1)
    g1 = GarbageCan(b, 2, 1, True)
    g2 = GarbageCan(b, 1, 2, False)
    r2 = Raccoon(b, 1, 2)

    assert b.to_grid() == [['-', 'S', '-', '-'], ['R', 'P', 'C', '-'],
                           ['-', '@', '-', '-']]
    assert p.move(UP) == False
    assert p.move(LEFT) == False
    assert p.move(DOWN) == False
    assert p.move(RIGHT) == False


def test_player_move3() -> None:
    b = GameBoard(5,3)
    p = Player(b, 1, 1)
    o = GarbageCan(b, 0, 1, False)
    rb1 = RecyclingBin(b, 1, 0)
    rb2 = RecyclingBin(b, 2, 1)
    rb3 = RecyclingBin(b, 3, 1)

    assert p.move(LEFT) == True
    assert b.at(0, 1) == [o]
    assert b.at(0, 1)[0].locked == True
    assert b.at(1, 1) == [p]

    assert p.move(UP) == False
    assert b.at(1, 0) == [rb1]
    assert b.at(1, 1) == [p]

    assert p.move(RIGHT) == True
    assert b.at(1, 1) == []
    assert b.at(2, 1) == [p]
    assert b.at(3, 1) == [rb2]
    assert b.at(4, 1) == [rb3]


def test_is_valid_path1() -> None:
    b = GameBoard(4, 7)
    r = SmartRaccoon(b, 0, 1)
    gb1 = GarbageCan(b, 3, 1, True)
    gb2 = GarbageCan(b, 0, 6, False)
    p = Player(b, 0, 3)
    assert r._is_valid_path(RIGHT) == (True, 3)
    assert r._is_valid_path(DOWN) == (True, 5)
    assert r._is_valid_path(LEFT) == (False, 0)
    assert r._is_valid_path(UP) == (False, 0)


def test_is_valid_path2() -> None:
    b = GameBoard(8, 7)
    c1 = GarbageCan(b, 3, 0, True)
    s1 = SmartRaccoon(b, 3, 1)
    c2 = GarbageCan(b, 0, 3, True)
    r = Raccoon(b, 1, 3)
    s2 = SmartRaccoon(b, 3, 3)
    c3 = GarbageCan(b, 5, 3, True)
    o1 = GarbageCan(b, 7, 3, False)
    _ = GarbageCan(b, 3, 5, False)
    _ = Raccoon(b, 3, 5)
    o2 = GarbageCan(b, 3, 6, False)
    assert s2._is_valid_path(UP) == (False, 0)
    assert s2._is_valid_path(LEFT) == (False, 0)
    assert s2._is_valid_path(RIGHT) == (True, 2)
    assert s2._is_valid_path(DOWN) == (False, 0)

def test_find_closest_path1() -> None:
    b = GameBoard(4, 7)
    r = SmartRaccoon(b, 0, 1)
    gb1 = GarbageCan(b, 3, 1, True)
    gb2 = GarbageCan(b, 0, 6, False)
    p = Player(b, 0, 3)
    assert r._find_closest_path() == RIGHT


def test_find_closest_path2() -> None:
    b = GameBoard(8, 7)
    c1 = GarbageCan(b, 3, 0, True)
    s1 = SmartRaccoon(b, 3, 1)
    c2 = GarbageCan(b, 0, 3, True)
    r = Raccoon(b, 1, 3)
    s2 = SmartRaccoon(b, 3, 3)
    c3 = GarbageCan(b, 5, 3, True)
    o1 = GarbageCan(b, 7, 3, False)
    _ = GarbageCan(b, 3, 5, False)
    _ = Raccoon(b, 3, 5)
    o2 = GarbageCan(b, 3, 6, False)
    assert s2._find_closest_path() == RIGHT


def test_find_closest_path3() -> None:
    b = GameBoard(8, 7)
    c1 = GarbageCan(b, 3, 0, True)
    s = SmartRaccoon(b, 3, 3)
    c2 = GarbageCan(b, 7, 3, True)
    o2 = GarbageCan(b, 3, 6, False)
    assert s._find_closest_path() == UP
    o1 = GarbageCan(b, 0, 3, False)
    assert s._find_closest_path() == LEFT


if __name__ == '__main__':
    import pytest

    pytest.main(['a1_my_own_tests.py'])
