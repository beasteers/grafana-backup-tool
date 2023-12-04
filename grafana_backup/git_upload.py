import os
from git import Repo


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')

    try:
        repo = Repo(backup_dir)
        repo.git.add(all=True)
        repo.git.commit('-m', f'Backup at {timestamp}')
        repo.git.push()
    except Exception as e:
        print("Exception: {0}".format(str(e)))
        return False
    return True
