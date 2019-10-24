import os

from click.testing import CliRunner
from ginpar import cli

def test_serve():
  runner = CliRunner()
  with runner.isolated_filesystem():
      runner.invoke(cli, ["init", "-q"])
      os.chdir("my-site")
      result = runner.invoke(cli, ["serve", "--help"])
      assert result.exit_code == 0
  