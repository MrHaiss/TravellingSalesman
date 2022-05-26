import turtle
import random
import tkinter as tk
from tkinter import messagebox
from random import choice
from itertools import permutations
import math

# Globals
NODE_COLOUR_RANGE = ["red", "blue", "green", "orange", "purple", "violet", "skyblue", "pink", "cyan"]
WIDTH = 500
HEIGHT = 500
NODES = []
NODE_SIZE = 15
BEST_DISTANCE = 999999999
BEST_PATHWAY = []
BEST_LINE_DRAWER = None
DISPLAY_VISUALS = False
DISPLAY_VISUALS_CBOX = None


# On Clicks/Callbacks
def start_button_click():
    global DISPLAY_VISUALS

    user_input_no_nodes = no_nodes.get()
    user_input_node_padding = node_padding.get()
    DISPLAY_VISUALS = DISPLAY_VISUALS_CBOX.get()

    if not user_input_no_nodes.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid number (integer) for the number of nodes.")
    elif not user_input_node_padding.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid number (integer) for the node padding.")
    elif 15 < int(user_input_node_padding) or int(user_input_node_padding) < 2:
        messagebox.showerror("Invalid Input", "Please enter a number between 2 and 10 for the node padding.")
    else:
        setup_turtle_nodes(abs(int(user_input_no_nodes)), int(user_input_node_padding))


# Turtle Calls
def setup_turtle_nodes(number_nodes, node_padding_val):
    win.destroy()
    turtle.screensize(WIDTH, HEIGHT)
    node_drawer = turtle.Turtle()
    node_drawer.speed(0)
    node_drawer.hideturtle()

    draw_boundary_x = int(WIDTH * 0.65)
    draw_boundary_y = int(HEIGHT * 0.65)

    for i in range(number_nodes):
        # Draw the nodes
        node_drawer.penup()
        # Check we aren't too close to another node
        check_node_spacing = True
        check_node_spacing_loop = 0
        while check_node_spacing:
            rand_x = random.randrange(-draw_boundary_x, draw_boundary_x)
            rand_y = random.randrange(-draw_boundary_y, draw_boundary_y)
            if len(NODES) == 0:
                break
            else:
                inner_check_node_spacing = True
                for n in NODES:
                    distance_x = n[1] - rand_x
                    distance_y = n[2] - rand_y
                    distance_padding = NODE_SIZE * node_padding_val

                    if abs(distance_x) <= distance_padding and abs(distance_y) <= distance_padding:
                        check_node_spacing_loop += 1
                        if check_node_spacing_loop >= 100:
                            messagebox.showwarning("Node Generator Warning",
                                                   "Either your node count or padding value is too high, program will "
                                                   "proceed with nodes generated so far.")
                            return
                        else:
                            inner_check_node_spacing = True
                            break
                    else:
                        inner_check_node_spacing = False

                check_node_spacing = inner_check_node_spacing

        node_drawer.setpos((rand_x, rand_y))
        node_drawer.pendown()
        node_drawer.color(choice(NODE_COLOUR_RANGE))
        node_drawer.begin_fill()
        node_drawer.circle(NODE_SIZE)
        node_drawer.end_fill()

        # Capture the positions
        NODES.append(("node-" + str(i), rand_x, rand_y))

    percentage_label = tk.Label(text="Progress: 0.00%")
    percentage_label.pack(pady=10)

    best_distance_label = tk.Label(text="Best Distance Calculated: n/a")
    best_distance_label.pack(pady=10)

    total_combinations = math.factorial(len(NODES))
    total_combo_label = tk.Label(text="Total Combinations: {0}".format(total_combinations))
    total_combo_label.pack(pady=10)

    draw_salesman_lines(percentage_label, best_distance_label, total_combinations)


def draw_salesman_lines(pct_l, bd_l, total_combo):
    global BEST_DISTANCE
    global BEST_PATHWAY
    global BEST_LINE_DRAWER

    counter = 0

    for p in permutations(NODES):
        if DISPLAY_VISUALS:
            line_drawer = turtle.Turtle()
            line_drawer.speed(0)
            line_drawer.color("black")
            line_drawer.width(2)
            line_drawer.hideturtle()
            line_drawer.penup()

        counter += 1
        progress_pct = (counter / total_combo) * 100
        progress_pct_frmt = "{:.2f}".format(progress_pct)
        pct_l.config(text="Progress: {0}%".format(progress_pct_frmt))

        if DISPLAY_VISUALS:
            for i in range(len(p) - 1):
                start_x = p[i][1]
                start_y = p[i][2] + NODE_SIZE
                target_x = p[i + 1][1]
                target_y = p[i + 1][2] + NODE_SIZE
                line_drawer.setpos((start_x, start_y))
                line_drawer.pendown()
                line_drawer.goto((target_x, target_y))

        distance = calc_path_distance(p)
        if distance <= BEST_DISTANCE:
            BEST_DISTANCE = distance
            BEST_PATHWAY = p
            bd_l.config(text="Best Distance Calculated: {0}".format(math.floor(distance)))
            if BEST_LINE_DRAWER is not None:
                BEST_LINE_DRAWER.clear()
                if DISPLAY_VISUALS:
                    BEST_LINE_DRAWER = line_drawer
            elif DISPLAY_VISUALS:
                BEST_LINE_DRAWER = line_drawer
        elif DISPLAY_VISUALS:
            line_drawer.clear()

    if not DISPLAY_VISUALS:
        best_line_drawer = turtle.Turtle()
        best_line_drawer.speed(1)
        best_line_drawer.color("black")
        best_line_drawer.width(2)
        best_line_drawer.hideturtle()
        best_line_drawer.penup()

        for i in range(len(BEST_PATHWAY) - 1):
            start_x = BEST_PATHWAY[i][1]
            start_y = BEST_PATHWAY[i][2] + NODE_SIZE
            target_x = BEST_PATHWAY[i + 1][1]
            target_y = BEST_PATHWAY[i + 1][2] + NODE_SIZE
            best_line_drawer.setpos((start_x, start_y))
            best_line_drawer.pendown()
            best_line_drawer.goto((target_x, target_y))


def calc_path_distance(node_points):
    total_distance = 0

    for i in range(len(node_points) - 1):
        first_pos = (node_points[i][1], node_points[i][2])
        next_pos = (node_points[i + 1][1], node_points[i + 1][2])
        d = math.dist(first_pos, next_pos)
        total_distance += d

    return total_distance


# Initial UI setup
win = tk.Tk()
win.title("Travelling Salesman Setup")
win.resizable(False, False)
win.geometry("{0}x{1}".format(WIDTH, int(HEIGHT / 1.5)))

header = tk.Label(text="Setup Options", font=("Courier", 30, "bold"))
header.pack()

no_nodes_label = tk.Label(text="Please enter the number of nodes:")
no_nodes_label.pack(pady=10)
no_nodes = tk.Entry()
no_nodes.pack()

node_padding_label = tk.Label(text="Please enter the padding amount for the nodes (between 2 and 15):")
node_padding_label.pack(pady=10)
node_padding = tk.Entry()
node_padding.pack()

display_visuals_label = tk.Label(text="Display in-progress visuals (note, this will be significantly slower):")
display_visuals_label.pack(pady=10)
DISPLAY_VISUALS_CBOX = tk.IntVar()
display_visuals_cbox = tk.Checkbutton(variable=DISPLAY_VISUALS_CBOX)
display_visuals_cbox.pack()

start_button = tk.Button(text="Start", command=start_button_click)
start_button.pack(pady=20)

win.mainloop()
