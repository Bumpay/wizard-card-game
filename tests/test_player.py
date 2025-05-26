from core.player import rotate_players, WizardBasePlayer


class DummyPlayer(WizardBasePlayer):
    def __repr__(self):
        return f'DummyPlayer({self.name})'


def test_rotate_players_basic():
    a, b, c, d = DummyPlayer('A'), DummyPlayer('B'), DummyPlayer('C'), DummyPlayer('D')
    players = [a, b, c, d]

    rotated = rotate_players(players, c)

    assert rotated == [c, d, a, b]
    assert players == [a, b, c, d]

def test_rotate_players_start_is_first():
    a, b, c = DummyPlayer('A'), DummyPlayer('B'), DummyPlayer('C')
    players = [a, b, c]

    rotated = rotate_players(players, a)

    assert rotated == [a, b, c]

def test_rotate_players_single():
    a = DummyPlayer('Solo')
    players = [a]

    rotated = rotate_players(players, a)

    assert rotated == [a]

def test_rotate_players_invalid_start():
    a, b = DummyPlayer('A'), DummyPlayer('B')
    players = [a]

    try:
        rotate_players(players, b)
    except ValueError:
        assert True
    else:
        assert False