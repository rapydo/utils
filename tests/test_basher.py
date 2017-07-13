from utilities.basher import BashCommands

import string
import random
import plumbum
import pytest


def randomString(len=16, prefix="TEST:"):
    """
        Create a random string to be used to build data for tests
    """
    if len > 500000:
        lis = list(string.ascii_lowercase)
        return ''.join(random.choice(lis) for _ in range(len))

    rand = random.SystemRandom()
    charset = string.ascii_uppercase + string.digits

    random_string = prefix
    for _ in range(len):
        random_string += rand.choice(charset)

    return random_string


def test():
    bash = BashCommands()

    output = "just_a_test"
    out = bash.execute_command("echo", output)
    assert out.strip() == output

    random_name = randomString()
    bash.create_empty(random_name)

    bash.remove(random_name)
    try:
        bash.remove(random_name)
    except plumbum.commands.processes.ProcessExecutionError:
        pass
    else:
        pytest.fail("This remove should fail, because was missing!")

    bash.create_directory(random_name)

    # try:
    #     bash.remove_directory(random_name)
    # except plumbum.commands.processes.ProcessExecutionError:
    #     pass
    # else:
    #     pytest.fail("This remove should fail, directory was missing!")
