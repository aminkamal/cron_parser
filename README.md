# cron_parser (Experimental)

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

# Running without installation (Linux, mac, Windows)
In cron_parser's directory, run:
```
python3 -m cron_parser "1,2-3,*/5 0 1,15 * 1,4-6 \"/bin/bash /path/to/script.sh\""
```

# Tests
A test suite is provided that tests functionality for various inputs, use:
```
make test
```

# Building & installing wheel

This is only required if you plan to run `python3 -m cron_parser` from anywhere on the system (if installed outside of a virtual env)
For **Linux**, the following prerequisites are required to build the wheel:
```
apt-get install python3-pip python3-venv
pip3 install pip --upgrade
pip3 install build
```

For **mac**, the wheel was built successfully using a Python build provided by homebrew (3.9):
```
brew install python@3.9
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install build
```

In cron_parser's directory:
```
make install_wheel
```
This would build a wheel file and install it, if you want to build the wheel only, use `make wheel` and find the `.whl` file in `dist/` folder.

You can then use it from anywhere on your system using (or within the virtual env it was installed to):
```
python3 -m cron_parser "* * * * * /command/to/run"
```
