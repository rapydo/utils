# -*- coding: utf-8 -*-

"""
Convert README file from Markdown to text
"""

from markdown import markdown
import html2text  # from `aaronsw` :(

MARKER = 'MARKER()()MARKER'


def fix_quotes(mdcontent):

    count = 0
    quote_state = False
    quote_char = '`'
    quote_string = ''
    new_string = ''
    quotes = []

    for char in mdcontent:

        is_quote = char == quote_char

        if quote_state and not is_quote:
            quote_string += char

        if is_quote:
            count += 1
        else:
            count = 0
            if not quote_state:
                new_string += char

        if count == 3:
            if quote_state:
                new_string += MARKER
                quotes.append(quote_string.split('\n')[1:])
                # for line in quote_string.split('\n')[1:]:
                #     if line.strip() != '':
                #         print("LINE *%s*" % line)
                #         new_string += '\t' + line + '\n'
                quote_state = False
            else:
                quote_state = True
                quote_string = ''

    return new_string, quotes


def fix_text(marked_text, quotes):

    new_string = ''
    quotes = quotes[::-1]

    for piece in marked_text.split(MARKER):
        new_string += piece
        try:
            quote = quotes.pop()
        except IndexError:
            pass
        else:
            for line in quote:
                if line.strip() != '':
                    # print("LINE *%s*" % line)
                    new_string += '\t' + line + '\n'

    return new_string


def convert_markdown_file(input_file):
    # input_file = 'README.md'
    output_file = input_file.split('.')[0]

    with open(input_file, 'r') as rhandler:

        # markdown
        mdcontent = rhandler.read()
        marked_content, quotes = fix_quotes(mdcontent)
        # HTML
        html = markdown(marked_content)
        # text
        marked_text = html2text.html2text(html)
        text = fix_text(marked_text, quotes)

        with open(output_file, 'w') as whandler:
            whandler.write(text)
