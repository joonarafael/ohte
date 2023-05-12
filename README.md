# FLAG QUIZ GAME

current ver **0.2.7** (*12.5.2023*)

## DOCUMENTATION

(suoritan kurssia suomeksi mutta dokumentaatio on englanniksi)

- [User Manual](./documentation/user_manual.md)

- [Software Requirements Specification](./documentation/requirements_specification.md)

- [Software Architecture](./documentation/architecture.md)

- [Changelog](./documentation/changelog.md)

- [Software Testing Document](./documentation/software_testing.md)

## VERSIONS

Flag Quiz Game has been built with **Python 3.10** and **Poetry 1.4.0**. Software might not run on other versions. Installation guide [provides some possible solutions](./README.md#troubleshooting-some-possible-poetry-errors) for two common errors encountered with other Poetry versions. A solution for the SQLite error: `database is locked`, is also provied [down below](./README.md#software-test-coverage-report).

## INSTALLATION GUIDE

### 1. Clone this Github repository to your local machine by executing:

```bash
git clone https://github.com/joonarafael/ohte.git
```

### 2. Navigate to `./flaggame`.

This folder is the root folder for the Poetry project. Not the Github repository "master folder".

### 3. Resolve Poetry dependencies by executing:

```bash
poetry install
```

### TROUBLESHOOTING SOME POSSIBLE POETRY ERRORS

**PROBLEM A**: *The Poetry configuration is invalid: Additional properties are not allowed ('group' was unexpected)*

**SOLUTION A**: This error occurs most likely due to mismatching Poetry editions. You can update your Poetry to 1.4.0 or alternatively manually edit the `pyproject.toml` at `./flaggame/pyproject.toml` by moving all developer dependencies to the "regular" group. You may also just remove them altogether if you don't need developer dependencies (e.g. pylint and pytest).

```bash
nano pyproject.toml
```

**PROBLEM B**: *The lock file is not compatible with the current version of Poetry. Upgrade Poetry to be able to read the lock file or, alternatively, regenerate the lock file with the poetry lock command.*

**SOLUTION B**: Your Poetry installation is too old/new. The original lock file has been generated with Poetry version 1.4.0. You can try to match your Poetry version, but this issue can also be resolved by first removing `poetry.lock` file at `./flaggame/poetry.lock` entirely, and then regenerating it again by executing:

```bash
rm -r poetry.lock
```

```bash
poetry lock --no-update
```

This command regenerates a new working `poetry.lock` file for your system without changing the actual dependencies and their corresponding versions within the `pyproject.toml`.

### 4. Run the game in Poetry project master folder `./flaggame` by executing:

```bash
poetry run invoke start
```

Complete user manual can be found [here](./documentation/user_manual.md). Complete rulebook for all game modes is located [here](./flaggame/src/logs/gamerules.txt).

## SOFTWARE TESTING WITH PYTEST

Run the tests ignoring all graphical user interface modules by executing:

```bash
poetry run invoke test
```

The config file for pytest can be found [here](./flaggame/pytest.ini) and all the source code for the tests is [here](./flaggame/src/tests/). The tests will take approximately 38 seconds. They are testing e.g. how the points awarding algorithms and statistics calculations work with different round times and scores. For a more complete document detailing all the software testing, read [Software Testing](./documentation/software_testing.md).

## SOFTWARE TEST COVERAGE REPORT

To generate the Coverage report (web browser version) for your local machine, execute:

```bash
poetry run invoke coverage-report
```

The generated report can be found at `./flaggame/htmlcov/index.html`.

Please note: if running the Coverage tool on a Horizon virtual desktop, execution might halt due to a SQLite error: `database is locked`. This is a direct consequence of the insufficient speed of the virtual disk (see [this page](https://ohjelmistotekniikka-hy.github.io/python/toteutus#sqlite-tietokanta-lukkiutuminen-virtuaality%C3%B6asemalla) for details). To fix this issue, the whole repository needs to be cloned in to the `/tmp` system folder for proper execution. Move to this folder with `cd /tmp` and follow the instructions from the [beginning](./README.md#installation-guide) again.

```bash
cd /tmp
```

## PYLINT AUTOMATED CODE REVIEW

To run the automated code review algorithm with parameters defined in [pylintrc](./flaggame/.pylintrc), execute:

```bash
poetry run invoke lint
```

To read my personal notes about pylint results and other comments regarding software source code quality, see [Software Architecture](./documentation/architecture.md#remaining-issues-with-source-code-quality--software-logic).
