import customtkinter
from tkinter import Canvas
import problem_maker as maker
import pulp_solver as solver
import signal
import sys

FONT_TYPE = "meiryo"
level_max = 10

base_problem = [[2, 3, 4, 1, 5, 9, 7, 8, 6],
        [7, 5, 6, 4, 8, 3, 1, 2, 9], 
        [8, 9, 1, 7, 2, 6, 4, 5, 3], 
        [4, 2, 3, 8, 6, 7, 5, 9, 1], 
        [5, 6, 7, 2, 9, 1, 8, 3, 4],
        [1, 8, 9, 5, 3, 4, 2, 6, 7],  
        [6, 4, 5, 3, 1, 2, 9, 7, 8], 
        [9, 7, 8, 6, 4, 5, 3, 1, 2], 
        [3, 1, 2, 9, 7, 8, 6, 4, 5]]

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # member variables
        self.fonts = (FONT_TYPE, 15)
        self.geometry("600x400")
        self.title("Number Place Solver GUI")
        self.current_level = 1
        self.solving_time = 0

        # current problem
        self.current_problem = maker.get_problem(base_problem)

        # setup
        self.setup_form()

    def setup_form(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        # "Next" Button
        self.next_button = customtkinter.CTkButton(master=self, text="Next", command=self.load_problem, font=self.fonts)
        self.next_button.place(x=50, y=100)

        # "Solve" Button
        self.solve_button = customtkinter.CTkButton(master=self, text="Solve", command=self.solve_sudoku, font=self.fonts)
        self.solve_button.place(x=50, y=150)

        # "Level" Button
        self.level_down_button = customtkinter.CTkButton(master=self, text="◀", command=self.decrease_level, font=self.fonts, width=5)
        self.level_down_button.place(x=48, y=50)
        self.level_up_button = customtkinter.CTkButton(master=self, text="▶", command=self.increase_level, font=self.fonts, width=5)
        self.level_up_button.place(x=163, y=50)

        # "Level" Label
        self.level_label = customtkinter.CTkLabel(master=self, text=f"Level: {self.current_level}", font=self.fonts)
        self.level_label.place(x=92, y=50)

        # Solve Time Label
        self.solving_time_label = customtkinter.CTkLabel(master=self, text=f"Solving time:  sec", font=self.fonts)
        self.solving_time_label.place(x=50, y=200)


        # Canvas for Sudoku
        self.sudoku_canvas = Canvas(self, width=295, height=295, bg="white")
        self.sudoku_canvas.place(x=250, y=50)

        # initial display
        self.display_sudoku(self.current_problem, color="blue", update_current=True)

    def increase_level(self):
        if self.current_level < level_max:
            self.current_level += 1
            self.update_level()

    def decrease_level(self):
        if self.current_level > 1:
            self.current_level -= 1
            self.update_level()

    def update_level(self):
        self.level_label.configure(text=f"Level: {self.current_level}")

    def display_sudoku(self, grid, color="black", update_current=False):
        self.sudoku_canvas.delete("all")
        cell_size = 33  # cell size
        for i in range(9):
            for j in range(9):
                x0 = j * cell_size
                y0 = i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                self.sudoku_canvas.create_rectangle(x0, y0, x1, y1, outline="black")

                if grid[i][j] != 0:
                    self.sudoku_canvas.create_text(
                        x0 + cell_size // 2, y0 + cell_size // 2,
                        text=str(grid[i][j]), fill=color, font=(FONT_TYPE, 14)
                    )
                if update_current:
                    self.current_problem[i][j] = grid[i][j]

    def load_problem(self):
        problem = maker.get_problem(base_problem, self.current_level)
        # print("Problem】")
        # print(problem)
        self.display_sudoku(problem, color="blue", update_current=True)

    def solve_sudoku(self):
        # print("【Current Problem】")
        # print(self.current_problem)
        solution, time = solver.solve(self.current_problem)
        for i in range(9):
            for j in range(9):
                if self.current_problem[i][j] == 0:  # remain blue number
                    self.sudoku_canvas.create_text(
                        j * 33 + 33 // 2, i * 33 + 33 // 2,
                        text=str(solution[i][j]), fill="black", font=(FONT_TYPE, 14)
                    )
        self.solving_time = time
        # print(time)
        if self.solving_time > 0:
            self.solving_time_label.configure(text=f"Solving time: {self.solving_time:.3f} sec")

def signal_handler(sig, frame):
    print("\nExiting...")
    app.destroy()  # close window
    sys.exit(0)    # finish program

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    app = App()
    app.mainloop()
