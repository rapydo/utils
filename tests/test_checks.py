
from utilities.checks import check_executable
from utilities.checks import import_package
from utilities.checks import check_package
from utilities.checks import check_internet


def test():
    out = check_executable("blabla")
    assert out is None

    out = check_executable("python")
    assert out is not None

    out = check_package("blabla")
    assert out is None

    out = check_package("logging")
    assert out is not None

    out = import_package("blabla")
    assert out is None

    out = import_package("logging")
    assert out is not None

    # How to check this??
    check_internet()
