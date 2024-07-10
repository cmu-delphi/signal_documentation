import importlib
from typing import Any


def split_class_name(class_name) -> tuple[str, Any]:
    """
    Splits a class name into module name and class name.
    """
    parts = class_name.split('.')
    module_name = '.'.join(parts[:-1])
    class_name = parts[-1]
    return module_name, class_name


def get_class_by_name(module_name, class_name) -> Any:
    """
    Returns a class by its name.
    """
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
