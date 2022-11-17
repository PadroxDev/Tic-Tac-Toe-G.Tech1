import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
from random import randint
from time import sleep

class BoardSlot:
    def __init__(self, x:int, y:int, parent:tk.Frame, slot_clicked_method, update_turn)->None:
        self.sign = "blank"
        self.x = x
        self.y = y
        self.parent = parent
        self.slot_clicked_method = slot_clicked_method
        self.update_turn = update_turn
        self.init_images()
        self.init_button()

    def init_images(self):
        self.normalImg = ImageTk.PhotoImage(Image.open(f"images/{self.sign}_normal.png"))
        self.hoverImg = ImageTk.PhotoImage(Image.open(f"images/{self.sign}_hover.png"))
        if (self.sign != "blank"): self.validatedImg = ImageTk.PhotoImage(Image.open(f"images/{self.sign}_validated.png"))

    def init_button(self):
        self.button = tk.Button(self.parent, image=self.normalImg)
        self.button.grid(row=self.x, column=self.y)
        self.clickBinding = self.button.bind("<Button-1>", self.on_click)
        self.enterBinding = self.button.bind("<Enter>", self.on_enter)
        self.leaveBinding = self.button.bind("<Leave>", self.on_leave)

    def on_click(self, e):
        self.button.unbind("<Button-1>", self.clickBinding)
        self.sign = self.slot_clicked_method()
        self.init_images()
        self.button.config(image=self.normalImg)
        self.update_turn()

    def on_enter(self, e):
        self.button.config(image=self.hoverImg)

    def on_leave(self, e):
        self.button.config(image=self.normalImg)

    def validate(self):
        self.button.unbind("<Enter>", self.enterBinding)
        self.button.unbind("<Leave>", self.leaveBinding)
        self.button.config(image=self.validatedImg)

# Inheritance from Tk
class App(tk.Tk):
    def __init__(self, size:int=500)->None:
        super().__init__()
        self.size = size
        self.turn = 0

        self.setup_window()
        self.init_game()

    # Setup window's properties
    def setup_window(self):
        self.title("Tic Tac Toe")
        self.geometry(f"{self.size}x{self.size}")

    def init_game(self):
        self.menu_frame = tk.Frame(self, width=self.size, height=self.size, bg="White")
        self.title_label = tk.Label(self.menu_frame, text="Welcome to Tic Tac Toe!", font=("Arial Black", 25), bg="White")
        self.title_label.pack(pady=10)
        self.name1_label = tk.Label(self.menu_frame, bg="White", text="Player1: ")
        self.name1_label.pack(padx=3)
        self.name1_entry = tk.Entry(self.menu_frame, bg="#ebebeb", justify="center")
        self.name1_entry.pack(pady=5)
        self.name2_label = tk.Label(self.menu_frame, bg="White", text="Player2: ")
        self.name2_label.pack(padx=3)
        self.name2_entry = tk.Entry(self.menu_frame, bg="#ebebeb", justify="center")
        self.name2_entry.pack(pady=5)
        self.second_player_ai_button = tk.Checkbutton(self.menu_frame, text="AI", font=("Arial", 18), bg="White")
        self.second_player_ai_button.pack(pady=10)
        self.start_button = tk.Button(self.menu_frame, text="Start", bg="#0097e6", fg="#ffffff", width=8, height=1, font=("Arial", 18), command=self.start_game)
        self.start_button.pack(pady=10)
        self.menu_frame.pack()

    def start_game(self):
        self.p1_name = self.name1_entry.get()
        self.p2_name = self.name2_entry.get()
        if (self.p1_name == ""): self.p1_name = "Player 1"
        if (self.p2_name == ""): self.p2_name = "Player 2"
        self.menu_frame.pack_forget()
        self.board = self.generate_board()

    # Generate the game board
    def generate_board(self):
        self.board_frame = tk.Frame(self, width=self.size, height=self.size, bg="White")
        board = [[BoardSlot(row, col, self.board_frame, self.slot_clicked, self.update_turn) for col in range(3)] for row in range(3)]
        self.board_frame.pack(padx=10, pady=10)
        return board

    # Returns the current player's sign
    def getPlayerSign(self)->str:
        return ["cross", "circle"][self.turn % 2]

    def validate_slot(self, slot:BoardSlot):
        slot.validate()
        self.update()
        sleep(0.2)

    # Check the rows of the board in case a player won
    def checkRows(self, board:list):
        for row in board:
            res = set()
            for slot in row:
                res.add(slot.sign)
            if(len(res)) == 1 and row[0].sign != "blank":
                for i in range(3):
                    self.validate_slot(row[i])
                return row[0].sign
        return 0

    # Check the diagonals of the board in case a player won
    def checkDiagonals(self):
        # From top left to bottom right
        if (len(set([self.board[i][i].sign for i in range(3)])) == 1 and self.board[0][0].sign != "blank"):
            for i in range(3):
                self.validate_slot(self.board[i][i])
            return self.board[0][0].sign
        # From top right to bottom left
        if (len(set([self.board[i][3-i-1].sign for i in range(3)])) == 1 and self.board[0][3-1].sign != "blank"):
            for i in range(3):
                self.validate_slot(self.board[i][3-i-1])
            return self.board[0][3-1].sign
        return 0

    # Check the rows, columns and diagonals in case a player won
    def checkWin(self):
        # transposition to check rows, then columns
        for newBoard in [self.board, np.transpose(self.board)]:
            result = self.checkRows(newBoard)
            if result: return result
        return self.checkDiagonals()

    # Return True if the board is full 
    def isBoardFull(self):
        for row in range(3):
            for col in range(3):
                if (self.board[row][col].sign == "blank"):
                    return False
        return True

    def slot_clicked(self):
        return self.getPlayerSign()
    
    def update_turn(self):
        self.turn += 1
        winner = self.checkWin()
        if (winner):
            print(winner)
        if (self.isBoardFull()):
            print("DRAW")

def main():
    app = App()
    app.mainloop()

if (__name__ == "__main__"):
    main()