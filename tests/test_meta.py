
from utilities.meta import Meta


def test():
    meta = Meta()

    module = meta.get_module_from_string("utilities.meta")

    assert module is not None

    assert hasattr(module, "Meta")
