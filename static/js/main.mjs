import { makeMove, resetGame, updateBoard } from './gameHandler.mjs';
import { toggleTurn } from './turnHandler.mjs';

document.addEventListener('DOMContentLoaded', () => {
    let turn = "Human"
    let selectedMode = 'Easy';
    const cells = document.querySelectorAll('.cell');
    const resetButton = document.getElementById('play-again');
    const pickPlayerTurn = document.getElementById('pick_player');
    const modes = document.querySelectorAll('.mode_button');
    const header = document.getElementById('titleMode');
     
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            makeMove(cell.id, cells, selectedMode);
        });
    });
    
    resetButton.addEventListener('click', () => {
        resetGame(turn, cells, selectedMode);
    });
    
    pickPlayerTurn.addEventListener('click', () => {
        if (turn === "AI") {turn = "Human"}
        else {turn = "AI"}
        resetGame(turn, cells, selectedMode)
        toggleTurn()
    })

    modes.forEach(modeButton => {
        modeButton.addEventListener('click', (event) => {
            selectedMode = event.target.textContent.toLowerCase(); 
            resetGame(turn, cells, selectedMode);
            header.textContent = `${event.target.textContent} Mode`
        });
    });

});

