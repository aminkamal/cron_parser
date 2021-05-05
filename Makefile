.PHONY = all wheel install_wheel test coverage

all: wheel

install:
	pip3 install .

wheel:
	python3 -m build

install_wheel: wheel
	pip3 install dist/cron_parser*.whl

test:
	python3 -m unittest
