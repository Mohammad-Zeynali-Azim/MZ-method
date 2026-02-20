import pygame
import MG9846 as mg  # MZ-Method

# ===========================================Coloring graph====================
list3 = []
l2 = []
L1 = []
n = int(input("Please enter initial vale of cellular automata:"))
num1 = [int(d) for d in str(n)]
L1 = mg.Graph_Generate(num1, 101)
for i in range(1, 101):
    l2 = mg.Node_value_in_Level(i, L1)  # peyda kardane magadire satrha
    list3.append(l2)

# Define some colors for cells
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# zero = (242, 249, 254)
zero = (232, 239, 255)

one = (205, 231, 251)
two = (159, 209, 249)
three = (111, 186, 246)
four = (74, 168, 245)
five = (40, 153, 243)
six = (33, 138, 230)
seven = (21, 117, 209)
eight = (20, 97, 188)
nine = (51, 100, 175)

# sets the WIDTH and HEIGHT of each lattice cells
WIDTH = 10
HEIGHT = 10
MARGIN = 1
lattice = []
for row in range(308):
    # Add an empty array that will hold each cell
    # in this row
    lattice.append([])
    for column in range(304):
        lattice[row].append(40)  # Append a cell
# Set row 1, cell 5 to one. (Remember rows and # column numbers start at zero.)
if (n < 10):
    y = 64-(len(num1)//2*4-1)
    ynew = 64-(len(num1)//2*4-1)
    roww = 0
    for p in list3:
        if (roww == 0):
            ynew = 65 -(len(num1)//2*4-1)- 2
        else:
            ynew = 65 -(len(num1)//2*4-1)- roww - 3
        for k in p:
            lattice[roww][ynew] = k
            if (roww % 2 == 0 and roww != 0):
                ynew = ynew + 2
            else:
                ynew = ynew + 4
        roww = roww + 1
else:
    y = 64-(len(num1)//2*4-1)
    ynew =64-(len(num1)//2*4-1)
    roww = 0
    for p in list3:
        ynew = 65-(len(num1)//2*4-1) - roww - 3
        for k in p:
            lattice[roww][ynew] = k
            if (roww % 2 == 0):
                ynew = ynew + 4
            else:
                ynew = ynew + 2
        roww = roww + 1

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [1400, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Set title of screen
pygame.display.set_caption("Array Backed Lattice")
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    screen.fill(BLACK)
    # Draw the Lattice
    for row in range(308):
        for column in range(304):
            color = WHITE
            if lattice[row][column] == 0:
                color = zero
            if lattice[row][column] == 1:
                color = one
            if lattice[row][column] == 2:
                color = two
            if lattice[row][column] == 3:
                color = three
            if lattice[row][column] == 4:
                color = four
            if lattice[row][column] == 5:
                color = five
            if lattice[row][column] == 6:
                color = six
            if lattice[row][column] == 7:
                color = seven
            if lattice[row][column] == 8:
                color = eight
            if lattice[row][column] == 9:
                color = nine
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)
    pygame.display.flip()
    if event.type == pygame.QUIT:
        pygame.image.save(screen, "gangou369.png")  # ذخیره تصویر
        done = True
pygame.quit()
