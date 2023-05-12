# SOFTWARE TESTING

Software has been rigorously tested with automated testing. Wider software functionality including e.g. software installation and graphical user interface performance has been manually checked.

Even though tests are written to avoid modifying the personal player logs (e.g. game history & statistics), all logs are copied to a backup directory before any software testing is committed for safety reasons. This action is done by the `tasks.py` module performed by the `shutil` library. No matter if the testing sequence is succesfull or not (e.g. halts due to an error), player logs will be copied back from these backups.

As the core game logic deals simultaneously with some GUI elements, the `MagicMock` library from `unittest.mock` is utilized to simulate e.g. the Statistics page from the graphical user interface. Similarly the `exit()` calls within the game source code are ignored with the help of `builtins` and `patch` libraries.

## TEST MODULES

All test modules can be found [here](../flaggame/src/tests/).

### GAMEHANDLER_TEST

The [GameHandler](../flaggame/src/tests/a_gamehandler_test.py) test module performs a wide range of tests assessing the core game logic. These tests include, for example, the launching of game modes, cancelling a game, and rewarding the player with a correct amount of points. It also checks e.g. if Time Trial games are cancelled after a 5 second round time.

### FLAGHANDLER_TEST

The [FlagHandler](../flaggame/src/tests/b_flaghandler_test.py) test module performs some tests assessing the logic responsible of the flag image importing. These tests include, for example, what happens if flags cannot be imported of if the [reference document](../flaggame/src/logs/correctflags.txt) listing the correct files is missing.

### TIMERLOGIC_TEST

The [TimerLogic](../flaggame/src/tests/c_timerlogic_test.py) test module performs a couple of tests assessing the timer logic. These tests include, for example, how the timer returns different decimal-point values.

### HISTORY_TEST

The [History](../flaggame/src/tests/d_history_test.py) test module performs mupltiple tests assessing the logic responsible for game history managing. These tests include, for example, how the software creates new files if old ones can't be found or what text is written to file when a game is terminated. It also checks that e.g. the history is correctly erased when requested.

### CSVHANDLER_TEST

The [CSVHandler](../flaggame/src/tests/e_csvhandler_test.py) test module performs a lot of tests assessing the logic responsible for game statistics recording. These tests include, for example, how the data files are written and handled, how the software calculates the player lifelong statistics, and whether it avoids all zero division errors. It also checks that e.g. the statistics are correctly erased when requested.

### RULES_TEST

The [Rules](../flaggame/src/tests/f_rules_test.py) test module performs a few tests assessing the logic reading the rulebook. These tests include, for example, how the software acts if no rulebook can be found, or if the rulebook row count is not the expected.

## 