# Welcome to TextDungeon

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

To run this game, you need to have the following:
- Python >3.6, <=3.10
- Poetry (optional for coloured output)

## Install Poetry
### Windows
```commandline
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### *nix based systems
```commandline
    curl -sSL https://install.python-poetry.org | python3 -
```

## Build game
```
    cd textdungeon
    poetry install && poetry lock
```

Then run the game with `poetry run start`

If you don't have poetry installed, or don't want to have poetry installed:
```commandline
    cp dungeon_map.json ./project_two
    cd project_two
    python main.py
```

If you want to have colors enabled for prompt, without poetry:
```commandline
    pip install simple_chalk
    cp dungeon_map.json ./project_two
    python main.py
```
