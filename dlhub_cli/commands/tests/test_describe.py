import pytest
from click.testing import CliRunner
from dlhub_cli.commands.describe import describe_cmd


@pytest.fixture
def runner():
    return CliRunner()


def test_noargs(runner: CliRunner):
    result = runner.invoke(describe_cmd)
    assert result.exit_code > 0
    assert 'Missing' in result.output


def test_print(runner: CliRunner):
    result = runner.invoke(describe_cmd, ['blaiszik_globusid', 'cherukara_phase'])
    assert result.output.startswith('datacite')
    assert 'Cherukara' in result.output


def test_single_arg(runner: CliRunner):
    result = runner.invoke(describe_cmd, ['blaiszik_globusid/cherukara_phase'])
    assert result.output.startswith('datacite')
    assert 'Cherukara' in result.output

    # Test the model name being omitted
    result = runner.invoke(describe_cmd, ['blaiszik_globusid'])
    assert result.exit_code > 0
    assert 'Model name missing' in result.output
