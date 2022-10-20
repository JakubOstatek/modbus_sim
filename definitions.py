import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = Path(os.path.join(ROOT_DIR, "config.toml"))
