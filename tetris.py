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
      'speed': 0.75,
      'level': 'Easy'
    },
    2: {
      'shape': ["././.", "./././.", "././././."],
      'speed': 0.5,
      'level': 'Medium'
    },
    3: {
      'shape': ["././././.", "./././././.", "././././././."],
      'speed': 0.25,
      'level': 'Hard'
    },
    4: {
      'shape': ["././././././.", "./././././././."],
      'speed': 0.1,
      'level': "You Can't Win"
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
    return self.shape_movement(1, middle_of_row, middle_of_row + len(shape))
      
  def shape_movement(self, current_row, shape_start_index, shape_end_index):
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
      self.draw()

      move, o, e = select([sys.stdin], [], [], self.level['speed'])

      if (move):
        direction = sys.stdin.readline().strip()
        if direction == 'd' or direction == 'D':
          if self.grid[next_row][shape_end_index] == ' ':
            shape_end_index = shape_end_index + 1
            shape_start_index = shape_start_index + 1
        elif direction == 'a' or direction == 'A':
          if self.grid[next_row][shape_start_index - 1] == ' ':
            shape_end_index = shape_end_index - 1
            shape_start_index = shape_start_index - 1

    if self.next_shape:
      return True
    else:
      self.shape_movement(next_row, shape_start_index, shape_end_index)

  def remove_point_row(self, row_to_sort):
    '''
    This function is used to remove a row that has been filled with dots, meaning a point can be gained. The function also adjusts the entire grid so that
    all rows above the completed row is moved a row down.:q
    a temporary variable is created to store the row above the current row being adusted. this ensures that self.grid[row_to_sort] does not become a reference to a different row.
    no using a temporary row will cause 2 shapes being created on the next spawn.
    arguments passed:
    row_to_sort: This is an integer that indicates the number of the row to be removed
    '''
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
    # [game_status, row_to_remove] or [game_status]
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
    print colors_dict['RED'] + "   ________    ______    _________________________    _________    ____    _____________ ______    ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['RED'] + "  /  _____/   / __   \  /  ___   ___   /  _______/   /   ____  \  /   /   /  /  _______//  __  \   ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['RED'] + " /  /   ___  / /__    \/  /  /  /  /  /  /______    /   /    /  \/   /   /  /  /______ /  / /  /   ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['RED'] + " \   \  \  \/  ___    /  /  /  /  /  /  _______/    \       /   /   /   /  /  _______//  _    /    ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['RED'] + "  \   \_/  /  /   /  /  /  /  /  /  /  /______       \         /\   \__/  /  /______ /  / \   \    ".center(int(get_term_column_length())) + colors_dict['NONE']
    print colors_dict['RED'] + "   \______/__/   /__/__/  /__/  /__/_________/        \_______/  \_______/_________//__/   \___\   ".center(int(get_term_column_length())) + colors_dict['NONE']
    if self.points != 0:
      score_added = False
      while score_added == False:
        name = raw_input('Please enter name:\n')
        if name:
          if len(name) >= 4:
            with open ('scores.txt', 'w') as f:
              f.write(name + ':' + str(self.points) + ':' + self.level['level'])
            score_added = True
          else:
            print colors_dict['RED'] + '[!] Name Too Short! Name must be atleast 4 characters.' + colors_dict['NONE']
        else:
          print colors_dict['RED'] + '[!] Unrecognized Input.' + colors_dict['NONE']

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
    print colors_dict['GREEN'] + '[3] How To Play   [4] Quit'.center(int(get_term_column_length())) + colors_dict['NONE']
    print ''.center(int(get_term_column_length())) + colors_dict['NONE']
    option = input('[ENTER]: ')
    if option in [1, 2, 3, 4]:
        return option
    else:
        print colors_dict['RED'] + '[!] Unrecognized Input!' + colors_dict['NONE']
        return 4

def start_process(difficulty):
  game_status = 0
  # Creates Instance of GridClass
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
  grid.gameover()
  return game_status

def show_highscores():
  os.system("clear")
  print colors_dict['PURPLE'] + "      ___     ___ ___ ________    ___      ___________   _________________     ______   _________________  ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['PURPLE'] + "     /  /    /  //  //   ____/   /  /     /  /   ____/  /  _____//   ____  \  /  __  \ /  ______/   ____/  ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['PURPLE'] + "    /  /____/  //  //   /  ___  /  /_____/  / \  \__   /  /     /   /    /  \/  / /  //  /____  \  \__     ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['PURPLE'] + "   /  ____    //  / \   \  \  \/  ______   /   \    \ /  /       \      /   /  _    //   ____/   \_    \   ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['PURPLE'] + "  /  /    /  //  /   \   \_/  /  /     /  /_ ___/  /  \  \ _____  \        /  / \  \/   /____ ____/    /   ".center(int(get_term_column_length())) + colors_dict['NONE']
  print colors_dict['PURPLE'] + " /__/    /__//__/     \______/__/     /__/________/    \________/  \______/__/   \__\_______//________/    ".center(int(get_term_column_length())) + colors_dict['NONE']
  print ''
  print colors_dict['YELLOW'] + '_______________________________________________________________'.center(int(get_term_column_length())) + colors_dict['NONE']
  print ''
  with open('scores.txt') as f:
    lines = f.readlines()
  if len(lines) == 0:
    print (colors_dict['RED'] + 'N O   H I G H S C O R E S   Y E T !' + colors_dict['NONE']).center(int(get_term_column_length()))
  else:
    for line in lines:
      line = line.strip().split(':')
      username = line[0]
      score = line[1]
      difficulty = line[2]
      if difficulty == 1:
        difficulty = 'Easy'
      elif difficulty == 2:
        difficulty = 'Medium'
      elif difficulty == 3:
        difficulty = 'Hard'
      elif difficulty == 4:
        difficulty = "You Can't Win"
      print (colors_dict['BLUE'] + username + colors_dict['NONE'] + ' - ' + colors_dict['GREEN'] + score + colors_dict['NONE'] + ' - ' + colors_dict['PURPLE'] + 'Difficulty: ' + difficulty + colors_dict['NONE']).center(int(get_term_column_length()))
  close = raw_input()
  if close:
    return

def show_how_to():
  os.system('clear')
  print colors_dict['BLUE'] + "How To Play DOTris:".center(int(get_term_column_length())) + colors_dict['NONE']
  print ''
  print colors_dict['YELLOW'] + '____________________________________________________________________'.center(int(get_term_column_length())) + colors_dict['NONE']
  print ''
  print colors_dict['GREEN'] + 'Movement'.center(int(get_term_column_length())) + colors_dict['NONE']
  print ''
  print (colors_dict['GREEN'] + 'A/a' + colors_dict['NONE'] + ' - Move Left').center(int(get_term_column_length())) + colors_dict['NONE']
  print (colors_dict['GREEN'] + 'D/d' + colors_dict['NONE'] + ' - Move Right').center(int(get_term_column_length())) + colors_dict['NONE']
  print ''
  print colors_dict['RED'] + '[!] Y O U   M U S T   P R E S S   "E N T E R"   I M M E D I A T E L Y   A F T E R   P R E S S I N G   A    L E T T E R   F O R   Y O U R   I N P U T   T O   R E G I S T E R ! ! !'.center(int(get_term_column_length())) + colors_dict['NONE']
  close = raw_input()
  if close:
    return

while running:
    choice = print_menu()
    if choice == 1:
      level = select_level()
      start_process(level)
      running = False
    elif choice == 2:
      show_highscores()
    elif choice == 3:
      show_how_to()
    elif choice == 4:
      running = False