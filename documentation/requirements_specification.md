# Software Requirements Specification

## Main Goal & Usage

The Software is a casual one-player flag quiz game. It is intended to include every national flag and support a few different game modes.

## Software Core Functionality & Interface

- Main langauge: Python.
- Utilize the Tkinter library for graphics.
- Keep track of high scores and previous games in a separate history file stored on disk.
- Game should be played with mouse pointer.
- Game includes only one "Classic" game mode first.
- Additional features and game modes are added in the future.

## Main Concerns

- Dependency on graphical interface, game is completely unplayable without a working UI. However, software testing should not pose any issues as game core functionality can still be tested with Pytest.
- Amount of data (approx. 200 pictures of flags).

## Future Ideas & Game Modes to Implement

After the main functionalities and the core application is up and running, these are the future ideas and game modes to be included in the game:

- Advanced Mode: Complex pointing system to give points for quick time and running streaks. Three lives.
- Free Mode: Unlimited lives & time to practice purposes
- Time Trial: Three lives with continious time pressure, game ends if time runs out.
- One Life: Just one life but unlimited time
- Custom Mode: Player can determine the game settings self
