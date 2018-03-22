virtualenv:
	virtualenv venv
	./venv/bin/pip install -r requirements.txt

develop: virtualenv

clean:
	rm -rf venv