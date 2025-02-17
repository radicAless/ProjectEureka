Documentazione:

Architettura alto livello: 
-	Frontend Development: HTML, CSS, JavaScript
-	Backend Development: Javascript, framework Django
-	Database: MySQL

Testing:
-	test “manuali” per controllare le funzionalità e i casi d’uso
	(accessibili dal seguente link https://drive.google.com/drive/folders/1At_El7Ki5FBruMwmk6-mqLy0BW7PhBCp?usp=share_link)
-	test automatici con utilizzo di: Django built-in TestCase

<details><summary>Struttura progetto:</summary>
Di seguito è presentata la struttura progetto, dove vengono descritti brevemente i file e il contenuto delle cartelle:

- manage.py: questo file fornisce un'interfaccia da riga di comando per eseguire comandi di gestione del progetto Django, come avviare il server di sviluppo, eseguire migrazioni del database, creare applicazioni.
- .gitlab-ci.yml: file di configurazione della pipeline presente su gitlab che consente l’esecuzione dei test presenti nel progetto.
- Requirements.txt: file utilizzato della pipeline di git per installare i componenti necessari per poter eseguire i test, è presente un file analogo per Docker.
- Dockerfile: file di testo che contiene una serie di istruzioni che Docker utilizza per creare un'immagine 
- Docker-compose.yml: file di configurazione per l’applicazione Docker.
- Cartella Eureka_project: cartella principale del progetto, indichiamo due file principali:
	-	Settings.py: file di configurazione del progetto, dove vengono specificate le impostazioni principali. Per la fase di Sprint1 e Sprint2 le seguenti variabili sono state modificate.
		- DEBUG: variabile booleana che controlla se le funzionalità di debug sono abilitate. Solitamente impostata su True nello sviluppo.
		- INSTALLED_APPS: Un elenco delle applicazioni Django installate nel progetto. Queste sono le app che vengono sviluppate e forniscono funzionalità specifiche al progetto.
		- STATIC_URL: Impostazioni per indicare dove si trovano i file statici (ad esempio, CSS, JavaScript, immagini).
	-	Urls.py: file in cui viene specificata una lista di Url, che indicano il percorso per raggiungere il file views.py di ogni app installata 
	-	db.sqlite3: file locale del db in cui sono contenute tutte le tabelle e oggetti.

- Cartella Home: cartella in cui sono definite le pagine principali dell’applicazione, qui si trovano l’implementazione della pagina inziale e l’implementazione delle pagine per la selezione dei giochi (categorie), per la selezione della difficoltà e per accedere al profilo utente
	- Cartella templates: in questa cartella sono presenti i file html che definiscono le pagine del sito.
	-	Tests.py: file in cui sono definiti i test relativi alle views e al funzionamento del db.
	-	Urls.py: file in cui vengono definiti gli URL che l'applicazione può gestire e le associazioni tra gli URL e le viste (views) corrispondenti. 
	-	Views.py: file che contiene le definizioni delle viste (views), che sono funzioni Python responsabili di elaborare le richieste HTTP e restituire una risposta http, questo consente di visualizzare il file HTML corrispondente.
	-	models.py: file in cui sono definite le tabelle presenti nel db.
	-	admin.py: file in cui è definita la logica per gestire gli oggetti presenti nel db, dalla pagina di configurazione presente all' indirizzo: 'http://127.0.0.1:8000/admin'
- Cartella Sudoku: cartella in cui è definito il gioco del sudoku, si sottolinea l’utilizzo di una API per la creazione e risoluzione di una tabella del sudoku.  Documentazione API utilizzata: https://github.com/bertoort/sugoku.
Come per l'app home sono anche qui presenti i file Urls.py, Views.py e la cartella templates con i file html.

- Cartella Regine: cartella in cui è definito il rompicapo delle regine, Come per l'app home sono anche qui presenti i file Urls.py, Views.py e la cartella templates con i file html.
</details>

<details><summary>Struttura DB:</summary>
Segue una descrizione sintetica delle tabelle attualmente implementate:

Modelli principali:
>> Game

- name: -> Nome del gioco.
- game_type: -> Tipo di gioco.

>> GameBoard

- game: ForeignKey(Game) -> Collegamento alla tabella gioco.
- board_data: JSONField -> Dati della board di gioco in formato JSON.
- difficulty: -> Difficoltà del gioco.
- value_points: -> Punti assegnati al gioco.

>> CustomUser

- email: -> Email dell'utente.

- username: -> Nome utente.

- total_score: -> Punteggio totale dell'utente.

- completed_games: ManyToManyField(GameBoard) -> Giochi completati dall'utente.

- E dati accessori (esempio: is_superuser Se l'utente ha diritti da superuser)

>> Metodi personalizzati

- m2m_changed.connect(): aggiorna total_score dell'utente online al completamento di un gioco
</details>

<details><summary>ISTRUZIONI PER IL FUNZIONAMENTO DELL'APP SU DOCKER:</summary>

- scaricare docker
- avviare docker
- aprire prompt dei comandi
- navigare fino alla cartella del progetto
- digitare docker-compose up
- attendere la fine della configurazione automatica quando compare questo messaggio:

	[+] Running 3/3
 		✔ Network eureka_default  Created                                                                          
 		✔ Container eureka-web-1  Created                                                                          
 		✔ Container eureka-db-1   Created                                                                          
		Attaching to eureka-db-1, eureka-web-1
		eureka-web-1  | Watching for file changes with StatReloader

- aprire un browser web e digitare: 

	-http://localhost:8000 
	oppure
	-http://127.0.0.1:8000

- per terminare premere ctrl-c nel prompt dei comandi
- uscire da docker-desktop
</details>


