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

doc:
	@sphinx-build -c docs -b html -d docs/.doctrees docs html

install:
	@python -m pip install . --no-deps -vv
