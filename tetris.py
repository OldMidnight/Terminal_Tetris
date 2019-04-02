#!/usr/bin/env python
'''
CA278 Project: DOTris: Modified Tetris
Maintainers:
Fareed Idris
Kevin Doyle
Moses Opebi
Tevin Thomas
'''

import random
import os
import time
from select import select
import sys


# Global Variables
running = True

def get_term_column_length():
  try:
    cols = os.environ['COLUMNS']
  except KeyError:
    cols = 25
  return cols

colors_dict = {
  'RED': '\033[31m',
  'GREEN': '\033[32;1m',
  'BLUE': '\033[34;1m',
  'YELLOW': '\033[33;1m',
  'PURPLE': '\033[35;1m',
  'NONE': '\033[0m'
}

colors_list = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'PURPLE']

class GridClass():
  '''
  Describes a Grid Object
  Properties include:
  grid: The initial empty list for the grid
  size: Defines the width of the grid
  level: Defines the current level of the grid instance

  Attributes include:
  level_dict: A dictionary containing a key-value relationship between a level and an object containing the properties of that level
  by a '/' to make splitting the shape when we choose it into a list much easier.

  next_shape: A Variable used during the shape_movement method. It lets the method know that the current shape has
  reached the bottom ans that a new shape should be spawned.

  incoming_shape: A variable used to store the shape that will be spawning next.

  row_sorted: A variable used to let the grid instance know that the row that is full of dots has been sorted and removed and to continue with the regular game processing.
  '''
  
  level_dict = {
    1: {
      'shape': [".", "./.", "././."],
      'speed': 0.75
    },
    2: {
      'shape': ["././.", "./././.", "././././."],
      'speed': 0.5
    },
    3: {
      'shape': ["././././.", "./././././.", "././././././."],
      'speed': 0.25
    },
    4: {
      'shape': ["././././././.", "./././././././."],
      'speed': 0.01
    },
  }
  next_shape = False
  points = 0
  incoming_shape = ''
  row_sorted = False
  def __init__(self, grid=[], size=15, level=1):
    '''
    The initial constructor for an instance of a GridClass object.
    Formal parameters inc]]reate Grid

    self: a pointer to the instantialized GridClass object
    grid: The initial empty list for the grid. This will be populated during initialization. default value = []
    size: This parameter defines the width of the grid. This can be changed based on settings chosen by the player. default value = 15
    level: This parameter indicates the initial level of the grid instance. This can be changed based on setting chosen by the player. default value = 1
    '''
    self.grid = grid
    self.size = size
    self.level = self.level_dict[level]
    self.grid.append("_" * self.size)
    i = 1
    while i < 21:
      self.grid.append([])
      self.grid[i].append("|")
      j = 0
      while j < self.size:
        self.grid[i].append(' ')
        j = j + 1
      self.grid[i].append("|")
      i = i + 1
    self.grid.append(("-" * self.size))
    #self.level_dict = GridClass.level_dict
    #self.next_shape = GridClass.next_shape
    #self.points = GridClass.points
    #self.incoming_shape = GridClass.incoming_shape
    #self.row_sorted = GridClass.row_sorted

  def draw(self):
    '''
    The draw function of the grid. Anytime this function is called, the screen will be cleared and an updated grid will be redrawn.
    '''
    os.system('clear')
    print colors_dict['GREEN'] + str('S C O R E: ' + str(self.points)).center(int(get_term_column_length()))
    for row in self.grid:
      print "".join(row).center(int(get_term_column_length()))
    print colors_dict['BLUE'] + str('I N C O M I N G   S H A P E: ' + "".join(self.incoming_shape)).center(int(get_term_column_length()))

  def spawn_shape(self):
    '''
    This function is called whenever a shape is needed to be spawned, either at the start of a new game or when a shape lands on a surface.
    A random number between 0 and the length of the shape dictionary (shape_dict) defined above is chosen. The current level is used to know from
    what list will a random shape be chosen.
    The shape is then split by the '/' that separates the dots and returned as a list.
    The midpoint of the top row of the grid is then calculated. This point is where the first dot of the shape will appear
    The positions from the midpoint of the top row to the length pf the shape is made equal to the shape.
    Below is what that operation would result in:

    top_row                          shape
      0    1    2    3    4    5 
    [' ', ' ', ' ', ' ', ' ', ' ']   ['.', '.', '.']

    midpoint = 2
    len(shape) - 1 = 2
    top_row[midpoint:midpoint + len(shape) - 1] = shape

    top_row = [' ', ' ', '.', '.', '.', ' ']
    '''
    self.next_shape = False

    color = colors_list[random.randint(0, 3)]
    current_color = colors_dict[color]

    if self.incoming_shape == '':
      current_shape_num = random.randint(0, len(self.level['shape']) - 1)
      shape = (current_color + self.level['shape'][current_shape_num] + colors_dict['NONE']).split('/')
    else:
      shape = self.incoming_shape
    next_shape_num = random.randint(0, len(self.level['shape']) - 1)
    color = colors_list[random.randint(0, 3)]
    next_color = colors_dict[color]
    self.incoming_shape = (next_color + self.level['shape'][next_shape_num] + colors_dict['NONE']).split('/')
    middle_of_row = len(self.grid[1]) / 2
    temp_row = self.grid[1]
    for a in range(middle_of_row, middle_of_row + len(shape)):
      temp_row[a] = '.'
      #self.grid[2][a] = ' '
    self.grid[1] = temp_row
    # self.grid[1][middle_of_row:middle_of_row + len(shape)] = shape
    
    self.draw()
    return self.shape_movement(1, middle_of_row, middle_of_row + len(shape), current_color)
      
  def shape_movement(self, current_row, shape_start_index, shape_end_index, color):
    next_row = current_row + 1
    if next_row == len(self.grid) - 1:
      self.next_shape = True

    if self.next_shape == False:
      for a in range(shape_start_index, shape_end_index):
        if self.grid[next_row][a] != ' ':
          self.next_shape = True

    if self.next_shape == False:
      for a in range(shape_start_index, shape_end_index):
        self.grid[next_row][a] = '.'
      for a in range(shape_start_index - 1, shape_end_index + 1):
        if self.grid[current_row][a] != '|':
          self.grid[current_row][a] = ' '
      # temp_row = self.grid[next_row]
      # self.grid[next_row] = self.grid[current_row]
      # self.grid[current_row] = temp_row
      # time.sleep(self.level['speed'])
      self.draw()

      move, o, e = select([sys.stdin], [], [], self.level['speed'])

      if (move):
        direction = sys.stdin.readline().strip()
        if direction == 'd':
          if self.grid[next_row][shape_end_index] == ' ':
            shape_end_index = shape_end_index + 1
            shape_start_index = shape_start_index + 1
        elif direction == 'a':
          if self.grid[next_row][shape_start_index - 1] == ' ':
            shape_end_index = shape_end_index - 1
            shape_start_index = shape_start_index - 1

    if self.next_shape:
      return True
    else:
      self.shape_movement(next_row, shape_start_index, shape_end_index, color)

  def remove_point_row(self, row_to_sort):
    if row_to_sort == 1:
      for a in range(1, len(self.grid[1]) - 1):
        self.grid[row_to_sort][a] = ' '
      self.row_sorted = True
    else:
      temp_row = []
      for i in self.grid[row_to_sort - 1]:
        temp_row.append(i)
      self.grid[row_to_sort] = temp_row
    if self.row_sorted:
      return True
    else:
      return self.remove_point_row(row_to_sort - 1)

  def check_status(self):
    if '.' in self.grid[1]:
      return [1]
    else:
        i = 1
        while i < len(self.grid) - 1:
            if ' ' not in self.grid[i]:
                return [2, i]
            i += 1
        return [0]
  
  def gameover(self):
    name = raw_input('Please enter name:\n')
    with open ('highscore', 'a') as f:
      f.write(name, self.points)

