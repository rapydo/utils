# -*- coding: utf-8 -*-

import pytest
from utilities.meta import Meta


def test():
    meta = Meta()
    cls_name = "Meta"

    import utilities

    modules = meta.get_submodules_from_package(utilities)
    assert "meta" in modules

    sub_modules = meta.import_submodules_from_package("utilities")
    assert sub_modules is not None
    assert isinstance(sub_modules, list)
    assert len(sub_modules) > 0

    module = Meta.get_module_from_string("utilities.meta")
    assert module is not None
    assert hasattr(module, cls_name)

    classes = meta.get_classes_from_module(module)
    assert classes is not None
    assert isinstance(classes, dict)
    assert cls_name in classes
    assert classes[cls_name].__name__ == cls_name

    new_classes = meta.get_new_classes_from_module(module)
    assert new_classes is not None
    assert isinstance(new_classes, dict)
    assert cls_name in new_classes
    assert new_classes[cls_name].__name__ == cls_name

    meta_class = meta.get_class_from_string(cls_name, module)
    assert meta_class is not None
    assert meta_class.__name__ == cls_name

    methods = meta.get_methods_inside_instance(meta, private_methods=True)
    assert methods is not None
    assert isinstance(methods, dict)
    # both are static methods
    assert "get_methods_inside_instance" not in methods
    assert "get_authentication_module" not in methods

    metacls = meta.metaclassing(Meta, "Test")
    assert metacls is not None
    assert metacls.__name__ == "Test"

    self_ref = meta.get_self_reference_from_args(meta, "test", 1)
    assert self_ref == meta

    # FIXME: abc is returned as self
    # self_ref = meta.get_self_reference_from_args("abc", meta, "test", 1)
    # assert self_ref == meta

    # FIXME: abc is returned as self, not None
    # self_ref = meta.get_self_reference_from_args("abc", "test", 1)
    # assert self_ref is None

    # FIXME: how to test these methods?
    # meta.models_module
    # meta.obj_from_models
    # meta.import_models
    # meta.get_authentication_module
    # meta.class_factory
    # Meta.get_celery_tasks_from_module


# def test_failures(capfd):
def test_failures():
    meta = Meta()

    try:
        meta.import_submodules_from_package("utilities_bla")
    except AttributeError:
        pass
    else:
        pytest.fail("This call should fail and raise and AttributeError")

    try:
        meta.import_submodules_from_package("utilities_bla", exit_if_not_found=True)
    except AttributeError:
        pass
    else:
        pytest.fail("This call should fail and raise and AttributeError")

    try:
        meta.import_submodules_from_package(
            "utilities_bla", exit_if_not_found=True, exit_on_fail=True
        )
    except AttributeError:
        pass
    else:
        pytest.fail("This call should fail and raise and AttributeError")

    try:
        meta.import_submodules_from_package("utilities_bla", exit_on_fail=True)
    except AttributeError:
        pass
    else:
        pytest.fail("This call should fail and raise and AttributeError")

    module = Meta.get_module_from_string("utilities.metabla")
    assert module is None

    try:
        module = Meta.get_module_from_string(
            "utilities.metabla", exit_if_not_found=True
        )
    except SystemExit:
        pass
    else:
        pytest.fail("This call should fail and exit")

    try:
        module = Meta.get_module_from_string(
            "utilities.metabla", exit_if_not_found=True, exit_on_fail=True
        )
    except SystemExit:
        pass
    else:
        pytest.fail("This call should fail and exit")

    try:
        module = Meta.get_module_from_string(
            "utilities.metabla",
            exit_if_not_found=True,
            exit_on_fail=True,
            debug_on_fail=True,
        )
    except SystemExit:
        pass
    else:
        pytest.fail("This call should fail and exit")

    # FIXME: unable to test exit_on_fail... we need a moule with import errors?
    module = Meta.get_module_from_string("utilities.metabla", exit_on_fail=True)
    assert module is None

    module = Meta.get_module_from_string("utilities.metabla", debug_on_fail=True)
    assert module is None

    # _, err = capfd.readouterr()
    # err = err.split("\n")
    # err = [cut_log(x) for x in err]

    # assert "ImportError: No module named 'utilities.metabla'" in err
