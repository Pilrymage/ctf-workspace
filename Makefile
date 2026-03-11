install:
	uv venv && uv pip install .
	pixi install

generate: challenges.csv
	python setup.py
	
test:
	pixi run pytest ctf_lib/tests/test_crypto.py