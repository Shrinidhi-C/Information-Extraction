init:
	pip install --user --ignore-installed -r requirements.txt

test:
	nosetests --nocapture tests
