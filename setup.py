# type: ignore
from setuptools import setup, find_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("./asuka/__init__.py") as fp:
    exec(fp.read(), VERSION)

    setup(
        name="asuk",
        author="sarth",
        author_email="shiva02939@gmail.com",
        description="A statically typed Discord API wrapper .",
        version=VERSION.get("__version__", "0.0.0"),
        packages=find_packages(where=".", exclude=["tests"]),
        install_requires=[
            "setuptools>=45.0",
            "aiohttp>=3.8",
        ],
        classifiers=[
            "Development Status :: 1 - Planning",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Typing :: Typed",
        ],
    )
