from random import choice

def check_win(grid):
    
    for player in range(1, 3):
        # Check all rows
        for y in range(3):
            if all(map(lambda x: x == player, grid[y])):
                return player
        
        # Check all cols
        for x in range(3):
            if all(map(lambda x: x == player, [grid[i][x] for i in range(3)])):
                return player
        
        # Diagonals
        if all(map(lambda x: x == player, [grid[i][i] for i in range(3)])):
            return player
        if all (map(lambda x: x == player, [grid[2-i][i] for i in range(3)])):
            return player
        
    return 0
        

def make_move(grid, player = 2) -> tuple[int, int]:
    candidates = []
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == 0:
                candidates.append((x, y))

    return choice(candidates)