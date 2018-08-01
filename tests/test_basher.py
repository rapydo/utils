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


class MyException(BaseException):
    pass


def test():
    bash = BashCommands()

    out = bash.execute_command("echo")
    assert out.strip() == ""

    output = "test_parameters"
    out = bash.execute_command("echo", output)
    assert out.strip() != output

    out = bash.execute_command("env")
    assert "MYSUPER_VAR=MYSUPER_VALUE" not in out.split('\n')

    out = bash.execute_command("env", env={"MYSUPER_VAR": "MYSUPER_VALUE"})
    assert "MYSUPER_VAR=MYSUPER_VALUE" in out.split('\n')

    # try:
    #     bash.execute_command("ls", "/invalid/path")
    # except plumbum.commands.processes.ProcessExecutionError:
    #     pass
    # else:
    #     pytest.fail("This command should fail, because path is missing!")

    # try:
    #     bash.execute_command(
    #         "ls", "/invalid/path", customException=MyException)
    # except MyException:
    #     pass
    # else:
    #     pytest.fail("This command should fail, because path is missing!")

    # bash.execute_command("ls", "/invalid/path", catchException=True)

    random_name = get_random_name()
    random_name2 = get_random_name()
    bash.create_empty(random_name)
    bash.copy(random_name, random_name2)
    bash.remove(random_name2)

    with open(random_name, 'w') as f:
        f.write("TEST")

    bash.replace_in_file('TEST', 'REPLACED!', random_name)
    out = bash.execute_command("cat", random_name)
    assert out.strip() == 'REPLACED!'

    bash.remove(random_name)
    try:
        bash.remove(random_name)
    except plumbum.commands.processes.ProcessExecutionError:
        pass
    else:
        pytest.fail("This remove should fail, because was missing!")

    # the path do not exist, but no fail with force flag
    bash.remove(random_name, force=True)

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
