# -*- encoding: utf-8 -*-
import os
import sys
from io import open

from setuptools import setup
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))
about = {}
packages = ["archibald"]


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count

            self.pytest_args = ["-n", str(cpu_count()), "--boxed"]
        except (ImportError, NotImplementedError):
            self.pytest_args = ["-n", "1", "--boxed"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open(
    os.path(here, "plugins", "__version__.py"), mode="r", encoding="utf-8"
) as f:
    exec(f.read(), about)

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

with open(
    os.path(here, "docs", "HISTORY.md"), mode="r", encoding="utf-8"
) as f:
    history = f.read()

with open(
    os.path(here, "requirements", "requirements.txt"),
    mode="r",
    encoding="utf-8",
) as f:
    requires = f.read().split("\n")

with open(
    os.path(here, "requirements", "requirements-test.txt"),
    mode="r",
    encoding="utf-8",
) as f:
    test_requirements = f.read().split("\n")

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    # os.system("twine upload dist/*) # commented until ready to publish
    sys.exit()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    # package_data={},
    package_dir={},
    include_package_data=True,
    python_requires=">2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=requires,
    license=about["__license__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python 2",
        "Programming Language :: Python 2.7",
        "Programming Language :: Python 3",
        "Programming Language :: Python 3.4",
        "Programming Language :: Python 3.5",
        "Programming Language :: Python 3.6",
        "Programming Language :: Python 3.7",
    ],
    cmdclass={"test": PyTest},
    tests_require=test_requirements,
)
