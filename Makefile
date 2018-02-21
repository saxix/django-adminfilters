VERSION=2.0.0
BUILDDIR=${PWD}/~build
BINDIR=${PWD}/~build/bin
PYTHONPATH:=${PWD}/tests/:${PWD}
DJANGO?='1.7.x'

.mkbuilddir:
	mkdir -p ${BUILDDIR}

develop:
	# pip install -e .[dev]
	pip install -r requirements/testing.pip
	pip install -r requirements/develop.pip

demo:
	cd src/tests/demo && python manage.py migrate
	cd src/tests/demo && python manage.py loaddata demoproject
	cd src/tests/demo && python manage.py runserver

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml pytest.xml .cache MANIFEST build .pytest_cache
	find . -name __pycache__ | xargs rm -rf
	find . -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf

qa:
	flake8 src tests
	isort -rc src tests --check-only
	check-manifest


fullclean:
	rm -fr .tox .cache
	rm -fr *.sqlite
	$(MAKE) clean


docs: mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/source ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif
