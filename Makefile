# Makefile for Python AIS Gateway.
#
# Source:: https://github.com/ampledata/aisgw
# Author:: Daniel J. Grinkevich
# Copyright:: Copyright 2017 Daniel J. Grinkevich
# License:: GNU General Public License, Version 3
#


.DEFAULT_GOAL := all


all: develop

install_requirements:
	pip install -r requirements.txt

develop: remember
	python setup.py develop

install: remember
	python setup.py install

uninstall:
	pip uninstall -y aisgw

reinstall: uninstall install

remember:
	@echo
	@echo "Hello from the Makefile..."
	@echo "Don't forget to run: 'make install_requirements'"
	@echo

clean:
	@rm -rf *.egg* build dist *.py[oc] */*.py[co] cover doctest_pypi.cfg \
		nosetests.xml pylint.log output.xml flake8.log tests.log \
		test-result.xml htmlcov fab.log .coverage

publish:
	python setup.py register sdist upload

nosetests: remember
	python setup.py nosetests

pep8: remember
	flake8 --max-complexity 12 --exit-zero *.py aisgw/*.py tests/*.py

flake8: pep8

lint: remember
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		-r n *.py  --ignore-imports=y aisgw/*.py tests/*.py || exit 0

pylint: lint

coverage:
	coverage report -m

test: lint pep8 mypy nosetests

mypy:
	mypy --strict .

docker_install_requirements:
	docker_install_requirements.sh

docker_build:
	docker build --build-arg github_token=${GITHUB_TOKEN} .

checkmetadata:
	python setup.py check -s --metadata --restructuredtext
