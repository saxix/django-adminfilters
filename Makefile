maVERSION=2.0.0
BUILDDIR=${PWD}/~build
BINDIR=${PWD}/~build/bin
export PYTHONPATH:=${PWD}/tests/:${PWD}/src
DJANGO?='1.7.x'


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z0-9_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("\033[93m%-10s\033[0m %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.mkbuilddir:
	@mkdir -p ${BUILDDIR}

lint:  ## code lint
	tox -e lint
	#pre-commit run --all-files

develop:  ## setup development env
	python3 -m venv ./.venv
	./.venv/bin/pip install -r src/requirements/testing.pip
	./.venv/bin/pip install -r src/requirements/develop.pip

demo:  ## run demo app
	cd tests/demoapp && python manage.py makemigrations demo
	cd tests/demoapp && python manage.py init_demo
	cd tests/demoapp && python manage.py runserver

clean:  ## clean development directory
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml pytest.xml .cache MANIFEST build .pytest_cache
	find . -name __pycache__ | xargs rm -rf
	find . -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf

fullclean:  ## clean development directory
	rm -fr .tox .cache
	rm -fr *.sqlite
	$(MAKE) clean

test:  ## run test
	 py.test src tests -vv --capture=no --doctest-modules --cov=adminfilters --cov-report=html --cov-config=tests/.coveragerc

docs: .mkbuilddir
	@sh docs/to_gif.sh docs/images
	@mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs ${BUILDDIR}/docs

bump:   ## Bumps version
	@while :; do \
		read -r -p "bumpversion [major/minor/release]: " PART; \
		case "$$PART" in \
			major|minor|release) break ;; \
  		esac \
	done ; \
	bumpversion --no-commit --allow-dirty $$PART
	@grep "^VERSION " src/adminfilters/__init__.py


heroku:
	@git checkout heroku
	@git merge develop -m "merge develop"
	@git push heroku heroku:master
	@git checkout develop
	@echo "check demo at https://django-adminfilters.herokuapp.com/"

heroku-reset: heroku
	heroku pg:reset --confirm django-adminfilters
	heroku config:set DEBUG=true
	heroku run python tests/demoapp/manage.py migrate
	heroku run python tests/demoapp/manage.py init_demo
	heroku run python tests/demoapp/manage.py collectstatic --noinput
