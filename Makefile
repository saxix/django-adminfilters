maVERSION=2.0.0
BUILDDIR=${PWD}/~build
BINDIR=${PWD}/~build/bin
export PYTHONPATH:=${PWD}/tests/:${PWD}/src
DJANGO?='1.7.x'

.mkbuilddir:
	mkdir -p ${BUILDDIR}

lint:
	flake8 src tests
	isort -rc src tests --check-only
	check-manifest


develop:
	python3 -m venv ./.venv
	./.venv/bin/pip install -r src/requirements/testing.pip
	./.venv/bin/pip install -r src/requirements/develop.pip

demo:
	cd tests/demo && python manage.py migrate
	cd tests/demo && python manage.py loaddata demoproject
	cd tests/demo && python manage.py runserver

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml pytest.xml .cache MANIFEST build .pytest_cache
	find . -name __pycache__ | xargs rm -rf
	find . -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf

fullclean:
	rm -fr .tox .cache
	rm -fr *.sqlite
	$(MAKE) clean

coverage:
	 py.test src tests -vv --capture=no --doctest-modules --cov=adminfilters --cov-report=html --cov-config=tests/.coveragerc

docs: mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/source ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif
