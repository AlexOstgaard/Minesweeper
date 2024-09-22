import pygame
import sys
import random
w_height = 800
w_width = w_height * 2
SCREEN = pygame.display.set_mode((w_width, w_height))
squareSize = int(w_height/20)
squareList = []
rows = []
mines = []
mineAmount = 120
squareQueue = []
squaresChecked = []
squaresFlagged = []
squaresOpened = []
firstClick = 0

#This for-loop creates the coordinates for every square.
#The rows-array contains each row as an array.
for x in range(1, w_width, squareSize):
    eachRow = []
    for y in range(1, w_height, squareSize):
        eachRow.append((x, y)) 
    rows.append(eachRow)

#This loop creates random mine locations
#Thereafter, as long as the coordinate is not occupied by another mine,
#The coordinate of the mine is appended to the mines-array
for x in range(mineAmount):
    while True:
        y_coordinate = random.randint(0, len(rows)-1)
        currRow = rows[y_coordinate]
        x_coordinate = random.randint(0, len(currRow)-1)
        currentMine = currRow[x_coordinate]

        if currentMine not in mines:
            mines.append(currentMine)
            break


def main():
    pygame.init()
    SCREEN.fill("dark gray")
    #The loop below runs until the user quits, or clicks on a mine.
    #Currently nothing happens when the player wins, but this should of course be added.
    while True:
        drawGrid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
#In minesweeper there are really only two buttons, as in the code beneath
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_coordinate = rows[mouse_pos[0]//squareSize][mouse_pos[1]//squareSize]

                if event.button == pygame.BUTTON_LEFT:
                    findSquare(mouse_coordinate)
                if event.button == pygame.BUTTON_RIGHT:
                    flag(mouse_coordinate)

        pygame.display.update()

#This function simply draws the black lines that makes up the grid
def drawGrid():
    for x in range(0, w_width, squareSize):
        for y in range(0, w_height, squareSize):
            rect = pygame.Rect(x, y, squareSize, squareSize)
            pygame.draw.rect(SCREEN, "black", rect, 1)

#When a square is opened, this function runs to check mines nearby.
#It also adds the number that is shown in the game, if there are mines nearby.            
def fillSquare(x, y):
    rect = pygame.Rect(x, y, squareSize, squareSize)
    
    minesNearby = 0
    #This loop counts all mines nearby
    for i in range(-1, 2):
        for j in range(-1, 2):
                if ((x+squareSize*i, y+squareSize*j)) in mines:
                    minesNearby += 1
                    
    if minesNearby > 0:
        pygame.draw.rect(SCREEN, "light gray", rect)
        myFont = pygame.font.SysFont("Arial", 25)
        SCREEN.blit(myFont.render(str(minesNearby), True, (0, 0, 0)), (x, y))
    else:
        pygame.draw.rect(SCREEN, "white", rect)
    squaresOpened.append((x, y))

#In order to avoid a blind guess on the first move,
#The firstSafe function simply deletes mines around the first square that is clicked.
#The only issue I find with this solution is that it reduces the total amount of mines that is in the code.
#Alternatively, a mark could be placed on a random square that does not contain a mine on the first move,
# to give the user a start.
def firstSafe(coordinate):
    for i in range(-1, 2):
        for j in range(-1, 2):
                if ((coordinate[0]+squareSize*i, coordinate[1]+squareSize*j)) in mines:
                    mines.remove((coordinate[0]+squareSize*i, coordinate[1]+squareSize*j))
    clickedSquare(coordinate)

#The clickedSquare function is called when a clicked square is not a mine.
#The functi
def clickedSquare(coordinate):
    
    x_coordinate = coordinate[0]
    y_coordinate = coordinate[1]
#In minesweeper, if there as as many flags nearby an opened square,
#as the square shows, the rest of the unopened squares opens automatically.
#If the flags are wrongly placed, then the program does what happens when a mine is clicked.
#The if-statement and its content runs this whole "shortcut operation"
    if (x_coordinate, y_coordinate) in squaresOpened:
        minesNearby = 0
        flagsNearby = 0
        miss = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x_coordinate+i*squareSize, y_coordinate+j*squareSize) in mines:
                    minesNearby+= 1
                if (x_coordinate+i*squareSize, y_coordinate+j*squareSize) in squaresFlagged:
                    flagsNearby+= 1 
                if minesNearby != flagsNearby:
                    miss += 1
#It is crucial that the number of mines and flags nearby are identical.
        if minesNearby == flagsNearby:
            if miss == 0:
                checkSquaresNearby(x_coordinate, y_coordinate)
            else: 
                pygame.quit()
                sys.exit()
#When the square clicked is a regular unopened square, the code below runs.
    else:
        fillSquare(x_coordinate, y_coordinate)
        minesNearby = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                    if ((x_coordinate+squareSize*i, y_coordinate+squareSize*j)) in mines:
                        minesNearby += 1          
#When a square that exists in an "island" of squares with no nearby mines,
# the program automatically opens all other squares around, so the user
# doesn't have to waste time opening squares that obvioulsy does not contain any mines.    
        if minesNearby == 0 and ((x_coordinate, y_coordinate)) not in squaresChecked:
    
            squareQueue.append((x_coordinate, y_coordinate))
#The squareQueue is a list of squares that are not close to any mines, and have not been checked yet.
#The program will search through the square in the list
    while len(squareQueue) > 0:
        checkSquaresNearby(squareQueue[0][0], squareQueue[0][1])
        squareQueue.pop(0)
#The function below checks all squares around the coordinates in the parameter. 
#It also  figures out if any of those squares have zero nearby mines, 
# and therefore also should be appended to the queue
def checkSquaresNearby(x, y):
    squaresChecked.append((x, y))
    
    for i in range(-1, 2):
            for j in range(-1, 2):
                if ((x+i*squareSize, y+j*squareSize)) not in squaresFlagged:
                    fillSquare(x+i*squareSize, y+j*squareSize)
                
                minesNearby = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if ((x+squareSize*i+squareSize*k, y+squareSize*j+squareSize*l)) in mines:
                            minesNearby +=1
#The very long if-statement below checks whether a square can be added to the squareQueue or not.
                if minesNearby == 0 and ((x+squareSize*i, y+squareSize*j)) not in squaresChecked and 0<x+squareSize*i<w_width and 0<y+squareSize*j<w_height and (x+squareSize*i, y+squareSize*j) not in squareQueue:
                    squareQueue.append((x+squareSize*i, y+squareSize*j))
                     
#The firstClick variable is part of the firstSafe function, explained above
def findSquare(coordinate):
    global firstClick
    
    if firstClick == 0:
        firstClick = 1
        firstSafe(coordinate)
    else:
        if coordinate not in squaresFlagged:
            if coordinate not in mines: 
                clickedSquare(coordinate)
            if coordinate in mines:
                pygame.quit()
                sys.exit()
    
        
#This function is called when the user right-clicks on a square.
#Checks if the square is opened first, and if it isn't, the square is marked with red.
#
def flag(coordinate):
    if coordinate not in squaresOpened:
        rect = pygame.Rect(coordinate[0], coordinate[1], squareSize, squareSize)
        if coordinate not in squaresFlagged:
            squaresFlagged.append(coordinate)
            pygame.draw.rect(SCREEN, "red", rect)
        else:
            squaresFlagged.remove(coordinate)
            pygame.draw.rect(SCREEN, "dark gray", rect)
        
main()