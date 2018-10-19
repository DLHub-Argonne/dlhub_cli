from dlhub_cli.parsing.click_wrappers import dlhub_group


def main_func(f):
    """
    Wrap root command func in common opts and make it a command group

    :param f:
    :return:
    """
    f = dlhub_group('dlhub-client',
                     help='CLI Client to the DLHub API')(f)
    return f