from __future__ import annotations
from typing import Optional
from a2_support import UserInterface, TextInterface
from constants import *



# Replace these <strings> with your name, student number and email address.
__author__ = "William Eason, 46425692"
__email__ = "w.eason@uqconnect.edu.au"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackboard changelog. 
__version__ = 1.0

# Uncomment this function when you have completed the Level class and are ready
# to attempt the Model class.

# def load_game(filename: str) -> list['Level']:
#     """ Reads a game file and creates a list of all the levels in order.
    
#     Parameters:
#         filename: The path to the game file
    
#     Returns:
#         A list of all Level instances to play in the game
#     """
#     levels = []
#     with open(filename, 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line.startswith('Maze'):
#                 _, _, dimensions = line[5:].partition(' - ')
#                 dimensions = [int(item) for item in dimensions.split()]
#                 levels.append(Level(dimensions))
#             elif len(line) > 0 and len(levels) > 0:
#                 levels[-1].add_row(line)
#     return levels


# Write your classes here
class Tile():
    block = False
    tile_damage = 0
    id = ABSTRACT_TILE

    def is_blocking(self) -> bool:
        return bool(self.block)
    
    def damage(self) -> int:
        return int(self.tile_damage)
    
    def get_id(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return str(self.get_id())

    def __repr__(self) -> str:
        return f"{type(self).__name__ }()"
        
class Wall(Tile):
    block = True
    id = WALL

class Empty(Tile):
    block = False
    id = EMPTY

class Lava(Tile):
    block = False
    id = LAVA
    tile_damage = LAVA_DAMAGE

class Door(Tile):
    block = True
    id = DOOR

    def unlock(self) -> None:
        self.block = False
        self.id = EMPTY

class Entity():
    id = "E"
    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position
    
    def get_position(self) -> tuple[int, int]:
        return self.position
    
    def get_name(self) -> str:
        return type(self).__name__
    
    def get_id(self) -> str:
        return str(self.id)
    
    def __str__(self) -> str:
        return str(self.get_id())
    
    def __repr__(self) -> str:
        return '{0}({1})'.format(self.get_name(), self.get_position())

class DynamicEntity(Entity):
    id = DYNAMIC_ENTITY

    def set_position(self, new_position: tuple[int, int]) -> None:
        self.position = new_position

class Inventory():

    def __init__(self, initial_items: Optional[list[Item,...]] = None) -> None:
        self._inventory = {}

        if initial_items is None:
            pass
        else:
            for items in initial_items:
                if items.get_name() not in self._inventory:
                    self._inventory[items.get_name()] = [items]
                else:
                    self._inventory[items.get_name()].append(items)

    def add_item(self, item: Item) -> None:
        if item.get_name() not in self._inventory:
            self._inventory[item.get_name()] = []
        self._inventory[item.get_name()].append(item)

    def get_items(self) -> dict[str, list[Item,...]]:
        return self._inventory

    def remove_item(self, item_name: str) -> Optional[Item]:
        if item_name not in self._inventory:
            return None
        removed_item = self._inventory[item_name].pop(0)
        if self._inventory[item_name] == []:
            del self._inventory[item_name]
        return removed_item

    def __str__(self) -> str:
        text = ""
        for item in self._inventory:
            item_counter = str(len(self._inventory[item]))
            text += item + ": " + item_counter + "\n"
        return text[0:-1]

    def __repr__(self) -> str:
        values = self._inventory.values()
        values_list = list(values)
        return '{0}({1}{2})'.format(type(self).__name__,"initial_items=", values_list)


class Player(DynamicEntity):
    hunger = 0
    thirst = 0
    health = 100

    def __init__(self, position):
        self.position = position
        self._inventory = Inventory()

    def get_hunger(self) -> int:
        return self.hunger

    def get_thirst(self) -> int:
        return self.thirst
    
    def get_health(self) -> int:
        return self.health

    # The change defs need to be capped
    def change_hunger(self, amount: int) -> None:
        new_hunger = self.hunger + amount
        self.hunger = max(min(new_hunger, MAX_HUNGER), 0)
    
    def change_thirst(self, amount: int) -> None:
        new_thirst = self.thirst + amount
        self.thirst = max(min(new_thirst, MAX_THIRST), 0)
    
    def change_health(self, amount: int) -> None:
        new_health = self.health + amount
        self.health = max(min(new_health, MAX_HEALTH), 0)
    
    def get_inventory(self):
        return self._inventory

    #add Item back to def -> item: Item
    def add_item(self, item: Item) -> None:
        return self._inventory.add_item(item)

# Add a __repr__ function for player (see assignment sheet)

class Item(Entity):
    id = ITEM
    def apply(self, player: Player) -> None:
        raise NotImplementedError

class Potion(Item):
    id = POTION
    def apply(self, player: Player) -> None:
        player.change_health(POTION_AMOUNT)

class Coin(Item):
    id = COIN
    def apply(self, player: Player) -> None:
        player.change_hunger(0)
        player.change_health(0)
        player.change_thirst(0)

class Water(Item):
    id = WATER
    def apply(self, player: Player) -> None:
        player.change_thirst(WATER_AMOUNT)

# change 0 to am
class Food(Item):
    id = FOOD
    def apply(self, player: Player) -> None:
        player.change_hunger(0)

class Apple(Food):
    id = APPLE

    def apply(self, player: Player) -> None:
        player.change_hunger(APPLE_AMOUNT)

class Honey(Food):
    id = HONEY
    def apply(self, player: Player) -> None:
        player.change_hunger(HONEY_AMOUNT)

class Maze():
    maze_rows = []
    tiles = {' ': Empty(),
             '#': Wall(),
             'L': Lava(),
             'D': Door()}
    id_list = []
    def __init__(self, dimensions: tuple[int, int]) -> None:
        self._dimensions = dimensions

    def get_dimensions(self) -> tuple[int, int]:
        return self._dimensions

    def add_row(self, row: str) -> None:
        row_list = []
        self.id_list.append(row)
        for tile in row:
            row_list.append(self.tiles.get(tile, Empty()))
        self.maze_rows.append(row_list)

    def get_tiles(self) -> list[list[Tile]]:
        return self.maze_rows

    def unlock_door(self) -> None:
        for row in self.maze_rows:
            for tile in range(len(row)):
                if row[tile] == 'D':
                    row[tile] = ' '

    def get_tile(self, position: tuple[int, int]) -> Tile:
        row_num = position[0]
        col_num = position[1]
        return self.maze_rows[row_num][col_num]

    def __str__(self) -> str:
        exp_output = []
        for row in self.id_list:
            new_row = ""
            for i in range(len(row)):
                new_row += row[i] if row[i] in self.tiles.keys() \
                    else EMPTY
            exp_output.append(new_row)
        return '\n'.join(exp_output)

    def __repr__(self) -> str:
        return '{0}({1})'.format(type(self).__name__, self.get_dimensions())

class Level():
    def __init__(self, dimensions: tuple[int, int]) -> None:
        self._dimensions = dimensions

    def get_maze(self) -> Maze:
        return '{0}({1})'.format('Maze', self.get_dimensions())

    def attempt_unlock_door(self) -> None:
        pass

    def add_row(self, row: str) -> None:
        pass

    def add_entity(self, position: tuple[int, int], entity_id: str) -> None:
        pass

    def get_dimensions(self) -> tuple[int, int]:
        return self._dimensions

    def get_items(self) -> dict[tuple[int, int], Item]:
        pass

    def remove_item(self, position: tuple[int, int]) -> None:
        pass

    def add_player_start(self, position: tuple[int, int]) -> None:
        pass

    def get_player_start(self) -> Optional[tuple[int, int]]:
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

class Model():
    def __init__(self, game_file: str) -> None:
        pass

    def has_won(self) -> bool:
        pass

    def has_lost(self) -> bool:
        pass

    def get_level(self) -> Level:
        pass

    def level_up(self) -> None:
        pass

    def did_level_up(self) -> bool:
        pass

    def move_player(self, delta: tuple[int, int]) -> None:
        pass

    def attempt_collect_item(self, position: tuple[int, int]) -> None:
        pass

    def get_player(self) -> Player:
        pass

    def get_player_stats(self) -> tuple[int, int, int]:
        pass

    def get_player_inventory(self) -> Inventory:
        pass

    def get_current_maze(self) -> Maze:
        pass

    def get_current_items(self) -> dict[tuple[int, int], Item]:
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

class MazeRunner():
    def __init__(self, game_file: str, view: UserInterface) -> None:
        pass

    def play(self) -> None:
        pass

def main():
    # Write your code here
    pass

if __name__ == '__main__':
    main()

