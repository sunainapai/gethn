venv: FORCE
	rm -rf ~/.venv/myhn venv
	python3 -m venv ~/.venv/myhn
	echo . ~/.venv/myhn/bin/activate > venv
	. ./venv && pip3 install -r requirements.txt

test: FORCE
	. ./venv && isort --diff --quiet
	. ./venv && pylama
	. ./venv && python3 -m unittest -v

coverage:
	. ./venv && coverage run --branch -m unittest -v
	. ./venv && coverage report --show-missing
	. ./venv && coverage html

dist: clean
	. ./venv && python3 setup.py sdist bdist_wheel

fakedist: clean
	. ./venv && python3 setup.py

upload: dist
	. ./venv && twine upload dist/*

test-upload: dist
	. ./venv && twine upload \
	    --repository-url https://test.pypi.org/legacy/ dist/*

verify-upload: verify-wheel verify-sdist

verify-test-upload: verify-test-wheel verify-test-sdist

test-venv: FORCE
	rm -rf ~/.venv/testmyhn testvenv
	python3 -m venv ~/.venv/testmyhn
	echo . ~/.venv/testmyhn/bin/activate > testvenv

verify-wheel: test-venv
	. ./testvenv && pip3 install myhn
	. ./testvenv && python3 -m myhn --version

verify-sdist: test-venv
	. ./testvenv && pip3 install --no-binary :all: myhn
	. ./testvenv && python3 -m myhn --version

verify-test-wheel: test-venv
	. ./testvenv && pip3 install myhn \
	    --index-url https://test.pypi.org/simple/
	. ./testvenv && python3 -m myhn --version

verify-test-sdist: test-venv
	. ./testvenv && pip3 install myhn \
	    --index-url https://test.pypi.org/simple/ --no-binary :all:
	. ./testvenv && python3 -m myhn --version

clean: FORCE
	rm -rf *.pyc __pycache__
	rm -rf build dist myhn.egg-info 
	rm -rf .coverage htmlcov

FORCE:
