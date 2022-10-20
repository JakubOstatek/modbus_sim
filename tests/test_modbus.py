import pytest
import logging

from modbus_simulator import modbus_client
from pymodbus.client import ModbusSerialClient


log = logging.getLogger(__name__)

def test_of_tests():
    assert True == True

@pytest.fixture(scope="session")
def client() -> ModbusSerialClient:
    return modbus_client.setup_sync_client()

@pytest.fixture(scope="function")
def connection(client):
    client.connect()
    log.info("Connected to server")
    yield
    client.close()
    log.info("Disconnected from server")


def test_request_read_register(client, connection):
    # Write register requests - no response needed
    for i in range(1, 50):
        client.write_register(i, 0)

    # Read holding registers request
    response = client.read_holding_registers(0, 101)
    print(response)
    
