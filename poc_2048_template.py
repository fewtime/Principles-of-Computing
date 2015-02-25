"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    
    if len(line) < 2:
        return line
    
    result_line = [0] * len(line)
    last_merge = False
    
    for origin_line_index in range(0, len(line)):
        if line[origin_line_index] != 0:
            
            for new_line_index in range(0, len(result_line)):
                if result_line[new_line_index] == 0:
                    result_line[new_line_index] = line[origin_line_index]
                    last_merge = False
                    break
                elif result_line[new_line_index+1] == 0:
                    if result_line[new_line_index] == line[origin_line_index] and last_merge == False:
                        result_line[new_line_index] += line[origin_line_index]
                        last_merge = True
                        break
                        
    return result_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
        
        self._up_list = [(0, col) for col in range(self._width)]
        self._down_list = [(self._height-1, col) for col in range(self._width)]
        self._left_list = [(row, 0) for row in range(self._height)]
        self._right_list = [(row, self._width-1) for row in range(self._height)]
        self._move_dict = {UP:self._up_list, DOWN:self._down_list, LEFT:self._left_list, RIGHT:self._right_list}
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [ [0 for dummy_col in range(self._width)] for dummy_row in range(self._height) ]
        self.new_tile()
        self.new_tile()
        
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grids_format = ''
        for dummy_row in range(self._height):
            grids_format += '\n' + str(self._grid[dummy_row])
        print grids_format
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        direction_tiles = self._move_dict[direction]
        offset = OFFSETS[direction]
        
        if direction == UP or direction == DOWN:
            times = self._height
        else:
            times = self._width
            
        for current_tile in direction_tiles:
            tile = list(current_tile)
            temp_list = []
            
            for current_time in range(times):
                temp_list.append(self.get_tile(tile[0], tile[1]))
                tile[0] += offset[0]
                tile[1] += offset[1]
                
            result = merge(temp_list)
            tile = list(current_tile)
            
            for current_time in range(times):
                self.set_tile(tile[0], tile[1], result[current_time])
                tile[0] += offset[0]
                tile[1] += offset[1]
        
        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        selected = False
        count = self._width * self._height
        
        while selected != True and count != 0:
            row = random.randint(0, self._height-1)
            col = random.randint(0, self._width-1)
            
            if self._grid[row][col] == 0:
                probability_list = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
                self.set_tile(row, col, random.choice(probability_list))
                selected = True
                
            count -= 1

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
