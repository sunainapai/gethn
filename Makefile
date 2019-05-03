# Set up development environment.

venv: FORCE
	rm -rf ~/.venv/myhn venv
	python3 -m venv ~/.venv/myhn
	echo . ~/.venv/myhn/bin/activate > venv

deps: FORCE
	touch venv
	. ./venv && pip install -r requirements.txt


# Check.

lint: FORCE
	. ./venv && isort --diff --quiet
	. ./venv && pylama

test: FORCE
	. ./venv && python -m unittest -v

coverage: FORCE
	. ./venv && coverage run --branch -m unittest -v
	. ./venv && coverage report --show-missing
	. ./venv && coverage html

checks: lint test coverage dist



# Package.

dist: clean
	. ./venv && python setup.py sdist bdist_wheel

test-upload: dist
	. ./venv && twine upload \
	    --repository-url https://test.pypi.org/legacy/ dist/*

upload: dist
	. ./venv && twine upload dist/*

test-venv: FORCE
	rm -rf ~/.venv/testmyhn testvenv
	python -m venv ~/.venv/testmyhn
	echo . ~/.venv/testmyhn/bin/activate > testvenv


# Verify package.

verify-test-wheel: test-venv
	. ./testvenv && pip install myhn \
	    --index-url https://test.pypi.org/simple/
	. ./testvenv && python -m myhn --version

verify-test-sdist: test-venv
	. ./testvenv && pip install myhn \
	    --index-url https://test.pypi.org/simple/ --no-binary :all:
	. ./testvenv && python -m myhn --version

verify-wheel: test-venv
	. ./testvenv && pip install myhn
	. ./testvenv && python -m myhn --version

verify-sdist: test-venv
	. ./testvenv && pip install --no-binary :all: myhn
	. ./testvenv && python -m myhn --version

verify-test-upload: verify-test-wheel verify-test-sdist

verify-upload: verify-wheel verify-sdist


# Clean up.

clean: FORCE
	rm -rf *.pyc __pycache__
	rm -rf build dist myhn.egg-info 
	rm -rf .coverage htmlcov

FORCE:
