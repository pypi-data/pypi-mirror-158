import setuptools
from pathlib import Path
setuptools.setup(name='Highest common factor', version='1.0.1', long_description=Path("README.md").read_text(),
                 packages=setuptools.find_packages(exclude=['tests', 'data']), url='https://pypi.org/')
