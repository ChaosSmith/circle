import random
from rvb.models.village import Village

def get_neighbors(x,y, height, width):
    neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return set([n for n in neighbors if n[0] < width and n[0] >= 0 and n[1] < height and n[1] >= 0])

def build_grid(width, height, game_id, mountains, mountain_size, villages):
    grid = [[{"x": x, "y": y, "type": "empty", "tile": " ", "move": False} for x in range(width)] for y in range(height)]
    for _ in range(mountains):
        x = random.randint(0,width-1)
        y = random.randint(0,width-1)
        if grid[y][x]["type"] == "empty":
            grid[y][x]["type"] = "mountain"
            grid[y][x]["tile"] = "M"
            neighbors = list(get_neighbors(x,y,height,width))
            for i in range(mountain_size-1):
                choice = random.choice(neighbors)
                grid[choice[1]][choice[0]]["type"] = "mountain"
                grid[choice[1]][choice[0]]["tile"] = "M"
                neighbors = list(set(neighbors) | get_neighbors(choice[0], choice[1],height,width))

    v_loc = []

    for _ in range(villages):
        x = random.randint(0,width-1)
        y = random.randint(0,width-1)
        for attempt in range(10):
            if grid[y][x]["type"] == "empty" and (x,y) not in v_loc:
                v_loc.append((x,y))
                grid[y][x]["tile"] = "V"
                Village.create(x=x, y=y, population=100, food=100, game_id=game_id)
                break

    return grid

def display_grid(grid):
    for y in range(len(grid)):
        new_line = []
        for x in range(len(grid[y])):
                new_line.append(grid[y][x]["tile"])
        print("".join(new_line))

# grid = build_grid(50, 50, 10, 100, 4, 10)
# display_grid(grid)
