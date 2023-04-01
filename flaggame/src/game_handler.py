import random
import timeit
import flaghandler
import gui

flaghandler

class GameHandler():
    def __init__(self):
        print("Initializing GameHandler...")
        self.score = 0
        self.round = 0
        self.lives = 0
        self.timer = 0
        self.gamemode = -1
        self.all_flags = flaghandler.completeFlagList
    
    def nextround(self):
        print("Current Round", self.round)
        #pick a random  flag, remove from remaining set
        self.current_flag = random.choice(list(self.remaining_flags))
        self.remaining_flags.remove(self.current_flag)

        self.current_flag = self.current_flag[:-4]

        #ask to update gui
        self.updateGUI()
    
    def classic(self):
        print("Launching Classic Game...")
        #reset scores
        self.round = 0
        self.score = 0
        self.lives = 3
        self.gamemode = 0

        #reset & randomize flag queue 
        self.remaining_flags = set(self.all_flags)

        print("Game Start!")
        self.nextround()

    def playerAnswered(self, btn: int):
        #if no game yet launched, skip function
        if self.gamemode == -1:
            return
        
        #check if answer was correct
        if self.buttons[btn] == self.current_flag.upper().replace("_", " "):
            self.round += 1

            #change score depending on the game mode
            if self.gamemode == 0:
                self.score += 100
                print("Correct! Your current score is:", self.score)
        
        else:
            self.lives -= 1
            print("Wrong!", self.lives, "lives remaining.")
        
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

        print("DEBUGGING: Generated options", self.buttons, "out of which", self.current_flag.upper().replace("_", " "), "is correct.")
        print()

        #update displayed buttons to player
        gui.nextbuttons(self.buttons)

masterGameHandler = GameHandler()