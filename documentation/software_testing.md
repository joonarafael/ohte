# SOFTWARE TESTING

Basic software logic has been rigorously tested with automated testing and wider software functionality, including e.g. software installation and graphical user interface performance, has been manually checked.

All personal player logs (e.g. game history & statistics) are copied to a backup directory before any software testing is executed for safety reasons. This action is done by the `tasks.py` module, and more specifically, performed by the `shutil` library. No matter if the testing sequence is succesful or not (e.g. halts due to an error), player logs will be copied back from these backups.

As the core game logic deals simultaneously with some GUI elements, the `MagicMock` library from `unittest.mock` is utilized to simulate e.g. the [`Stats`](../flaggame/src/gui_elements/gui_stats.py) class from the graphical user interface. Similarly the `exit()` calls within the game source code are ignored with the help of `builtins` and `patch` libraries.

## AUTOMATED TEST MODULES

All automated test modules are located [here](../flaggame/src/tests/). Short descriptions of the test modules are provided down below:

### GAMEHANDLER_TEST

The [GameHandler](../flaggame/src/tests/a_gamehandler_test.py) test module performs a wide range of tests assessing the core game logic. These tests include, for example, the launching of game modes, cancelling a game, and rewarding the player with a correct amount of points. It also checks e.g. if Time Trial games are cancelled after a 5 second round time.

### FLAGHANDLER_TEST

The [FlagHandler](../flaggame/src/tests/b_flaghandler_test.py) test module performs some tests assessing the logic responsible for the flag image importing. These tests include, for example, what happens if flags cannot be imported, or if the [reference document](../flaggame/src/logs/correctflags.txt) listing the correct files is missing.

### TIMERLOGIC_TEST

The [TimerLogic](../flaggame/src/tests/c_timerlogic_test.py) test module performs a couple of tests assessing the timer logic. These tests include, for example, how the timer returns different decimal place values.

### HISTORY_TEST

The [History](../flaggame/src/tests/d_history_test.py) test module performs multiple tests assessing the logic responsible for game history managing. These tests include, for example, how the software creates new files if old ones cannot be found, or what text is written to file when a game is terminated. It also checks that e.g. the history is correctly erased when requested.

### CSVHANDLER_TEST

The [CSVHandler](../flaggame/src/tests/e_csvhandler_test.py) test module performs a lot of tests assessing the logic responsible for game statistics recording. These tests include, for example, how the data files are written and handled, how the software calculates the player lifelong statistics, and whether it avoids all zero division errors. It also checks that e.g. the statistics are correctly erased when requested.

### RULES_TEST

The [Rules](../flaggame/src/tests/f_rules_test.py) test module performs a few tests assessing the logic reading the [rulebook](../flaggame/src/logs/gamerules.txt). These tests include, for example, how the software acts if no rulebook can be found, or if the rulebook row count is not the expected (70).

## TEST COVERAGE

The automated pytest covers around 95% of the software source code excluding all [graphical user interface modules](../flaggame/src/gui_elements/) along with `gui.py`. It also ignores the `main.py` module.

<img src="./images/coverage_report.png">

## SOFTWARE BUILD & GRAPHICAL USER INTERFACE

Software installation and graphical user interface functionality has been checked manually.

### INSTALLATION

Software installation has been tried on Horizon virtual desktop and on school laptop (both Cubbli environments). **Software has not been tested on a MacOS machine**.

Along with the basic installation procedure, different execution order of invoke tasks has been also tested (error handling within `tasks.py`). Previously the execution halted if no player logs yet existed when pytests were launched.

### GRAPHICAL USER INTERFACE

The overall functionality and appearance of the graphical user interface has been manually checked and verified to be working as intended. Every game mode has been tested with multiple different inputs to ensure all error handling is working properly.  All core functionality from [Software Requirements Specification](requirements_specification.md) has been tested.

## REMAINING QUALITY CONCERNS

Software does not handle well situations where it lacks the proper read/write permissions to e.g. flag source directories or existing player statistics files.

History doesn't pick up the change of date during software execution (e.g. software launched at 23:57 and session lasts for more than 3 minutes). This could be addressed better to get a more accurate history logbook.

For more information regarding source code quality, see [remaining issues with source code quality](./architecture.md#remaining-issues-with-source-code-quality--software-logic).
