# Modbus simulator

Simulator represent server and client programs.

It can connect with each other and simulate communications with modbus protocol.

Server represents entity of slaves with common datastore or separated for each slave.

Client represents master side that can initiate communication with slaves and send requests to them.

## Usage

Script `run_simulator` will run simulator with default configuration for serial port.
```bash
# Start with start modbus server:
run_simulator server
# then, in another terminal run:
run_simulator client
```

## HMMMMM
