import pytest

from click.testing import CliRunner

from dlhub_cli.commands.methods import methods_cmd


@pytest.fixture()
def runner():
    return CliRunner()


def test_long_args(runner: CliRunner):

    # Give No model name
    result = runner.invoke(methods_cmd)
    assert result.exit_code > 0
    assert 'Missing argument' in result.output

    # Leave off the model name
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail'])
    assert result.exit_code > 0
    assert 'Please enter name in the form' in result.output

    # Leave off the method name, should give all methods
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail/1d_norm'])
    assert result.exit_code == 0
    assert result.output.startswith('run')

    # Provide the method name
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail/1d_norm', 'run'])
    assert result.exit_code == 0
    assert result.output.startswith('input')

    # Provide a non-existant method name
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail/1d_norm', 'notamethod'])
    assert result.exit_code != 0
    assert 'No such method' in str(result.exception)


def test_short_args(runner: CliRunner):
    """Using the owner/model syntax"""
    # Leave off the model name
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail/'])
    assert result.exit_code > 0
    assert 'Please enter name in the form' in result.output

    # Leave off the method name, should give all methods
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail/1d_norm'])
    assert result.exit_code == 0
    assert result.output.startswith('run')

    # Provide the method name
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail/1d_norm', 'run'])
    assert result.exit_code == 0
    assert result.output.startswith('input')

    # Provide a non-existant method name
    result = runner.invoke(methods_cmd, ['dlhub.test_gmail/1d_norm', 'notamethod'])
    assert result.exit_code != 0
    assert 'No such method' in str(result.exception)
