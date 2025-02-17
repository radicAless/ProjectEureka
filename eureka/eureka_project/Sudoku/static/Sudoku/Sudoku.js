// definizione variabili
let numSelected = null;
let cellaSelected = null;
let gommaSelected = null;
let difficulty = "easy"
let board;
let board_sol;

document.addEventListener('DOMContentLoaded', function() {
    let difficultyElement = document.getElementById('difficulty');
    if (difficultyElement !== null && difficultyElement.dataset.difficulty !== undefined) {
        difficulty = difficultyElement.dataset.difficulty;
        console.log("Difficulty:", difficulty);
    }
    else{
        difficulty = "easy";
    }
    fetchApi("1", difficulty);
});


// let difficultyElement = document.getElementById('difficulty');
// if (difficultyElement) {
//     let difficulty = difficultyElement.dataset.difficulty;
//     console.log("Difficulty:", difficulty);
// }



// chiamata api
function fetchApi(n, difficulty){
    console.log(difficulty);
    // definizione funzioni per consentire l'uso dell'api
    const encodeBoard = (board) => board.reduce((result, row, i) => result + `%5B${encodeURIComponent(row)}%5D${i === board.length -1 ? '' : '%2C'}`, '')
    const encodeParams = (params) =>
    Object.keys(params)
    .map(key => key + '=' + `%5B${encodeBoard(params[key])}%5D`)
    .join('&');

    let apiUrl = "https://sugoku.onrender.com/board?difficulty="+difficulty
    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if(difficulty == "easy"){
            board = data.board;
            
            fetch('https://sugoku.onrender.com/solve', {
                method: 'POST',
                body: encodeParams(data),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            })
            .then(response => response.json())
            .then(response => {
                console.log(response);
                board_sol = response.solution;
            })
        }
        if(difficulty == "medium"){
            board = data.board;
            fetch('https://sugoku.onrender.com/solve', {
                method: 'POST',
                body: encodeParams(data),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            })
            .then(response => response.json())
            .then(response => {
                console.log(response);
                board_sol = response.solution;
            })
        }
        if(difficulty == "hard"){
            
            board = data.board;
            fetch('https://sugoku.onrender.com/solve', {
                method: 'POST',
                body: encodeParams(data),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            })
            .then(response => response.json())
            .then(response => {
                console.log(response);
                board_sol = response.solution;
            })
        }
        if(n == "1"){
            setGame();
        }
        else{
            setNewGame();
        }
        
    })
    
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        problema_api();
    });
}





// fetchApi("1");


// window.onload = function(){
//     //setGame();
//     cancella();
// }

function setGame(){

    testo = document.getElementById("difficulty")
    if(testo == null){
        console.log("testo")
        testo = document.getElementById("Difficoltà")
    }
    if(difficulty == "easy"){
        testo.innerText = "Difficoltà: facile"
    }
    if(difficulty == "medium"){
        testo.innerText = "Difficoltà: media"
    }
    if(difficulty == "hard"){
        testo.innerText = "Difficoltà: difficile"
    }
    for (let i = 1; i <= 9; i++){
        // creo i div per la barra di inserimento numeri
        let number = document.createElement("div");
        
        number.id = i;
        number.innerText = i;
        number.addEventListener("click", selectNumber);
        number.classList.add("numero");
        document.getElementById("numeri").appendChild(number);
    }
   
    // creo la tabella
    for(let i = 0; i < 9; i++){
        for(let j = 0; j < 9; j++){
           let cella = document.createElement("div");
           cella.id = i.toString() + "-" + j.toString();
           if(board[i][j] > 0){
            cella.innerText = board[i][j];
            cella.classList.add("celle_iniziali");
           }
           if( i == 2 || i == 5){
            cella.classList.add("riga_orizzontale");
           }
           if( j == 2 || j == 5){
            cella.classList.add("riga_verticale");
           }
           cella.addEventListener("click", selectCella);
           cella.classList.add("cella"); 
           document.getElementById("tabella").appendChild(cella);
        }
    }
}


// aggiunta sfondo grigio per il numero che seleziono dalla barra in basso
function selectNumber(){
    if(numSelected != null){
        numSelected.classList.remove("num_selected");
    }
    numSelected = this;
    numSelected.classList.add("num_selected");
}

