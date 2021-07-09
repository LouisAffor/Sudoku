import pygame, sys
import requests
from bs4 import BeautifulSoup
from settings import *
from buttonClass import *

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True       
        self.selected = None
        self.mousePos = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.playingButtons = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont("arial", (cellSize//2), False)
        self.grid = []
        self.getPuzzle("1")
        self.getPuzzle2
        self.getPuzzle3
        self.getPuzzle4
        self.getSol1
        self.getSol2
        self.getSol3



    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

    

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
            # user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playingButtons:
                        if button.highlighted:
                            button.click()

            # user types a key
            if event.type == pygame.KEYDOWN:
                if self.selected != None and list(self.selected) not in self.lockedCells: #Need to compare list(not tuple) with list
                    if self.isInt(event.unicode):
                        # cell changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True

    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)

        if self.cellChanged:
            self.incorrectCells = []
            if self.checkComp():
                # check if board is completed correctly
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    self.finished = True
     
    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)

        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)

        self.shadeIncorrectCells(self.window, self.incorrectCells)
        
        self.drawNumbers(self.window) 
        
        self.drawGrid(self.window)
        pygame.display.update()

        self.cellChanged = False



    def checkComp(self):
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        return True

    def checkAllCells(self):
        self.checkRows()
        self.checkCols()
        self.check3x3Grid()

    def checkRows(self): # check no repeat number in rows
        for yidx, row in enumerate(self.grid):
            possible = [1,2,3,4,5,6,7,8,9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possible:
                    possible.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx,yidx])
                    if [xidx, yidx] in self.lockedCells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.lockedCells:
                                self.incorrectCells.append([k, yidx])

    def checkCols(self): # check no repeat number in Cols
        for xidx in range(9):    
            possible = [1,2,3,4,5,6,7,8,9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possible:
                    possible.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx,yidx])
                    if [xidx, yidx] in self.lockedCells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.lockedCells:
                                self.incorrectCells.append([xidx, k])

    def check3x3Grid(self):
        for x in range(3):
            for y in range(3):
                possible = [1,2,3,4,5,6,7,8,9]
                for i in range(3):
                    for j in range(3):
                        xidx = x*3+i
                        yidx = y*3+j
                        if self.grid[yidx][xidx] in possible:
                            possible.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                                self.incorrectCells.append([xidx, yidx])
                            if [xidx, yidx] in self.lockedCells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x*3+k
                                        yidx2 = y*3+l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx2] not in self.lockedCells:
                                            self.incorrectCells.append([xidx2, yidx2])
   


    def getPuzzle(self, difficulty):
        # difficulty passed in as string with 1 - 4 (1 easiest, 4 Hardest)
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
        soup = BeautifulSoup(html_doc, features="lxml")
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f10', 'f11', 'f12', 'f13',
        'f14', 'f15', 'f16', 'f17', 'f18', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27',
        'f28', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f40', 'f41', 'f42',
        'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56',
        'f57', 'f58', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f70', 'f71',
        'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f80', 'f81', 'f82', 'f83', 'f84', 'f85',
        'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index//9][index%9] = int(cell['value'])
            except:
                pass
        self.grid = board
        self.load()

    def getPuzzle2(self):
        self.grid = board1
        self.load()

    def getPuzzle3(self):
        self.grid = board2
        self.load()

    def getPuzzle4(self):
        self.grid = board3
        self.load()

    def getSol1(self):
        self.grid = sol1
        self.load()

    def getSol2(self):
        self.grid = sol2
        self.load()

    def getSol3(self):
        self.grid = sol3
        self.load()

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, WHITE, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))
    
    def shadeIncorrectCells(self, window, incorrect):
        for cell in incorrect:
            pygame.draw.rect(window, LIGHTBLUE, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [(xidx*cellSize)+gridPos[0], (yidx*cellSize)+gridPos[1]]
                    self.textToScreen(window, str(num), pos)

    def drawSelection(self, window, pos):
        pygame.draw.rect(window, LIGHTGREY, ((pos[0]*cellSize)+gridPos[0], (pos[1]*cellSize)+gridPos[1], cellSize, cellSize ))

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH-50, HEIGHT-150),2,2)
        for x in range(9):
            pygame.draw.line(window, BLACK, (gridPos[0]+(x*cellSize), gridPos[1]),(gridPos[0]+(x*cellSize), gridPos[1]+449), 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1]+(x*cellSize)),(gridPos[0]+449, gridPos[1]+(x*cellSize)), 2 if x % 3 == 0 else 1)

    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        elif self.mousePos[0] > gridPos[0]+gridSize or self.mousePos[1] > gridPos[1]+gridSize:
            return False
        return ((self.mousePos[0] - gridPos[0])//cellSize, (self.mousePos[1]-gridPos[1])//cellSize)

    def loadButtons(self):
        self.playingButtons.append(Button(125, 560, 100, 30,
        function = self.checkAllCells, colour=(GREY), text="Check"))

        self.playingButtons.append(Button(25,40, 100, 40,
        colour=(GREY), function=self.getPuzzle2,
        text = "Easy"))

        self.playingButtons.append(Button(141,40, 100, 40,
        colour=(GREY), function=self.getPuzzle3,
        text = "Medium"))

        self.playingButtons.append(Button(259,40, 100, 40,
        colour=(GREY), function=self.getPuzzle4,
        text = "Hard"))

        self.playingButtons.append(Button(375,40, 100, 40,
        colour=(GREY), function=self.getPuzzle,
        params="2", text = "Random")) # random difficulty set to medium, could use a variable set to random for random difficulty

        self.playingButtons.append(Button(105, 60, 20, 20, 
        function = self.getSol1, colour=(DIMGREY), text="S")) 

        self.playingButtons.append(Button(221, 60, 20, 20, 
        function = self.getSol2, colour=(DIMGREY), text="S")) 

        self.playingButtons.append(Button(339, 60, 20, 20, 
        function = self.getSol3, colour=(DIMGREY), text="S"))
       
    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize-fontWidth)//2
        pos[1] += (cellSize-fontHeight)//2
        window.blit(font, pos)

    def load(self):
        self.playingButtons = []
        self.loadButtons()
        self.lockedCells = []
        self.incorrectCells = []
        self.finished = False

        # Setting for locking cells from original board
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx, yidx])

    def isInt(self,string):
        try:
            int(string)
            return True
        except:
            return False













