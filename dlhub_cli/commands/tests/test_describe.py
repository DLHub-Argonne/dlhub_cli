import pytest
from click.testing import CliRunner
from dlhub_cli.commands.describe import describe_cmd

@pytest.fixture
def runner():
    return CliRunner()


def test_noargs(runner: CliRunner):
    result = runner.invoke(describe_cmd)
    assert result.exit_code > 0
    assert 'Missing argument' in result.output


def test_print(runner: CliRunner):
    result = runner.invoke(describe_cmd, ['loganw_globusid/1d_norm'])
    assert result.output.startswith('datacite')
    assert '1d_norm' in result.output

    # Test the model name being omitted
    result = runner.invoke(describe_cmd, ['loganw_globusid'])
    assert result.exit_code > 0
    assert 'Please enter name in the form' in result.output
