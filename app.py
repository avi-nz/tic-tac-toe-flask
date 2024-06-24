from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

class TicTacToeGame:
    def __init__(self):
        self.board = ['-'] * 9
        self.winner = None
        self.game_running = True
        self.player = 'X'
        self.single_player = False
    
    def check_winner(self):
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] and self.board[line[0]] != '-':
                self.winner = self.board[line[0]]
                self.game_running = False
                return self.winner
        if '-' not in self.board:
            self.game_running = False
            return 'Tie'
        return None
    
    def make_move(self, position, player):
        if self.board[position] == '-':
            self.board[position] = player
            return True
        return False
    
    def switch_player(self):
        self.player = 'O' if self.player == 'X' else 'X'
    
    def computer_move(self):
        empty_positions = [i for i, spot in enumerate(self.board) if spot == '-']
        if empty_positions:
            position = random.choice(empty_positions)
            self.make_move(position, self.player)
            self.check_winner()
            self.switch_player()

game = TicTacToeGame()

@app.route('/')
def index():
    return render_template('index.html', board=game.board, message=None, game_running=game.game_running)

@app.route('/move', methods=['POST'])
def move():
    position = int(request.form['move'])
    if game.game_running and game.make_move(position, game.player):
        winner = game.check_winner()
        if winner:
            message = f"{winner} wins!" if winner != 'Tie' else "It's a tie!"
            return render_template('index.html', board=game.board, message=message, game_running=game.game_running)
        game.switch_player()
        if game.single_player and game.game_running:
            game.computer_move()
            winner = game.check_winner()
            if winner:
                message = f"{winner} wins!" if winner != 'Tie' else "It's a tie!"
                return render_template('index.html', board=game.board, message=message, game_running=game.game_running)
    return redirect(url_for('index'))

@app.route('/set_mode', methods=['POST'])
def set_mode():
    mode = request.form['mode']
    game.__init__()  # Reset the game
    if mode == 'single':
        game.single_player = True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

