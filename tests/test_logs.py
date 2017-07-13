
from utilities.logs import get_logger
log = get_logger(__name__)


def test():
    # assert nextint(3) == 4
    log.very_verbose("testing")
    log.verbose("testing")
    log.debug("testing")
    log.info("testing")
    log.warning("testing")
    log.error("testing")
    log.checked_simple("testing")
    log.checked("testing")
    log.print_stack("testing")
    log.myprint("testing")
    log.pretty_print({"test": 123})
    log.fail_exit("testing")
    # log.critical_exit("testing")
