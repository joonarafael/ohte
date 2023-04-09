import random
import flaghandler
import timerlogic
import history
import gui

# GameHandler class is responsible for every game mode


class GameHandler():
    def __init__(self):
        print("Initializing GameHandler...")

        self.score = 0
        self.round = 0
        self.lives = 0
        self.streak = 0
        self.highestStreak = 0
        self.gamemode = -1
        self.devstatusprint = False
        self.all_flags = flaghandler.completeFlagList
        self.freeIndex = 0

    def __str__(self):
        return f"GameHandler Status: Game Mode {self.gamemode}; Round {self.round}; Score {self.score}; Lives {self.lives}; Streak {self.streak}; DevPrint {self.devstatusprint}."

    # call next round
    def nextround(self):
        if self.devstatusprint:
            print("Current Round", self.round)

        gui.display_round(self.round)

        # pick a random  flag, remove from remaining set
        self.current_flag = random.choice(list(self.remaining_flags))
        self.remaining_flags.remove(self.current_flag)
        self.current_flag = self.current_flag[:-4]

        # start timer if needed
        if self.gamemode == 1:
            gui.displayTimer()
            timerlogic.clock.runClassicTimer()

        # ask to update GUI
        self.updateGUI()

    # if new game is launched while old one still running (or window is destroyed), ask to record previous to history
    def terminatedGame(self):
        if self.gamemode >= 0:
            history.terminated(
                [self.gamemode, self.score, self.highestStreak, self.lives])

    # reset counters
    def reset(self, desiredLives: int):
        self.terminatedGame()

        self.remaining_flags = set(self.all_flags)
        self.round = 1
        self.score = 0
        self.streak = 0
        self.highestStreak = 0
        self.lives = desiredLives

        gui.display_score(self.score)
        gui.displayStreak(self.streak)
        gui.displayLives(self.lives)
        gui.display_round(self.round)

    # initialize classic game mode
    def classic(self):
        print("Launching Classic Game...")
        gui.change_title("Classic")
        history.gameStart("Classic")

        self.reset(3)
        self.gamemode = 0

        print("Game Start!")
        gui.historyUpdate()
        self.nextround()

    # initialize advanced game mode
    def advanced(self):
        print("Launching Advanced Game...")
        gui.change_title("Advanced")
        history.gameStart("Advanced")

        self.reset(3)
        self.gamemode = 1

        print("Game Start!")
        gui.historyUpdate()
        self.nextround()

    # initialize free game mode
    def free(self):
        print("Launching Free Game...")
        gui.change_title("Free Mode")
        history.gameStart("Free")

        self.reset(-1)
        self.gamemode = 4

        print("Game Start!")
        gui.historyUpdate()
        self.nextround()

    def playerAnswered(self, btn: int):
        # if no game yet launched, skip function
        if self.gamemode == -1:
            return

        # debug option
        elif self.gamemode == -2:
            self.flagSlideShow()
            return

        # check if answer was correct
        if self.buttons[btn] == self.current_flag.upper().replace("_", " "):
            self.streak += 1

            if self.streak > self.highestStreak:
                self.highestStreak = self.streak

            # change score depending on the game mode
            # classic score
            if self.gamemode == 0:
                self.score += 100

            # advanced score
            elif self.gamemode == 1:
                roundtime = timerlogic.clock.readAccurate()

                if roundtime < 5:
                    pointsGained = 100 + (20 * (5 - roundtime))

                else:
                    pointsGained = 100

                pointsGained = pointsGained * (((1 / -self.streak) + 2) ** 1.5)
                self.score += int(pointsGained)

            # free game mode
            elif self.gamemode == 4:
                self.score += 100

            # developer print
            if self.devstatusprint:
                print("Correct! You have answered",
                      self.streak, "times correct in a row!")

        # wrong answer handling
        else:
            self.lives -= 1
            self.streak = 0

            if self.devstatusprint:
                print("Wrong!", self.lives, "lives remaining.")

        if self.devstatusprint:
            print("Current score:", self.score)

        # round is over, update game status for player
        gui.display_score(self.score)
        gui.displayStreak(self.streak)
        gui.displayLives(self.lives)

        # check if game is over, ask to record history
        if self.lives == 0:
            history.gameOver([self.gamemode, self.score, self.highestStreak])
            gui.change_title("Flag Game")
            self.gamemode = -1

            if self.devstatusprint:
                print(
                    "Game over, you're out of lives! Start new game from File > New game.")

            gui.historyUpdate()

        # launch next round
        else:
            self.round += 1
            self.nextround()

    def updateGUI(self):
        # read new flag
        flagPath = flaghandler.flagdir
        photoPath = flagPath + '/' + self.current_flag + ".png"

        # update displayed flag to player
        gui.nextflag(photoPath)

        # generate 4 options with 3 dummies
        self.buttons = [self.current_flag.upper().replace("_", " ")]
        picked = [self.current_flag]

        for _ in range(3):
            wrong_answer = self.current_flag

            while wrong_answer == self.current_flag or wrong_answer in picked:
                wrong_answer = random.choice(self.all_flags)
                wrong_answer = wrong_answer[:-4]

            picked.append(wrong_answer)
            self.buttons.append(wrong_answer.upper().replace("_", " "))

        # shuffle buttons
        random.shuffle(self.buttons)

        if self.devstatusprint:
            print("Generated options", self.buttons, "out of which",
                  self.current_flag.upper().replace("_", " "), "is correct.")

        # update displayed buttons to player
        gui.nextbuttons(self.buttons)

    # debugging to scroll through every flag
    def flagSlideShow(self):
        self.gamemode = -2
        flagPath = flaghandler.flagdir

        curr_flag = self.all_flags[self.freeIndex]
        photoPath = flagPath + '/' + curr_flag

        gui.nextflag(photoPath)
        self.freeIndex += 1

        if self.freeIndex == len(self.all_flags) - 1:
            self.freeIndex == 0

        self.buttons = ["NEXT FLAG", "NEXT FLAG", "NEXT FLAG", "NEXT FLAG"]

        gui.nextbuttons(self.buttons)


masterGameHandler = GameHandler()
