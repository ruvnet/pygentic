# app/__init__.py
import toml

def load_config(config_file: str = "connectors.toml"):
    with open(config_file, "r") as file:
        config = toml.load(file)
    return config

config = load_config()
