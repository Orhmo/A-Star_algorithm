import turtle
import sys
import copy
import time
from collections import deque

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("G-DFS Algorithm Maze Solving Program")
wn.setup(1300, 700)

start_x = 0
start_y = 0
end_x = 0
end_y = 0

move_costs = {(-24, 0): 1, (24, 0): 1, (0, -24): 1, (0, 24): 2}  # Define move costs

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
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)

class Red(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.setheading(270)
        self.penup()
        self.speed(0)

class Yellow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.speed(0)

class Purple(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("purple")
        self.penup()
        self.speed(0)

class Pink(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("pink")
        self.penup()
        self.speed(0)

grid1 = [
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
            if character == " ":
                path.append((screen_x, screen_y))
            if character == "e":
                end_x, end_y = screen_x, screen_y
                yellow.goto(screen_x, screen_y)
                yellow.stamp()
                path.append((screen_x, screen_y))
            elif character == "s":
                start_x, start_y = screen_x, screen_y
                red.goto(screen_x, screen_y)  
                red.stamp()

def graph_search(x, y):
    start_time = time.time()  # Record the start time
    frontier.append((x, y))
    solution[x, y] = x, y
    explored = set()

    while len(frontier) > 0:
        time.sleep(0)
        x, y = frontier.pop()

        if (x, y) in explored:
            continue

        explored.add((x, y))

        # Check and add adjacent cells only if not explored
        for dx, dy in [(-24, 0), (0, -24), (24, 0), (0, 24)]:
            neighbor = (x + dx, y + dy)

            if neighbor in path and neighbor not in explored and neighbor not in frontier:
                solution[neighbor] = x, y
                blue.goto(neighbor)
                blue.stamp()
                frontier.append(neighbor)

        green.goto(x, y)
        green.stamp()
        if (x, y) == (end_x, end_y):
            yellow.stamp()
            break  # Stop the search if the goal is reached
        if (x, y) == (start_x, start_y):
            red.goto(x, y)  # Make sure to move to the current position before stamping

    end_time = time.time()  # Record the end time
    time_taken = end_time - start_time  # Calculate the time taken
    print(f"Time Taken: {time_taken} seconds")

    # Calculate and print the storage used
    storage = sys.getsizeof(copy.deepcopy(solution))
    print(f"Storage Used: {storage} bytes")


def back_route(x, y):
    yellow = Yellow()  # Use the modified Purple class
    yellow.penup()
    yellow.speed(0)

    yellow.goto(x, y)
    yellow.stamp()

    reverse_path = []
    total_cost = 0

    while (x, y) != (start_x, start_y):
        reverse_path.append((x, y))
        yellow.goto(solution[x, y])
        yellow.stamp()
        total_cost += move_costs[(x - solution[x, y][0], y - solution[x, y][1])]
        x, y = solution[x, y]

    reverse_path.reverse()

    purple = Purple()
    purple.penup()
    purple.speed(0)

    purple_path = []  # Variable to store the coordinates of the purple path
    for pos in reverse_path:
        purple.goto(pos)
        purple.stamp()
        purple_path.append(pos)

    print("Path:", purple_path)
    print("Total Cost:", total_cost)

maze = Maze()
red = Red()
blue = Blue()
green = Green()
yellow = Yellow()
purple = Purple()
walls = []
path = []
visited = []
frontier = deque()
solution = {}

setup_maze(grid1)
graph_search(start_x, start_y)
back_route(end_x, end_y)

wn.exitonclick()
