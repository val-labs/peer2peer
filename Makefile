#xtest: realclean
#	tree .
test: clean .v2 .v3
	@echo ==AAAA
	PYTHONPATH=. .v2/bin/python peer2peer/dbc.py get qwert || echo SHOULD FAIL
	@echo ==BBBB
	PYTHONPATH=. .v2/bin/python peer2peer/dbc.py put qwert Makefile
	@echo ==CCCC
	PYTHONPATH=. .v2/bin/python peer2peer/dbc.py get qwert
clean:
	@echo ' * Cleaning . . . * '
	@find . -name '*.pyc' -o -name '*~' -o -name '*.pid' | xargs rm
.v2:
	virtualenv -p python2 .v2
	.v2/bin/python setup.py install
.v3:
	virtualenv -p python3 .v3
	.v3/bin/python setup.py install
realclean: clean
	rm -fr .v2 .v3 dist build *egg* db

