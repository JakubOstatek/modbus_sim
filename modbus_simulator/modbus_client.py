#!/usr/bin/env python3
"""Pymodbus Synchronous Client"""

import logging

from config_loader import load_config
from definitions import CONFIG_PATH
from pymodbus.client import ModbusSerialClient
from pymodbus.client.base import ModbusBaseClient
from pymodbus.transaction import ModbusRtuFramer


def setup_sync_client():
    """Run client setup."""
    config = load_config(CONFIG_PATH).client
    _logger.setLevel(
        config.common.log_level.upper() if config.common.log_level else logging.INFO
    )
    _logger.info("### Create client object")

    client = ModbusSerialClient(
        framer=ModbusRtuFramer,
        port=config.common.port,
        baudrate=config.common.baudrate,
        bytesize=config.common.bytesize,
        parity=config.common.parity,
        stopbits=config.common.stopbits,
        timeout=config.common.timeout,
        handle_local_echo=config.common.handle_local_echo,
        strict=config.common.strict,
        retries=config.retries,
        retry_on_empty=config.retry_on_empty,
        close_comm_on_error=config.close_comm_on_error,
    )
    return client


def run_sync_client(client, modbus_calls=False):
    """Run sync client."""
    _logger.info("### Client starting")
    client.connect()
    if modbus_calls:
        test_procedure(client)
    client.close()
    _logger.info("### End of Program")


def test_procedure(client: ModbusBaseClient):
    # Check memory with coil requests
    for i in range(1, 50):
        client.write_register(i, 0)
    # _logger.info(space)
    response = client.read_holding_registers(0, 99)
    print(response)
    # sleep(1)


FORMAT = "%(asctime)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()

if __name__ == "__main__":
    # Connect/disconnect no calls.
    testclient = setup_sync_client()
    run_sync_client(testclient, modbus_calls=True)
