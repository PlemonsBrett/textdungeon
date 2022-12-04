import json
from os import system, name

# The following try:except block will attempt to import simple_chalk
# this package is used to make the prompt a bit more interesting
# if the package isn't installed, then the created functions will simply return the input value.
try:
    from simple_chalk import chalk

    success = chalk.green.bold
    failed = chalk.red.bold
    standard = chalk.black.bgWhite
except ImportError as e:
    success = lambda x: x
    failed = lambda x: x
    standard = lambda x: x


def clear_prompt():
    """
    Checks the current OS and applies the appropriate command to clear the prompt
    """
    # the system() function from Pythons os standard library, pushes the passed in string to the current terminal
    # in windows, to clear the terminal we use `cls`
    # in *nix systems, we use `clear`
    # if current OS is Windows/DOSIX
    if name == 'nt':
        _ = system('cls')
    # if current OS is *nix-based (MacOS/Linux)
    else:
        _ = system('clear')


def setup_map():
    """
    Takes the dungeon_map.json file in same directory, and converts it into a dictionary.
    :return: dictionary of the dungeon map
    """
    # The dictionary that holds the game data is rather large, so a separate file was necessary
    map_file = open("dungeon_map.json")

    # Converts the json file into a dictionary collection
    data = json.load(map_file)

    # Closes the process that is accessing the file, to not cause corruption
    map_file.close()
    return data


def unavailable():
    """
    Prints a message when an entered move is not in the available_moves
    :return:
    """
    print(failed('Sorry that is not an available move, try again'))


