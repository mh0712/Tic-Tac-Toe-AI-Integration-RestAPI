

function makeMove(move, cells, difficulty) {
    fetch(`/make_move/${difficulty}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ move: parseInt(move) }),
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data, cells);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function resetGame(starting_player, cells, difficulty) {
    fetch(`/reset_game/${starting_player}/${difficulty}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message)
        updateBoard(data, cells);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateBoard(data, cells) {
    // to remove the background of the previous winner, if there is any.
    cells.forEach(cell => {
        cell.classList.remove('winning-cells');
    });

    cells.forEach((cell, index) => {
        cell.textContent = data.board[index]; // fill
        if (data.winningIndexes && data.winningIndexes.includes(index)) {
            cell.classList.add('winning-cells');
        }
    });
}

export { makeMove, resetGame, updateBoard };
