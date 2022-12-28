from asyncore import read
from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Restocks.net client for Python'

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


setup(
    name="restocks-client",
    version=VERSION,
    author="banjo",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4", "lxml"],
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["python", "client"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)