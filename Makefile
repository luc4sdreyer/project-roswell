virtualenv:
	python3 -m venv venv
	./venv/bin/pip3 install -r requirements.txt

develop: virtualenv

clean:
	rm -rf venv