from os import system

from project_two import __version__
from project_two.main import Game


# A sanity test to ensure poetry builder is working
def test_version():
    assert __version__ == "0.1.0"


def test_game_class():
    game = Game()
    assert isinstance(game, Game)
