# SOFTWARE MODULE ARCHITECTURE LAYOUT

```mermaid
---
title: FLAG QUIZ GAME MODULE ARCHITECTURE
---
classDiagram

main --|> gui
gui -- gamehandler
gui <-- rules
gui <-- stats
gui <-- history
stats <-- gamehandler
history <-- gamehandler
gamehandler -- flaghandler
gamehandler -- timerlogic
gui <-- timerlogic

class main{
empty main.py module created to
dodge the circular import error
}

class gui{
- responsible for the graphical interface
- creates an underlying 4-tab structure
- other modules are free to update these tabs
- sends player actions and events to gamehandler
(tab0) : Game
(tab1) : History
(tab2) : Stats
(tab3) : Rules
}

class rules{
- reads the rulebook file, handles errors
- sends rules as text once to gui.tab3
}

class stats{
- separate csv file used to keep track
of local machine all-time statistics
- updated after each game
- handles reading and writing
}

class history{
- reads and writes the game history,
handles any errors
- updated after each game
}

class gamehandler{
- responsible for all game logic
- handles every game mode
- updates GUI accordingly
- sends updates to history & statistics 
}

class flaghandler{
- manages the flag source image directory
- reads flag files and notifies if imports
fail or flags are missing
}

class timerlogic{
- utilizes the timeit library to read
accurate timings
- sends timing info constantly to gui
}

```
