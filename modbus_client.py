#!/usr/bin/env python3
"""Pymodbus Synchronous Client.
hardcode:   comm - serial
            framer - rtu
to choose:  log, port, transfer parameters eg. baudrate 

usage: client_sync.py [-h] 
                      [--log {critical,error,warning,info,debug}]
                      [--port PORT]
options:
  -h, --help            show this help message and exit
  --log {critical,error,warning,info,debug}
                        "critical", "error", "warning", "info" or "debug"
  --port PORT           the port to use
"""
import argparse
import logging

from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer

from pymodbus.client.base import ModbusBaseClient

from definitions import CONFIG_PATH
from simulation_config import load_config

def setup_sync_client():
    """Run client setup."""
    config = load_config(CONFIG_PATH).client
    _logger.setLevel(config.log_level.upper() if config.log_level else logging.INFO)
    _logger.info("### Create client object")
    client = ModbusSerialClient(
        framer=ModbusRtuFramer,
        port=config.port,
        timeout=config.timeout,
        retries=config.retries,
        retry_on_empty=config.retry_on_empty,
        close_comm_on_error=config.close_comm_on_error,
        strict=config.strict,
        # Serial setup parameters
        baudrate=config.baudrate,
        bytesize=config.bytesize,
        parity=config.parity,
        stopbits=config.stopbits,
        handle_local_echo=config.handle_local_echo,
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


def test_procedure(client : ModbusBaseClient):
    space = "----------------------------------------------"
    # Check memory with coil requests
    for i in range(1,50):
        client.write_register(i, 0)
    # _logger.info(space)
    response = client.read_holding_registers(0,99)
    print(response)
    # sleep(1)


FORMAT = "%(asctime)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()

if __name__ == "__main__":
    # Connect/disconnect no calls.
    testclient = setup_sync_client()
    run_sync_client(testclient, modbus_calls=True)
