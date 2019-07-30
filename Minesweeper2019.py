import pygame
import random
import time
import math

pygame.init()

width = 20
height = 20
mines = math.floor(width * height * 0.15) # Normal(0.15), Medium(0.2), Hard(0.25)
flags = 0
board = [[0 for i in range(width)] for ii in range(height)]
compiled_board = [(x, y) for x in range(width) for y in range(height)]
secondary_board = board
mineGrid = []


class HiddenCell:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def touching(self, x, y):
        return x in range(self.x, self.x+self.width) and y in range(self.y, self.y+self.height)


class GameBoard:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def makeMine(x, y):
        matrix = [(x+i, y+ii) for i in range(-1, 2) for ii in range(-1, 2)]
        matrix.remove((x, y)) # the center piece is going to be mine and therefore can't have a value
        for b in matrix:
            try:
                thisValue = board[b[1]][b[0]]
                if thisValue == 'X':
                    pass
                else:
                    thisValue += 1
                board[b[1]][b[0]] = thisValue
            except:
                pass

    def getNeighbors(x, y):
        matrix = [(x+i, y+ii) for i in range(-1, 2) for ii in range(-1, 2)]
        matrix.remove((x, y)) # the center piece is going to be mine and therefore can't have a value
        return matrix

    def flag(x, y):
        global mines
        flags += 1
        mines -= 1
        secondary_board[y][x] = 'F'

    def unflag(x, y):
        global mines
        flags -= 1
        mines += 1
        secondary_board[y][x] = 'f'

def floodFill(x, y):
    global selected
    for cell in GameBoard.getNeighbors(x, y):
        if cell not in mineGrid and cell not in selected:
            reveal(cell[0], cell[1])


def reveal(x, y):
    global compiled_board
    global board
    global selected
    if (x, y) in compiled_board:
        selected.append((x, y))
    else:
        return
    try:
        if board[y][x] == 0:
            # Flood fill algorithm time!!!
            floodFill(x, y)
    except:
        return

def chooseMines(amt):
    global mineGrid
    random.shuffle(compiled_board)
    mineGrid = compiled_board[0:amt]

win = pygame.display.set_mode((width * 30, height * 30 + 50))
pygame.display.set_caption('Minesweeper!!!')

top_panel_left = pygame.image.load('top-panel-left.png')
top_panel_left = pygame.transform.scale(top_panel_left, (100, 50))
top_panel_right = pygame.image.load('top-panel-right.png')
top_panel_right = pygame.transform.scale(top_panel_right, (100, 50))
top_panel_middle = pygame.image.load('top-panel-middle.png')
top_panel_middle = pygame.transform.scale(top_panel_middle, (width * 30 - 200, 50))
hidden_cell = pygame.image.load('hidden_cell.png')
hidden_cell = pygame.transform.scale(hidden_cell, (30, 30))
back_grid = pygame.image.load('back-grid.png')
back_grid = pygame.transform.scale(back_grid, (30, 30))
flagged_cell = pygame.image.load('hidden_cell-flagged.png')
flagged_cell = pygame.transform.scale(flagged_cell, (30, 30))
start_button = pygame.image.load('start_button.png').convert()
start_button = pygame.transform.smoothscale(start_button, (24, 24))
end_button = pygame.image.load('end_button.png').convert()
end_button = pygame.transform.smoothscale(end_button, (24, 24))
numbered_cells = [pygame.image.load('game-block-1.png'), pygame.image.load('game-block-2.png'), pygame.image.load('game-block-3.png'), pygame.image.load('game-block-4.png'), pygame.image.load('game-block-5.png'), pygame.image.load('game-block-6.png'), pygame.image.load('game-block-7.png')]
for i in range(len(numbered_cells)):
    numbered_cells[i] = pygame.transform.scale(numbered_cells[i], (30, 30))
mine_cell = pygame.image.load('game-block-MINE.png')
mine_cell = pygame.transform.scale(mine_cell, (30, 30))

numbered_times = [
    pygame.image.load('time-0.png'),
    pygame.image.load('time-1.png'),
    pygame.image.load('time-2.png'),
    pygame.image.load('time-3.png'),
    pygame.image.load('time-4.png'),
    pygame.image.load('time-5.png'),
    pygame.image.load('time-6.png'),
    pygame.image.load('time-7.png'),
    pygame.image.load('time-8.png'),
    pygame.image.load('time-9.png')
]

for i in range(10):
    numbered_times[i] = pygame.transform.scale(numbered_times[i], (13, 24))