def select_level():
  selected_level = 0
  print colors_dict['BLUE'] + 'S E L E C T   A   D I F F I C U L T Y :'.center(int(get_term_column_length())) + colors_dict['NONE']
  print ''.center(int(get_term_column_length()))
  print colors_dict['GREEN'] +  '    [1]        E A S Y                    '.center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['YELLOW'] + '    [2]        M E D I U M                '.center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['RED'] +    '    [3]        H A R D                    '.center(int(get_term_column_length()))
  print colors_dict['PURPLE'] + '    [4]        Y O U   W O N T   W I N    '.center(int(get_term_column_length())) + colors_dict['NONE']
  print ''.center(int(get_term_column_length()))
  while selected_level == 0:
    level = raw_input('[ENTER]: ')
    if level == '1':
      print colors_dict['GREEN'] + 'Taking it easy huh?'.center(int(get_term_column_length())) + colors_dict['NONE']
      time.sleep(2)
      selected_level = 1
    elif level == '2':
      print colors_dict['YELLOW'] + 'Not much of a challenge really.'.center(int(get_term_column_length())) + colors_dict['NONE']
      time.sleep(2)
      selected_level = 2
    elif level == '3':
      print colors_dict['RED'] + "That's More like it!".center(int(get_term_column_length())) + colors_dict['NONE']
      time.sleep(2)
      selected_level = 3
    elif level == '4':
      print colors_dict['PURPLE'] + 'Abandon hope all ye who have chosen this option...'.center(int(get_term_column_length())) + colors_dict['NONE']
      time.sleep(2)
      selected_level = 4
    else:
      print colors_dict['RED'] + '[!] Unrecognized Input!' + colors_dict['NONE']
      print colors_dict['RED'] + '[!] Try Again.' + colors_dict['NONE']
  return selected_level
    

