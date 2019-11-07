"""Git repository management inside Ginpar for themes and quickstart.
"""
import os
import subprocess

from ginpar.utils.echo import success, echo, error
from ginpar.utils.files import try_remove


def clone_repo(repo, path):
    """Clone the contents of a repository in a custom path

    Parameters
    ----------
    repo : str
        GitHub repository as in "{USER}/{REPO}"
    path : str
        Path to clone the repository to
    """

    repo_url = f"https://github.com/{repo}.git"

    echo(f"> Cloning {repo} in `{path}`")
    try:
        subprocess.call(["git", "clone", repo_url, path, "--quiet"])
    except OSError:
        error("You don't have git installed in your machine.")
        echo("Please install git and rerun or download the files manually:")
        echo(f"\t{repo_url}")
        return 1

    success(f"Successfully cloned {repo}.\n")
    return 0


def delete_git_files(path):
    """Delete the git files to only keep the relevant files

    Parameters
    ----------
    path : str
        Path to look for git files
    """

    echo("> Deleting .git files")
    try:
        print(os.path.join(path, ".git"))
        try_remove(os.path.join(path, ".git"))
        success("Successfully deleted .git files")
    except:
        error(f"Couldn't delete files. Delete all .git files manually in `{path}`")
        return 1

    return 0
