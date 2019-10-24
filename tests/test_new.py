import os

from click.testing import CliRunner
from ginpar import cli

def test_new():
    """New works properly on the default scenario.

    Default scenario is when the directory of the new sketch doesn't
    exist in the source_path..
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        ## Initialize a new project and cd it
        runner.invoke(cli, ["init", "-q"])
        os.chdir("my-site")

        result = runner.invoke(cli, ["new", "test"])
        
        data_path = os.path.join("sketches", "test", "data.yaml")
        sketch_path = os.path.join("sketches", "test", "sketch.js")
        assert result.exit_code == 0
        assert os.path.isfile(data_path)
        assert os.path.isfile(sketch_path)
       

def test_new_existent():
    """New works properly when the sketch already exists
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        ## Initialize a new project and cd it
        runner.invoke(cli, ["init", "-q"])
        os.chdir("my-site")
        
        ## Create test
        runner.invoke(cli, ["new", "test"])

        result = runner.invoke(cli, ["new", "test"])
        assert result.exit_code == 1
       