# -*- coding: utf-8 -*-

from utilities.logs import get_logger
log = get_logger(__name__)

try:
    from invoke import Program as InvokeProgram, Argument
except ImportError as e:
    log.exit("\nThis module requires an extra package:\n%s", e)


class App(InvokeProgram):
    """
    The invoke modified class:
    for a command line program/application in Python;

    To be included in a cookiecutter template in the future.
    """

    def __init__(self, version=None, namespace=None, extra_arguments=None):

        if extra_arguments is None:
            self.extra_args = []
        else:
            self.extra_args = extra_arguments

        self.extra_args.append(
            Argument(
                name='log-level',
                help="set the application log level"
            )
        )

        super(App, self).__init__(version=version, namespace=namespace)

    @staticmethod
    def setup_logger(name=None):
        if name is None:
            name = __name__
        from utilities import apiclient
        level = apiclient.check_cli_arg('log-level', get=True)
        return apiclient.setup_logger(name, level_name=level)

    def core_args(self):
        core_args = super(App, self).core_args()
        return core_args + self.extra_args

    def print_help(self):
        """
        Hacking the code base, src:
        https://github.com/pyinvoke/invoke/blob/master/invoke/program.py
        """

        # USAGE
        usage_suffix = "task1 [--task1-opts] ... taskN [--taskN-opts]"
        if self.namespace is not None:
            # usage_suffix = "<subcommand> [--subcommand-opts] ..."
            usage_suffix = "<command> [--command-opts] ..."
        # print(
        #     "Usage: {0} [--core-opts] {1}"
        #     .format(self.binary, usage_suffix))
        print("Usage: {0} {1}".format(self.binary, usage_suffix))
        print("")

        print("Core options:")
        print("")

        helps = [arg.help for arg in self.extra_args]
        tuples = []
        for mytuple in self.initial_context.help_tuples():
            if mytuple[1] in helps:
                tuples.append(mytuple)
        self.print_columns(tuples)

        if self.namespace is not None:
            self.list_tasks()
