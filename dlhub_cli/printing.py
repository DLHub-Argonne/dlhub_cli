"""Functions related to cleaner printing of the outputs"""

import six
import sys
import json


def safeprint(s):
    """Catch print errors.

    Args:
        s (string): String to print.
    """
    try:
        print(s)
        sys.stdout.flush()
    except IOError:
        pass


def format_output(dataobject):
    """Use safe print to make sure jobs are correctly printed.

    Args:
        dataobject (string): String to print.
    """
    if isinstance(dataobject, six.string_types):
        safeprint(dataobject)
    else:
        safeprint(json.dumps(dataobject, indent=2, separators=(',', ': ')))
