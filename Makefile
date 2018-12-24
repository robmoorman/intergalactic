.PHONY: tests

default: install

install:
	pip3 install -r requirements.txt
	pip3 install -e .[test]

test:
	py.test tests
