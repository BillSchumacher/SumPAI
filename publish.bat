rmdir dist /q /s
python -m build
python -m twine upload --repository pypi dist/*
python -m twine upload --repository testpypi dist/*