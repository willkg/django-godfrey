# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from setuptools import setup, find_packages

from godfrey import __version__


setup(
    name='django-godfrey',
    version=__version__,
    description='Utilities for making API experience better',
    long_description=open('README.rst').read(),
    author='Will Kahn-Greene',
    author_email='willkg@mozilla.com',
    url='http://github.com/willkg/django-godfrey',
    license='Mozilla Public License v2',
    packages=find_packages(),
    include_package_data=True,
    package_data = {'': ['README.rst']},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ]
)
