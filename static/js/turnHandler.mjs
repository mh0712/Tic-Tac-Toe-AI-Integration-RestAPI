function toggleTurn() {
    const x_turn = document.getElementById('X_turn');
    const o_turn = document.getElementById('O_turn');

    x_turn.classList.toggle('turn-background');
    o_turn.classList.toggle('turn-background');
}

export { toggleTurn }