import random
import flaghandler
import timerlogic
import gui

flaghandler

#GameHandler class is responsible for every game mode
class GameHandler():
    def __init__(self):
        print("Initializing GameHandler...")

        self.score = 0
        self.round = 0
        self.lives = 0
        self.streak = 0
        self.gamemode = -1
        self.devstatusprint = False
        self.all_flags = flaghandler.completeFlagList
    
    #call next round
    def nextround(self):
        if self.devstatusprint:
            print()
            print("Current Round", self.round)

        gui.displayRound(self.round)

        #pick a random  flag, remove from remaining set
        self.current_flag = random.choice(list(self.remaining_flags))
        self.remaining_flags.remove(self.current_flag)
        self.current_flag = self.current_flag[:-4]

        #start timer if needed
        if self.gamemode == 1:
            gui.displayTimer()
            timerlogic.clock.runClassicTimer()

        #ask to update gui
        self.updateGUI()
    
    #reset counters
    def reset(self):
        self.remaining_flags = set(self.all_flags)
        self.round = 1
        self.score = 0
        self.streak = 0
        
        gui.displayScore(self.score)
        gui.displayStreak(self.streak)
        gui.displayLives(self.lives)

    #initialize classic game mode
    def classic(self):
        print("Launching Classic Game...")
        gui.changeTitle("Classic")

        self.reset()
        self.lives = 3
        self.gamemode = 0

        print("Game Start!")
        self.nextround()

    #initialize adnvanced game mode
    def advanced(self):
        print("Launching Advanced Game...")
        gui.changeTitle("Advanced")

        self.reset()
        self.lives = 3
        self.gamemode = 1

        print("Game Start!")
        self.nextround()

    def playerAnswered(self, btn: int):
        #if no game yet launched, skip function
        if self.gamemode == -1:
            return
        
        #check if answer was correct
        if self.buttons[btn] == self.current_flag.upper().replace("_", " "):
            self.streak += 1

            #change score depending on the game mode
            #classic score
            if self.gamemode == 0:
                self.score += 100

            #advanced score
            elif self.gamemode == 1:
                roundtime = timerlogic.clock.readAccurate()

                if roundtime < 5:
                    pointsGained = 100 + (20 * (5 - roundtime))
                
                else:
                    pointsGained = 100
                
                pointsGained = pointsGained * (((1 / -self.streak) + 2) ** 1.5)
                self.score += int(pointsGained)

            if self.devstatusprint:
                print("Correct! You have answered", self.streak, "times correct in a row!")

        #wrong answer handling
        else:
            self.lives -= 1
            self.streak = 0

            if self.devstatusprint:
                print("Wrong!", self.lives, "lives remaining.")
        
        if self.devstatusprint:
            print("Current score:", self.score)

        gui.displayScore(self.score)
        gui.displayStreak(self.streak)
        gui.displayLives(self.lives)
        
        #check if game is over
        if self.lives == 0:
            self.gamemode = -1

            if self.devstatusprint:
                print("Game over, you're out of lives! Start new game from File > New game.")
        
        #launch next round
        else:
            self.round += 1
            self.nextround()

    def updateGUI(self):
        #read new flag
        flagPath = flaghandler.flagdir
        photoPath = flagPath + '/' + self.current_flag + ".png"

        #update displayed flag to player
        gui.nextflag(photoPath)

        #generate 4 options
        self.buttons = [self.current_flag.upper().replace("_", " ")]
        
        for _ in range(3):
            wrong_answer = self.current_flag
            
            while wrong_answer == self.current_flag:
                wrong_answer = random.choice(self.all_flags)
                wrong_answer = wrong_answer[:-4]
            
            self.buttons.append(wrong_answer.upper().replace("_", " "))
        
        random.shuffle(self.buttons)

        if self.devstatusprint:
            print("Generated options", self.buttons, "out of which", self.current_flag.upper().replace("_", " "), "is correct.")

        #update displayed buttons to player
        gui.nextbuttons(self.buttons)

masterGameHandler = GameHandler()