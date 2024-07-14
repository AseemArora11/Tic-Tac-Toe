import tkinter as tk
from tkinter import messagebox
from random import choice

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player_character = ''
        self.ai_character = ''
        self.positions = ['-'] * 9
        self.turn = 1
        self.player_score = 0
        self.ai_score = 0
        self.difficulty = 'Easy'
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text='Welcome to Tic-Tac-Toe!', font=("Arial", 16))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.select_label = tk.Label(self.root, text='Select a character to play as', font=("Arial", 14))
        self.select_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.x_button = tk.Button(self.root, text="X", font=("Arial", 12), width=10, command=lambda: self.select_character("X"))
        self.x_button.grid(row=2, column=1, padx=5, pady=5)

        self.o_button = tk.Button(self.root, text="O", font=("Arial", 12), width=10, command=lambda: self.select_character("O"))
        self.o_button.grid(row=2, column=2, padx=5, pady=5)

        self.difficulty_label = tk.Label(self.root, text='Select difficulty level', font=("Arial", 14))
        self.difficulty_label.grid(row=3, column=0, columnspan=3, pady=5)

        self.easy_button = tk.Button(self.root, text="Easy", font=("Arial", 12), width=10, command=lambda: self.set_difficulty('Easy'))
        self.easy_button.grid(row=4, column=0, padx=5, pady=5)

        self.hard_button = tk.Button(self.root, text="Hard", font=("Arial", 12), width=10, command=lambda: self.set_difficulty('Hard'))
        self.hard_button.grid(row=4, column=1, padx=5, pady=5)

        self.impossible_button = tk.Button(self.root, text="Impossible", font=("Arial", 12), width=10, command=lambda: self.set_difficulty('Impossible'))
        self.impossible_button.grid(row=4, column=2, padx=5, pady=5)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.score_label = tk.Label(self.root, text='Scoreboard', font=("Arial", 14))
        self.score_label.grid(row=6, column=0, columnspan=3, pady=5)

        self.player_score_label = tk.Label(self.root, text='Player: 0', font=("Arial", 12))
        self.player_score_label.grid(row=7, column=0, padx=5, pady=5)

        self.ai_score_label = tk.Label(self.root, text='AI: 0', font=("Arial", 12))
        self.ai_score_label.grid(row=7, column=2, padx=5, pady=5)

    def set_difficulty(self, level):
        self.difficulty = level

    def select_character(self, character):
        self.player_character = character
        self.ai_character = "X" if character == "O" else "O"
        self.clear_board()

    def clear_board(self):
        self.positions = ['-'] * 9
        self.turn = 1
        self.draw_board()
        if self.player_character == 'O':
            self.ai_turn()

    def draw_board(self):
        for i in range(3):
            for j in range(3):
                position = i * 3 + j
                btn_text = self.positions[position]
                btn = tk.Button(self.board_frame, text=btn_text, font=("Arial", 16), width=6, height=2,
                                command=lambda pos=position: self.player_pos(pos))
                btn.grid(row=i, column=j, padx=5, pady=5)

    def player_pos(self, position):
        if self.positions[position] == '-' and self.turn == 1:
            self.positions[position] = self.player_character
            self.update_button(position)
            self.check_game_status()
            self.turn = 0
            self.ai_turn()

    def update_button(self, position):
        btn = self.board_frame.grid_slaves(row=position // 3, column=position % 3)[0]
        btn.config(text=self.positions[position])
        btn.config(state="disabled")

    def ai_turn(self):
        if self.turn == 0 and '-' in self.positions:
            if self.difficulty == 'Easy':
                ai_select = choice([i for i, x in enumerate(self.positions) if x == '-'])
            elif self.difficulty == 'Hard':
                if choice([True, False]):
                    ai_select = self.minimax(self.positions, self.ai_character)['position']
                else:
                    ai_select = choice([i for i, x in enumerate(self.positions) if x == '-'])
            else:  # Impossible
                ai_select = self.minimax(self.positions, self.ai_character)['position']

            self.positions[ai_select] = self.ai_character
            self.update_button(ai_select)
            self.check_game_status()
            self.turn = 1

    def minimax(self, current_board, player):
        available_positions = [i for i, x in enumerate(current_board) if x == '-']

        if self.check_winner(current_board, self.player_character):
            return {'score': -1}
        elif self.check_winner(current_board, self.ai_character):
            return {'score': 1}
        elif len(available_positions) == 0:
            return {'score': 0}

        moves = []
        for pos in available_positions:
            move = {}
            move['position'] = pos
            current_board[pos] = player
            if player == self.ai_character:
                result = self.minimax(current_board, self.player_character)
                move['score'] = result['score']
            else:
                result = self.minimax(current_board, self.ai_character)
                move['score'] = result['score']
            current_board[pos] = '-'
            moves.append(move)

        if player == self.ai_character:
            best_score = -float('inf')
            for move in moves:
                if move['score'] > best_score:
                    best_score = move['score']
                    best_move = move
        else:
            best_score = float('inf')
            for move in moves:
                if move['score'] < best_score:
                    best_score = move['score']
                    best_move = move

        return best_move

    def check_winner(self, board, player):
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                return True
        return False

    def check_game_status(self):
        if self.check_winner(self.positions, self.player_character):
            self.end_game(self.player_character)
        elif self.check_winner(self.positions, self.ai_character):
            self.end_game(self.ai_character)
        elif '-' not in self.positions:
            self.end_game('Draw')

    def end_game(self, winner):
        if winner == self.player_character:
            message = 'Congratulations! You are the Tic-Tac-Toe Champion!'
            self.player_score += 1
            self.player_score_label.config(text=f'Player: {self.player_score}')
        elif winner == self.ai_character:
            message = 'AI: I\'ve won! Better luck next time, human!'
            self.ai_score += 1
            self.ai_score_label.config(text=f'AI: {self.ai_score}')
        else:
            message = 'It\'s a draw! Both are equally skilled!'

        messagebox.showinfo("Game Over", message)
        self.clear_board()


def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
