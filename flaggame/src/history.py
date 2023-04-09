import sys
from datetime import datetime

print("Opening (creating if it doesn't exist) the game history file 'history.txt'...")

def curr_time():
    return datetime.now().isoformat(sep=" ", timespec="minutes")

#check history file
try:
    f = open('history.txt', 'a+')
    f.write(f"\n\n/// /// /// /// /// ///\nNEW SESSION AT {curr_time()}\n")
    f.close()

except:
    print("ERROR while opening 'history.txt.':")
    print("Please ensure file integrity or create it manually before continuing.")
    print("You may have to close the file before running the software again.")
    sys.exit(1)

def clearHistory():
    print("Deleting all progress and history permantently.")
    f = open('history.txt', 'w+')
    f.close()
    print("Closing program...")
    sys.exit(1)

#debug option to
def consolePrint():
    print("Contents of file 'history.txt':")
    with open('history.txt', 'r') as f:
        print(f.read())

#game_handler calls history changes
#game start recorded
def gameStart(mode: str):
    with open('history.txt', 'a+') as f:
        f.write(f"\n\n{mode} Game launched at {curr_time()}.")

#game over, game info recorded
def gameOver(info: list):
    with open('history.txt', 'a+') as f:
        if info[0] == 0:
            mode = "Classic"
        
        elif info[0] == 1:
            mode = "Advanced"

        elif info[0] == 4:
            mode = "Free"
        
        time = datetime.now().isoformat(sep=" ", timespec="seconds")
        f.write(f"\n{mode} Game finished at {curr_time()}:")
        f.write(f"\nScore: {info[1]} - Longest Continuous Streak: {info[2]}.")

#reading most recent history from file
def update():
    with open('history.txt', 'r') as f:
        return f.read()