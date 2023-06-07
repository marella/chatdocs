from typing import Any, Dict

from deepmerge import always_merger


def merge(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, Any]:
    c = {}
    always_merger.merge(c, a)
    always_merger.merge(c, b)
    return c
