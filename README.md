# Packet Sender
Layer 2 packet constructor and sender using Python

## Tested Enviroment
- CLI: Ubuntu 20.04 WSL, Python 3.8.5
- GUI: Ubuntu Desktop 20.04 inside VMware, Python 3.8.5

## Used Libraries
- builtin [`socket`](https://docs.python.org/3/library/socket.html) library
- [`netifaces`](https://pypi.org/project/netifaces/)
- [`PySide2`](https://doc.qt.io/qtforpython-5/)

## How-to
1. Clone this repo: `git clone https://github.com/nickchen120235/packet-sender.git`
2. (Strongly recommended) Install requirements inside a virtual environment
```sh
nick@nick:~/packet-sender$ sudo pip3 install virtualenv
nick@nick:~/packet-sender$ virtualenv venv
nick@nick:~/packet-sender$ source ./venv/bin/activate
(venv) nick@nick:~/packet-sender$ pip3 install PySide2 netifaces
(venv) nick@nick:~/packet-sender$ deactivate
```
3. Run `./main.py` (`sudo` is required for raw socket): `sudo ./venv/bin/python3 ./main.py`

## File Structure
- `./main.py`: Main script
- `./ICMPexample.py`: Example script of library usage
- `./lib`: Backend
  - `./lib/packet.py`: Packet class
  - `./lib/helper.py`: Unpacker class, constant, helper function
- `./views`: QT frontend
  - `./widgets/info`: Information groupbox
  - `./widgets/*.py`: Different views of different protocols