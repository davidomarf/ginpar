from click.testing import CliRunner
from ginpar import cli

def test_new():
  runner = CliRunner()
  result = runner.invoke(cli, ["new", 'hey'])
  assert result.exit_code == 0
  assert "You're in new" in result.output