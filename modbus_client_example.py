#!/usr/bin/env python3
"""Pymodbus Synchronous Client Example.

An example of a single threaded synchronous client.

usage: client_sync.py [-h] [--comm {serial}]
                      [--framer {ascii,binary,rtu}]
                      [--log {critical,error,warning,info,debug}]
                      [--port PORT]
options:
  -h, --help            show this help message and exit
  --comm {serial}
                        "serial"
  --framer {ascii,binary,rtu}
                        "ascii", "binary", "rtu"
  --log {critical,error,warning,info,debug}
                        "critical", "error", "warning", "info" or "debug"
  --port PORT           the port to use

The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import argparse
import os
import logging

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.client import (
    ModbusSerialClient,
)
from pymodbus.transaction import (
    ModbusAsciiFramer,
    ModbusBinaryFramer,
    ModbusRtuFramer,
)


def setup_sync_client(args=None):
    """Run client setup."""
    if not args:
        args = get_commandline()
    _logger.info("### Create client object")
    if args.comm == "serial":
        client = ModbusSerialClient(
            port=args.port,  # serial port
            # Common optional paramers:
            #    framer=ModbusRtuFramer,
            timeout=3,
            #    retries=3,
            #    retry_on_empty=False,
            #    close_comm_on_error=False,.
            #    strict=True,
            # Serial setup parameters
            baudrate=9600,
            bytesize=8,
            # parity="N",
            stopbits=1,
            #    handle_local_echo=False,
        )
    return client


def run_sync_client(client, modbus_calls=None):
    """Run sync client."""
    _logger.info("### Client starting")
    client.connect()
    commands_to_send(client)
    if modbus_calls:
        modbus_calls(client)
    client.close()
    _logger.info("### End of Program")

def commands_to_send(client: ModbusSerialClient):
    # client.write_coil(address=20, value=True)
    # result = client.read_coils(1,1)
    # print(result)
    # client.write_coil(1, False)
    # result = client.read_coils(1,1)
    # print(result)
    result = client.read_holding_registers(0, 10)
    print(result)


# --------------------------------------------------------------------------- #
# Extra code, to allow commandline parameters instead of changing the code
# --------------------------------------------------------------------------- #
FORMAT = "%(asctime)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()


def get_commandline():
    """Read and validate command line arguments"""
    parser = argparse.ArgumentParser(
        description="Connect/disconnect a synchronous client."
    )
    parser.add_argument(
        "--comm",
        choices=["serial"],
        help='"serial"',
        type=str,
    )
    parser.add_argument(
        "--framer",
        choices=["ascii", "binary", "rtu"],
        help='"ascii", "binary", "rtu"',
        type=str,
    )
    parser.add_argument(
        "--log",
        choices=["critical", "error", "warning", "info", "debug"],
        help='"critical", "error", "warning", "info" or "debug"',
        type=str,
    )
    parser.add_argument(
        "--port",
        help="the port to use",
        type=str,
    )
    args = parser.parse_args()

    # set defaults
    comm_defaults = {
        "serial": ["rtu", "/dev/tnt1"],
    }
    framers = {
        "ascii": ModbusAsciiFramer,
        "binary": ModbusBinaryFramer,
        "rtu": ModbusRtuFramer,
    }
    _logger.setLevel(args.log.upper() if args.log else logging.INFO)
    if not args.comm:
        args.comm = "serial"
    if not args.framer:
        args.framer = comm_defaults[args.comm][0]
    args.port = args.port or comm_defaults[args.comm][1]
    args.framer = framers[args.framer]
    return args


if __name__ == "__main__":
    # Connect/disconnect no calls.
    testclient = setup_sync_client()
    run_sync_client(testclient)
