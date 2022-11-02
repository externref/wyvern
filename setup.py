# type: ignore

"""Install packages as defined in this file into the Python environment."""
from setuptools import find_packages, setup

VERSION: dict[str, str] = {}

with open("./wyvern/__init__.py") as fp:
    exec(fp.read(), VERSION)

with open("./README.md") as file:
    desc = file.read()

setup(
    name="wyvern",
    author="sarthhh",
    author_email="shiva02939@gmail.com",
    description="A flexible and easy to use Discord API wrapper for python 🚀.",
    long_description=desc,
    long_description_content_type="text/markdown",
    version=VERSION.get("__version__", "0.0.0"),
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        "aiohttp>=3.8.1",
        "attrs>=22.1.0",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)