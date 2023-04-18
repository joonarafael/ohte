# FLAG QUIZ GAME

current ver **0.2.1** (*18.4.2023*)

## DOCUMENTATION

(suoritan kurssia suomeksi mutta dokumentaatio on englanniksi)

- [Software Requirements Specification](./documentation/requirements_specification.md)

- [Software Architecture Layout](./documentation/architecture.md)

- [Changelog](./documentation/changelog.md)

- [Working Hours Record](./documentation/working_hours_record.md)

- [Game Rules](./flaggame/src/gamerules.txt)

## VERSIONS

Flag Quiz Game has been built with **Python 3.10** and **Poetry 1.4.0**. Software might not run on other versions. Installation guide provides possible solutions for two common errors encountered with other Poetry versions.

## INSTALLATION GUIDE

### 1. Clone this github repository to your local machine by executing:

```bash
git clone https://github.com/joonarafael/ohte.git
```

### 2. Navigate to `./flaggame/`.

This folder is the root folder for the Poetry project. Not the github repository `/ohte/` folder.

### 3. Resolve Poetry dependencies by executing:

```bash
poetry install
```

### TROUBLESHOOTING SOME POSSIBLE POETRY ERRORS

**PROBLEM A**: *The Poetry configuration is invalid: Additional properties are not allowed ('group' was unexpected)*

**SOLUTION A**: Manually edit the `pyproject.toml` at `./flaggame/pyproject.toml` by moving all "dev dependencies" to the regular group. You may also just remove them altogether if you don't need developer dependencies (e.g. pylint and pytest).

**PROBLEM B**: *The lock file is not compatible with the current version of Poetry. Upgrade Poetry to be able to read the lock file or, alternatively, regenerate the lock file with the `poetry lock` command.*

**SOLUTION B**: Your Poetry installation is too old/new. Lock file has been generated with Poetry version 1.4.0. You could try to match your Poetry version, but this issue can also be resolved by first removing `poetry.lock` file entirely, and then regenerating it again by executing:

```bash
poetry lock --no-update
```

This command regenerates a new working `poetry.lock` file for your system without changing the actual dependencies and their corresponding versions within the `pyproject.toml`.

### 4. Run the game in Poetry project master folder `./flaggame/` by executing:

```bash
poetry run invoke start
```

## PYTEST, PYLINT & COVERAGE

Pytest ignores `main` and `gui` modules. Main module is almost empty (only dodging the cirular import error), and `gui` is responsible for the graphical interface:

```bash
poetry run invoke test
```

To generate the Pytest coverage report (web browser version) for your local machine, execute:

```bash
poetry run invoke coverage-report
```

To run the code review algorithm with parameters defined in [pylintrc](./flaggame/.pylintrc), execute:

```bash
poetry run invoke lint
```
