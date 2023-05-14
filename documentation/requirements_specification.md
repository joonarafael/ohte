# Software Requirements Specification

## Main Goal & Usage

The Software is a casual one-player flag quiz game. It is intended to include every national flag and support a few different game modes.

## Software Core Functionality & Interface

- [x] Main langauge: Python.
- [x] Utilize the Tkinter library for graphics.
- [x] Keep track of high scores and previous games in a separate history file stored on disk.
- [x] Game should be played with mouse pointer.
- [x] Game includes only one "Classic" game mode first.
- [x] Additional features and game modes are added in the future.

## Future Ideas & Game Modes to Implement

After the main functionalities and the core application is up and running, these are the future ideas and game modes to be included in the game:

- [x] Advanced Mode: Complex pointing system to give points for quick time and running streaks. Three lives.
- [x] Free Mode: Unlimited lives & time to practice purposes
- [x] Time Trial: Three lives with continious time pressure, game ends if time runs out
- [x] One Life: Just one life but unlimited time
- [ ] Custom Mode: Player can determine the game settings self
- [x] Player Lifetime Statistics: Keep track of lifetime statistics, amount of games, accuracy, etc. ...

## Custom Mode

**Custom Mode was never added to the game** as time run out. It was not an easy task to implement this feature given the poor architecture of the core game logic. The 5 different game modes currently in the game are *hard coded* into the actual source code which makes any change/fix extremely difficult. If I'd do this now from the beginning, I'd create some kind of config files for the game modes out of which the game logic could read the game mode properties. For the custom game, player would just modify an additional config file located on disk.