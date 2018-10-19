import six
import sys
import json


def safeprint(s):
    """
    Catch print errors.

    :param s:
    :return:
    """
    try:
        print(s)
        sys.stdout.flush()
    except IOError:
        pass


def format_output(dataobject):
    """
    Use safe print to make sure jobs are correctly printed.

    :param dataobject:
    :return:
    """
    if isinstance(dataobject, six.string_types):
        safeprint(dataobject)
    else:
        safeprint(json.dumps(dataobject, indent=2, separators=(',', ': ')))