class Game:
    """
    The Game Class is the scaffolding for the game state, and game information
    """
    available_moves = ('go North', 'go South', 'go East', 'go West')
    available_rooms = (
        'Drawbridge', 'Gatehouse', 'Great Hall', 'Phylactery', 'Apothecary', 'Battlement', 'Donjon', 'Drum Tower')
    available_items = ('Atiesh', 'Frostmourne', 'Scepter of Sargeras', "Felo'malorn", "Thas'dorah", 'Umbral Crescent')
    current_state = 'continue'
    current_inventory = []

    def __init__(self):
        """
        Initializes the game object with the default attribute values, and initializes the game_map
        """
        self.player_name = None
        self.current_room = None
        self.game_map = setup_map()
        self.reset()

    def print_instructions(self):
        """ Prints out the basic instructions"""
        print('Your movement commands are:', end=' ')
        # The '*' in front of self.available_moves is the 'spread' operator,
        # it is basically running a for-loop of the elements in the list object and printing them with 'sep' in between
        print(*self.available_moves, sep=', ')
        print('You may leave at any time by typing: "exit"')
        # TODO: Add instructions for adding items to inventory
        # print('You may search a room with the command: "search"')
        # print('To add an item to your inventory: "get item name"')

    def get_description(self):
        """
        Gets the description of the current_room from game_map
        :return: string; description of current_room
        """
        # Navigating the nested dictionary to get the necessary data
        room_description = self.game_map[self.current_room]['description']
        return room_description

    def add_item(self):
        """
        Adds the item from the current_room to the current_inventory
        :return: Updated inventory state
        """
        # Navigating the nested dictionary to get the necessary data
        self.current_inventory.append(self.game_map[self.current_room]['items'][0])

    def search(self):
        """
        Checks the game_map for the current_room to see if there are any available items.
        :return: Message to inform user if there are any items in the current room.
        """
        # Since the room_items value is used multiple times, it makes more sense to create a variable to hold that value
        room_items = self.game_map[self.current_room]['items']
        if len(room_items) != 0:
            print(success(f'You found {room_items[0]}!'))
            print(success(f'Collect it by using move "get {room_items[0].split()[0]}'))
        else:
            print(standard("You didn't find anything of value... try looking elsewhere..."))

    def move(self, move):
        """
        Takes a movement command, tests for validity, and then updates room state
        :param move: string; ("go North", "go South", "go East", "go West") - case doesn't matter
        :return: Updated room state, or a message
        """
        # Since the room value is used frequently here, it makes more sense to create a variable
        room = self.game_map[self.current_room]
        # While this nested if statement seems complex, we are actually only making two checks
        # is 'move' an available move?
        # if it is we should check the game_map and make any necessary updates to the game state
        # if not, we should let the user know.
        if move.lower() in [i.lower() for i in self.available_moves]:
            self.current_state = room['moves'][move][0]
            if room['moves'][move][1] in self.available_rooms:
                next_room = room['moves'][move][1]
                # Since not all move options in the game_map have 3 elements,
                # we want to make sure that we aren't accidentally trying to access an out of index element
                # if we are, we should re-prompt the user. (Handled in game_loop)
                try:
                    print(success(room['moves'][move][2]))
                except IndexError:
                    print('We seem to have run into a problem... sorry about that, try again.')
                    return -1
                self.current_room = next_room
            # This step is really only relevant when win conditions are implemented
            elif room['moves'][move][0] == 'game over':
                print(failed(room['moves'][move][1]))
            else:
                print(failed(room['moves'][move][1]))
        else:
            print(f'That doesn\'t seem to be an available move, does this look right? {move}')
            print('Available moves are: ', end='')
            print(*self.available_moves, sep=', ')

    def play_again(self):
        """
        Prompts the user to play the game again, and then either resets or exits
        """
        clear_prompt()
        again = input(standard('Would you like to play again (y/n): '))
        if again == 'y':
            self.reset()
        else:
            exit(1)

    def reset(self):
        """
        Sets the initial game state
        """
        clear_prompt()
        self.current_state = 'continue'
        self.current_inventory = []
        self.current_room = 'Drawbridge'
        self.player_name = input(standard('Please enter your name, adventurer: ')) or 'Adventurer'
        print(success(f'Welcome to TextDungeon, {self.player_name}'))
        print(standard(
            'The name and description of the room you are in will always be displayed at the top of the prompt!'))
        # TODO: Print win conditions to user
        # print(standard('In order to successfully conquer this dungeon, you must collect 6 rare artifacts, or be killed by an Enemy!'))
        self.print_instructions()
        # Since this is not actually part of the game loop, we need to ensure that we give the user ample time to read
        # any messages before returning to the loop
        input('Press Enter to continue...')

    def get_move(self):
        """
        Checks if the user has won the game, if not
        collects the users move and updates the game state
        """
        # Clear the prompt
        system('cls')
        # Check win condition, not currently implemented
        if len(self.current_inventory) == 6:
            print(success("You've won! You are a worth adversary!"))
            self.play_again()
        # if the user hasn't yet won
        else:
            self.print_instructions()
            print(standard(f'{self.get_description()}\n'))
            # TODO: Show user their current inventory
            # print(standard(f'Current inventory: {game.current_inventory}'))
            print('-' * 25)
            move = input('Enter your move: ')
            # Check if the user entered an invalid input, or no input
            if move is None or not move:
                unavailable()
                return -1
            # New in Python 3.10, similar to a 'switch' statement in other languages
            # Helps to reduce code, and improve readability by removing the need for lots of if/elif/else statements
            match move.lower().split()[0]:
                case 'search':
                    self.search()
                case 'get':
                    self.add_item()
                case 'exit':
                    # A Python built-in function, that stops the current execution of the program, gracefully.
                    exit(1)
                # Cases have to be simple, and since we want to allow the user to enter a value that isn't
                # case-sensitive, we just check that they at least provided 'go' and then do additional checks in
                # the move method
                case 'go':
                    self.move(move)
                case _:
                    unavailable()


def game_loop():
    """
    The main game loop
    """
    # This is the main entry point for this application, as such, we need to make sure to initialize a Game object
    # to set the initial state before we start the game loop.
    game = Game()
    # A loop is the main component of a game, in games, we are constantly checking for the status of a game
    # More complex games might have multiple game loops for different functionalities in a game, like HP or Ammo
    # Here we only have two states;
    # `continue`: the game is in a good state and will continue
    # `game over`: the player has died, and the game will end.
    while game.current_state == 'continue':
        # Prompt the user for the current move
        game.get_move()
        # We use an input() as a way to stop the prompt from continuing or resetting
        # since we use a loop to maintain the games state, we don't want it to continue going
        # or we could run into an infinite loop.
        input('Press Enter to continue...')


if __name__ == '__main__':
    game_loop()
