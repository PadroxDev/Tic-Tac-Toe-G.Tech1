from random import randint
from numpy import transpose

from tictactoe_ai import AI

class TicTacToe:
    def __init__(self):
        self.board = self.generate_board()
        self.running = True

    def generate_board(self):
        board = [['_' for col in range(3)] for row in range(3)]
        return board

    def set_character(self, row, col, char):
        if (self.board[row][col] == '_'):
            self.board[row][col] = char

    def player_turn(self, char):
        xInput = int(input("x: "))
        yInput = int(input("y: "))
        self.set_character(xInput, yInput, char)

    def check_rows(self, board):
        for row in board:
            if len(set(row)) == 1 and row[0] != '_':
                return row[0]
        return 0

    def check_diagonals(self):
        if len(set([self.board[i][i] for i in range(3)])) == 1 and self.board[0][0] != '_':
            return self.board[0][0]
        if len(set([self.board[i][3-i-1] for i in range(3)])) == 1 and self.board[0][2] != '_':
            return self.board[0][2]
        return 0

    def check_win(self):
        for new_board in [self.board, transpose(self.board)]:
            result = self.check_rows(new_board)
            if result: return result
        return self.check_diagonals()

    def is_board_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '_':
                    return False
        return True

    def run(self):
        turn = 0
        p1_sign = 'x' if randint(0, 1) else 'o'
        p2_sign = 'o' if p1_sign == 'x' else 'x'
        while self.running:
            self.player_turn(p1_sign if turn % 2 == 0 else p2_sign)
            print(self)
            winner = self.check_win()
            
            if winner:
                print(f"{winner} won!")
                self.running = False
            elif self.is_board_full():
                print("Draw")
                self.running = False
            else: turn += 1
                
    def __str__(self):
        res = ""
        for row in self.board:
            res += str(row) + "\n"
        return res

if __name__ == "__main__":
    game = TicTacToe()
    game.run()