## test packaging
- https://www.youtube.com/watch?v=wCGsLqHOT2I&list=PLlM3i4cwc8zD-sac6lBQvC_yre7d9tbkj
- https://packaging.python.org/en/latest/tutorials/packaging-projects/

## make a distribution file so that it can be installed via pip
- ```pip install --upgrade setuptools```
    - https://setuptools.pypa.io/en/latest/userguide/quickstart.html
- ``` pip install --upgrade build``` 
    - build is a tool which makes a distribution file (e.g., tar.gz or .whl) that can be uploaded to pyPI.
- create setup.py
    ```
    # https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html
    from setuptools import setup
    setup()
    ```
- create pyproject.tolm
    ```
    [build-system]
    requires = ["setuptools", "setuptools-scm"]
    build-backend = "setuptools.build_meta"
    
    [project]
    name = "hsoft"
    version = "0.0.2"
    description = "My package description"
    readme = "README.md"
    requires-python = ">=3.6"
    ```
- ```python -m build``` inside of my project folder
    this makes distribution file (e.g., tar.gz file and a .whl file) that can be uploaded to PyPI!

- pip install twine
- twine upload dist/*
- check at the PyPI
