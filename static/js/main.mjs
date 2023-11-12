import { makeMove, resetGame, updateBoard } from './gameHandler.mjs';
import { toggleTurn } from './turnHandler.mjs';

document.addEventListener('DOMContentLoaded', () => {
    let turn = "Human"
    const cells = document.querySelectorAll('.cell');
    const resetButton = document.getElementById('play-again');
    const pickPlayerTurn = document.getElementById('pick_player');
     
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            makeMove(cell.id, cells);
        });
    });

    pickPlayerTurn.addEventListener('click', () => {
        console.log(turn)
        if (turn === "AI") {turn = "Human"}
        else {turn = "AI"}
        resetGame(turn, cells)
        toggleTurn()
    })
    
    resetButton.addEventListener('click', () => {
        resetGame(turn, cells);
    });

});

