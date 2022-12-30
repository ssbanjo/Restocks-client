from setuptools import setup, find_packages
import os

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "restocks", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)
    
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    description=about["__description__"],
    license=about["__license__"],
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4", "lxml"],
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