import yaml
from pathlib import Path

CONFIG_PATH = Path("DataModifying/config/config.yaml")


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


CONFIG = load_config()

