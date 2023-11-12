document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const resetButton = document.getElementById('reset-button');
     
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            makeMove(cell.id);
        });
    });
    
    resetButton.addEventListener('click', () => {
        resetGame();
    });
    
    function makeMove(move) {
        fetch('/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ move: parseInt(move) }),
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    function resetGame() {
        fetch('/reset_game', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message)
            updateBoard(data.board);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    function updateBoard(data) {
        cells.forEach((cell, index) => {
            cell.textContent = data[index]; // fill
        });
    }
    
});
