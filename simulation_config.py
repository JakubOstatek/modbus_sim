import logging

from dataclasses import dataclass

from pathlib import Path
from dacite.core import from_dict
from dacite.config import Config
import toml


log = logging.getLogger(__name__)

@dataclass
class ClientParameters:
    port: str
    baudrate: int
    bytesize: int
    parity: str
    stopbits: int
    handle_local_echo: bool
    timeout: int
    retries: int
    retry_on_empty: bool
    close_comm_on_error: bool
    strict: bool

@dataclass
class ServerParameters:
    pass

@dataclass
class ModbusSimulationConfig:
    log_level:str 
    client: ClientParameters
    server: ServerParameters

def load_config(config_path: Path) -> ModbusSimulationConfig:
    log.info("Loading config...")
    config = from_dict(
        data_class = ModbusSimulationConfig,
        data = toml.load(config_path),
        config = Config(cast=[Path]),
        )
    log.info("Loading config: SUCCESS")
    log.debug("Config:")
    log.debug(config)
    return config
