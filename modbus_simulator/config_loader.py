import logging
from dataclasses import dataclass
from pathlib import Path

import toml
from dacite.config import Config
from dacite.core import from_dict

log = logging.getLogger(__name__)


@dataclass
class ModbusClientConfig:
    port: str
    baudrate: int
    bytesize: int
    parity: str
    stopbits: int
    timeout: float
    handle_local_echo: bool
    strict: bool
    retries: int
    retry_on_empty: bool
    close_comm_on_error: bool


def load_config(config_path: Path) -> ModbusClientConfig:
    log.info("Loading config...")
    config = from_dict(
        data_class=ModbusClientConfig,
        data=toml.load(config_path),
        config=Config(cast=[Path]),
    )
    log.info("Loading config: SUCCESS")
    log.debug("Config:")
    log.debug(config)
    return config
