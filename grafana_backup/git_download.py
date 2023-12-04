import io
import os
import tarfile
from git import Repo

def archive(source_dir):
    # Create a BytesIO object to store the tar file in memory
    tar_buffer = io.BytesIO()

    # Create a tar file in memory
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        # Walk through the source directory and add all files and subdirectories
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                tar.add(file_path, arcname=arcname)

    # Reset the buffer position to the beginning
    tar_buffer.seek(0)
    return tar_buffer


def main(args, settings):
    repo_url = settings.get('GIT_REPO_URL')
    git_ref = settings.get('GIT_REPO_REF', 'HEAD')
    backup_dir = settings.get('BACKUP_DIR')

    try:
        if os.path.isdir(backup_dir):
            repo = Repo(backup_dir)
            repo.git.checkout(git_ref)
            repo.git.pull()
        else:
            repo = Repo.clone_from(repo_url, backup_dir, branch=git_ref)
            # try:
            # except :
            #     repo = Repo.init(backup_dir, initial_branch=git_ref)
        buffer = archive(backup_dir)
        return buffer
    except Exception as e:
        print("Exception: {0}".format(str(e)))
        return False
