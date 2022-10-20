import logging

from dataclasses import dataclass

from pathlib import Path
from dacite.core import from_dict
from dacite.config import Config
import toml


log = logging.getLogger(__name__)

@dataclass
class ClientParameters:
    log_level:str 
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
    log_level: str
    port: str
    store: str
    slaves: int
    timeout: float  # waiting time for request to complete
    stopbits: int  # The number of stop bits to use
    bytesize: int  # The bytesize of the serial messages
    parity: str  # Which kind of parity to use
    baudrate: int  # The baud rate to use for the serial device
    handle_local_echo: bool  # Handle local echo of the USB-to-RS485 adaptor
    ignore_missing_slaves: bool  # ignore request to a missing slave
    broadcast_enable: bool  # treat unit_id 0 as broadcast address,
    strict: bool  # use strict timing, t1.5 for Modbus RTU
    defer_start: bool  # Only define server do not activate

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
