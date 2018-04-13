from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 6):
    raise Exception("This package requires Python 3.6 or higher.")


PACKAGE_NAME = "minisentry"
VERSION = "0.0.1"
QUICK_DESCRIPTION = "MiniSentry. Stripped Sentry replacement for development"
SOURCE_DIR_NAME = "src"


def readme():
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


test_requirements = [
    "isort",
    "flake8",
    "pytest",
    "pytest-cov",
]

develop_requirements = [
    "colorlog",
    "django-silk",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=QUICK_DESCRIPTION,
    author="Dmitry Litvinenko",
    author_email="anti1869@gmail.com",
    long_description=readme(),
    url="https://github.com/anti1869/minisentry/",
    package_dir={"": SOURCE_DIR_NAME},
    packages=find_packages(SOURCE_DIR_NAME, exclude=("*.tests",)),
    include_package_data=True,
    zip_safe=False,
    package_data={},
    license="Proprietary",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Bug Tracking",
        "Framework :: Django :: 2.0",
    ],
    install_requires=[
        "django >=2.0, <=2.1",
        "python-dotenv",
        "uwsgi",
    ],
    tests_require=test_requirements,
    extras_require={
        "develop": develop_requirements + test_requirements,
    },
    scripts=[
        "src/manage.py",
    ],
    entry_points={
        "console_scripts": [
            "minisentry = minisentry.__main__:main",
        ],
    }
)