function del_cella(){
    if(numSelected != null){
        numSelected.classList.remove("num_selected");
        numSelected = null;
    }
    gommaSelected = this;
    //gomma.classList.add("gomma_selected");
}

function selectCella() {
    if(gommaSelected != null){
        if(this.classList.contains("celle_iniziali")){
            return;
        }
        else{
            this.innerText = "";
            gommaSelected = null;
        }
    }
    if (numSelected) {
            if(this.innerText != ""){
                return;
            }
            this.innerText = numSelected.id;
        }
}


function cancella(){
    gommaSelected = true;
    del_cella();
    var elements = document.getElementsByClassName("div");
    for (var i = 0; i < elements.length; i++) {
    
        elements[i].addEventListener("click", selectCella);
    }
}

function reset(){
    for(let i = 0; i < 9; i++){
        for(let j = 0; j < 9; j++){
            let id = i.toString() + "-" + j.toString();
            let v = document.getElementById(id);
            if(v.classList.contains("celle_iniziali")){}
            else{
                v.innerText = "";
            }
        }
    }
}

let sol = false;

function soluzione(){
    for(let i = 0; i < 9; i++){
        for(let j = 0; j < 9; j++){
            let id = i.toString() + "-" + j.toString();
            let v = document.getElementById(id);
            v.innerText = board_sol[i][j];
        }
    }
    sol = true;
}   

function verifica(){
    flag = true;
    for(let i = 0; i < 9 && flag; i++){
        for(let j = 0; j < 9 && flag; j++){
            let id = i.toString() + "-" + j.toString();
            let v = document.getElementById(id);
            if(v.innerText == board_sol[i][j]){
                flag = true;
            }
            else{
                flag = false;
            }
        }
    }
    if (flag){
        if(sol){
            alert("Risolto con successo ! punti ottenuti = 0");
        }
        else{
            alert("Risolto con successo ! punti ottenuti = n");
        }
        
    }
    else{
        alert("Errore !")
    }
}

// function nuovo(){
//     difficulty = "hard"
//     fetchApi("nuovo");

// }

function setNewGame(){
    testo = document.getElementById("difficulty")
    if(testo == null){
        testo = document.getElementById("Difficoltà")
    }
    if(difficulty === "easy"){
        testo.innerText = "Difficoltà: facile"
    }
    if(difficulty === "medium"){
        testo.innerText = "Difficoltà: media"
    }
    if(difficulty === "hard"){
        testo.innerText = "Difficoltà: difficile"
    }

    for(let i = 0; i < 9; i++){
        for(let j = 0; j < 9; j++){
            let id = i.toString() + "-" + j.toString();
            let v = document.getElementById(id);
            v.innerHTML = ""
            if(v.classList.contains("celle_iniziali")){
                v.classList.remove("celle_iniziali")
            }
            if(board[i][j] > 0){
                v.innerText = board_med[i][j];
                v.classList.add("celle_iniziali");
            }
        }
    }
}


// board di default se api non funziona

function problema_api(){
    board= [[0, 0, 7, 5, 1, 3, 6, 0, 9],
                [3, 5, 0, 7, 0, 9, 0, 0, 0],
                [1, 0, 9, 8, 2, 0, 0, 0, 0],
                [0, 8, 3, 4, 9, 2, 0, 0, 5],
                [0, 0, 0, 3, 7, 1, 2, 0, 0],
                [7, 0, 2, 6, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 5, 7, 0, 0, 4],
                [9, 0, 1, 2, 4, 0, 5, 0, 0],
                [4, 0, 0, 0, 3, 0, 8, 0, 0]]

    board_sol = [[2, 4, 7, 5, 1, 3, 6, 8, 9],
                    [3, 5, 8, 7, 6, 9, 1, 4, 2],
                    [1, 6, 9, 8, 2, 4, 3, 5, 7],
                    [6, 8, 3, 4, 9, 2, 7, 1, 5],
                    [5, 9, 4, 3, 7, 1, 2, 6, 8],
                    [7, 1, 2, 6, 8, 5, 4, 9, 3],
                    [8, 2, 6, 1, 5, 7, 9, 3, 4],
                    [9, 3, 1, 2, 4, 8, 5, 7, 6],
                    [4, 7, 5, 9, 3, 6, 8, 2, 1]]
    difficulty = "medium";
    setGame();
}

