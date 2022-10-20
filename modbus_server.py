#!/usr/bin/env python3
"""Pymodbus Synchronous Server

                      [--log {critical,error,warning,info,debug}]
                      [--port PORT]
                      [--store {sequential,sparse,factory,none}]
                      [--slaves SLAVES]
"""
import argparse
import os
import logging

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification

from pymodbus.server import StartSerialServer
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.version import version

from definitions import CONFIG_PATH
from simulation_config import load_config, ServerParameters

def setup_sync_server(config: ServerParameters):
    """Run server setup."""
    _logger.info("### Create datastore")
    if config.store == "sequential":
        datablock = ModbusSequentialDataBlock(0x00, [17] * 100)
    elif config.store == "sparse":
        datablock = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
    elif config.store == "factory":
        datablock = ModbusSequentialDataBlock.create()

    if config.slaves:
        context = {
            0x01: ModbusSlaveContext(
                di=datablock,
                co=datablock,
                hr=datablock,
                ir=datablock,
            ),
            0x02: ModbusSlaveContext(
                di=datablock,
                co=datablock,
                hr=datablock,
                ir=datablock,
            ),
            0x03: ModbusSlaveContext(
                di=datablock, co=datablock, hr=datablock, ir=datablock, zero_mode=True
            ),
        }
        single = False
    else:
        context = ModbusSlaveContext(
            di=datablock,
            co=datablock,
            hr=datablock,
            ir=datablock,
        )
        single = True

    # Build data storage
    return ModbusServerContext(slaves=context, single=single)


def run_sync_server():
    """Run server."""
    config = load_config(CONFIG_PATH).server
    _logger.setLevel(config.log_level.upper() if config.log_level else logging.INFO)

    store = setup_sync_server(config)
    txt = f"### start server, listening on {config.port} - serial"
    _logger.info(txt)

    server = StartSerialServer(
        context=store,  # Data storage
        # identity=identity,  # server identify
        framer= ModbusRtuFramer,  # The framer strategy to use
        port=config.port,  # serial port
        timeout=config.timeout,  # waiting time for request to complete
        # custom_functions=[],  # allow custom handling
        # handler=None,  # handler for each session
        stopbits=config.stopbits,  # The number of stop bits to use
        bytesize=config.bytesize,  # The bytesize of the serial messages
        parity=config.parity,  # Which kind of parity to use
        baudrate=config.baudrate,  # The baud rate to use for the serial device
        handle_local_echo=config.handle_local_echo,  # Handle local echo of the USB-to-RS485 adaptor
        ignore_missing_slaves=config.ignore_missing_slaves,  # ignore request to a missing slave
        broadcast_enable=config.broadcast_enable,  # treat unit_id 0 as broadcast address,
        strict=config.strict,  # use strict timing, t1.5 for Modbus RTU
        defer_start=config.defer_start,  # Only define server do not activate
        )
    return server


FORMAT = "%(asctime)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()


if __name__ == "__main__":
    server = run_sync_server()
    server.shutdown()
