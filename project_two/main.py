"""
A simple text-based RPG
:author: Brett Plemons, <Brett.Plemons@snhu.edu>
"""
import json
import sys
from os import name, system

try:
    from simple_chalk import chalk

    success = chalk.green.bold
    failed = chalk.red.bold
    standard = chalk.black.bgWhite
except ImportError as e:

    def success(input_string) -> str:
        """
        Simple replacement function if simple_chalk isn't installed
        :param input_string: str; string to be printed
        :return: str; the input string
        """
        return input_string

    def failed(input_string) -> str:
        """
        Simple replacement function if simple_chalk isn't installed
        :param input_string: str; string to be printed
        :return: str; the input string
        """
        return input_string

    def standard(input_string) -> str:
        """
        Simple replacement function if simple_chalk isn't installed
        :param input_string: str; string to be printed
        :return: str; the input string
        """
        return input_string


def clear_prompt():
    """
    Checks the current OS and applies the appropriate command to clear the prompt
    """
    if name == "nt":
        system("cls")
    else:
        system("clear")


def unavailable():
    """
    Prints a message when an entered move is not in the available_moves
    :return:
    """
    print(failed("Sorry that is not an available move, try again"))


class Game:
    """
    The Game Class is the scaffolding for the game state, and game information
    """

    available_moves = ("go North", "go South", "go East", "go West")
    available_rooms = (
        "Drawbridge",
        "Gatehouse",
        "Great Hall",
        "Phylactery",
        "Apothecary",
        "Battlement",
        "Donjon",
        "Drum Tower",
    )
    current_state = "continue"
    current_inventory = []

    def __init__(self):
        """
        Initializes the game object with the default attribute values,
        and initializes the game_map
        """
        self.game_map = None
        self.player_name = None
        self.current_room = None
        self.setup_map()
        self.reset()

    def setup_map(self):
        """
        Takes the dungeon_map.json file in same directory,
        and converts it into a dictionary.
        :return: dictionary of the dungeon map
        """
        with open("dungeon_map.json", encoding="utf-8") as map_file:
            self.game_map = json.load(map_file)

            map_file.close()

    def print_instructions(self):
        """Prints out the basic instructions"""
        print("Your movement commands are:", end=" ")
        print(*self.available_moves, sep=", ")
        print('You may leave at any time by typing: "exit"')
        print('You may search a room with the command: "search"')
        print('To add an item to your inventory: "get item name"')

    def get_description(self):
        """
        Gets the description of the current_room from game_map
        :return: string; description of current_room
        """
        room_description = self.game_map[self.current_room]["description"]
        return room_description

    def add_item(self):
        """
        Adds the item from the current_room to the current_inventory
        :return: Updated inventory state
        """
        print(
            success(
                f'You pick up {self.game_map[self.current_room]["items"][0]}'
                f"and gently shove it into your pack."
            )
        )
        self.current_inventory.append(self.game_map[self.current_room]["items"][0])

    def search(self):
        """
        Checks the game_map for the current_room to
        see if there are any available items.
        :return: Message to inform user if there are any items in the current room.
        """
        room_items = self.game_map[self.current_room]["items"]
        if len(room_items) != 0:
            print(success(f"You found {room_items[0]}!"))
            print(success(f'Collect it by using move "get {room_items[0]}"'))
        else:
            print(
                standard(
                    "You didn't find anything of value... try looking elsewhere..."
                )
            )

    def move(self, move):
        """
        Takes a movement command, tests for validity, and then updates room state
        :param move: ("go North", "go South", "go East", "go West")
        :return: Updated room state, or a message
        """
        room = self.game_map[self.current_room]
        if move.lower() in [
            move_element.lower() for move_element in self.available_moves
        ]:
            self.current_state = room["moves"][move][0]
            if room["moves"][move][1] in self.available_rooms:
                next_room = room["moves"][move][1]
                try:
                    print(success(room["moves"][move][2]))
                except IndexError:
                    print(
                        "We seem to have run into a problem... "
                        "sorry about that, try again."
                    )
                    return -1
                self.current_room = next_room
            # This step is really only relevant when win conditions are implemented
            elif room["moves"][move][0] == "game over":
                print(failed(room["moves"][move][1]))
            else:
                print(failed(room["moves"][move][1]))
        else:
            print(
                f"That doesn't seem to be an available move,"
                f" does this look right? {move}"
            )
            print("Available moves are: ", end="")
            print(*self.available_moves, sep=", ")
        return -1

    def play_again(self):
        """
        Prompts the user to play the game again, and then either resets or exits
        """
        clear_prompt()
        again = input(standard("Would you like to play again (y/n): "))
        if again == "y":
            self.reset()
        else:
            sys.exit()

    def reset(self):
        """
        Sets the initial game state
        """
        clear_prompt()
        self.current_state = "continue"
        self.current_inventory = []
        self.current_room = "Drawbridge"
        self.player_name = (
            input(standard("Please enter your name, adventurer: ")) or "Adventurer"
        )
        print(success(f"Welcome to TextDungeon, {self.player_name}"))
        print(
            standard(
                "The name and description of the room you are in "
                "will always be displayed at the top of the prompt!"
            )
        )
        # TODO: Print win conditions to user
        print(
            standard(
                "In order to successfully conquer this dungeon, "
                "you must collect 6 rare artifacts, or be killed by an Enemy!"
            )
        )
        self.print_instructions()
        input("Press Enter to continue...")

    def get_move(self):
        """
        Checks if the user has won the game, if not
        collects the users move and updates the game state
        """
        clear_prompt()
        if len(self.current_inventory) == 6:
            print(success("You've won! You are a worth adversary!"))
            self.play_again()
        else:
            self.print_instructions()
            print(standard(f"{self.get_description()}\n"))
            print(standard(f"Current inventory: {self.current_inventory}"))
            print("-" * 25)
            move = input("Enter your move: ")
            # Check if the user entered an invalid input, or no input
            if move is None or not move:
                unavailable()
                return -1
            # New in Python 3.10, similar to a 'switch' statement in other languages
            # Helps to reduce code, and improve readability by
            # removing the need for lots of if/elif/else statements
            match move.lower().split()[0]:
                case "search":
                    self.search()
                case "get":
                    self.add_item()
                case "exit":
                    sys.exit()
                case "go":
                    self.move(move)
                case _:
                    unavailable()
        return -1


def game_loop():
    """
    The main game loop
    """
    game = Game()
    # Here we only have two states;
    # `continue`: the game is in a good state and will continue
    # `game over`: the player has died, and the game will end.
    while game.current_state == "continue":
        game.get_move()
        input("Press Enter to continue...")


if __name__ == "__main__":
    game_loop()
