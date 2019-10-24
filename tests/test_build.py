import os

from click.testing import CliRunner
from ginpar import cli


def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a project with default values
        runner.invoke(cli, ["init", "-q"])
        # => Creates a path "my-site/"

        # Change directories
        os.chdir("my-site")

        result = runner.invoke(cli, ["build"])
        assert result.exit_code == 0
