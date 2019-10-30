import os

from click.testing import CliRunner

from ginpar import cli


def test_quickstart():
    """Quickstart works properly on the default scenario.

    Default scenario is when the directory of the quickstart project doesn't
    exist in the current path: `./quickstart`.
    This also doesn't need to send the force flag.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["quickstart"])
        assert result.exit_code == 0
        assert "The Ginpar sample site is ready." in result.output


def test_quickstart_existent_path():
    """Quickstart works properly when `./quickstart` exists.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("quickstart")
        file_path = os.path.join("quickstart", "a.txt")

        with open(file_path, "w+") as f:
            f.write("a")

        result = runner.invoke(cli, ["quickstart"])
        assert result.exit_code == 1


def test_quickstart_existent_path_force():
    """Quickstart works properly when `./quickstart` exists and --force
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("quickstart")
        file_path = os.path.join("quickstart", "a.txt")

        with open(file_path, "w+") as f:
            f.write("a")

        result = runner.invoke(cli, ["quickstart", "--force"])
        assert result.exit_code == 0


def test_quickstart_removes_git_files():
    """Quickstart removes git files after cloning

    Check for the existence of any file that starts with `.git`.
    This will report the existent files.
    """
    import os

    runner = CliRunner()
    with runner.isolated_filesystem():
        git_files = []
        runner.invoke(cli, ["quickstart"])
        for _, d, f in os.walk("quickstart"):
            for name in d:
                if name.startswith(".git"):
                    git_files.append(name)
            for file in f:
                if file.startswith(".git"):
                    git_files.append(file)

        assert ".git" not in git_files
