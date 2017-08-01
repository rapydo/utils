
from utilities import checks


def test():
    out = checks.executable("blabla")
    assert out is None

    out = checks.executable("python")
    assert out is not None

    out = checks.package("blabla")
    assert out is None

    out = checks.package("logging")
    assert out is not None

    out = checks.import_package("blabla")
    assert out is None

    out = checks.import_package("logging")
    assert out is not None

    # How to check this??
    # TODO: use a context manager to block requests outgoing into this com
    checks.internet_connection_available()
