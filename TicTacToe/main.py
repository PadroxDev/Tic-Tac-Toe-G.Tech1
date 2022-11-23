import tkinter as tk

from PIL import ImageTk, Image
from random import randint
from time import sleep
from numpy import transpose

# This is the global class for the Players
class Player:
    def __init__(self, name:str):
        self.name = name
        self.score = 0
        self.order = 0

    def change_order(self, order:int)->None:
        self.order = order

    def play(self):
        print("Playing...")

# This class is deriving from Player, for Human Behaviour
class Human(Player):
    def __init__(self, name:str):
        super().__init__(name)

    def play(self):
        print("Human's playing")

# This class is deriving from Player, for AI Behaviour
class AI(Player):
    def __init__(self, name:str):
        super().__init__(name)

    def play(self):
        print("AI's playing")

# This class represent each cell of the game board
class BoardSlot:
    def __init__(self, x:int, y:int, parent_surf:tk.Frame, get_current_player_sign, update_turn)->None:
        self.sign = 'blank'
        self.x = x
        self.y = y
        self.parent_surf = parent_surf
        self.get_current_player_sign = get_current_player_sign
        self.update_turn = update_turn
        self.update_images()
        self.init_button()

    # Return the loaded image from the given path
    def load_image(self, path:str):
        return ImageTk.PhotoImage(Image.open(path))

    # Update the images based on the slot sign
    def update_images(self):
        self.default_img = self.load_image(f"images/{self.sign}_default.png")
        self.hover_img = self.load_image(f"images/{self.sign}_hover.png")
        if (self.sign != 'blank'): self.validated_img = self.load_image(f"images/{self.sign}_validated.png")
    
    # Initialize the button
    def init_button(self):
        self.button = tk.Button(self.parent_surf, image=self.default_img)
        self.button.grid(row=self.x, column=self.y)
        self.click_binding = self.button.bind("<Button-1>", self.on_click)
        self.enter_binding = self.button.bind("<Enter>", self.on_enter)
        self.leave_binding = self.button.bind("<Leave>", self.on_leave)

    # Disconnect the click binding or every bindings
    def disconnect_bindings(self, all=False):
        self.button.unbind("<Button-1>")
        if (all):
            self.button.unbind("<Enter>")
            self.button.unbind("<Leave>")

    # On Click action
    def on_click(self, _):
        self.disconnect_bindings() # One time click
        self.sign = self.get_current_player_sign()
        self.update_images()
        self.button.config(image=self.hover_img)
        self.update_turn()

    # On hover enter action
    def on_enter(self, _):
        self.button.config(image=self.hover_img)

    # On hover leave action
    def on_leave(self, _):
        self.button.config(image=self.default_img)

    # This method is called to validate a slot
    def validate(self):
        self.disconnect_bindings(True)
        self.button.config(image=self.validated_img)

