'''
Tetris.py
CA278 Project
Maintainers:
    Fareed Idris
    Kevin Doyle
    Moses Opebi
    Tevin Thomas
'''
######################################################################
#Functions

#GRID
def create_grid(size=20):
  grid = []
  grid.append(" " + ("_" * size))
  i = 1
  while i < size:
    grid.append([])
    grid[i].append("|")
    j = 0
    while j < size:
      grid[i].append(' ')
      j = j + 1
    grid[i].append("|")
    i = i + 1
  grid.append(" " + ("-" * size))	
  return grid
  token = grid[0]

def draw_grid(grid):
  for row in grid:
    print "".join(row)

draw_grid(create_grid())

#shapes
levels = { 
  1: ["..","...."],
  2: [".","..","..."],
  3: [".","..","....","......",],
  4: [".","..","...","....",".....",".......",]
  }
def get_shape(size=len(levels)):
  import random
  for num in range(1):
    n = random.randint(1,size)
    lvl = levels[n]
    for shape in range(1):
	  dot = random.randint(0,(len(lvl) - 1))
	  shape = list(lvl[dot])
#add shapes

def draw_shape(token):
  middle = len(token) / 2
  token[middle:(middle + len(shape))] = shape

# I know some of the names for the functions are different but this is just for me to test it myself before i change it
draw_grid(create_grid(draw_shape(get_shape()))
	
######################################################################
# GLOBAL VARIABLES HERE
######################################################################
#running = True
######################################################################
# SHAPES HERE

######################################################################

shape_dict = {
 level_1: [".",".","./.","./.","./."]
 level_2: ["./.","./.","././.","./.","././."]
 level_3: ["././.","./.","./././.","././.","./././."]
 level_4: ["./././.","./././.","././.","./././.","."]
}
          

######################################################################
# GRID HERE
# I looked up the dimesions of  a rectangle.(x,x + 8)

#def outer_grid(x):
 # width = ["-"]
  #lside = ["|"]
  #rside = ["|"]
  #spaces = []
  #i = 0
  #while i < x:
   # width.append("-")
   # spaces.append(" ")
   # i = i + 1
  #print (" ").join(width)
  
  #j = 0
  #while j < len(width) + 8:
   # print (" ").join(lside) + (" ").join(spaces) + (" ").join(rside)
   # j = j + 1
  #print (" ").join(width)

#It outputs 1 size bigger than the actual input but it still looks good.
#Incase any of you wanna test it.

######################################################################
######################################################################
# FUNCTIONS HERE
######################################################################
#def draw_grid()

#def draw_square()

#def draw_line()

#def draw_complex()

#def get_shape()

#def drop_shape()

#def check_loss()

#def check_win()

#def show_menu()

######################################################################
# GAME LOOP HERE
######################################################################
#while running:
#   show_menu