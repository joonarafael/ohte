# FLAG QUIZ GAME

current ver **0.2.65** (*8.5.2023*)

## DOCUMENTATION

(suoritan kurssia suomeksi mutta dokumentaatio on englanniksi)

- [User Manual](./documentation/user_manual.md)

- [Software Requirements Specification](./documentation/requirements_specification.md)

- [Software Repository Architecture](./documentation/architecture.md)

- [Changelog](./documentation/changelog.md)

- [Working Hours Record](./documentation/working_hours_record.md)

## VERSIONS

Flag Quiz Game has been built with **Python 3.10** and **Poetry 1.4.0**. Software might not run on other versions. Installation guide [provides possible solutions](./README.md#troubleshooting-some-possible-poetry-errors) for two common errors encountered with other Poetry versions. A solution for the SQLite error: `database is locked`, is also provied [down below](./README.md#software-test-coverage-report).

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

**SOLUTION A**: Manually edit the `pyproject.toml` at `./flaggame/pyproject.toml` by moving all developer dependencies to the "regular" group. You may also just remove them altogether if you don't need developer dependencies (e.g. pylint and pytest).

```bash
nano pyproject.toml
```

**PROBLEM B**: *The lock file is not compatible with the current version of Poetry. Upgrade Poetry to be able to read the lock file or, alternatively, regenerate the lock file with the poetry lock command.*

**SOLUTION B**: Your Poetry installation is too old/new. The original lock file has been generated with Poetry version 1.4.0. You could try to match your Poetry version, but this issue can also be resolved by first removing `poetry.lock` file at `./flaggame/poetry.lock` entirely, and then regenerating it again by executing:

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

## SOFTWARE TESTING WITH PYTEST

Run the tests ignoring all graphical user interface modules by executing:

```bash
poetry run invoke test
```

The tests will take approximately 38 seconds. It is checking how the points rewarding algorithms and statistics calculations work with different round times.

## SOFTWARE TEST COVERAGE REPORT

To generate the Coverage report (web browser version) for your local machine, execute:

```bash
poetry run invoke coverage-report
```

Please note: if running the Coverage tool on a Horizon virtual desktop, execution might halt to a SQLite error: `database is locked`. This is due to the insufficient speed of the virtual disk (see [this page](https://ohjelmistotekniikka-hy.github.io/python/toteutus#sqlite-tietokanta-lukkiutuminen-virtuaality%C3%B6asemalla) for details). To fix this issue, the whole repository needs to be cloned in to the `/tmp` system folder for execution. Move to this folder with `cd /tmp` and follow the instructions from the [beginning](./README.md#installation-guide) again.

## PYLINT AUTOMATED CODE REVIEW

To run the automated code review algorithm with parameters defined in [pylintrc](./flaggame/.pylintrc), execute:

```bash
poetry run invoke lint
```
