#!/usr/bin/env python
'''
CA278 Project: DOTris: Modified Tetris
Maintainers:
Fareed Idris
Kevin Doyle
Moses Opebi
Tevin Thomas
'''

# Global Variables
running = True

import random
import os
import time

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
    self.grid.append("-" * self.size)

  def draw(self):
    '''
    The draw function of the grid. Anytime this function is called, the screen will be cleared and an updated grid will be redrawn.
    '''
    os.system('clear')
    print 'S C O R E :' + str(self.points).center(int(os.environ['COLUMNS']))
    for row in self.grid:
      print "".join(row).center(int(os.environ['COLUMNS']))
    print 'I N C O M I N G   S H A P E :' + "".join(self.incoming_shape).center(int(os.environ['COLUMNS']))

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
    if self.incoming_shape == '':
      current_shape_num = random.randint(0, len(self.level['shape']) - 1)
      shape = self.level['shape'][current_shape_num].split('/')
    else:
      shape = self.incoming_shape
    next_shape_num = random.randint(0, len(self.level['shape']) - 1)
    self.incoming_shape = self.level['shape'][next_shape_num].split('/')
    middle_of_row = len(self.grid[1]) / 2
    self.grid[1][middle_of_row:middle_of_row + len(shape)] = shape
    for a in range(middle_of_row, middle_of_row + len(shape)):
      self.grid[2][a] = ' '
    self.draw()
    return self.shape_movement(1, middle_of_row, middle_of_row + len(shape))
      
  def shape_movement(self, current_row, shape_start_index, shape_end_index):
    next_row = current_row + 1
    if next_row == len(self.grid) - 1:
      self.next_shape = True
    if self.next_shape == False:
      for a in range(shape_start_index, shape_end_index):
        if self.grid[next_row][a] == '.':
          self.next_shape = True
    if self.next_shape == False:
      temp_row = self.grid[next_row]
      self.grid[next_row] = self.grid[current_row]
      self.grid[current_row] = temp_row
      time.sleep(self.level['speed'])
      self.draw()
    if self.next_shape:
      return True
    else:
      self.shape_movement(next_row, shape_start_index, shape_end_index)
  def check_status(self):
    if '.' in self.grid[1]:
        return [1]
    else:
        i = 1
        while i < len(self.grid):
            if ' ' not in self.grid[i]:
                return [2, i]
            i += 1
        return [0]

def select_level():
    print '            S E L E C T   A   D I F F I C U L T Y :            '.center(int(os.environ['COLUMNS']))
    print ''.center(int(os.environ['COLUMNS']))
    print '                    [1]        E A S Y                         '.center(int(os.environ['COLUMNS']))
    print '                    [2]        M E D I U M                     '.center(int(os.environ['COLUMNS']))
    print '                    [3]        H A R D                         '.center(int(os.environ['COLUMNS']))
    print '                    [4]        Y O U   W O N T   W I N         '.center(int(os.environ['COLUMNS']))
    print ''.center(int(os.environ['COLUMNS']))
    level = raw_input('[ENTER]: ')
    if level == '1':
        print 'Taking it easy huh?'.center(int(os.environ['COLUMNS']))
        time.sleep(2)
        return 1
    elif level == '2':
        print 'Not much of a challenge really.'.center(int(os.environ['COLUMNS']))
        time.sleep(2)
        return 2
    elif level == '3':
        print "That's More like it!".center(int(os.environ['COLUMNS']))
        time.sleep(2)
        return 3
    elif level == '4':
        print 'Abandon hope all ye who have chosen this option...'.center(int(os.environ['COLUMNS']))
        time.sleep(2)
        return 4

def print_menu():
    os.system('clear')
    print "     ______    ________    ________________     ___ _______    ".center(int(os.environ['COLUMNS']))
    print "    /      \  /        \  /         /  __  \   /  //  ____/    ".center(int(os.environ['COLUMNS']))
    print "   /  ____  \/   _____  \/___   ___/  / /  /  /  / \  \__      ".center(int(os.environ['COLUMNS']))
    print "  /  /   /  /\  /    /  /  /   /  /  _    /  /  /   \    \     ".center(int(os.environ['COLUMNS']))
    print " /         /  \        /  /   /  /  / \  \  /  / ___/    /     ".center(int(os.environ['COLUMNS']))
    print "/_________/    \______/  /___/  /__/   \__\/__/ /_______/      ".center(int(os.environ['COLUMNS']))
    print ''.center(int(os.environ['COLUMNS']))
    print '                   C A 2 7 8   P R O J E C T                   '.center(int(os.environ['COLUMNS']))
    print '_______________________________________________________________'.center(int(os.environ['COLUMNS']))
    print '                        M A D E   B Y :                        '.center(int(os.environ['COLUMNS']))
    print '                    F A R E E D   I D R I S                    '.center(int(os.environ['COLUMNS']))
    print '                     M O S E S   O P E B I                     '.center(int(os.environ['COLUMNS']))
    print '                     K E V I N   D O Y L E                     '.center(int(os.environ['COLUMNS']))
    print '                    T E V I N   T H O M A S                    '.center(int(os.environ['COLUMNS']))
    print '_______________________________________________________________'.center(int(os.environ['COLUMNS']))
    print ''.center(int(os.environ['COLUMNS']))
    print '                 [1] New Game      [2] Highscores              '.center(int(os.environ['COLUMNS']))
    print '                            [3] Quit                           '.center(int(os.environ['COLUMNS']))
    print ''.center(int(os.environ['COLUMNS']))
    option = input('[ENTER]: ')
    if option in [1, 2, 3]:
        return option
    else:
        print '[!] Unrecognized Input!'
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
      #grid.remove_point_row(status[1])
      #grid.row_sorted = False
      game_status = 0
  return game_status

def show_game_over():
  print ""
while running:
    choice = print_menu()
    if choice == 1:
        level = select_level()
        start_process(level)
        show_game_over()
        running = False
    elif choice == 3:
        show_highscores()
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
