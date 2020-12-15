# Packet Sender <!-- omit in toc -->
Layer 2 packet constructor and sender using Python
## Table of Contents <!-- omit in toc -->
- [Environment](#environment)
- [Used Library](#used-library)
- [Run Directly](#run-directly)
- [Build Executable](#build-executable)
- [Folder Structure](#folder-structure)
- [API Reference](#api-reference)
- [Program Usage](#program-usage)

## Environment
- Ubuntu Desktop 20.04 with linux kernel `5.4.0-58-generic`
- Python 3.8.5

## Used Library
- builtin [`socket`](https://docs.python.org/3/library/socket.html) library
- [`netifaces`](https://pypi.org/project/netifaces/): get local IP and MAC address
- [`PySide2`](https://doc.qt.io/qtforpython-5/): official python library of Qt

## Run Directly
1. Install requirements inside a virtual environment
```sh
nick@nick:~/packet-sender$ sudo pip3 install virtualenv
nick@nick:~/packet-sender$ virtualenv venv
nick@nick:~/packet-sender$ source ./venv/bin/activate
(venv) nick@nick:~/packet-sender$ pip3 install PySide2 netifaces
(venv) nick@nick:~/packet-sender$ deactivate
```
2. Run `./main.py` with `sudo` using `./venv/bin/python3`: `sudo ./venv/bin/python3 ./main.py`

## Build Executable
1. Install [`pyinstaller`](https://pyinstaller.readthedocs.io/en/stable/index.html): `sudo pip3 install pyinstaller`
2. Run `pyinstall --onefile ./main.py`
3. Run `./main` with `sudo`: `sudo ./main`

## Folder Structure
- `./main.py`: Program entrance
- `./ICMPexample.py`: Example of library usage
- `./lib`: Self-defined libraries
  - `./lib/packet.py`: Packet factory classes of different protocols
  - `./lib/helper.py`: Packet unpack class, constants, helper functions
- `./views`: Qt frontend
  - `./views/*.py`: Views of different protocols
  - `./views/widgets/info.*.py`: Visualization of unpacked data

## API Reference
See `./docs/api` for library usage

## Program Usage
See `./docs/program` for program usage
