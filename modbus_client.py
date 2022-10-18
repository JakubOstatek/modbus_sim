"""Script launch client which is able to send modbus packets through RS485"""
import argparse
import logging
import asyncio
import os

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer

def setup_async_client(args=None):
    """Run client setup"""
    if not args:
        args = get_commandline()
    if args.comm != "serial" and args.port:
        args.port = int(args.port)
    _logger.info("### Create client object")
    if args.comm == "serial":
        client = AsyncModbusSerialClient(args.port)
    return client

async def run_async_client(client, modbus_calls=None):
    """Run async client"""
    _logger.info("### Client starting")
    await client.connect()
    assert client.protocol
    if modbus_calls:
        await modbus_calls(client)
    await client.close()
    _logger.info("### End of program")

FORMAT = "%(asctime)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()

def get_commandline():
    """Read and validate command line arguments"""
    parser = argparse.ArgumentParser(
            description="Connect/disconnect a sunchronous client."
            )
    parser.add_argument(
            "--comm",
            choices=["serial"],
            type=str,
            )
    parser.add_argument(
            "--framer",
            choices=["rtu"]
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

    comm_defaults = {
            "serial": ["rtu", "/dev/tnt2"],
            }
    framers = {
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
    # Connect/disconnect no callsself.
    testclient = setup_async_client()
    asyncio.run(run_async_client(testclient), debug=True)
    coil = testclient.read_holding_registers(0x01,1,slave=1)# address, count, slave address
    print(coil)

