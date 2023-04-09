# FLAG QUIZ GAME

current ver 0.1.4 (2.4.2023)
built with python3 poetry

## IMPORTANT NOTICES ABOUT INSTALLATION

- My current build (0.1.6) is running fine on an Oracle VirtualBox Ubuntu installation and Cubbli laptop provided by the school.

- When run through the VMware Horizon, poetry fails due to the "dev" group in pyproject.toml. If this error occurs, move all dependencies from the dev group to the "regular" group. This resolved the issue for me and I was able to run the flag quiz game on an Cubbli 20 virtual desktop.

- Additionally the 2to3 library has been added to the poetry developer dependicies due to weird errors I run into with autopep8.
