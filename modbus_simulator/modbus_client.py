"""Pymodbus Synchronous Client"""

from modbus_simulator.config_loader import load_config
from modbus_simulator.definitions import CONFIG_PATH
from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer


def setup_sync_client() -> ModbusSerialClient:
    """Setup client(master) with config loaded from 'config.toml'"""
    config = load_config(CONFIG_PATH)

    client = ModbusSerialClient(
        framer=ModbusRtuFramer,
        port=config.port,
        baudrate=config.baudrate,
        bytesize=config.bytesize,
        parity=config.parity,
        stopbits=config.stopbits,
        timeout=config.timeout,
        handle_local_echo=config.handle_local_echo,
        strict=config.strict,
        retries=config.retries,
        retry_on_empty=config.retry_on_empty,
        close_comm_on_error=config.close_comm_on_error,
    )
    return client
