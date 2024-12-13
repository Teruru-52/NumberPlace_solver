target_num = 1 # 生成する数独の数

import random
import copy
import math
import matplotlib.pyplot as plt
import datetime
import os

os.makedirs("./problem/", exist_ok=True)
os.makedirs("./hint/", exist_ok=True)
os.makedirs("./answer/", exist_ok=True)

base_problem = [[2, 3, 4, 1, 5, 9, 7, 8, 6],
        [7, 5, 6, 4, 8, 3, 1, 2, 9], 
        [8, 9, 1, 7, 2, 6, 4, 5, 3], 
        [4, 2, 3, 8, 6, 7, 5, 9, 1], 
        [5, 6, 7, 2, 9, 1, 8, 3, 4],
        [1, 8, 9, 5, 3, 4, 2, 6, 7],  
        [6, 4, 5, 3, 1, 2, 9, 7, 8], 
        [9, 7, 8, 6, 4, 5, 3, 1, 2], 
        [3, 1, 2, 9, 7, 8, 6, 4, 5]]

hint = 0
hint_mat = [[0] * 9 for i in range(9)]

def mix_mat(mat):
    ran = random.randint(0,5)
    num1 = 3*(ran//2) + 1
    num2 = 3*(ran//2) + 2*(ran%2)
    for i in range(9):
        tmp = mat[i][num1]
        mat[i][num1] = mat[i][num2]
        mat[i][num2] = tmp
    ran = random.randint(0,5)
    num1 = 3*(ran//2) + 1
    num2 = 3*(ran//2) + 2*(ran%2)
    for i in range(9):
        tmp = mat[num1][i]
        mat[num1][i] = mat[num2][i]
        mat[num2][i] = tmp
    num1 = random.randint(1,9)
    ran = random.randint(0,7)
    num2 = (num1+ran)%9 + 1
    for i in range(9):
        for j in range(9):
            if mat[i][j] == num2:
                mat[i][j] = num1
            elif mat[i][j] == num1:
                mat[i][j] = num2
    return mat

def check(x,y,mat,check_mat):
    global hint,hint_mat
    hint_mat[x][y] = hint
    hint += 1
    for i in range(9):
        check_mat[x][y][i] = 0
    for i in range(9):
        check_mat[x][i][mat[x][y]-1] = 0
    for i in range(9):
        check_mat[i][y][mat[x][y]-1] = 0
    for i in range(3*(x//3), 3 + 3*(x//3)):
        for j in range(3*(y//3), 3 + 3*(y//3)):
            check_mat[i][j][mat[x][y]-1] = 0

def final_check(mat):
    flag = 1
    for i in range(9):
        tmp_mat = [0]*10
        for j in range(9):
            tmp_mat[mat[i][j]] += 1
        for j in range(1,10):
            if tmp_mat[j] != 1:
                flag = 0
    for i in range(9):
        tmp_mat = [0]*10
        for j in range(9):
            tmp_mat[mat[j][i]] += 1
        for j in range(1,10):
            if tmp_mat[j] != 1:
                flag = 0
    for i in range(3):
        for j in range(3):
            tmp_mat = [0]*10
            for k in range(i*3, i*3+3):
                for l in range(j*3, j*3+3):
                    tmp_mat[mat[k][l]] += 1
            for k in range(1,10):
                if tmp_mat[k] != 1:
                    flag = 0
    if flag == 1:
        return True
    if flag == 0:
        return False

def make(mat):
    global hint,hint_mat
    check_mat = [[[1,2,3,4,5,6,7,8,9] for i in range(9)] for j in range(9)]
    hint_mat = [[0] * 9 for i in range(9)]
    first_num = 0
    for i in range(9):
        for j in range(9):
            if mat[i][j] != 0:
                first_num += 1
                hint = 0
                check(i,j,mat,check_mat)

    level = 0
    sum_num = 0
    for i in range(9):
        for j in range(9):
            tmp = 0
            for k in range(9):
                if check_mat[i][j][k] != 0:
                    tmp += 1
            if mat[i][j] != 0:
                tmp = 0
            level += max(0, (tmp**0.5)-1)

    level = int(((level-40)//2) + 1)

    hint = 1
    while True:
        flag = 1
        for i in range(9):
            tmp_mat = [0]*9
            for j in range(9):
                for k in range(9):
                    if check_mat[i][j][k] != 0:
                        tmp_mat[k] += 1
            for k in range(9):
                if tmp_mat[k] == 1:
                    for j in range(9):
                        if check_mat[i][j][k] != 0:
                            mat[i][j] = k+1
                            check(i,j,mat,check_mat)
                            flag = 0
        for i in range(9):
            tmp_mat = [0]*9
            for j in range(9):
                for k in range(9):
                    if check_mat[j][i][k] != 0:
                        tmp_mat[k] += 1
            for k in range(9):
                if tmp_mat[k] == 1:
                    for j in range(9):
                        if check_mat[j][i][k] != 0:
                            mat[j][i] = k+1
                            check(j,i,mat,check_mat)
                            flag = 0
        for i in range(3):
            for j in range(3):
                tmp_mat = [0]*9
                for k in range(i*3, i*3+3):
                    for l in range(j*3, j*3+3):
                        for m in range(9):
                            if check_mat[k][l][m] != 0:
                                tmp_mat[m] += 1
                for m in range(9):
                    if tmp_mat[m] == 1:
                        for k in range(i*3, i*3+3):
                            for l in range(j*3, j*3+3):
                                if check_mat[k][l][m] != 0:
                                    mat[k][l] = m+1
                                    check(k,l,mat,check_mat)
                                    flag = 0
        for i in range(9):
            for j in range(9):
                if mat[i][j] == 0:
                    tmp = 0
                    num = 0
                    for k in range(9):
                        if check_mat[i][j][k] != 0:
                            tmp += 1
                            num = k+1
                    if tmp == 1:
                        flag = 0
                        mat[i][j] = num
                        check(i,j,mat,check_mat)
        if flag == 1:
            break
    return final_check(mat),level,first_num,mat

def get_problem(base_problem, level=1):
    ver = 1
    dt_now = datetime.datetime.now()
    T = str(dt_now.strftime('_%Y_%m_%d_%H'))
    while True:
        if ver > target_num:
            break
        for j in range(10):
            base_problem = mix_mat(base_problem)
        problem = [[0] * 9 for i in range(9)]
        problem = copy.deepcopy(base_problem)
        while True:
            num1 = random.randint(0,8)
            FLAG = 1
            for k in range(9):
                num2 = random.randint(0,8)
                for l in range(9):
                    if problem[(k+num1)%9][(l+num2)%9] != 0:
                        problem[(k+num1)%9][(l+num2)%9] = 0
                        tmp_problem = copy.deepcopy(problem)
                        ToF,LEVEL,num,ans = make(tmp_problem)
                        if ToF == True:
                            FLAG = 0
                            problem[(k+num1)%9][(l+num2)%9] = 0
                            break
                        else:
                            problem[(k+num1)%9][(l+num2)%9] = base_problem[(k+num1)%9][(l+num2)%9]
            if FLAG == 1:
                break

        tmp_problem = copy.deepcopy(problem)
        ToF,LEVEL,num,ans = make(tmp_problem)

        target = level
        if LEVEL >= target:
            print("----------------------------")
            print("Level: ",LEVEL)
            print("Initial Number:",num)
            print()
            print("【Problem】")
            [print(*problem[i]) for i in range(len(problem))]
            print()
            print("【Answer】")
            [print(*base_problem[i]) for i in range(len(base_problem))]

            LEVEL = int(LEVEL)

            fig = plt.figure(figsize=(18, 15), dpi=50)
            ax1 = fig.add_subplot(111)

            ax1.set_xlim(-460,460)
            ax1.set_ylim(-600,600)
            ax1.set_aspect('equal')
            plt.axis('off')

            for i in range(10):
                ax1.plot([-450, 450], [-450+i*100, -450+i*100], color='black')
                ax1.plot([-450+i*100, -450+i*100], [-450, 450], color='black')
            for i in range(4):
                ax1.plot([-450, 450], [-450+i*300, -450+i*300], color='black', linewidth = 3.0)
                ax1.plot([-450+i*300, -450+i*300], [-450, 450], color='black', linewidth = 3.0)
            for i in range(9):
                for j in range(9):
                    if problem[i][j] != 0:
                        ax1.text(-400+j*100,400-i*100,problem[i][j],fontsize=50,horizontalalignment='center',verticalalignment='center')
            ax1.text(0,500,"LEVEL "+"☆"*LEVEL,fontsize=40,horizontalalignment='center',verticalalignment='center')
            ax1.text(0,-500,"problem_Lv" + str(LEVEL) + "_ver" + str(ver) + T,fontsize=30,horizontalalignment='center',verticalalignment='center')

            # NAME = "./problem/problem_Lv" + str(LEVEL) + "_ver" + str(ver) + T + ".png"
            #plt.show()
            # plt.savefig(NAME)

            fig = plt.figure(figsize=(18, 15), dpi=50)
            ax1 = fig.add_subplot(111)

            ax1.set_xlim(-460,460)
            ax1.set_ylim(-600,600)
            ax1.set_aspect('equal')
            plt.axis('off')

            for i in range(10):
                ax1.plot([-450, 450], [-450+i*100, -450+i*100], color='black')
                ax1.plot([-450+i*100, -450+i*100], [-450, 450], color='black')
            for i in range(4):
                ax1.plot([-450, 450], [-450+i*300, -450+i*300], color='black', linewidth = 3.0)
                ax1.plot([-450+i*300, -450+i*300], [-450, 450], color='black', linewidth = 3.0)
            for i in range(9):
                for j in range(9):
                    if problem[i][j] != 0:
                        ax1.text(-400+j*100,400-i*100,problem[i][j],fontsize=50,horizontalalignment='center',verticalalignment='center')
                    else:
                        ax1.text(-430+j*100,430-i*100,hint_mat[i][j],fontsize=20,horizontalalignment='center',verticalalignment='center')
            ax1.text(0,500,"LEVEL "+"☆"*LEVEL,fontsize=40,horizontalalignment='center',verticalalignment='center')
            ax1.text(0,-500,"with_hint_Lv" + str(LEVEL) + "_ver" + str(ver) + T,fontsize=30,horizontalalignment='center',verticalalignment='center')

            # NAME = "./hint/answer_Lv" + str(LEVEL) + "_ver" + str(ver) + T + ".png"
            #plt.show()
            # plt.savefig(NAME)
            ver += 1

            fig = plt.figure(figsize=(18, 15), dpi=50)
            ax1 = fig.add_subplot(111)

            ax1.set_xlim(-460,460)
            ax1.set_ylim(-600,600)
            ax1.set_aspect('equal')
            plt.axis('off')

            for i in range(10):
                ax1.plot([-450, 450], [-450+i*100, -450+i*100], color='black')
                ax1.plot([-450+i*100, -450+i*100], [-450, 450], color='black')
            for i in range(4):
                ax1.plot([-450, 450], [-450+i*300, -450+i*300], color='black', linewidth = 3.0)
                ax1.plot([-450+i*300, -450+i*300], [-450, 450], color='black', linewidth = 3.0)
            for i in range(9):
                for j in range(9):
                    if problem[i][j] != 0:
                        ax1.text(-400+j*100,400-i*100,problem[i][j],fontsize=50,horizontalalignment='center',verticalalignment='center')
                    else:
                        ax1.text(-400+j*100,380-i*100,base_problem[i][j],fontsize=40,horizontalalignment='center',verticalalignment='center',color='red')
                        ax1.text(-400+j*100,430-i*100,hint_mat[i][j],fontsize=20,horizontalalignment='center',verticalalignment='center')
            ax1.text(0,500,"LEVEL "+"☆"*LEVEL,fontsize=40,horizontalalignment='center',verticalalignment='center')
            ax1.text(0,-500,"answer_Lv" + str(LEVEL) + "_ver" + str(ver) + T,fontsize=30,horizontalalignment='center',verticalalignment='center')

            # NAME = "./answer/answer_Lv" + str(LEVEL) + "_ver" + str(ver) + T + ".png"
            #plt.show()
            # plt.savefig(NAME)
            ver += 1
            return problem

if __name__ == '__main__':
    level = 1
    problem = get_problem(base_problem, level)