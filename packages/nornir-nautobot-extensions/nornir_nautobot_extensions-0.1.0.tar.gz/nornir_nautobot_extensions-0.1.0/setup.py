#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Glenn Akester",
    author_email='glennake.1@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Nornir Nautobot Extensions",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nornir_nautobot_extensions',
    name='nornir_nautobot_extensions',
    packages=find_packages(include=['nornir_nautobot_extensions', 'nornir_nautobot_extensions.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/glennake/nornir_nautobot_extensions',
    version='0.1.0',
    zip_safe=False,
)
