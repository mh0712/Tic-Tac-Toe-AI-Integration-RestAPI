import random
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
            return (True, line)

    return (False, None)

def make_ai_move(board, difficulty):
    if difficulty == 'medium':
        return make_depth_limited_move(board, depth=1)
    elif difficulty == 'hard':
        return make_minimax_move(board)
    else:
        return make_random_move(board)

##################################################################
# Easy Level:      |        Random       | 
##################################################################
def make_random_move(board):
    available_moves = [i for i, val in enumerate(board) if val == ' ']
    return random.choice(available_moves)

##################################################################
# Medium Level:    |    Depth limited     | 
##################################################################
def make_depth_limited_move(board, depth):
    best_score = float('-inf')
    best_move = None

    available_moves = [i for i, val in enumerate(board) if val == ' ']

    for move in available_moves:
        board[move] = AI_PLAYER
        score = depth_limited_search(board, False, depth)
        board[move] = ' '

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def depth_limited_search(board, is_maximizing, depth):
    if depth == 0 or is_winner(board, AI_PLAYER)[0] or is_winner(board, HUMAN_PLAYER)[0] or is_board_full(board):
        return calculate_utility(board)

    if is_maximizing:
        return maximizing_1(board, depth)
    else:
        return minimizing_1(board, depth)

def calculate_utility(board):
    if is_winner(board, AI_PLAYER)[0]:
        return 1
    if is_winner(board, HUMAN_PLAYER)[0]:
        return -1
    else:
        return 0
    

def maximizing_1(board, depth):
    best_score = float("-inf")
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = AI_PLAYER
            score = depth_limited_search(board, False, depth - 1)
            board[i] = ' '
            best_score = max(score, best_score)
    return best_score

def minimizing_1(board, depth):
    best_score = float('inf')
    for i in range(len(board)):
        if board[i] == ' ':
            board[i] = HUMAN_PLAYER
            score = depth_limited_search(board, True, depth - 1)
            board[i] = ' '
            best_score = min(score, best_score)
    return best_score

##################################################################
# Hard Level:      |       Minimax        | 
##################################################################

def make_minimax_move(board):
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
    if is_winner(board, AI_PLAYER)[0]:
        return 1
    if is_winner(board, HUMAN_PLAYER)[0]:
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        return maximizing_2(board, alpha, beta)
    else:
        return minimizing_2(board, alpha, beta)

def maximizing_2(board, alpha, beta):
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

def minimizing_2(board, alpha, beta):
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


##################################################################
# Routes
##################################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move/<difficulty>', methods=['POST'])
def make_move(difficulty):
    data = request.get_json()
    human_move = data['move'] # i

    # Check the status of the game after human move
    if (board[human_move] == ' ' and not is_winner(board, HUMAN_PLAYER)[0] and
        not is_winner(board, AI_PLAYER)[0] and not is_board_full(board)):    

        board[human_move] = HUMAN_PLAYER

        # Check if the human wins after the move or if the board is full
        if not is_winner(board, HUMAN_PLAYER)[0] and not is_board_full(board):
            ai_move = make_ai_move(board, difficulty)
            board[ai_move] = AI_PLAYER

    if is_winner(board, HUMAN_PLAYER)[0]:
        return jsonify({'board': board, 'winningIndexes': is_winner(board, HUMAN_PLAYER)[1]}), 201

    if is_winner(board, AI_PLAYER)[0]:
        return jsonify({'board': board, 'winningIndexes': is_winner(board, AI_PLAYER)[1]}), 201

    # Return is_winner of the AI or Human it doesn't matter in both ways it will be None
    return jsonify({'board': board, 'winningIndexes': is_winner(board, AI_PLAYER)[1]}), 201 

@app.route('/reset_game/<starting_player>/<difficulty>', methods=['POST'])
def reset_game(starting_player, difficulty):
    global board
    board = [' ' for _ in range(9)]
    if starting_player == "AI":
        ai_move = make_ai_move(board, difficulty)
        board[ai_move] = AI_PLAYER
    return jsonify({'message': 'Game reset', 'board': board})

# Run the flask app
if __name__ == '__main__':
    app.run(debug=True)
    
