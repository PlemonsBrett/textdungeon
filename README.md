# Welcome to TextDungeon

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