# Kakuro Reader

# quantitative
import gurobipy as gp
from gurobipy import quicksum
from gurobipy import GRB
import re

# display 
# import pygame
from PIL import Image, ImageDraw, ImageFont
from numpy import size

kakuro = open('expert.txt', 'r')
# kakuro = open('simple.txt', 'r')

lines = kakuro.readlines()

board_width = 0
board_height = 0

board = []

for line in lines:
    line = line.replace("\n", "")
    line = line.split(".")
    board_width = len(line)
    board_height += 1
    board.append(line)
    
def print_board():
    for row in board:
        print(row)
        
def find_right_bound(start_i, start_j):
    for j in range(start_j+1, board_width):
        if "," in board[start_i][j]:
            return j
    return board_width

def find_lower_bound(start_i, start_j):
    print(start_i)
    print(start_j)
    print(board[start_i][start_j])
    for i in range(start_i + 1, board_height):
        if "," in board[i][start_j]:
            return i
    return board_height

model = gp.Model('kakuro')

tiles_to_fill = set([])

vars = 0

def create_binary_vars():
    for i in range(board_height):
        for j in range(board_width):
            if board[i][j] == " ":
                tiles_to_fill.add((i,j))
    global vars 
    vars = model.addVars([(i, j, k) for i in range(board_height) 
                                    for j in range(board_width) 
                                    for k in range(9) 
                                    if (i,j) in tiles_to_fill], 
            vtype=GRB.BINARY, name='G')
                
def add_summ_constraint():
    for i in range(board_height):
        for j in range(board_width):

            # we have a row and/or column clue 
            if board[i][j] != "0,0" and board[i][j] != " ":
                left, right = board[i][j].split(",")
                left = int(left)
                right = int(right)
                
                # process left
                # going down
                if left != 0:
                    u_b = find_lower_bound(i,j)
                    
                    # vertical sum must equal number in left 
                    model.addConstr(
                        (quicksum(vars[i_, j,k]*(k+1) for i_ in range(i+1, u_b) for k in range(0,9)) == left), 
                        name=f'''Vertical_Sum_at_({i},{j})'''
                    )

                    # a number can only be used once 
                    for k in range(0,9):
                        model.addConstr(
                            (quicksum(vars[i_, j,k] for i_ in range(i+1, u_b)) <= 1), 
                            name=f'''ColUniqueness_at_({i},{j})'''
                        )
                    
                # process right
                # going right 
                if right != 0:
                    r_b = find_right_bound(i,j)
                    # model.addConstrs((vars.sum('*', j, k) * k = right
                    # for k in range(0,9):
                    model.addConstr(
                        (quicksum(vars[i, j_,k]*(k+1) for j_ in range(j+1, r_b) for k in range(0,9)) == right), 
                        name=f'''RightSum_at_({i},{j})'''
                    )

                    for k in range(0,9):
                        model.addConstr(
                            (quicksum(vars[i, j_,k] for j_ in range(j+1, r_b)) <= 1), 
                            name=f'''RowUniqueness_at_({i},{j})'''
                        )

            #TODO This seems to be optional??
            # we have to fill in a value 
            # use less than or equal to in order to final illegal solution 
            elif board[i][j] == " ":
                model.addConstr(
                    (quicksum(vars[i, j,k] for k in range(0, 9) ) == 1), 
                    name=f'''MissingVal_at_({i},{j})'''
                )

print_board()

create_binary_vars()

add_summ_constraint()

model.optimize()

model.write('kakuro_expert.lp')

status = model.status

print(status)

print('')
print('Solution:')
print('')

# Retrieve optimization result

# solution = model.getAttr(vars)

# print(solution)

sol_dict = {}

for v in model.getVars():
    # solution
    if int(v.X) == 1:
        variables = re.findall('\[(.*?)\]', v.VarName)[0]
        i,j,val = variables.split(",")
        sol_dict[(i,j)] = int(val)+1

def display_solution():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (211, 211, 211)
    BLUEVIOLET = (138,43,226)
    # font = ImageFont.truetype("unic", 2)
    font = ImageFont.load_default()
    block_size = 50
    WINDOW_HEIGHT = board_height*block_size
    WINDOW_WIDTH = board_width*block_size

    img = Image.new("RGB", (WINDOW_WIDTH, WINDOW_HEIGHT), color=WHITE)

    draw = ImageDraw.Draw(img)

    # draw out clues 
    for i in range(board_height):
        for j in range(board_width):
            # we have a row and/or column clue 
            if board[i][j] != "0,0" and board[i][j] != " ":
                left, right = board[i][j].split(",")
                left = int(left)
                right = int(right)

                # shade gray background 
                draw.rectangle([(j*block_size, i*block_size),((j+1)*block_size, (i+1)*block_size)],fill=GRAY)
                # draw diagonal line 
                draw.line([(j*block_size, i*block_size),((j+1)*block_size, (i+1)*block_size)], fill=BLACK)

                if left != 0:
                    # add left clue 
                    draw.text(((j+0.33)*block_size, (i+0.66)*block_size), str(left), fill=BLACK, font=font)

                if right != 0:
                    # add right clue 
                    draw.text(((j+0.66)*block_size, (i+0.33)*block_size), str(right), fill=BLACK, font=font)

            # no clues provided, gray square 
            elif board[i][j] == "0,0":
                # shade gray background 
                draw.rectangle([(j*block_size, i*block_size),((j+1)*block_size, (i+1)*block_size)],fill=GRAY)
                # draw diagonal line 
                draw.line([(j*block_size, i*block_size),((j+1)*block_size, (i+1)*block_size)], fill=BLACK)
    
    # draw out solutions
    for sol_location in sol_dict:
        i = int(sol_location[0])
        j = int(sol_location[1])
        draw.text(((j+0.5)*block_size, (i+0.5)*block_size), str(sol_dict[sol_location]), fill=BLUEVIOLET, font=font)


    # draw out the grid 
    for i in range(board_height):
        # horizontal lines
        draw.line([(0,i*block_size),(board_width*block_size,i*block_size)], fill=BLACK)
    for j in range(board_width):
        # vertical lines 
        draw.line([(j*block_size, 0),(j*block_size, board_height*block_size)], fill=BLACK)


    img.show()

display_solution()

# print(sol_dict)
