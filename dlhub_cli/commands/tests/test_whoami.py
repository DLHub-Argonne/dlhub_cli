import os
import pytest
from click.testing import CliRunner
from dlhub_cli.commands.whoami import whoami_cmd

# Check if we are on travis
#  See: https://blog.travis-ci.com/august-2012-upcoming-ci-environment-updates
is_travis = 'HAS_JOSH_K_SEAL_OF_APPROVAL' in os.environ


@pytest.mark.skipif(not is_travis, reason='Only runs with credentials on Travis CI')
def test_whoami():
    runner = CliRunner()
    res = runner.invoke(whoami_cmd)
    assert res.exit_code == 0
    assert 'dlhub.test_gmail' in res.output
