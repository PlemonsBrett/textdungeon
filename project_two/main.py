import json
from os import system, name
import pprint

pp = pprint.PrettyPrinter(indent=4)

try:
    from simple_chalk import chalk

    success = chalk.green.bold
    failed = chalk.red.bold
    standard = chalk.black.bgWhite
except ImportError as e:
    success = lambda x: x
    failed = lambda x: x
    standard = lambda x: x


def setup_map():
    """
    Takes the dungeon_map.json file in same directory, and converts it into a dictionary.
    :return: dictionary of the dungeon map
    """
    map_file = open("dungeon_map.json")

    data = json.load(map_file)

    map_file.close()
    return data


def clear_prompt():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def unavailable():
    print(failed('Sorry that is not an available move, try again'))


class Game:
    available_moves = ('go North', 'go South', 'go East', 'go West')
    available_rooms = (
        'Drawbridge', 'Gatehouse', 'Great Hall', 'Phylactery', 'Apothecary', 'Battlement', 'Donjon', 'Drum Tower')
    available_items = ('Atiesh', 'Frostmourne', 'Scepter of Sargeras', "Felo'malorn", "Thas'dorah", 'Umbral Crescent')
    current_state = 'continue'
    current_inventory = []

    def __init__(self):
        self.player_name = None
        self.current_room = None
        self.game_map = setup_map()
        self.reset()

    def print_greeting(self):
        """ Prints out the basic instructions"""
        print('Your movement commands are:', end=' ')
        print(*self.available_moves, sep=', ')
        print('You may leave at any time by typing: "exit"')
        # TODO: Add instructions for adding items to inventory
        # print('You may search a room with the command: "search"')
        # print('To add an item to your inventory: "get item name"')

    def get_description(self):
        room_description = self.game_map[self.current_room]['description']
        return room_description

    def add_item(self):
        self.current_inventory.append(self.game_map[self.current_room]['items'][0])

    def search(self):
        room_items = self.game_map[self.current_room]['items']
        if len(room_items) != 0:
            print(success(f'You found {room_items[0]}!'))
            print(success(f'Collect it by using move "get {room_items[0].split()[0]}'))
        else:
            print(standard("You didn't find anything of value... try looking elsewhere..."))

    def move(self, move):
        room = self.game_map[self.current_room]
        if move.lower() in [i.lower() for i in self.available_moves]:
            self.current_state = room['moves'][move][0]
            if room['moves'][move][1] in self.available_rooms:
                next_room = room['moves'][move][1]
                try:
                    print(success(room['moves'][move][2]))
                except IndexError:
                    print('We seem to have run into a problem... sorry about that, try again.')
                    return -1
                self.current_room = next_room
            elif room['moves'][move][0] == 'game over':
                print(failed(room['moves'][move][1]))
            else:
                print(failed(room['moves'][move][1]))
        else:
            print(f'That doesn\'t seem to be an available move, does this look right? {move}')
            print('Available moves are: ', end='')
            print(*self.available_moves, sep=', ')

    def play_again(self):
        clear_prompt()
        again = input(standard('Would you like to play again (y/n): '))
        if again == 'y':
            self.reset()
        else:
            exit(1)

    def reset(self):
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
        self.print_greeting()
        input('Press Enter to continue...')

    def get_move(self):
        system('cls')
        if len(self.current_inventory) == 6:
            print(success("You've won! You are a worth adversary!"))
            self.play_again()
        else:
            self.print_greeting()
            print(standard(f'{self.get_description()}\n'))
            # TODO: Show user their current inventory
            # print(standard(f'Current inventory: {game.current_inventory}'))
            print('-' * 25)
            move = input('Enter your move: ')
            if move is None or not move:
                unavailable()
                return -1
            match move.lower().split()[0]:
                case 'search':
                    self.search()
                case 'get':
                    self.add_item()
                case 'exit':
                    exit(1)
                case 'go':
                    self.move(move)
                case _:
                    unavailable()


def game_loop():
    game = Game()
    while game.current_state == 'continue':
        game.get_move()
        input('Press Enter to continue...')


if __name__ == '__main__':
    game_loop()
