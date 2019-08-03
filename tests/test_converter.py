import os
from utilities.converter import convert_markdown_file


def test():
    convert_markdown_file("README.md")

    # TODO: how to verify if the converted file is right?
    assert os.path.isfile("README")
