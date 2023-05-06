import shutil
from invoke import task

# let us utilize the shutil library and take backups of the log files to ensure integrity of player game history & statistics

def create_backups():
    print("Creating backups of player log files...")

    logs_dir = "src/logs"
    empty_dir = "src/logs/empty"
    backup_dir = "src/logs/backup"

    try:
        shutil.copy(f"{logs_dir}/history.txt", f"{backup_dir}/history_backup.txt")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/history_empty.txt", f"{backup_dir}/history_backup.txt")

    try:
        shutil.copy(f"{logs_dir}/rounds.csv", f"{backup_dir}/rounds_backup.csv")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/rounds_empty.csv", f"{backup_dir}/rounds_backup.csv")
    
    try:
        shutil.copy(f"{logs_dir}/stats.csv", f"{backup_dir}/stats_backup.csv")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/stats_empty.csv", f"{backup_dir}/stats_backup.csv")

    try:
        shutil.copy(f"{logs_dir}/streaks.csv", f"{backup_dir}/streaks_backup.csv")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/streaks_empty.csv", f"{backup_dir}/streaks_backup.csv")

def restore_backups():
    print("Restoring player logs from backup files...")

    logs_dir = "src/logs"
    empty_dir = "src/logs/empty"
    backup_dir = "src/logs/backup"

    try:
        shutil.copy(f"{backup_dir}/history_backup.txt", f"{logs_dir}/history.txt")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/history_empty.txt", f"{logs_dir}/history.txt")

    try:
        shutil.copy(f"{backup_dir}/rounds_backup.csv", f"{logs_dir}/rounds.csv")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/rounds_empty.csv", f"{logs_dir}/rounds.csv")
    
    try:
        shutil.copy(f"{backup_dir}/stats_backup.csv", f"{logs_dir}/stats.csv")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/stats_empty.csv", f"{logs_dir}/stats.csv")

    try:
        shutil.copy(f"{backup_dir}/streaks_backup.csv", f"{logs_dir}/streaks.csv")
    
    except FileNotFoundError:
        shutil.copy(f"{empty_dir}/streaks_empty.csv", f"{logs_dir}/streaks.csv")


@task
def start(ctx):
    ctx.run("python3 src/main.py", pty=True)

@task
def test(ctx):
    print("EXPECTED test RUNTIME: 38 s.")
    create_backups()

    try:
        ctx.run("pytest src", pty=True)
        restore_backups()
    
    except:
        restore_backups()

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task
def coverage(ctx):
    print("EXPECTED coverage RUNTIME: 38 s.")
    create_backups()

    try:
        ctx.run("coverage run --branch -m pytest src", pty=True)
        restore_backups()
    
    except:
        restore_backups()

@task
def coverage_report(ctx):
    print("EXPECTED coverage-report RUNTIME: 38 s.")
    create_backups()

    try:
        ctx.run("coverage run --branch -m pytest src", pty=True)
        ctx.run("coverage html", pty=True)
        restore_backups()
    
    except:
        restore_backups()
