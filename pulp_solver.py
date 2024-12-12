# -*- coding: utf-8 -*-
import argparse
from pulp import LpVariable, LpInteger, LpProblem, LpMinimize, LpStatus, lpSum, value

# base = [[0, 0, 0, 0, 2, 0, 0, 0, 0],
#         [0, 0, 0, 3, 7, 0, 0, 0, 6],
#         [0, 0, 0, 0, 0, 5, 2, 1, 0],
#         [6, 0, 0, 0, 0, 1, 5, 0, 0],
#         [8, 0, 0, 0, 0, 0, 0, 2, 1],
#         [0, 0, 2, 0, 0, 9, 0, 7, 0],
#         [0, 0, 8, 5, 0, 0, 3, 0, 0],
#         [4, 0, 6, 8, 0, 0, 0, 0, 0],
#         [7, 1, 0, 0, 0, 4, 0, 0, 0]]

base = [[0, 0, 9, 6, 0, 0, 0, 0, 0],
        [8, 3, 0, 0, 0, 0, 0, 0, 7],
        [1, 2, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 0],
        [5, 0, 0, 0, 0, 1, 0, 0, 2],
        [0, 7, 1, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 4, 9, 8, 0, 0],
        [9, 0, 2, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 3, 0, 0, 4]]

def main(inp):
    n = 9
    b = 3
    digits = [str(d + 1) for d in range(n)]
    print(digits)
    values = rows = columns = digits
    answers = []

    choices = LpVariable.dicts("Choice", (values, rows, columns), 0, 1, LpInteger)
    boxes = [[(rows[b * i + k], columns[b * j + l]) for k in range(b) for l in range(b)] for j in range(b) for i in range(b)]
    print(boxes)

    # 問題定義
    problem = LpProblem("Solving Sudoku", LpMinimize)  # MinimizeでもMaximizeでもOK
    problem += 0, "Arbitrary Objective Function"

    # 制約追加
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
    print(flat_inp)
    for i in range(n**2):
        val = flat_inp[i]
        if val != '0':
            problem += choices[str(val)][str(int(i/n) + 1)][str(i % n + 1)] == 1, ""

    while True:
        # cbcソルバー利用
        problem.solve()
        if LpStatus[problem.status] == "Optimal":
            answers.append(''.join([v for r in rows for c in columns for v in values if value(choices[v][r][c]) == 1]))
            # 見つけた解を制約として追加
            problem += lpSum(
                [choices[v][r][c] for v in values for r in rows for c in columns if value(choices[v][r][c]) == 1]
            ) <= 80
        else:
            break

    if answers:
        # 最初の解だけ表示
        print(answers[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('inp', type=str)
    args = parser.parse_args()
    # main(args.inp)
    main(base)
