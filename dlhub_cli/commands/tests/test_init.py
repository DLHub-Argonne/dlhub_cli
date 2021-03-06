import os
import pytest
from click.testing import CliRunner
from dlhub_cli.commands.init import init_cmd


@pytest.fixture
def runner():
    return CliRunner()


def test_init_overwrite(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(init_cmd, ['--name', 'test'])
        assert result.exit_code == 0
        assert os.path.isfile('describe_servable.py')
        with open('describe_servable.py') as fp:
            assert 'set_name("test")' in fp.read()

        # Make sure it tests a user that overwriting is not default
        with open('describe_servable.py', 'w') as fp:
            fp.write("Hello!")
        result = runner.invoke(init_cmd, ['--name', 'test'])
        assert "Use --force to overwrite" in result.output
        with open('describe_servable.py', 'r') as fp:
            assert fp.read() == 'Hello!'

        # Workaround: Naming the file something else
        runner.invoke(init_cmd, ['--name', 'test', '--filename', 'test.py'])
        assert os.path.isfile('test.py')

        # Workaround: Forcing overwrite
        result = runner.invoke(init_cmd, ['--name', 'test', '--force'])
        assert result.exit_code == 0
        with open('describe_servable.py', 'r') as fp:
            assert fp.read() != 'Hello!'


def test_authors(runner):
    with runner.isolated_filesystem():
        # Adding authors to the initial description
        result = runner.invoke(init_cmd, ['--name', 'test', '--force',
                                          '--author', 'Ward, Logan', 'Argonne National Laboratory'])
        assert result.exit_code == 0
        with open('describe_servable.py', 'r') as fp:
            assert 'Ward, Logan' in fp.read()

    with runner.isolated_filesystem():
        # Make sure that it throws errors if we do not provide in Last, First
        result = runner.invoke(init_cmd, ['--name', 'test', '--force',
                                          '--author', 'Logan Ward', 'Argonne National Laboratory'])
        assert result.exit_code > 0
        assert "must be listed as" in result.output


def test_title(runner):
    with runner.isolated_filesystem():
        # Add a title to the output
        result = runner.invoke(init_cmd, ['--name', 'test', '--force',
                                          '--author', 'Ward, Logan', 'Argonne National Laboratory',
                                          '--title', 'Test case for py.test'])
        assert result.exit_code == 0
        with open('describe_servable.py', 'r') as fp:
            assert 'Test case for py.test' in fp.read()


def test_run_after(runner):
    with runner.isolated_filesystem():
        # Make sure it runs the script at the end of the generation
        result = runner.invoke(init_cmd, ['--name', 'test'])
        assert result.exit_code == 0
        assert os.path.isfile('dlhub.json')

    with runner.isolated_filesystem():
        # Make sure it doesn't runs at the end of the code
        result = runner.invoke(init_cmd, ['--name', 'test', '--skip-run'])
        assert result.exit_code == 0
        assert not os.path.isfile('dlhub.json')
