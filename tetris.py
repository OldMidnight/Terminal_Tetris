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
  shape_dict: A dictionary containing a key-value relationship between a level and a list of potential shapes that can be spawned at that level. The shapes are split up
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
    self.grid.append(" " + ("_" * self.size))
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
    self.grid.append(" " + ("-" * self.size))

  def draw(self):
    '''
    The draw function of the grid. Anytime this function is called, the screen will be cleared and an updated grid will be redrawn.
    '''
    os.system('clear')
    for row in self.grid:
      print "".join(row)

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

    shape_num = random.randint(0, len(self.level['shape']) - 1)
    shape = self.level['shape'][shape_num]
    shape = shape.split('/')
    middle_of_row = len(self.grid[1]) / 2
    self.grid[1][middle_of_row:middle_of_row + len(shape)] = shape
    self.draw()
    return self.shape_movement(1)
      
  def shape_movement(self, current_row):
	next_row = current_row + 1
	if next_row == len(self.grid) - 1:
	  self.next_shape = True
	else:
	  temp_row = self.grid[next_row]
	  self.grid[next_row] = self.grid[current_row]
	  self.grid[current_row] = temp_row
	  time.sleep(self.level['speed'])
	  self.draw()
	if self.next_shape:
	  return True
	else:
	  return self.shape_movement(next_row)

def select_level():
    print '            S E L E C T   A   D I F F I C U L T Y :            '
    print ''
    print '                    [1]        E A S Y                         '
    print '                    [2]        M E D I U M                     '
    print '                    [3]        H A R D                         '
    print '                    [4]        Y O U   W O N T   W I N         '
    print ''
    level = raw_input('[ENTER]: ')
    if level == '1':
        print 'Taking it easy huh?'
        time.sleep(2)
        return 1
    elif level == '2':
        print 'Not much of a challenge really.'
        time.sleep(2)
        return 2
    elif level == '3':
        print "That's More like it!"
        time.sleep(2)
        return 3
    elif level == '4':
        print 'Abandon hope all ye who have chosen this option...'
        time.sleep(2)
        return 4

def print_menu():
    os.system('clear')
    print "     ______    ________    ________________     ___ _______    "
    print "    /      \  /        \  /         /  __  \   /  //  ____/    "
    print "   /  ____  \/   _____  \/___   ___/  / /  /  /  / \  \__      "
    print "  /  /   /  /\  /    /  /  /   /  /  _    /  /  /   \    \     "
    print " /         /  \        /  /   /  /  / \  \  /  / ___/    /     "
    print "/_________/    \______/  /___/  /__/   \__\/__/ /_______/      "
    print ''
    print '                   C A 2 7 8   P R O J E C T                   '
    print '_______________________________________________________________'
    print '                        M A D E   B Y :                        '
    print '                    F A R E E D   I D R I S                    '
    print '                     M O S E S   O P E B I                     '
    print '                     K E V I N   D O Y L E                     '
    print '                    T E V I N   T H O M A S                    '
    print '_______________________________________________________________'
    print ''
    print '                 [1] New Game      [2] Highscores              '
    print '                            [3] Quit                           '
    print ''
    option = input('[ENTER]: ')
    if option in [1, 2, 3]:
        return option
    else:
        print '[!] Unrecognized Input!'
        return 3

def start_process(difficulty):
  game_status = 0
  grid = GridClass(level=difficulty)
  while game_status != 1:
    process = grid.spawn_shape()

while running:
    choice = print_menu()
    if choice == 1:
        level = select_level()
        start_process(level)
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
