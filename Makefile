clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

prepare:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements/dev.txt

test:
	. venv/bin/activate && pytest

run_server:
	. venv/bin/activate && python app/app.py