import ast
import io
import re
from codecs import open
from os.path import dirname, join

from setuptools import find_packages, setup

"""
PyPI configuration module.

This is prepared for easing the generation of deployment files.
"""

__license__ = "MIT"

# Source package
_source_package = "ornitho/"

# Regular expression for the version
_version_re = re.compile(r"__version__\s+=\s+(.*)")


# Gets the long description from the readme
def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ).read()


# Gets the version for the source folder __init__.py file
with open(_source_package + "__init__.py", "rb", encoding="utf-8") as f:
    version_lib = f.read()
    search = _version_re.search(version_lib)
    if search is not None:
        version_lib = search.group(1)
    version_lib = str(ast.literal_eval(version_lib.rstrip()))


setup(
    name="ornitho",
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    version=version_lib,
    description="An ornitho API client",
    author="Dachverband Deutscher Avifaunisten e.V.",
    author_email="info@dda-web.de",
    license="MIT",
    url="https://github.com/dda-dev/ornitho-client-python",
    download_url="https://pypi.python.org/pypi/ornitho",
    keywords=[],
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=read("README.rst"),
    install_requires=["requests-oauthlib"],
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*,!=3.3.*, !=3.4.*, <4",
)
