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

def create_grid(size = 21):
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

create_grid(21)

def draw_grid(grid):
  for row in grid:
    print "".join(row)

draw_grid(create_grid(21))
######################################################################
# GLOBAL VARIABLES HERE
######################################################################
#running = True
######################################################################
# SHAPES HERE

######################################################################
######################################################################
# GRID HERE
# I looked up the dimesions of  a rectangle.(x,x + 8)
''' - - - - - - 
    |         |
	|         |
	|         |
	|	      |
	|         |
    - - - - - -
'''

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
