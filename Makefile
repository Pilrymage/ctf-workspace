venv:
	uv venv
	
generate: challenges.csv
	python setup.py
	