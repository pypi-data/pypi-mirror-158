#!/usr/bin/env python

"""The setup script."""
import sys

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

sys.path.append("ta_bitwarden_cli")
sys.path.append("download_bitwarden")
from download_bitwarden import DownloadBitwarden  # noqa


class Download(build_py, DownloadBitwarden):
    def run(self):
        self.download_bitwarden()
        build_py.run(self)


with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = ["requests~=2.26.0", "retry~=0.9.2"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Bohdan Sukhov",
    author_email="bohdan.sukhov@thoughtfulautomation.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Thoughtful Automation BitWarden CLI installation package",
    entry_points={
        "console_scripts": [
            "ta_bitwarden_cli=ta_bitwarden_cli.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="ta_bitwarden_cli",
    name="ta_bitwarden_cli",
    packages=find_packages(include=["ta_bitwarden_cli", "ta_bitwarden_cli.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://www.thoughtfulautomation.com/",
    version="0.7.8",
    zip_safe=False,
    cmdclass={"build_py": Download},
)
