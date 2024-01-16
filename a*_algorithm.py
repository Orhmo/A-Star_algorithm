import turtle
import time
import sys
from collections import deque
import copy

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A* Maze Solving Program")
wn.setup(1300, 700)

class Maze(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

class Green(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)

class Blue(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.speed(0)

class Red(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")  # Circular robot representation
        self.color("red")
        self.penup()
        self.speed(0)

class Yellow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.speed(0)

def setup_maze(grid):
    global start_x, start_y, end_x, end_y
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            character = grid[y][x]
            screen_x = -588 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "+":
                maze.goto(screen_x, screen_y)
                maze.stamp()
                walls.append((screen_x, screen_y))

            if character == " " or character == "e":
                path.append((screen_x, screen_y))

            if character == "e":
                green.goto(screen_x, screen_y)
                end_x, end_y = screen_x, screen_y
                green.stamp()

            if character == "s":
                start_x, start_y = screen_x, screen_y
                red.goto(screen_x, screen_y)

def heuristic(a, b):
    # Euclidean distance heuristic
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def cost(current, next_cell):
    # Cost function for each motion (adjust as needed)
    return 1

def tree_search():
    start_time = time.time()
    frontier.append((start_x, start_y))
    solution.clear()  # Clear the solution for tree search

    while len(frontier) > 0:
        time.sleep(0)
        current = frontier.pop(0)

        if current == (end_x, end_y):
            break

        for next_cell in get_neighbors(current):
            if next_cell not in solution:
                frontier.append(next_cell)
                solution[next_cell] = current  # Store parent-child relationship

    elapsed_time = time.time() - start_time
    print(f"Tree Search - ")
    path_found = trace_path()
    visualize_path(path_found, tree_search=True)

    # Analyze memory consumption
    tree_memory = sys.getsizeof(copy.deepcopy(solution))
    print(f"Memory Consumption (Tree Search): {tree_memory} bytes")

    return path_found, elapsed_time

def search(graph_search=False):
    solution.clear()  # Clear the solution for tree search
    start_time = time.time()
    frontier.append((start_x, start_y))
    g_values = {(start_x, start_y): 0}
    f_values = {(start_x, start_y): heuristic((start_x, start_y), (end_x, end_y))}

    while len(frontier) > 0:
        time.sleep(0)
        current = min(frontier, key=lambda x: f_values.get(x, float('inf')))

        if current == (end_x, end_y):
            break

        frontier.remove(current)

        for next_cell in get_neighbors(current):
            new_g = g_values[current] + cost(current, next_cell)
            if next_cell not in g_values or new_g < g_values[next_cell]:
                g_values[next_cell] = new_g
                f_values[next_cell] = new_g + heuristic(next_cell, (end_x, end_y))
                frontier.append(next_cell)
                solution[next_cell] = current

    elapsed_time = time.time() - start_time
    print(f"{'Graph' if graph_search else 'A*'} Search - ")
    path_found = trace_path()
    visualize_path(path_found, graph_search)


    # Analyze memory consumption
    graph_memory = sys.getsizeof(copy.deepcopy(solution))
    print(f"Memory Consumption (Graph Search): {graph_memory} bytes")

    return path_found, elapsed_time

def get_neighbors(cell):
    x, y = cell
    neighbors = [(x - 24, y), (x, y - 24), (x + 24, y), (x, y + 24)]
    return [neighbor for neighbor in neighbors if neighbor in path]

def trace_path():
    current = (end_x, end_y)
    path_found = []
    while current:
        path_found.append(current)
        current = solution.get(current)

    path_found.reverse()
    return path_found

def visualize_path(path_found, graph_search=False, tree_search=False):
    if tree_search:
        turtle_color = "purple"
        turtle_shape = "circle"  # Use a circle shape for tree search
        turtle_name = "Purple"
    elif graph_search:
        turtle_color = "blue"
        turtle_shape = "square"  # Use a square shape for graph search
        turtle_name = "Blue"
    else:
        turtle_color = "yellow"
        turtle_shape = "circle"  # Use a circle shape for A* search
        turtle_name = "Yellow"

    turtle_instance = turtle.Turtle()
    turtle_instance.shape(turtle_shape)
    turtle_instance.color(turtle_color)
    turtle_instance.penup()
    turtle_instance.speed(0)

    for point in path_found:
        turtle_instance.goto(point)
        turtle_instance.stamp()
        wn.update()  # Manually update the screen during each iteration

    print(f"{turtle_name} Path Visualized")

maze = Maze()
red = Red()
blue = Blue()
green = Green()
yellow = Yellow()

walls = []
path = []
visited = set()
frontier = []
solution = {}

# Define your environment as a binary matrix
grid = [
"+++++++++++++++++++++++++++++++++++++++++++++++++++",
"+               +                                 +",
"+  ++++++++++  +++++++++++++  +++++++  ++++++++++++",
"+s          +                 +               ++  +",
"+  +++++++  +++++++++++++  +++++++++++++++++++++  +",
"+  +     +  +           +  +                 +++  +",
"+  +  +  +  +  +  ++++  +  +  +++++++++++++  +++  +",
"+  +  +  +  +  +  +        +  +  +        +       +",
"+  +  ++++  +  ++++++++++  +  +  ++++  +  +  ++   +",
"+  +     +  +          +   +           +  +  ++  ++",
"+  ++++  +  +++++++ ++++++++  +++++++++++++  ++  ++",
"+     +  +     +              +              ++   +",
"++++  +  ++++++++++ +++++++++++  ++++++++++  +++  +",
"+  +  +                    +     +     +  +  +++  +",
"+  +  ++++  +++++++++++++  +  ++++  +  +  +  ++   +",
"+  +  +     +     +     +  +  +     +     +  ++  ++",
"+  +  +  +++++++  ++++  +  +  +  ++++++++++  ++  ++",
"+                       +  +  +              ++  ++",
"+ ++++++             +  +  +  +  +++        +++  ++",
"+ ++++++ ++++++ +++++++++    ++ ++   ++++++++++  ++",
"+ +    +    +++ +     +++++++++ ++  +++++++    + ++",
"+ ++++ ++++ +++ + +++ +++    ++    ++    ++ ++ + ++",
"+ ++++    +     + +++ +++ ++ ++++++++ ++ ++ ++   ++",
"+      ++ +++++++e+++     ++          ++    +++++++",
"+++++++++++++++++++++++++++++++++++++++++++++++++++",
 ]

setup_maze(grid)

# Run Tree Search
path_tree_search, time_tree_search = tree_search()

# Reset variables for graph search
frontier.clear()
solution.clear()

# Run A* Search with Graph Search
path_graph_search, time_graph_search = search(graph_search=True)

# Print paths and cost
print("\nTree Search Path:")
print(path_tree_search)
print(f"Time Elapsed (Tree Search): {time_tree_search} seconds")

tree_search_cost = sum(cost(solution[parent], parent) for parent in solution)
print(f"Cost (Tree Search): {tree_search_cost}")

print("\nGraph Search Path:")
print(path_graph_search)
print(f"Time Elapsed (Graph Search): {time_graph_search} seconds")

graph_search_cost = sum(cost(solution[parent], parent) for parent in solution)
print(f"Cost (Graph Search): {graph_search_cost}")

# Analyze total memory consumption
total_memory = sys.getsizeof(copy.deepcopy(solution)) + sys.getsizeof(copy.deepcopy(walls)) + sys.getsizeof(copy.deepcopy(path))
print(f"Total Memory Consumption: {total_memory} bytes")




wn.exitonclick()
sys.exit()