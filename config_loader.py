import logging

from dataclasses import dataclass

from pathlib import Path
from dacite.core import from_dict
from dacite.config import Config
import toml


log = logging.getLogger(__name__)

@dataclass
class CommonParameters:
    log_level:str 
    port: str
    baudrate: int
    bytesize: int
    parity: str
    stopbits: int
    timeout: float 
    handle_local_echo: bool
    strict: bool

@dataclass
class ClientParameters:
    common: CommonParameters
    retries: int
    retry_on_empty: bool
    close_comm_on_error: bool

@dataclass
class ServerParameters:
    common: CommonParameters
    store: str
    slaves: int
    ignore_missing_slaves: bool
    broadcast_enable: bool
    defer_start: bool 

@dataclass
class ModbusSimulationConfig:
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
