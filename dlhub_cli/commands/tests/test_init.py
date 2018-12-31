import os
from click.testing import CliRunner
from dlhub_cli.commands.init import init_cmd


def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Run basic command
        runner.invoke(init_cmd)
        assert os.path.isfile('describe_model.py')

        # Make sure it tests a user that overwriting is not default
        with open('describe_model.py', 'w') as fp:
            fp.write("Hello!")
        result = runner.invoke(init_cmd)
        assert "Use --force to overwrite" in result.output
        with open('describe_model.py', 'r') as fp:
            assert fp.read() == 'Hello!'

        # Workaround: Naming the file something else
        runner.invoke(init_cmd, ['--name', 'test.py'])
        assert os.path.isfile('test.py')

        # Workaround: Forcing overwrite
        result = runner.invoke(init_cmd, ['--force'])
        assert result.exit_code == 0
        with open('describe_model.py', 'r') as fp:
            assert fp.read() != 'Hello!'
