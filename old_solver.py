# Kakuro Reader

import math
import gurobipy as gp
from gurobipy import quicksum
from gurobipy import GRB

# kakuro = open('kakuro_example.txt', 'r')
kakuro = open('simple.txt', 'r')
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
                # model.addVars(i, j, 9, vtype=GRB.BINARY, name=f'''Val_({i},{j})''')
                # create_binary_var(i,j)
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
                    # model.addConstrs((vars.sum(i_, j, k) * k == left
                    #     for i_ in range(i, u_b)
                    #     for k in range(1, 9)), name='Down_Sum = ' + str(right) + " at " + str(i) + "," + str(j))
                    
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

                    # number of blanks to fill 


                    # model.addConstrs(
                    #     ((vars.sum(i_, j, "*") <= 1)
                    #         for i_ in range(i, u_b)),
                    #         name=f'''ColUniqueness_at_({i},{j})'''
                    # )
                    # for k in range(0,8):
                    #     model.addConstrs(
                    #         (vars.sum(i_, j, k) <= 1
                    #             for i_ in range(i, u_b)),
                    #             name=f'''ColUniqueness_at_({i},{j})'''
                    #     )
                    # model.addConstrs((vars.sum(i_, j, k) <= 1
                    #     for i_ in range(i, u_b)
                    #     for k in range(1, 9)), name='ColUniqueness ' + str(right) + " at " + str(i) + "," + str(j))
                    # pass 
                    # going down
                    # get lower_bound
                    # add constraint from j to lower_bound
                    
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
                    # model.addConstrs((vars.sum(i, j_, k) * k == right
                    #     for j_ in range(j, r_b)
                    #     for k in range(1, 9)), name='Right_Sum = ' + str(right) + " at " + str(i) + "," + str(j))
                    
                    for k in range(0,9):
                        model.addConstr(
                            (quicksum(vars[i, j_,k] for j_ in range(j+1, r_b)) <= 1), 
                            name=f'''RowUniqueness_at_({i},{j})'''
                        )
                    # k = 0
                    # model.addConstrs(
                    #             ((vars.sum(i, j_, k) <= 1)
                    #                 # for k in range(0, 9)),
                    #                 for j_ in range(j, r_b)),
                    #                 name=f'''RowUniqueness_at_({i},{j})'''
                    #         )
                    # for k in range(0,8):
                    #     model.addConstrs(
                    #         (vars.sum(i, j_, k) <= 1
                    #             for j_ in range(j, r_b)),
                    #             name=f'''RowUniqueness_at_({i},{j})'''
                    #     )
                        #     (vars.sum(i, j_, k) <= 1
                        # for j_ in range(j, r_b)))
                    
                        # for k in range(1, 9)), name='RowUniqueness ' + str(right) + " at " + str(i) + "," + str(j))


                    # model.addConstrs((vars.sum(i, j_, k) <= 1
                    #     for j_ in range(j, r_b)
                    #     for k in range(1, 9)), name='RowUniqueness ' + str(right) + " at " + str(i) + "," + str(j))
                    # going right
                    # get right_bound
                    # add constraint from i to right_bound

            #TODO This seems to be optional??
            # we have to fill in a value 
            # elif board[i][j] == " ":
            #     model.addConstr(
            #         (quicksum(vars[i, j,k] for k in range(0, 9) ) == 1), 
            #         name=f'''MissingVal_at_({i},{j})'''
            #     )
                
                        
print_board()

create_binary_vars()

add_summ_constraint()

model.optimize()

model.write('kakuro_2.lp')

status = model.status

print(status)

print('')
print('Solution:')
print('')

# Retrieve optimization result

# solution = model.getAttr(vars)

# print(solution)

for v in model.getVars():
    print(v)
    print(type(v))

# for i in range(board_height):
#     sol = ''
#     for j in range(board_width):
#         for k in range(9):
#             if solution[i, j, k] > 0.5:
#                 sol += str(k+1)
#     print(sol)
                        
# find_right_bound(0,4)
        
    
# def find_right_bound(start):
    
    
    
# print()
# print(board_width)
# print(board_height)