# This is the application class deriving from the Tk object of tkinter
class App(tk.Tk):
    def __init__(self, width:int=500, height:int=600)->None:
        super().__init__()
        
        # General attributes
        self.width = width
        self.height = height

        self.turn = 0

        self.setup_window()
        self.setup_menu_window()

    # Setup the window's properties
    def setup_window(self):
        self.title('Tic Tac Toe')
        self.geometry(f"{self.width}x{self.height}")

    # Handle all the graphic elements of the menu viewport
    def setup_menu_window(self):
        self.menu_frame = tk.Frame(self, width=self.width, height=self.height, bg="White")
        self.title_label = tk.Label(self.menu_frame, text="Welcome to Tic Tac Toe!", font=("Arial Black", 25), bg="White")
        self.title_label.pack(pady=10)
        self.name1_label = tk.Label(self.menu_frame, bg="White", text="Player1: ")
        self.name1_label.pack()
        self.name1_entry = tk.Entry(self.menu_frame, bg="#ebebeb", justify="center")
        self.name1_entry.pack(pady=5)
        self.name2_label = tk.Label(self.menu_frame, bg="White", text="Player2: ")
        self.name2_label.pack(padx=3)
        self.name2_entry = tk.Entry(self.menu_frame, bg="#ebebeb", justify="center")
        self.name2_entry.pack(pady=5)
        self.is_ai_result = tk.IntVar()
        self.second_player_ai_button = tk.Checkbutton(self.menu_frame, text="Is AI?", font=("Arial", 18), bg="White", variable=self.is_ai_result)
        self.second_player_ai_button.pack(pady=10)
        self.start_button = tk.Button(self.menu_frame, text="Start", bg="#0097e6", fg="#ffffff", width=8, height=1, font=("Arial", 18), command=self.player_data)
        self.start_button.pack(pady=10)
        self.menu_frame.pack()

    # Create two instances of Player and start the game
    def player_data(self)->None:
        name1, name2 = self.name1_entry.get(), self.name2_entry.get()
        if (name1 == ""): name1 = "Player 1"
        if (name2 == ""): name2 = "Player 2"
        self.player1 = Human(name1)
        if (self.is_ai_result):
            self.player2 = AI(name2)
        else:
            self.player2 = Human(name2)
        self.setup_static_game_window()
        self.start_game()

    # Start a new round
    def start_game(self)->None:
        randomizedOrder = self.get_random_first_player()
        self.player1.change_order(randomizedOrder[0])
        self.player2.change_order(randomizedOrder[1])
        self.setup_game_window()

    # Restart the game for a new round
    def restart_game(self)->None:
        self.enable_element(self.game_state_label, False)
        self.enable_element(self.rematch_button, False)
        self.remove_current_board()
        self.start_game()

    # Handle all the static graphic elements of the game viewport
    def setup_static_game_window(self)->None:
        self.enable_element(self.menu_frame, False)
        self.score_label = tk.Label(self, width=self.width, bg="#353b48", fg="#f5f6fa", font=("Arial Black", 20))
        self.score_label.pack()
        self.update_score()

    # Handle all the graphic elements of the game viewport
    def setup_game_window(self)->None:
        self.board_frame = tk.Frame(self, width=self.width, height=self.height, bg="White")
        self.board = self.generate_board()
        self.board_frame.pack(padx=10, pady=20)
        self.game_state_label = tk.Label(self, text=f"{self.get_current_player().name} 's turn!", fg="#f5f6fa", bg="#00a8ff", font=("Arial", 18))
        self.game_state_label.pack()
        self.rematch_button = tk.Button(self, text="REMATCH", font=("Arial Black", 20), fg="White", bg="#44bd32", command=self.restart_game)

    # Handle the board generation
    def generate_board(self)->list:
        board = [[BoardSlot(row, col, self.board_frame, self.get_current_player_sign, self.update_turn) for col in range(3)] for row in range(3)]
        return board

    # Enable or Disable the given graphic element
    def enable_element(self, element, enabled=True)->None:
        if (enabled):
            element.pack()
        else:
            element.pack_forget()

    # Update the displayed score
    def update_score(self):
        score_formated_message = f"{self.player1.score} {self.player1.name} VS {self.player2.name} {self.player2.score}"
        self.score_label.config(text=score_formated_message)
    
    # Update the displayed game state
    def update_game_state(self, text:str, bg:str="#00a8ff", font:tuple=("Arial", 18)):
        self.game_state_label.config(text=text, bg=bg, font=font)

    # Returns the order in which the players will play
    def get_random_first_player(self)->tuple:
        return (1, -1) if randint(0, 1) else (-1, 1)

    # Return the sign of the given player
    def get_sign(self, player:Player)->str:
        return 'cross' if player.order == 1 else 'circle'

    def get_current_player(self)->Player:
        if (self.turn % 2 == 0):
            return self.player1 if self.player1.order == 1 else self.player2
        else:
            return self.player2 if self.player2.order == -1 else self.player1

    # Return the current player
    def get_current_player_sign(self)->str:
        return self.get_sign(self.get_current_player())

    # Return if the given board is full, so a draw
    def is_board_full(self, current_board:list):
        for row in range(3):
            for col in range(3):
                if (current_board[row][col].sign == 'blank'):
                    return False
        return True

    # This method loop through each rows of the given board and return if a player won
    def check_rows(self, current_board:list):
        for row in current_board:
            res = set() # A set is similar than a list but cannot contain doubles
            for slot in row:
                res.add(slot.sign)
            if (len(res) == 1 and row[0].sign != 'blank'):
                self.disconnect_buttons_click_binding()
                for i in range(3):
                    self.validate_slot(row[i]) # Display victory line in green
                return row[0].sign
        return 0
    
    # This method loop through both diagonals of the board and return if a player won
    def check_diagonals(self, current_board:list):
        # From top left to bottom right
        if (len(set([current_board[i][i].sign for i in range(3)])) == 1 and current_board[0][0].sign != 'blank'):
            self.disconnect_buttons_click_binding()
            for i in range(3):
                self.validate_slot(self.board[i][i])
            return current_board[0][0].sign
        # From top right to bottom left
        if (len(set([current_board[i][3-i-1].sign for i in range(3)])) == 1 and current_board[0][2].sign != 'blank'):
            self.disconnect_buttons_click_binding()
            for i in range(3):
                self.validate_slot(self.board[i][3-i-1])
            return current_board[0][2].sign
        return 0
    
    # Check the rows, columns and diagonals and return the winner's sign
    def check_win(self, current_board:list):
        # transposition to check rows, then columns
        for new_board in [current_board, transpose(current_board)]:
            result = self.check_rows(new_board)
            if (result): return result
        return self.check_diagonals(current_board)

    # This method is called each time a button is clicked
    def update_turn(self)->None:
        # Check for any winner and display a victory message
        winner = self.check_win(self.board)
        if (winner):
            if (winner == self.get_sign(self.player1)): # Player 1 won
                self.update_game_state(f"--> {self.player1.name} WON! <--", "#e1b12c", ("Arial Black", 20))
                self.player1.score += 1
                self.update_score()
            else:
                self.update_game_state(f"--> {self.player2.name} WON! <--", "#e1b12c", ("Arial Black", 20))
                self.player2.score += 1
            self.update_score()
            self.enable_element(self.rematch_button)
        elif (self.is_board_full(self.board)): # Draw
            self.update_game_state("--> DRAW <--", "#487eb0", ("Arial Black", 20))
            self.enable_element(self.rematch_button)
        else: # New turn
            self.turn += 1
            self.update_game_state(f"{self.get_current_player().name}'s turn!")

    # ----------------------
    # -----> GRAPHICS <-----
    # ----------------------

    # Disconnect the click binding for each button
    def disconnect_buttons_click_binding(self)->None:
        for row in range(3):
            for col in range(3):
                self.board[row][col].disconnect_bindings()

    # Validate the given slot
    def validate_slot(self, slot:BoardSlot)->None:
        slot.validate()
        self.update() # Update the viewport
        sleep(0.2)

    # Remove the current board from the viewport
    def remove_current_board(self)->None:
        self.enable_element(self.board_frame, False)
        self.board = None

def main():
    app = App()
    app.mainloop()

if (__name__ == "__main__"):
    main()