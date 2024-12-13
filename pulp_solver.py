# -*- coding: utf-8 -*-
import argparse
from pulp import LpVariable, LpInteger, LpProblem, LpMinimize, LpStatus, lpSum, value
import time

# base_problem = [[0, 0, 0, 0, 2, 0, 0, 0, 0],
#         [0, 0, 0, 3, 7, 0, 0, 0, 6],
#         [0, 0, 0, 0, 0, 5, 2, 1, 0],
#         [6, 0, 0, 0, 0, 1, 5, 0, 0],
#         [8, 0, 0, 0, 0, 0, 0, 2, 1],
#         [0, 0, 2, 0, 0, 9, 0, 7, 0],
#         [0, 0, 8, 5, 0, 0, 3, 0, 0],
#         [4, 0, 6, 8, 0, 0, 0, 0, 0],
#         [7, 1, 0, 0, 0, 4, 0, 0, 0]]

base_problem = [[0, 0, 9, 6, 0, 0, 0, 0, 0],
        [8, 3, 0, 0, 0, 0, 0, 0, 7],
        [1, 2, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [5, 0, 0, 0, 0, 1, 0, 0, 2],
        [0, 7, 1, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 4, 9, 8, 0, 0],
        [9, 0, 2, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 3, 0, 0, 4]]

def solve(inp):
    n = 9
    b = 3
    digits = [str(d + 1) for d in range(n)]
    # print(digits)
    values = rows = columns = digits
    answers = []

    choices = LpVariable.dicts("Choice", (values, rows, columns), 0, 1, LpInteger)
    boxes = [[(rows[b * i + k], columns[b * j + l]) for k in range(b) for l in range(b)] for j in range(b) for i in range(b)]
    # print(boxes)

    # problem definition
    problem = LpProblem("Solving Sudoku", LpMinimize)  # MinimizeでもMaximizeでもOK
    problem += 0, "Arbitrary Objective Function"

    # add constraints
    for r in rows:
        for c in columns:
            problem += lpSum([choices[v][r][c] for v in values]) == 1, ""

    for v in values:
        for r in rows:
            problem += lpSum([choices[v][r][c] for c in columns]) == 1, ""

        for c in columns:
            problem += lpSum([choices[v][r][c] for r in rows]) == 1, ""

        for b in boxes:
            problem += lpSum([choices[v][r][c] for (r, c) in b]) == 1, ""

    flat_inp = ''.join([str(cell) for row in inp for cell in row])
    # print(flat_inp)
    for i in range(n**2):
        val = flat_inp[i]
        if val != '0':
            problem += choices[str(val)][str(int(i/n) + 1)][str(i % n + 1)] == 1, ""

    start_time = time.time()
    while True:
        # use CBC as solver
        problem.solve()
        if LpStatus[problem.status] == "Optimal":
            answers.append(''.join([v for r in rows for c in columns for v in values if value(choices[v][r][c]) == 1]))
            # add solution to problem as a constraint
            problem += lpSum(
                [choices[v][r][c] for v in values for r in rows for c in columns if value(choices[v][r][c]) == 1]
            ) <= 80
        else:
            break
    elapsed_time = time.time() - start_time

    if answers:
        # desplay answer
        for i in range(9):        
            [print([int(answers[0][i * 9 + j]) for j in range(9)])]
        return [[int(answers[0][i * 9 + j]) for j in range(9)] for i in range(9)], elapsed_time


if __name__ == '__main__':
    solve(base_problem)
