#!/usr/bin/env python3

from setuptools import setup, find_packages
import io
import django_serve


with io.open("README.md", "rt", encoding="utf-8") as fp:
    long_description = fp.read()


setup(
    packages=find_packages(),
    include_package_data=True,
    name="django-serve",
    version=django_serve.__version__,
    description="A gunicorn based django runserver command.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=django_serve.__author__,
    author_email=django_serve.__email__,
    url="https://bitbucket.org/rsalmaso/django-serve",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: JavaScript",
    ],
    install_requires=["gunicorn", "inotify"],
    zip_safe=False,
)
