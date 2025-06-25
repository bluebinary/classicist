import sys, os
import pytest

path = os.path.join(os.path.dirname(__file__), "..", "source")

sys.path.insert(0, path)  # add 'classicist' library path for importing into the tests

import classicist


# Override the default alpha sort of the test modules, into the order we wish to test
TEST_MODULE_ORDER = [
    "test_hybridmethod",
    "test_classproperty",
]


def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test modules run in the given order."""

    module_mapping = {item: item.module.__name__ for item in items}

    sorted_items = items.copy()

    # Iteratively move tests of each module to the end of the test queue
    for module in TEST_MODULE_ORDER:
        sorted_items = [it for it in sorted_items if module_mapping[it] != module] + [
            it for it in sorted_items if module_mapping[it] == module
        ]

    items[:] = sorted_items
