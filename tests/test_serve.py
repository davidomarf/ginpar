from click.testing import CliRunner
from ginpar import cli

def test_serve():
  runner = CliRunner()
  with runner.isolated_filesystem():
      result = runner.invoke(cli.serve)
      assert result.exit_code == 0
      assert "You're serving" in result.output
  