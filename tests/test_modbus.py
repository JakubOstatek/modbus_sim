import logging

import pytest
from pymodbus.client import ModbusSerialClient

from modbus_simulator import modbus_client

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def client() -> ModbusSerialClient:
    """Setups client for tests session"""
    return modbus_client.setup_sync_client()


@pytest.fixture(scope="function")
def connection(client):
    """Attempt to connect with the slave at the start.
    Then assert if connection was established correctly.
    Finally close connection at the end of test case that use this fixture"""
    assert client.connect() == True
    log.info("Connected to serial port")
    yield
    if client.socket:
        client.close()
        log.info("Closed serial connection")
    else:
        log.info(
            "Probably connection closed with unknown reason during execute of the test logic"
        )


def test():
    return True
