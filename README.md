# cron_parser

Parses a crontab entry and displays the times it would run at.
Example:
```
python3 -m cron_parser "1,2-3,*/5 0 1,15 * 1,4-6 \"/bin/bash /path/to/script.sh\""
```
Would print the following:
```
minute        0 1 2 3 5 10 15 20 25 30 35 40 45 50 55
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 4 5 6
command       "/bin/bash /path/to/script.sh"
```

# Prerequisites

The following prerequisites are required to build the wheels for cron_parser:
```
apt-get install python3-pip python3-venv
pip3 install build
```

# Building wheel & Installation
In cron_parser's directory:
```
make install_wheel
```
This would build a wheel file and install it, if you want to build the wheel only, use `make wheel` and find the `.whl` file in `dist/` folder.

You can then use it from anywhere on your system using:
```
python3 -m cron_parser "* * * * * /command/to/run"
```

# Running without installation
In cron_parser's directory, run:
```
python3 -m cron_parser "1,2-3,*/5 0 1,15 * 1,4-6 \"/bin/bash /path/to/script.sh\""
```

# Tests
A test suite is provided that tests functionality for various inputs, use:
```
make test
```
