"""
Mostly copied from globus-cli and globus-search-cli
We want the niceties of parsing improvements worked out in that project.
"""
import warnings
import logging.config
import click


from dlhub_cli.version import __version__


class HiddenOption(click.Option):
    """
    HiddenOption -- absent from Help text.
    Supported in latest and greatest version of Click, but not old versions, so
    use generic 'cls=HiddenOption' to get the desired behavior.
    """

    def get_help_record(self, ctx):
        """
        Has "None" as its help record. All that's needed.

        :param ctx:
        :return:
        """
        return


class CommandState(object):
    def __init__(self):
        self.debug = False


def setup_logging(level="DEBUG"):
    """
    Configure the logger.

    :param level:
    :return:
    """
    conf = {
        'version': 1,
        'formatters': {
            'basic': {
                'format':
                    '[%(levelname)s] %(name)s::%(funcName)s() %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': level,
                'formatter': 'basic'
            }
        },
        'loggers': {
            'dlhub_cli': {
                'level': level,
                'handlers': ['console']
            }
        }
    }

    logging.config.dictConfig(conf)


def debug_option(f):
    """
    Enable debugging for commands.

    :param f:
    :return:
    """
    def callback(ctx, param, value):
        if not value or ctx.resilient_parsing:
            # turn off warnings altogether
            warnings.simplefilter('ignore')
            return

        warnings.simplefilter('default')
        state = ctx.ensure_object(CommandState)
        state.debug = True
        setup_logging(level="DEBUG")

    return click.option(
        '--debug', is_flag=True, cls=HiddenOption,
        expose_value=False, callback=callback, is_eager=True)(f)


def index_argument(f):
    """
    Click indexing for arguments.

    :param f:
    :return:
    """
    f = click.argument('INDEX_ID')(f)
    return f


def common_options(f):
    """
    Global/shared options decorator.

    :param f:
    :return:
    """
    f = click.help_option('-h', '--help')(f)
    f = click.version_option(__version__, '-v', '--version')(f)
    f = debug_option(f)

    return f


class DLHubCommandGroup(click.Group):
    """
    This is a click.Group with any customizations which we deem necessary
    *everywhere*.
    In particular, at present it provides a better form of handling for
    no_args_is_help. If that flag is set, helptext will be triggered not only
    off of cases where there are no arguments at all, but also cases where
    there are options, but no subcommand (positional arg) is given.
    """
    def invoke(self, ctx):
        # if no subcommand was given (but, potentially, flags were passed),
        # ctx.protected_args will be empty
        # improves upon the built-in detection given on click.Group by
        # no_args_is_help , since that treats options (without a subcommand) as
        # being arguments and blows up with a "Missing command" failure
        # for reference to the original version (as of 2017-02-26):
        # https://github.com/pallets/click/blob/02ea9ee7e864581258b4902d6e6c1264b0226b9f/click/core.py#L1039-L1052
        if self.no_args_is_help and not ctx.protected_args:
            click.echo(ctx.get_help())
            ctx.exit()
        try:
            return super(DLHubCommandGroup, self).invoke(ctx)
        except Exception as err:
            click.echo(err, err=True)
            click.get_current_context().exit(1)


def dlhub_group(*args, **kwargs):
    """
    Wrapper over click.group which sets GlobusCommandGroup as the Class

    :param args:
    :param kwargs:
    :return:
    """
    def inner_decorator(f):
        f = click.group(*args, cls=DLHubCommandGroup, **kwargs)(f)
        f = common_options(f)
        return f
    return inner_decorator


def dlhub_cmd(*args, **kwargs):
    """
    Wrapper over click.command which sets common opts

    :param args:
    :param kwargs:
    :return:
    """
    def inner_decorator(f):
        f = click.command(*args, **kwargs)(f)
        f = common_options(f)
        return f
    return inner_decorator
