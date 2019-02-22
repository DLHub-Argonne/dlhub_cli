import pytest
from click.testing import CliRunner
from dlhub_cli.commands.search import search_cmd


@pytest.fixture()
def runner():
    return CliRunner()


def test_noargs(runner: CliRunner):
    result = runner.invoke(search_cmd)
    assert result.exit_code == 1
    assert 'No query' in result.output


def test_noresults(runner: CliRunner):
    result = runner.invoke(search_cmd, ["--owner", "totallynotauser_uchicago"])
    assert result.exit_code == 0
    assert "No results" in result.output


def test_all_models(runner: CliRunner):
    # Get only 1 version
    result = runner.invoke(search_cmd, ["--owner", "dlhub.test_gmail", "--name", "1d_norm"])
    assert result.exit_code == 0
    assert result.output.count('dlhub.test_gmail') == 1

    # Get all versions
    result = runner.invoke(search_cmd, ["--owner", "dlhub.test_gmail",
                                        "--name", "1d_norm", "--all"])
    assert result.exit_code == 0
    assert result.output.count('dlhub.test_gmail') > 1


def test_manual_query(runner: CliRunner):
    result = runner.invoke(search_cmd, ["dlhub.name:1d_norm", 'AND',
                                        "dlhub.owner:dlhub.test_gmail"])
    assert result.exit_code == 0
    assert result.output.count('1d_norm') == 1

    # Also add in a query term
    result = runner.invoke(search_cmd,
                           ["dlhub.name:1d_norm", 'AND', "dlhub.owner:dlhub.test_gmail",
                            "--domain", "chemistry"])
    assert result.exit_code == 0
    assert 'No results' in result.output
