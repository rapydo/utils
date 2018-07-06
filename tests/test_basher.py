# -*- coding: utf-8 -*-

from utilities.basher import BashCommands
from utilities.basher import file_os_owner_raw
from utilities.basher import file_os_owner
from utilities.basher import path_is_readable
from utilities.basher import path_is_writable
from utilities.basher import current_os_uid
from utilities.basher import current_os_user
from utilities.basher import detect_vargroup

from utilities.random import get_random_name
import plumbum
import pytest
import os


def test():
    bash = BashCommands()

    output = "just_a_test"
    out = bash.execute_command("echo", output)
    assert out.strip() == output

    random_name = get_random_name()
    random_name2 = get_random_name()
    bash.create_empty(random_name)

    bash.remove(random_name)
    try:
        bash.remove(random_name)
    except plumbum.commands.processes.ProcessExecutionError:
        pass
    else:
        pytest.fail("This remove should fail, because was missing!")

    bash.create_directory(random_name)

    bash.copy_folder(random_name, random_name2)

    bash.remove_directory(random_name)
    bash.remove_directory(random_name2)

    # try:
    #     bash.remove_directory(random_name)
    # except plumbum.commands.processes.ProcessExecutionError:
    #     pass
    # else:
    #     pytest.fail("This remove should fail, directory was missing!")


    assert file_os_owner_raw('/etc') == 0
    assert file_os_owner('/etc') == 'root'
    assert path_is_readable('/etc')
    assert not path_is_writable('/etc')

    home = os.getenv("HOME")

    assert file_os_owner_raw(home) == current_os_uid()
    assert file_os_owner(home) == current_os_user()

    assert path_is_readable(home)
    assert path_is_writable(home)

    assert not path_is_readable("/do/not/exists")
    assert not path_is_writable("/do/not/exists")

    v = detect_vargroup('SDVOJSDOFJSV')
    assert len(v) == 0
