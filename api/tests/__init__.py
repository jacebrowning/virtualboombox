import json
import logging

import expecter

log = logging.getLogger(__name__)


def contains_json(response, **kwargs):
    __tracebackhide__ = True

    data = response.json()
    missing = None
    for key, value in kwargs.items():
        if data.get(key) == value:
            continue
        elif not missing:
            missing = {key: value}

    if not missing:
        return True

    data_s = json.dumps(data, indent=4, sort_keys=True)
    missing_s = json.dumps(missing, indent=None, sort_keys=True)
    assert 0, (f"Expected:\n{data_s}\nto contain {missing_s}, but it didn't")


expecter.add_expectation(contains_json)
