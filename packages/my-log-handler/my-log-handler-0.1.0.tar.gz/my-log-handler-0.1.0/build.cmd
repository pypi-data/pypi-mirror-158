echo "Starting to create wheel"
python setup.py bdist_wheel sdist

echo "Installing local package"
pip install -e .[dev]

echo "Running tox"
tox

@REM check-manifest --create