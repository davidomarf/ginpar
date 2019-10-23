from click.testing import CliRunner
from ginpar import cli

def test_quickstart():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["quickstart"])
        assert result.exit_code == 0
        assert "Success" in result.output

def test_quickstart_force():
  runner = CliRunner()
  with runner.isolated_filesystem():
      result = runner.invoke(cli, ["quickstart", "-f"])
      assert result.exit_code == 0
      assert "Success" in result.output