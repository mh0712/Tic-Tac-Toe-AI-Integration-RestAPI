from flask import Flask, request, jsonify, render_template 

# Initialize the Flask app
app = Flask(__name__)


board = [' ' for _ in range(9)]
HUMAN_PLAYER = 'X'
AI_PLAYER = 'O'

def is_board_full(board):
    return ' ' not in board

def is_winner(board, player):
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for line in lines:
        a, b, c = line
        if board[a] == player and board[b] == player and board[c] == player:
            return True

    return False


def make_ai_move(board):
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = AI_PLAYER
            score = minimax(board, False, alpha, beta)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
                alpha = max(alpha, best_score)
    return best_move

def minimax(board, is_maximizing, alpha, beta):
    if is_winner(board, AI_PLAYER):
        return 1
    if is_winner(board, HUMAN_PLAYER):
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        return maximizing(board, alpha, beta)
    else:
        return minimizing(board, alpha, beta)

def maximizing(board, alpha, beta):
    best_score = float("-inf")
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = AI_PLAYER
            score = minimax(board, False, alpha, beta)
            board[i] = ' '
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if best_score >= beta: break
    return best_score

def minimizing(board, alpha, beta):
    best_score = float('inf')
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = HUMAN_PLAYER
            score = minimax(board, True, alpha, beta)
            board[i] = ' '
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if best_score <= alpha: break
    return best_score



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    human_move = data['move'] # i

    # Check the status of the game after human move
    if board[human_move] == ' ' and not is_winner(board, HUMAN_PLAYER) and not is_winner(board, AI_PLAYER) and not is_board_full(board): 
        board[human_move] = HUMAN_PLAYER
        # Check if the human wins after the move or if the board is full
        if not is_winner(board, HUMAN_PLAYER) and not is_board_full(board):
            ai_move = make_ai_move(board)
            board[ai_move] = AI_PLAYER

    return jsonify({'board': board}), 201

# Route to reset the game
@app.route('/reset_game', methods=['POST'])
def reset_game():
    global board
    board = [' ' for _ in range(9)]
    return jsonify({'message': 'Game reset', 'board': board})

# Run the flask app
if __name__ == '__main__':
    app.run(debug=True)
    
