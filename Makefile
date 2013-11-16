all:
	@./pyRabbitHoleChat.py

clean:
	rm -rf build dist pyRabbitHoleChat.egg-info

sdist:
	python setup.py sdist

testinstall:
	rm -rf /tmp/bla
	mkdir -p /tmp/bla
	python setup.py install --root /tmp/bla/ --prefix /usr

win32:
	@python27 setup.py py2exe
