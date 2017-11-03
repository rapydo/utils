# -*- coding: utf-8 -*-

from jinja2 import FileSystemLoader, Environment


# Simplify the usage of jinja2 templating.
# https://www.pydanny.com/jinja2-quick-load-function.html
def render(template_name, directory, **kwargs):

    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(**kwargs)