def print_menu():
    os.system('clear')
    print colors_dict['GREEN'] + "       ______    ________    ________________     ___ _______    ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['GREEN'] + "      /      \  /        \  /         /  __  \   /  //  ____/    ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['GREEN'] + "     /  ____  \/   _____  \/___   ___/  / /  /  /  / \  \__      ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['GREEN'] + "    /  /   /  /\  /    /  /  /   /  /  _    /  /  /   \    \     ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['GREEN'] + "   /         /  \        /  /   /  /  / \  \  /  / ___/    /     ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['GREEN'] + "  /_________/    \______/  /___/  /__/   \__\/__/ /_______/      ".center(int(get_term_column_length())) + colors_dict['NONE']
    print ''.center(int(get_term_column_length()))
    print colors_dict['GREEN'] + 'C A 2 7 8   P R O J E C T'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['YELLOW'] + '_______________________________________________________________'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['BLUE'] + 'M A D E   B Y :'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['BLUE'] + 'F A R E E D   I D R I S'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['BLUE'] + 'M O S E S   O P E B I'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['BLUE'] + 'K E V I N   D O Y L E'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['BLUE'] + 'T E V I N   T H O M A S'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['YELLOW'] + '_______________________________________________________________'.center(int(get_term_column_length())) + colors_dict['NONE']
    print ''.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['GREEN'] + '[1] New Game      [2] Highscores'.center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['GREEN'] + '[3] Quit'.center(int(get_term_column_length())) + colors_dict['NONE']
    print ''.center(int(get_term_column_length())) + colors_dict['NONE']
    option = input('[ENTER]: ')
    if option in [1, 2, 3]:
        return option
    else:
        print colors_dict['RED'] + '[!] Unrecognized Input!' + colors_dict['NONE']
        return 3

def start_process(difficulty):
  game_status = 0
  grid = GridClass(level=difficulty)
  while game_status == 0:
    grid.spawn_shape()
    status = grid.check_status()
    game_status = status[0]
    if game_status == 2:
      grid.points += 1
      grid.remove_point_row(status[1])
      grid.row_sorted = False
      game_status = 0
  return game_status

def show_game_over():
  print colors_dict['RED'] + "   ________    ______    _________________________    _________    ____    _____________ ______    ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['RED'] + "  /  _____/   / __   \  /  ___   ___   /  _______/   /   ____  \  /   /   /  /  _______//  __  \   ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['RED'] + " /  /   ___  / /__    \/  /  /  /  /  /  /______    /   /    /  \/   /   /  /  /______ /  / /  /   ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['RED'] + " \   \  \  \/  ___    /  /  /  /  /  /  _______/    \       /   /   /   /  /  _______//  _    /    ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['RED'] + "  \   \_/  /  /   /  /  /  /  /  /  /  /______       \         /\   \__/  /  /______ /  / \   \    ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['RED'] + "   \______/__/   /__/__/  /__/  /__/_________/        \_______/  \_______/_________//__/   \___\   ".center(int(get_term_column_length())) + colors_dict['NONE']

def read_hi_score():
  hi_score_list = []
  with open(highscores.txt, 'r') as f:
    for line in f:
      hi_score_list.append(line)
  return hi_score_list

def show_hi_scores(hi_score_list):
  print colors_dict['PURPLE'] + "      ___    _______________   ___     ___________   _________________      ______   _________________  ".center(int(os.environ['COLUMNS'])) + colors_dict['NONE']    
  print colors_dict['PURPLE'] + "     / /    / /   /   ____/   / /     /    ____ /  /  _____//   ____  \    /  __  \ /  ______/   ____/  ".center(int(os.environ['COLUMNS'])) + colors_dict['NONE']
  print colors_dict['PURPLE'] + "    / -----/ /  //   /  ___  /  -----/ / \  \__   /  /     /   /    /  \  /  / /  /  /______  \  \__    ".center(int(os.environ['COLUMNS'])) + colors_dict['NONE']
  print colors_dict['PURPLE'] + "   /  ____  /  / \   \  \  \/  -----  /   \    \/  /       \       /    \/  _    /   _____ /   \     \  ".center(int(os.environ['COLUMNS'])) + colors_dict['NONE']
  print colors_dict['PURPLE'] + "  / /    / /  /   \   \_/  / /     / /_ ___/  /    \ _____   \             / \  \   /_____  __ /     /  ".center(int(os.environ['COLUMNS'])) + colors_dict['NONE']
  print colors_dict['PURPLE'] + " /_/    /_/__/     \______/_/     /_/_______/   \________/    \_______//__/   \___\_______/_________/   ".center(int(os.environ['COLUMNS'])) + colors_dict['NONE']

while running:
    choice = print_menu()
    hi_score_list = read_hi_score()
    if choice == 1:
        level = select_level()
        start_process(level)
        show_game_over()
        time.sleep(5)
        running = False
    elif choice == 2:
        show_hi_scores(hi_score_list)
    if choice == 3:
        running = False


''' Testing
if __name__ == '__main__':
  grid = GridClass(level=4)
  grid.draw()
  grid.spawn_shape()
  grid.draw()

#test          

'''