def displayNumber(string, offset=0):
    if len(string) == 1:
        win.blit(numbered_times[int(string[0])], (46 + offset, 13))
        win.blit(numbered_times[0], (33 + offset, 13))
        win.blit(numbered_times[0], (20 + offset, 13))
    elif len(string) == 2:
        win.blit(numbered_times[int(string[0])], (33 + offset, 13))
        win.blit(numbered_times[int(string[1])], (46 + offset, 13))
        win.blit(numbered_times[0], (20 + offset, 13))
    elif len(string) == 3:
        win.blit(numbered_times[int(string[0])], (20 + offset, 13))
        win.blit(numbered_times[int(string[1])], (33 + offset, 13))
        win.blit(numbered_times[int(string[2])], (46 + offset, 13))
    elif len(string) >= 4:
        win.blit(numbered_times[9], (33 + offset, 13))
        win.blit(numbered_times[9], (20 + offset, 13))
        win.blit(numbered_times[9], (46 + offset, 13))

clock = pygame.time.Clock()
timeCount = 0
timeString = str(timeCount)


run = True
#selected = [(x, y) for x in range(10) for y in range(10)]
selected = []
s1 = True
s2 = True
fail = False

def generateMines():
    for i in mineGrid:
        GameBoard.makeMine(i[0], i[1])

chooseMines(mines)
generateMines()
print(mineGrid)

while run:
    selected = set(selected)
    selected = list(selected)
    win.fill((190, 190, 190))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    mouse_clicked_left = pygame.mouse.get_pressed()[0]
    mouse_clicked_right = pygame.mouse.get_pressed()[2]

    pygame.draw.rect(win, (255, 255, 255), (0, 0, 300, 50))

    for i in range(width):
        for ii in range(height):
            if mouse_x in range(i * 30, i * 30 + 30) and mouse_y - 50 in range(ii * 30, ii * 30 + 30):
                if mouse_clicked_left and secondary_board[ii][i] != 'F' and (i, ii) not in selected:
                    reveal(i, ii)
                    if (i, ii) in mineGrid:
                        selected = [(x, y) for x in range(width) for y in range(height)]
                        fail = True

            if mouse_clicked_right:
                if mouse_x in range(i * 30, i * 30 + 30) and mouse_y - 50 in range(ii * 30, ii * 30 + 30) and mouse_clicked_right and (i, ii) not in selected:
                    if s1:
                        if secondary_board[ii][i] == 'F':
                            secondary_board[ii][i] = 'f'
                            flags -= 1
                            s1 = False
                            time.sleep(0.3)
                        else:
                            secondary_board[ii][i] = 'F'
                            flags += 1
                            s1 = False
                            time.sleep(0.3)
            else:
                s1 = True

    start_button_x = int(width * 30 / 2 - 12)
    start_button_endX = start_button_x + 24
    if mouse_x in range(start_button_x, start_button_endX) and mouse_y in range(13, 37) and mouse_clicked_left:
        if s2:
            timeCount = 0
            selected = []
            board = [[0 for i in range(width)] for ii in range(height)]
            compiled_board = [(x, y) for x in range(width) for y in range(height)]
            secondary_board = board
            mineGrid = []
            flags = 0
            chooseMines(mines)
            generateMines()
            s2 = False
            fail = False
    else:
        s2 = True

    win.blit(top_panel_left, (0, 0))

    win.blit(top_panel_middle, (100, 0))

    win.blit(top_panel_right, (width * 30 - 100, 0))

    if not fail:
        win.blit(start_button, (width * 30 / 2 - 12, 13))
    else:
        win.blit(end_button, (width * 30 / 2 - 12, 13))

    displayNumber(timeString)
    displayNumber(str(flags), width * 30 - 80)

    for x in range(width):
        for y in range(height):
            if secondary_board[y][x] == 0:
                win.blit(back_grid, (x*30, y*30 + 50))

            if secondary_board[y][x] == 1:
                win.blit(numbered_cells[0], (x*30, y*30 + 50))

            if secondary_board[y][x] == 2:
                win.blit(numbered_cells[1], (x*30, y*30 + 50))

            if secondary_board[y][x] == 3:
                win.blit(numbered_cells[2], (x*30, y*30 + 50))

            if secondary_board[y][x] == 4:
                win.blit(numbered_cells[3], (x*30, y*30 + 50))

            if secondary_board[y][x] == 5:
                win.blit(numbered_cells[4], (x*30, y*30 + 50))

            if secondary_board[y][x] == 6:
                win.blit(numbered_cells[5], (x*30, y*30 + 50))

            if secondary_board[y][x] == 7:
                win.blit(numbered_cells[6], (x*30, y*30 + 50))

            if (x, y) in mineGrid:
                win.blit(mine_cell, (x*30, y*30 + 50))

            if (x, y) not in selected:
                win.blit(hidden_cell, (x*30, y*30 + 50))

            if secondary_board[y][x] == 'F' and not fail:
                win.blit(flagged_cell, (x*30, y*30 + 50))

    pygame.display.update()

    if fail:
        win.blit(end_button, (width * 30 / 2 - 12, 13))
        pygame.display.update()

    if width * height - len(selected) == mines: # checks for a win
        print("You Win!!")

    timeCount += clock.get_time()*0.001
    timeString = str(math.floor(timeCount))
    clock.tick()
