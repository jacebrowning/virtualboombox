import logging

import expecter

import log


def contains_html(response, text):
    __tracebackhide__ = True  # pylint: disable=unused-variable

    html = response.content.decode('utf-8')
    # TODO: make this a regular expression to check word boundaries
    if text in html:
        return True

    assert 0, (f"Expected:\n{html}\nto contain {text!r}, but it didn't")


expecter.add_expectation(contains_html)
