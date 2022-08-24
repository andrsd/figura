SRC=figura

all:
	@echo ""

init:
	@pip install -e .
	@pip install -r requirements/devel.txt

syntax-check check-syntax:
	@flake8 $(SRC) tests

test:
	@pytest .

coverage:
	@coverage run --source=$(SRC) -m pytest
	@coverage html
