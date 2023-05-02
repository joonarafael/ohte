# FLAG QUIZ GAME

current ver **0.2.5** (*2.5.2023*)

POSSIBLE ISSUES WITH COVERAGE! SEE [KNOWN COVERAGE ISSUES](./README.md#software-testing-with-pytest--coverage).

## DOCUMENTATION

(suoritan kurssia suomeksi mutta dokumentaatio on englanniksi)

- [Software Requirements Specification](./documentation/requirements_specification.md)

- [Software Architecture Layout](./documentation/architecture.md)

- [Changelog](./documentation/changelog.md)

- [Working Hours Record](./documentation/working_hours_record.md)

- [Game Rules](./flaggame/src/gamerules.txt)

## VERSIONS

Flag Quiz Game has been built with **Python 3.10** and **Poetry 1.4.0**. Software might not run on other versions. Installation guide [provides possible solutions](./README.md#troubleshooting-some-possible-poetry-errors) for two common errors encountered with other Poetry versions.

## INSTALLATION GUIDE

### 1. Clone this Github repository to your local machine by executing:

```bash
git clone https://github.com/joonarafael/ohte.git
```

### 2. Navigate to `./flaggame`.

This folder is the root folder for the Poetry project. Not the github repository master folder `/ohte`.

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

## SOFTWARE TESTING WITH PYTEST & COVERAGE

Run the pytest ignoring `main` and all graphical user interface modules by executing:

```bash
poetry run invoke test
```

The test will take approximately 38 seconds. It is checking how the pointing mechanisms and statistics calculations work with different round times.

**The automate Coverage report is currently** (2.5.2023 with Flag Game 0.2.5) **providing some inconsistent results on some runs**. *Sometimes* the coverage report states, for example, that not all print statements are executed within the flaghandler module, although the tests do actually test this functionality and do pass successfully. Please study the provided Coverage report thoroughly and check especially details about flaghandler and gamehandler modules. To generate this Coverage report (web browser version) for your local machine, execute:

```bash
poetry run invoke coverage-report
```

## PYLINT AUTOMATED CODE REVIEW

To run the automated code review algorithm with parameters defined in [pylintrc](./flaggame/.pylintrc), execute:

```bash
poetry run invoke lint
```
