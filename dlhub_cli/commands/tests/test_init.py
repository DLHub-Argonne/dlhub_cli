import os
from click.testing import CliRunner
from dlhub_cli.commands.init import init_cmd


def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Run basic command
        result = runner.invoke(init_cmd, ['--name', 'test'])
        print(result.output)
        assert os.path.isfile('describe_model.py')
        with open('describe_model.py') as fp:
            assert 'set_name("test")' in fp.read()

        # Make sure it tests a user that overwriting is not default
        with open('describe_model.py', 'w') as fp:
            fp.write("Hello!")
        result = runner.invoke(init_cmd, ['--name', 'test'])
        assert "Use --force to overwrite" in result.output
        with open('describe_model.py', 'r') as fp:
            assert fp.read() == 'Hello!'

        # Workaround: Naming the file something else
        runner.invoke(init_cmd, ['--name', 'test', '--filename', 'test.py'])
        assert os.path.isfile('test.py')

        # Workaround: Forcing overwrite
        result = runner.invoke(init_cmd, ['--name', 'test', '--force'])
        assert result.exit_code == 0
        with open('describe_model.py', 'r') as fp:
            assert fp.read() != 'Hello!'

        # Adding authors to the initial description
        result = runner.invoke(init_cmd, ['--name', 'test', '--force',
                                          '--author', 'Ward, Logan', 'Argonne National Laboratory'])
        assert result.exit_code == 0
        with open('describe_model.py', 'r') as fp:
            assert 'Ward, Logan' in fp.read()

        # Make sure that it throws errors if we do not provide in Last, First
        result = runner.invoke(init_cmd, ['--name', 'test', '--force',
                                          '--author', 'Logan Ward', 'Argonne National Laboratory'])
        assert result.exit_code > 0
        assert "must be listed as" in result.output

        # Add a title to the output
        result = runner.invoke(init_cmd, ['--name', 'test', '--force',
                                          '--author', 'Ward, Logan', 'Argonne National Laboratory',
                                          '--title', 'Test case for py.test'])
        assert result.exit_code == 0
        with open('describe_model.py', 'r') as fp:
            assert 'Test case for py.test' in fp.read()

