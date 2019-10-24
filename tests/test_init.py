from click.testing import CliRunner
from ginpar import cli


def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init", "-q"])
        assert result.exit_code == 0
        assert "Done" in result.output
