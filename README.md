# FLAG QUIZ GAME

current ver 0.2.1 (17.4.2023)
built with python3 poetry

## INSTALLATION & RUNNING THE GAME

1. Clone this github repository to your local machine.

2. Navigate to /ohte/flaggame.

3. Resolve poetry dependicies by executing:

```bash
poetry install
```

4. Run the game from /ohte/flaggame by executing:

```bash
poetry run invoke start
```
5. Every machine has a local history file, thus history.txt in gitignore.

6. Pytests and pylint review can be executed with:

```bash
poetry run invoke test
```

and

```bash
poetry run invoke lint
```

## IMPORTANT NOTICES ABOUT INSTALLATION

- My current build (0.2.1) is running fine on an Oracle VirtualBox Ubuntu installation and Cubbli laptop provided by the school.

- Just running the game requires only the Pillow library (excluding built-ins like math, timeit, etc.). All other libraries are for dev group.

- 2to3 library has been added to the poetry dependicies due to weird errors I run into with autopep8.
