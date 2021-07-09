from settings import *

grid = board1

def possible(x, y, n): # row(x) column (y) number(n)
    for i in range(0, 9):
        if grid[i][x] == n and i != y:
            return False # checks rows

    for i in range(0, 9):
         if grid[y][i] == n and i != x:
             return False # checks columns

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for X in range(x0, x0 + 3):
        for Y in range(y0, y0 + 3):
            if grid[Y][X] == n:
                return False # checks the box, checks box top left of grid and checks box 3*3 down right
    return True

def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(x, y, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    print(grid)

solve()

# need to pass board selected from app_class through backTracking to settings to make single solver button.