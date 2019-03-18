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

def outer_grid(x):
  width = ["-"]
  lside = ["|"]
  rside = ["|"]
  spaces = []
  i = 0
  while i < x:
    width.append("-")
    spaces.append(" ")
    i = i + 1
  print (" ").join(width)
  
  j = 0
  while j < len(width) + 8:
    print (" ").join(lside) + (" ").join(spaces) + (" ").join(rside)
    j = j + 1
  print (" ").join(width)

#It outputs 1 size bigger than the actual input
#Incase any of you wanna test it.
outer_grid(23)

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
