import importlib.util
import os
from typing import List, Type
from app.services.interfaces import BaseConnector

def load_plugins(plugin_dir: str) -> List[Type[BaseConnector]]:
    connectors = []
    if not os.path.isdir(plugin_dir):
        return connectors
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(plugin_dir, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseConnector) and attr is not BaseConnector:
                    connectors.append(attr)
    return connectors