import turtle
import time
import sys
import copy
import heapq

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A* Algorithm Maze Solving Program")
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
        self.shape("circle")
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
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def cost(current, next_cell):
    return 1

def tree_search():
    start_time = time.time()
    # Using a priority queue with heapq
    tree_frontier.append((0, (start_x, start_y)))  
    tree_solution = {}

    tree_explore_turtle = turtle.Turtle()
    tree_explore_turtle.shape("circle")
    tree_explore_turtle.color("lightblue")
    tree_explore_turtle.penup()
    tree_explore_turtle.speed(0)

    while tree_frontier:
        time.sleep(0)
        current = tree_frontier.pop(0)[1]

        if current == (end_x, end_y):
            break

        for next_cell in get_neighbors(current):
            if next_cell not in tree_solution:
                g_value = cost(current, next_cell) + cost((0, 0), current)
                heapq.heappush(tree_frontier, (g_value, next_cell))
                tree_solution[next_cell] = current

                tree_explore_turtle.goto(next_cell)
                tree_explore_turtle.stamp()
                wn.update()

    tree_path_turtle = turtle.Turtle()
    tree_path_turtle.shape("circle")
    tree_path_turtle.color("purple")
    tree_path_turtle.penup()
    tree_path_turtle.speed(0)

    elapsed_time = time.time() - start_time
    print(f"A* Tree Search - ")
    path_found = trace_path(tree_solution)

    for point in path_found:
        tree_path_turtle.goto(point)
        tree_path_turtle.stamp()
        wn.update()

    tree_explore_turtle.clear()
    tree_path_turtle.clear()

    tree_search_cost = sum(cost(tree_solution[parent], parent) for parent in tree_solution)
    print(f"Cost (Tree Search): {tree_search_cost}")

    tree_memory = sys.getsizeof(copy.deepcopy(tree_solution))
    print(f"Memory Consumption (A* Tree Search): {tree_memory} bytes")

    return path_found, elapsed_time

def graph_search():
    start_time = time.time()
    graph_solution = {}
    # Using a priority queue with heapq
    heapq.heappush(graph_frontier, (0, (start_x, start_y)))  
    g_values = {(start_x, start_y): 0}

    graph_explore_turtle = turtle.Turtle()
    graph_explore_turtle.shape("square")
    graph_explore_turtle.color("lightgreen")
    graph_explore_turtle.penup()
    graph_explore_turtle.speed(0)

    while graph_frontier:
        time.sleep(0)
        current = heapq.heappop(graph_frontier)[1]

        if current == (end_x, end_y):
            break

        for next_cell in get_neighbors(current):
            new_g = g_values[current] + cost(current, next_cell)
            if next_cell not in g_values or new_g < g_values[next_cell]:
                g_values[next_cell] = new_g
                f_value = new_g + heuristic(next_cell, (end_x, end_y))
                heapq.heappush(graph_frontier, (f_value, next_cell))
                graph_solution[next_cell] = current

                graph_explore_turtle.goto(next_cell)
                graph_explore_turtle.stamp()
                wn.update()

    graph_path_turtle = turtle.Turtle()
    graph_path_turtle.shape("square")
    graph_path_turtle.color("blue")
    graph_path_turtle.penup()
    graph_path_turtle.speed(0)

    elapsed_time = time.time() - start_time
    print(f"A* Graph Search - ")
    path_found = trace_path(graph_solution)

    for point in path_found:
        graph_path_turtle.goto(point)
        graph_path_turtle.stamp()
        wn.update()

    graph_explore_turtle.clear()

    graph_search_cost = sum(cost(graph_solution[parent], parent) for parent in graph_solution)
    print(f"Cost (Graph Search): {graph_search_cost}")

    graph_memory = sys.getsizeof(copy.deepcopy(graph_solution))
    print(f"Memory Consumption (A* Graph Search): {graph_memory} bytes")

    return path_found, elapsed_time

def get_neighbors(cell):
    x, y = cell
    neighbors = [(x - 24, y), (x, y - 24), (x + 24, y), (x, y + 24)]
    return [neighbor for neighbor in neighbors if neighbor in path]

def trace_path(solution):
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
        turtle_shape = "circle"
        turtle_name = "Purple"
    elif graph_search:
        turtle_color = "blue"
        turtle_shape = "square"
        turtle_name = "Blue"
    else:
        turtle_color = "yellow"
        turtle_shape = "circle"
        turtle_name = "Yellow"

    turtle_instance = turtle.Turtle()
    turtle_instance.shape(turtle_shape)
    turtle_instance.color(turtle_color)
    turtle_instance.penup()
    turtle_instance.speed(0)

    for point in path_found:
        turtle_instance.goto(point)
        turtle_instance.stamp()
        wn.update()

    print(f"{turtle_name} Path Visualized")

maze = Maze()
red = Red()
blue = Blue()
green = Green()
yellow = Yellow()

walls = []
path = []
tree_frontier = []
graph_frontier = []
solution = {}

# Defining the environment as a binary matrix
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
    "+                       +  +                 ++  ++",
    "+ ++++++             +  +  +  +  +++        +++  ++",
    "+ ++++++ ++++++ +++++++++    ++ ++   ++++++++++  ++",
    "+ +    +    +++ +     +++++++++ ++  +++++++    + ++",
    "+ ++++ ++++ +++ + +++ +++    ++    ++    ++ ++ + ++",
    "+ ++++    +     + +++ +++ ++ +++ ++++ ++ ++ ++   ++",
    "+      ++ +++++++e+++     ++          ++    +++++++",
    "+++++++++++++++++++++++++++++++++++++++++++++++++++",
]

setup_maze(grid)

# Run Tree Search
path_tree_search, time_tree_search = tree_search()

tree_frontier.clear()
solution.clear()

# Run A* Search with Graph Search
path_graph_search, time_graph_search = graph_search()

print("\nTree Search Path:")
print(path_tree_search)
print(f"Time Elapsed (Tree Search): {time_tree_search} seconds")

print("\nGraph Search Path:")
print(path_graph_search)
print(f"Time Elapsed (Graph Search): {time_graph_search} seconds")

total_memory = sys.getsizeof(copy.deepcopy(solution)) + sys.getsizeof(copy.deepcopy(walls)) + sys.getsizeof(copy.deepcopy(path))
print(f"Total Memory Consumption: {total_memory} bytes")

wn.exitonclick()
sys.exit()
